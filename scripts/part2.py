import sys; sys.path.insert(0,'scripts')
from part1 import A,B,natal_md,hnums
from astro_lib import *

BODY_NAMES=[n for n,_ in BODIES]
def points(c, include_lots=True):
    pts={}
    for n in BODY_NAMES: pts[n]=c[n]
    for n in ("ASC","MC","DSC","IC"): pts[n]=c[n]
    if include_lots:
        for k,v in c['_lots'].items():
            pts["Lot "+k]=dict(lon=v,speed=0.0,decl=decl_of(v),lat=0.0)
    return pts

# ensure lots computed
natal_md(A); natal_md(B)
PA=points(A); PB=points(B)

def syn_grid():
    res=[]
    for na,pa in PA.items():
        for nb,pb in PB.items():
            base_a = na.replace("Lot ","") if na.startswith("Lot") else na
            base_b = nb.replace("Lot ","") if nb.startswith("Lot") else nb
            def lim(x,y,asp,na=na,nb=nb):
                return orb_limit_syn(na if not na.startswith("Lot") else "Lot",
                                     nb if not nb.startswith("Lot") else "Lot", asp)
            res+=find_aspects(pa['lon'],pa['speed'],na,pb['lon'],pb['speed'],nb,MAJOR+MINOR,lim)
    return res

R = syn_grid()

