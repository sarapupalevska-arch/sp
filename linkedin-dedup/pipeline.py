#!/usr/bin/env python3
"""
LinkedIn Sales Navigator export: dedupe + hygiene + ICP filter.

Consumes the three HeyReach-style Sales Nav exports, produces one deduplicated,
ICP-filtered master list plus full audit trail.

Every input row lands in exactly one output file. See reconcile() at the bottom.
"""
import pandas as pd, numpy as np, glob, os, re, sys, unicodedata, json
from collections import defaultdict, Counter

SRC = '/root/.claude/uploads/f24803cb-81e8-5a62-a7d9-1798d6383e7d/'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- STEP 2: LOAD + NORMALIZE
def short_name(path):
    b = os.path.basename(path)
    for k in ('First', 'Second', 'Third'):
        if k in b:
            return k
    return b

def collapse(s):
    """Trim + collapse internal whitespace. NBSP and friends count as space."""
    if s is None:
        return ''
    s = str(s).replace(' ', ' ').replace('​', '')
    return re.sub(r'\s+', ' ', s).strip()

# Strip a locale prefix only when it is genuinely a locale, i.e. followed by a
# real path segment. Without the lookahead this eats "/in/" itself, since "in"
# is indistinguishable from a 2-letter locale code.
LOCALE_RE = re.compile(r'^[a-z]{2}(-[a-z]{2})?/(?=(in|pub|company|school)/)')
def norm_url(u):
    """lowercase, strip protocol/www/query/fragment/trailing slash/locale prefix."""
    u = collapse(u).lower()
    if not u:
        return ''
    u = re.sub(r'^https?://', '', u)
    u = u.split('?', 1)[0].split('#', 1)[0]
    u = u.rstrip('/')
    u = re.sub(r'^www\.', '', u)
    # locale as subdomain: nl.linkedin.com, de-de.linkedin.com
    u = re.sub(r'^[a-z]{2}(-[a-z]{2})?\.(?=linkedin\.com/)', '', u)
    if u.startswith('linkedin.com/'):
        rest = u[len('linkedin.com/'):]
        rest = LOCALE_RE.sub('', rest)          # /nl/in/foo -> in/foo
        u = 'linkedin.com/' + rest
    return u

def norm_text(s):
    """Aggressive normalization for matching only (never written to output fields)."""
    s = collapse(s).lower()
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r'[^a-z0-9 ]', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()

COMPANY_SUFFIX = r'\b(inc|llc|l l c|ltd|limited|co|corp|corporation|company|group|holdings|plc|gmbh|llp|lp|pllc|pc|sa|bv|nv)\b'
def norm_company(s):
    s = norm_text(s)
    s = re.sub(COMPANY_SUFFIX, ' ', s)
    return re.sub(r'\s+', ' ', s).strip()

frames = []
file_rows = {}
for path in sorted(glob.glob(SRC + '*.csv')):
    sn = short_name(path)
    df = pd.read_csv(path, dtype=str, encoding='utf-8-sig', keep_default_na=False)
    df.columns = [c.strip() for c in df.columns]
    ORIG_COLS = list(df.columns)
    for c in df.columns:
        df[c] = df[c].map(collapse)
    df.insert(0, 'source_file', sn)
    df.insert(1, 'source_row', np.arange(2, len(df) + 2))   # 1-based incl. header
    file_rows[sn] = len(df)
    frames.append(df)

work = pd.concat(frames, ignore_index=True)
work['row_uid'] = np.arange(len(work))
work['original_profile_url'] = work['Profile URL']
work['norm_profile_url']     = work['Profile URL'].map(norm_url)
work['norm_full_name']       = work['Full Name'].map(norm_text)
work['norm_company']         = work['Company'].map(norm_company)
TOTAL_IN = len(work)
print(f'[load] {TOTAL_IN} rows from {len(file_rows)} files: {file_rows}')

# ---------------------------------------------------------------- STEP 3: DEDUPE
URL_RE = re.compile(r'^linkedin\.com/in/[^/\s]+$')
work['url_valid'] = work['norm_profile_url'].map(lambda u: bool(URL_RE.match(u)))

def cluster_key(r):
    if r['url_valid']:
        return ('url', r['norm_profile_url'])
    if r['norm_full_name'] and r['norm_company']:
        return ('namecompany', r['norm_full_name'] + '|' + r['norm_company'])
    return ('rowuid', str(r['row_uid']))          # unmatchable -> its own cluster

