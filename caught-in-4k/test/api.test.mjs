import test from 'node:test';
import assert from 'node:assert/strict';
import { promises as fs } from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { startServer } from '../dev-server.mjs';

const PNG = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==';

let server;
let host = '';

async function fresh() {
  if (server) await server.close();
  const dir = await fs.mkdtemp(path.join(os.tmpdir(), 'c4k-'));
  server = await startServer({ dataDir: dir });
  host = '';
  return server;
}

function call(method, route, body, headers) {
  const base = { 'content-type': 'application/json' };
  if (host) base['x-host-token'] = host;
  return fetch(server.url + route, {
    method,
    headers: Object.assign(base, headers || {}),
    body: body ? JSON.stringify(body) : undefined
  });
}
const asJson = async (pending) => {
  const res = await pending;
  return { status: res.status, body: await res.json() };
};

async function login(pass) {
  const res = await asJson(call('POST', '/api/host/login', { passphrase: pass }));
  host = res.body.token;
  return res;
}
const upload = (owner) => asJson(call('POST', '/api/host/upload', { owner, data: PNG, mime: 'image/png' }));
const act = (action, extra) => asJson(call('POST', '/api/host/action', Object.assign({ action }, extra || {})));
const join = (name) => asJson(call('POST', '/api/join', { name }, { 'content-type': 'application/json' }));
const hostState = () => asJson(call('GET', '/api/host/state'));
const playerState = (name, token) => asJson(
  fetch(server.url + '/api/state?name=' + name + '&token=' + token)
);

test.after(async () => { if (server) await server.close(); });

test('the first visitor sets the passphrase and a wrong one is refused', async () => {
  await fresh();
  const first = await login('let me in');
  assert.equal(first.status, 200);
  assert.equal(first.body.created, true);
  const wrong = await asJson(call('POST', '/api/host/login', { passphrase: 'nope' }, { 'content-type': 'application/json' }));
  assert.equal(wrong.status, 401);
  const again = await login('let me in');
  assert.equal(again.body.created, false);
});

test('host routes refuse an unknown token', async () => {
  const res = await asJson(call('GET', '/api/host/state', null, { 'x-host-token': 'rubbish' }));
  assert.equal(res.status, 401);
});

test('an upload with no name against it is refused', async () => {
  const res = await asJson(call('POST', '/api/host/upload', { owner: '', data: PNG }));
  assert.equal(res.status, 400);
});

test('a whole game plays through with scoring settled on the server', async () => {
  await fresh();
  await login('let me in');
  for (let i = 0; i < 3; i += 1) await upload('Carla');
  await upload('Noel');
  await asJson(call('POST', '/api/host/order', { order: ['Carla', 'Noel'] }));

  let s = await hostState();
  assert.equal(s.body.totalRounds, 2);
  assert.deepEqual(s.body.slides.map((x) => x.owner), ['Carla', 'Noel']);
  assert.equal(s.body.slides[0].count, 3);

  const players = {};
  for (const name of ['Kasia', 'Carla', 'Ivan', 'Chels', 'Ana', 'Andjela', 'Noel', 'Sara']) {
    const res = await join(name);
    assert.equal(res.status, 200);
    players[name] = res.body.token;
  }
  const dup = await join('Ivan');
  assert.equal(dup.status, 409);

  // Nothing can be voted on before the game starts.
  const early = await asJson(call('POST', '/api/vote', { name: 'Ivan', token: players.Ivan, guess: 'Carla' }, { 'content-type': 'application/json' }));
  assert.equal(early.status, 409);

  // Starting the game puts the first slide up with voting already open.
  assert.equal((await act('start')).status, 200);
  assert.equal((await hostState()).body.phase, 'voting');

  // Nothing in a player payload gives away that this is Carla's slide.
  let pv = await playerState('Ivan', players.Ivan);
  assert.equal(pv.body.round, 1);
  assert.equal(pv.body.shotCount, 3);
  assert.equal(pv.body.youAreSubject, false);
  assert.equal(pv.body.reveal, null);
  assert.equal(JSON.stringify(pv.body).includes('subject'), false);

  const carla = await playerState('Carla', players.Carla);
  assert.equal(carla.body.youAreSubject, true);

  const vote = (name, guess) => asJson(call('POST', '/api/vote', { name, token: players[name], guess }, { 'content-type': 'application/json' }));
  assert.equal((await vote('Ivan', 'Carla')).status, 200);
  assert.equal((await vote('Sara', 'Carla')).status, 200);
  assert.equal((await vote('Kasia', 'Ana')).status, 200);
  // The person whose slide it is may not vote.
  assert.equal((await vote('Carla', 'Ana')).status, 403);
  // No second vote.
  const second = await vote('Ivan', 'Sara');
  assert.equal(second.status, 409);
  assert.equal(second.body.locked, true);
  // A stolen name does not work either.
  const forged = await asJson(call('POST', '/api/vote', { name: 'Noel', token: 'wrong', guess: 'Carla' }, { 'content-type': 'application/json' }));
  assert.equal(forged.status, 401);

  pv = await playerState('Ivan', players.Ivan);
  assert.equal(pv.body.voteCount, 3);
  assert.equal(pv.body.eligibleCount, 7);
  assert.equal(pv.body.youVoted, true);
  assert.equal(pv.body.yourGuess, 'Carla');

  await act('reveal');
  pv = await playerState('Ivan', players.Ivan);
  assert.equal(pv.body.reveal.owner, 'Carla');
  assert.equal(pv.body.reveal.caught, 2);
  assert.equal(pv.body.reveal.eligible, 7);
  const board = Object.fromEntries(pv.body.leaderboard.map((r) => [r.name, r.score]));
  assert.equal(board.Ivan, 1);
  assert.equal(board.Sara, 1);
  assert.equal(board.Kasia, 0);
  assert.equal(pv.body.leaderboard[0].rank, 1);

  await act('next');
  s = await hostState();
  assert.equal(s.body.subject, 'Noel');
  await act('open-voting');
  assert.equal((await vote('Noel', 'Carla')).status, 403);
  assert.equal((await vote('Ivan', 'Noel')).status, 200);
  await act('reveal');
  await act('next');
  pv = await playerState('Ivan', players.Ivan);
  assert.equal(pv.body.phase, 'finished');
  assert.deepEqual(pv.body.champions, ['Ivan']);
  assert.ok(pv.body.stats);
});