def md():
    o=[]
    o.append("## PART 2: SYNASTRY\n")
    o.append("### 2.1 Cross-aspect grid — sorted by orb (tightest first)\n")
    o.append("| A body | Aspect | B body | Orb | App/Sep | TIGHT |")
    o.append("|---|---|---|---|---|---|")
    for r in sorted(R,key=lambda x:x['orb']):
        o.append(f"| {r['a']} | {r['asp']} | {r['b']} | {orbfmt(r['orb'])} | {r['app']} | {'TIGHT' if r['tight'] else ''} |")
    o.append("")
    o.append("### 2.1b Same grid grouped by A body\n")
    for na in PA.keys():
        sub=[r for r in R if r['a']==na]
        if not sub: continue
        o.append(f"**A {na}**\n")
        o.append("| Aspect | B body | Orb | App/Sep | TIGHT |")
        o.append("|---|---|---|---|---|")
        for r in sorted(sub,key=lambda x:x['orb']):
            o.append(f"| {r['asp']} | {r['b']} | {orbfmt(r['orb'])} | {r['app']} | {'TIGHT' if r['tight'] else ''} |")
        o.append("")
    # 2.2 overlays
    o.append("### 2.2 House overlays\n")
    FLAGH={1,5,7,8,10,12}
    for src,dst,lab in ((A,B,"A's bodies in B's houses"),(B,A,"B's bodies in A's houses")):
        o.append(f"**{lab}**\n")
        o.append("| Body | Longitude | Placidus house | WS house | Flag |")
        o.append("|---|---|---|---|---|")
        for n in BODY_NAMES+["ASC","MC","DSC","IC"]:
            l=src[n]['lon']; hp=house_of(l,dst['_cusps_P']); hw=house_of(l,dst['_ws'])
            fl="FLAG" if (hp in FLAGH or hw in FLAGH) else ""
            o.append(f"| {n} | {fmt(l)} | {hp} | {hw} | {fl} |")
        o.append("")
    # 2.3 declinations
    o.append("### 2.3 Declination cross-aspects (orb 1°)\n")
    o.append("| A body | Type | B body | A decl | B decl | Orb (arcmin) |")
    o.append("|---|---|---|---|---|---|")
    dl=[]
    for na in BODY_NAMES+["ASC","MC"]:
        for nb in BODY_NAMES+["ASC","MC"]:
            d1=A[na]['decl']; d2=B[nb]['decl']
            if abs(d1-d2)<=1.0: dl.append((na,"parallel",nb,d1,d2,abs(d1-d2)*60))
            if abs(d1+d2)<=1.0: dl.append((na,"contraparallel",nb,d1,d2,abs(d1+d2)*60))
    for x in sorted(dl,key=lambda z:z[5]):
        o.append(f"| {x[0]} | {x[1]} | {x[2]} | {x[3]:+.2f} | {x[4]:+.2f} | {x[5]:.1f}' |")
    o.append("")
    # 2.4 antiscia
    o.append("### 2.4 Antiscia / contra-antiscia contacts (orb 1°)\n")
    o.append("| A body | Type | B body | A point | B longitude | Orb |")
    o.append("|---|---|---|---|---|---|")
    an=[]
    for na in BODY_NAMES+["ASC","MC"]:
        for nb in BODY_NAMES+["ASC","MC"]:
            a1=antiscion(A[na]['lon']); c1=cantiscion(A[na]['lon'])
            for typ,pt in (("antiscion",a1),("contra-antiscion",c1)):
                d=sep(pt,B[nb]['lon'])
                if d<=1.0: an.append((na,typ,nb,pt,B[nb]['lon'],d))
    for x in sorted(an,key=lambda z:z[5]):
        o.append(f"| {x[0]} | {x[1]} | {x[2]} | {fmt(x[3])} | {fmt(x[4])} | {orbfmt(x[5])} |")
    if not an: o.append("| — | — | — | — | — | none within 1° |")
    o.append("")
    # 2.5 node contacts
    o.append("### 2.5 Cross-chart nodal-axis contacts (orb 5°)\n")
    o.append("| Body | Direction | Node point | Aspect | Orb |")
    o.append("|---|---|---|---|---|")
    nc=[]
    for src,dst,lab in ((A,B,"A body → B nodal axis"),(B,A,"B body → A nodal axis")):
        for nn in ("True Node","Mean Node"):
            nl=dst[nn]['lon']
            for n in BODY_NAMES+["ASC","MC"]:
                if n in ("True Node","Mean Node"): continue
                for asp,ang in (("conjunction",0),("opposition",180)):
                    d=abs(sep(src[n]['lon'],nl)-ang)
                    if d<=5.0: nc.append((n,lab,f"{nn} ({fmt(nl)})",asp,d))
    for x in sorted(nc,key=lambda z:z[4]):
        o.append(f"| {x[0]} | {x[1]} | {x[2]} | {x[3]} | {orbfmt(x[4])} |")
    o.append("")
    # 2.6 draconic
    o.append("### 2.6 Draconic synastry (orb 2°, major aspects)\n")
    def drac(c):
        off=c['True Node']['lon']
        d={}
        for n in BODY_NAMES+["ASC","MC","DSC","IC"]:
            d[n]=dict(lon=(c[n]['lon']-off)%360, speed=c[n]['speed'], decl=0.0)
        return d
    DA=drac(A); DB=drac(B)
    def lim2(x,y,asp): return 2.0
    for lab,X,Y in (("Draconic A → Natal B",DA,{n:B[n] for n in BODY_NAMES+['ASC','MC','DSC','IC']}),
                    ("Draconic A → Draconic B",DA,DB)):
        o.append(f"**{lab}**\n")
        o.append("| A point | Aspect | B point | Orb | App/Sep |")
        o.append("|---|---|---|---|---|")
        rr=[]
        for na,pa in X.items():
            for nb,pb in Y.items():
                rr+=find_aspects(pa['lon'],pa['speed'],na,pb['lon'],pb['speed'],nb,MAJOR,lim2)
        for r in sorted(rr,key=lambda z:z['orb']):
            o.append(f"| {r['a']} | {r['asp']} | {r['b']} | {orbfmt(r['orb'])} | {r['app']} |")
        o.append("")
    # 2.7 checklist
    o.append("### 2.7 Classical indicator checklist\n")
    o.append("| Indicator | Status | Detail |")
    o.append("|---|---|---|")
    def hits(s1, s2):
        out=set()
        for r in R:
            if (r['a'] in s1 and r['b'] in s2) or (r['a'] in s2 and r['b'] in s1):
                out.add(f"A {r['a']} {r['asp']} B {r['b']} {orbfmt(r['orb'])}")
        return sorted(out)
    def line(label, res):
        o.append(f"| {label} | {'PRESENT' if res else 'ABSENT'} | {'; '.join(res) if res else '—'} |")
    line("Sun–Moon (either direction)", hits(["Sun"],["Moon"]))
    line("Venus–Mars (either direction)", hits(["Venus"],["Mars"]))
    line("Moon–Moon", hits(["Moon"],["Moon"]))
    line("Venus–Saturn", hits(["Venus"],["Saturn"]))
    line("Moon–Saturn", hits(["Moon"],["Saturn"]))
    line("Sun–Saturn", hits(["Sun"],["Saturn"]))
    r7a = RULER[signof(A['_ws'][6])]; r7ap = RULER[signof(A['_cusps_P'][6])]
    r7b = RULER[signof(B['_ws'][6])]; r7bp = RULER[signof(B['_cusps_P'][6])]
    ra=sorted({r7a,r7ap}); rb=sorted({r7b,r7bp})
    line(f"Ruler of A's 7th ({'/'.join(ra)}) touching any B body",
         [f"A {r['a']} {r['asp']} B {r['b']} {orbfmt(r['orb'])}" for r in R if r['a'] in ra])
    line(f"Ruler of B's 7th ({'/'.join(rb)}) touching any A body",
         [f"A {r['a']} {r['asp']} B {r['b']} {orbfmt(r['orb'])}" for r in R if r['b'] in rb])
    lum=["Sun","Moon","Venus"]
    asc_hits=[f"A {r['a']} {r['asp']} B {r['b']} {orbfmt(r['orb'])}" for r in R
              if r['asp'] in ("conjunction","opposition") and
              ((r['a']=="ASC" and r['b'] in lum) or (r['b']=="ASC" and r['a'] in lum))]
    line("Either ASC conjunct/opposite the other's luminaries or Venus", asc_hits)
    mh=[]
    if house_of(A['Moon']['lon'],B['_cusps_P'])==7 or house_of(A['Moon']['lon'],B['_ws'])==7:
        mh.append(f"A Moon in B's 7th (P:{house_of(A['Moon']['lon'],B['_cusps_P'])}, WS:{house_of(A['Moon']['lon'],B['_ws'])})")
    if house_of(B['Moon']['lon'],A['_cusps_P'])==7 or house_of(B['Moon']['lon'],A['_ws'])==7:
        mh.append(f"B Moon in A's 7th (P:{house_of(B['Moon']['lon'],A['_cusps_P'])}, WS:{house_of(B['Moon']['lon'],A['_ws'])})")
    line("Either Moon in the other's 7th house", mh)
    line("Mars–Saturn", hits(["Mars"],["Saturn"]))
    line("Venus–Uranus", hits(["Venus"],["Uranus"]))
    line("Moon–Neptune", hits(["Moon"],["Neptune"]))
    outers=["Jupiter","Saturn","Uranus","Neptune","Pluto"]
    oa=[f"A {r['a']} conjunction B {r['b']} {orbfmt(r['orb'])}" for r in R
        if r['asp']=="conjunction" and ((r['a'] in outers and r['b'] in ANGLES) or (r['b'] in outers and r['a'] in ANGLES))]
    line("Any outer planet conjunct the other's angles", oa)
    o.append("")
    return "\n".join(o)

if __name__=="__main__":
    print(md())