work['cluster'] = work.apply(cluster_key, axis=1)

CONTENT_COLS = [c for c in work.columns if c not in
                ('source_file','source_row','row_uid','original_profile_url','norm_profile_url',
                 'norm_full_name','norm_company','url_valid','cluster')]
work['n_filled'] = (work[CONTENT_COLS].map(lambda v: str(v).strip() != '')).sum(axis=1)

winners, loser_rows, dup_pairs = [], [], []
within, cross = 0, 0
for key, grp in work.groupby('cluster', sort=False):
    grp = grp.sort_values(['n_filled', 'row_uid'], ascending=[False, True])
    win = grp.iloc[0].copy()
    srcs = sorted(set(grp['source_file']), key=lambda s: ['First','Second','Third'].index(s))
    win['source_files'] = '|'.join(srcs)
    win['n_source_files'] = len(srcs)
    win['dup_count'] = len(grp)
    win['match_basis'] = key[0]
    if len(grp) > 1:
        # merge non-empty values the winner is missing
        for c in CONTENT_COLS:
            if str(win[c]).strip() == '':
                for _, o in grp.iloc[1:].iterrows():
                    if str(o[c]).strip() != '':
                        win[c] = o[c]
                        break
        for _, o in grp.iloc[1:].iterrows():
            l = o.copy()
            l['removal_reason'] = 'duplicate'
            l['removal_detail'] = f"collapsed into row_uid {win['row_uid']} ({win['source_file']} row {win['source_row']}) via {key[0]}"
            l['source_files'] = '|'.join(srcs)
            loser_rows.append(l)
        # within vs cross accounting
        per_file = Counter(grp['source_file'])
        within += sum(v - 1 for v in per_file.values())
        cross  += len(per_file) - 1
        for a in range(len(srcs)):
            for b in range(a + 1, len(srcs)):
                dup_pairs.append((srcs[a], srcs[b]))
    winners.append(win)

uni = pd.DataFrame(winners).reset_index(drop=True)
dups = pd.DataFrame(loser_rows).reset_index(drop=True) if loser_rows else pd.DataFrame(columns=list(work.columns)+['removal_reason','removal_detail','source_files'])
print(f'[dedupe] {len(uni)} unique / {len(dups)} collapsed  (within={within} cross={cross})')

# ---------------------------------------------------------------- near-match report (NOT merged)
near = []
by_name = defaultdict(list)
for i, r in uni.iterrows():
    if r['norm_full_name']:
        by_name[r['norm_full_name']].append(i)
for nm, idxs in by_name.items():
    if len(idxs) > 1:
        for a in range(len(idxs)):
            for b in range(a + 1, len(idxs)):
                ra, rb = uni.loc[idxs[a]], uni.loc[idxs[b]]
                near.append({
                    'reason': 'same_full_name_different_company_not_merged',
                    'full_name': ra['Full Name'],
                    'company_a': ra['Company'], 'url_a': ra['original_profile_url'],
                    'title_a': ra['Job Title'], 'location_a': ra['Location'], 'source_a': ra['source_files'],
                    'company_b': rb['Company'], 'url_b': rb['original_profile_url'],
                    'title_b': rb['Job Title'], 'location_b': rb['Location'], 'source_b': rb['source_files'],
                })
print(f'[near-match] {len(near)} same-name pairs left unmerged')

# ---------------------------------------------------------------- STEP 4: HYGIENE
CRED = r'\b(mba|phd|ph d|md|cpa|cfa|pmp|msc|bsc|ma|ms|bs|ba|jd|esq|rn|dds|do|mph|cfp|cissp|pe|aia|scrum|csm|cmo|ceo)\b'
JUNK_CO = {'self','self employed','selfemployed','n a','na','none','null','freelance','freelancer',
           'stealth','stealth mode','stealth startup','unemployed','independent','independent consultant',
           'private','confidential','tbd','x','test','my own company','myself','home','retired'}
JUNK_NAME_TOKENS = {'seo','ai','uhc','nexta','tes','blk grl magic','inc','llc','agency','marketing','media','the'}

EMOJI_RE = re.compile('[\U0001F000-\U0001FAFF☀-➿⬀-⯿️←-⇿⌀-⏿]')
LATIN_OK = re.compile(r'^[A-Za-zÀ-ɏ][A-Za-zÀ-ɏ\'\-\.’ ]*$')

