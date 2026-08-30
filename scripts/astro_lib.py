import sys; sys.path.insert(0,'scripts')
from astro_core import *
import swisseph as swe, math, datetime as dt

RULER = {"Aries":"Mars","Taurus":"Venus","Gemini":"Mercury","Cancer":"Moon","Leo":"Sun",
 "Virgo":"Mercury","Libra":"Venus","Scorpio":"Mars","Sagittarius":"Jupiter",
 "Capricorn":"Saturn","Aquarius":"Saturn","Pisces":"Jupiter"}
DOMICILE = {"Sun":["Leo"],"Moon":["Cancer"],"Mercury":["Gemini","Virgo"],"Venus":["Taurus","Libra"],
 "Mars":["Aries","Scorpio"],"Jupiter":["Sagittarius","Pisces"],"Saturn":["Capricorn","Aquarius"]}
EXALT = {"Sun":"Aries","Moon":"Taurus","Mercury":"Virgo","Venus":"Pisces","Mars":"Capricorn",
 "Jupiter":"Cancer","Saturn":"Libra"}
FALL = {k:SIGNS[(SIGNS.index(v)+6)%12] for k,v in EXALT.items()}
DETRI = {k:[SIGNS[(SIGNS.index(s)+6)%12] for s in v] for k,v in DOMICILE.items()}

def condition(planet, sign):
    if planet in DOMICILE and sign in DOMICILE[planet]: return "domicile"
    if EXALT.get(planet)==sign: return "exaltation"
    if planet in DETRI and sign in DETRI[planet]: return "detriment"
    if FALL.get(planet)==sign: return "fall"
    return "peregrine"

def signof(lon): return SIGNS[int((lon%360)//30)]

# ---------- aspects ----------
MAJOR = [("conjunction",0),("opposition",180),("trine",120),("square",90),("sextile",60)]
MINOR = [("quincunx",150),("semisextile",30),("semisquare",45),("sesquiquadrate",135),
         ("quintile",72),("biquintile",144)]
LUMS = {"Sun","Moon"}
PERSONAL = {"Mercury","Venus","Mars"}
ANGLES = {"ASC","MC","DSC","IC"}

def sep(a,b):
    d = abs((a-b)%360)
    return d if d<=180 else 360-d

def orb_limit_syn(n1,n2,aspname):
    if aspname in ("quincunx","semisextile"): return 3.0
    if aspname in ("semisquare","sesquiquadrate"): return 2.0
    if aspname in ("quintile","biquintile"): return 1.5
    def cat(n):
        if n in LUMS: return 8.0
        if n in PERSONAL: return 6.0
        return 5.0
    return min(cat(n1),cat(n2))

def find_aspects(l1,s1,n1,l2,s2,n2,aspects,limitfn):
    out=[]
    d = sep(l1,l2)
    for nm,ang in aspects:
        lim = limitfn(n1,n2,nm)
        o = d-ang
        if abs(o)<=lim:
            # applying/separating
            fut = sep((l1+s1*0.01)%360,(l2+s2*0.01)%360)
            app = "applying" if abs(fut-ang)<abs(d-ang) else "separating"
            out.append(dict(a=n1,b=n2,asp=nm,orb=abs(o),app=app,tight=abs(o)<1.0))
    return out

# ---------- lots ----------
def is_day(sun_lon, asc_lon):
    # sun above horizon => houses 7..12 (i.e. sun between DSC..ASC going ccw? ) use altitude via house
    return ((sun_lon - asc_lon) % 360) > 180

def lots(c):
    asc=c['ASC']['lon']; sun=c['Sun']['lon']; moon=c['Moon']['lon']
    ven=c['Venus']['lon']; mar=c['Mars']['lon']; mer=c['Mercury']['lon']; sat=c['Saturn']['lon']
    day = is_day(sun,asc)
    L={}
    L['Fortune'] = (asc + (moon-sun if day else sun-moon))%360
    L['Spirit']  = (asc + (sun-moon if day else moon-sun))%360
    sp=L['Spirit']; fo=L['Fortune']
    L['Eros']    = (asc + (ven-sp if day else sp-ven))%360
    L['Necessity']=(asc + (fo-mer if day else mer-fo))%360
    L['Marriage (Venus-based, Hellenistic)'] = (asc + ven - sat) % 360
    L['Marriage (Saturn-based)'] = (asc + sat - ven) % 360
    return L, day

def antiscion(l): return (180-l)%360
def cantiscion(l): return (360-l)%360
