// Netlify serves individual blob reads with strong consistency, but key
// listings lag behind writes and two function instances can disagree about
// what exists. These tests run the handler against a store whose listing is
// deliberately stale, which is what broke images during a live game.
import test from 'node:test';
import assert from 'node:assert/strict';
import { promises as fs } from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { handle } from '../lib/handler.mjs';
import { createDiskStore } from '../lib/store-disk.mjs';

const PNG = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==';

// A store that can be told to stop noticing new keys, the way a lagging
// listing does. Reads of a known key still work, exactly like Netlify.
function laggyStore(inner) {
  let frozen = null;
  return {
    get: inner.get,
    set: inner.set,
    delete: inner.delete,
    list: async (prefix) => (frozen === null
      ? inner.list(prefix)
      : frozen.filter((k) => k.startsWith(prefix))),
    freeze: async () => { frozen = await inner.list(''); },
    thaw: () => { frozen = null; }
  };
}

async function setup() {
  const dir = await fs.mkdtemp(path.join(os.tmpdir(), 'c4k-lag-'));
  const store = laggyStore(createDiskStore(dir));
  const login = await handle({ method: 'POST', path: '/api/host/login', query: {}, body: { passphrase: 'lagging' }, headers: {} }, store);
  return { store, token: JSON.parse(login.body).token };
}

const call = (store, method, path, body, token, query) => handle({
  method, path, query: query || {}, body: body || null,
  headers: token ? { 'x-host-token': token } : {}
}, store);

const upload = async (store, token, owner) => JSON.parse(
  (await call(store, 'POST', '/api/host/upload', { owner, data: PNG, mime: 'image/png' }, token)).body
).id;

test('a screenshot uploaded while the listing lags is still served', async () => {
  const { store, token } = await setup();
  const first = await upload(store, token, 'Carla');
  await call(store, 'POST', '/api/host/action', { action: 'start' }, token);

  // From here the listing stops seeing anything new, as it does on Netlify
  // for a second or two after a write.
  await store.freeze();
  const second = await upload(store, token, 'Carla');
  const third = await upload(store, token, 'Carla');

  const view = JSON.parse((await call(store, 'GET', '/api/state')).body);
  assert.deepEqual(view.shotIds, [first, second, third], 'the slide must carry all three');

  for (const id of [first, second, third]) {
    const res = await call(store, 'GET', '/api/image/' + id);
    assert.equal(res.status, 200, 'image ' + id + ' must serve while the listing lags');
  }
  store.thaw();
});

test('the running order does not shift when the listing lags mid game', async () => {
  const { store, token } = await setup();
  await upload(store, token, 'Carla');
  await upload(store, token, 'Noel');
  await call(store, 'POST', '/api/host/order', { order: ['Carla', 'Noel'] }, token);
  await call(store, 'POST', '/api/host/action', { action: 'start' }, token);

  const before = JSON.parse((await call(store, 'GET', '/api/host/state', null, token)).body);
  assert.equal(before.subject, 'Carla');
  assert.equal(before.totalRounds, 2);

  // A listing that has lost sight of Carla's screenshot must not renumber the
  // rounds and hand the wrong person's slide to everybody.
  await store.freeze();
  const stale = laggyStore(store);
  await stale.freeze();
  const during = JSON.parse((await call(store, 'GET', '/api/host/state', null, token)).body);
  assert.equal(during.subject, 'Carla');
  assert.equal(during.totalRounds, 2);
  store.thaw();
});

test('a screenshot still refuses to serve when it belongs to a later slide', async () => {
  const { store, token } = await setup();
  await upload(store, token, 'Carla');
  const noelShot = await upload(store, token, 'Noel');
  await call(store, 'POST', '/api/host/order', { order: ['Carla', 'Noel'] }, token);
  await call(store, 'POST', '/api/host/action', { action: 'start' }, token);
  const res = await call(store, 'GET', '/api/image/' + noelShot);
  assert.equal(res.status, 404, 'the fix must not open up screenshots from later rounds');
});