def clean_first_name(raw):
    """Return (cleaned, status, note). status in {ok, cleaned, unusable}."""
    s = collapse(raw)
    if not s:
        return '', 'unusable', 'empty'
    orig = s
    notes = []
    if EMOJI_RE.search(s):
        s = collapse(EMOJI_RE.sub(' ', s)); notes.append('stripped emoji')
    # A fully-quoted name is a preferred name -> unwrap it.
    # A quoted fragment inside a name is a nickname -> drop the fragment.
    m = re.fullmatch(r'[\u201c\u2018"\'`]\s*(.+?)\s*[\u201d\u2019"\'`]', s)
    if m:
        s = collapse(m.group(1)); notes.append('unwrapped quoted preferred name')
    else:
        s2 = re.sub(r'[\u201c\u2018"`]\s*[^\u201d\u2019"`]*[\u201d\u2019"`]', ' ', s)
        if collapse(s2) and s2 != s:
            s = collapse(s2); notes.append('dropped quoted nickname')
    # credentials after comma/pipe/dash:  "Jane, MBA" / "Jane | CPA"
    s2 = re.split(r'\s*[,|]\s*', s)[0]
    if s2 != s:
        s = collapse(s2); notes.append('dropped post-comma segment')
    if re.search(CRED, s, flags=re.I):
        s2 = collapse(re.sub(CRED, ' ', s, flags=re.I))
        if s2 and LATIN_OK.match(s2):
            s = s2; notes.append('stripped credentials')
    s = collapse(re.sub(r'[^\w\'\-\.À-ɏ ]', ' ', s))
    if not s:
        return '', 'unusable', 'nothing left after cleaning: ' + repr(orig)
    if not LATIN_OK.match(s):
        return orig, 'unusable', 'non-Latin script or not parseable as a personal name'
    if norm_text(s) in JUNK_NAME_TOKENS:
        return orig, 'unusable', 'looks like a brand/keyword, not a person'
    if len(s.replace('.','').replace(' ','')) <= 1:
        return orig, 'unusable', 'single character'
    # ALL CAPS -> Title Case, but keep short initialisms (TJ, DJ, AJ, RJ, T.J.)
    letters = re.sub(r'[^A-Za-z]', '', s)
    if s.isupper() and len(letters) >= 4:
        s = ' '.join(w.capitalize() for w in s.split()); notes.append('de-capsed')
    elif s.isupper():
        notes.append('kept short initialism')
    elif s.islower():
        s = ' '.join(w.capitalize() for w in s.split()); notes.append('title-cased')
    return s, ('cleaned' if (notes and s != orig) else 'ok'), '; '.join(notes)

cf = uni['First Name'].map(clean_first_name)
uni['cleaned_first_name'] = [x[0] for x in cf]
uni['first_name_status']  = [x[1] for x in cf]
uni['first_name_note']    = [x[2] for x in cf]

def hygiene(r):
    if not r['url_valid']:
        return 'bad_profile_url', f"normalized='{r['norm_profile_url']}'"
    if not collapse(r['First Name']):
        return 'missing_first_name', ''
    if r['first_name_status'] == 'unusable':
        return 'unusable_first_name', r['first_name_note']
    if not collapse(r['Company']):
        return 'missing_company', ''
    if norm_text(r['Company']) in JUNK_CO:
        return 'junk_company', repr(r['Company'])
    return '', ''

hy = uni.apply(hygiene, axis=1)
uni['hygiene_reason'] = [x[0] for x in hy]
uni['hygiene_detail'] = [x[1] for x in hy]

# ---------------------------------------------------------------- STEP 5B: TITLE
ACCEPTED = ['chief executive officer','group chief executive officer','deputy chief executive officer',
    'interim chief executive officer','advisor to chief executive officer','acting chief executive officer',
    'principal chief executive officer','founder','co founder','managing director','executive director',
    'director','owner','co owner','agency director','president','executive vice president','general manager']
ACCEPTED_SET = set(ACCEPTED)
TOPLEVEL_DIRECTOR = {'managing director','executive director','agency director','director'}

ABBREV = [(r'\bc\.?e\.?o\.?\b','chief executive officer'), (r'\bevp\b','executive vice president'),
          (r'\bsvp\b','senior vice president'), (r'\bvp\b','vice president'),
          (r'\bgm\b','general manager'), (r'\bpres\b','president'), (r'\bmng\b','managing'),
          (r'\bmd\b','managing director'), (r'\bcofounder\b','co founder'),
          (r'\bco-founder\b','co founder'), (r'\bco-owner\b','co owner')]

