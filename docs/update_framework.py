#!/usr/bin/env python3
"""Put approved commercial headlines into the Key statements table of messaging-framework.html.

Reads approved-headlines.json (keys: "main", "1".."9" for pillars, "1.1".."9.6" for points;
value = approved headline text, or null/"" for not yet approved) and writes each into
  1) the table cell <td class="h"> for that row, and
  2) the Board view's data object (D), so both views stay in sync.
Idempotent: run it again after every approval. Only rows with a non-empty value are touched;
rows set to null keep whatever the file already has (empty = shows the "To write" placeholder).

Usage: python3 update_framework.py [--file messaging-framework.html] [--json approved-headlines.json] [--check]
"""
import argparse, html, json, re, sys

ap = argparse.ArgumentParser()
ap.add_argument('--file', default='messaging-framework.html')
ap.add_argument('--json', default='approved-headlines.json')
ap.add_argument('--check', action='store_true', help='report only, do not write')
a = ap.parse_args()

src = open(a.file, encoding='utf-8').read()
approved = {k: v for k, v in json.load(open(a.json, encoding='utf-8')).items() if not k.startswith('_')}

# --- Board data object D (JS) ---
m = re.search(r'const D=(\{.*?\});\n', src, flags=re.S)
if not m:
    sys.exit('Could not find the Board data object (const D=...).')
D = json.loads(m.group(1))

# document order of the 44 table cells: main, pillars 1-9, then points 1.1 ... 9.6
order = ['main'] + [p['n'] for p in D['pillars']]
for p in D['pillars']:
    order += [f"{p['n']}.{i+1}" for i in range(len(p['pts']))]

unknown = [k for k in approved if k not in order]
if unknown:
    sys.exit(f'Unknown keys in {a.json}: {unknown}')

cells = list(re.finditer(r'<td class="h"[^>]*>(.*?)</td>', src, flags=re.S))
if len(cells) != len(order):
    sys.exit(f'Expected {len(order)} headline cells, found {len(cells)}. File structure changed; not writing.')

# update D
for k, v in approved.items():
    if not v:
        continue
    if k == 'main':
        D['root']['h'] = v
    elif '.' in k:
        n, i = k.split('.')
        [p for p in D['pillars'] if p['n'] == n][0]['pts'][int(i) - 1]['h'] = v
    else:
        [p for p in D['pillars'] if p['n'] == k][0]['h'] = v

# rebuild table cells (from the end so offsets stay valid)
out = src
for key, cm in reversed(list(zip(order, cells))):
    v = approved.get(key)
    if not v:
        continue
    new = '<td class="h">' + html.escape(v, quote=False) + '</td>'
    out = out[:cm.start()] + new + out[cm.end():]

m2 = re.search(r'const D=(\{.*?\});\n', out, flags=re.S)
out = out[:m2.start(1)] + json.dumps(D, ensure_ascii=True) + out[m2.end(1):]

filled = sum(1 for k in order if approved.get(k))
print(f'{filled} of {len(order)} headlines set.')
if a.check:
    sys.exit(0)
open(a.file, 'w', encoding='utf-8').write(out)
print(f'Wrote {a.file}')
