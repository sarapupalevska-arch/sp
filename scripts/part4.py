import sys; sys.path.insert(0,'scripts')
from part1 import A,B,natal_md
from part3 import COMP,DAV,dlat,dlon
from astro_lib import *
import swisseph as swe, math, datetime as dt

YR=365.2422
SKO_LAT,SKO_LON=41.9973,21.4280
NOW_JD,NOW_OFF,NOW_UTC = local_to_jd(2026,8,30,12,0)
BODY_NAMES=[n for n,_ in BODIES]

# ---------- 4.1 profections ----------
def profection(c,byear,bmon,bday):
    ref=dt.date(2026,8,30); b=dt.date(byear,bmon,bday)
    age=ref.year-b.year-((ref.month,ref.day)<(b.month,b.day))
    h=(age%12)+1
    sign=signof(c['_ws'][h-1]); lord=RULER[sign]
    last=dt.date(ref.year if (b.month,b.day)<=(ref.month,ref.day) else ref.year-1, b.month, b.day)
    nxt=dt.date(last.year+1,b.month,b.day)
    return age,h,sign,lord,last,nxt

# ---------- 4.2 firdaria ----------
DAYSEQ=["Sun","Venus","Mercury","Moon","Saturn","Jupiter","Mars","North Node","South Node"]
NIGHTSEQ=["Moon","Saturn","Jupiter","Mars","Sun","Venus","Mercury","North Node","South Node"]
FYRS={"Sun":10,"Venus":8,"Mercury":13,"Moon":9,"Saturn":11,"Jupiter":12,"Mars":7,
      "North Node":3,"South Node":2}
def firdaria(jd_birth, day):
    seq = DAYSEQ if day else NIGHTSEQ
    planets=[p for p in seq if "Node" not in p]
    out=[]; t=jd_birth
    for major in seq:
        span=FYRS[major]*YR
        if "Node" in major:
            out.append((major,None,t,t+span)); t+=span; continue
        sub=span/7.0
        i=planets.index(major); st=t
        for k in range(7):
            minor=planets[(i+k)%7]
            out.append((major,minor,st,st+sub)); st+=sub
        t+=span
    return out
def jd2d(j):
    y,m,d,h=swe.revjul(j,swe.GREG_CAL)
    return (dt.datetime(y,m,d,tzinfo=dt.timezone.utc)+dt.timedelta(hours=h)).strftime("%Y-%m-%d")

# ---------- 4.3 progressions ----------
def progressed(c, blat, blon):
    el=(NOW_JD-c['_jd'])/YR
    pjd=c['_jd']+el
    pc=chart(pjd, blat, blon)
    pc['_pjd']=pjd; pc['_years']=el; pc['_natal_jd']=c['_jd']
    return pc

# ---------- transit search ----------
TR=[("Jupiter",swe.JUPITER),("Saturn",swe.SATURN),("Uranus",swe.URANUS),
    ("Neptune",swe.NEPTUNE),("Pluto",swe.PLUTO)]
def tlon(code,jd): return swe.calc_ut(jd,code,FLG)[0][0]
def tspd(code,jd): return swe.calc_ut(jd,code,FLG)[0][3]

def find_perfections(code,target,ang,j0,j1,step=1.0):
    hits=[]
    def f(j):
        d=(tlon(code,j)-target-ang)%360
        return d-360 if d>180 else d
    j=j0; prev=f(j)
    while j<j1:
        jn=min(j+step,j1); cur=f(jn)
        if (prev<0)!=(cur<0) and abs(cur-prev)<180:
            lo,hi=j,jn
            for _ in range(60):
                mid=(lo+hi)/2
                if (f(lo)<0)==(f(mid)<0): lo=mid
                else: hi=mid
            hits.append((lo+hi)/2)
        prev=cur; j=jn
    return hits

def station_in_orb(code,jd_perf,target,ang,orb=1.0):
    """True if the planet stations while within `orb` of the exact aspect point."""
    for k in range(-250,251):
        j=jd_perf+k
        s1=tspd(code,j); s2=tspd(code,j+1)
        if s1*s2<0:
            lo,hi=j,j+1
            for _ in range(40):
                mid=(lo+hi)/2
                if tspd(code,lo)*tspd(code,mid)<0: hi=mid
                else: lo=mid
            js=(lo+hi)/2
            d=sep(tlon(code,js),(target+ang)%360)
            if d<=orb:
                return True, f"{jd2d(js)} at {fmt(tlon(code,js))} ({d:.2f}° from exact)"
    return False, None

