"""Emerging trend detection across Google Trends, X, Reddit, and blogs/news.

Usage:
  python scripts/trends.py                # everything
  python scripts/trends.py --only gtrends|x|reddit|signals

Outputs:
  data/trends/gtrends-{date}.json         interest + rising queries per keyword set
  data/trends/region-race-{date}.json     region keyword comparison (chart data)
  data/x/x-search-urls-{date}.txt         advanced search URLs to open manually
  data/reddit/reddit-{date}.json          matching top/rising threads, last 30 days
  data/trends/signals-{date}.json         Near blog, Somewhere blog, Google News

All raw responses cached; each source's health recorded for the report.
"""
import argparse
import re
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import quote

import requests

sys.path.insert(0, str(Path(__file__).parent))
from common import (DATA, cache_fresh, load_json, load_yaml,
                    record_source_status, save_json, today)

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"}

KEYWORD_SETS = ("core", "regions", "buyer_intent", "adjacent_emerging")


# ---------------- Google Trends ----------------

def chunk(lst, n=5):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def run_gtrends():
    out_file = DATA / "trends" / f"gtrends-{today()}.json"
    race_file = DATA / "trends" / f"region-race-{today()}.json"
    if cache_fresh(out_file, 6):
        print("Google Trends: cache fresh, skipping")
        record_source_status("google_trends", "ok", "cache <6 days old")
        return
    try:
        from pytrends.request import TrendReq
    except ImportError:
        record_source_status("google_trends", "failed", "pytrends not installed (pip install pytrends)")
        return
    kw = load_yaml("keywords.yaml")
    pytrends = TrendReq(hl="en-US", tz=0, timeout=(10, 30), retries=2, backoff_factor=2)
    results = {}
    errors = []
    for set_name in KEYWORD_SETS:
        results[set_name] = {}
        for group in chunk(kw[set_name]):
            for timeframe, label in (("today 3-m", "90d"), ("today 12-m", "12m")):
                try:
                    pytrends.build_payload(group, timeframe=timeframe)
                    df = pytrends.interest_over_time()
                    if df is not None and not df.empty:
                        df = df.drop(columns=["isPartial"], errors="ignore")
                        for col in df.columns:
                            entry = results[set_name].setdefault(col, {})
                            series = df[col]
                            recent = series.tail(max(4, len(series) // 8)).mean()
                            earlier = series.head(max(4, len(series) // 8)).mean()
                            entry[label] = {
                                "mean_interest": round(float(series.mean()), 1),
                                "recent_mean": round(float(recent), 1),
                                "earlier_mean": round(float(earlier), 1),
                                "pct_change": round((recent - earlier) / earlier * 100, 1) if earlier else None,
                            }
                    time.sleep(3)
                except Exception as e:
                    errors.append(f"{set_name}/{group[0]}... {timeframe}: {e}")
                    time.sleep(8)
            # related rising queries per group (one call per keyword batch)
            try:
                pytrends.build_payload(group, timeframe="today 3-m")
                related = pytrends.related_queries()
                for k, tables in (related or {}).items():
                    rising = tables.get("rising") if tables else None
                    if rising is not None and not rising.empty:
                        entry = results[set_name].setdefault(k, {})
                        entry["rising_queries"] = [
                            {"query": r["query"],
                             "value": ("Breakout" if r["value"] >= 5000 else int(r["value"])),
                             "flag": bool(r["value"] >= 200)}
                            for _, r in rising.head(10).iterrows()
                        ]
                time.sleep(3)
            except Exception as e:
                errors.append(f"related/{group[0]}: {e}")
                time.sleep(8)
    save_json(out_file, {"generated": today(), "results": results, "errors": errors})

    # Region race comparison (single payload so values are directly comparable)
    try:
        race_kw = kw["region_race"][:5]
        pytrends.build_payload(race_kw, timeframe="today 12-m")
        df = pytrends.interest_over_time()
        race = {}
        if df is not None and not df.empty:
            df = df.drop(columns=["isPartial"], errors="ignore")
            race = {
                "keywords": race_kw,
                "weekly": [{"date": str(idx.date()), **{c: int(row[c]) for c in df.columns}}
                           for idx, row in df.iterrows()],
                "growth_pct": {
                    c: (round((df[c].tail(8).mean() - df[c].head(8).mean())
                              / df[c].head(8).mean() * 100, 1) if df[c].head(8).mean() else None)
                    for c in df.columns
                },
            }
        save_json(race_file, race)
    except Exception as e:
        errors.append(f"region_race: {e}")

    any_data = any(results[s] for s in results)
    record_source_status(
        "google_trends", "ok" if any_data else "failed",
        f"{sum(len(v) for v in results.values())} keywords with data, {len(errors)} errors"
        + (f"; first error: {errors[0]}" if errors else ""))
    print(f"Google Trends done: {out_file} ({len(errors)} errors)")


# ---------------- X / Twitter ----------------

def run_x():
    kw = load_yaml("keywords.yaml")
    since = (datetime.now(timezone.utc) - timedelta(days=60)).strftime("%Y-%m-%d")
    lines = ["X advanced searches. Open, note top posts and recurring accounts",
             "(new voices appearing repeatedly = leading indicator). Paste findings",
             f"into data/manual/x-notes-{today()}.txt if worth tracking.\n"]
    for set_name in KEYWORD_SETS:
        lines.append(f"[{set_name}]")
        for k in kw[set_name]:
            q = quote(f'min_faves:100 "{k}" since:{since}')
            lines.append(f"  {k}: https://x.com/search?q={q}&f=top")
        lines.append("")
    out = DATA / "x" / f"x-search-urls-{today()}.txt"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines))
    record_source_status("x_search", "needs_input",
                        f"Search URLs generated at {out.name}; no scraping token provided")
    print(f"X search URLs written to {out}")


# ---------------- Reddit ----------------

def run_reddit():
    kw = load_yaml("keywords.yaml")
    subs = kw["subreddits"]
    all_terms = [t.lower() for s in KEYWORD_SETS for t in kw[s]]
    # broader single-word stems so we do not miss variations
    stems = ["remote hir", "offshore", "outsourc", "virtual assistant", "overseas",
             "eastern europe", "south africa", "philippines", "latam", "nearshor",
             "ai employee", "ai agent", "eor", "employer of record", "global payroll",
             "remote team", "delegat"]
    out_file = DATA / "reddit" / f"reddit-{today()}.json"
    if cache_fresh(out_file, 6):
        record_source_status("reddit", "ok", "cache <6 days old")
        return
    results = {}
    failed = []
    for sub in subs:
        matches = []
        for listing in ("top", "rising"):
            url = f"https://www.reddit.com/r/{sub}/{listing}.json"
            params = {"limit": 100, "t": "month"} if listing == "top" else {"limit": 50}
            try:
                r = requests.get(url, params=params, headers=UA, timeout=20)
                r.raise_for_status()
                for child in r.json().get("data", {}).get("children", []):
                    d = child["data"]
                    text = (d.get("title", "") + " " + d.get("selftext", "")[:2000]).lower()
                    hit = [s for s in stems if s in text] or [t for t in all_terms if t in text]
                    if hit:
                        matches.append({
                            "title": d.get("title"),
                            "url": "https://reddit.com" + d.get("permalink", ""),
                            "score": d.get("score"),
                            "num_comments": d.get("num_comments"),
                            "created": datetime.fromtimestamp(d.get("created_utc", 0), timezone.utc).strftime("%Y-%m-%d"),
                            "listing": listing,
                            "matched": hit[:3],
                            "question_phrasing": d.get("title") if "?" in d.get("title", "") else None,
                        })
                time.sleep(2)
            except Exception as e:
                failed.append(f"r/{sub}/{listing}: {e}")
        if matches:
            results[sub] = matches
    save_json(out_file, {"generated": today(), "results": results, "failed": failed})
    total = sum(len(v) for v in results.values())
    status = "ok" if total else ("failed" if failed else "ok")
    record_source_status("reddit", status,
                        f"{total} matching threads across {len(results)} subreddits"
                        + (f"; {len(failed)} fetch failures ({failed[0]})" if failed else ""))
    print(f"Reddit done: {total} matches, {len(failed)} failures -> {out_file}")


# ---------------- Other signals ----------------

def fetch_text(url):
    r = requests.get(url, headers=UA, timeout=20)
    r.raise_for_status()
    return r.text


def extract_links(html, base, pattern):
    links = []
    for m in re.finditer(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', html, re.S | re.I):
        href, label = m.group(1), re.sub(r"<[^>]+>", "", m.group(2)).strip()
        if re.search(pattern, href) and label and len(label) > 15:
            if href.startswith("/"):
                href = base + href
            links.append({"title": label[:200], "url": href})
    seen, out = set(), []
    for l in links:
        if l["url"] not in seen:
            seen.add(l["url"])
            out.append(l)
    return out[:15]


def run_signals():
    out_file = DATA / "trends" / f"signals-{today()}.json"
    signals = {"generated": today()}
    statuses = []

    # Near blog / reports
    try:
        html = fetch_text("https://www.hirewithnear.com/blog")
        signals["near_blog"] = extract_links(html, "https://www.hirewithnear.com", r"/blog/|/report")
        statuses.append(("near_blog", "ok", f"{len(signals['near_blog'])} posts found"))
    except Exception as e:
        statuses.append(("near_blog", "failed", str(e)[:120]))

    # Somewhere blog (Success Stories cadence)
    try:
        html = fetch_text("https://somewhere.com/blog")
        signals["somewhere_blog"] = extract_links(html, "https://somewhere.com", r"/blog|/success|/stories|/case")
        statuses.append(("somewhere_blog", "ok", f"{len(signals['somewhere_blog'])} posts found"))
    except Exception as e:
        statuses.append(("somewhere_blog", "failed", str(e)[:120]))

    # Google News RSS, last 7 days
    news = []
    try:
        for q in ("remote hiring", "offshore talent"):
            xml = fetch_text(f"https://news.google.com/rss/search?q={quote(q)}+when:7d&hl=en-US&gl=US&ceid=US:en")
            root = ET.fromstring(xml)
            for item in root.iter("item"):
                news.append({
                    "query": q,
                    "title": item.findtext("title"),
                    "url": item.findtext("link"),
                    "published": item.findtext("pubDate"),
                    "source": (item.find("source").text if item.find("source") is not None else ""),
                })
            time.sleep(1)
        signals["google_news"] = news[:40]
        statuses.append(("google_news", "ok", f"{len(news)} articles, last 7 days"))
    except Exception as e:
        statuses.append(("google_news", "failed", str(e)[:120]))

    # Exploding Topics (free page, often blocked; best effort)
    try:
        html = fetch_text("https://explodingtopics.com/hr-topics")
        topics = re.findall(r'"keyword":"([^"]+)"', html)[:25]
        if not topics:
            topics = [t for t in re.findall(r"<h3[^>]*>([^<]{4,40})</h3>", html)][:25]
        signals["exploding_topics"] = topics
        statuses.append(("exploding_topics", "ok" if topics else "failed",
                         f"{len(topics)} topics scraped" if topics else "page fetched but no topics parsed"))
    except Exception as e:
        statuses.append(("exploding_topics", "failed", str(e)[:120]))

    save_json(out_file, signals)
    for name, status, detail in statuses:
        record_source_status(name, status, detail)
    print(f"Signals done -> {out_file}")
    for name, status, detail in statuses:
        print(f"  {name}: {status} ({detail})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=["gtrends", "x", "reddit", "signals"])
    args = ap.parse_args()
    runners = {"gtrends": run_gtrends, "x": run_x, "reddit": run_reddit, "signals": run_signals}
    if args.only:
        runners[args.only]()
    else:
        for name, fn in runners.items():
            try:
                fn()
            except Exception as e:
                record_source_status(name, "failed", str(e)[:200])
                print(f"{name} FAILED: {e}")
