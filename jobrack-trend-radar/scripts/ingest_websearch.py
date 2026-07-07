"""Ingest web-search-found post URLs (priority 3 fallback) into combined.csv.

Reads the newest data/linkedin/websearch-*.json (hand-curated from
site-restricted searches). Engagement fields stay blank (unavailable for this
method). Post dates are derived from the LinkedIn activity ID, whose top bits
encode a millisecond epoch timestamp (id >> 22).

Usage: python scripts/ingest_websearch.py
"""
import glob
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import DATA, append_rows, load_json, load_yaml, record_source_status, today

ACTIVITY_RE = re.compile(r"activity-(\d{19})")


def date_from_activity_id(url):
    m = ACTIVITY_RE.search(url)
    if not m:
        return ""
    ms = int(m.group(1)) >> 22
    try:
        return datetime.fromtimestamp(ms / 1000, timezone.utc).strftime("%Y-%m-%d")
    except (ValueError, OSError):
        return ""


def company_for(founder_name):
    cfg = load_yaml("competitors.yaml")
    for tier in ("tier1", "tier2"):
        for c in cfg.get(tier, []):
            if c["name"] == founder_name:
                return c.get("company", "")
    return ""


def main():
    files = sorted(glob.glob(str(DATA / "linkedin" / "websearch-*.json")))
    if not files:
        print("No websearch-*.json files in data/linkedin/")
        record_source_status("linkedin_websearch", "skipped", "no websearch export present")
        return
    data = load_json(files[-1])
    rows = []
    for founder, info in data["founders"].items():
        company = company_for(founder)
        for post in info["posts"]:
            rows.append({
                "founder": founder,
                "company": company,
                "post_url": post["url"],
                "date": date_from_activity_id(post["url"]),
                "format": "unknown",
                "hook_text": post["title"][:300],
                "full_text": post["title"],
                "reactions": post.get("reactions", ""),
                "comments": post.get("comments", ""),
                "reposts": post.get("reposts", ""),
                "theme": "", "pillar": "", "cta_type": "",
                "source": f"websearch:{data['collected']}",
                "collected_at": today(),
            })
    n = append_rows(rows)
    record_source_status(
        "linkedin_websearch", "ok",
        f"{n} new indexed post URLs ingested; engagement unavailable for this method; "
        "hook_text is the indexed title snippet only")
    print(f"Ingested {n} new rows from {Path(files[-1]).name}")


if __name__ == "__main__":
    main()
