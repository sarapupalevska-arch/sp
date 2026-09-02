// All of the rules for the game live here. The same handler runs behind the
// Netlify Function in production and behind the local dev server in tests.
import {
  PLAYERS, emptyState, newId, hashPass, buildSlides, voteKey, parseVoteKeys,
  eligibleVoters, scoresFrom, leaderboard, winners, revealSummary, funStats, signature
} from './game.mjs';
import { buildPlayerView } from './player-view.mjs';

const MAX_IMAGE_BYTES = 4 * 1024 * 1024;

function json(status, body, headers) {
  return {
    status,
    headers: Object.assign({ 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' }, headers || {}),
    body: JSON.stringify(body)
  };
}

async function readState(store) {
  const raw = await store.get('state');
  if (!raw) return emptyState();
  try {
    return Object.assign(emptyState(), JSON.parse(raw));
  } catch {
    return emptyState();
  }
}

async function writeState(store, state) {
  await store.set('state', JSON.stringify(state));
}

async function readShots(store) {
  const keys = await store.list('shot:');
  const shots = [];
  for (const key of keys) {
    const raw = await store.get(key);
    if (!raw) continue;
    try {
      const shot = JSON.parse(raw);
      if (shot && PLAYERS.includes(shot.owner)) shots.push(shot);
    } catch { /* a half written blob is simply skipped */ }
  }
  return shots;
}

async function readVotes(store, subject, state) {
  if (!subject) return {};
  const stored = state.revealed[subject];
  if (stored && stored.votes) return stored.votes;
  const keys = await store.list('vote:' + subject + ':');
  return parseVoteKeys(keys, subject);
}

async function currentScores(store, state) {
  return scoresFrom(state.revealed);
}

async function hostConfig(store) {
  const raw = await store.get('config');
  if (!raw) return null;
  try { return JSON.parse(raw); } catch { return null; }
}

function isHost(config, token) {
  return Boolean(config && token && token === config.hash);
}

// Slides live in the state blob. Individual blob reads are strongly consistent
// on Netlify but key listings lag behind writes, so rebuilding the running order
// from a listing on every read means two requests a moment apart can disagree
// about which screenshots exist. Recompute only when the host changes something.
async function syncSlides(store, state) {
  const slides = buildSlides(state.order, await knownShots(store, state));
  state.slides = slides;
  await writeState(store, state);
  return slides;
}

function slidesOf(state) {
  return Array.isArray(state.slides) ? state.slides : [];
}

// A game state written before the running order was stored has no slides at
// all, which is not the same as having none. Build them once and keep them,
// so an upgrade in the middle of a live game cannot empty the show.
async function ensureSlides(store, state) {
  if (Array.isArray(state.slides)) return state.slides;
  state.slides = buildSlides(state.order, await knownShots(store, state));
  await writeState(store, state);
  return state.slides;
}

// What the stored running order remembers, as plain screenshot records.
function shotsFromState(state) {
  const out = [];
  for (const slide of slidesOf(state)) {
    slide.shotIds.forEach((id, i) => out.push({ id, owner: slide.owner, position: i }));
  }
  return out;
}

// The listing can only ever add to what is already known. Contents come from
// individual reads, which are strongly consistent, so a listed screenshot wins
// on owner and position, but a screenshot the listing has not caught up with
// is never dropped.
async function knownShots(store, state, changes) {
  const merged = new Map();
  for (const shot of shotsFromState(state)) merged.set(shot.id, shot);
  for (const shot of await readShots(store)) merged.set(shot.id, shot);
  if (changes && changes.add) merged.set(changes.add.id, changes.add);
  if (changes && changes.drop) merged.delete(changes.drop);
  return [...merged.values()];
}

function subjectOf(slides, state) {
  const slide = slides[state.roundIndex];
  return slide ? slide.owner : null;
}

function allowedShotIds(state, slides) {
  // A player may fetch an image only from the slide that is live right now or
  // from a slide that has already been revealed.
  const allowed = new Set();
  const live = slides[state.roundIndex];
  if (live && ['viewing', 'voting', 'closed', 'revealed'].includes(state.phase)) {
    for (const id of live.shotIds) allowed.add(id);
  }
  for (const slide of slides) {
    if (state.revealed[slide.owner]) for (const id of slide.shotIds) allowed.add(id);
  }
  return allowed;
}

export async function handle(req, store) {
  const { method, path, query, body, headers } = req;
  const token = (headers && headers['x-host-token']) || (query && query.host) || '';
  const route = path.replace(/^\/api/, '') || '/';

  // ---- health ----
  if (route === '/ping') return json(200, { ok: true });

  // ---- player identity ----
  if (route === '/join' && method === 'POST') {
    const name = body && body.name;
    if (!PLAYERS.includes(name)) return json(400, { error: 'Unknown name' });
    const existing = await store.get('claim:' + name);
    if (existing) {
      const claim = JSON.parse(existing);
      if (body.token && body.token === claim.token) return json(200, { name, token: claim.token });
      return json(409, { error: 'That name is already taken' });
    }
    const claimToken = newId();
    await store.set('claim:' + name, JSON.stringify({ token: claimToken }));
    const state = await readState(store);
    state.joined[name] = true;
    await writeState(store, state);
    return json(200, { name, token: claimToken });
  }

  if (route === '/claims' && method === 'GET') {
    const keys = await store.list('claim:');
    return json(200, { taken: keys.map((k) => k.slice('claim:'.length)) });
  }

  // ---- the player facing state ----
  if (route === '/state' && method === 'GET') {
    const state = await readState(store);
    const slides = await ensureSlides(store, state);
    const subject = subjectOf(slides, state);
    const votes = await readVotes(store, subject, state);
    const scores = await currentScores(store, state);
    let you = null;
    if (query.name && PLAYERS.includes(query.name)) {
      const claim = await store.get('claim:' + query.name);
      if (claim && JSON.parse(claim).token === query.token) you = query.name;
    }
    const view = buildPlayerView({ state, slides, votes, scores, you });
    if (query.sig && query.sig === view.sig) return json(200, { unchanged: true, sig: view.sig });
    return json(200, view);
  }

  // ---- voting ----
  if (route === '/vote' && method === 'POST') {
    const { name, token: voterToken, guess } = body || {};
    if (!PLAYERS.includes(name) || !PLAYERS.includes(guess)) return json(400, { error: 'Unknown name' });
    const claim = await store.get('claim:' + name);
    if (!claim || JSON.parse(claim).token !== voterToken) return json(401, { error: 'Not your name' });
    const state = await readState(store);
    if (state.phase !== 'voting') return json(409, { error: 'Voting is not open' });
    const slides = await ensureSlides(store, state);
    const subject = subjectOf(slides, state);
    if (!subject) return json(409, { error: 'No slide is live' });
    if (name === subject) return json(403, { error: 'You have been caught. You do not get to vote.' });
    const existing = await store.list('vote:' + subject + ':' + name + ':');
    if (existing.length > 0) return json(409, { error: 'You already locked it in', locked: true });
    // The whole vote lives in the key, so two people voting at the same instant
    // cannot overwrite each other.
    await store.set(voteKey(subject, name, guess), '1');
    return json(200, { ok: true, locked: true });
  }

  // ---- images ----
  if (route.startsWith('/image/') && method === 'GET') {
    const id = route.slice('/image/'.length);
    const state = await readState(store);
    const config = await hostConfig(store);
    if (!isHost(config, token)) {
      const allowed = allowedShotIds(state, await ensureSlides(store, state));
      if (!allowed.has(id)) return json(404, { error: 'Not found' });
    }
    const meta = await store.get('shot:' + id);
    if (!meta) return json(404, { error: 'Not found' });
    const data = await store.get('img:' + id);
    if (!data) return json(404, { error: 'Not found' });
    const parsed = JSON.parse(meta);
    return {
      status: 200,
      headers: {
        'content-type': parsed.mime || 'image/jpeg',
        'cache-control': 'private, max-age=300'
      },
      body: Buffer.from(data, 'base64'),
      isBinary: true
    };
  }

  // ---- host passphrase ----
  if (route === '/host/login' && method === 'POST') {
    const pass = (body && body.passphrase) || '';
    if (pass.length < 4) return json(400, { error: 'Use at least four characters' });
    let config = await hostConfig(store);
    if (!config) {
      const salt = newId();
      config = { salt, hash: hashPass(pass, salt) };
      await store.set('config', JSON.stringify(config));
      return json(200, { token: config.hash, created: true });
    }
    if (hashPass(pass, config.salt) !== config.hash) return json(401, { error: 'Wrong passphrase' });
    return json(200, { token: config.hash, created: false });
  }

  if (route === '/host/exists' && method === 'GET') {
    return json(200, { exists: Boolean(await hostConfig(store)) });
  }

  // ---- everything below is host only ----
  const config = await hostConfig(store);
  if (route.startsWith('/host/')) {
    if (!isHost(config, token)) return json(401, { error: 'Host only' });
  } else {
    return json(404, { error: 'No such route' });
  }

  if (route === '/host/state' && method === 'GET') {
    const state = await readState(store);
    const shots = await readShots(store);
    let slides = await ensureSlides(store, state);
    // Before a game starts, heal the stored running order against the locker,
    // so a listing that was lagging during an upload cannot leave a slide out.
    if (state.phase === 'lobby') {
      const fresh = buildSlides(state.order, await knownShots(store, state));
      if (JSON.stringify(fresh) !== JSON.stringify(slides)) {
        state.slides = fresh;
        await writeState(store, state);
        slides = fresh;
      }
    }
    const subject = subjectOf(slides, state);
    const votes = await readVotes(store, subject, state);
    const scores = scoresFrom(state.revealed);
    const claims = (await store.list('claim:')).map((k) => k.slice('claim:'.length));
    const payload = {
      phase: state.phase,
      order: state.order,
      roundIndex: state.roundIndex,
      round: subject ? state.roundIndex + 1 : 0,
      totalRounds: slides.length,
      subject,
      shotIds: slides[state.roundIndex] ? slides[state.roundIndex].shotIds : [],
      slides: slides.map((s) => ({ owner: s.owner, count: s.shotIds.length, shotIds: s.shotIds })),
      shots: shots.map((s) => ({ id: s.id, owner: s.owner, position: s.position })),
      votes,
      voteCount: Object.keys(votes).length,
      eligible: subject ? eligibleVoters(subject) : [],
      joined: state.joined,
      claims,
      leaderboard: leaderboard(scores),
      champions: winners(scores),
      revealedOwners: Object.keys(state.revealed),
      stats: state.phase === 'finished' ? funStats(state.revealed) : null,
      reveal: state.phase === 'revealed' && subject ? revealSummary(subject, votes) : null
    };
    payload.sig = signature(payload);
    if (query.sig && query.sig === payload.sig) return json(200, { unchanged: true, sig: payload.sig });
    return json(200, payload);
  }

  if (route === '/host/upload' && method === 'POST') {
    const { owner, data, mime } = body || {};
    if (!PLAYERS.includes(owner)) return json(400, { error: 'Every screenshot needs a name against it' });
    if (typeof data !== 'string' || data.length === 0) return json(400, { error: 'No image data' });
    const bytes = Buffer.from(data, 'base64');
    if (bytes.length > MAX_IMAGE_BYTES) return json(413, { error: 'That image is too large' });
    const state = await readState(store);
    // Counted from everything known, not just the listing. Counting a lagging
    // listing gives two screenshots uploaded moments apart the same position,
    // and then they show up in the wrong order.
    const known = await knownShots(store, state);
    const position = known.filter((s2) => s2.owner === owner).length;
    const id = newId();
    // No original filename is ever stored. A file called carla-searches.png
    // would give the whole game away.
    await store.set('img:' + id, bytes.toString('base64'));
    await store.set('shot:' + id, JSON.stringify({ id, owner, position, mime: mime || 'image/jpeg' }));
    // The listing will not carry the new key for a second or two, so it is
    // added by hand rather than waiting for it to turn up.
    state.slides = buildSlides(state.order, known.concat([{ id, owner, position }]));
    await writeState(store, state);
    return json(200, { id, owner, position });
  }

  if (route.startsWith('/host/shot/')) {
    const id = route.slice('/host/shot/'.length);
    const raw = await store.get('shot:' + id);
    if (!raw) return json(404, { error: 'No such screenshot' });
    const shot = JSON.parse(raw);
    if (method === 'DELETE') {
      await store.delete('shot:' + id);
      await store.delete('img:' + id);
      const state = await readState(store);
      state.slides = buildSlides(state.order, await knownShots(store, state, { drop: id }));
      await writeState(store, state);
      return json(200, { ok: true });
    }
    if (method === 'POST') {
      if (body && PLAYERS.includes(body.owner) && body.owner !== shot.owner) {
        const shots = await readShots(store);
        shot.owner = body.owner;
        shot.position = shots.filter((s) => s.owner === body.owner).length;
      }
      if (body && Number.isFinite(body.position)) shot.position = body.position;
      await store.set('shot:' + id, JSON.stringify(shot));
      const state = await readState(store);
      state.slides = buildSlides(state.order, await knownShots(store, state, { add: shot }));
      await writeState(store, state);
      return json(200, { ok: true, shot });
    }
  }

  if (route === '/host/reorder-shots' && method === 'POST') {
    const ids = (body && body.ids) || [];
    for (let i = 0; i < ids.length; i += 1) {
      const raw = await store.get('shot:' + ids[i]);
      if (!raw) continue;
      const shot = JSON.parse(raw);
      shot.position = i;
      await store.set('shot:' + ids[i], JSON.stringify(shot));
    }
    await syncSlides(store, await readState(store));
    return json(200, { ok: true });
  }

  if (route === '/host/order' && method === 'POST') {
    const order = (body && body.order) || [];
    const clean = order.filter((n) => PLAYERS.includes(n));
    for (const name of PLAYERS) if (!clean.includes(name)) clean.push(name);
    const state = await readState(store);
    state.order = clean;
    await syncSlides(store, state);
    return json(200, { ok: true, order: clean });
  }

  if (route === '/host/release' && method === 'POST') {
    const name = body && body.name;
    if (!PLAYERS.includes(name)) return json(400, { error: 'Unknown name' });
    await store.delete('claim:' + name);
    const state = await readState(store);
    delete state.joined[name];
    await writeState(store, state);
    return json(200, { ok: true });
  }

  if (route === '/host/action' && method === 'POST') {
    const action = body && body.action;
    const state = await readState(store);
    let slides = await ensureSlides(store, state);
    // Starting a game settles the running order from whatever is in the locker.
    if (action === 'start') slides = buildSlides(state.order, await knownShots(store, state));
    const subject = subjectOf(slides, state);

    const clearVotes = async (owner) => {
      if (!owner) return;
      const keys = await store.list('vote:' + owner + ':');
      for (const key of keys) await store.delete(key);
      delete state.revealed[owner];
    };

    if (action === 'start') {
      if (slides.length === 0) return json(409, { error: 'Nobody has any screenshots yet' });
      state.slides = slides;
      state.roundIndex = 0;
      state.phase = 'viewing';
    } else if (action === 'open-voting') {
      if (!subject) return json(409, { error: 'No slide is live' });
      state.phase = 'voting';
    } else if (action === 'close-voting') {
      state.phase = 'closed';
    } else if (action === 'reveal') {
      if (!subject) return json(409, { error: 'No slide is live' });
      const keys = await store.list('vote:' + subject + ':');
      const votes = parseVoteKeys(keys, subject);
      // Scoring is settled here, on the server, from the stored votes only.
      state.revealed[subject] = { votes, at: Date.now() };
      state.phase = 'revealed';
    } else if (action === 'next') {
      if (state.roundIndex + 1 >= slides.length) state.phase = 'finished';
      else { state.roundIndex += 1; state.phase = 'viewing'; }
    } else if (action === 'previous') {
      if (state.roundIndex > 0) { state.roundIndex -= 1; state.phase = 'viewing'; }
    } else if (action === 'reset-round') {
      await clearVotes(subject);
      state.phase = 'viewing';
    } else if (action === 'end-game') {
      state.phase = 'finished';
    } else if (action === 'lobby') {
      state.phase = 'lobby';
    } else if (action === 'goto') {
      const index = Number(body.index);
      if (!Number.isInteger(index) || index < 0 || index >= slides.length) return json(400, { error: 'No such slide' });
      state.roundIndex = index;
      state.phase = 'viewing';
    } else {
      return json(400, { error: 'Unknown action' });
    }
    await writeState(store, state);
    return json(200, { ok: true, phase: state.phase, roundIndex: state.roundIndex });
  }

  if (route === '/host/wipe' && method === 'POST') {
    const what = (body && body.what) || 'game';
    const prefixes = what === 'all'
      ? ['vote:', 'claim:', 'shot:', 'img:', 'state']
      : ['vote:', 'claim:', 'state'];
    for (const prefix of prefixes) {
      for (const key of await store.list(prefix)) await store.delete(key);
    }
    return json(200, { ok: true });
  }

  return json(404, { error: 'No such route' });
}
