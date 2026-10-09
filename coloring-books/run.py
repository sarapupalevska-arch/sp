#!/usr/bin/env python3
"""Build one coloring book: ideas -> images -> QA -> review sheet -> PDF -> listing.

  python3 run.py                 # real run, needs OPENAI_API_KEY
  python3 run.py --dry-run       # offline test with placeholder art
"""
import argparse
from pathlib import Path

from pipeline.book import build_interior, page_count, review_sheet, write_listing
from pipeline.config import KDP_MIN_PAGES, BookSpec
from pipeline.generate import generate_pages
from pipeline.ideas import generate_ideas
from pipeline.qa import run_qa


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--theme", default="friendly dinosaurs")
    ap.add_argument("--age", default="3-5")
    ap.add_argument("--pages", type=int, default=30)
    ap.add_argument("--out", default="output")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    spec = BookSpec(theme=a.theme, age_range=a.age, pages=a.pages)
    out = Path(a.out) / spec.theme.replace(" ", "_")
    out.mkdir(parents=True, exist_ok=True)

    ideas = generate_ideas(spec, a.dry_run)
    print(f"{len(ideas)} page ideas")
    raws = generate_pages(spec, ideas, out, a.dry_run)
    results = run_qa(raws, out)

    good = sum(r.ok for r in results)
    for r in results:
        if not r.ok:
            print(f"  page {r.index} rejected: {'; '.join(r.problems)}")
    sheet = review_sheet(results, out)
    print(f"{good}/{len(results)} pages passed QA -> review sheet: {sheet}")

    if page_count(good) < KDP_MIN_PAGES:
        print(f"Only {page_count(good)} pages after QA (KDP needs {KDP_MIN_PAGES}). "
              "Delete the rejected raw/ images and re-run to regenerate them.")
        return
    print("Interior PDF:", build_interior(spec, results, out))
    print("Listing text:", write_listing(spec, results, out))
    print("Now look at the review sheet before uploading anything.")


if __name__ == "__main__":
    main()
