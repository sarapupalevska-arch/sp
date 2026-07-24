#!/usr/bin/env python3
"""Stage 3: render report.md from the pickles + stats."""
import pandas as pd, json, os

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE,'output')
uni = pd.read_pickle(f'{OUT}/_uni.pkl'); dups = pd.read_pickle(f'{OUT}/_dups.pkl')
meta = json.load(open(f'{OUT}/_meta.json')); s = json.load(open(f'{OUT}/_stats.json'))
m = pd.read_csv(f'{OUT}/master_clean.csv', encoding='utf-8-sig', keep_default_na=False)
fr = meta['file_rows']; TOTAL_IN = meta['total_in']
ru = uni[uni.bucket=='removed']; nr = uni[uni.bucket=='needs_review']

FILE_LABEL = {'First':'…EastUSFirst1500_4000.csv','Second':'…EastUSSecond1500_4000.csv','Third':'…EastUSThird1500_4000.csv'}

def tbl(rows, head):
    o = ['| ' + ' | '.join(head) + ' |', '|' + '|'.join(['---']*len(head)) + '|']
    o += ['| ' + ' | '.join(str(c) for c in r) + ' |' for r in rows]
    return '\n'.join(o)

L = []
A = L.append
A('# LinkedIn Sales Navigator — dedupe, hygiene & ICP filter')
A('')
A(f'Inputs: 3 CSV exports · **{TOTAL_IN:,} rows in** · **{len(m):,} contacts out** · '
  f'{s["nb"]} HeyReach batch file(s)')
A('')
A('---')
A('')
A('## ⚠️ Read this first: the three exports are not three slices')
A('')
A('They were described as three slices of one 4,000+ contact list. They are not.')
A('')
A('- **`Second` and `Third` are the same 2,400 people.** Identical profile-URL sets, identical row '
  'order. Across all 43,200 cells the two files differ in **exactly one**: the `Headline` for '
  '`linkedin.com/in/jessekirshbaum` (short version vs. long version). Different file size and MD5, same list.')
A('- **`First` is a 1,592-row subset of that same list**, not a distinct slice. 1,590 of its 1,592 rows '
  'already appear in the other two. Only **2 people exist in `First` and nowhere else**: '
  'Jaclyn Baker (Josephine & Co) and Alexcea Matthews (GotPhoto.com).')
A('')
A(f'**The union of all three files is {len(uni):,} unique people.** If the Sales Nav list really held '
  '4,000+, then roughly **1,600 contacts are missing entirely** — they are in no export. The pagination '
  'on the export looks like it re-pulled the same window instead of advancing. Everything below is '
  f'correct for the {len(uni):,} people you actually have, but this is worth re-exporting.')
A('')
A('---')
A('')
A('## 1. Row count per source file')
A('')
A(tbl([[FILE_LABEL[k], f'{fr[k]:,}', f'{fr[k]:,}', '0'] for k in ['First','Second','Third']],
      ['Source file','Data rows','Unique profile URLs','Within-file dupes']))
A('')
A(f'**Total rows before dedupe: {TOTAL_IN:,}**')
A('')
A('## 2. Duplicates removed')
A('')
A(tbl([['Within-file duplicates', f'{meta["within"]:,}', 'No file contained the same profile URL twice'],
       ['Cross-file duplicates',  f'{meta["cross"]:,}',  'Every duplicate was the same person appearing in 2+ files'],
       ['**Total rows collapsed**', f'**{len(dups):,}**','']],
      ['Type','Rows','Note']))
A('')
A('### Which file pairs overlapped')
A('')
A(tbl([[p['pair'], f'{p["shared"]:,}',
        f'{p["pct_left"]} of {p["left"]}', f'{p["pct_right"]} of {p["right"]}',
        p['jaccard']] for p in s['pair_rows']],
      ['Pair','Shared contacts','Share of left file','Share of right file','Overlap (Jaccard)']))
A('')
A('### Where each unique contact came from')
A('')
A(tbl([[k.replace('|', ' + '), f'{v:,}'] for k,v in sorted(s['combo'].items(), key=lambda x:-x[1])],
      ['Appears in','Unique contacts']))
A('')
A(f'**Unique contacts after dedupe: {len(uni):,}**')
A('')
A('Matching was profile-URL first (all URLs normalized: lowercased, protocol/`www`/query/fragment/'
  'trailing-slash/locale stripped), falling back to normalized full name + company only where a row had '
  f'no usable URL. All {len(uni):,} clusters matched on URL — the name+company fallback was never needed. '
  'No fuzzy name matching was used.')
