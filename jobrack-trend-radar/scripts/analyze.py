"""Analysis pipeline over the combined LinkedIn CSV.

Produces data/analysis.json with:
  1. theme tags per post (LLM if ANTHROPIC_API_KEY set, else keyword rules)
  2. pillar rotation map per founder (% per theme + week-by-week sequence)
  3. normalized engagement (per 1,000 followers) and theme rankings
  4. hook taxonomy and which hook types land in top-quartile engagement
  5. gap analysis vs JobRack differentiators (white space table)

Usage:
  python scripts/analyze.py
  python scripts/analyze.py --set-followers   # interactively record follower counts

Follower counts are stored in data/followers.json; the script prompts once per
run if any founder in the CSV is missing a count (skippable, normalization is
then marked unavailable for that founder).
"""
import argparse
import json
import re
import statistics
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import (DATA, load_env, load_json, read_combined,
                    record_source_status, save_json)

FOLLOWERS_FILE = DATA / "followers.json"
ANALYSIS_FILE = DATA / "analysis.json"

THEMES = [
    "money-math", "myth-busting", "origin-story", "hire-success-story",
    "compliance-education", "milestone", "delegation-advice",
    "region-advocacy", "ai-and-hiring", "candidate-voice", "data-report",
    "direct-promotion", "other",
]

# Keyword rules fallback for theme tagging. Order matters; max 2 themes kept.
THEME_RULES = [
    ("money-math", r"\$\d|salary|cost|save[sd]? (you |us )?\$|per hour|/hr|payroll cost|(half|fraction) (of |the )?(the )?(cost|price)|80% less|70% less"),
    ("myth-busting", r"myth|misconception|wrong about|people (think|believe|assume)|unpopular opinion|contrary to|actually isn'?t"),
    ("origin-story", r"(when|before) (i|we) (started|founded|quit)|years? ago,? i|my first (hire|business)|turning point|i almost (quit|failed)"),
    ("hire-success-story", r"(hired?|placed) (a|an|our|his|her|their)|success story|now (runs|manages|leads)|from \$\d+.*to \$\d+|her first (month|week)|joined us"),
    ("compliance-education", r"compliance|legal(ly)?|contractor vs|misclassif|employer of record|\bEOR\b|tax(es)?\b|labor law|mistake"),
    ("milestone", r"milestone|we (just )?(hit|crossed|reached)|(placed|hired) \d+|anniversar|celebrat|team of \d+"),
    ("delegation-advice", r"delegat|SOP|standard operating|manage (remote|your)|onboard|hiring process|interview (question|process)|how (i|we|to) (hire|manage)"),
    ("region-advocacy", r"eastern europe|south africa|philippines|latam|latin america|balkan|serbia|macedonia|bosnia|romania|timezone|time zone|english (level|skills)|talent pool"),
    ("ai-and-hiring", r"\bAI\b|artificial intelligence|chatgpt|claude|automation|ai agent|ai employee"),
    ("candidate-voice", r"in (his|her|their) (own )?words|meet [A-Z]|candidate (story|spotlight)|from the candidate"),
    ("data-report", r"report|survey(ed)?|we analyzed|data (from|on|shows)|\d+% of (companies|businesses|agencies)|benchmark"),
    ("direct-promotion", r"book a call|link in (bio|comments)|DM me|we('re| are) hiring for|apply now|get started|schedule|free (guide|checklist|call)"),
]

HOOK_TYPES = [
    ("number-led", r"^\W*\d|\d+%|\$\d"),
    ("question", r"\?\s*$|^(why|how|what|when|who|should|do you|have you|are you)\b"),
    ("i-did-x", r"^i ('|’)?(ve)? ?(did|built|made|hired|fired|spent|quit|sold|grew|learned|tried)|^i (just|once|recently)"),
    ("people-think-x", r"(people|everyone|most (founders|owners|agencies)) (think|believe|say|assume)|unpopular opinion"),
    ("list-promise", r"\b\d+ (ways|things|lessons|reasons|mistakes|steps|rules|signs)\b|here('|’)s (how|what|why)"),
    ("story-opener", r"^(last (week|month|year)|yesterday|in 20\d\d|two years ago|when i|she |he |meet )"),
    ("bold-claim", r"(never|always|only|best|worst|nobody|stop|quit)\b|is (dead|broken|a scam|overrated)"),
]

