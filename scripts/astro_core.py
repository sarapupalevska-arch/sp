import swisseph as swe, math, datetime as dt
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Europe/Skopje")
SIGNS = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra","Scorpio",
         "Sagittarius","Capricorn","Aquarius","Pisces"]

BODIES = [("Sun",swe.SUN),("Moon",swe.MOON),("Mercury",swe.MERCURY),("Venus",swe.VENUS),
    ("Mars",swe.MARS),("Jupiter",swe.JUPITER),("Saturn",swe.SATURN),("Uranus",swe.URANUS),
    ("Neptune",swe.NEPTUNE),("Pluto",swe.PLUTO),("Chiron",swe.CHIRON),
    ("True Node",swe.TRUE_NODE),("Mean Node",swe.MEAN_NODE),("Mean Lilith",swe.MEAN_APOG)]

swe.set_ephe_path("/home/user/eph")
FLG = swe.FLG_SWIEPH | swe.FLG_SPEED

def local_to_jd(y,m,d,hh,mm,tz=TZ):
    loc = dt.datetime(y,m,d,hh,mm,tzinfo=tz)
    off = loc.utcoffset()
    u = loc.astimezone(dt.timezone.utc)
    ut = u.hour + u.minute/60 + u.second/3600
    jd = swe.julday(u.year,u.month,u.day,ut,swe.GREG_CAL)
    return jd, off, u

def dms(lon):
    lon = lon % 360.0
    s = int(lon//30); r = lon-30*s
    dg = int(r); rm=(r-dg)*60; mi=int(rm); se=(rm-mi)*60
    sec = int(round(se))
    if sec==60: sec=0; mi+=1
    if mi==60: mi=0; dg+=1
    return SIGNS[s], dg, mi, sec

def fmt(lon):
    sg,d,m,s = dms(lon)
    return f"{sg} {d:02d} {m:02d} {s:02d}"

def orbfmt(o):
    o=abs(o); d=int(o); m=(o-d)*60
    return f"{d}°{m:04.1f}'"

def body_pos(jd, code):
    xx,_ = swe.calc_ut(jd, code, FLG)
    lon, lat, dist, slon = xx[0], xx[1], xx[2], xx[3]
    e = swe.calc_ut(jd, code, FLG|swe.FLG_EQUATORIAL)[0]
    return dict(lon=lon, lat=lat, speed=slon, decl=e[1], ra=e[0])

def chart(jd, lat, lon, hsys=b'P'):
    c = {}
    for name, code in BODIES:
        c[name] = body_pos(jd, code)
    cusps, ascmc = swe.houses_ex(jd, lat, lon, hsys)
    c['_cusps_P'] = list(cusps)
    asc, mc = ascmc[0], ascmc[1]
    for nm, v in (("ASC",asc),("MC",mc),("DSC",(asc+180)%360),("IC",(mc+180)%360)):
        c[nm] = dict(lon=v, lat=0.0, speed=0.0, decl=decl_of(v), ra=0.0)
    c['_jd']=jd; c['_lat']=lat; c['_lon']=lon
    c['_ws'] = [ (int(asc//30)*30 + 30*i) % 360 for i in range(12) ]
    return c

def decl_of(lon, lat=0.0, jd=None):
    eps = 23.4392911 if jd is None else swe.calc_ut(jd, swe.ECL_NUT)[0][0]
    l=math.radians(lon); b=math.radians(lat); e=math.radians(eps)
    return math.degrees(math.asin(math.sin(b)*math.cos(e)+math.cos(b)*math.sin(e)*math.sin(l)))

def house_of(lon, cusps):
    # cusps: list of 13 (index 0 unused from swe) or 12-list
    cs = cusps[1:13] if len(cusps)==13 else cusps
    for i in range(12):
        a=cs[i]; b=cs[(i+1)%12]
        span=(b-a)%360
        if span==0: span=360
        if (lon-a)%360 < span: return i+1
    return 12
