"""Parse manually pasted LinkedIn post dumps into the combined CSV.

Usage:
  python scripts/parse_manual.py                 # parse all files in data/manual/
  python scripts/parse_manual.py --checklist     # print the manual collection checklist

Dump file naming: data/manual/{founder-slug}-{YYYY-MM-DD}.txt
  e.g. data/manual/nick-huber-2026-07-06.txt

Dump format (flexible, built for copy-paste from LinkedIn):
  - Separate posts with a line containing only:  ===
  - Inside each post block, the parser looks for:
      * a date line: either an absolute date (2026-06-12, Jun 12, June 12 2026)
        or LinkedIn relative format (3d, 2w, 1mo) which is resolved against the
        file's date suffix
      * engagement lines anywhere in the block, e.g.
        "1,234 reactions" / "1,234" followed by "56 comments" / "12 reposts"
        LinkedIn copy-paste usually yields lines like: "234" "45 comments" "12 reposts"
      * a format hint line if you add one: [image] [video] [poll] [document] [text]
        (optional, defaults to text)
  - Everything else in the block is treated as post text. First non-empty,
    non-metadata line = hook.
"""
import argparse
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import DATA, append_rows, load_yaml, record_source_status, today

FORMAT_TAGS = {"image", "video", "poll", "document", "text", "carousel"}

RELATIVE_RE = re.compile(r"^\s*(\d+)\s*(h|d|w|mo|yr)\s*(?:•.*)?$")
REACTIONS_RE = re.compile(r"^\s*([\d,\.]+)\s*(?:reactions?|likes?)?\s*$")
COMMENTS_RE = re.compile(r"^\s*([\d,\.]+)\s+comments?\s*$", re.I)
REPOSTS_RE = re.compile(r"^\s*([\d,\.]+)\s+reposts?\s*$", re.I)
ABS_DATE_RES = [
    (re.compile(r"^(\d{4}-\d{2}-\d{2})$"), "%Y-%m-%d"),
    (re.compile(r"^([A-Z][a-z]{2,8} \d{1,2},? \d{4})$"), None),
]

CHECKLIST = """
MANUAL LINKEDIN COLLECTION CHECKLIST (do once per run, ~15 min per founder)

For each Tier 1 founder below:
  1. Open the LinkedIn profile URL in your browser (logged in).
  2. Click "Activity" then filter to "Posts".
  3. Scroll back 6 months (hold End key or scroll; LinkedIn lazy-loads).
  4. Either use a browser extension that exports the feed to text, or select-all
     and copy-paste the visible posts into a plain text file.
  5. Save as: data/manual/{slug}-{today}.txt
  6. Separate each post with a line containing only:  ===
  7. For each post keep: the relative date line (e.g. "3w"), the post text, and
     the engagement numbers (reactions count, "N comments", "N reposts").
  8. Optional: add a line like [image] or [video] if the post had media.

Then run:  python scripts/parse_manual.py

Tier 1 targets:
"""


def num(s):
    s = s.replace(",", "").replace(".", "")
    return int(s) if s.isdigit() else ""


def resolve_relative(match, file_date):
    n, unit = int(match.group(1)), match.group(2)
    days = {"h": 0, "d": 1, "w": 7, "mo": 30, "yr": 365}[unit] * n
    return (file_date - timedelta(days=days)).strftime("%Y-%m-%d")