# JobRack differentiators for the white space tracker
JOBRACK_DIFFERENTIATORS = {
    "eastern-europe-narrative": ["region-advocacy"],
    "candidate-voice-stories": ["candidate-voice"],
    "agency-specific-ops-content": ["delegation-advice"],
    "retention-led-claims": ["hire-success-story", "compliance-education"],
    "original-data-reports": ["data-report"],
}


def tag_themes_rules(text):
    hits = []
    for theme, pattern in THEME_RULES:
        if re.search(pattern, text, re.I):
            hits.append(theme)
        if len(hits) == 2:
            break
    return hits or ["other"]


def tag_themes_llm(posts, env):
    """Batch theme tagging via the Anthropic API. Falls back silently on error."""
    try:
        import anthropic
    except ImportError:
        return None
    client = anthropic.Anthropic(api_key=env["ANTHROPIC_API_KEY"])
    results = []
    batch = 20
    for i in range(0, len(posts), batch):
        chunk = posts[i:i + batch]
        prompt = (
            "Classify each LinkedIn post into 1-2 themes from this list: "
            + ", ".join(THEMES)
            + ".\nReturn JSON: {\"tags\": [[\"theme1\", \"theme2\"], ...]} with one entry per post, in order.\n\n"
            + "\n\n".join(f"POST {j+1}:\n{p['full_text'][:1500]}" for j, p in enumerate(chunk))
        )
        resp = client.messages.create(
            model="claude-opus-4-8",
            max_tokens=2000,
            output_config={"format": {"type": "json_schema", "schema": {
                "type": "object",
                "properties": {"tags": {"type": "array", "items": {
                    "type": "array", "items": {"type": "string", "enum": THEMES}}}},
                "required": ["tags"], "additionalProperties": False,
            }}},
            messages=[{"role": "user", "content": prompt}],
        )
        text = next(b.text for b in resp.content if b.type == "text")
        results.extend(json.loads(text)["tags"])
    return results


def get_followers(founders, interactive=True):
    stored = load_json(FOLLOWERS_FILE) if FOLLOWERS_FILE.exists() else {}
    missing = [f for f in founders if f not in stored or not stored[f].get("count")]
    if missing and interactive and sys.stdin.isatty():
        print("Follower counts needed for engagement normalization (Enter to skip):")
        from common import today
        for f in missing:
            val = input(f"  {f} followers: ").strip().replace(",", "")
            if val.isdigit():
                stored[f] = {"count": int(val), "as_of": today()}
        save_json(FOLLOWERS_FILE, stored)
    return stored


def week_of(date_str):
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d")
        return d.strftime("%G-W%V")
    except (ValueError, TypeError):
        return "unknown"


