import sys; sys.path.insert(0,'scripts')
import importlib.metadata as md, swisseph as swe
from part1 import A,B,natal_md
mdA=natal_md(A); mdB=natal_md(B)
import part2, part3, part4

sanity=[]
sanity.append("## SANITY CHECK\n")
sanity.append(f"- pyswisseph version: **{md.version('pyswisseph')}**")
sanity.append(f"- swe.version: **{swe.version}**")
sanity.append(f"- Ephemeris: Swiss Ephemeris files (seas_18.se1, sepl_18.se1, semo_18.se1)\n")
sanity.append("| Item | Computed UTC offset (zoneinfo Europe/Skopje) | UT | JD (UT) |")
sanity.append("|---|---|---|---|")
sanity.append(f"| A birth moment | `{A['_off']}` | {A['_utc']} | {A['_jd']:.6f} |")
sanity.append(f"| B birth moment | `{B['_off']}` | {B['_utc']} | {B['_jd']:.6f} |")
sanity.append(f"| Reference 30 Aug 2026 12:00 | `{part4.NOW_OFF}` | {part4.NOW_UTC} | {part4.NOW_JD:.6f} |")
sanity.append("")
from astro_lib import fmt, signof
checks=[("A Ascendant","Scorpio ~6°",A['ASC']['lon'],signof(A['ASC']['lon'])=="Scorpio" and 5<=A['ASC']['lon']%30<7),
        ("A Sun","Cancer ~13°",A['Sun']['lon'],signof(A['Sun']['lon'])=="Cancer" and 12<=A['Sun']['lon']%30<14),
        ("B Sun","Aquarius",B['Sun']['lon'],signof(B['Sun']['lon'])=="Aquarius"),
        ("B Mercury","Aquarius",B['Mercury']['lon'],signof(B['Mercury']['lon'])=="Aquarius"),
        ("B Ascendant","Aquarius",B['ASC']['lon'],signof(B['ASC']['lon'])=="Aquarius"),
        ("B Mars","Leo, retrograde",B['Mars']['lon'],signof(B['Mars']['lon'])=="Leo" and B['Mars']['speed']<0)]
sanity.append("| Check | Expected | Computed | Match |")
sanity.append("|---|---|---|---|")
for n,e,v,ok in checks:
    extra=f", speed {B['Mars']['speed']:+.4f} (retrograde)" if n=="B Mars" else ""
    sanity.append(f"| {n} | {e} | {fmt(v)} ({v:.4f}){extra} | {'MATCH' if ok else 'MISMATCH'} |")
allok=all(c[3] for c in checks)
sanity.append(f"\n**All sanity checks: {'PASS' if allok else 'FAIL'}**\n")
SAN="\n".join(sanity)
if not allok:
    print(SAN); sys.exit("SANITY MISMATCH — stopping")

doc=["# Astrological data computation — Subjects A and B",
"",
"All positions computed with Swiss Ephemeris via pyswisseph. Tropical zodiac, geocentric, apparent positions. "
"No value in this document is recalled or estimated; every figure is a direct Swiss Ephemeris computation. "
"UTC offsets resolved with `zoneinfo.ZoneInfo(\"Europe/Skopje\")`.",
"",
"**Subjects**",
"",
"| | Name | Date | Local time | Place | Latitude | Longitude |",
"|---|---|---|---|---|---|---|",
"| A | Sara | 5 July 1994 | 14:45 | Bitola, North Macedonia | 41.0297 N | 21.3347 E |",
"| B | Trajche | 27 January 1995 | 07:15 | Stip, North Macedonia | 41.7364 N | 22.1917 E |",
"",
"Reference location (composite angles, transits): Skopje, 41.9973 N, 21.4280 E. "
"Reference moment for anything current: 30 August 2026, 12:00 Europe/Skopje.",
"",
"Position format: `Sign DD MM SS | absolute ecliptic longitude (decimal, 4 dp) | daily speed | D/R | declination`.",
"",
SAN,
"---","",
"## PART 1: THE TWO NATAL CHARTS","",
mdA, mdB,
"---","",
part2.md(),
"---","",
part3.md(),
"---","",
part4.md()]
out="\n".join(doc)
open('outputs/astro-data-A-B.md','w').write(out)
open('/tmp/sanity_block.md','w').write(SAN)
open('/tmp/part2_block.md','w').write(part2.md())
print("written", len(out), "chars")