def parse_block(block, file_date):
    date, fmt, reactions, comments, reposts = "", "text", "", "", ""
    text_lines = []
    for line in block.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        low = stripped.lower().strip("[]")
        if stripped.startswith("[") and stripped.endswith("]") and low in FORMAT_TAGS:
            fmt = low
            continue
        m = RELATIVE_RE.match(stripped)
        if m and not date:
            date = resolve_relative(m, file_date)
            continue
        matched_abs = False
        for rx, strf in ABS_DATE_RES:
            m = rx.match(stripped)
            if m and not date:
                raw = m.group(1).replace(",", "")
                for f in ([strf] if strf else ["%b %d %Y", "%B %d %Y"]):
                    try:
                        date = datetime.strptime(raw, f).strftime("%Y-%m-%d")
                        matched_abs = True
                        break
                    except ValueError:
                        pass
            if matched_abs:
                break
        if matched_abs:
            continue
        m = COMMENTS_RE.match(stripped)
        if m:
            comments = num(m.group(1))
            continue
        m = REPOSTS_RE.match(stripped)
        if m:
            reposts = num(m.group(1))
            continue
        # bare number line right after text = reactions (LinkedIn paste artifact)
        m = REACTIONS_RE.match(stripped)
        if m and reactions == "" and text_lines:
            val = num(m.group(1))
            if val != "":
                reactions = val
                continue
        text_lines.append(stripped)
    if not text_lines:
        return None
    full_text = "\n".join(text_lines)
    return {
        "date": date,
        "format": fmt,
        "hook_text": text_lines[0][:300],
        "full_text": full_text,
        "reactions": reactions,
        "comments": comments,
        "reposts": reposts,
    }


def founder_lookup():
    cfg = load_yaml("competitors.yaml")
    out = {}
    for tier in ("tier1", "tier2"):
        for c in cfg.get(tier, []):
            slug = re.sub(r"[^a-z0-9]+", "-", c["name"].lower()).strip("-")
            out[slug] = c
    return out


def parse_all():
    manual_dir = DATA / "manual"
    files = sorted(manual_dir.glob("*.txt"))
    if not files:
        record_source_status("linkedin_manual", "needs_input",
                            "No dump files in data/manual/. Run with --checklist for instructions.")
        print("No files found in data/manual/. Run with --checklist for instructions.")
        return
    founders = founder_lookup()
    total = 0
    for path in files:
        m = re.match(r"(.+)-(\d{4}-\d{2}-\d{2})\.txt$", path.name)
        if not m:
            print(f"SKIP {path.name}: name must be {{slug}}-{{YYYY-MM-DD}}.txt")
            continue
        slug, date_str = m.group(1), m.group(2)
        file_date = datetime.strptime(date_str, "%Y-%m-%d")
        # match slug to a configured founder (prefix match tolerated)
        founder = None
        for known_slug, cfg in founders.items():
            if known_slug.startswith(slug) or slug.startswith(known_slug.split("-")[0]):
                founder = cfg
                break
        if founder is None:
            print(f"SKIP {path.name}: no founder in competitors.yaml matches slug '{slug}'")
            continue
        rows = []
        for block in re.split(r"^\s*===\s*$", path.read_text(), flags=re.M):
            parsed = parse_block(block, file_date)
            if parsed:
                parsed.update({
                    "founder": founder["name"],
                    "company": founder.get("company", ""),
                    "post_url": "",
                    "theme": "", "pillar": "", "cta_type": "",
                    "source": f"manual:{path.name}",
                    "collected_at": today(),
                })
                rows.append(parsed)
        n = append_rows(rows)
        total += n
        print(f"{path.name}: parsed {len(rows)} posts, {n} new")
    record_source_status("linkedin_manual", "ok" if total else "needs_input",
                        f"{total} new posts ingested from manual dumps")


def print_checklist():
    print(CHECKLIST.replace("{today}", today()))
    cfg = load_yaml("competitors.yaml")
    for c in cfg["tier1"]:
        slug = re.sub(r"[^a-z0-9]+", "-", c["name"].lower()).strip("-")
        url = c.get("linkedin_url") or c.get("company_page") or "(URL needed, add to competitors.yaml)"
        print(f"  - {c['name']} ({c['company']}): {url}")
        print(f"    save as: data/manual/{slug}-{today()}.txt")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--checklist", action="store_true")
    args = ap.parse_args()
    if args.checklist:
        print_checklist()
    else:
        parse_all()
