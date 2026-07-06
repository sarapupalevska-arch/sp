"""Generate the weekly brief: reports/brief-{date}.md

Sections (fixed): Three moves, Competitor pulse, Trend movers,
White space tracker, Data health. Under 600 words, no em dashes.
Every number is labelled with its source and date; missing data is stated,
never filled in.

Usage: python scripts/report.py
"""
import glob
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import DATA, REPORTS, load_json, load_yaml, today

ANALYSIS = DATA / "analysis.json"
STATUS = DATA / "source_status.json"


def latest(pattern):
    files = sorted(glob.glob(str(pattern)))
    return Path(files[-1]) if files else None


def load_or_none(path):
    return load_json(path) if path and Path(path).exists() else None


def gather():
    return {
        "analysis": load_or_none(ANALYSIS),
        "gtrends": load_or_none(latest(DATA / "trends" / "gtrends-*.json")),
        "race": load_or_none(latest(DATA / "trends" / "region-race-*.json")),
        "reddit": load_or_none(latest(DATA / "reddit" / "reddit-*.json")),
        "signals": load_or_none(latest(DATA / "trends" / "signals-*.json")),
        "status": load_or_none(STATUS) or {},
    }


def top_rising(gtrends, n=6):
    out = []
    if not gtrends:
        return out
    for set_name, kws in gtrends.get("results", {}).items():
        for kw, data in kws.items():
            for rq in data.get("rising_queries", []):
                if rq.get("flag"):
                    out.append((rq["query"], rq["value"], kw))
            change = (data.get("90d") or {}).get("pct_change")
            if change is not None and abs(change) >= 25:
                out.append((kw, f"{change:+.0f}% (90d)", set_name))
    return out[:n]


def reddit_questions(reddit, n=5):
    qs = []
    if not reddit:
        return qs
    for sub, threads in reddit.get("results", {}).items():
        for t in threads:
            if t.get("question_phrasing"):
                qs.append((t["question_phrasing"], f"r/{sub}", t.get("score", 0), t["url"]))
    qs.sort(key=lambda x: -(x[2] or 0))
    return qs[:n]


def three_moves(d):
    """Pick the 3 highest conviction moves from whatever data exists."""
    moves = []
    a = d["analysis"]
    rising = top_rising(d["gtrends"], 10)
    questions = reddit_questions(d["reddit"], 10)

    if a:
        # white space with engagement evidence
        ws = sorted([w for w in a["white_space"] if w.get("median_engagement")],
                    key=lambda w: (w["competitor_volume_pct"], -(w["median_engagement"] or 0)))
        if ws:
            w = ws[0]
            hooks = a.get("hooks") or {}
            best_hook = max(hooks, key=lambda h: hooks[h]["share_of_top_quartile"]) if hooks else "number-led"
            moves.append(
                f"**Own the '{w['differentiator']}' lane.** Competitor volume is only "
                f"{w['competitor_volume_pct']}% of tagged posts but median engagement on these "
                f"themes is {w['median_engagement']} (source: combined.csv analysis, {a['generated_at'][:10]}). "
                f"Format: {best_hook} hook, text post. Draft angle: JobRack take on "
                f"{w['themes'][0]}, framed with a concrete client number.")
    for q in questions[:2]:
        moves.append(
            f"**Answer a live buyer question.** \"{q[0]}\" is pulling {q[2]} upvotes on {q[1]} "
            f"(source: reddit export {d['reddit']['generated']}). Draft angle: answer it "
            f"verbatim as a LinkedIn post, question as the hook, JobRack client example as proof.")
    for r in rising[:2]:
        if len(moves) >= 3:
            break
        moves.append(
            f"**Ride the '{r[0]}' rise.** Google Trends shows {r[1]} for this term "
            f"(source: gtrends export {d['gtrends']['generated']}). Draft angle: myth-busting or "
            f"money-math post connecting the term to Eastern Europe hiring before competitors do.")
    # web-search collected signals (used when scripted sources are unavailable);
    # cap at 2 so at least one move can come from the white space data
    ws_news = (d["signals"] or {}).get("websearch_news", {})
    for item in ws_news.get("items", [])[:2]:
        if len(moves) >= 3:
            break
        moves.append(
            f"**React to a niche signal.** {item['title']} ({item['url']}, "
            f"source: web search {ws_news.get('collected')}). Draft angle: JobRack counter-take "
            f"or Eastern Europe equivalent, published before competitors respond.")
    # volume-only white space (no engagement data yet)
    if a and len(moves) < 3:
        ws = sorted(a["white_space"], key=lambda w: w["competitor_volume_pct"])
        if ws:
            w = ws[0]
            moves.append(
                f"**Own the '{w['differentiator']}' lane.** Only {w['competitor_volume_pct']}% of "
                f"tagged competitor posts touch it (source: combined.csv, {a['generated_at'][:10]}; "
                f"engagement data not yet available). Draft angle: {w['themes'][0]} post with a "
                f"concrete JobRack client example.")
    if not moves:
        moves.append("No data-backed moves available this run. Provide LinkedIn dumps and "
                     "re-run; trend sources alone did not return enough signal.")
    return moves[:3]


