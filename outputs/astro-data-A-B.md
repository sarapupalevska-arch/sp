# Astrological data computation — Subjects A and B

All positions computed with Swiss Ephemeris via pyswisseph. Tropical zodiac, geocentric, apparent positions. No value in this document is recalled or estimated; every figure is a direct Swiss Ephemeris computation. UTC offsets resolved with `zoneinfo.ZoneInfo("Europe/Skopje")`.

**Subjects**

| | Name | Date | Local time | Place | Latitude | Longitude |
|---|---|---|---|---|---|---|
| A | Sara | 5 July 1994 | 14:45 | Bitola, North Macedonia | 41.0297 N | 21.3347 E |
| B | Trajche | 27 January 1995 | 07:15 | Stip, North Macedonia | 41.7364 N | 22.1917 E |

Reference location (composite angles, transits): Skopje, 41.9973 N, 21.4280 E. Reference moment for anything current: 30 August 2026, 12:00 Europe/Skopje.

Position format: `Sign DD MM SS | absolute ecliptic longitude (decimal, 4 dp) | daily speed | D/R | declination`.

## SANITY CHECK

- pyswisseph version: **2.10.3.2**
- swe.version: **2.10.03**
- Ephemeris: Swiss Ephemeris files (seas_18.se1, sepl_18.se1, semo_18.se1)

| Item | Computed UTC offset (zoneinfo Europe/Skopje) | UT | JD (UT) |
|---|---|---|---|
| A birth moment | `2:00:00` | 1994-07-05 12:45:00+00:00 | 2449539.031250 |
| B birth moment | `1:00:00` | 1995-01-27 06:15:00+00:00 | 2449744.760417 |
| Reference 30 Aug 2026 12:00 | `2:00:00` | 2026-08-30 10:00:00+00:00 | 2461282.916667 |

| Check | Expected | Computed | Match |
|---|---|---|---|
| A Ascendant | Scorpio ~6° | Scorpio 06 04 56 (216.0823) | MATCH |
| A Sun | Cancer ~13° | Cancer 13 16 06 (103.2684) | MATCH |
| B Sun | Aquarius | Aquarius 06 50 01 (306.8336) | MATCH |
| B Mercury | Aquarius | Aquarius 21 07 34 (321.1261) | MATCH |
| B Ascendant | Aquarius | Aquarius 14 07 31 (314.1252) | MATCH |
| B Mars | Leo, retrograde | Leo 28 46 10 (148.7693), speed -0.3120 (retrograde) | MATCH |

**All sanity checks: PASS**

---

## PART 1: THE TWO NATAL CHARTS

### Chart A (Sara)
UTC offset: `2:00:00` | UT: `1994-07-05 12:45:00+00:00` | JD(UT): `2449539.031250`

#### 1.1 / 1.2 Positions with houses
| Body | Sign D M S | Longitude | Speed/day | Rx | Decl | House (Placidus) | House (Whole Sign) |
|---|---|---|---|---|---|---|---|
| Sun | Cancer 13 16 06 | 103.2684 | +0.9537 | D | +22.78 | 9 | 9 |
| Moon | Gemini 04 45 56 | 64.7656 | +12.0159 | D | +20.04 | 8 | 8 |
| Mercury | Gemini 29 29 09 | 89.4859 | -0.1041 | R | +18.83 | 8 | 8 |
| Venus | Leo 23 27 42 | 143.4616 | +1.1441 | D | +15.29 | 10 | 10 |
| Mars | Gemini 01 07 52 | 61.1312 | +0.7089 | D | +20.01 | 7 | 8 |
| Jupiter | Scorpio 04 47 07 | 214.7853 | +0.0102 | D | -12.01 | 12 | 1 |
| Saturn | Pisces 12 16 38 | 342.2771 | -0.0202 | R | -8.63 | 4 | 5 |
| Uranus | Capricorn 24 49 34 | 294.8261 | -0.0390 | R | -21.68 | 3 | 3 |
| Neptune | Capricorn 22 12 31 | 292.2086 | -0.0266 | R | -20.99 | 3 | 3 |
| Pluto | Scorpio 25 32 16 | 235.5378 | -0.0161 | R | -5.33 | 1 | 1 |
| Chiron | Virgo 06 28 20 | 156.4722 | +0.1037 | D | +4.67 | 10 | 11 |
| True Node | Scorpio 22 50 24 | 232.8400 | -0.0288 | R | -18.48 | 1 | 1 |
| Mean Node | Scorpio 21 16 19 | 231.2720 | -0.0529 | R | -18.08 | 1 | 1 |
| Mean Lilith | Taurus 09 55 48 | 39.9299 | +0.1108 | D | +15.75 | 7 | 7 |

**Angles**
| Point | Sign D M S | Longitude | Decl |
|---|---|---|---|
| ASC | Scorpio 06 04 56 | 216.0823 | -13.55 |
| MC | Leo 13 24 18 | 133.4051 | +16.80 |
| DSC | Taurus 06 04 56 | 36.0823 | +13.55 |
| IC | Aquarius 13 24 18 | 313.4051 | -16.80 |

**House cusps**
| House | Placidus cusp | Placidus long. | Whole-sign cusp | WS long. |
|---|---|---|---|---|
| 1 | Scorpio 06 04 56 | 216.0823 | Scorpio 00 00 00 | 210.0000 |
| 2 | Sagittarius 04 45 20 | 244.7557 | Sagittarius 00 00 00 | 240.0000 |
| 3 | Capricorn 07 52 19 | 277.8720 | Capricorn 00 00 00 | 270.0000 |
| 4 | Aquarius 13 24 18 | 313.4051 | Aquarius 00 00 00 | 300.0000 |
| 5 | Pisces 16 21 03 | 346.3508 | Pisces 00 00 00 | 330.0000 |
| 6 | Aries 13 47 59 | 13.7997 | Aries 00 00 00 | 0.0000 |
| 7 | Taurus 06 04 56 | 36.0823 | Taurus 00 00 00 | 30.0000 |
| 8 | Gemini 04 45 20 | 64.7557 | Gemini 00 00 00 | 60.0000 |
| 9 | Cancer 07 52 19 | 97.8720 | Cancer 00 00 00 | 90.0000 |
| 10 | Leo 13 24 18 | 133.4051 | Leo 00 00 00 | 120.0000 |
| 11 | Virgo 16 21 03 | 166.3508 | Virgo 00 00 00 | 150.0000 |
| 12 | Libra 13 47 59 | 193.7997 | Libra 00 00 00 | 180.0000 |

#### 1.3 Sect and Ascendant ruler
- Chart: **DAY**
- Sect light: **Sun** (Cancer 13 16 06)
- Ascendant sign: **Scorpio**; ruler: **Mars**
- Mars: Gemini 01 07 52 (61.1312), Placidus house 7, whole-sign house 8, condition: **peregrine**

#### 1.4 Lots
| Lot | Formula used | Sign D M S | Longitude | House (P) | House (WS) |
|---|---|---|---|---|---|
| Fortune | ASC + Moon − Sun | Virgo 27 34 46 | 177.5794 | 11 | 11 |
| Spirit | ASC + Sun − Moon | Sagittarius 14 35 06 | 254.5851 | 2 | 2 |
| Eros | ASC + Venus − Spirit | Cancer 14 57 32 | 104.9588 | 9 | 9 |
| Necessity | ASC + Fortune − Mercury | Aquarius 04 10 33 | 304.1758 | 3 | 4 |
| Marriage (Venus-based, Hellenistic) | ASC + Venus − Saturn | Aries 17 16 00 | 17.2668 | 6 | 6 |
| Marriage (Saturn-based) | ASC + Saturn − Venus | Taurus 24 53 52 | 54.8978 | 7 | 7 |

#### 1.5 Internal natal aspects
| Body 1 | Aspect | Body 2 | Orb | Applying/Separating |
|---|---|---|---|---|
| Moon | quincunx | Jupiter | 0°01.2' | separating |
| Sun | semisextile | MC | 0°08.2' | applying |
| Mars | quintile | MC | 0°16.4' | applying |
| Chiron | sextile | ASC | 0°23.4' | separating |
| Venus | quintile | ASC | 0°37.2' | applying |
| Venus | square | True Node | 0°37.3' | separating |
| Neptune | sextile | True Node | 0°37.9' | applying |
| Mercury | biquintile | True Node | 0°38.8' | applying |
| Venus | quintile | Jupiter | 0°40.6' | separating |
| Uranus | sextile | Pluto | 0°42.7' | separating |
| Neptune | sesquiquadrate | Chiron | 0°44.2' | applying |
| Neptune | sextile | Mean Node | 0°56.2' | separating |
| Sun | trine | Saturn | 0°59.5' | separating |
| Mercury | semisquare | MC | 1°04.9' | applying |
| Saturn | quincunx | MC | 1°07.7' | separating |
| Venus | quincunx | Neptune | 1°15.2' | separating |
| Jupiter | conjunction | ASC | 1°17.8' | applying |
| Moon | quincunx | ASC | 1°19.0' | applying |
| Venus | quincunx | Uranus | 1°21.9' | applying |
| Mercury | semisextile | Mars | 1°38.7' | separating |
| Jupiter | sextile | Chiron | 1°41.2' | separating |
| Moon | square | Chiron | 1°42.4' | applying |
| Uranus | sextile | True Node | 1°59.2' | applying |
| Venus | square | Pluto | 2°04.6' | applying |
| Venus | square | Mean Node | 2°11.4' | separating |
| Saturn | sextile | Mean Lilith | 2°20.8' | applying |
| Uranus | conjunction | Neptune | 2°37.0' | applying |
| Pluto | conjunction | True Node | 2°41.9' | separating |
| Neptune | sextile | Pluto | 3°19.8' | separating |
| Sun | sextile | Mean Lilith | 3°20.3' | separating |
| Chiron | trine | Mean Lilith | 3°27.5' | separating |
| Mean Lilith | square | MC | 3°28.5' | applying |
| Uranus | sextile | Mean Node | 3°33.2' | separating |
| Moon | conjunction | Mars | 3°38.1' | separating |
| Mean Lilith | opposition | ASC | 3°50.9' | separating |
| Pluto | conjunction | Mean Node | 4°15.9' | separating |

