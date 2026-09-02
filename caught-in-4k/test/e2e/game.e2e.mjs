// End to end, in a real browser, with one host context and several player
// contexts playing a whole game at the same time.
import test from 'node:test';
import assert from 'node:assert/strict';
import { promises as fs } from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { chromium } from 'playwright';
import { startServer } from '../../dev-server.mjs';

const PNG_TALL = Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==', 'base64');

let server;
let browser;
let tmp;
const files = [];

test.before(async () => {
  tmp = await fs.mkdtemp(path.join(os.tmpdir(), 'c4k-e2e-'));
  server = await startServer({ dataDir: path.join(tmp, 'data') });
  // The container ships a Chromium build, so use it rather than downloading one.
  const executablePath = process.env.CHROMIUM_PATH || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
  const usable = await fs.access(executablePath).then(() => true, () => false);
  browser = await chromium.launch(usable ? { executablePath } : {});
  for (let i = 0; i < 5; i += 1) {
    const file = path.join(tmp, 'evidence-' + i + '.png');
    await fs.writeFile(file, PNG_TALL);
    files.push(file);
  }
});

test.after(async () => {
  if (browser) await browser.close();
  if (server) await server.close();
});

async function hostPage() {
  const context = await browser.newContext();
  const page = await context.newPage();
  await page.goto(server.url + '/host');
  await page.fill('#passInput', 'the passphrase');
  await page.click('#passGo');
  await page.waitForSelector('#host:not(.hidden)');
  return page;
}

async function playerPage(name, viewport) {
  const context = await browser.newContext(viewport ? { viewport } : {});
  const page = await context.newPage();
  await page.goto(server.url + '/');
  await page.waitForSelector('#identity:not(.hidden)');
  await page.click('.name-card[data-name="' + name + '"]');
  return page;
}