# ---------- 4.5 lunations ----------
def lunations(j0,j1):
    out=[]
    def elong(j):
        d=(swe.calc_ut(j,swe.MOON,FLG)[0][0]-swe.calc_ut(j,swe.SUN,FLG)[0][0])%360
        return d
    for phase,ang in (("New Moon",0),("Full Moon",180)):
        def f(j):
            d=(elong(j)-ang)%360
            return d-360 if d>180 else d
        j=j0; prev=f(j)
        while j<j1:
            jn=min(j+1.0,j1); cur=f(jn)
            if (prev<0)!=(cur<0) and abs(cur-prev)<180:
                lo,hi=j,jn
                for _ in range(60):
                    mid=(lo+hi)/2
                    if (f(lo)<0)==(f(mid)<0): lo=mid
                    else: hi=mid
                jm=(lo+hi)/2
                out.append((phase,jm,swe.calc_ut(jm,swe.SUN,FLG)[0][0],swe.calc_ut(jm,swe.MOON,FLG)[0][0]))
            prev=cur; j=jn
    return sorted(out,key=lambda x:x[1])

def jd2local(j):
    y,m,d,h=swe.revjul(j,swe.GREG_CAL)
    u=dt.datetime(y,m,d,tzinfo=dt.timezone.utc)+dt.timedelta(hours=h)
    return u.astimezone(TZ)