def build():
    d = gather()
    date = today()
    L = []
    L.append(f"# JobRack Trend Radar Brief, {date}\n")

    # 1. Three moves
    L.append("## 1. Three moves for this week")
    for i, m in enumerate(three_moves(d), 1):
        L.append(f"{i}. {m}")
    L.append("")

    # 2. Competitor pulse
    L.append("## 2. Competitor pulse")
    a = d["analysis"]
    if a:
        for f, rot in a["rotation"].items():
            posts = [p for p in a["posts"] if p["founder"] == f]
            key = "eng_per_1k" if a["normalization_available"] else "engagement"
            top = max(posts, key=lambda p: p.get(key) or 0, default=None)
            top_desc = "n/a"
            if top and top.get(key):
                link = top.get("post_url") or "no URL captured"
                top_desc = f"\"{top['hook_text'][:70]}\" ({top[key]} {key}, {link})"
            mix = ", ".join(f"{t} {p}%" for t, p in list(rot["theme_pct"].items())[:3])
            L.append(f"- **{f}**: {rot['post_count']} posts in dataset. Top post: {top_desc}. "
                     f"Theme mix: {mix}. (source: combined.csv, themes via {a['theme_method']})")
        if not a["normalization_available"]:
            L.append("- Note: engagement is raw, not per-1k-followers. Follower counts not yet provided.")
        L.append("- Theme mix shift vs last period: unavailable, first run has no prior period.")
    else:
        L.append("No LinkedIn post data collected yet. Manual dumps needed "
                 "(python scripts/parse_manual.py --checklist).")
    L.append("")

    # 3. Trend movers
    L.append("## 3. Trend movers")
    rising = top_rising(d["gtrends"])
    if rising:
        for q, v, ctx in rising:
            L.append(f"- Rising: \"{q}\" ({v}) [{ctx}] (source: Google Trends, {d['gtrends']['generated']})")
    else:
        L.append("- Google Trends: no data this run (see Data health).")
    race = d["race"]
    if race and race.get("growth_pct"):
        g = race["growth_pct"]
        pairs = ", ".join(f"{k} {v:+.0f}%" for k, v in g.items() if v is not None)
        L.append(f"- Region race (12m growth, same payload): {pairs} "
                 f"(source: region-race export; chart data in data/trends/)")
    qs = reddit_questions(d["reddit"])
    if qs:
        for q, sub, score, url in qs[:3]:
            L.append(f"- Reddit question: \"{q}\" ({sub}, {score} upvotes) {url}")
    else:
        L.append("- Reddit: no matching questions this run (see Data health).")
    ws_news = (d["signals"] or {}).get("websearch_news", {})
    for item in ws_news.get("items", [])[:4]:
        L.append(f"- Signal: {item['title']} (source: web search {ws_news.get('collected')})")
    L.append("- New voices on X: manual check needed, open data/x/x-search-urls-*.txt.")
    L.append("")

    # 4. White space tracker
    L.append("## 4. White space tracker")
    if a:
        for w in a["white_space"]:
            active = ", ".join(w["competitors_active"]) or "none"
            warn = " EARLY WARNING" if w["competitor_volume_pct"] >= 10 else ""
            L.append(f"- {w['differentiator']}: {w['competitor_volume_pct']}% of competitor "
                     f"posts, active: {active}.{warn}")
    else:
        L.append("Unavailable until LinkedIn post data is collected.")
    L.append("")

    # 5. Data health (compact: group network-blocked sources into one line)
    L.append("## 5. Data health")
    if d["status"]:
        blocked, other = [], []
        for src, info in sorted(d["status"].items()):
            if info["status"] == "failed" and ("ProxyError" in info["detail"]
                                               or "Max retries" in info["detail"]):
                blocked.append(src)
            else:
                other.append((src, info))
        for src, info in other:
            detail = info["detail"][:140]
            L.append(f"- {src}: {info['status']} ({detail}) [{info['at'][:10]}]")
        if blocked:
            L.append(f"- Blocked by network access in this environment: {', '.join(blocked)}. "
                     f"These run fine on a normal machine; re-run there.")
    else:
        L.append("- No sources have run yet.")
    needs = [s for s, i in d["status"].items() if i["status"] == "needs_input"]
    if needs:
        L.append(f"- Needs your input next run: {', '.join(sorted(needs))}.")
    L.append("")

    text = "\n".join(L).replace("—", ", ").replace("–", "-")
    out = REPORTS / f"brief-{date}.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text(text)
    words = len(text.split())
    print(f"Wrote {out} ({words} words)")
    if words > 600:
        print("WARNING: brief exceeds 600 words, trim before forwarding.")
    return out


if __name__ == "__main__":
    build()