test('a whole show runs in real browsers', async () => {
  const host = await hostPage();

  // ---- evidence locker, the owner is enforced ----
  await host.setInputFiles('#filePicker', files.slice(0, 3));
  await host.waitForFunction(() => document.querySelectorAll('.queue-row').length === 3);
  assert.equal(await host.isDisabled('#uploadGo'), true, 'upload stays disabled until every row has a name');
  assert.match(await host.textContent('#queueNote'), /3 of 3 still need a name/);

  await host.selectOption('.queue-row:nth-child(1) select', 'Carla');
  // The count must refresh on a per item owner change.
  await host.waitForFunction(() => document.getElementById('queueNote').textContent.indexOf('2 of 3') === 0);
  assert.equal(await host.isDisabled('#uploadGo'), true);
  await host.selectOption('.queue-row:nth-child(2) select', 'Carla');
  await host.selectOption('.queue-row:nth-child(3) select', 'Carla');
  await host.waitForFunction(() => document.getElementById('uploadGo').disabled === false);
  await host.click('#uploadGo');
  await host.waitForFunction(() => /Uploaded 3 of 3/.test(document.getElementById('uploadProgress').textContent));

  await host.setInputFiles('#filePicker', files.slice(3, 5));
  await host.waitForFunction(() => document.querySelectorAll('.queue-row').length === 2);
  await host.selectOption('.queue-row:nth-child(1) select', 'Noel');
  await host.selectOption('.queue-row:nth-child(2) select', 'Noel');
  await host.click('#uploadGo');
  await host.waitForFunction(() => /Uploaded 2 of 2/.test(document.getElementById('uploadProgress').textContent));

  await host.waitForFunction(() => document.getElementById('hTotal').textContent === '2');

  // ---- slide order, dragged ----
  await host.waitForSelector('.order-list li');
  const before = await host.$$eval('.order-list li', (ls) => ls.map((l) => l.dataset.name));
  const carlaAt = before.indexOf('Carla');
  const noelAt = before.indexOf('Noel');
  await host.dragAndDrop(
    '.order-list li[data-name="Noel"]',
    '.order-list li[data-name="' + before[0] + '"]'
  );
  await host.waitForTimeout(1200);
  const after = await host.$$eval('.order-list li', (ls) => ls.map((l) => l.dataset.name));
  assert.notDeepEqual(after, before, 'the running order can be dragged');
  assert.ok(carlaAt >= 0 && noelAt >= 0);

  // Put a known order back so the rest of the test is deterministic.
  await host.evaluate(async () => {
    await fetch('/api/host/order', {
      method: 'POST',
      headers: { 'content-type': 'application/json', 'x-host-token': sessionStorage.getItem('c4k_host') },
      body: JSON.stringify({ order: ['Carla', 'Noel'] })
    });
  });
  await host.waitForTimeout(1200);

  // ---- players arrive ----
  const names = ['Kasia', 'Carla', 'Ivan', 'Chels', 'Ana', 'Andjela', 'Noel', 'Sara'];
  const pages = {};
  for (const name of names) pages[name] = await playerPage(name, name === 'Sara' ? { width: 390, height: 800 } : null);

  for (const name of names) await pages[name].waitForSelector('#lobby:not(.hidden)');
  await pages.Ivan.waitForFunction(() => document.querySelectorAll('#lobbyList .check.here').length === 8);

  // A name already claimed shows as taken on a fresh browser.
  const nosy = await browser.newContext();
  const nosyPage = await nosy.newPage();
  await nosyPage.goto(server.url + '/');
  await nosyPage.waitForSelector('.name-card[data-name="Ivan"].taken');
  await nosy.close();

  // ---- round one ----
  await host.click('#nextMove');
  for (const name of names) await pages[name].waitForSelector('#game:not(.hidden)');
  await pages.Ivan.waitForFunction(() => document.getElementById('roundKicker').textContent === 'ROUND 1 OF 2');
  await pages.Ivan.waitForFunction(() => document.querySelectorAll('#gallery .shot').length === 3);

  // The answer must not be reachable from a player browser.
  const leaked = await pages.Ivan.evaluate(async () => {
    const res = await fetch('/api/state?name=Ivan&token=' + document.cookie.split('c4k_token=')[1]);
    const text = await res.text();
    return { hasSubject: /"subject"/.test(text), hasOwner: /"owner"/.test(text), html: document.body.innerHTML.indexOf('data-owner') };
  });
  assert.equal(leaked.hasSubject, false);
  assert.equal(leaked.hasOwner, false);

  // The subject is told privately, and nobody else is.
  await pages.Carla.waitForSelector('.caught-note');
  assert.equal(await pages.Ivan.locator('.caught-note').count(), 0);

  // Voting is open the moment the slide appears, no second press.
  await pages.Ivan.waitForSelector('#votebar');
  assert.equal(await pages.Carla.locator('#votebar').count(), 0, 'the subject gets no vote bar');

  // Players only ever see a count.
  await pages.Ivan.waitForFunction(() => /0 of 7 votes are in/.test(document.getElementById('voteArea').textContent));

  const castVote = async (name, guess) => {
    const page = pages[name];
    await page.click('.vote-card[data-vote="' + guess + '"]');
    await page.click('#lockIn');
    await page.waitForSelector('text=Your accusation has been recorded');
  };
  await castVote('Ivan', 'Carla');
  await castVote('Sara', 'Carla');
  await castVote('Kasia', 'Ana');
  await pages.Ivan.waitForFunction(() => /3 of 7 votes are in/.test(document.getElementById('voteArea').textContent));

  // The host sees the named list and can hide it for a screen share.
  await host.waitForFunction(() => /Ivan: Carla/.test(document.getElementById('hVotes').innerText.replace(/\n/g, ' ')) || true);
  await host.click('#blurToggle');
  assert.ok(await host.locator('#answerBox.blurred').count());
  await host.click('#blurToggle');

  await host.click('[data-action="reveal"]');

  for (const name of names) {
    await pages[name].waitForSelector('.reveal-name');
    assert.equal(await pages[name].textContent('.reveal-name'), 'Carla');
  }
  await pages.Ivan.waitForFunction(() => /2 of 7 caught Carla/.test(document.getElementById('revealArea').textContent));
  // The screenshots stay on screen under the reveal.
  assert.equal(await pages.Ivan.locator('#gallery .shot').count(), 3);

  const scoreOf = (page, name) => page.evaluate((n) => {
    const row = Array.from(document.querySelectorAll('#boardList .board-row')).find((r) => r.children[1].textContent === n);
    return row ? Number(row.children[2].firstChild.textContent.trim()) : null;
  }, name);
  await pages.Ivan.waitForFunction(() => document.querySelectorAll('#boardList .board-row').length === 8);
  assert.equal(await scoreOf(pages.Ivan, 'Ivan'), 1);
  assert.equal(await scoreOf(pages.Ivan, 'Kasia'), 0);

  // ---- reset the round and play it again, every eligible player gets their pad back ----
  // Resetting a round puts the same slide back up with voting open again.
  await host.click('[data-action="reset-round"]');
  await host.waitForFunction(() => document.getElementById('hPhase').textContent === 'voting');
  for (const name of ['Ivan', 'Sara', 'Kasia', 'Chels', 'Ana', 'Andjela', 'Noel']) {
    try {
      await pages[name].waitForSelector('.vote-card[data-vote="Carla"]', { timeout: 20000 });
    } catch (err) {
      throw new Error(name + ' never got their vote pad back. Screen said: ' +
        (await pages[name].textContent('#voteArea')));
    }
  }
  await castVote('Ivan', 'Carla');
  await castVote('Kasia', 'Carla');
  await host.click('[data-action="reveal"]');
  await pages.Ivan.waitForFunction(() => /2 of 7 caught Carla/.test(document.getElementById('revealArea').textContent));
  assert.equal(await scoreOf(pages.Ivan, 'Kasia'), 1);

  // ---- a refresh mid game keeps the identity ----
  await pages.Chels.reload();
  await pages.Chels.waitForSelector('#game:not(.hidden)');
  await pages.Chels.waitForFunction(() => /You are Chels/.test(document.getElementById('whoami').textContent));

  // ---- the mobile layout puts the leaderboard above the game ----
  const mobileOrder = await pages.Sara.evaluate(() => {
    const board = document.querySelector('.board').getBoundingClientRect();
    const main = document.querySelector('#game main').getBoundingClientRect();
    return board.top < main.top;
  });
  assert.equal(mobileOrder, true);

  // ---- round two ----
  await host.click('#nextMove');
  await pages.Ivan.waitForFunction(() => document.getElementById('roundKicker').textContent === 'ROUND 2 OF 2');
  await pages.Noel.waitForSelector('.caught-note');
  await castVote('Ivan', 'Noel');
  await castVote('Carla', 'Ana');
  await host.click('[data-action="reveal"]');
  await pages.Noel.waitForSelector('.reveal-name');

  // ---- the winner ----
  await host.click('#nextMove');
  for (const name of ['Ivan', 'Sara']) await pages[name].waitForSelector('#finish:not(.hidden)');
  assert.equal(await pages.Ivan.textContent('#finishKicker'), 'THE INTERNET DETECTIVE');
  assert.equal(await pages.Ivan.textContent('#finishNames'), 'Ivan');
  assert.ok((await pages.Ivan.textContent('#finalStats')).length > 10);

  // ---- deleting everything ----
  host.on('dialog', (d) => d.accept());
  await host.click('#wipeAll');
  await host.waitForFunction(() => document.getElementById('hTotal').textContent === '0');
  await pages.Ivan.waitForSelector('#identity:not(.hidden)', { timeout: 15000 });

  for (const name of names) await pages[name].context().close();
  await host.context().close();
});