def norm_title_part(p):
    p = p.lower().replace('&',' and ')
    p = re.sub(r'[^a-z0-9\s\-\.]',' ', p)
    p = re.sub(r'\bco[\s\-]?founder\b','co founder', p)
    p = re.sub(r'\bco[\s\-]?owner\b','co owner', p)
    for pat, rep in ABBREV:
        p = re.sub(pat, rep, p)
    p = re.sub(r'[^a-z0-9\s]',' ', p)
    p = re.sub(r'\s+',' ', p).strip()
    p = re.sub(r'^(the|a)\s+','', p)
    return p

SPLIT_RE = re.compile(r'\s*(?:[&,|/\+()]|\band\b)\s*')
def title_status(raw):
    """-> (status, detail). status in {pass, review, fail}"""
    t = collapse(raw)
    if not t:
        return 'review', 'title missing - criterion B unverifiable'
    parts = [norm_title_part(p) for p in SPLIT_RE.split(t)]
    parts = [p for p in parts if p]
    if not parts:
        return 'review', 'title unparseable'
    review_hits = []
    for p in parts:
        if p in ACCEPTED_SET:
            if p == 'director':
                return 'pass', 'standalone director'
            return 'pass', f'matched "{p}"'
    for p in parts:
        if 'board' in p or 'trustee' in p:
            continue                       # board seats are not the CEO/Founder persona
        if 'director' in p and p not in TOPLEVEL_DIRECTOR:
            review_hits.append(f'director variant "{p}"')
        elif 'president' in p and p not in ('president','executive vice president'):
            review_hits.append(f'president variant "{p}"')
        elif any(k in p for k in ('owner','founder','founding','chief','partner','principal',
                                  'head of','chairman','chairwoman','chairperson','managing')):
            review_hits.append(f'senior-adjacent "{p}"')
    if review_hits:
        return 'review', '; '.join(sorted(set(review_hits)))
    return 'fail', 'no accepted title in: ' + ' | '.join(parts)

ts = uni['Job Title'].map(title_status)
uni['title_status'] = [x[0] for x in ts]
uni['title_detail'] = [x[1] for x in ts]

# ---------------------------------------------------------------- STEP 5C: GEOGRAPHY
ICP_STATES = {'maine','new hampshire','massachusetts','rhode island','connecticut','new york','new jersey',
 'pennsylvania','delaware','maryland','district of columbia','virginia','north carolina','south carolina',
 'georgia','florida','ohio','michigan','indiana','kentucky','tennessee','alabama','mississippi','wisconsin',
 'illinois','minnesota','missouri','arkansas','louisiana','iowa','west virginia'}
ALL_STATES = {**{s:s for s in ICP_STATES}, **{s:s for s in
 ['california','texas','washington','colorado','arizona','oregon','nevada','utah','new mexico','oklahoma',
  'kansas','nebraska','south dakota','north dakota','montana','wyoming','idaho','alaska','hawaii','vermont',
  'puerto rico']}}
ABBR = {'me':'maine','nh':'new hampshire','ma':'massachusetts','ri':'rhode island','ct':'connecticut',
 'ny':'new york','nj':'new jersey','pa':'pennsylvania','de':'delaware','md':'maryland','dc':'district of columbia',
 'va':'virginia','nc':'north carolina','sc':'south carolina','ga':'georgia','fl':'florida','oh':'ohio',
 'mi':'michigan','in':'indiana','ky':'kentucky','tn':'tennessee','al':'alabama','ms':'mississippi',
 'wi':'wisconsin','il':'illinois','mn':'minnesota','mo':'missouri','ar':'arkansas','la':'louisiana',
 'ia':'iowa','wv':'west virginia','ca':'california','tx':'texas','wa':'washington','co':'colorado',
 'az':'arizona','or':'oregon','nv':'nevada','ut':'utah','nm':'new mexico','ok':'oklahoma','ks':'kansas',
 'ne':'nebraska','sd':'south dakota','nd':'north dakota','mt':'montana','wy':'wyoming','id':'idaho',
 'ak':'alaska','hi':'hawaii','vt':'vermont'}