# ================= markdown =================
def md():
    o=["## PART 4: TIMING (reference 30 August 2026, 12:00 Europe/Skopje)\n"]
    o.append(f"Reference JD (UT): `{NOW_JD:.6f}` | UTC offset applied: `{NOW_OFF}` | UT: `{NOW_UTC}`\n")
    # 4.1
    o.append("### 4.1 Annual profection and Lord of the Year\n")
    o.append("| Subject | Age | Profected house (WS) | Sign | Lord of the Year | Year runs | Lord natal position | Natal house (P/WS) | Natal condition | Transiting position 30 Aug 2026 |")
    o.append("|---|---|---|---|---|---|---|---|---|---|")
    prof={}
    for lab,c,bd in (("A",A,(1994,7,5)),("B",B,(1995,1,27))):
        age,h,sign,lord,last,nxt=profection(c,*bd)
        prof[lab]=(age,h,sign,lord)
        lp=c[lord]; hp=house_of(lp['lon'],c['_cusps_P']); hw=house_of(lp['lon'],c['_ws'])
        code=dict(BODIES)[lord]
        tp=body_pos(NOW_JD,code)
        o.append(f"| {lab} | {age} | {h} | {sign} | **{lord}** | {last} → {nxt} | {fmt(lp['lon'])} ({lp['lon']:.4f}) | {hp} / {hw} | {condition(lord,signof(lp['lon']))} | {fmt(tp['lon'])} ({tp['lon']:.4f}, {tp['speed']:+.4f}, {'R' if tp['speed']<0 else 'D'}) |")
    o.append("")
    # 4.2
    o.append("### 4.2 Firdaria (Persian, 75-year cycle; sub-periods for the seven planets only)\n")
    for lab,c in (("A",A),("B",B)):
        fd=firdaria(c['_jd'], c['_day'])
        cur=[x for x in fd if x[2]<=NOW_JD<x[3]]
        idx=fd.index(cur[0]) if cur else None
        o.append(f"**Subject {lab}** — {'day' if c['_day'] else 'night'} sequence\n")
        o.append("| | Major lord | Minor lord | Start | End |")
        o.append("|---|---|---|---|---|")
        for k in range(max(0,idx-1), min(len(fd),idx+2)):
            mark="**CURRENT**" if k==idx else ("previous" if k<idx else "next")
            mj,mn,s,e=fd[k]
            o.append(f"| {mark} | {mj} | {mn or '—'} | {jd2d(s)} | {jd2d(e)} |")
        mj,mn,s,e=fd[idx]
        majs=[x for x in fd if x[0]==mj]
        o.append(f"\n- Current major lord: **{mj}** ({jd2d(majs[0][2])} → {jd2d(majs[-1][3])})")
        o.append(f"- Current minor lord: **{mn}** ({jd2d(s)} → {jd2d(e)})")
        o.append(f"- Handover before: {jd2d(fd[idx-1][2])} → {jd2d(fd[idx-1][3])} ({fd[idx-1][0]}/{fd[idx-1][1]})")
        o.append(f"- Handover after: {jd2d(fd[idx+1][2])} → {jd2d(fd[idx+1][3])} ({fd[idx+1][0]}/{fd[idx+1][1]})\n")
    # 4.3
    o.append("### 4.3 Secondary progressions to 30 August 2026\n")
    o.append("Method: day-for-a-year (1 day of ephemeris time = 1 tropical year of 365.2422 days), chart cast for the birthplace at the progressed moment; ASC/MC from the progressed moment's own sidereal time.\n")
    PA=progressed(A,41.0297,21.3347); PB=progressed(B,41.7364,22.1917)
    o.append("| Subject | Elapsed yrs | Progressed JD | Prog Sun | Prog Moon | Prog Venus | Prog Mars | Prog ASC | Prog MC |")
    o.append("|---|---|---|---|---|---|---|---|---|")
    for lab,p in (("A",PA),("B",PB)):
        o.append(f"| {lab} | {p['_years']:.4f} | {p['_pjd']:.5f} | {fmt(p['Sun']['lon'])} | {fmt(p['Moon']['lon'])} | {fmt(p['Venus']['lon'])} | {fmt(p['Mars']['lon'])} | {fmt(p['ASC']['lon'])} | {fmt(p['MC']['lon'])} |")
    o.append("")
    PROGPTS=["Sun","Moon","Venus","Mars","ASC","MC"]
    NATPTS=BODY_NAMES+["ASC","MC","DSC","IC"]
    def lim15(a,b,asp): return 1.5
    def perfect_date(pchart, blat, blon, pname, tgt_lon, tgt_speed, ang, is_prog_target, pchart2=None):
        """Find when the progressed aspect perfects, within 24 months of ref."""
        def val(j):
            nj=pchart['_natal_jd']
            pc=chart(nj+(j-nj)/YR, blat, blon)
            l1=pc[pname]['lon']
            if is_prog_target:
                nj2=pchart2['_natal_jd']
                pc2=chart(nj2+(j-nj2)/YR, pchart2['_lat'], pchart2['_lon'])
                l2=pc2[is_prog_target]['lon']
            else:
                l2=tgt_lon
            d=(l1-l2-ang)%360
            return d-360 if d>180 else d
        j0=NOW_JD-1; j1=NOW_JD+730
        prev=val(j0); j=j0
        while j<j1:
            jn=min(j+10,j1); cur=val(jn)
            if (prev<0)!=(cur<0) and abs(cur-prev)<180:
                lo,hi=j,jn
                for _ in range(40):
                    mid=(lo+hi)/2
                    if (val(lo)<0)==(val(mid)<0): lo=mid
                    else: hi=mid
                return jd2d((lo+hi)/2)
            prev=cur; j=jn
        return "—"
    for lab,pc,other,blat,blon,pc2 in (
        ("Progressed A → Natal B",PA,B,41.0297,21.3347,None),
        ("Progressed B → Natal A",PB,A,41.7364,22.1917,None)):
        o.append(f"**{lab} (orb 1.5°)**\n")
        o.append("| Progressed point | Aspect | Natal point | Orb | App/Sep | Perfects within 24 months |")
        o.append("|---|---|---|---|---|---|")
        rows=[]
        for pn in PROGPTS:
            for nn in NATPTS:
                for r in find_aspects(pc[pn]['lon'],pc[pn]['speed'],pn,other[nn]['lon'],0,nn,MAJOR+MINOR,lim15):
                    ang=dict(MAJOR+MINOR)[r['asp']]
                    d=perfect_date(pc,blat,blon,pn,other[nn]['lon'],0,ang,None)
                    if d=="—":
                        d=perfect_date(pc,blat,blon,pn,other[nn]['lon'],0,-ang,None)
                    rows.append((r,d))
        for r,d in sorted(rows,key=lambda x:x[0]['orb']):
            o.append(f"| {r['a']} | {r['asp']} | {r['b']} | {orbfmt(r['orb'])} | {r['app']} | {d} |")
        o.append("")
    o.append("**Progressed A → Progressed B (orb 1.5°)**\n")
    o.append("| Prog A point | Aspect | Prog B point | Orb | App/Sep | Perfects within 24 months |")
    o.append("|---|---|---|---|---|---|")
    rows=[]
    for pn in PROGPTS:
        for qn in PROGPTS:
            for r in find_aspects(PA[pn]['lon'],PA[pn]['speed'],pn,PB[qn]['lon'],PB[qn]['speed'],qn,MAJOR+MINOR,lim15):
                ang=dict(MAJOR+MINOR)[r['asp']]
                d=perfect_date(PA,41.0297,21.3347,pn,None,0,ang,qn,PB)
                if d=="—": d=perfect_date(PA,41.0297,21.3347,pn,None,0,-ang,qn,PB)
                rows.append((r,d))
    for r,d in sorted(rows,key=lambda x:x[0]['orb']):
        o.append(f"| A-prog {r['a']} | {r['asp']} | B-prog {r['b']} | {orbfmt(r['orb'])} | {r['app']} | {d} |")
    o.append("")
    # 4.4
    o.append("### 4.4 Outer-planet transits, 30 Aug 2026 – 31 Dec 2027\n")
    o.append("Aspects: conjunction, opposition, trine, square, sextile. Every retrograde pass listed separately. Station-in-orb tested at 1°.\n")
    j0=NOW_JD; j1=local_to_jd(2027,12,31,23,59)[0]
    targets=[]
    for lab,c,pts in (("A",A,["ASC","MC","DSC","IC","Sun","Moon"]),
                      ("B",B,["ASC","MC","DSC","IC","Sun","Moon"]),
                      ("Composite",COMP,["ASC","MC","Sun","Moon","Venus"]),
                      ("Davison",DAV,["ASC","MC","Sun","Moon","Venus"])):
        for p in pts: targets.append((f"{lab} {p}", c[p]['lon']))
    o.append("| Transiting planet | Aspect | Target | Target position | Exact date | Station inside orb |")
    o.append("|---|---|---|---|---|---|")
    trows=[]
    for pname,code in TR:
        for tname,tl in targets:
            for aname,ang in MAJOR:
                for jp in find_perfections(code,tl,ang,j0,j1):
                    st,info=station_in_orb(code,jp,tl,ang)
                    trows.append((jp,pname,aname,tname,tl,st,info))
    for jp,pn,an,tn,tl,st,info in sorted(trows):
        o.append(f"| {pn} | {an} | {tn} | {fmt(tl)} | {jd2d(jp)} | {('YES — station '+info) if st else 'no'} |")
    o.append("")
    # 4.5
    o.append("### 4.5 New and full moons within 2° of a composite/Davison angle, luminary or Venus\n")
    o.append("| Phase | Date | Time (Europe/Skopje) | Sun degree | Moon degree | Target | Target position | Orb |")
    o.append("|---|---|---|---|---|---|---|---|")
    ltargets=[]
    for lab,c in (("Composite",COMP),("Davison",DAV)):
        for p in ["ASC","MC","DSC","IC","Sun","Moon","Venus"]:
            ltargets.append((f"{lab} {p}", c[p]['lon']))
    cnt=0
    for phase,jm,sl,ml in lunations(j0,j1):
        loc=jd2local(jm)
        for tn,tl in ltargets:
            for ang in (0,180):
                d=abs(sep(sl,tl)-ang)
                if d<=2.0:
                    cnt+=1
                    rel="conjunct" if ang==0 else "opposite"
                    o.append(f"| {phase} | {loc.strftime('%Y-%m-%d')} | {loc.strftime('%H:%M:%S %Z')} | {fmt(sl)} | {fmt(ml)} | {tn} ({rel}) | {fmt(tl)} | {orbfmt(d)} |")
    if cnt==0: o.append("| — | — | — | — | — | none within 2° | — | — |")
    o.append("")
    return "\n".join(o)

if __name__=="__main__":
    natal_md(A); natal_md(B); print(md())
