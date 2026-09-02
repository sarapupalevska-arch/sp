import test from 'node:test';
import assert from 'node:assert/strict';
import {
  PLAYERS, buildSlides, parseVoteKeys, scoresFrom, leaderboard, winners,
  revealSummary, funStats, emptyState
} from '../lib/game.mjs';
import { buildPlayerView, PLAYER_KEYS } from '../lib/player-view.mjs';

const shot = (id, owner, position) => ({ id, owner, position });

test('one person is one slide holding all of their screenshots', () => {
  const shots = [
    shot('a', 'Carla', 0), shot('b', 'Carla', 1), shot('c', 'Carla', 2),
    shot('d', 'Carla', 3), shot('e', 'Carla', 4),
    shot('f', 'Noel', 0), shot('g', 'Noel', 1), shot('h', 'Noel', 2)
  ];
  const slides = buildSlides(PLAYERS, shots);
  assert.equal(slides.length, 2);
  assert.deepEqual(slides.map((s) => s.owner), ['Carla', 'Noel']);
  assert.equal(slides[0].shotIds.length, 5);
  assert.equal(slides[1].shotIds.length, 3);
});

test('people with no screenshots are skipped, and the order is respected', () => {
  const shots = [shot('a', 'Sara', 0), shot('b', 'Ivan', 0)];
  const slides = buildSlides(['Ivan', 'Kasia', 'Sara'], shots);
  assert.deepEqual(slides.map((s) => s.owner), ['Ivan', 'Sara']);
});

test('screenshots keep their position order inside a slide', () => {
  const slides = buildSlides(PLAYERS, [shot('z', 'Ana', 2), shot('x', 'Ana', 0), shot('y', 'Ana', 1)]);
  assert.deepEqual(slides[0].shotIds, ['x', 'y', 'z']);
});

test('vote keys collapse duplicates and reject the subject voting', () => {
  const votes = parseVoteKeys([
    'vote:Carla:Ivan:Carla',
    'vote:Carla:Ivan:Sara',
    'vote:Carla:Carla:Carla',
    'vote:Carla:Noel:Ana',
    'vote:Carla:Nobody:Ana',
    'vote:Sara:Ivan:Sara'
  ], 'Carla');
  assert.deepEqual(votes, { Ivan: 'Carla', Noel: 'Ana' });
});

test('scores come only from stored votes and never from a client', () => {
  const revealed = {
    Carla: { votes: { Ivan: 'Carla', Noel: 'Ana', Sara: 'Carla' } },
    Noel: { votes: { Ivan: 'Noel', Carla: 'Ana' } }
  };
  const scores = scoresFrom(revealed);
  assert.equal(scores.Ivan, 2);
  assert.equal(scores.Sara, 1);
  assert.equal(scores.Noel, 0);
  assert.equal(scores.Carla, 0);
});

test('competition ranking shares a rank and skips the next one', () => {
  const rows = leaderboard({ Kasia: 3, Carla: 3, Ivan: 1, Chels: 0, Ana: 0, Andjela: 0, Noel: 0, Sara: 0 });
  assert.equal(rows[0].rank, 1);
  assert.equal(rows[1].rank, 1);
  assert.equal(rows[2].rank, 3);
  assert.deepEqual(winners({ Kasia: 3, Carla: 3, Ivan: 1, Chels: 0, Ana: 0, Andjela: 0, Noel: 0, Sara: 0 }), ['Carla', 'Kasia']);
});

test('a reveal counts caught out of the eligible voters, not out of eight', () => {
  const summary = revealSummary('Carla', { Ivan: 'Carla', Noel: 'Carla', Sara: 'Ana' });
  assert.equal(summary.eligible, 7);
  assert.equal(summary.caught, 2);
  assert.equal(summary.voted, 3);
  assert.deepEqual(summary.wrong, [{ voter: 'Sara', guess: 'Ana' }]);
});

