# LinkedIn Sales Navigator — dedupe / hygiene / ICP pipeline

Merges multiple Sales Navigator (HeyReach-format) CSV exports into one
deduplicated, ICP-filtered master list, with a full audit trail.

## Running

```bash
python3 pipeline.py      # load, normalize, dedupe, hygiene, ICP  -> output/_*.pkl
python3 outputs.py       # write the deliverable CSVs, assert reconciliation
python3 make_report.py   # render output/report.md
```

Set `SRC` at the top of `pipeline.py` to the directory holding the source CSVs.

## Outputs (written to `output/`, gitignored)

| File | Contents |
|---|---|
| `master_clean.csv` | Final list. Original column order + `source_files` + `cleaned_first_name` |
| `heyreach_batch_N.csv` | `master_clean` split into 1,000-row import chunks |
| `removed.csv` | Every dropped row, with `removal_reason` and `removal_detail` |
| `needs_review.csv` | Contacts where an ICP criterion could not be verified |
| `near_matches.csv` | Same-name pairs deliberately left unmerged (advisory) |
| `titles_{accepted,rejected,needs_review}.csv` | Raw-title frequency tables |
| `company_counts.csv` | Per-company contact counts, `flag_over_3` |
| `first_name_before_after.csv` | Every first name that was cleaned or rejected |
| `report.md` | Full narrative report |

## Matching rules

- **Dedupe** on normalized profile URL first (lowercase; protocol, `www`,
  query/fragment, trailing slash and locale prefix stripped — locale handled both
  as path segment `/nl/in/…` and as subdomain `nl.linkedin.com`). Falls back to
  normalized full name + company only when a row has no usable URL. No fuzzy
  matching; same name + different company is not a duplicate.
- **Cluster winner** is the row with the most non-empty fields; non-empty values
  from the other copies are merged in where the winner is missing them.
- **Titles** are split on `& , | / +`, `and` and parentheses, then each part is
  matched against the accepted list. `Director` and `President` variants that are
  not clearly top-level go to `needs_review`, never to `removed`.
- **Geography** scans comma segments right-to-left, because LinkedIn writes
  `City, State, Country` — `California, Maryland, United States` is in Maryland.
  Genuinely ambiguous locations (bare `United States`, `Kansas City`, `Columbus`,
  `Lancaster`) go to `needs_review` rather than being guessed.

## Reconciliation

`outputs.py` asserts that every input row lands in exactly one of
`master_clean.csv`, `needs_review.csv` or `removed.csv`. It fails loudly if the
arithmetic does not balance. `near_matches.csv` is an advisory overlay and is
excluded from that count by design.