# Metro -> state. Only metros where the resolution is unambiguous, OR where every
# candidate state is inside the 31 (outcome identical either way).
METRO = {
 'new york city metropolitan area':'new york','greater boston':'massachusetts',
 'greater boston area':'massachusetts','greater philadelphia':'pennsylvania',
 'greater philadelphia area':'pennsylvania','washington dc baltimore area':'district of columbia',
 'atlanta metropolitan area':'georgia','miami fort lauderdale area':'florida',
 'greater chicago area':'illinois','greater minneapolis st paul area':'minnesota',
 'greater tampa bay area':'florida','detroit metropolitan area':'michigan',
 'raleigh durham chapel hill area':'north carolina','charlotte metro':'north carolina',
 'greater cleveland':'ohio','greater orlando':'florida','cincinnati metropolitan area':'ohio',
 'nashville metropolitan area':'tennessee','greater indianapolis':'indiana',
 'memphis metropolitan area':'tennessee','greater pittsburgh region':'pennsylvania',
 'greater hartford':'connecticut','greensboro winston salem high point area':'north carolina',
 'des moines metropolitan area':'iowa','greater milwaukee':'wisconsin','greater st louis':'missouri',
 'metro jacksonville':'florida','greater birmingham alabama area':'alabama',
 'greater richmond region':'virginia','greater new orleans region':'louisiana',
 'knoxville metropolitan area':'tennessee','little rock metropolitan area':'arkansas',
 'louisville metropolitan area':'kentucky','greater harrisburg area':'pennsylvania',
 'grand rapids metropolitan area':'michigan','greater madison area':'wisconsin',
 'greater bloomington illinois area':'illinois','greater duluth area':'minnesota',
 'johnson city kingsport bristol area':'tennessee','charleston huntington area':'west virginia',
 'buffalo niagara falls area':'new york','greater fort wayne':'indiana',
 'gainesville metropolitan area':'florida','north port sarasota area':'florida',
 'greater kalamazoo area':'michigan','la crosse onalaska area':'wisconsin',
 'greater myrtle beach area':'south carolina','greater savannah area':'georgia',
 'greater lansing':'michigan','mobile metropolitan area':'alabama',
 'appleton oshkosh neenah area':'wisconsin','greater florence muscle shoals alabama area':'alabama',
 'pensacola metropolitan area':'florida','cape coral metropolitan area':'florida',
 'erie meadville area':'pennsylvania','greater ocala area':'florida',
 'greater syracuse auburn area':'new york','greater scranton area':'pennsylvania',
 'peoria metropolitan area':'illinois','greater roanoke area':'virginia',
 'quad cities metropolitan area':'iowa','greater wilmington area':'delaware',
 'greater augusta area':'georgia',
 # non-ICP metros, resolved so they get a clean geo_out_of_icp
 'san francisco bay area':'california','dallas fort worth metroplex':'texas',
 'greater phoenix area':'arizona','greater seattle area':'washington',
 'los angeles metropolitan area':'california','greater denver area':'colorado',
 'greater sacramento':'california','greater houston':'texas','austin texas metropolitan area':'texas',
 'greater salt lake city area':'utah','portland oregon metropolitan area':'oregon',
 'las vegas metropolitan area':'nevada','san diego metropolitan area':'california',
 'oklahoma city metropolitan area':'oklahoma','wichita ks metropolitan area':'kansas',
 'omaha metropolitan area':'nebraska','greater boise area':'idaho',
}
AMBIGUOUS = {'kansas city metropolitan area':'Kansas City straddles MO/KS',
 'greater columbus area':'Columbus exists in OH, GA, IN, MS',
 'lancaster metropolitan area':'Lancaster exists in PA, OH and CA',
 'united states':'country-level only, no state',
 'greater springfield area':'Springfield exists in IL, MO, MA, OH',
 'portland maine metropolitan area':'ok', 'washington':'could be WA state or Washington DC'}

NON_US_HINT = re.compile(r'(canada|united kingdom|england|india|australia|germany|france|spain|italy|brazil|mexico|'
 r'netherlands|ireland|poland|portugal|sweden|norway|denmark|switzerland|belgium|austria|greece|turkey|'
 r'israel|uae|emirates|saudi|qatar|egypt|nigeria|kenya|south africa|singapore|philippines|indonesia|'
 r'malaysia|thailand|vietnam|japan|china|korea|hong kong|taiwan|pakistan|bangladesh|sri lanka|nepal|'
 r'argentina|chile|colombia|peru|venezuela|ecuador|guatemala|costa rica|panama|dominican|puerto rico|'
 r'new zealand|romania|ukraine|russia|czech|hungary|bulgaria|croatia|serbia|lithuania|latvia|estonia|'
 r'finland|iceland|luxembourg|slovakia|slovenia|morocco|tunisia|ghana|uganda|tanzania|zimbabwe|armenia|'
 r'georgia, georgia|albania|cyprus|malta|jordan|lebanon|kuwait|bahrain|oman|yemen|iraq|iran|afghanistan)',
 re.I)