#### 1.6 Seventh house
- 7th cusp (Placidus): Taurus 06 04 56 — sign **Taurus**
- 7th cusp (whole sign): Taurus 00 00 00 — sign **Taurus**
- Placidus 7th ruler: **Venus** — Leo 23 27 42, Placidus house 10, WS house 10, dignity: peregrine
  - Aspects to Venus: quintile ASC (0°37.2', applying); square True Node (0°37.3', separating); quintile Jupiter (0°40.6', separating); quincunx Neptune (1°15.2', separating); quincunx Uranus (1°21.9', applying); square Pluto (2°04.6', applying); square Mean Node (2°11.4', separating)
- Whole sign 7th ruler: **Venus** — Leo 23 27 42, Placidus house 10, WS house 10, dignity: peregrine
  - Aspects to Venus: quintile ASC (0°37.2', applying); square True Node (0°37.3', separating); quintile Jupiter (0°40.6', separating); quincunx Neptune (1°15.2', separating); quincunx Uranus (1°21.9', applying); square Pluto (2°04.6', applying); square Mean Node (2°11.4', separating)
- Planets in 7th (Placidus): Mars, Mean Lilith
- Planets in 7th (Whole sign): Mean Lilith

### Chart B (Trajche)
UTC offset: `1:00:00` | UT: `1995-01-27 06:15:00+00:00` | JD(UT): `2449744.760417`

#### 1.1 / 1.2 Positions with houses
| Body | Sign D M S | Longitude | Speed/day | Rx | Decl | House (Placidus) | House (Whole Sign) |
|---|---|---|---|---|---|---|---|
| Sun | Aquarius 06 50 01 | 306.8336 | +1.0167 | D | -18.56 | 12 | 1 |
| Moon | Sagittarius 17 10 55 | 257.1819 | +14.4807 | D | -19.84 | 10 | 11 |
| Mercury | Aquarius 21 07 34 | 321.1261 | -0.2301 | R | -12.71 | 1 | 1 |
| Venus | Sagittarius 20 30 42 | 260.5116 | +1.0902 | D | -20.03 | 10 | 11 |
| Mars | Leo 28 46 10 | 148.7693 | -0.3120 | R | +15.98 | 7 | 7 |
| Jupiter | Sagittarius 09 34 15 | 249.5707 | +0.1649 | D | -21.13 | 10 | 11 |
| Saturn | Pisces 10 32 29 | 340.5413 | +0.1090 | D | -9.25 | 1 | 2 |
| Uranus | Capricorn 27 00 50 | 297.0138 | +0.0585 | D | -21.24 | 12 | 12 |
| Neptune | Capricorn 23 33 29 | 293.5582 | +0.0372 | D | -20.84 | 12 | 12 |
| Pluto | Sagittarius 00 13 42 | 240.2283 | +0.0207 | D | -7.03 | 9 | 11 |
| Chiron | Virgo 26 10 05 | 176.1680 | -0.0321 | R | -2.76 | 7 | 8 |
| True Node | Scorpio 10 43 58 | 220.7328 | -0.0809 | R | -15.04 | 9 | 10 |
| Mean Node | Scorpio 10 22 39 | 220.3775 | -0.0529 | R | -14.93 | 9 | 10 |
| Mean Lilith | Gemini 02 43 20 | 62.7223 | +0.1110 | D | +18.78 | 3 | 5 |

**Angles**
| Point | Sign D M S | Longitude | Decl |
|---|---|---|---|
| ASC | Aquarius 14 07 31 | 314.1252 | -16.59 |
| MC | Sagittarius 03 59 56 | 243.9990 | -20.95 |
| DSC | Leo 14 07 31 | 134.1252 | +16.59 |
| IC | Gemini 03 59 56 | 63.9990 | +20.95 |

**House cusps**
| House | Placidus cusp | Placidus long. | Whole-sign cusp | WS long. |
|---|---|---|---|---|
| 1 | Aquarius 14 07 31 | 314.1252 | Aquarius 00 00 00 | 300.0000 |
| 2 | Aries 02 56 33 | 2.9425 | Pisces 00 00 00 | 330.0000 |
| 3 | Taurus 08 48 53 | 38.8148 | Aries 00 00 00 | 0.0000 |
| 4 | Gemini 03 59 56 | 63.9990 | Taurus 00 00 00 | 30.0000 |
| 5 | Gemini 24 54 44 | 84.9122 | Gemini 00 00 00 | 60.0000 |
| 6 | Cancer 16 12 35 | 106.2098 | Cancer 00 00 00 | 90.0000 |
| 7 | Leo 14 07 31 | 134.1252 | Leo 00 00 00 | 120.0000 |
| 8 | Libra 02 56 33 | 182.9425 | Virgo 00 00 00 | 150.0000 |
| 9 | Scorpio 08 48 53 | 218.8148 | Libra 00 00 00 | 180.0000 |
| 10 | Sagittarius 03 59 56 | 243.9990 | Scorpio 00 00 00 | 210.0000 |
| 11 | Sagittarius 24 54 44 | 264.9122 | Sagittarius 00 00 00 | 240.0000 |
| 12 | Capricorn 16 12 35 | 286.2098 | Capricorn 00 00 00 | 270.0000 |

#### 1.3 Sect and Ascendant ruler
- Chart: **DAY**
- Sect light: **Sun** (Aquarius 06 50 01)
- Ascendant sign: **Aquarius**; ruler: **Saturn**
- Saturn: Pisces 10 32 29 (340.5413), Placidus house 1, whole-sign house 2, condition: **peregrine**

#### 1.4 Lots
| Lot | Formula used | Sign D M S | Longitude | House (P) | House (WS) |
|---|---|---|---|---|---|
| Fortune | ASC + Moon − Sun | Sagittarius 24 28 25 | 264.4735 | 10 | 11 |
| Spirit | ASC + Sun − Moon | Aries 03 46 37 | 3.7769 | 2 | 3 |
| Eros | ASC + Venus − Spirit | Scorpio 00 51 36 | 210.8599 | 8 | 10 |
| Necessity | ASC + Fortune − Mercury | Sagittarius 17 28 21 | 257.4726 | 10 | 11 |
| Marriage (Venus-based, Hellenistic) | ASC + Venus − Saturn | Scorpio 24 05 44 | 234.0955 | 9 | 10 |
| Marriage (Saturn-based) | ASC + Saturn − Venus | Taurus 04 09 18 | 34.1549 | 2 | 4 |

#### 1.5 Internal natal aspects
| Body 1 | Aspect | Body 2 | Orb | Applying/Separating |
|---|---|---|---|---|
| Mars | quintile | True Node | 0°02.2' | applying |
| Saturn | trine | Mean Node | 0°09.8' | separating |
| Saturn | trine | True Node | 0°11.5' | applying |
| Mars | quintile | Mean Node | 0°23.5' | applying |
| Chiron | semisquare | True Node | 0°26.1' | separating |
| Mercury | quintile | Jupiter | 0°26.7' | separating |
| Mercury | sextile | Venus | 0°36.9' | applying |
| Mars | biquintile | Neptune | 0°47.3' | separating |
| Chiron | semisquare | Mean Node | 0°47.4' | separating |
| Jupiter | semisextile | Mean Node | 0°48.4' | applying |
| Neptune | quintile | True Node | 0°49.5' | separating |
| Uranus | trine | Chiron | 0°50.7' | separating |
| Mercury | biquintile | Chiron | 0°57.5' | applying |
| Jupiter | square | Saturn | 0°58.2' | applying |
| Jupiter | semisquare | Neptune | 1°00.8' | separating |
| Jupiter | semisextile | True Node | 1°09.7' | applying |
| Neptune | quintile | Mean Node | 1°10.8' | separating |
| Mean Lilith | opposition | MC | 1°16.6' | applying |
| Sun | semisquare | Venus | 1°19.3' | applying |
| Jupiter | quintile | Chiron | 1°24.2' | separating |
| Mars | square | Pluto | 1°27.5' | separating |
| Saturn | semisquare | Uranus | 1°28.3' | applying |
| Mars | quincunx | Uranus | 1°45.3' | applying |
| Saturn | semisquare | Neptune | 1°59.0' | separating |
| Mercury | semisextile | Neptune | 2°25.9' | separating |
| Pluto | opposition | Mean Lilith | 2°29.6' | separating |
| Mars | semisextile | Chiron | 2°36.1' | applying |
| Neptune | trine | Chiron | 2°36.6' | applying |
| Sun | sextile | Jupiter | 2°44.2' | applying |
| Sun | sextile | MC | 2°50.1' | separating |
| Moon | sextile | ASC | 3°03.4' | separating |
| Uranus | sextile | Pluto | 3°12.9' | applying |
| Moon | conjunction | Venus | 3°19.8' | applying |
| True Node | square | ASC | 3°23.5' | separating |
| Uranus | conjunction | Neptune | 3°27.3' | separating |
| Sun | square | Mean Node | 3°32.6' | applying |
| Mean Node | square | ASC | 3°44.9' | separating |
| Pluto | conjunction | MC | 3°46.2' | applying |
| Sun | square | True Node | 3°53.9' | applying |
| Moon | sextile | Mercury | 3°56.7' | applying |
| Mars | square | Mean Lilith | 3°57.2' | separating |
| Pluto | sextile | Chiron | 4°03.6' | separating |
| Sun | trine | Mean Lilith | 4°06.7' | separating |
| Jupiter | sextile | ASC | 4°33.3' | applying |

#### 1.6 Seventh house
- 7th cusp (Placidus): Leo 14 07 31 — sign **Leo**
- 7th cusp (whole sign): Leo 00 00 00 — sign **Leo**
- Placidus 7th ruler: **Sun** — Aquarius 06 50 01, Placidus house 12, WS house 1, dignity: detriment
  - Aspects to Sun: semisquare Venus (1°19.3', applying); sextile Jupiter (2°44.2', applying); sextile MC (2°50.1', separating); square Mean Node (3°32.6', applying); square True Node (3°53.9', applying); trine Mean Lilith (4°06.7', separating)
- Whole sign 7th ruler: **Sun** — Aquarius 06 50 01, Placidus house 12, WS house 1, dignity: detriment
  - Aspects to Sun: semisquare Venus (1°19.3', applying); sextile Jupiter (2°44.2', applying); sextile MC (2°50.1', separating); square Mean Node (3°32.6', applying); square True Node (3°53.9', applying); trine Mean Lilith (4°06.7', separating)
- Planets in 7th (Placidus): Mars, Chiron
- Planets in 7th (Whole sign): Mars

---

## PART 2: SYNASTRY

### 2.1 Cross-aspect grid — sorted by orb (tightest first)

| A body | Aspect | B body | Orb | App/Sep | TIGHT |
|---|---|---|---|---|---|
| Lot Fortune | quintile | Jupiter | 0°00.5' | applying | TIGHT |
| Lot Necessity | square | Lot Marriage (Saturn-based) | 0°01.3' | separating | TIGHT |
| Lot Marriage (Venus-based, Hellenistic) | trine | Moon | 0°05.1' | applying | TIGHT |
| Venus | quincunx | Neptune | 0°05.8' | applying | TIGHT |
| Mean Node | square | Mercury | 0°08.8' | separating | TIGHT |
| Lot Eros | biquintile | Mercury | 0°10.0' | applying | TIGHT |
| Neptune | quintile | Mean Node | 0°10.1' | applying | TIGHT |
| Lot Necessity | sextile | MC | 0°10.6' | separating | TIGHT |
| Lot Necessity | trine | IC | 0°10.6' | separating | TIGHT |
| Lot Marriage (Venus-based, Hellenistic) | trine | Lot Necessity | 0°12.3' | separating | TIGHT |
| Uranus | semisquare | Jupiter | 0°15.3' | applying | TIGHT |
| Saturn | semisquare | Uranus | 0°15.8' | applying | TIGHT |
| Lot Eros | sesquiquadrate | Pluto | 0°16.2' | separating | TIGHT |
| Mars | quincunx | Lot Eros | 0°16.3' | separating | TIGHT |
| Uranus | semisextile | Lot Fortune | 0°21.2' | applying | TIGHT |
| Mean Lilith | quincunx | Jupiter | 0°21.6' | applying | TIGHT |
| Mercury | sesquiquadrate | ASC | 0°21.6' | applying | TIGHT |
| Mercury | semisquare | DSC | 0°21.6' | applying | TIGHT |
| Chiron | quincunx | Sun | 0°21.7' | separating | TIGHT |
| Lot Necessity | sextile | Lot Spirit | 0°23.9' | separating | TIGHT |
| Lot Marriage (Saturn-based) | quincunx | Lot Fortune | 0°25.5' | separating | TIGHT |
| Neptune | quintile | Lot Spirit | 0°25.9' | applying | TIGHT |
| Mean Lilith | opposition | Mean Node | 0°26.9' | applying | TIGHT |
| Lot Fortune | biquintile | Mercury | 0°27.2' | separating | TIGHT |
| Lot Marriage (Venus-based, Hellenistic) | semisquare | Mean Lilith | 0°27.3' | separating | TIGHT |
| Mean Lilith | sesquiquadrate | Lot Fortune | 0°27.4' | separating | TIGHT |
| Lot Spirit | sextile | ASC | 0°27.6' | separating | TIGHT |
| Lot Spirit | trine | DSC | 0°27.6' | separating | TIGHT |
| Sun | semisquare | Mars | 0°30.1' | applying | TIGHT |
| Neptune | quintile | True Node | 0°31.5' | applying | TIGHT |
| Neptune | biquintile | Mars | 0°33.6' | applying | TIGHT |
| Lot Fortune | trine | Uranus | 0°33.9' | applying | TIGHT |
| ASC | semisquare | Venus | 0°34.2' | applying | TIGHT |
| DSC | sesquiquadrate | Venus | 0°34.2' | applying | TIGHT |
| Lot Fortune | biquintile | Lot Marriage (Saturn-based) | 0°34.5' | separating | TIGHT |
| Mercury | biquintile | Lot Marriage (Venus-based, Hellenistic) | 0°36.6' | separating | TIGHT |
| Moon | semisextile | Lot Marriage (Saturn-based) | 0°36.6' | separating | TIGHT |
| Mean Lilith | sextile | Saturn | 0°36.7' | applying | TIGHT |
| Lot Eros | biquintile | Jupiter | 0°36.7' | separating | TIGHT |
| Pluto | sextile | Chiron | 0°37.8' | applying | TIGHT |
| Jupiter | opposition | Lot Marriage (Saturn-based) | 0°37.8' | separating | TIGHT |
| Venus | square | Lot Marriage (Venus-based, Hellenistic) | 0°38.0' | applying | TIGHT |
| Pluto | quintile | Sun | 0°42.2' | applying | TIGHT |
| Uranus | semisquare | Saturn | 0°42.9' | separating | TIGHT |
| Mercury | sextile | Mars | 0°43.0' | separating | TIGHT |
| True Node | sextile | Neptune | 0°43.1' | separating | TIGHT |
| IC | conjunction | ASC | 0°43.2' | separating | TIGHT |
| IC | opposition | DSC | 0°43.2' | separating | TIGHT |
| MC | opposition | ASC | 0°43.2' | separating | TIGHT |
| MC | conjunction | DSC | 0°43.2' | separating | TIGHT |
| Jupiter | semisquare | Venus | 0°43.6' | separating | TIGHT |
| Uranus | sextile | Lot Marriage (Venus-based, Hellenistic) | 0°43.8' | applying | TIGHT |
| Mercury | quincunx | Pluto | 0°44.5' | separating | TIGHT |
| ASC | square | Sun | 0°45.1' | separating | TIGHT |
| DSC | square | Sun | 0°45.1' | separating | TIGHT |
| Mean Node | semisextile | Venus | 0°45.6' | applying | TIGHT |
| Moon | opposition | MC | 0°46.0' | separating | TIGHT |
| Moon | conjunction | IC | 0°46.0' | separating | TIGHT |
| Jupiter | semisextile | MC | 0°47.2' | separating | TIGHT |
| Jupiter | quincunx | IC | 0°47.2' | separating | TIGHT |
| Lot Eros | quintile | Chiron | 0°47.4' | separating | TIGHT |
| Lot Marriage (Saturn-based) | opposition | Lot Marriage (Venus-based, Hellenistic) | 0°48.1' | separating | TIGHT |
| Mean Lilith | opposition | True Node | 0°48.2' | applying | TIGHT |
| Lot Marriage (Venus-based, Hellenistic) | biquintile | Lot Marriage (Venus-based, Hellenistic) | 0°49.7' | separating | TIGHT |
| Lot Eros | quincunx | ASC | 0°50.0' | separating | TIGHT |
| Lot Eros | semisextile | DSC | 0°50.0' | separating | TIGHT |
| Sun | quincunx | ASC | 0°51.4' | applying | TIGHT |
| Sun | semisextile | DSC | 0°51.4' | applying | TIGHT |
| Sun | quintile | Chiron | 0°54.0' | applying | TIGHT |
| Mars | opposition | Pluto | 0°54.2' | separating | TIGHT |
| Moon | sextile | Lot Spirit | 0°59.3' | separating | TIGHT |
| Mars | quintile | DSC | 0°59.6' | applying | TIGHT |
| Jupiter | quincunx | Lot Spirit | 1°00.5' | separating |  |
| Venus | trine | Lot Fortune | 1°00.7' | applying |  |
| Pluto | semisextile | Lot Fortune | 1°03.9' | applying |  |
| Neptune | semisextile | Mercury | 1°04.9' | separating |  |
| IC | quintile | Pluto | 1°10.6' | applying |  |
| Lot Eros | semisquare | Mars | 1°11.4' | separating |  |
| Lot Fortune | semisextile | Mars | 1°11.4' | applying |  |
| Lot Eros | quintile | Lot Marriage (Saturn-based) | 1°11.8' | separating |  |
| Mean Lilith | sesquiquadrate | Chiron | 1°14.3' | applying |  |
| Mean Lilith | biquintile | Moon | 1°15.1' | separating |  |
| True Node | conjunction | Lot Marriage (Venus-based, Hellenistic) | 1°15.3' | separating |  |
| Uranus | conjunction | Neptune | 1°16.1' | applying |  |
| Lot Marriage (Saturn-based) | trine | Chiron | 1°16.2' | applying |  |
| Lot Spirit | semisquare | Lot Eros | 1°16.5' | separating |  |
| MC | quintile | Mean Lilith | 1°19.0' | separating |  |
| Lot Necessity | semisquare | Venus | 1°20.1' | separating |  |
| Lot Marriage (Saturn-based) | trine | Neptune | 1°20.4' | applying |  |
| Uranus | trine | Chiron | 1°20.5' | separating |  |
| Mercury | biquintile | Sun | 1°20.9' | separating |  |
| Neptune | conjunction | Neptune | 1°21.0' | separating |  |
| Mercury | trine | Lot Eros | 1°22.4' | separating |  |
| Lot Fortune | conjunction | Chiron | 1°24.7' | separating |  |
| Pluto | conjunction | Lot Marriage (Venus-based, Hellenistic) | 1°26.5' | applying |  |
| Lot Necessity | trine | Mean Lilith | 1°27.2' | applying |  |
| Pluto | sextile | Uranus | 1°28.6' | separating |  |
| Saturn | trine | True Node | 1°32.7' | separating |  |
| Lot Fortune | sesquiquadrate | ASC | 1°32.7' | separating |  |
| Lot Fortune | semisquare | DSC | 1°32.7' | separating |  |
| Mars | conjunction | Mean Lilith | 1°35.5' | applying |  |
| True Node | semisextile | Lot Fortune | 1°38.0' | separating |  |
| Neptune | semisextile | Venus | 1°41.8' | applying |  |
| Lot Necessity | semisquare | Lot Necessity | 1°42.2' | separating |  |
| True Node | square | Mercury | 1°42.8' | separating |  |
| Lot Marriage (Venus-based, Hellenistic) | semisquare | IC | 1°43.9' | separating |  |
| Lot Marriage (Venus-based, Hellenistic) | sesquiquadrate | MC | 1°43.9' | separating |  |
| Saturn | conjunction | Saturn | 1°44.1' | applying |  |
| Lot Fortune | semisquare | True Node | 1°50.8' | separating |  |
| Saturn | semisextile | ASC | 1°50.9' | separating |  |
| Saturn | quincunx | DSC | 1°50.9' | separating |  |
| Neptune | sextile | Lot Marriage (Venus-based, Hellenistic) | 1°53.2' | separating |  |
| Saturn | trine | Mean Node | 1°54.0' | separating |  |
| ASC | opposition | Lot Marriage (Saturn-based) | 1°55.6' | separating |  |
| DSC | conjunction | Lot Marriage (Saturn-based) | 1°55.6' | separating |  |
| Sun | sesquiquadrate | Pluto | 1°57.6' | applying |  |
| Pluto | sextile | Neptune | 1°58.8' | applying |  |
| Lot Necessity | semisquare | Moon | 1°59.6' | applying |  |
| Moon | conjunction | Mean Lilith | 2°02.6' | separating |  |
| Jupiter | square | Sun | 2°02.9' | separating |  |
| Jupiter | quincunx | Mean Lilith | 2°03.8' | applying |  |
| Moon | trine | Sun | 2°04.1' | applying |  |
| DSC | quincunx | MC | 2°05.0' | separating |  |
| ASC | semisextile | MC | 2°05.0' | separating |  |
| ASC | quincunx | IC | 2°05.0' | separating |  |
| DSC | semisextile | IC | 2°05.0' | separating |  |
| Lot Marriage (Saturn-based) | trine | Uranus | 2°07.0' | separating |  |
| Uranus | conjunction | Uranus | 2°11.3' | separating |  |
| Lot Eros | quincunx | Moon | 2°13.4' | separating |  |
| Neptune | semisextile | Lot Fortune | 2°15.9' | separating |  |
| Mean Node | sextile | Neptune | 2°17.2' | separating |  |
| ASC | quincunx | Lot Spirit | 2°18.3' | separating |  |
| DSC | semisextile | Lot Spirit | 2°18.3' | separating |  |
| Chiron | trine | Lot Marriage (Saturn-based) | 2°19.0' | separating |  |
| True Node | semisextile | Venus | 2°19.7' | applying |  |
| Venus | opposition | Mercury | 2°20.1' | separating |  |
| Mars | square | Mars | 2°21.7' | separating |  |
| Mercury | quincunx | Uranus | 2°28.3' | applying |  |
| Chiron | square | MC | 2°28.4' | separating |  |
| Chiron | square | IC | 2°28.4' | separating |  |
| Lot Eros | quincunx | Lot Necessity | 2°30.8' | separating |  |
| Sun | trine | True Node | 2°32.1' | separating |  |
| Lot Spirit | conjunction | Moon | 2°35.8' | separating |  |
| Mars | sextile | Lot Spirit | 2°38.7' | applying |  |
| Lot Fortune | sextile | Pluto | 2°38.9' | separating |  |
| Lot Necessity | conjunction | Sun | 2°39.5' | separating |  |
| MC | square | True Node | 2°40.3' | separating |  |
| IC | square | True Node | 2°40.3' | separating |  |
| Chiron | quincunx | Lot Spirit | 2°41.7' | separating |  |
| Venus | semisextile | Chiron | 2°42.4' | applying |  |
| Saturn | square | Jupiter | 2°42.4' | applying |  |
| Sun | trine | Saturn | 2°43.6' | separating |  |
| Mean Node | conjunction | Lot Marriage (Venus-based, Hellenistic) | 2°49.4' | separating |  |
| MC | quincunx | Saturn | 2°51.8' | applying |  |
| IC | semisextile | Saturn | 2°51.8' | applying |  |
| Mars | conjunction | IC | 2°52.1' | applying |  |
| Mars | opposition | MC | 2°52.1' | applying |  |
| Lot Spirit | conjunction | Lot Necessity | 2°53.2' | separating |  |
| Sun | trine | Mean Node | 2°53.5' | separating |  |
| Venus | trine | Venus | 2°57.0' | separating |  |
| MC | square | Mean Node | 3°01.7' | separating |  |
| IC | square | Mean Node | 3°01.7' | separating |  |
| Mean Lilith | square | Sun | 3°05.8' | applying |  |
| Chiron | square | Jupiter | 3°05.9' | separating |  |
| Lot Fortune | square | Lot Fortune | 3°06.4' | separating |  |
| Lot Marriage (Venus-based, Hellenistic) | sextile | ASC | 3°08.5' | separating |  |
| Lot Marriage (Venus-based, Hellenistic) | trine | DSC | 3°08.5' | separating |  |
| Pluto | square | Mars | 3°13.9' | applying |  |
| Lot Marriage (Venus-based, Hellenistic) | trine | Venus | 3°14.7' | separating |  |
| Lot Necessity | square | Lot Eros | 3°19.0' | separating |  |
| Mercury | square | Chiron | 3°19.1' | applying |  |
| True Node | sextile | Chiron | 3°19.7' | applying |  |
| Lot Fortune | sextile | Lot Marriage (Venus-based, Hellenistic) | 3°29.0' | separating |  |
| Chiron | square | Mean Lilith | 3°45.0' | applying |  |
| Lot Marriage (Saturn-based) | square | Mercury | 3°46.3' | separating |  |
| IC | sextile | Moon | 3°46.6' | separating |  |
| MC | trine | Moon | 3°46.6' | separating |  |
| MC | trine | Jupiter | 3°50.1' | applying |  |
| IC | sextile | Jupiter | 3°50.1' | applying |  |
| Lot Marriage (Venus-based, Hellenistic) | sextile | Mercury | 3°51.6' | applying |  |
| Lot Marriage (Saturn-based) | square | Mars | 3°52.3' | applying |  |
| Chiron | sextile | Mean Node | 3°54.3' | applying |  |
| Jupiter | conjunction | Lot Eros | 3°55.5' | separating |  |
| Lot Necessity | sextile | Pluto | 3°56.8' | applying |  |
| Neptune | trine | Chiron | 3°57.6' | applying |  |
| Lot Fortune | trine | Neptune | 4°01.3' | applying |  |
| Lot Spirit | square | Saturn | 4°02.6' | applying |  |
| IC | sextile | Lot Necessity | 4°04.0' | separating |  |
| MC | trine | Lot Necessity | 4°04.0' | separating |  |
| Chiron | opposition | Saturn | 4°04.1' | separating |  |
| Mars | trine | Uranus | 4°07.0' | separating |  |
| True Node | sextile | Uranus | 4°10.4' | separating |  |
| Mean Lilith | square | ASC | 4°11.7' | applying |  |
| Mean Lilith | square | DSC | 4°11.7' | applying |  |
| Lot Eros | trine | True Node | 4°13.6' | separating |  |
| Chiron | sextile | True Node | 4°15.6' | applying |  |
| Mercury | square | Lot Spirit | 4°17.5' | separating |  |
| ASC | conjunction | Mean Node | 4°17.7' | applying |  |
| DSC | opposition | Mean Node | 4°17.7' | applying |  |
| Pluto | square | Mercury | 4°24.7' | separating |  |
| Lot Eros | trine | Saturn | 4°25.0' | applying |  |
| ASC | trine | Saturn | 4°27.5' | separating |  |
| DSC | sextile | Saturn | 4°27.5' | separating |  |
| Moon | opposition | Pluto | 4°32.2' | separating |  |
| Lot Eros | trine | Mean Node | 4°34.9' | separating |  |
| ASC | conjunction | True Node | 4°39.0' | applying |  |
| DSC | opposition | True Node | 4°39.0' | applying |  |
| Mercury | sextile | Lot Marriage (Saturn-based) | 4°40.1' | separating |  |
| Pluto | conjunction | Pluto | 4°41.4' | separating |  |
| Moon | opposition | Jupiter | 4°48.3' | applying |  |
| Neptune | conjunction | Uranus | 4°48.3' | separating |  |
| Mean Node | sextile | Chiron | 4°53.8' | separating |  |
| Saturn | square | Moon | 4°54.3' | separating |  |
| Mars | trine | Chiron | 4°57.8' | separating |  |
| Venus | conjunction | Mars | 5°18.5' | applying |  |
| Mars | trine | Sun | 5°42.1' | separating |  |
| Moon | square | Mars | 5°59.8' | separating |  |

### 2.1b Same grid grouped by A body

**A Sun**

| Aspect | B body | Orb | App/Sep | TIGHT |
|---|---|---|---|---|
| semisquare | Mars | 0°30.1' | applying | TIGHT |
| quincunx | ASC | 0°51.4' | applying | TIGHT |
| semisextile | DSC | 0°51.4' | applying | TIGHT |
| quintile | Chiron | 0°54.0' | applying | TIGHT |
| sesquiquadrate | Pluto | 1°57.6' | applying |  |
| trine | True Node | 2°32.1' | separating |  |
| trine | Saturn | 2°43.6' | separating |  |
| trine | Mean Node | 2°53.5' | separating |  |

**A Moon**

| Aspect | B body | Orb | App/Sep | TIGHT |
|---|---|---|---|---|
| semisextile | Lot Marriage (Saturn-based) | 0°36.6' | separating | TIGHT |
| opposition | MC | 0°46.0' | separating | TIGHT |
| conjunction | IC | 0°46.0' | separating | TIGHT |
| sextile | Lot Spirit | 0°59.3' | separating | TIGHT |
| conjunction | Mean Lilith | 2°02.6' | separating |  |
| trine | Sun | 2°04.1' | applying |  |
| opposition | Pluto | 4°32.2' | separating |  |
| opposition | Jupiter | 4°48.3' | applying |  |
| square | Mars | 5°59.8' | separating |  |

**A Mercury**

| Aspect | B body | Orb | App/Sep | TIGHT |
|---|---|---|---|---|
| sesquiquadrate | ASC | 0°21.6' | applying | TIGHT |
| semisquare | DSC | 0°21.6' | applying | TIGHT |
| biquintile | Lot Marriage (Venus-based, Hellenistic) | 0°36.6' | separating | TIGHT |
| sextile | Mars | 0°43.0' | separating | TIGHT |
| quincunx | Pluto | 0°44.5' | separating | TIGHT |
| biquintile | Sun | 1°20.9' | separating |  |
| trine | Lot Eros | 1°22.4' | separating |  |
| quincunx | Uranus | 2°28.3' | applying |  |
| square | Chiron | 3°19.1' | applying |  |
| square | Lot Spirit | 4°17.5' | separating |  |
| sextile | Lot Marriage (Saturn-based) | 4°40.1' | separating |  |

**A Venus**

| Aspect | B body | Orb | App/Sep | TIGHT |
|---|---|---|---|---|
| quincunx | Neptune | 0°05.8' | applying | TIGHT |
| square | Lot Marriage (Venus-based, Hellenistic) | 0°38.0' | applying | TIGHT |
| trine | Lot Fortune | 1°00.7' | applying |  |
| opposition | Mercury | 2°20.1' | separating |  |
| semisextile | Chiron | 2°42.4' | applying |  |
| trine | Venus | 2°57.0' | separating |  |
| conjunction | Mars | 5°18.5' | applying |  |

**A Mars**

| Aspect | B body | Orb | App/Sep | TIGHT |
|---|---|---|---|---|
| quincunx | Lot Eros | 0°16.3' | separating | TIGHT |
| opposition | Pluto | 0°54.2' | separating | TIGHT |
| quintile | DSC | 0°59.6' | applying | TIGHT |
| conjunction | Mean Lilith | 1°35.5' | applying |  |
| square | Mars | 2°21.7' | separating |  |
| sextile | Lot Spirit | 2°38.7' | applying |  |
| conjunction | IC | 2°52.1' | applying |  |
| opposition | MC | 2°52.1' | applying |  |
| trine | Uranus | 4°07.0' | separating |  |
| trine | Chiron | 4°57.8' | separating |  |
| trine | Sun | 5°42.1' | separating |  |

**A Jupiter**

| Aspect | B body | Orb | App/Sep | TIGHT |
|---|---|---|---|---|
| opposition | Lot Marriage (Saturn-based) | 0°37.8' | separating | TIGHT |
| semisquare | Venus | 0°43.6' | separating | TIGHT |
| semisextile | MC | 0°47.2' | separating | TIGHT |
| quincunx | IC | 0°47.2' | separating | TIGHT |
| quincunx | Lot Spirit | 1°00.5' | separating |  |
| square | Sun | 2°02.9' | separating |  |
| quincunx | Mean Lilith | 2°03.8' | applying |  |
| conjunction | Lot Eros | 3°55.5' | separating |  |

**A Saturn**

| Aspect | B body | Orb | App/Sep | TIGHT |
|---|---|---|---|---|
| semisquare | Uranus | 0°15.8' | applying | TIGHT |
| trine | True Node | 1°32.7' | separating |  |
| conjunction | Saturn | 1°44.1' | applying |  |
| semisextile | ASC | 1°50.9' | separating |  |
| quincunx | DSC | 1°50.9' | separating |  |
| trine | Mean Node | 1°54.0' | separating |  |
| square | Jupiter | 2°42.4' | applying |  |
| square | Moon | 4°54.3' | separating |  |

**A Uranus**

| Aspect | B body | Orb | App/Sep | TIGHT |
|---|---|---|---|---|
| semisquare | Jupiter | 0°15.3' | applying | TIGHT |
| semisextile | Lot Fortune | 0°21.2' | applying | TIGHT |
| semisquare | Saturn | 0°42.9' | separating | TIGHT |
| sextile | Lot Marriage (Venus-based, Hellenistic) | 0°43.8' | applying | TIGHT |
| conjunction | Neptune | 1°16.1' | applying |  |
| trine | Chiron | 1°20.5' | separating |  |
| conjunction | Uranus | 2°11.3' | separating |  |

**A Neptune**

| Aspect | B body | Orb | App/Sep | TIGHT |
|---|---|---|---|---|
| quintile | Mean Node | 0°10.1' | applying | TIGHT |
| quintile | Lot Spirit | 0°25.9' | applying | TIGHT |
| quintile | True Node | 0°31.5' | applying | TIGHT |
| biquintile | Mars | 0°33.6' | applying | TIGHT |
| semisextile | Mercury | 1°04.9' | separating |  |
| conjunction | Neptune | 1°21.0' | separating |  |
| semisextile | Venus | 1°41.8' | applying |  |
| sextile | Lot Marriage (Venus-based, Hellenistic) | 1°53.2' | separating |  |
| semisextile | Lot Fortune | 2°15.9' | separating |  |
| trine | Chiron | 3°57.6' | applying |  |
| conjunction | Uranus | 4°48.3' | separating |  |

**A Pluto**

| Aspect | B body | Orb | App/Sep | TIGHT |
|---|---|---|---|---|
| sextile | Chiron | 0°37.8' | applying | TIGHT |
| quintile | Sun | 0°42.2' | applying | TIGHT |
| semisextile | Lot Fortune | 1°03.9' | applying |  |
| conjunction | Lot Marriage (Venus-based, Hellenistic) | 1°26.5' | applying |  |
| sextile | Uranus | 1°28.6' | separating |  |
| sextile | Neptune | 1°58.8' | applying |  |
| square | Mars | 3°13.9' | applying |  |
| square | Mercury | 4°24.7' | separating |  |
| conjunction | Pluto | 4°41.4' | separating |  |

**A Chiron**

| Aspect | B body | Orb | App/Sep | TIGHT |
|---|---|---|---|---|
| quincunx | Sun | 0°21.7' | separating | TIGHT |
| trine | Lot Marriage (Saturn-based) | 2°19.0' | separating |  |
| square | MC | 2°28.4' | separating |  |
| square | IC | 2°28.4' | separating |  |
| quincunx | Lot Spirit | 2°41.7' | separating |  |
| square | Jupiter | 3°05.9' | separating |  |
| square | Mean Lilith | 3°45.0' | applying |  |
| sextile | Mean Node | 3°54.3' | applying |  |
| opposition | Saturn | 4°04.1' | separating |  |
| sextile | True Node | 4°15.6' | applying |  |

**A True Node**

| Aspect | B body | Orb | App/Sep | TIGHT |
|---|---|---|---|---|
| sextile | Neptune | 0°43.1' | separating | TIGHT |
| conjunction | Lot Marriage (Venus-based, Hellenistic) | 1°15.3' | separating |  |
| semisextile | Lot Fortune | 1°38.0' | separating |  |
| square | Mercury | 1°42.8' | separating |  |
| semisextile | Venus | 2°19.7' | applying |  |
| sextile | Chiron | 3°19.7' | applying |  |
| sextile | Uranus | 4°10.4' | separating |  |

**A Mean Node**

| Aspect | B body | Orb | App/Sep | TIGHT |
|---|---|---|---|---|
| square | Mercury | 0°08.8' | separating | TIGHT |
| semisextile | Venus | 0°45.6' | applying | TIGHT |
| sextile | Neptune | 2°17.2' | separating |  |
| conjunction | Lot Marriage (Venus-based, Hellenistic) | 2°49.4' | separating |  |
| sextile | Chiron | 4°53.8' | separating |  |

**A Mean Lilith**

| Aspect | B body | Orb | App/Sep | TIGHT |
|---|---|---|---|---|
| quincunx | Jupiter | 0°21.6' | applying | TIGHT |
| opposition | Mean Node | 0°26.9' | applying | TIGHT |
| sesquiquadrate | Lot Fortune | 0°27.4' | separating | TIGHT |
| sextile | Saturn | 0°36.7' | applying | TIGHT |
| opposition | True Node | 0°48.2' | applying | TIGHT |
| sesquiquadrate | Chiron | 1°14.3' | applying |  |
| biquintile | Moon | 1°15.1' | separating |  |
| square | Sun | 3°05.8' | applying |  |
| square | ASC | 4°11.7' | applying |  |
| square | DSC | 4°11.7' | applying |  |

**A ASC**

| Aspect | B body | Orb | App/Sep | TIGHT |
|---|---|---|---|---|
| semisquare | Venus | 0°34.2' | applying | TIGHT |
| square | Sun | 0°45.1' | separating | TIGHT |
| opposition | Lot Marriage (Saturn-based) | 1°55.6' | separating |  |
| semisextile | MC | 2°05.0' | separating |  |
| quincunx | IC | 2°05.0' | separating |  |
| quincunx | Lot Spirit | 2°18.3' | separating |  |
| conjunction | Mean Node | 4°17.7' | applying |  |
| trine | Saturn | 4°27.5' | separating |  |
| conjunction | True Node | 4°39.0' | applying |  |

**A MC**

| Aspect | B body | Orb | App/Sep | TIGHT |
|---|---|---|---|---|
| opposition | ASC | 0°43.2' | separating | TIGHT |
| conjunction | DSC | 0°43.2' | separating | TIGHT |
| quintile | Mean Lilith | 1°19.0' | separating |  |
| square | True Node | 2°40.3' | separating |  |
| quincunx | Saturn | 2°51.8' | applying |  |
| square | Mean Node | 3°01.7' | separating |  |
| trine | Moon | 3°46.6' | separating |  |
| trine | Jupiter | 3°50.1' | applying |  |
| trine | Lot Necessity | 4°04.0' | separating |  |

**A DSC**

| Aspect | B body | Orb | App/Sep | TIGHT |
|---|---|---|---|---|
| sesquiquadrate | Venus | 0°34.2' | applying | TIGHT |
| square | Sun | 0°45.1' | separating | TIGHT |
| conjunction | Lot Marriage (Saturn-based) | 1°55.6' | separating |  |
| quincunx | MC | 2°05.0' | separating |  |
| semisextile | IC | 2°05.0' | separating |  |
| semisextile | Lot Spirit | 2°18.3' | separating |  |
| opposition | Mean Node | 4°17.7' | applying |  |
| sextile | Saturn | 4°27.5' | separating |  |
| opposition | True Node | 4°39.0' | applying |  |

**A IC**

| Aspect | B body | Orb | App/Sep | TIGHT |
|---|---|---|---|---|
| conjunction | ASC | 0°43.2' | separating | TIGHT |
| opposition | DSC | 0°43.2' | separating | TIGHT |
| quintile | Pluto | 1°10.6' | applying |  |
| square | True Node | 2°40.3' | separating |  |
| semisextile | Saturn | 2°51.8' | applying |  |
| square | Mean Node | 3°01.7' | separating |  |
| sextile | Moon | 3°46.6' | separating |  |
| sextile | Jupiter | 3°50.1' | applying |  |
| sextile | Lot Necessity | 4°04.0' | separating |  |

**A Lot Fortune**

| Aspect | B body | Orb | App/Sep | TIGHT |
|---|---|---|---|---|
| quintile | Jupiter | 0°00.5' | applying | TIGHT |
| biquintile | Mercury | 0°27.2' | separating | TIGHT |
| trine | Uranus | 0°33.9' | applying | TIGHT |
| biquintile | Lot Marriage (Saturn-based) | 0°34.5' | separating | TIGHT |
| semisextile | Mars | 1°11.4' | applying |  |
| conjunction | Chiron | 1°24.7' | separating |  |
| sesquiquadrate | ASC | 1°32.7' | separating |  |
| semisquare | DSC | 1°32.7' | separating |  |
| semisquare | True Node | 1°50.8' | separating |  |
| sextile | Pluto | 2°38.9' | separating |  |
| square | Lot Fortune | 3°06.4' | separating |  |
| sextile | Lot Marriage (Venus-based, Hellenistic) | 3°29.0' | separating |  |
| trine | Neptune | 4°01.3' | applying |  |

**A Lot Spirit**

| Aspect | B body | Orb | App/Sep | TIGHT |
|---|---|---|---|---|
| sextile | ASC | 0°27.6' | separating | TIGHT |
| trine | DSC | 0°27.6' | separating | TIGHT |
| semisquare | Lot Eros | 1°16.5' | separating |  |
| conjunction | Moon | 2°35.8' | separating |  |
| conjunction | Lot Necessity | 2°53.2' | separating |  |
| square | Saturn | 4°02.6' | applying |  |

**A Lot Eros**

| Aspect | B body | Orb | App/Sep | TIGHT |
|---|---|---|---|---|
| biquintile | Mercury | 0°10.0' | applying | TIGHT |
| sesquiquadrate | Pluto | 0°16.2' | separating | TIGHT |
| biquintile | Jupiter | 0°36.7' | separating | TIGHT |
| quintile | Chiron | 0°47.4' | separating | TIGHT |
| quincunx | ASC | 0°50.0' | separating | TIGHT |
| semisextile | DSC | 0°50.0' | separating | TIGHT |
| semisquare | Mars | 1°11.4' | separating |  |
| quintile | Lot Marriage (Saturn-based) | 1°11.8' | separating |  |
| quincunx | Moon | 2°13.4' | separating |  |
| quincunx | Lot Necessity | 2°30.8' | separating |  |
| trine | True Node | 4°13.6' | separating |  |
| trine | Saturn | 4°25.0' | applying |  |
| trine | Mean Node | 4°34.9' | separating |  |

**A Lot Necessity**

| Aspect | B body | Orb | App/Sep | TIGHT |
|---|---|---|---|---|
| square | Lot Marriage (Saturn-based) | 0°01.3' | separating | TIGHT |
| sextile | MC | 0°10.6' | separating | TIGHT |
| trine | IC | 0°10.6' | separating | TIGHT |
| sextile | Lot Spirit | 0°23.9' | separating | TIGHT |
| semisquare | Venus | 1°20.1' | separating |  |
| trine | Mean Lilith | 1°27.2' | applying |  |
| semisquare | Lot Necessity | 1°42.2' | separating |  |
| semisquare | Moon | 1°59.6' | applying |  |
| conjunction | Sun | 2°39.5' | separating |  |
| square | Lot Eros | 3°19.0' | separating |  |
| sextile | Pluto | 3°56.8' | applying |  |

**A Lot Marriage (Venus-based, Hellenistic)**

| Aspect | B body | Orb | App/Sep | TIGHT |
|---|---|---|---|---|
| trine | Moon | 0°05.1' | applying | TIGHT |
| trine | Lot Necessity | 0°12.3' | separating | TIGHT |
| semisquare | Mean Lilith | 0°27.3' | separating | TIGHT |
| biquintile | Lot Marriage (Venus-based, Hellenistic) | 0°49.7' | separating | TIGHT |
| semisquare | IC | 1°43.9' | separating |  |
| sesquiquadrate | MC | 1°43.9' | separating |  |
| sextile | ASC | 3°08.5' | separating |  |
| trine | DSC | 3°08.5' | separating |  |
| trine | Venus | 3°14.7' | separating |  |
| sextile | Mercury | 3°51.6' | applying |  |

**A Lot Marriage (Saturn-based)**

| Aspect | B body | Orb | App/Sep | TIGHT |
|---|---|---|---|---|
| quincunx | Lot Fortune | 0°25.5' | separating | TIGHT |
| opposition | Lot Marriage (Venus-based, Hellenistic) | 0°48.1' | separating | TIGHT |
| trine | Chiron | 1°16.2' | applying |  |
| trine | Neptune | 1°20.4' | applying |  |
| trine | Uranus | 2°07.0' | separating |  |
| square | Mercury | 3°46.3' | separating |  |
| square | Mars | 3°52.3' | applying |  |

### 2.2 House overlays

**A's bodies in B's houses**

| Body | Longitude | Placidus house | WS house | Flag |
|---|---|---|---|---|
| Sun | Cancer 13 16 06 | 5 | 6 | FLAG |
| Moon | Gemini 04 45 56 | 4 | 5 | FLAG |
| Mercury | Gemini 29 29 09 | 5 | 5 | FLAG |
| Venus | Leo 23 27 42 | 7 | 7 | FLAG |
| Mars | Gemini 01 07 52 | 3 | 5 | FLAG |
| Jupiter | Scorpio 04 47 07 | 8 | 10 | FLAG |
| Saturn | Pisces 12 16 38 | 1 | 2 | FLAG |
| Uranus | Capricorn 24 49 34 | 12 | 12 | FLAG |
| Neptune | Capricorn 22 12 31 | 12 | 12 | FLAG |
| Pluto | Scorpio 25 32 16 | 9 | 10 | FLAG |
| Chiron | Virgo 06 28 20 | 7 | 8 | FLAG |
| True Node | Scorpio 22 50 24 | 9 | 10 | FLAG |
| Mean Node | Scorpio 21 16 19 | 9 | 10 | FLAG |
| Mean Lilith | Taurus 09 55 48 | 3 | 4 |  |
| ASC | Scorpio 06 04 56 | 8 | 10 | FLAG |
| MC | Leo 13 24 18 | 6 | 7 | FLAG |
| DSC | Taurus 06 04 56 | 2 | 4 |  |
| IC | Aquarius 13 24 18 | 12 | 1 | FLAG |

**B's bodies in A's houses**

| Body | Longitude | Placidus house | WS house | Flag |
|---|---|---|---|---|
| Sun | Aquarius 06 50 01 | 3 | 4 |  |
| Moon | Sagittarius 17 10 55 | 2 | 2 |  |
| Mercury | Aquarius 21 07 34 | 4 | 4 |  |
| Venus | Sagittarius 20 30 42 | 2 | 2 |  |
| Mars | Leo 28 46 10 | 10 | 10 | FLAG |
| Jupiter | Sagittarius 09 34 15 | 2 | 2 |  |
| Saturn | Pisces 10 32 29 | 4 | 5 | FLAG |
| Uranus | Capricorn 27 00 50 | 3 | 3 |  |
| Neptune | Capricorn 23 33 29 | 3 | 3 |  |
| Pluto | Sagittarius 00 13 42 | 1 | 2 | FLAG |
| Chiron | Virgo 26 10 05 | 11 | 11 |  |
| True Node | Scorpio 10 43 58 | 1 | 1 | FLAG |
| Mean Node | Scorpio 10 22 39 | 1 | 1 | FLAG |
| Mean Lilith | Gemini 02 43 20 | 7 | 8 | FLAG |
| ASC | Aquarius 14 07 31 | 4 | 4 |  |
| MC | Sagittarius 03 59 56 | 1 | 2 | FLAG |
| DSC | Leo 14 07 31 | 10 | 10 | FLAG |
| IC | Gemini 03 59 56 | 7 | 8 | FLAG |

### 2.3 Declination cross-aspects (orb 1°)

| A body | Type | B body | A decl | B decl | Orb (arcmin) |
|---|---|---|---|---|---|
| Moon | contraparallel | Venus | +20.04 | -20.03 | 0.7' |
| Mars | contraparallel | Venus | +20.01 | -20.03 | 0.9' |
| Neptune | parallel | MC | -20.99 | -20.95 | 2.8' |
| Mercury | parallel | Mean Lilith | +18.83 | +18.78 | 3.3' |
| True Node | parallel | Sun | -18.48 | -18.56 | 4.9' |
| Neptune | parallel | Jupiter | -20.99 | -21.13 | 7.9' |
| Neptune | parallel | Neptune | -20.99 | -20.84 | 9.1' |
| Mars | contraparallel | Moon | +20.01 | -19.84 | 10.4' |
| Moon | contraparallel | Moon | +20.04 | -19.84 | 12.0' |
| MC | contraparallel | ASC | +16.80 | -16.59 | 12.4' |
| Mean Lilith | parallel | Mars | +15.75 | +15.98 | 13.7' |
| Venus | contraparallel | True Node | +15.29 | -15.04 | 14.8' |
| Neptune | parallel | Uranus | -20.99 | -21.24 | 14.8' |
| Mercury | contraparallel | Sun | +18.83 | -18.56 | 16.3' |
| True Node | contraparallel | Mean Lilith | -18.48 | +18.78 | 17.9' |
| Venus | contraparallel | Mean Node | +15.29 | -14.93 | 21.4' |
| Uranus | parallel | Uranus | -21.68 | -21.24 | 26.2' |
| Mean Node | parallel | Sun | -18.08 | -18.56 | 29.1' |
| Uranus | parallel | Jupiter | -21.68 | -21.13 | 33.2' |
| Saturn | parallel | Saturn | -8.63 | -9.25 | 36.7' |
| Venus | parallel | Mars | +15.29 | +15.98 | 41.6' |
| Jupiter | parallel | Mercury | -12.01 | -12.71 | 42.1' |
| Mean Node | contraparallel | Mean Lilith | -18.08 | +18.78 | 42.1' |
| Mean Lilith | contraparallel | True Node | +15.75 | -15.04 | 42.6' |
| Uranus | parallel | MC | -21.68 | -20.95 | 43.8' |
| Moon | contraparallel | Neptune | +20.04 | -20.84 | 48.2' |
| MC | parallel | Mars | +16.80 | +15.98 | 48.9' |
| Mean Lilith | contraparallel | Mean Node | +15.75 | -14.93 | 49.3' |
| Mars | contraparallel | Neptune | +20.01 | -20.84 | 49.8' |
| Uranus | parallel | Neptune | -21.68 | -20.84 | 50.1' |
| Mean Lilith | contraparallel | ASC | +15.75 | -16.59 | 50.2' |
| ASC | parallel | Mercury | -13.55 | -12.71 | 50.3' |
| Moon | contraparallel | MC | +20.04 | -20.95 | 54.4' |
| Mars | contraparallel | MC | +20.01 | -20.95 | 56.0' |
| Neptune | parallel | Venus | -20.99 | -20.03 | 57.9' |

### 2.4 Antiscia / contra-antiscia contacts (orb 1°)

| A body | Type | B body | A point | B longitude | Orb |
|---|---|---|---|---|---|
| True Node | antiscion | Sun | Aquarius 07 09 36 | Aquarius 06 50 01 | 0°19.6' |
| Sun | contra-antiscion | Moon | Sagittarius 16 43 54 | Sagittarius 17 10 55 | 0°27.0' |

### 2.5 Cross-chart nodal-axis contacts (orb 5°)

| Body | Direction | Node point | Aspect | Orb |
|---|---|---|---|---|
| Mean Lilith | A body → B nodal axis | Mean Node (Scorpio 10 22 39) | opposition | 0°26.9' |
| Mean Lilith | A body → B nodal axis | True Node (Scorpio 10 43 58) | opposition | 0°48.2' |
| ASC | A body → B nodal axis | Mean Node (Scorpio 10 22 39) | conjunction | 4°17.7' |
| ASC | A body → B nodal axis | True Node (Scorpio 10 43 58) | conjunction | 4°39.0' |

### 2.6 Draconic synastry (orb 2°, major aspects)

**Draconic A → Natal B**

| A point | Aspect | B point | Orb | App/Sep |
|---|---|---|---|---|
| Pluto | sextile | Mean Lilith | 0°01.5' | separating |
| MC | conjunction | Venus | 0°03.2' | applying |
| IC | opposition | Venus | 0°03.2' | applying |
| Mean Lilith | square | Moon | 0°05.5' | separating |
| Mercury | square | Sun | 0°11.3' | separating |
| True Node | trine | Pluto | 0°13.7' | separating |
| IC | trine | Mercury | 0°33.7' | applying |
| MC | sextile | Mercury | 0°33.7' | applying |
| Neptune | square | Mars | 0°36.0' | separating |
| Sun | square | Mercury | 0°41.9' | applying |
| Uranus | conjunction | Mean Lilith | 0°44.2' | separating |
| Neptune | opposition | Pluto | 0°51.6' | separating |
| Jupiter | trine | True Node | 1°12.8' | separating |
| Mars | sextile | Jupiter | 1°16.8' | applying |
| Pluto | sextile | IC | 1°18.1' | separating |
| Pluto | trine | MC | 1°18.1' | separating |
| Jupiter | conjunction | Saturn | 1°24.2' | applying |
| Mean Node | sextile | Uranus | 1°25.1' | applying |
| Mars | trine | Sun | 1°27.5' | applying |
| Jupiter | trine | Mean Node | 1°34.1' | separating |
| Uranus | opposition | Pluto | 1°45.5' | applying |
| Mean Node | trine | Pluto | 1°47.8' | separating |
| Venus | trine | Mars | 1°51.1' | separating |

**Draconic A → Draconic B**

| A point | Aspect | B point | Orb | App/Sep |
|---|---|---|---|---|
| True Node | conjunction | True Node | 0°00.0' | separating |
| Saturn | square | Pluto | 0°03.5' | separating |
| True Node | trine | Saturn | 0°11.5' | applying |
| Mercury | opposition | Moon | 0°11.8' | applying |
| Neptune | sextile | Mean Node | 0°16.6' | applying |
| True Node | conjunction | Mean Node | 0°21.3' | separating |
| DSC | square | Neptune | 0°25.0' | applying |
| ASC | square | Neptune | 0°25.0' | applying |
| Neptune | sextile | Saturn | 0°26.4' | separating |
| Venus | square | True Node | 0°37.3' | separating |
| Neptune | sextile | True Node | 0°37.9' | applying |
| Pluto | square | ASC | 0°41.7' | separating |
| Pluto | square | DSC | 0°41.7' | separating |
| Mean Lilith | square | Uranus | 0°48.5' | separating |
| Jupiter | square | Neptune | 0°52.8' | separating |
| Moon | trine | Neptune | 0°54.0' | applying |
| Mean Lilith | trine | Mars | 0°56.8' | applying |
| Venus | square | Mean Node | 0°58.6' | separating |
| MC | trine | Pluto | 1°04.2' | applying |
| IC | sextile | Pluto | 1°04.2' | applying |
| Mean Node | conjunction | Mean Node | 1°12.8' | separating |
| Mean Node | trine | Saturn | 1°22.6' | separating |
| Saturn | opposition | Mars | 1°24.0' | separating |
| IC | trine | Mean Lilith | 1°25.5' | separating |
| MC | sextile | Mean Lilith | 1°25.5' | separating |
| Moon | square | Mercury | 1°31.9' | separating |
| Jupiter | trine | Mercury | 1°33.1' | separating |
| Mean Node | conjunction | True Node | 1°34.1' | applying |
| Venus | trine | Jupiter | 1°47.0' | separating |
| Uranus | sextile | True Node | 1°59.2' | separating |

### 2.7 Classical indicator checklist

| Indicator | Status | Detail |
|---|---|---|
| Sun–Moon (either direction) | PRESENT | A Moon trine B Sun 2°04.1' |
| Venus–Mars (either direction) | PRESENT | A Venus conjunction B Mars 5°18.5' |
| Moon–Moon | ABSENT | — |
| Venus–Saturn | ABSENT | — |
| Moon–Saturn | PRESENT | A Saturn square B Moon 4°54.3' |
| Sun–Saturn | PRESENT | A Sun trine B Saturn 2°43.6' |
| Ruler of A's 7th (Venus) touching any B body | PRESENT | A Venus opposition B Mercury 2°20.1'; A Venus trine B Venus 2°57.0'; A Venus conjunction B Mars 5°18.5'; A Venus quincunx B Neptune 0°05.8'; A Venus semisextile B Chiron 2°42.4'; A Venus trine B Lot Fortune 1°00.7'; A Venus square B Lot Marriage (Venus-based, Hellenistic) 0°38.0' |
| Ruler of B's 7th (Sun) touching any A body | PRESENT | A Moon trine B Sun 2°04.1'; A Mercury biquintile B Sun 1°20.9'; A Mars trine B Sun 5°42.1'; A Jupiter square B Sun 2°02.9'; A Pluto quintile B Sun 0°42.2'; A Chiron quincunx B Sun 0°21.7'; A Mean Lilith square B Sun 3°05.8'; A ASC square B Sun 0°45.1'; A DSC square B Sun 0°45.1'; A Lot Necessity conjunction B Sun 2°39.5' |
| Either ASC conjunct/opposite the other's luminaries or Venus | ABSENT | — |
| Either Moon in the other's 7th house | ABSENT | — |
| Mars–Saturn | ABSENT | — |
| Venus–Uranus | ABSENT | — |
| Moon–Neptune | ABSENT | — |
| Any outer planet conjunct the other's angles | ABSENT | — |

---

## PART 3: THE RELATIONSHIP CHARTS

### 3.1 Composite midpoint chart

Derivation method: planetary positions are **closest (shorter-arc) midpoints** of the two natal longitudes. The composite MC is the closest midpoint of the two natal MCs; the composite ASC is derived by converting that composite MC to its RAMC (using the obliquity of the ecliptic) and computing the Ascendant for **Skopje latitude 41.9973 N** from that RAMC. House cusps are Placidus from the same RAMC/latitude. This is the *midpoint-MC / derived-ASC* method, not the midpoint-of-Ascendants method.

Composite MC = Libra 08 42 07 (188.7020); RAMC = 187.9937°; obliquity = 23.438240°

**Composite positions**

| Body | Sign D M S | Longitude | Speed/day | Rx | Decl | House (P) | House (WS) |
|---|---|---|---|---|---|---|---|
| Sun | Aries 25 03 04 | 25.0510 | +0.9852 | D | +9.70 | 4 | 5 |
| Moon | Pisces 10 58 26 | 340.9738 | +13.2483 | D | -7.45 | 3 | 4 |
| Mercury | Aries 25 18 22 | 25.3060 | -0.1671 | R | +9.79 | 4 | 5 |
| Venus | Libra 21 59 12 | 201.9866 | +1.1171 | D | -8.56 | 10 | 11 |
| Mars | Cancer 14 57 01 | 104.9503 | +0.1985 | D | +22.60 | 7 | 8 |
| Jupiter | Scorpio 22 10 41 | 232.1780 | +0.0876 | D | -18.31 | 11 | 12 |
| Saturn | Pisces 11 24 33 | 341.4092 | +0.0444 | D | -7.29 | 3 | 4 |
| Uranus | Capricorn 25 55 12 | 295.9199 | +0.0097 | D | -20.96 | 2 | 2 |
| Neptune | Capricorn 22 53 00 | 292.8834 | +0.0053 | D | -21.50 | 2 | 2 |
| Pluto | Scorpio 27 52 59 | 237.8830 | +0.0023 | D | -19.69 | 12 | 12 |
| Chiron | Virgo 16 19 12 | 166.3201 | +0.0358 | D | +5.40 | 9 | 10 |
| True Node | Scorpio 16 47 11 | 226.7864 | -0.0549 | R | -16.85 | 11 | 12 |
| Mean Node | Scorpio 15 49 29 | 225.8248 | -0.0529 | R | -16.58 | 11 | 12 |
| Mean Lilith | Taurus 21 19 34 | 51.3261 | +0.1109 | D | +18.09 | 5 | 6 |
| ASC | Sagittarius 16 53 45 | 256.8959 | +0.0000 | D | -22.79 | 1 | 1 |
| MC | Libra 08 42 07 | 188.7020 | +0.0000 | D | -3.45 | 10 | 11 |
| DSC | Gemini 16 53 45 | 76.8959 | +0.0000 | D | +22.79 | 7 | 7 |
| IC | Aries 08 42 07 | 8.7020 | +0.0000 | D | +3.45 | 4 | 5 |

**Composite house cusps**

| House | Placidus | Long. | Whole sign |
|---|---|---|---|
| 1 | Sagittarius 16 53 45 | 256.8959 | Sagittarius 00 00 00 |
| 2 | Capricorn 22 17 28 | 292.2910 | Capricorn 00 00 00 |
| 3 | Pisces 02 51 12 | 332.8534 | Aquarius 00 00 00 |
| 4 | Aries 08 42 07 | 8.7020 | Pisces 00 00 00 |
| 5 | Taurus 06 07 43 | 36.1287 | Aries 00 00 00 |
| 6 | Taurus 27 45 09 | 57.7525 | Taurus 00 00 00 |
| 7 | Gemini 16 53 45 | 76.8959 | Gemini 00 00 00 |
| 8 | Cancer 22 17 28 | 112.2910 | Cancer 00 00 00 |
| 9 | Virgo 02 51 12 | 152.8534 | Leo 00 00 00 |
| 10 | Libra 08 42 07 | 188.7020 | Virgo 00 00 00 |
| 11 | Scorpio 06 07 43 | 216.1287 | Libra 00 00 00 |
| 12 | Scorpio 27 45 09 | 237.7525 | Scorpio 00 00 00 |

**Composite internal aspects (orb 5°)**

| Body 1 | Aspect | Body 2 | Orb |
|---|---|---|---|
| Sun | conjunction | Mercury | 0°15.3' |
| Moon | conjunction | Saturn | 0°26.1' |
| Chiron | sextile | True Node | 0°28.0' |
| Chiron | sextile | Mean Node | 0°29.7' |
| Chiron | square | DSC | 0°34.5' |
| Chiron | square | ASC | 0°34.5' |
| Mercury | square | Uranus | 0°36.8' |
| Jupiter | sextile | Neptune | 0°42.3' |
| Jupiter | opposition | Mean Lilith | 0°51.1' |
| Sun | square | Uranus | 0°52.1' |
| Mars | trine | Mean Node | 0°52.5' |
| Venus | square | Neptune | 0°53.8' |
| Mars | sextile | Chiron | 1°22.2' |
| Neptune | trine | Mean Lilith | 1°33.4' |
| Mars | trine | True Node | 1°50.2' |
| Uranus | sextile | Pluto | 1°57.8' |
| Sun | square | Neptune | 2°10.1' |
| Mercury | square | Neptune | 2°25.4' |
| Uranus | conjunction | Neptune | 3°02.2' |
| Sun | opposition | Venus | 3°03.9' |
| Mercury | opposition | Venus | 3°19.2' |
| Mars | trine | Saturn | 3°32.5' |
| Jupiter | sextile | Uranus | 3°44.5' |
| Venus | square | Uranus | 3°56.0' |
| Moon | trine | Mars | 3°58.6' |
| Saturn | trine | Mean Node | 4°24.9' |
| True Node | opposition | Mean Lilith | 4°32.4' |
| Uranus | trine | Mean Lilith | 4°35.6' |
| Moon | trine | Mean Node | 4°51.1' |
| Saturn | opposition | Chiron | 4°54.7' |
| Neptune | sextile | Pluto | 4°60.0' |

### 3.2 Davison relationship chart

- Time midpoint (JD UT): `2449641.895833`
- Davison moment UTC: **1994-10-16 09:29:59 UTC**
- Davison moment Europe/Skopje: **1994-10-16 10:29:59 CET** (offset 1:00:00)
- Great-circle midpoint of birthplaces: **lat 41.3838 N, lon 21.7609 E**

**Davison positions**

| Body | Sign D M S | Longitude | Speed/day | Rx | Decl | House (P) | House (WS) |
|---|---|---|---|---|---|---|---|
| Sun | Libra 22 47 36 | 202.7932 | +0.9915 | D | -8.86 | 10 | 11 |
| Moon | Pisces 17 56 34 | 347.9429 | +12.4413 | D | -0.71 | 3 | 4 |
| Mercury | Scorpio 03 07 49 | 213.1302 | -0.9465 | R | -15.00 | 10 | 12 |
| Venus | Scorpio 17 48 41 | 227.8113 | -0.1269 | R | -23.89 | 11 | 12 |
| Mars | Leo 06 27 25 | 126.4570 | +0.5340 | D | +19.85 | 8 | 9 |
| Jupiter | Scorpio 18 11 25 | 228.1904 | +0.2091 | D | -16.45 | 11 | 12 |
| Saturn | Pisces 06 10 04 | 336.1677 | -0.0396 | R | -11.07 | 3 | 4 |
| Uranus | Capricorn 22 28 33 | 292.4760 | +0.0122 | D | -22.07 | 1 | 2 |
| Neptune | Capricorn 20 37 34 | 290.6262 | +0.0076 | D | -21.28 | 1 | 2 |
| Pluto | Scorpio 26 37 51 | 236.6309 | +0.0345 | D | -6.36 | 11 | 12 |
| Chiron | Virgo 20 02 58 | 170.0496 | +0.1287 | D | -0.03 | 9 | 10 |
| True Node | Scorpio 14 55 55 | 224.9319 | -0.0611 | R | -16.32 | 11 | 12 |
| Mean Node | Scorpio 15 49 27 | 225.8243 | -0.0530 | R | -16.58 | 11 | 12 |
| Mean Lilith | Taurus 21 19 19 | 51.3219 | +0.1107 | D | +17.61 | 5 | 6 |
| ASC | Sagittarius 18 06 39 | 258.1110 | +0.0000 | D | -22.91 | 1 | 1 |
| MC | Libra 09 43 25 | 189.7236 | +0.0000 | D | -3.85 | 10 | 11 |
| DSC | Gemini 18 06 39 | 78.1110 | +0.0000 | D | +22.91 | 7 | 7 |
| IC | Aries 09 43 25 | 9.7236 | +0.0000 | D | +3.85 | 4 | 5 |

**Davison house cusps**

| House | Placidus | Long. | Whole sign |
|---|---|---|---|
| 1 | Sagittarius 18 06 39 | 258.1110 | Sagittarius 00 00 00 |
| 2 | Capricorn 23 37 25 | 293.6236 | Capricorn 00 00 00 |
| 3 | Pisces 04 03 39 | 334.0607 | Aquarius 00 00 00 |
| 4 | Aries 09 43 25 | 9.7236 | Pisces 00 00 00 |
| 5 | Taurus 07 05 12 | 37.0867 | Aries 00 00 00 |
| 6 | Taurus 28 46 27 | 58.7743 | Taurus 00 00 00 |
| 7 | Gemini 18 06 39 | 78.1110 | Gemini 00 00 00 |
| 8 | Cancer 23 37 25 | 113.6236 | Cancer 00 00 00 |
| 9 | Virgo 04 03 39 | 154.0607 | Leo 00 00 00 |
| 10 | Libra 09 43 25 | 189.7236 | Virgo 00 00 00 |
| 11 | Scorpio 07 05 12 | 217.0867 | Libra 00 00 00 |
| 12 | Scorpio 28 46 27 | 238.7743 | Scorpio 00 00 00 |

**Davison internal aspects (orb 5°)**

| Body 1 | Aspect | Body 2 | Orb |
|---|---|---|---|
| Moon | trine | Venus | 0°07.9' |
| Moon | square | ASC | 0°10.1' |
| Moon | square | DSC | 0°10.1' |
| Moon | trine | Jupiter | 0°14.9' |
| Sun | square | Uranus | 0°19.0' |
| Venus | conjunction | Jupiter | 0°22.7' |
| Neptune | trine | Chiron | 0°34.6' |
| Neptune | trine | Mean Lilith | 0°41.7' |
| Uranus | trine | Mean Lilith | 1°09.2' |
| Chiron | trine | Mean Lilith | 1°16.3' |
| Uranus | conjunction | Neptune | 1°51.0' |
| Jupiter | sextile | Chiron | 1°51.6' |
| Chiron | square | ASC | 1°56.3' |
| Chiron | square | DSC | 1°56.3' |
| Venus | conjunction | Mean Node | 1°59.2' |
| Moon | opposition | Chiron | 2°06.4' |
| Moon | trine | Mean Node | 2°07.1' |
| Sun | square | Neptune | 2°10.0' |
| Venus | sextile | Chiron | 2°14.3' |
| Jupiter | conjunction | Mean Node | 2°22.0' |
| Uranus | trine | Chiron | 2°25.6' |
| Jupiter | sextile | Neptune | 2°26.2' |
| Moon | sextile | Neptune | 2°41.0' |
| Venus | sextile | Neptune | 2°48.9' |
| Venus | conjunction | True Node | 2°52.8' |
| Moon | trine | True Node | 3°00.7' |
| Mercury | trine | Saturn | 3°02.2' |
| Jupiter | opposition | Mean Lilith | 3°07.9' |
| Jupiter | conjunction | True Node | 3°15.5' |
| Mars | sextile | MC | 3°16.0' |
| Mars | trine | IC | 3°16.0' |
| Mercury | square | Mars | 3°19.6' |
| Moon | sextile | Mean Lilith | 3°22.7' |
| Venus | opposition | Mean Lilith | 3°30.6' |
| Uranus | sextile | Pluto | 4°09.3' |
| Chiron | sextile | Mean Node | 4°13.5' |
| Jupiter | sextile | Uranus | 4°17.1' |
| Moon | sextile | Uranus | 4°32.0' |
| Venus | sextile | Uranus | 4°39.9' |
| Sun | trine | DSC | 4°40.9' |
| Sun | sextile | ASC | 4°40.9' |
| Neptune | sextile | Mean Node | 4°48.1' |

### 3.3 Composite vs Davison comparison

| Body | Composite sign | Davison sign | Sign agree | Comp house (P) | Dav house (P) | House agree (P) | Comp house (WS) | Dav house (WS) | House agree (WS) |
|---|---|---|---|---|---|---|---|---|---|
| Sun | Aries | Libra | DISAGREE | 4 | 10 | DISAGREE | 5 | 11 | DISAGREE |
| Moon | Pisces | Pisces | AGREE | 3 | 3 | AGREE | 4 | 4 | AGREE |
| Mercury | Aries | Scorpio | DISAGREE | 4 | 10 | DISAGREE | 5 | 12 | DISAGREE |
| Venus | Libra | Scorpio | DISAGREE | 10 | 11 | DISAGREE | 11 | 12 | DISAGREE |
| Mars | Cancer | Leo | DISAGREE | 7 | 8 | DISAGREE | 8 | 9 | DISAGREE |
| Jupiter | Scorpio | Scorpio | AGREE | 11 | 11 | AGREE | 12 | 12 | AGREE |
| Saturn | Pisces | Pisces | AGREE | 3 | 3 | AGREE | 4 | 4 | AGREE |
| Uranus | Capricorn | Capricorn | AGREE | 2 | 1 | DISAGREE | 2 | 2 | AGREE |
| Neptune | Capricorn | Capricorn | AGREE | 2 | 1 | DISAGREE | 2 | 2 | AGREE |
| Pluto | Scorpio | Scorpio | AGREE | 12 | 11 | DISAGREE | 12 | 12 | AGREE |
| Chiron | Virgo | Virgo | AGREE | 9 | 9 | AGREE | 10 | 10 | AGREE |
| True Node | Scorpio | Scorpio | AGREE | 11 | 11 | AGREE | 12 | 12 | AGREE |
| Mean Node | Scorpio | Scorpio | AGREE | 11 | 11 | AGREE | 12 | 12 | AGREE |
| Mean Lilith | Taurus | Taurus | AGREE | 5 | 5 | AGREE | 6 | 6 | AGREE |
| ASC | Sagittarius | Sagittarius | AGREE | 1 | 1 | AGREE | 1 | 1 | AGREE |
| MC | Libra | Libra | AGREE | 10 | 10 | AGREE | 11 | 11 | AGREE |
| DSC | Gemini | Gemini | AGREE | 7 | 7 | AGREE | 7 | 7 | AGREE |
| IC | Aries | Aries | AGREE | 4 | 4 | AGREE | 5 | 5 | AGREE |

---

## PART 4: TIMING (reference 30 August 2026, 12:00 Europe/Skopje)

Reference JD (UT): `2461282.916667` | UTC offset applied: `2:00:00` | UT: `2026-08-30 10:00:00+00:00`

### 4.1 Annual profection and Lord of the Year

| Subject | Age | Profected house (WS) | Sign | Lord of the Year | Year runs | Lord natal position | Natal house (P/WS) | Natal condition | Transiting position 30 Aug 2026 |
|---|---|---|---|---|---|---|---|---|---|
| A | 32 | 9 | Cancer | **Moon** | 2026-07-05 → 2027-07-05 | Gemini 04 45 56 (64.7656) | 8 / 8 | peregrine | Aries 04 04 33 (4.0759, +13.3078, D) |
| B | 31 | 8 | Virgo | **Mercury** | 2026-01-27 → 2027-01-27 | Aquarius 21 07 34 (321.1261) | 1 / 1 | peregrine | Virgo 09 41 41 (159.6946, +1.9141, D) |

### 4.2 Firdaria (Persian, 75-year cycle; sub-periods for the seven planets only)

**Subject A** — day sequence

| | Major lord | Minor lord | Start | End |
|---|---|---|---|---|
| previous | Mercury | Venus | 2023-08-26 | 2025-07-05 |
| **CURRENT** | Moon | Moon | 2025-07-05 | 2026-10-17 |
| next | Moon | Saturn | 2026-10-17 | 2028-01-30 |

- Current major lord: **Moon** (2025-07-05 → 2034-07-05)
- Current minor lord: **Moon** (2025-07-05 → 2026-10-17)
- Handover before: 2023-08-26 → 2025-07-05 (Mercury/Venus)
- Handover after: 2026-10-17 → 2028-01-30 (Moon/Saturn)

**Subject B** — day sequence

| | Major lord | Minor lord | Start | End |
|---|---|---|---|---|
| previous | Mercury | Venus | 2024-03-19 | 2026-01-26 |
| **CURRENT** | Moon | Moon | 2026-01-26 | 2027-05-11 |
| next | Moon | Saturn | 2027-05-11 | 2028-08-22 |

- Current major lord: **Moon** (2026-01-26 → 2035-01-26)
- Current minor lord: **Moon** (2026-01-26 → 2027-05-11)
- Handover before: 2024-03-19 → 2026-01-26 (Mercury/Venus)
- Handover after: 2027-05-11 → 2028-08-22 (Moon/Saturn)

### 4.3 Secondary progressions to 30 August 2026

Method: day-for-a-year (1 day of ephemeris time = 1 tropical year of 365.2422 days), chart cast for the birthplace at the progressed moment; ASC/MC from the progressed moment's own sidereal time.

| Subject | Elapsed yrs | Progressed JD | Prog Sun | Prog Moon | Prog Venus | Prog Mars | Prog ASC | Prog MC |
|---|---|---|---|---|---|---|---|---|
| A | 32.1537 | 2449571.18494 | Leo 13 58 34 | Leo 05 29 25 | Virgo 29 01 31 | Gemini 23 18 07 | Capricorn 20 48 09 | Scorpio 15 21 28 |
| B | 31.5904 | 2449776.35084 | Pisces 08 46 37 | Aquarius 18 05 42 | Capricorn 26 24 01 | Leo 17 06 10 | Libra 27 56 33 | Leo 03 23 25 |

**Progressed A → Natal B (orb 1.5°)**

| Progressed point | Aspect | Natal point | Orb | App/Sep | Perfects within 24 months |
|---|---|---|---|---|---|
| Moon | sesquiquadrate | Venus | 0°01.3' | separating | 2026-08-31 |
| Venus | sesquiquadrate | ASC | 0°06.0' | applying | 2026-10-03 |
| Venus | semisquare | DSC | 0°06.0' | applying | 2026-10-03 |
| Sun | conjunction | DSC | 0°08.9' | applying | 2026-10-26 |
| Sun | opposition | ASC | 0°08.9' | applying | 2026-10-26 |
| Venus | semisextile | Mars | 0°15.4' | separating | — |
| Mars | quincunx | Neptune | 0°15.4' | applying | 2027-01-17 |
| ASC | semisextile | Venus | 0°17.5' | separating | 2026-08-30 |
| ASC | semisextile | Mercury | 0°19.4' | separating | 2026-10-11 |
| MC | quintile | Uranus | 0°20.6' | separating | 2027-01-24 |
| Sun | quintile | Mean Lilith | 0°44.8' | applying | 2027-06-10 |
| Moon | biquintile | Saturn | 0°56.9' | separating | — |
| Venus | sextile | Pluto | 1°12.2' | applying | 2027-10-20 |
| MC | square | ASC | 1°14.0' | separating | 2027-02-27 |
| MC | square | DSC | 1°14.0' | separating | 2027-08-28 |
| Moon | opposition | Sun | 1°20.6' | applying | 2026-10-06 |
| Venus | quintile | Jupiter | 1°27.3' | separating | — |
| Mars | sesquiquadrate | Sun | 1°28.1' | separating | — |
| Moon | trine | MC | 1°29.5' | separating | — |
| Moon | sextile | IC | 1°29.5' | separating | — |

**Progressed B → Natal A (orb 1.5°)**

| Progressed point | Aspect | Natal point | Orb | App/Sep | Perfects within 24 months |
|---|---|---|---|---|---|
| Mars | quintile | Moon | 0°20.2' | applying | 2027-10-07 |
| ASC | sesquiquadrate | Saturn | 0°39.9' | separating | 2027-05-04 |
| ASC | biquintile | Moon | 0°49.4' | separating | 2026-08-31 |
| Venus | sextile | Pluto | 0°51.7' | separating | — |
| Venus | semisquare | Saturn | 0°52.6' | applying | 2027-05-31 |
| Sun | semisquare | Uranus | 1°02.9' | applying | 2027-09-15 |
| Sun | sextile | Mean Lilith | 1°09.2' | applying | 2027-10-23 |
| Moon | biquintile | Sun | 1°10.4' | applying | 2026-09-30 |
| MC | sextile | Moon | 1°22.5' | separating | 2026-08-31 |
| MC | square | Jupiter | 1°23.7' | separating | 2027-03-01 |

**Progressed A → Progressed B (orb 1.5°)**

| Prog A point | Aspect | Prog B point | Orb | App/Sep | Perfects within 24 months |
|---|---|---|---|---|---|
| A-prog MC | quintile | B-prog Venus | 0°57.5' | applying | 2027-01-24 |
| A-prog Venus | semisextile | B-prog ASC | 1°05.0' | separating | 2027-06-15 |

### 4.4 Outer-planet transits, 30 Aug 2026 – 31 Dec 2027

Aspects: conjunction, opposition, trine, square, sextile. Every retrograde pass listed separately. Station-in-orb tested at 1°.

| Transiting planet | Aspect | Target | Target position | Exact date | Station inside orb |
|---|---|---|---|---|---|
| Jupiter | conjunction | A MC | Leo 13 24 18 | 2026-08-30 | no |
| Jupiter | opposition | A IC | Aquarius 13 24 18 | 2026-08-30 | no |
| Jupiter | conjunction | B DSC | Leo 14 07 31 | 2026-09-03 | no |
| Jupiter | opposition | B ASC | Aquarius 14 07 31 | 2026-09-03 | no |
| Saturn | sextile | A IC | Aquarius 13 24 18 | 2026-09-05 | no |
| Saturn | opposition | Davison MC | Libra 09 43 25 | 2026-10-25 | no |
| Uranus | conjunction | A Moon | Gemini 04 45 56 | 2026-10-29 | YES — station 2026-09-10 at Gemini 05 41 49 (0.93° from exact) |
| Jupiter | trine | Composite Sun | Aries 25 03 04 | 2026-11-07 | no |
| Saturn | opposition | Composite MC | Libra 08 42 07 | 2026-11-11 | YES — station 2026-12-10 at Aries 07 55 52 (0.77° from exact) |
| Uranus | conjunction | B IC | Gemini 03 59 56 | 2026-11-18 | no |
| Uranus | opposition | B MC | Sagittarius 03 59 56 | 2026-11-18 | no |
| Pluto | sextile | B MC | Sagittarius 03 59 56 | 2026-12-19 | YES — station 2026-10-16 at Aquarius 03 04 07 (0.93° from exact) |
| Saturn | opposition | Composite MC | Libra 08 42 07 | 2027-01-09 | YES — station 2026-12-10 at Aries 07 55 52 (0.77° from exact) |
| Jupiter | trine | Composite Sun | Aries 25 03 04 | 2027-01-17 | no |
| Saturn | opposition | Davison MC | Libra 09 43 25 | 2027-01-25 | no |
| Pluto | square | A ASC | Scorpio 06 04 56 | 2027-02-26 | no |
| Saturn | sextile | A IC | Aquarius 13 24 18 | 2027-03-03 | no |
| Saturn | sextile | B ASC | Aquarius 14 07 31 | 2027-03-10 | YES — station 2026-07-26 at Aries 14 45 00 (0.62° from exact) |
| Neptune | trine | B MC | Sagittarius 03 59 56 | 2027-03-22 | no |
| Pluto | conjunction | B Sun | Aquarius 06 50 01 | 2027-03-30 | YES — station 2027-05-08 at Aquarius 07 10 41 (0.34° from exact) |
| Saturn | trine | Composite ASC | Sagittarius 16 53 45 | 2027-04-01 | no |
| Saturn | trine | B Moon | Sagittarius 17 10 55 | 2027-04-03 | no |
| Saturn | trine | Davison ASC | Sagittarius 18 06 39 | 2027-04-11 | no |
| Uranus | conjunction | B IC | Gemini 03 59 56 | 2027-04-26 | no |
| Uranus | opposition | B MC | Sagittarius 03 59 56 | 2027-04-26 | no |
| Uranus | conjunction | A Moon | Gemini 04 45 56 | 2027-05-10 | YES — station 2026-09-10 at Gemini 05 41 49 (0.93° from exact) |
| Saturn | opposition | Composite Venus | Libra 21 59 12 | 2027-05-12 | YES — station 2027-12-24 at Aries 21 01 14 (0.97° from exact) |
| Saturn | opposition | Davison Sun | Libra 22 47 36 | 2027-05-20 | no |
| Saturn | conjunction | Composite Sun | Aries 25 03 04 | 2027-06-11 | no |
| Uranus | trine | B Sun | Aquarius 06 50 01 | 2027-06-14 | YES — station 2028-02-12 at Gemini 05 55 52 (0.90° from exact) |
| Pluto | conjunction | B Sun | Aquarius 06 50 01 | 2027-06-17 | YES — station 2027-05-08 at Aquarius 07 10 41 (0.34° from exact) |
| Jupiter | trine | Composite Sun | Aries 25 03 04 | 2027-06-30 | no |
| Pluto | square | A ASC | Scorpio 06 04 56 | 2027-07-23 | no |
| Jupiter | square | B IC | Gemini 03 59 56 | 2027-08-14 | no |
| Jupiter | square | A Moon | Gemini 04 45 56 | 2027-08-17 | no |
| Jupiter | trine | A DSC | Taurus 06 04 56 | 2027-08-23 | no |
| Jupiter | opposition | Composite Moon | Pisces 10 58 26 | 2027-09-15 | no |
| Jupiter | sextile | A Sun | Cancer 13 16 06 | 2027-09-26 | no |
| Saturn | conjunction | Composite Sun | Aries 25 03 04 | 2027-10-09 | no |
| Jupiter | opposition | Davison Moon | Pisces 17 56 34 | 2027-10-19 | YES — station 2028-05-13 at Virgo 17 32 25 (0.40° from exact) |
| Saturn | opposition | Davison Sun | Libra 22 47 36 | 2027-11-08 | no |
| Saturn | opposition | Composite Venus | Libra 21 59 12 | 2027-11-20 | YES — station 2027-12-24 at Aries 21 01 14 (0.97° from exact) |
| Neptune | trine | B MC | Sagittarius 03 59 56 | 2027-11-22 | YES — station 2027-12-15 at Aries 03 51 09 (0.15° from exact) |
| Uranus | trine | B Sun | Aquarius 06 50 01 | 2027-12-27 | YES — station 2028-02-12 at Gemini 05 55 52 (0.90° from exact) |

### 4.5 New and full moons within 2° of a composite/Davison angle, luminary or Venus

| Phase | Date | Time (Europe/Skopje) | Sun degree | Moon degree | Target | Target position | Orb |
|---|---|---|---|---|---|---|---|
| New Moon | 2026-09-11 | 05:27:00 CEST | Virgo 18 25 54 | Virgo 18 25 54 | Davison Moon (opposite) | Pisces 17 56 34 | 0°29.3' |
| New Moon | 2026-11-09 | 08:02:07 CET | Scorpio 16 53 23 | Scorpio 16 53 23 | Davison Venus (conjunct) | Scorpio 17 48 41 | 0°55.3' |
| New Moon | 2026-12-09 | 01:51:51 CET | Sagittarius 16 56 48 | Sagittarius 16 56 48 | Composite ASC (conjunct) | Sagittarius 16 53 45 | 0°03.0' |
| New Moon | 2026-12-09 | 01:51:51 CET | Sagittarius 16 56 48 | Sagittarius 16 56 48 | Composite DSC (opposite) | Gemini 16 53 45 | 0°03.0' |
| New Moon | 2026-12-09 | 01:51:51 CET | Sagittarius 16 56 48 | Sagittarius 16 56 48 | Davison ASC (conjunct) | Sagittarius 18 06 39 | 1°09.9' |
| New Moon | 2026-12-09 | 01:51:51 CET | Sagittarius 16 56 48 | Sagittarius 16 56 48 | Davison DSC (opposite) | Gemini 18 06 39 | 1°09.9' |
| New Moon | 2027-03-08 | 10:29:29 CET | Pisces 17 34 48 | Pisces 17 34 48 | Davison Moon (conjunct) | Pisces 17 56 34 | 0°21.8' |
| New Moon | 2027-09-30 | 04:36:05 CEST | Libra 06 43 27 | Libra 06 43 27 | Composite MC (conjunct) | Libra 08 42 07 | 1°58.7' |
| New Moon | 2027-09-30 | 04:36:05 CEST | Libra 06 43 27 | Libra 06 43 27 | Composite IC (opposite) | Aries 08 42 07 | 1°58.7' |
| Full Moon | 2027-10-15 | 15:47:00 CEST | Libra 21 58 57 | Aries 21 58 57 | Composite Venus (conjunct) | Libra 21 59 12 | 0°00.2' |
| Full Moon | 2027-10-15 | 15:47:00 CEST | Libra 21 58 57 | Aries 21 58 57 | Davison Sun (conjunct) | Libra 22 47 36 | 0°48.6' |
