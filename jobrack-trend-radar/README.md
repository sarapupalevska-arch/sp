# JobRack Trend Radar

Weekly competitor and trend intelligence for JobRack's LinkedIn content.
Tracks what competitor founders publish and how it performs, and spots
emerging topics in the remote hiring / offshore talent niche early.

## Weekly run order

```bash
pip install -r requirements.txt   # once

# 1. Collect LinkedIn data (pick whichever applies)
python scripts/parse_manual.py --checklist   # instructions for manual export
python scripts/parse_manual.py               # parse pasted dumps in data/manual/
python scripts/collect_linkedin.py           # Apify (needs APIFY_TOKEN in .env)

# 2. Trends
python scripts/trends.py                     # Google Trends, Reddit, X URLs, blogs/news

# 3. Analysis (prompts for follower counts if missing)
python scripts/analyze.py

# 4. Weekly brief
python scripts/report.py                     # -> reports/brief-YYYY-MM-DD.md
```

## Credentials (all optional, in `.env` at project root)

| Variable | Unlocks |
|---|---|
| `APIFY_TOKEN` | Automated LinkedIn post scraping (priority 2 after manual export) |
| `ANTHROPIC_API_KEY` | LLM theme tagging instead of keyword rules |

## Structure

```
config/competitors.yaml   watch list (edit freely to add names)
config/keywords.yaml      trend keyword sets
data/manual/              your pasted LinkedIn dumps ({slug}-{date}.txt, posts split by ===)
data/linkedin/            normalized combined.csv + raw Apify JSON
data/trends|x|reddit/     dated exports per source
data/followers.json       follower counts for engagement normalization
reports/                  weekly briefs
```

## Operating rules baked in

- Engagement numbers always carry a source label and date in the brief.
- Posts are only attributed to a founder if collected from their own profile
  URL or a dump you made from it. Search-fallback posts have engagement marked
  unavailable.
- Everything is cached; data younger than 6 days is never re-fetched.
- Briefs contain no em dashes and stay under 600 words.
- Missing data is stated in the Data health section, never filled in.