def _verdict(st, how):
    return ('pass' if st in ICP_STATES else 'fail'), st, f'{how} -> "{st}"'

# Longest first so "west virginia" wins over "virginia", "new york" over "york".
_STATE_PHRASES = sorted(ALL_STATES, key=len, reverse=True)

def geo_status(raw):
    """-> (status, state_or_blank, detail). status in {pass, review, fail}

    LinkedIn writes "City, State, Country", so comma segments are scanned
    RIGHT-TO-LEFT: "California, Maryland, United States" is a town in Maryland,
    not the state of California.
    """
    loc = collapse(raw)
    if not loc:
        return 'review', '', 'location missing - criterion C unverifiable'
    n = norm_text(loc)

    # DC before anything else: "Washington, District of Columbia" and
    # "Washington DC-Baltimore Area" must not be read as Washington State.
    if 'district of columbia' in n or re.search(r'\bwashington d ?c\b', n):
        return 'pass', 'district of columbia', 'DC'

    # explicit state name / abbreviation in a comma segment, rightmost wins
    for seg in reversed([norm_text(x) for x in loc.split(',')]):
        if seg in ALL_STATES:
            if seg == 'washington' and n == 'washington':
                return 'review', '', f'"Washington" ambiguous (state vs DC) :: "{loc}"'
            return _verdict(ALL_STATES[seg], 'state')
        if seg in ABBR:
            return _verdict(ABBR[seg], 'state abbr')

    if n in METRO:
        return _verdict(METRO[n], 'metro')
    if n in AMBIGUOUS:
        return 'review', '', AMBIGUOUS[n] + f' :: "{loc}"'

    # state named inside a metro string: "Columbus, Ohio Metropolitan Area",
    # "Greenville-Spartanburg-Anderson, South Carolina Area". Rightmost match wins.
    # "washington" excluded - too ambiguous to resolve this way.
    best = (-1, None)
    for ph in _STATE_PHRASES:
        if ph == 'washington':
            continue
        m = None
        for m in re.finditer(r'(?<![a-z])' + re.escape(ph) + r'(?![a-z])', n):
            pass
        if m and m.start() > best[0]:
            best = (m.start(), ph)
    if best[1]:
        return _verdict(ALL_STATES[best[1]], 'state named in metro string')

    if NON_US_HINT.search(loc):
        return 'fail', '', f'outside US :: "{loc}"'
    return 'review', '', f'location not resolvable to a state :: "{loc}"'

gs = uni['Location'].map(geo_status)
uni['geo_status'] = [x[0] for x in gs]
uni['geo_state']  = [x[1] for x in gs]
uni['geo_detail'] = [x[2] for x in gs]

# criterion A: no headcount column exists anywhere in the source
uni['headcount_verified'] = 'no_data_in_export'

# ---------------------------------------------------------------- ROUTE
def route(r):
    if r['hygiene_reason']:
        return 'removed', r['hygiene_reason'], r['hygiene_detail']
    if r['geo_status'] == 'fail':
        return 'removed', 'geo_out_of_icp', r['geo_detail']
    if r['title_status'] == 'fail':
        return 'removed', 'title_out_of_icp', r['title_detail']
    notes = []
    if r['geo_status'] == 'review':
        notes.append('GEO(C): ' + r['geo_detail'])
    if r['title_status'] == 'review':
        notes.append('TITLE(B): ' + r['title_detail'])
    if notes:
        return 'needs_review', 'icp_unverifiable', ' || '.join(notes)
    return 'master', '', ''

rt = uni.apply(route, axis=1)
uni['bucket']         = [x[0] for x in rt]
uni['removal_reason'] = [x[1] for x in rt]
uni['removal_detail'] = [x[2] for x in rt]
print('[route]', uni['bucket'].value_counts().to_dict())

uni.to_pickle(os.path.join(OUT, '_uni.pkl'))
dups.to_pickle(os.path.join(OUT, '_dups.pkl'))
with open(os.path.join(OUT, '_meta.json'), 'w') as f:
    json.dump({'file_rows': file_rows, 'total_in': TOTAL_IN, 'within': within, 'cross': cross,
               'dup_pairs': [list(p) for p in dup_pairs], 'orig_cols': ORIG_COLS,
               'near': near}, f)
print('[stage1 done]')