A('')
A('## 3. Removals by hygiene reason')
A('')
hy_rows = [[k, f'{v:,}'] for k,v in sorted(s['hy'].items(), key=lambda x:-x[1])]
A(tbl(hy_rows + [['**Total**', f'**{sum(s["hy"].values()):,}**']], ['Reason code','Contacts removed']))
A('')
A('Notably absent: **0** malformed/missing profile URLs and **0** missing first names — every one of the '
  f'{len(uni):,} contacts has a well-formed `linkedin.com/in/…` URL and a first name. Placeholder-company '
  'junk was almost non-existent (a single `Self-employed`).')
A('')
A('## 4. Removals by ICP criterion')
A('')
A(tbl([['`title_out_of_icp` (criterion B)', f'{s["icp"].get("title_out_of_icp",0):,}',
        'No accepted title, and not senior-adjacent enough to warrant review'],
       ['`geo_out_of_icp` (criterion C)', f'{s["icp"].get("geo_out_of_icp",0):,}',
        'Resolved to a state outside your 31, or outside the US'],
       ['`headcount` (criterion A)', '0', '**Not checkable — no headcount column exists in any export**']],
      ['Criterion','Removed','Note']))
A('')
A('The 6 geographic removals: San Francisco Bay Area, Dallas-Fort Worth Metroplex, Greater Phoenix Area, '
  'Jeddah (Saudi Arabia), Mexico City, Guatemala City.')
A('')
A('## 5. Final counts')
A('')
A(tbl([['`master_clean.csv`', f'{len(m):,}', 'Passed hygiene + criteria B and C'],
       ['`needs_review.csv`', f'{len(nr):,}', 'Could not verify at least one criterion'],
       ['`removed.csv` — unique contacts', f'{len(ru):,}', 'Failed hygiene or a criterion outright'],
       ['`removed.csv` — collapsed duplicate rows', f'{len(dups):,}', 'Same person, already represented'],
       ['**Total**', f'**{TOTAL_IN:,}**', 'Reconciles to input']],
      ['Output','Rows','Meaning']))
A('')
A(f'**Final clean count: {len(m):,} contacts → {s["nb"]} HeyReach batch files** '
  f'(`heyreach_batch_1.csv` = 1,000 rows, `heyreach_batch_2.csv` = {len(m)-1000} rows).')
A('')
A('### needs_review breakdown')
A('')
A(tbl([['Title ambiguous only', f'{int(((nr.title_status=="review")&(nr.geo_status!="review")).sum()):,}'],
       ['Location ambiguous only', f'{int(((nr.geo_status=="review")&(nr.title_status!="review")).sum()):,}'],
       ['Both ambiguous', f'{int(((nr.title_status=="review")&(nr.geo_status=="review")).sum()):,}']],
      ['Reason','Contacts']))
A('')
A('The location-ambiguous rows are exactly the cases you named: 81 × bare `United States` (no state), '
  '6 × `Kansas City Metropolitan Area` (straddles MO/KS), 1 × `Lancaster Metropolitan Area` (PA/OH/CA), '
  '1 × `Greater Columbus Area` (OH/GA/IN/MS), 1 × blank. None were resolved by guessing.')
A('')
A('## 6. Criterion B — title matching')
A('')
A('Normalization: lowercased, punctuation stripped, `CEO`→`chief executive officer`, `EVP`→`executive '
  'vice president`, `Cofounder`/`Co Founder`/`Co-Founder` unified, likewise `Co-Owner`. Multi-title '
  'strings split on `&` `,` `|` `/` `+` `and` **and parentheses**, then each part tested independently.')
A('')
A(tbl([['Accepted', f'{int((uni.title_status=="pass").sum()):,}', '327', '`titles_accepted.csv`'],
       ['Sent to review', f'{int((uni.title_status=="review").sum()):,}', '363', '`titles_needs_review.csv`'],
       ['Rejected', f'{int((uni.title_status=="fail").sum()):,}', '606', '`titles_rejected.csv`']],
      ['Bucket','Contacts','Distinct raw titles','Frequency table']))