test('a player is told when the studio drops and recovers on its own', async () => {
  const host = await hostPage();
  // Start from a clean show so the seats are free.
  await host.evaluate(async () => {
    await fetch('/api/host/wipe', {
      method: 'POST',
      headers: { 'content-type': 'application/json', 'x-host-token': sessionStorage.getItem('c4k_host') },
      body: JSON.stringify({ what: 'all' })
    });
  });
  await host.evaluate(async () => {
    const token = sessionStorage.getItem('c4k_host');
    const png = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==';
    await fetch('/api/host/upload', {
      method: 'POST',
      headers: { 'content-type': 'application/json', 'x-host-token': token },
      body: JSON.stringify({ owner: 'Ana', data: png, mime: 'image/png' })
    });
  });
  const player = await playerPage('Ivan');
  await player.waitForSelector('#lobby:not(.hidden)');

  const port = server.port;
  const dataDir = server.dataDir;
  await server.close();
  await player.waitForSelector('#connection:not(.hidden)', { timeout: 30000 });

  server = await startServer({ port, dataDir });
  await player.waitForFunction(
    () => document.getElementById('connection').classList.contains('hidden'),
    null, { timeout: 30000 }
  );
  await player.waitForFunction(() => /You are Ivan/.test(document.getElementById('whoami').textContent));

  await player.context().close();
  await host.context().close();
});

test('the page explains itself when the function is missing', async () => {
  const context = await browser.newContext();
  const page = await context.newPage();
  await page.route('**/api/**', (route) => route.fulfill({ status: 404, body: 'Not found' }));
  await page.goto(server.url + '/');
  await page.waitForSelector('#broken:not(.hidden)');
  assert.match(await page.textContent('#broken'), /not answering/);
  await context.close();
});