test('fun stats survive a full game without throwing', () => {
  const stats = funStats({
    Carla: { votes: { Ivan: 'Carla', Noel: 'Ana', Sara: 'Ana' } },
    Noel: { votes: { Ivan: 'Noel', Carla: 'Ana' } }
  });
  assert.equal(stats.bestDetective.name, 'Ivan');
  assert.equal(stats.mostSuspicious.name, 'Ana');
  assert.equal(stats.redHerring.count, 2);
});

// ---- the security rule ----

function ctx(overrides) {
  const state = Object.assign(emptyState(), { phase: 'voting', roundIndex: 0 }, overrides.state || {});
  return Object.assign({
    state,
    slides: [{ owner: 'Carla', shotIds: ['s1', 's2'] }, { owner: 'Noel', shotIds: ['s3'] }],
    votes: { Ivan: 'Sara', Noel: 'Carla' },
    scores: Object.fromEntries(PLAYERS.map((n) => [n, 0])),
    you: 'Ivan'
  }, overrides, { state });
}

test('the player payload carries only allowlisted keys', () => {
  const view = buildPlayerView(ctx({}));
  assert.deepEqual(Object.keys(view).sort(), PLAYER_KEYS.slice().sort());
});

test('the hidden identity is nowhere in the payload before the reveal', () => {
  const view = buildPlayerView(ctx({}));
  const forbidden = ['owner', 'subject', 'slides', 'order', 'votes', 'voters', 'shots', 'revealed', 'answer', 'filename'];
  // Assert the forbidden keys are absent rather than hunting for a name string,
  // because all eight names legitimately appear in the leaderboard.
  const seen = new Set();
  (function walk(node) {
    if (!node || typeof node !== 'object') return;
    for (const key of Object.keys(node)) { seen.add(key); walk(node[key]); }
  })(view);
  for (const key of forbidden) assert.ok(!seen.has(key), 'payload must not contain ' + key);
  assert.equal(view.reveal, null);
});

test('players get a vote count, never a list of who has voted', () => {
  const view = buildPlayerView(ctx({}));
  assert.equal(view.voteCount, 2);
  assert.equal(view.eligibleCount, 7);
  assert.ok(!Array.isArray(view.voteCount));
  assert.equal(JSON.stringify(view).includes('"Ivan":"Sara"'), false);
});

test('only the subject is told that they are the subject', () => {
  assert.equal(buildPlayerView(ctx({ you: 'Carla' })).youAreSubject, true);
  assert.equal(buildPlayerView(ctx({ you: 'Ivan' })).youAreSubject, false);
  assert.equal(buildPlayerView(ctx({ you: null })).youAreSubject, false);
});

test('a player sees their own guess and nobody else', () => {
  const view = buildPlayerView(ctx({ you: 'Ivan' }));
  assert.equal(view.yourGuess, 'Sara');
  assert.equal(view.youVoted, true);
  const other = buildPlayerView(ctx({ you: 'Sara' }));
  assert.equal(other.yourGuess, null);
  assert.equal(other.youVoted, false);
});

test('the payload only lists screenshot ids for the slide that is live', () => {
  const view = buildPlayerView(ctx({}));
  assert.deepEqual(view.shotIds, ['s1', 's2']);
  const lobby = buildPlayerView(ctx({ state: { phase: 'lobby' } }));
  assert.deepEqual(lobby.shotIds, []);
});

test('the name arrives once the round is revealed', () => {
  const view = buildPlayerView(ctx({ state: { phase: 'revealed' } }));
  assert.equal(view.reveal.owner, 'Carla');
  assert.equal(view.reveal.caught, 1);
  assert.deepEqual(view.reveal.correct, ['Noel']);
});

test('an unchanged payload keeps the same signature', () => {
  assert.equal(buildPlayerView(ctx({})).sig, buildPlayerView(ctx({})).sig);
  assert.notEqual(buildPlayerView(ctx({})).sig, buildPlayerView(ctx({ state: { phase: 'closed' } })).sig);
});