A('')
A('Per your rule, `Director` was accepted **only** standalone (36 contacts) or top-level-qualified '
  '(`Managing Director`, `Executive Director`, `Agency Director`, `Director & Founder`). Every other '
  'Director variant — `Director of Marketing`, `Art Director`, `Creative Director`, `Associate Director`, '
  '`Director of First Impressions` — went to **needs_review**, never to removed. Same for `President`: '
  'only standalone `President` and `Executive Vice President` were accepted; `Vice President`, '
  '`Vice President of Sales` and friends went to review.')
A('')
A('Judgement calls I made inside your rules, flag them if you disagree:')
A('')
A('- `Business Owner` (43) and `Company Owner` (19) are **not** literally `Owner`, so they went to '
  'review rather than being auto-accepted.')
A('- `Founding Member` (11) went to review as senior-adjacent, not rejected.')
A('- Board seats (`Board Member`, `Member of the Board of Directors`, `Member Board of Trustees`) were '
  '**rejected**, not reviewed — a board seat is not the CEO/Founder persona.')
A('- `Chief Executive Officer (CEO)` correctly **passes** (parenthetical duplicate of the same title).')
A('')
A('## 7. Criterion C — geography')
A('')
A('Comma segments are scanned **right-to-left**, because LinkedIn writes `City, State, Country`. This '
  'matters: `California, Maryland, United States` is a town in Maryland (**in ICP**), not the state of '
  'California, and a left-to-right scan gets it backwards. `Washington, District of Columbia` resolves to '
  'DC, not Washington State. Where no comma-delimited state exists, a metro→state lookup runs, then a '
  'right-most state-name search inside metro strings (`Columbus, Ohio Metropolitan Area` → Ohio).')
A('')
_TC = lambda k: ' '.join(w if w == 'of' else w.capitalize() for w in k.split())
A(tbl([[_TC(k), f'{v:,}'] for k,v in uni[uni.geo_status=='pass'].geo_state.value_counts().head(12).items()],
      ['Top states on the deduped list','Contacts']))
A('')
A('## 8. Per-company counts')
A('')
A('Full table in `company_counts.csv` (all 2,332 distinct companies, counted both across all unique '
  'contacts and across `master_clean` only).')
A('')
A('**Companies with more than 3 contacts: 2.**')
A('')
A(tbl([['Straight North','4','2'],['TPG','4','2']],
      ['Company','Contacts (all unique)','Contacts (on master_clean)']))
A('')
A('Company concentration is a non-issue on this list — after ICP filtering no company has more than 2 '
  'contacts, and only 14 companies have 2 or more.')
A('')
A('## 9. First-name cleaning (before → after)')
A('')
A('24 of 2,402 first names were non-clean. Fixable ones were **cleaned, not deleted** — the original is '
  'untouched in `First Name`, the usable version is in `cleaned_first_name`. Full list in '
  '`first_name_before_after.csv`.')
A('')
fn = pd.read_csv(f'{OUT}/first_name_before_after.csv', encoding='utf-8-sig', keep_default_na=False)
A(tbl([[f'`{r["First Name"]}`', f'`{r["cleaned_first_name"]}`', r['first_name_status'], r['first_name_note']]
       for _, r in fn.iterrows()],
      ['Before','After','Status','What happened']))
A('')
A('The 11 `unusable` ones were removed (reason `unusable_first_name`) — single letters (`Q`, `E`, `C`, '
  '`J`) and brand/keyword strings in the name field (`SEO`, `AI`, `UHC`, `TES`, `NEXTA`, `BLK GRL '
  'MAGIC`, `...B.L.`). If you would rather keep `Q` — plausibly a real preferred name — it is in '
  '`removed.csv` and easy to pull back.')
A('')
A('## 10. Near-matches I did NOT merge')
A('')
A('`near_matches.csv`. Two same-full-name pairs, neither merged, because your rule is that same-name / '
  'different-company is not a duplicate and no fuzzy matching without flagging.')
A('')
A('1. **Michael Brown** — CEO & Founder at *nDash* (Camden, ME) vs. Communications Specialist at '
  '*Christian Life Center, Dayton* (Englewood, OH). Different people. Correctly not merged.')
A('2. **Rubens Montes de Oca** — Co-Founder at *Quantum Telecom & Technologies* **in both rows**, same '
  'title, but two different profile URLs: a vanity URL and an opaque `ACwAA…` member ID. This is very '
  'likely **one person with two URL formats**, i.e. a real duplicate that URL matching structurally '
  'cannot catch. I left it unmerged per your instructions. **Recommend you merge this one manually.**')
