#!/usr/bin/env python3
"""Stage 2: write deliverables + report.md and prove the arithmetic reconciles."""
import pandas as pd, numpy as np, os, json, itertools, glob, re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(HERE, 'output')
uni  = pd.read_pickle(os.path.join(OUT, '_uni.pkl'))
dups = pd.read_pickle(os.path.join(OUT, '_dups.pkl'))
meta = json.load(open(os.path.join(OUT, '_meta.json')))
ORIG = meta['orig_cols']; file_rows = meta['file_rows']; TOTAL_IN = meta['total_in']
ORDER = ['First','Second','Third','Forth']

def w(df, name):
    p = os.path.join(OUT, name)
    df.to_csv(p, index=False, encoding='utf-8-sig')
    print(f'  wrote {name:28s} {len(df):>5} rows')
    return p

# ------------------------------------------------- master_clean
MASTER_COLS = ORIG + ['source_files', 'cleaned_first_name']
master = uni[uni.bucket == 'master'].copy()
master = master[MASTER_COLS]
w(master, 'master_clean.csv')

# ------------------------------------------------- removed
rm_uni = uni[uni.bucket == 'removed'].copy()
rm_uni['removed_stage'] = 'unique_contact'
rm_cols = ['source_file','source_row','source_files','removal_reason','removal_detail','removed_stage'] + ORIG
dups2 = dups.copy()
dups2['removed_stage'] = 'duplicate_row'
for c in ('source_files',):
    if c not in dups2: dups2[c] = ''
removed = pd.concat([rm_uni.reindex(columns=rm_cols), dups2.reindex(columns=rm_cols)], ignore_index=True)
w(removed, 'removed.csv')

# ------------------------------------------------- needs_review
nr = uni[uni.bucket == 'needs_review'].copy()
nr = nr.rename(columns={'removal_detail':'review_note'})
nr['review_reason'] = 'icp_unverifiable'
nr_cols = ['source_files','review_reason','review_note','geo_status','geo_detail',
           'title_status','title_detail','headcount_verified'] + ORIG
w(nr.reindex(columns=nr_cols), 'needs_review.csv')

# near-matches: advisory overlay, NOT part of reconciliation
near = pd.DataFrame(meta['near'])
w(near, 'near_matches.csv')

# ------------------------------------------------- HeyReach batches
CHUNK = 1000
nb = max(1, int(np.ceil(len(master)/CHUNK)))
for i in range(nb):
    w(master.iloc[i*CHUNK:(i+1)*CHUNK], f'heyreach_batch_{i+1}.csv')

# ------------------------------------------------- audit tables
tt = uni.groupby(['title_status','Job Title']).size().reset_index(name='count')
for st, fn in [('pass','titles_accepted.csv'),('fail','titles_rejected.csv'),('review','titles_needs_review.csv')]:
    t = tt[tt.title_status==st][['Job Title','count']].sort_values(['count','Job Title'], ascending=[False,True])
    w(t, fn)

cc = (uni.groupby('Company').size().reset_index(name='contacts_all_unique')
        .merge(uni[uni.bucket=='master'].groupby('Company').size().reset_index(name='contacts_on_master'),
               on='Company', how='left').fillna({'contacts_on_master':0}))
cc['contacts_on_master'] = cc['contacts_on_master'].astype(int)
cc = cc.sort_values(['contacts_all_unique','contacts_on_master','Company'], ascending=[False,False,True])
cc['flag_over_3'] = np.where((cc.contacts_all_unique > 3) | (cc.contacts_on_master > 3), 'YES', '')
w(cc, 'company_counts.csv')

fn_sample = uni[uni.first_name_status.isin(['cleaned','unusable'])][
    ['source_files','First Name','cleaned_first_name','first_name_status','first_name_note','Full Name','Company']]
w(fn_sample, 'first_name_before_after.csv')

# ------------------------------------------------- overlap stats
raw = []
for path in sorted(glob.glob('/root/.claude/uploads/f24803cb-81e8-5a62-a7d9-1798d6383e7d/*.csv')):
    sn = [k for k in ORDER if k in os.path.basename(path)][0]
    d = pd.read_csv(path, dtype=str, encoding='utf-8-sig', keep_default_na=False)
    raw.append((sn, set(d['Profile URL'].str.strip().str.lower())))
sets = dict(raw)
pair_rows = []
for a, b in itertools.combinations(ORDER, 2):
    inter = len(sets[a] & sets[b]); union = len(sets[a] | sets[b])
    pair_rows.append({'pair': f'{a} ∩ {b}', 'left': a, 'right': b, 'shared': inter,
                      'pct_left':  f'{100*inter/len(sets[a]):.1f}%',
                      'pct_right': f'{100*inter/len(sets[b]):.1f}%',
                      'jaccard':   f'{100*inter/union:.1f}%'})

# how many unique contacts appeared in each combination of files
combo = Counter(uni['source_files'])

# ------------------------------------------------- RECONCILE
n_master, n_removed, n_review = len(master), len(removed), len(nr)
total_out = n_master + n_removed + n_review
ok = (total_out == TOTAL_IN)
print(f'\n[reconcile] {n_master} master + {n_removed} removed + {n_review} needs_review'
      f' = {total_out}  vs input {TOTAL_IN}  -> {"OK" if ok else "MISMATCH"}')
assert ok, 'ROW ARITHMETIC DOES NOT RECONCILE'
# no contact in two buckets
assert uni.bucket.isin(['master','removed','needs_review']).all()
assert len(uni) == n_master + len(rm_uni) + n_review

hy = uni[uni.hygiene_reason!=''].hygiene_reason.value_counts()
icp = uni[uni.removal_reason.isin(['geo_out_of_icp','title_out_of_icp'])].removal_reason.value_counts()

json.dump({'pair_rows':pair_rows,'combo':dict(combo),'n_master':n_master,'n_removed':n_removed,
           'n_review':n_review,'nb':nb,'hy':hy.to_dict(),'icp':icp.to_dict(),
           'n_dups':len(dups),'n_rm_uni':len(rm_uni),'ok':ok},
          open(os.path.join(OUT,'_stats.json'),'w'), indent=1)
print('[stage2 done]')
