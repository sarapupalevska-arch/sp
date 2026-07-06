"""Shared helpers for the JobRack trend radar."""
import csv
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CONFIG = ROOT / "config"
REPORTS = ROOT / "reports"

# One CSV schema for all LinkedIn post data, regardless of collection method.
CSV_FIELDS = [
    "founder", "company", "post_url", "date", "format", "hook_text",
    "full_text", "reactions", "comments", "reposts", "theme", "pillar",
    "cta_type", "source", "collected_at",
]

COMBINED_CSV = DATA / "linkedin" / "combined.csv"

CACHE_MAX_AGE_DAYS = 6  # never re-fetch data younger than this


def load_yaml(name):
    with open(CONFIG / name) as f:
        return yaml.safe_load(f)


def load_env():
    """Read .env at project root into a dict without external deps."""
    env = {}
    env_path = ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    # environment variables win over .env
    env.update({k: v for k, v in os.environ.items()})
    return env


def today():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def cache_fresh(path, max_age_days=CACHE_MAX_AGE_DAYS):
    """True if a cache file exists and is younger than max_age_days."""
    p = Path(path)
    if not p.exists():
        return False
    age = time.time() - p.stat().st_mtime
    return age < max_age_days * 86400


def save_json(path, obj):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False, default=str)


def load_json(path):
    with open(path) as f:
        return json.load(f)


def append_rows(rows, csv_path=COMBINED_CSV):
    """Append normalized rows to the combined CSV, de-duping on (founder, date, hook_text)."""
    csv_path = Path(csv_path)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    existing = set()
    if csv_path.exists():
        with open(csv_path, newline="") as f:
            for r in csv.DictReader(f):
                existing.add((r.get("founder"), r.get("date"), (r.get("hook_text") or "")[:80]))
    is_new_file = not csv_path.exists()
    written = 0
    with open(csv_path, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS, extrasaction="ignore")
        if is_new_file:
            w.writeheader()
        for row in rows:
            key = (row.get("founder"), row.get("date"), (row.get("hook_text") or "")[:80])
            if key in existing:
                continue
            existing.add(key)
            w.writerow(row)
            written += 1
    return written


def read_combined(csv_path=COMBINED_CSV):
    csv_path = Path(csv_path)
    if not csv_path.exists():
        return []
    with open(csv_path, newline="") as f:
        return list(csv.DictReader(f))


def record_source_status(source, status, detail=""):
    """Log data source health for the report's Data Health section."""
    log = DATA / "source_status.json"
    entries = load_json(log) if log.exists() else {}
    entries[source] = {
        "status": status,  # ok | failed | skipped | needs_input
        "detail": detail,
        "at": datetime.now(timezone.utc).isoformat(),
    }
    save_json(log, entries)