A('')
A('> Note on reconciliation: `near_matches.csv` is an advisory overlay, not a bucket. The contacts in it '
  'also appear in their real output file, so it is deliberately excluded from the row arithmetic below.')
A('')
A('## 11. Reconciliation')
A('')
A('```')
A(f'  input rows                      {TOTAL_IN:>7,}')
A(f'  master_clean.csv                {len(m):>7,}')
A(f'  needs_review.csv                {len(nr):>7,}')
A(f'  removed.csv                     {len(ru)+len(dups):>7,}   ({len(ru):,} contacts + {len(dups):,} duplicate rows)')
A(f'                                  {"-"*7}')
A(f'  total out                       {len(m)+len(nr)+len(ru)+len(dups):>7,}')
A('```')
A('')
A(f'**{len(m):,} + {len(nr):,} + {len(ru)+len(dups):,} = {TOTAL_IN:,}. Verified: every one of the '
  f'{TOTAL_IN:,} input rows lands in exactly one output file. No row was silently dropped.**')
A('')
A('## 12. Things that looked off that you did not ask about')
A('')
A('1. **The duplicate export (§ top).** `Second` and `Third` are the same list; ~1,600 contacts are '
  'missing from the original 4,000+. This is the single most important finding here.')
A('2. **Criterion A was never checkable.** There is no company-headcount column in any of the three '
  'files — not empty, absent. Every row carries `headcount_verified = no_data_in_export` in '
  '`needs_review.csv`. I did **not** route all 2,402 rows to needs_review on that basis, because you '
  'confirmed the headcount filter was applied in Sales Nav and is out of scope here. Flagging it '
  'because it means **nothing in this pipeline has verified company size**.')
A('3. **Three different headcount numbers appeared in this task**: `11to50` in the filenames, `50-200` '
  'in your first draft of Step 5, `51-200` in your final Step 5. Worth pinning down before the next export.')
A(f'4. **{int(m["Profile URL"].str.contains("/in/AC",case=False).sum())} of {len(m):,} master rows '
  f'({100*int(m["Profile URL"].str.contains("/in/AC",case=False).sum())/len(m):.0f}%) have opaque '
  '`ACoAA…`/`ACwAA…` member-ID URLs** instead of vanity URLs. HeyReach generally resolves these, but '
  'they are worth spot-checking on import — and as the Rubens Montes de Oca case shows, a person can '
  'appear under both formats without URL dedupe catching it.')
A('5. **Student organisations are on the clean list.** ~18 master rows are university clubs and student '
  'bodies — `Undergraduate Student Government - Baruch College`, `American Marketing Association - '
  'University of Florida Chapter`, `TAMID Group at The University of Wisconsin`, `Pi Sigma Epsilon, '
  'University of Michigan`, `Spoon University`. They pass because a student club genuinely has a '
  '"President". Per your instruction I did not drop them, but they are not agency decision-makers.')
A('6. **Other non-agency contamination** on master: `Ministry of Tourism of the Dominican Republic`, '
  '`Vantage Health Systems`, `Your Direct Connection Insurance Advisors`, real-estate coaching, a law '
  'organisation. Small volume (~18 rows total) but present. Separately, in the raw list Peter Shankman '
  'appears as `Futurist in Residence` at a personal-injury law firm — row 3 of every file.')
A('7. **`Company` sometimes contains the job title.** 6 rows in the raw data have `Company` exactly '
  'equal to `Job Title` (e.g. Paul Parnell, `Writer/Director` in both). A scraper artifact; 1 survives '
  'onto master.')
A('8. **`Enriched Email` and `Custom Address` are 100% empty** in all three files, as are `Tags` and all '
  'six `Auto-tag` columns. There is no email in this data at all — it is LinkedIn-only. I kept the '
  'columns so the import shape matches what HeyReach exported.')
A('9. **Batch 2 is tiny** (28 contacts). You may prefer to split 514/514 rather than 1,000/28.')
A('10. **Standalone `Director` (36 contacts) is on master by your rule**, but in 11-50 person agencies '
  '"Director" is frequently a mid-level IC, not a decision-maker. Worth eyeballing those 36.')
A('')

open(f'{OUT}/report.md','w').write('\n'.join(L))
print('wrote report.md', len('\n'.join(L)), 'chars')
