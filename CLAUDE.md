# Project notes

## Shopping & fashion site tracker

Living list of fashion, footwear, and resale sites, with a trust rating on each.
Sara adds to this regularly — when she mentions new brands or sites, append them here.

**Canonical copy (edit this one):**
https://docs.google.com/spreadsheets/d/13iBdYt_0JhLCQy9eEV6udCcp39kMSbzNLt5njOCgN0Y/edit

- Drive file ID: `13iBdYt_0JhLCQy9eEV6udCcp39kMSbzNLt5njOCgN0Y`
- Title: "Fashion & Shopping Sites — Aug 2026"
- Owner: sarapupalevska@gmail.com, in My Drive

**Local copies** in `out/` — regenerate these when the sheet changes so they stay in sync:
- `out/shopping-sites.xlsx` — formatted version, color-coded by trust, plus a Summary tab of counts
- `out/shopping-sites.csv` — plain export, matches the Google Sheet exactly

**Columns:** Name · Category · Subcategory · Website · Trust · Notes

**Categories in use:** Bags & Purses · Clothing · Footwear · Resale · Aggregator · Marketplace · Utility

**Trust values:** `OK` · `Caution` · `Avoid`
Ratings are a judgement call on authenticity risk, data/privacy practices, and seller
legitimacy — not a formal security scan. Say so when presenting them.

**To add rows:** read the sheet first (`read_file_content` with the file ID above) so you
append rather than overwrite, then update it. The Google Sheet is the source of truth.
