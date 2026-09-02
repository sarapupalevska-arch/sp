// The player payload is built field by field from an allowlist.
// Nothing is ever assembled in full and trimmed afterwards, because that is how
// a new field leaks the answer one day.
import { leaderboard, eligibleVoters, revealSummary, funStats, winners, signature, PLAYERS } from './game.mjs';

// Every key a player browser is allowed to receive. Tests assert this list.
export const PLAYER_KEYS = [
  'phase', 'round', 'totalRounds', 'shotIds', 'shotCount',
  'voteCount', 'eligibleCount', 'you', 'youAreSubject', 'youVoted', 'yourGuess',
  'players', 'leaderboard', 'reveal', 'stats', 'champions', 'sig'
];

export function buildPlayerView(ctx) {
  const {
    state, slides, votes, scores, you
  } = ctx;
  const slide = slides[state.roundIndex] || null;
  const subject = slide ? slide.owner : null;
  const revealedNow = state.phase === 'revealed' && subject;
  const inPlay = ['viewing', 'voting', 'closed', 'revealed'].includes(state.phase);

  const view = {};
  view.phase = state.phase;
  view.round = inPlay && slide ? state.roundIndex + 1 : 0;
  view.totalRounds = slides.length;
  view.shotIds = inPlay && slide ? slide.shotIds.slice() : [];
  view.shotCount = view.shotIds.length;

  const eligible = subject ? eligibleVoters(subject) : PLAYERS.slice();
  view.eligibleCount = inPlay && slide ? eligible.length : 0;
  // A count only. A named list of who has voted would identify the one person
  // sitting the round out, which is the answer.
  view.voteCount = inPlay && slide ? Object.keys(votes).length : 0;

  view.you = you || null;
  view.youAreSubject = Boolean(you && subject && you === subject && inPlay);
  view.youVoted = Boolean(you && Object.prototype.hasOwnProperty.call(votes, you));
  view.yourGuess = you && votes[you] ? votes[you] : null;

  view.players = PLAYERS.map((name) => ({ name, joined: Boolean(state.joined[name]) }));
  view.leaderboard = leaderboard(scores).map((row) => ({ name: row.name, score: row.score, rank: row.rank }));

  if (revealedNow) {
    const summary = revealSummary(subject, votes);
    view.reveal = {
      owner: summary.owner,
      correct: summary.correct.slice(),
      wrong: summary.wrong.map((w) => ({ voter: w.voter, guess: w.guess })),
      caught: summary.caught,
      eligible: summary.eligible,
      voted: summary.voted
    };
  } else {
    view.reveal = null;
  }

  if (state.phase === 'finished') {
    view.stats = funStats(state.revealed);
    view.champions = winners(scores);
  } else {
    view.stats = null;
    view.champions = null;
  }

  view.sig = signature(view);
  return view;
}
