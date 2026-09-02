// Pure game rules. No storage, no HTTP, so this can be unit tested directly.
import { createHash, randomBytes } from 'node:crypto';

export const PLAYERS = ['Kasia', 'Carla', 'Ivan', 'Chels', 'Ana', 'Andjela', 'Noel', 'Sara'];

export const PHASES = ['lobby', 'viewing', 'voting', 'closed', 'revealed', 'finished'];

export function emptyState() {
  return {
    phase: 'lobby',
    order: PLAYERS.slice(),
    roundIndex: 0,
    revealed: {},
    joined: {}
  };
}

export function newId() {
  return randomBytes(12).toString('hex');
}

export function hashPass(pass, salt) {
  return createHash('sha256').update(salt + ':' + pass).digest('hex');
}

export function signature(payload) {
  return createHash('sha1').update(JSON.stringify(payload)).digest('hex').slice(0, 16);
}

// One person equals one slide equals all of their screenshots.
// A person gets a slide as soon as they have at least one screenshot.
export function buildSlides(order, shots) {
  const byOwner = new Map();
  for (const shot of shots) {
    if (!byOwner.has(shot.owner)) byOwner.set(shot.owner, []);
    byOwner.get(shot.owner).push(shot);
  }
  const slides = [];
  const seen = new Set();
  const sequence = order.filter((n) => PLAYERS.includes(n));
  for (const name of PLAYERS) if (!sequence.includes(name)) sequence.push(name);
  for (const name of sequence) {
    if (seen.has(name)) continue;
    seen.add(name);
    const own = byOwner.get(name);
    if (!own || own.length === 0) continue;
    own.sort((a, b) => (a.position - b.position) || a.id.localeCompare(b.id));
    slides.push({ owner: name, shotIds: own.map((s) => s.id) });
  }
  return slides;
}

export function voteKey(subject, voter, guess) {
  return 'vote:' + subject + ':' + voter + ':' + guess;
}

// Collapse duplicates deterministically so one voter can only ever count once.
export function parseVoteKeys(keys, subject) {
  const prefix = 'vote:' + subject + ':';
  const chosen = new Map();
  for (const key of keys) {
    if (!key.startsWith(prefix)) continue;
    const rest = key.slice(prefix.length).split(':');
    if (rest.length !== 2) continue;
    const [voter, guess] = rest;
    if (!PLAYERS.includes(voter) || !PLAYERS.includes(guess)) continue;
    if (voter === subject) continue;
    const current = chosen.get(voter);
    if (current === undefined || guess < current) chosen.set(voter, guess);
  }
  return Object.fromEntries([...chosen.entries()].sort((a, b) => a[0].localeCompare(b[0])));
}

export function eligibleVoters(subject) {
  return PLAYERS.filter((n) => n !== subject);
}

// Scores are always recomputed on the server from stored votes.
export function scoresFrom(revealed) {
  const scores = Object.fromEntries(PLAYERS.map((n) => [n, 0]));
  for (const subject of Object.keys(revealed)) {
    const votes = revealed[subject].votes || {};
    for (const voter of Object.keys(votes)) {
      if (votes[voter] === subject && voter !== subject) scores[voter] += 1;
    }
  }
  return scores;
}

// Competition ranking, so a tie shares a rank and the next rank skips.
export function leaderboard(scores) {
  const rows = PLAYERS.map((name) => ({ name, score: scores[name] || 0 }));
  rows.sort((a, b) => (b.score - a.score) || a.name.localeCompare(b.name));
  let rank = 0;
  let lastScore = null;
  rows.forEach((row, index) => {
    if (row.score !== lastScore) {
      rank = index + 1;
      lastScore = row.score;
    }
    row.rank = rank;
  });
  return rows;
}

export function winners(scores) {
  const rows = leaderboard(scores);
  const top = rows.length ? rows[0].score : 0;
  return rows.filter((r) => r.rank === 1 && r.score === top).map((r) => r.name);
}

export function revealSummary(subject, votes) {
  const eligible = eligibleVoters(subject);
  const correct = [];
  const wrong = [];
  for (const voter of eligible) {
    const guess = votes[voter];
    if (!guess) continue;
    if (guess === subject) correct.push(voter);
    else wrong.push({ voter, guess });
  }
  return {
    owner: subject,
    correct,
    wrong,
    caught: correct.length,
    eligible: eligible.length,
    voted: correct.length + wrong.length
  };
}

// Secondary fun stats. Nothing here is load bearing.
export function funStats(revealed) {
  const subjects = Object.keys(revealed);
  if (subjects.length === 0) return null;
  const attempts = Object.fromEntries(PLAYERS.map((n) => [n, 0]));
  const hits = Object.fromEntries(PLAYERS.map((n) => [n, 0]));
  const accused = Object.fromEntries(PLAYERS.map((n) => [n, 0]));
  const pairings = new Map();
  const readRates = [];
  for (const subject of subjects) {
    const votes = revealed[subject].votes || {};
    const summary = revealSummary(subject, votes);
    if (summary.voted > 0) readRates.push({ name: subject, rate: summary.caught / summary.voted, caught: summary.caught });
    for (const voter of Object.keys(votes)) {
      const guess = votes[voter];
      attempts[voter] += 1;
      if (guess === subject) hits[voter] += 1;
      else {
        accused[guess] = (accused[guess] || 0) + 1;
        const pair = guess + ' for ' + subject;
        pairings.set(pair, (pairings.get(pair) || 0) + 1);
      }
    }
  }
  const tried = PLAYERS.filter((n) => attempts[n] > 0);
  const bestDetective = tried.length
    ? tried.slice().sort((a, b) => (hits[b] / attempts[b]) - (hits[a] / attempts[a]) || a.localeCompare(b))[0]
    : null;
  const mostSuspicious = PLAYERS.slice().sort((a, b) => accused[b] - accused[a] || a.localeCompare(b))[0];
  const sortedReads = readRates.slice().sort((a, b) => b.rate - a.rate || a.name.localeCompare(b.name));
  let redHerring = null;
  let topPair = 0;
  for (const [pair, count] of pairings) {
    if (count > topPair) { topPair = count; redHerring = pair; }
  }
  return {
    bestDetective: bestDetective && attempts[bestDetective] > 0
      ? { name: bestDetective, hits: hits[bestDetective], of: attempts[bestDetective] }
      : null,
    mostSuspicious: accused[mostSuspicious] > 0 ? { name: mostSuspicious, count: accused[mostSuspicious] } : null,
    openBook: sortedReads.length ? { name: sortedReads[0].name, caught: sortedReads[0].caught } : null,
    hardestToRead: sortedReads.length ? { name: sortedReads[sortedReads.length - 1].name, caught: sortedReads[sortedReads.length - 1].caught } : null,
    redHerring: redHerring ? { pair: redHerring, count: topPair } : null
  };
}
