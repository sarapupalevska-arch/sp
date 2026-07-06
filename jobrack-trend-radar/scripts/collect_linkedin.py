"""LinkedIn post collection, in priority order.

Priority 1 is manual export (scripts/parse_manual.py). This script covers:
  Priority 2: Apify actors, if APIFY_TOKEN is set in .env
  Priority 3: web search for indexed post URLs (engagement marked unavailable)

Usage:
  python scripts/collect_linkedin.py            # tries Apify, falls back to search-URL generation
  python scripts/collect_linkedin.py --tier2    # include tier 2 (monthly)

Caching: raw Apify JSON is stored in data/linkedin/raw/ and never re-fetched
if younger than 6 days.
"""
import argparse
import json
import re
import sys
import time
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent))
from common import (DATA, append_rows, cache_fresh, load_env, load_json,
                    load_yaml, record_source_status, save_json, today)

RAW_DIR = DATA / "linkedin" / "raw"

# Apify actor for LinkedIn profile posts. Swap the actor ID here if you buy a
# different one; this is the commonly used "LinkedIn Profile Posts" actor slug.
APIFY_ACTOR = "apimaestro~linkedin-profile-posts"
APIFY_RUN_URL = "https://api.apify.com/v2/acts/{actor}/run-sync-get-dataset-items"


def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def targets(include_tier2=False):
    cfg = load_yaml("competitors.yaml")
    out = list(cfg.get("tier1", []))
    if include_tier2:
        out += cfg.get("tier2", [])
    return [c for c in out if c.get("linkedin_url") or c.get("company_page")]


def fetch_apify(token, competitor):
    """Fetch posts for one profile via Apify, with a 6-day cache."""
    url = competitor.get("linkedin_url") or competitor.get("company_page")
    cache_file = RAW_DIR / f"{slugify(competitor['name'])}.json"
    if cache_fresh(cache_file):
        print(f"  cache hit (<6 days old): {cache_file.name}")
        return load_json(cache_file)
    resp = requests.post(
        APIFY_RUN_URL.format(actor=APIFY_ACTOR),
        params={"token": token},
        json={"profileUrl": url, "maxPosts": 100},
        timeout=300,
    )
    resp.raise_for_status()
    items = resp.json()
    save_json(cache_file, items)
    time.sleep(5)  # be polite between actor runs
    return items


def normalize_apify(items, competitor):
    rows = []
    for it in items:
        text = it.get("text") or it.get("postText") or ""
        if not text:
            continue
        stats = it.get("stats") or it
        rows.append({
            "founder": competitor["name"],
            "company": competitor.get("company", ""),
            "post_url": it.get("url") or it.get("postUrl") or "",
            "date": (it.get("postedAt") or it.get("date") or "")[:10],
            "format": it.get("type") or ("image" if it.get("images") else "text"),
            "hook_text": text.split("\n")[0][:300],
            "full_text": text,
            "reactions": stats.get("totalReactions") or stats.get("likes") or "",
            "comments": stats.get("comments") or "",
            "reposts": stats.get("reposts") or stats.get("shares") or "",
            "theme": "", "pillar": "", "cta_type": "",
            "source": f"apify:{today()}",
            "collected_at": today(),
        })
    return rows


def search_fallback(competitors):
    """No API and no manual dumps: emit site-restricted search URLs for Sara to
    open manually. Engagement fields stay unavailable per operating rules."""
    lines = ["Open these searches to find indexed post URLs (engagement will be marked unavailable):\n"]
    for c in competitors:
        url = c.get("linkedin_url") or c.get("company_page") or ""
        handle = url.rstrip("/").split("/")[-1] if url else slugify(c["name"])
        q = f"site:linkedin.com/posts {handle}"
        lines.append(f"  {c['name']}: https://www.google.com/search?q={requests.utils.quote(q)}")
    out = DATA / "linkedin" / f"search-fallback-urls-{today()}.txt"
    out.write_text("\n".join(lines))
    print("\n".join(lines))
    print(f"\nSaved to {out}")


def main(include_tier2=False):
    env = load_env()
    token = env.get("APIFY_TOKEN")
    comps = targets(include_tier2)
    if not comps:
        print("No competitors with LinkedIn URLs in config. Fill in competitors.yaml.")
        return
    if token:
        total = 0
        for c in comps:
            print(f"Fetching {c['name']} via Apify...")
            try:
                items = fetch_apify(token, c)
                n = append_rows(normalize_apify(items, c))
                total += n
                print(f"  {n} new posts")
            except Exception as e:
                print(f"  FAILED: {e}")
        record_source_status("linkedin_apify", "ok" if total else "failed",
                            f"{total} new posts via Apify")
    else:
        record_source_status("linkedin_apify", "skipped", "No APIFY_TOKEN in .env")
        print("No APIFY_TOKEN found. Manual export is the primary path")
        print("(python scripts/parse_manual.py --checklist). Fallback search URLs:\n")
        search_fallback(comps)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--tier2", action="store_true")
    args = ap.parse_args()
    main(args.tier2)
