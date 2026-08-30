import sys; sys.path.insert(0,'scripts')
from part1 import A,B,natal_md
from astro_lib import *
import swisseph as swe, math, datetime as dt

SKO_LAT, SKO_LON = 41.9973, 21.4280
BODY_NAMES=[n for n,_ in BODIES]

def midp(a,b):
    d=(b-a)%360
    m=(a+d/2)%360
    return m if d<=180 else (m+180)%360   # closest midpoint

# ---------- 3.1 composite ----------
COMP={}
for n in BODY_NAMES:
    l=midp(A[n]['lon'],B[n]['lon'])
    COMP[n]=dict(lon=l, speed=(A[n]['speed']+B[n]['speed'])/2, decl=decl_of(l))
comp_mc = midp(A['MC']['lon'],B['MC']['lon'])
# ASC derived from composite MC + Skopje latitude via obliquity/ARMC relation
eps = math.radians(swe.calc_ut(A['_jd'], swe.ECL_NUT)[0][0])
def armc_from_mc(mc):
    mcr=math.radians(mc)
    ra=math.atan2(math.sin(mcr)*math.cos(eps), math.cos(mcr))
    return math.degrees(ra)%360
armc = armc_from_mc(comp_mc)
_c,_a = swe.houses_armc(armc, SKO_LAT, math.degrees(eps), b'P')
comp_asc=_a[0]
COMP['ASC']=dict(lon=comp_asc,speed=0,decl=decl_of(comp_asc))
COMP['MC']=dict(lon=comp_mc,speed=0,decl=decl_of(comp_mc))
COMP['DSC']=dict(lon=(comp_asc+180)%360,speed=0,decl=decl_of((comp_asc+180)%360))
COMP['IC']=dict(lon=(comp_mc+180)%360,speed=0,decl=decl_of((comp_mc+180)%360))
COMP['_cusps_P']=list(_c); COMP['_ws']=[(int(comp_asc//30)*30+30*i)%360 for i in range(12)]

# ---------- 3.2 Davison ----------
jdD=(A['_jd']+B['_jd'])/2
def gc_mid(lat1,lon1,lat2,lon2):
    p1,l1,p2,l2=map(math.radians,(lat1,lon1,lat2,lon2))
    bx=math.cos(p2)*math.cos(l2-l1); by=math.cos(p2)*math.sin(l2-l1)
    lat=math.atan2(math.sin(p1)+math.sin(p2), math.sqrt((math.cos(p1)+bx)**2+by**2))
    lon=l1+math.atan2(by, math.cos(p1)+bx)
    return math.degrees(lat), math.degrees(lon)
dlat,dlon = gc_mid(41.0297,21.3347,41.7364,22.1917)
DAV = chart(jdD, dlat, dlon)
y,m,d,h = swe.revjul(jdD, swe.GREG_CAL)
dav_utc = dt.datetime(y,m,d,tzinfo=dt.timezone.utc)+dt.timedelta(hours=h)
dav_loc = dav_utc.astimezone(TZ)

def table(c,names,title):
    o=[f"**{title}**\n","| Body | Sign D M S | Longitude | Speed/day | Rx | Decl | House (P) | House (WS) |","|---|---|---|---|---|---|---|---|"]
    for n in names:
        p=c[n]; rx="R" if p['speed']<0 else "D"
        hp=house_of(p['lon'],c['_cusps_P']); hw=house_of(p['lon'],c['_ws'])
        o.append(f"| {n} | {fmt(p['lon'])} | {p['lon']:.4f} | {p['speed']:+.4f} | {rx} | {p['decl']:+.2f} | {hp} | {hw} |")
    return "\n".join(o)

def internal(c,names,orb):
    def lim(a,b,asp): return orb
    res=[]
    for i in range(len(names)):
        for j in range(i+1,len(names)):
            n1,n2=names[i],names[j]
            if {n1,n2} in ({"True Node","Mean Node"},{"ASC","DSC"},{"MC","IC"},{"ASC","MC"}): continue
            res+=find_aspects(c[n1]['lon'],c[n1]['speed'],n1,c[n2]['lon'],c[n2]['speed'],n2,MAJOR,lim)
    o=["| Body 1 | Aspect | Body 2 | Orb |","|---|---|---|---|"]
    for r in sorted(res,key=lambda x:x['orb']):
        o.append(f"| {r['a']} | {r['asp']} | {r['b']} | {orbfmt(r['orb'])} |")
    return "\n".join(o)

NAMES=BODY_NAMES+["ASC","MC","DSC","IC"]

def md():
    o=["## PART 3: THE RELATIONSHIP CHARTS\n","### 3.1 Composite midpoint chart\n"]
    o.append("Derivation method: planetary positions are **closest (shorter-arc) midpoints** of the two natal longitudes. "
             "The composite MC is the closest midpoint of the two natal MCs; the composite ASC is derived by converting that "
             "composite MC to its RAMC (using the obliquity of the ecliptic) and computing the Ascendant for **Skopje latitude 41.9973 N** "
             "from that RAMC. House cusps are Placidus from the same RAMC/latitude. This is the *midpoint-MC / derived-ASC* method, "
             "not the midpoint-of-Ascendants method.\n")
    o.append(f"Composite MC = {fmt(comp_mc)} ({comp_mc:.4f}); RAMC = {armc:.4f}°; obliquity = {math.degrees(eps):.6f}°\n")
    o.append(table(COMP,NAMES,"Composite positions"))
    o.append("\n**Composite house cusps**\n")
    o.append("| House | Placidus | Long. | Whole sign |")
    o.append("|---|---|---|---|")
    for i in range(12):
        o.append(f"| {i+1} | {fmt(COMP['_cusps_P'][i])} | {COMP['_cusps_P'][i]:.4f} | {fmt(COMP['_ws'][i])} |")
    o.append("\n**Composite internal aspects (orb 5°)**\n")
    o.append(internal(COMP,NAMES,5.0))
    o.append("\n### 3.2 Davison relationship chart\n")
    o.append(f"- Time midpoint (JD UT): `{jdD:.6f}`")
    o.append(f"- Davison moment UTC: **{dav_utc.strftime('%Y-%m-%d %H:%M:%S')} UTC**")
    o.append(f"- Davison moment Europe/Skopje: **{dav_loc.strftime('%Y-%m-%d %H:%M:%S %Z')}** (offset {dav_loc.utcoffset()})")
    o.append(f"- Great-circle midpoint of birthplaces: **lat {dlat:.4f} N, lon {dlon:.4f} E**\n")
    o.append(table(DAV,NAMES,"Davison positions"))
    o.append("\n**Davison house cusps**\n")
    o.append("| House | Placidus | Long. | Whole sign |")
    o.append("|---|---|---|---|")
    for i in range(12):
        o.append(f"| {i+1} | {fmt(DAV['_cusps_P'][i])} | {DAV['_cusps_P'][i]:.4f} | {fmt(DAV['_ws'][i])} |")
    o.append("\n**Davison internal aspects (orb 5°)**\n")
    o.append(internal(DAV,NAMES,5.0))
    o.append("\n### 3.3 Composite vs Davison comparison\n")
    o.append("| Body | Composite sign | Davison sign | Sign agree | Comp house (P) | Dav house (P) | House agree (P) | Comp house (WS) | Dav house (WS) | House agree (WS) |")
    o.append("|---|---|---|---|---|---|---|---|---|---|")
    for n in NAMES:
        cs=signof(COMP[n]['lon']); ds=signof(DAV[n]['lon'])
        ch=house_of(COMP[n]['lon'],COMP['_cusps_P']); dh=house_of(DAV[n]['lon'],DAV['_cusps_P'])
        cw=house_of(COMP[n]['lon'],COMP['_ws']); dw=house_of(DAV[n]['lon'],DAV['_ws'])
        o.append(f"| {n} | {cs} | {ds} | {'AGREE' if cs==ds else 'DISAGREE'} | {ch} | {dh} | {'AGREE' if ch==dh else 'DISAGREE'} | {cw} | {dw} | {'AGREE' if cw==dw else 'DISAGREE'} |")
    o.append("")
    return "\n".join(o)

if __name__=="__main__":
    natal_md(A); natal_md(B); print(md())
