# Project notes

## Shopping & fashion site tracker

Living list of fashion, footwear, and resale sites, with a trust rating on each.
Sara adds to this regularly — when she mentions new brands or sites, append them here.

**Canonical copy (edit this one):**
https://docs.google.com/spreadsheets/d/1RN1gx2gb2eJE2jLvxUy0vvJ2RagZ3NnlUuhHw10odyk/edit

- Drive file ID: `1RN1gx2gb2eJE2jLvxUy0vvJ2RagZ3NnlUuhHw10odyk`
- Title: "Fashion & Shopping Sites — Aug 2026"
- Owner: sarapupalevska@gmail.com, in My Drive

**Local copies** in `out/` — regenerate these when the sheet changes so they stay in sync:
- `out/shopping-sites.xlsx` — formatted version, color-coded by trust, plus a Summary tab of counts
- `out/shopping-sites.csv` — plain export, matches the Google Sheet exactly

**Columns:** Name · Category · Subcategory · Website · Trust · Notes · Items viewed

**Categories in use** (this is also the sheet's sort order, then alphabetical within each):
Bags & Purses · Clothing · Footwear · Accessories · Beauty · Resale · Aggregator ·
Marketplace · Home · Supplements · Food · Travel · Utility

**Scope:** every commerce site Sara visits, not only fashion. Jobs, social, streaming and
news sites are deliberately excluded.

**Coverage so far:** browser history 14-22 Aug 2026, 154 sites.

**Rebuild the workbook** after editing the CSV: `python3 scripts/build-shopping-sheet.py`

**Trust values:** `OK` · `Caution` · `Avoid`
Ratings are a judgement call on authenticity risk, data/privacy practices, and seller
legitimacy — not a formal security scan. Say so when presenting them.

**To add rows:** read the sheet first (`read_file_content` with the file ID above) so you
append rather than overwrite. `out/shopping-sites.csv` mirrors it and is the easiest thing
to append to; re-upload the whole merged file when done.

**Important — the Drive connector cannot edit sheet contents.** `update_file` changes only
title and parent. Updating the data means `create_file` with the full merged CSV, which mints
a NEW file ID and URL. So each update: create the new sheet, rename the old one
"(superseded <date>)", and replace the file ID in this document. Warn Sara that the link
changed. Old versions are left in Drive rather than trashed — ask before deleting any.

**Purchases confirmed in history** — worth not double-buying:
- NYRVA, 21 Aug, order #13468 — HIRAYA Shoulder Bag + Mini in Blue (~17,700 MKD)
- Coslovemetics, 14 Aug — Korean haircare/skincare, paid via Halkbank 3-D Secure
