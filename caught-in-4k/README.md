# Who Searched That? Caught in 4K

A live game show for eight people and their search history. Everyone sends the
host screenshots privately. Each round shows one person's screenshots
anonymously, everybody else guesses whose they are, the host presses REVEAL, and
the leaderboard moves.

**One person equals one slide equals all of their screenshots.** If Carla gave
you five screenshots, all five appear together on Carla's slide. Nobody creates
rounds by hand: a person gets a slide the moment they have one screenshot.

The eight identities are fixed: Kasia, Carla, Ivan, Chels, Ana, Andjela, Noel,
Sara. No signup, no passwords, no email. Players open one link and click a name.

## What is in here

```
public/index.html          the entire UI, players and host, no build step
netlify/functions/api.mjs  the Netlify Function entry point
lib/handler.mjs            every rule, storage agnostic
lib/game.mjs               pure rules: slides, votes, scoring, ranking, stats
lib/player-view.mjs        the allowlist that builds a player payload
lib/store-blobs.mjs        Netlify Blobs storage
lib/store-disk.mjs         the same interface over a folder on disk
dev-server.mjs             local server, same handler, disk storage
test/                      unit and API tests
test/e2e/                  real browser tests, one host and eight players
```

No framework, no bundler, no database, no third party accounts. Netlify Blobs
holds the state, the votes and the screenshot bytes.

## Running it locally

```
npm install
npm start          # http://127.0.0.1:8888 for players, /host for the host
npm test           # unit and API tests
npm run test:e2e   # real browsers, needs a Chromium available to Playwright
```

The code that runs during the game is the code the tests drive. The only
difference between local and live is which storage module is plugged in.

## How the answer stays hidden

The hidden person's name never reaches a player browser before the reveal.

1. `lib/player-view.mjs` builds the player payload field by field from an
   allowlist. The full game state is never assembled and trimmed, because that
   is how a newly added field leaks the answer one day.
2. Screenshots are opaque random ids with no filename kept anywhere.
   `/api/image/<id>` serves the bytes only if that id belongs to the slide that
   is live right now or to a slide already revealed. Everything else is a 404.
3. Players see vote progress as a count, never a list of names. A named list
   would give it away: when the last vote lands, the only person without a tick
   is the one sitting the round out, which is the answer. The host screen shows
   the named list, because the host already knows.

Scoring is computed on the server from stored votes. A client can never submit a
score. The subject of a slide gets a 403 if they try to vote, and a second vote
from the same person gets a 409.

Votes are stored one blob per vote with the whole vote in the key
(`vote:<subject>:<voter>:<guess>`), so simultaneous voters cannot overwrite each
other and a round reads back with a single key listing.

## Deploying to Netlify

You need a GitHub account and a Netlify account. You do not need any
organisation admin rights: this deploys from a repository on your own personal
account.

1. **Put this folder in a repository on your own GitHub account.** On
   github.com press the plus in the top right, then New repository. Give it a
   name, leave it Private if you like, and press Create repository. Follow the
   "push an existing repository" lines that GitHub shows you.
   You should see your files listed on the repository page afterwards.
2. **Sign in at app.netlify.com** with your GitHub account.
3. **Press Add new site, then Import an existing project.** Choose GitHub, and
   authorise Netlify when it asks. If your repository does not appear, press
   "Configure the Netlify app on GitHub" and grant access to that one repository.
4. **Pick the repository.** Netlify reads `netlify.toml`, so the build command
   stays empty and the publish directory is `public`. Do not change them.
   You should see "Publish directory: public" on the screen.
5. **Press Deploy.** It takes about a minute. When it finishes you get a URL
   like `https://something-random.netlify.app`.
6. **Open that URL with `/host` on the end.** The first person to arrive sets
   the passphrase, so set it now and keep it to yourself. The answers live
   behind it.
7. **Press Copy player link** on the host screen and paste it to your team. That
   is the link everybody else uses.

Netlify Blobs turns itself on for the site, so there is nothing else to
configure and no keys to paste anywhere.

If the page ever says the rules engine is not answering, the site was deployed
as a static file without the function. Redeploy the whole repository, not just
`public/index.html`.

## Running the show

The host screen has one big next move button that always says the thing you
almost certainly want next: start, open voting, close voting, reveal, next
slide. Every finer control sits underneath it, deliberately muted.

Before you start: upload the screenshots and put a name against every single
one. The upload button refuses to work until you have, on purpose, so a
distracted host cannot file the entire game against Kasia.

While you are screen sharing, press Blur the answer. It stays blurred until you
press it again.