def run(interactive=True):
    posts = read_combined()
    if not posts:
        record_source_status("analysis", "needs_input", "combined.csv is empty; nothing to analyze")
        print("No posts in data/linkedin/combined.csv. Collect data first "
              "(parse_manual.py or collect_linkedin.py).")
        return

    env = load_env()

    # 1. Theme tagging
    tags = None
    method = "keyword-rules"
    if env.get("ANTHROPIC_API_KEY"):
        try:
            tags = tag_themes_llm(posts, env)
            if tags:
                method = "llm"
        except Exception as e:
            print(f"LLM tagging failed ({e}); using keyword rules")
    if tags is None:
        tags = [tag_themes_rules(p["full_text"]) for p in posts]
    for p, t in zip(posts, tags):
        p["themes"] = t

    # Hook typing
    for p in posts:
        hook = (p.get("hook_text") or "").strip()
        p["hook_type"] = "other"
        for htype, pattern in HOOK_TYPES:
            if re.search(pattern, hook, re.I):
                p["hook_type"] = htype
                break

    founders = sorted({p["founder"] for p in posts})
    followers = get_followers(founders, interactive)

    # 3. Normalized engagement
    for p in posts:
        try:
            eng = int(p.get("reactions") or 0) + int(p.get("comments") or 0) + int(p.get("reposts") or 0)
        except ValueError:
            eng = 0
        p["engagement"] = eng
        fol = followers.get(p["founder"], {}).get("count")
        p["eng_per_1k"] = round(eng / fol * 1000, 2) if fol and eng else None

    # 2. Pillar rotation map
    rotation = {}
    for f in founders:
        fposts = sorted([p for p in posts if p["founder"] == f], key=lambda p: p.get("date") or "")
        theme_counts = Counter(t for p in fposts for t in p["themes"])
        total = sum(theme_counts.values()) or 1
        by_week = defaultdict(list)
        for p in fposts:
            by_week[week_of(p.get("date"))].extend(p["themes"])
        rotation[f] = {
            "post_count": len(fposts),
            "theme_pct": {t: round(c / total * 100, 1) for t, c in theme_counts.most_common()},
            "weekly_sequence": {w: themes for w, themes in sorted(by_week.items())},
        }

    # Theme rankings by median normalized engagement (per founder + pooled)
    def median_by_theme(subset, key):
        buckets = defaultdict(list)
        for p in subset:
            v = p.get(key)
            if v is not None:
                for t in p["themes"]:
                    buckets[t].append(v)
        return {t: round(statistics.median(vs), 2) for t, vs in
                sorted(buckets.items(), key=lambda kv: -statistics.median(kv[1]))}

    normalized_available = any(p["eng_per_1k"] is not None for p in posts)
    key = "eng_per_1k" if normalized_available else "engagement"
    theme_rank = {
        "metric": key,
        "pooled": median_by_theme(posts, key),
        "per_founder": {f: median_by_theme([p for p in posts if p["founder"] == f], key)
                        for f in founders},
    }

    # 4. Hook taxonomy vs top quartile
    engaged = sorted([p for p in posts if p.get(key)], key=lambda p: p[key])
    hooks = {}
    if engaged:
        q3 = engaged[int(len(engaged) * 0.75)][key]
        top = [p for p in engaged if p[key] >= q3]
        all_counts = Counter(p["hook_type"] for p in engaged)
        top_counts = Counter(p["hook_type"] for p in top)
        hooks = {h: {"share_of_all": round(all_counts[h] / len(engaged) * 100, 1),
                     "share_of_top_quartile": round(top_counts.get(h, 0) / len(top) * 100, 1)}
                 for h in all_counts}

    # 5. Gap analysis / white space
    pooled_counts = Counter(t for p in posts for t in p["themes"])
    total_tags = sum(pooled_counts.values()) or 1
    white_space = []
    for diff, themes in JOBRACK_DIFFERENTIATORS.items():
        vol = sum(pooled_counts.get(t, 0) for t in themes)
        med = [theme_rank["pooled"].get(t) for t in themes if theme_rank["pooled"].get(t)]
        white_space.append({
            "differentiator": diff,
            "themes": themes,
            "competitor_volume_pct": round(vol / total_tags * 100, 1),
            "median_engagement": round(statistics.median(med), 2) if med else None,
            "competitors_active": sorted({p["founder"] for p in posts
                                          if set(p["themes"]) & set(themes)}),
        })

    analysis = {
        "generated_at": datetime.utcnow().isoformat(),
        "post_count": len(posts),
        "founders": founders,
        "theme_method": method,
        "followers": followers,
        "normalization_available": normalized_available,
        "rotation": rotation,
        "theme_rank": theme_rank,
        "hooks": hooks,
        "white_space": white_space,
        "posts": [{k: p.get(k) for k in ("founder", "date", "post_url", "hook_text",
                                          "themes", "hook_type", "engagement",
                                          "eng_per_1k", "source")} for p in posts],
    }
    save_json(ANALYSIS_FILE, analysis)
    record_source_status("analysis", "ok",
                        f"{len(posts)} posts analyzed, themes via {method}, "
                        f"normalization {'on' if normalized_available else 'OFF (no follower counts)'}")
    print(f"Wrote {ANALYSIS_FILE} ({len(posts)} posts, themes via {method})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--set-followers", action="store_true")
    args = ap.parse_args()
    if args.set_followers:
        posts = read_combined()
        founders = sorted({p["founder"] for p in posts}) or []
        if not founders:
            from common import load_yaml
            founders = [c["name"] for c in load_yaml("competitors.yaml")["tier1"]]
        get_followers(founders, interactive=True)
    else:
        run()