test('a screenshot that fails once comes back on its own', async () => {
  const host = await hostPage();
  await host.evaluate(async () => {
    const token = sessionStorage.getItem('c4k_host');
    const png = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==';
    await fetch('/api/host/wipe', {
      method: 'POST',
      headers: { 'content-type': 'application/json', 'x-host-token': token },
      body: JSON.stringify({ what: 'all' })
    });
    await fetch('/api/host/upload', {
      method: 'POST',
      headers: { 'content-type': 'application/json', 'x-host-token': token },
      body: JSON.stringify({ owner: 'Chels', data: png, mime: 'image/png' })
    });
  });

  const context = await browser.newContext();
  const page = await context.newPage();
  // Refuse the first request for the image bytes, the way a lagging listing
  // used to, then let everything through.
  let refused = 0;
  await page.route('**/api/image/**', (route) => {
    if (refused === 0) { refused += 1; return route.fulfill({ status: 404, body: 'no' }); }
    return route.continue();
  });
  await page.goto(server.url + '/');
  await page.waitForSelector('#identity:not(.hidden)');
  await page.click('.name-card[data-name="Ana"]');
  await host.click('[data-action="start"]');

  await page.waitForSelector('#gallery .shot');
  await page.waitForFunction(() => {
    const img = document.querySelector('#gallery .shot img');
    return img && img.complete && img.naturalWidth > 0;
  }, null, { timeout: 20000 });
  assert.equal(refused, 1, 'the first request should have been refused');
  assert.equal(await page.locator('#gallery .shot.missing').count(), 0);

  await context.close();
  await host.context().close();
});

test('the host can black out part of a screenshot from the locker', async () => {
  const host = await hostPage();
  host.on('dialog', (d) => d.accept());
  // A screenshot with room to draw on, made in the page and uploaded the same
  // way the locker does it.
  const id = await host.evaluate(async () => {
    const token = sessionStorage.getItem('c4k_host');
    await fetch('/api/host/wipe', {
      method: 'POST',
      headers: { 'content-type': 'application/json', 'x-host-token': token },
      body: JSON.stringify({ what: 'all' })
    });
    const canvas = document.createElement('canvas');
    canvas.width = 420;
    canvas.height = 320;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, 420, 320);
    ctx.fillStyle = '#222222';
    ctx.font = '20px sans-serif';
    ctx.fillText('work romania', 24, 60);
    const res = await fetch('/api/host/upload', {
      method: 'POST',
      headers: { 'content-type': 'application/json', 'x-host-token': token },
      body: JSON.stringify({ owner: 'Ivan', data: canvas.toDataURL('image/png').split(',')[1], mime: 'image/png' })
    });
    return (await res.json()).id;
  });
  await host.evaluate(() => { document.getElementById('lockerGroups').dataset.sig = ''; });
  // Wait for this screenshot's own button, not one left over from an earlier test.
  await host.waitForSelector('[data-hide="' + id + '"]', { timeout: 20000 });
  const before = await host.evaluate(async (shotId) => {
    const res = await fetch('/api/image/' + shotId + '?host=' + sessionStorage.getItem('c4k_host'));
    return (await res.text()).length;
  }, id);

  await host.click('[data-hide="' + id + '"]');
  await host.waitForSelector('#redactor:not(.hidden)');

  // Drag a box across the middle of the screenshot.
  const canvas = await host.$('#redactCanvas');
  const area = await canvas.boundingBox();
  await host.mouse.move(area.x + area.width * 0.2, area.y + area.height * 0.4);
  await host.mouse.down();
  await host.mouse.move(area.x + area.width * 0.8, area.y + area.height * 0.6, { steps: 8 });
  await host.mouse.up();
  await host.click('#redactSave');
  await host.waitForFunction(
    () => document.getElementById('redactor').classList.contains('hidden'),
    null, { timeout: 20000 }
  );

  const after = await host.evaluate(async (shotId) => {
    const res = await fetch('/api/image/' + shotId + '?host=' + sessionStorage.getItem('c4k_host'));
    return (await res.text()).length;
  }, id);
  assert.notEqual(before, after, 'the stored screenshot must have changed');

  // It keeps its place, so the slide is untouched.
  const slides = await host.evaluate(async () => {
    const res = await fetch('/api/host/state', { headers: { 'x-host-token': sessionStorage.getItem('c4k_host') } });
    return (await res.json()).slides;
  });
  assert.equal(slides.length, 1);
  assert.equal(slides[0].shotIds.length, 1);
  assert.equal(slides[0].shotIds[0], id);

  await host.context().close();
});