test('resetting a round clears the votes and every eligible player can vote again', async () => {
  await fresh();
  await login('again');
  await upload('Carla');
  const tokens = {};
  for (const name of ['Ivan', 'Sara', 'Kasia', 'Carla']) tokens[name] = (await join(name)).body.token;
  await act('start');
  await act('open-voting');
  const vote = (name, guess) => asJson(call('POST', '/api/vote', { name, token: tokens[name], guess }, { 'content-type': 'application/json' }));
  assert.equal((await vote('Ivan', 'Carla')).status, 200);
  assert.equal((await vote('Sara', 'Carla')).status, 200);
  await act('reveal');
  assert.equal((await hostState()).body.leaderboard.find((r) => r.name === 'Ivan').score, 1);

  await act('reset-round');
  const after = await hostState();
  assert.equal(after.body.voteCount, 0);
  assert.equal(after.body.leaderboard.find((r) => r.name === 'Ivan').score, 0);
  await act('open-voting');
  // Every eligible player gets their vote back, not just one of them.
  for (const name of ['Ivan', 'Sara', 'Kasia']) {
    assert.equal((await vote(name, 'Carla')).status, 200, name + ' should be able to vote again');
  }
  await act('reveal');
  const pv = await playerState('Kasia', tokens.Kasia);
  assert.equal(pv.body.reveal.caught, 3);
});

test('a screenshot from a later slide is a 404 for a player and fine for the host', async () => {
  await fresh();
  await login('images');
  const carlaShot = (await upload('Carla')).body.id;
  const noelShot = (await upload('Noel')).body.id;
  await asJson(call('POST', '/api/host/order', { order: ['Carla', 'Noel'] }));
  await act('start');

  const asPlayer = (id) => fetch(server.url + '/api/image/' + id);
  assert.equal((await asPlayer(carlaShot)).status, 200);
  assert.equal((await asPlayer(noelShot)).status, 404);
  assert.equal((await fetch(server.url + '/api/image/' + noelShot + '?host=' + host)).status, 200);

  await act('reveal');
  await act('next');
  // Carla is revealed, so her evidence stays fetchable while Noel is live.
  assert.equal((await asPlayer(carlaShot)).status, 200);
  assert.equal((await asPlayer(noelShot)).status, 200);
  assert.equal((await asPlayer('made-up-id')).status, 404);
});

test('a state poll with a matching signature returns a tiny unchanged reply', async () => {
  const first = await playerState('Ivan', 'nope');
  const again = await asJson(fetch(server.url + '/api/state?sig=' + first.body.sig));
  assert.equal(again.body.unchanged, true);
  assert.equal(Object.keys(again.body).length, 2);
});

test('deleting the game data resets the show but keeps the evidence', async () => {
  const before = (await hostState()).body.shots.length;
  assert.ok(before > 0);
  await asJson(call('POST', '/api/host/wipe', { what: 'game' }));
  const after = await hostState();
  assert.equal(after.body.shots.length, before);
  assert.equal(after.body.phase, 'lobby');
  assert.deepEqual(after.body.claims, []);
  await asJson(call('POST', '/api/host/wipe', { what: 'all' }));
  assert.equal((await hostState()).body.shots.length, 0);
});

test('the name appears by itself once everybody in the room has voted', async () => {
  await fresh();
  await login('all in');
  await upload('Carla');
  const names = ['Kasia', 'Carla', 'Ivan', 'Chels', 'Ana', 'Andjela', 'Noel', 'Sara'];
  const tokens = {};
  for (const name of names) tokens[name] = (await join(name)).body.token;
  // Starting a game opens voting straight away.
  await act('start');
  assert.equal((await hostState()).body.phase, 'voting');

  const vote = (name) => asJson(call('POST', '/api/vote', { name, token: tokens[name], guess: 'Carla' }, { 'content-type': 'application/json' }));
  const voters = names.filter((n) => n !== 'Carla');
  for (const name of voters.slice(0, voters.length - 1)) {
    const res = await vote(name);
    assert.equal(res.status, 200);
    assert.equal(res.body.revealed, false, 'nothing is revealed while somebody has not voted');
  }
  const last = await vote(voters[voters.length - 1]);
  assert.equal(last.body.revealed, true, 'the last vote reveals the name');

  const view = await playerState('Ivan', tokens.Ivan);
  assert.equal(view.body.phase, 'revealed');
  assert.equal(view.body.reveal.owner, 'Carla');
  assert.equal(view.body.reveal.caught, 7);
});

test('a missing player does not stop the host revealing by hand', async () => {
  await fresh();
  await login('absent');
  await upload('Noel');
  const tokens = {};
  for (const name of ['Ivan', 'Sara', 'Noel']) tokens[name] = (await join(name)).body.token;
  await act('start');
  const vote = (name) => asJson(call('POST', '/api/vote', { name, token: tokens[name], guess: 'Noel' }, { 'content-type': 'application/json' }));
  assert.equal((await vote('Ivan')).body.revealed, false);
  const last = await vote('Sara');
  assert.equal(last.body.revealed, true, 'only the people actually in the room have to vote');
});
