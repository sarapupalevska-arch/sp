# Coloring book pipeline

Builds a KDP-ready kids' coloring book from a theme:
ideas -> AI line art -> automatic QA -> review sheet -> interior PDF -> listing text.

## Setup
```
pip install -r requirements.txt
export OPENAI_API_KEY=...        # never commit this; output/ and .env are git-ignored
```

## Run
```
python3 run.py --dry-run         # offline test with placeholder art, no API cost
python3 run.py                   # real book: dinosaurs, ages 3-5, 30 pages
python3 run.py --theme "farm animals" --age 3-5 --pages 30
```
Output goes to `output/<theme>/`:
- `review_sheet.png` - every page on one image; rejected pages outlined in red. **Look at this before uploading.**
- `interior.pdf` - 8.5x11 in, 300 dpi, black and white, blank page behind each picture
- `listing.txt` - title, subtitle, description, 7 keywords for KDP

Runs are resumable: already generated pages in `raw/` are skipped. To regenerate a
rejected page, delete its file in `raw/` and run again.

## QA checks (pipeline/qa.py)
gray shading, almost-empty page, too much ink, drawing cut off at the edge, near-duplicate pages.
Pages that fail are left out of the PDF. KDP needs at least 24 pages.

## Still manual
- Look through the review sheet (a minute), and check for odd anatomy, garbled shapes, or anything that looks like an existing character.
- Make a cover (KDP Cover Creator works) and upload interior + cover in KDP.
- In KDP title setup, answer YES to "AI-generated images".
