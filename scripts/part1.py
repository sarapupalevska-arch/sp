import sys; sys.path.insert(0,'scripts')
from astro_lib import *

LOC = dict(A=(41.0297,21.3347,"Bitola"), B=(41.7364,22.1917,"Stip"), REF=(41.9973,21.4280,"Skopje"))

def build(name,y,m,d,hh,mi,lat,lon):
    jd,off,u = local_to_jd(y,m,d,hh,mi)
    c = chart(jd,lat,lon)
    c['_name']=name; c['_off']=off; c['_utc']=u
    return c

A = build("A (Sara)",1994,7,5,14,45,*LOC['A'][:2])
B = build("B (Trajche)",1995,1,27,7,15,*LOC['B'][:2])

def row(nm,p):
    rx = "R" if p['speed']<0 else "D"
    return f"| {nm} | {fmt(p['lon'])} | {p['lon']:.4f} | {p['speed']:+.4f} | {rx} | {p['decl']:+.2f} |"

def hnums(c,l):
    return house_of(l,c['_cusps_P']), house_of(l,c['_ws'])

def natal_md(c):
    o=[]
    o.append(f"### Chart {c['_name']}")
    o.append(f"UTC offset: `{c['_off']}` | UT: `{c['_utc']}` | JD(UT): `{c['_jd']:.6f}`")
    o.append("")
    o.append("#### 1.1 / 1.2 Positions with houses")
    o.append("| Body | Sign D M S | Longitude | Speed/day | Rx | Decl | House (Placidus) | House (Whole Sign) |")
    o.append("|---|---|---|---|---|---|---|---|")
    for nm,_ in BODIES:
        p=c[nm]; hp,hw = hnums(c,p['lon'])
        o.append(row(nm,p)+f" {hp} | {hw} |")
    o.append("")
    o.append("**Angles**")
    o.append("| Point | Sign D M S | Longitude | Decl |")
    o.append("|---|---|---|---|")
    for nm in ("ASC","MC","DSC","IC"):
        p=c[nm]; o.append(f"| {nm} | {fmt(p['lon'])} | {p['lon']:.4f} | {p['decl']:+.2f} |")
    o.append("")
    o.append("**House cusps**")
    o.append("| House | Placidus cusp | Placidus long. | Whole-sign cusp | WS long. |")
    o.append("|---|---|---|---|---|")
    for i in range(12):
        pc=c['_cusps_P'][i]
        wc=c['_ws'][i]
        o.append(f"| {i+1} | {fmt(pc)} | {pc:.4f} | {fmt(wc)} | {wc:.4f} |")
    o.append("")
    # sect
    L,day = lots(c)
    o.append("#### 1.3 Sect and Ascendant ruler")
    o.append(f"- Chart: **{'DAY' if day else 'NIGHT'}**")
    o.append(f"- Sect light: **{'Sun' if day else 'Moon'}** ({fmt(c['Sun' if day else 'Moon']['lon'])})")
    ascsign = signof(c['ASC']['lon']); rl = RULER[ascsign]
    rp = c[rl]; rs = signof(rp['lon']); hp,hw = hnums(c,rp['lon'])
    o.append(f"- Ascendant sign: **{ascsign}**; ruler: **{rl}**")
    o.append(f"- {rl}: {fmt(rp['lon'])} ({rp['lon']:.4f}), Placidus house {hp}, whole-sign house {hw}, condition: **{condition(rl,rs)}**")
    o.append("")
    o.append("#### 1.4 Lots")
    o.append("| Lot | Formula used | Sign D M S | Longitude | House (P) | House (WS) |")
    o.append("|---|---|---|---|---|---|")
    F = {
      'Fortune': "ASC + Moon − Sun" if day else "ASC + Sun − Moon",
      'Spirit': "ASC + Sun − Moon" if day else "ASC + Moon − Sun",
      'Eros': "ASC + Venus − Spirit" if day else "ASC + Spirit − Venus",
      'Necessity': "ASC + Fortune − Mercury" if day else "ASC + Mercury − Fortune",
      'Marriage (Venus-based, Hellenistic)': "ASC + Venus − Saturn",
      'Marriage (Saturn-based)': "ASC + Saturn − Venus"}
    for k,v in L.items():
        hp,hw=hnums(c,v)
        o.append(f"| {k} | {F[k]} | {fmt(v)} | {v:.4f} | {hp} | {hw} |")
    c['_lots']=L; c['_day']=day
    o.append("")
    o.append("#### 1.5 Internal natal aspects")
    o.append("| Body 1 | Aspect | Body 2 | Orb | Applying/Separating |")
    o.append("|---|---|---|---|---|")
    names=[n for n,_ in BODIES]+["ASC","MC"]
    res=[]
    for i in range(len(names)):
        for j in range(i+1,len(names)):
            n1,n2=names[i],names[j]
            if {n1,n2}=={"True Node","Mean Node"}: continue
            res += find_aspects(c[n1]['lon'],c[n1]['speed'],n1,c[n2]['lon'],c[n2]['speed'],n2,
                                MAJOR+MINOR, orb_limit_syn)
    for r in sorted(res,key=lambda x:x['orb']):
        o.append(f"| {r['a']} | {r['asp']} | {r['b']} | {orbfmt(r['orb'])} | {r['app']} |")
    o.append("")
    o.append("#### 1.6 Seventh house")
    p7 = c['_cusps_P'][6]; w7 = c['_ws'][6]
    o.append(f"- 7th cusp (Placidus): {fmt(p7)} — sign **{signof(p7)}**")
    o.append(f"- 7th cusp (whole sign): {fmt(w7)} — sign **{signof(w7)}**")
    for label,sgn in (("Placidus",signof(p7)),("Whole sign",signof(w7))):
        r=RULER[sgn]; rp=c[r]; hp,hw=hnums(c,rp['lon'])
        o.append(f"- {label} 7th ruler: **{r}** — {fmt(rp['lon'])}, Placidus house {hp}, WS house {hw}, dignity: {condition(r,signof(rp['lon']))}")
        asps=[]
        for n,_ in BODIES:
            if n==r: continue
            asps+=find_aspects(rp['lon'],rp['speed'],r,c[n]['lon'],c[n]['speed'],n,MAJOR+MINOR,orb_limit_syn)
        for n in ("ASC","MC"):
            asps+=find_aspects(rp['lon'],rp['speed'],r,c[n]['lon'],0,n,MAJOR+MINOR,orb_limit_syn)
        if asps:
            o.append(f"  - Aspects to {r}: " + "; ".join(f"{x['asp']} {x['b']} ({orbfmt(x['orb'])}, {x['app']})" for x in sorted(asps,key=lambda z:z['orb'])))
        else: o.append(f"  - Aspects to {r}: none within orb")
    for label,test in (("Placidus", lambda l: house_of(l,c['_cusps_P'])==7),("Whole sign", lambda l: house_of(l,c['_ws'])==7)):
        inh=[n for n,_ in BODIES if test(c[n]['lon'])]
        o.append(f"- Planets in 7th ({label}): {', '.join(inh) if inh else 'none'}")
    o.append("")
    return "\n".join(o)

if __name__=="__main__":
    print(natal_md(A)); print(natal_md(B))
