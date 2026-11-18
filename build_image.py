#!/usr/bin/env python3
"""Draw the 17 November 2026 world-news digest as a 1024x1024 PNG."""
from PIL import Image, ImageDraw, ImageFont
import math, os, sys

W = H = 1024
FONT_DIR = "C:/Windows/Fonts"
REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")
BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
COND = os.path.join(FONT_DIR, "DejaVuSansCondensed.ttf")
COND_BOLD = os.path.join(FONT_DIR, "DejaVuSansCondensed-Bold.ttf")

BG = (9, 20, 34)
OCEAN = (11, 26, 44)
LAND = (188, 203, 218)
CARD = (16, 36, 58)
PANEL = (14, 31, 51)
WHITE = (245, 249, 252)
MUTED = (158, 174, 190)
DIM = (112, 130, 148)
ACCENT = (255, 176, 32)
INK = (12, 24, 38)
RULE = (44, 64, 86)

_font_cache = {}
def F(path, size):
    key = (path, size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(path, size)
    return _font_cache[key]

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)
boxes = []

def register(x0, y0, x1, y1, label):
    if x0 < 0 or y0 < 0 or x1 > W or y1 > H:
        raise SystemExit("OUT OF BOUNDS: %s (%s,%s,%s,%s)" % (label, x0, y0, x1, y1))
    for (a0, b0, a1, b1, lab) in boxes:
        if x0 < a1 and a0 < x1 and y0 < b1 and b0 < y1:
            raise SystemExit("OVERLAP: %s with %s (%s,%s,%s,%s)" % (label, lab, x0, y0, x1, y1))
    boxes.append((x0, y0, x1, y1, label))

def T(xy, s, font, fill, anchor="la", label=None, check=True, pad=0):
    bb = d.textbbox(xy, s, font=font, anchor=anchor)
    if check:
        register(bb[0] - pad, bb[1] - pad, bb[2] + pad, bb[3] + pad, label or s)
    d.text(xy, s, font=font, fill=fill, anchor=anchor)
    return bb

def TW(s, font):
    return d.textbbox((0, 0), s, font=font)[2]

# ---------------------------------------------------------------- header
d.rectangle([24, 30, 30, 102], fill=ACCENT)
T((44, 4), "THE WORLD ON TUESDAY", F(BOLD, 25), WHITE, label="kicker")
T((40, 32), "17 NOVEMBER 2026", F(COND_BOLD, 72), WHITE, label="date")
T((998, 10), "A ONE-IMAGE DIGEST", F(BOLD, 16), ACCENT, anchor="ra", label="digest")
T((998, 74), "8 HEADLINES \u00b7 27 BRIEFS", F(REG, 16), MUTED, anchor="ra", label="counts")
d.rectangle([24, 120, 1000, 121], fill=RULE)

# ---------------------------------------------------------------- map
MX0, MX1, MY0, MY1 = 26, 998, 126, 408
LAT_TOP, LAT_BOT = 78.0, -58.0

def P(lon, lat):
    x = MX0 + (lon + 180.0) / 360.0 * (MX1 - MX0)
    y = MY0 + (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * (MY1 - MY0)
    return x, y

POLYS = [
    # North America
    [(-168,65),(-166,71),(-156,71),(-140,70),(-128,70),(-115,69),(-100,69),(-88,70),(-80,68),(-72,63),(-64,60),(-56,52),(-60,47),(-67,45),(-70,41),(-75,36),(-81,31),(-80,25),(-83,25),(-85,30),(-89,29),(-94,29),(-97,26),(-105,22),(-110,24),(-114,28),(-117,33),(-122,37),(-125,42),(-124,48),(-130,54),(-140,60),(-150,60),(-160,56),(-165,60)],
    [(-110,24),(-114,28),(-115,31),(-112,29),(-108,26),(-110,24)],          # Baja
    [(-82,25),(-80,25),(-80,31),(-83,30),(-82,25)],                          # Florida
    [(-92,18),(-88,16),(-84,10),(-78,8),(-77,10),(-82,15),(-87,18),(-92,18)],# Central America
    [(-85,22),(-77,20),(-74,20),(-80,23),(-85,22)],                          # Cuba
    [(-74,19),(-68,19),(-68,18),(-74,18),(-74,19)],                          # Hispaniola
    [(-45,60),(-25,70),(-20,78),(-30,82),(-50,83),(-58,78),(-55,68),(-50,62),(-45,60)], # Greenland
    # South America
    [(-80,10),(-75,12),(-70,12),(-62,10),(-52,5),(-44,0),(-35,-5),(-38,-15),(-47,-24),(-58,-34),(-62,-40),(-65,-48),(-70,-54),(-74,-50),(-72,-40),(-70,-30),(-76,-15),(-80,-5),(-80,3),(-80,10)],
    # Africa
    [(-17,15),(-12,28),(-5,35),(5,36),(15,36),(25,32),(32,31),(35,25),(40,15),(43,11),(51,12),(48,2),(42,-10),(40,-20),(35,-25),(30,-33),(20,-35),(15,-30),(12,-15),(8,5),(0,5),(-8,5),(-12,10),(-17,15)],
    [(43,-13),(49,-15),(50,-22),(47,-25),(44,-22),(43,-17),(43,-13)],          # Madagascar
    # Europe
    [(-10,37),(-9,43),(-5,48),(-1,49),(2,51),(4,53),(7,54),(8,57),(10,58),(8,62),(12,66),(18,70),(25,71),(30,70),(30,60),(28,56),(24,50),(20,45),(18,40),(15,39),(12,45),(8,44),(3,42),(-2,37),(-10,37)],
    [(12,45),(13,42),(15,40),(16,38),(15,37),(13,41),(10,44),(12,45)],         # Italy
    [(-5,50),(-3,53),(-5,58),(-3,59),(-1,54),(1,51),(-5,50)],                  # Britain
    [(-10,52),(-6,53),(-6,55),(-9,55),(-10,52)],                               # Ireland
    [(-24,64),(-14,66),(-14,64),(-22,63),(-24,64)],                            # Iceland
    # Asia
    [(30,70),(45,70),(60,72),(80,74),(100,76),(120,74),(140,73),(160,70),(170,68),(180,66),(180,60),(170,60),(160,59),(155,52),(145,48),(140,45),(135,42),(130,42),(128,38),(122,40),(120,36),(122,31),(121,25),(110,21),(108,10),(105,8),(100,5),(98,10),(95,16),(92,21),(88,22),(85,20),(80,13),(77,8),(74,15),(70,22),(66,25),(60,25),(57,25),(55,27),(50,30),(48,30),(45,38),(42,42),(40,42),(35,42),(30,41),(30,70)],
    [(38,30),(43,30),(48,30),(56,26),(59,22),(55,17),(48,13),(43,12),(38,22),(38,30)], # Arabia
    [(97,20),(105,20),(110,20),(110,10),(105,5),(100,5),(98,10),(97,20)],       # SE Asia mainland
    [(95,5),(105,-6),(115,-8),(130,-8),(140,-8),(150,-9),(140,-2),(130,0),(120,2),(110,3),(100,5),(95,5)], # Indonesia
    [(120,18),(124,18),(126,12),(126,7),(122,6),(120,12),(120,18)],            # Philippines
    [(130,31),(136,35),(141,37),(143,42),(145,44),(142,45),(138,37),(132,33),(130,31)], # Japan
    [(80,8),(82,7),(81,9),(80,10),(80,8)],                                     # Sri Lanka
    # Oceania
    [(113,-22),(114,-34),(121,-34),(129,-32),(138,-35),(147,-38),(150,-35),(153,-28),(153,-25),(146,-19),(142,-11),(136,-12),(130,-11),(125,-14),(122,-18),(113,-22)],
    [(172,-34),(178,-38),(175,-41),(170,-45),(166,-46),(170,-42),(173,-38),(172,-34)],
]
# faint graticule
for lat in (60, 30, 0, -30):
    _, yy = P(-180, lat)
    d.line([(MX0, yy), (MX1, yy)], fill=(20, 43, 68), width=1)
for lon in (-120, -60, 0, 60, 120):
    xx, _ = P(lon, 0)
    d.line([(xx, MY0), (xx, MY1)], fill=(20, 43, 68), width=1)
for poly in POLYS:
    d.polygon([P(lon, lat) for lon, lat in poly], fill=LAND)
# inland seas
for (lon, lat, rx, ry) in [(34,43,7.5,2.6),(51,42,2.4,4.6),(-84,45,2.2,1.4),(-82,43,1.8,1.3),(-88,45,1.4,0.9)]:
    x0, y0 = P(lon-rx, lat+ry)
    x1, y1 = P(lon+rx, lat-ry)
    d.ellipse([x0, y0, x1, y1], fill=OCEAN)
d.rectangle([MX0-1, MY0-1, MX1+1, MY1+1], outline=RULE, width=1)

# news: (num, lat, lon, headline?, preferred-angle)
NEWS = [
    (1, 45.3, 36.5, True, 300),   # Kerch
    (2, 26.0, 50.6, True, 200),   # Bahrain
    (3, -3.0, 23.0, True, 240),   # DR Congo
    (4, 22.0, -101.0, True, 220), # Mexico / PAHO
    (5, 14.6, 121.0, True, 90),   # Manila
    (6, 37.4, -122.0, True, 180), # Nvidia / Santa Clara
    (7, 40.7, -74.0, True, 60),   # New York
    (8, -21.0, -159.8, True, 90), # Cook Islands
    (9, 52.1, 4.3, False, 180),   # Hague
    (10, 55.4, 86.0, False, 280), # Kemerovo
    (11, 44.8, 20.5, False, 200), # Belgrade
    (12, 43.0, 28.0, False, 150), # Bulgaria Black Sea
    (13, 56.9, 24.6, False, 300), # Latvia
    (14, 51.5, -0.1, False, 220), # UK
    (15, 59.9, 10.7, False, 330), # Norway
    (16, 31.4, 34.4, False, 240), # Gaza
    (17, 26.2, 56.3, False, 120), # Musandam
    (18, 36.9, 30.7, False, 140), # Antalya
    (19, 47.9, 106.9, False, 280),# Mongolia
    (20, 33.6, 130.4, False, 90), # Fukuoka
    (21, 13.8, 100.5, False, 200),# Bangkok
    (22, 21.0, 78.0, False, 230), # India
    (23, 38.9, -77.0, False, 60), # Washington
    (24, 38.9, -77.0, False, 300),# Washington retail
    (25, 22.5, 114.1, False, 120),# Shenzhen
    (26, -12.0, -77.0, False, 200),# Peru
    (27, -15.8, -47.9, False, 90),# Brasilia
    (28, 15.5, 30.0, False, 240), # Sudan
    (29, -25.9, 32.6, False, 130),# Mozambique
    (30, 46.2, 6.1, False, 170),  # Geneva
    (31, 29.0, 48.0, False, 90),  # Brent / Gulf pricing
    (32, 37.8, -122.3, False, 240),# Anthropic / SF
    (33, 50.9, 4.5, False, 320),  # EU Commission / Brussels
    (34, -33.9, 151.2, False, 100),# RBA / Sydney
    (35, 47.5, 19.0, False, 20),  # Hungary / Budapest
]
placed = []
def place_label(x, y, radius, preferred, label, color=DIM, lw=1):
    offs = [0, 15, -15, 30, -30, 45, -45, 60, -60, 75, -75, 90, -90, 105, -105, 120, -120, 135, -135, 150, -150, 180]
    for r in (16, 23, 32, 43, 56, 71, 88, 107, 128):
        for off in offs:
            a = math.radians(preferred + off)
            cx = x + math.cos(a) * r
            cy = y + math.sin(a) * r
            if cx - radius - 3 < MX0 or cx + radius + 3 > MX1 or cy - radius - 3 < MY0 or cy + radius + 3 > MY1:
                continue
            ok = True
            for (px, py, pr) in placed:
                if math.hypot(cx - px, cy - py) < radius + pr + 3:
                    ok = False
                    break
            if not ok:
                continue
            placed.append((cx, cy, radius))
            dx, dy = cx - x, cy - y
            dist = math.hypot(dx, dy)
            if dist > radius + 4:
                ux, uy = dx / dist, dy / dist
                lx, ly = x + ux * 4, y + uy * 4
                ex, ey = cx - ux * (radius + 1), cy - uy * (radius + 1)
                d.line([(lx, ly), (ex, ey)], fill=color, width=lw)
            return cx, cy
    raise SystemExit("NO ROOM FOR LABEL %s" % label)

for (num, lat, lon, head, ang) in NEWS:
    x, y = P(lon, lat)
    r = 12 if head else 10
    cx, cy = place_label(x, y, r, ang, num, ACCENT if head else DIM, 2 if head else 1)
    if head:
        d.line([(x - 4, y), (x + 4, y)], fill=ACCENT, width=2)
        d.line([(x, y - 4), (x, y + 4)], fill=ACCENT, width=2)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ACCENT, outline=WHITE, width=1)
        T((cx, cy - 1), str(num), F(BOLD, 17), INK, anchor="mm", label="map%d" % num)
    else:
        d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=WHITE)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BG, outline=ACCENT, width=1)
        T((cx, cy - 1), str(num), F(BOLD, 13), WHITE, anchor="mm", label="map%d" % num)

d.rectangle([24, 410, 1000, 411], fill=RULE)

# ---------------------------------------------------------------- headlines
HEAD = [
    ("Kerch bridge hit", "road span down; Kremlin vow", "KERCH", 1),
    ("Gulf drone exchange", "Bahrain/US: intercepted; US hit Qeshm; Kuwait: intercepting", "3", 2),
    ("Ebola: 11,000+", "cases; deaths; WHO; >2x in 3 mo", "5,400", 3),
    ("Measles elimination lost", "US, Mexico, Bolivia; PAHO", "3", 4),
    ("Indo-Pacific watch", "surveillance initiative; Manila", "QUAD", 5),
    ("Nvidia doubles", "revenue; after US close", "$115.8B", 6),
    ("STOXX selloff", "Dow -1.6%; S&P -1.0%; Nasdaq -0.7%", "-1.75%", 7),
    ("Cyclone Xavier Cat 5", "Cook Islands; km/h gusts", "315", 8),
]

def icon(n, x, y, s=18):
    c = ACCENT
    if n == 1:  # broken bridge
        d.line([(x, y+s-4), (x+s*0.35, y+s-4)], fill=c, width=2)
        d.line([(x+s*0.55, y+s-4), (x+s, y+s-4)], fill=c, width=2)
        d.line([(x+3, y+s-4), (x+3, y+4)], fill=c, width=2)
        d.line([(x+s-3, y+s-4), (x+s-3, y+4)], fill=c, width=2)
        d.line([(x+3, y+4), (x+s*0.35, y+8)], fill=c, width=2)
        d.line([(x+s-3, y+4), (x+s*0.55, y+8)], fill=c, width=2)
    elif n == 2:  # drone / radar
        d.polygon([(x+2, y+s-3),(x+s-2, y+s-3),(x+5, y+7),(x+2, y+s-3)], outline=c)
        d.arc([x+s-4, y+2, x+s+12, y+s-2], 180, 300, fill=c, width=1)
    elif n == 3:  # virus
        d.ellipse([x+3, y+3, x+s-3, y+s-3], outline=c, width=2)
        for a in range(0, 360, 45):
            ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
            d.line([(x+s/2 + ca*(s/2-1), y+s/2 + sa*(s/2-1)),
                    (x+s/2 + ca*(s/2+2), y+s/2 + sa*(s/2+2))], fill=c, width=1)
    elif n == 4:  # shield with slash
        d.polygon([(x+2, y+3),(x+s-2, y+3),(x+s-4, y+s-2),(x+s/2, y+s+2),(x+4, y+s-2)], outline=c)
        d.line([(x+3, y+s-2), (x+s-2, y+3)], fill=c, width=2)
    elif n == 5:  # ship + radar arc
        d.line([(x+2, y+s-5),(x+s-2, y+s-5),(x+s-5, y+s-1),(x+5, y+s-1),(x+2, y+s-5)], fill=c, width=1)
        d.arc([x+2, y-2, x+s-2, y+s-6], 200, 340, fill=c, width=2)
    elif n == 6:  # chip
        d.rectangle([x+4, y+4, x+s-4, y+s-4], outline=c, width=2)
        for i in range(3):
            d.line([(x+2, y+6+i*4), (x+4, y+6+i*4)], fill=c, width=1)
            d.line([(x+s-4, y+6+i*4), (x+s-2, y+6+i*4)], fill=c, width=1)
    elif n == 7:  # falling chart
        d.line([(x+2, y+4), (x+7, y+8), (x+11, y+7), (x+s-1, y+s-2)], fill=c, width=2)
        d.line([(x+s-6, y+s-2), (x+s-1, y+s-2), (x+s-1, y+s-7)], fill=c, width=2)
    elif n == 8:  # cyclone
        pts = []
        for i in range(50):
            t = i / 49.0 * 4.2 * math.pi
            rr = 1 + t * 1.7
            pts.append((x+s/2 + math.cos(t)*rr, y+s/2 + math.sin(t)*rr))
        d.line(pts, fill=c, width=2)

for i, (title, sub, key, num) in enumerate(HEAD):
    row, col = divmod(i, 2)
    x = 24 + col * 494
    y = 420 + row * 76
    d.rounded_rectangle([x, y, x+482, y+68], radius=7, fill=CARD)
    d.rectangle([x, y, x+4, y+68], fill=ACCENT)
    d.ellipse([x+12, y+20, x+38, y+46], fill=ACCENT)
    T((x+25, y+32), str(num), F(BOLD, 15), INK, anchor="mm", label="hnum%d" % num)
    kw = TW(key, F(COND_BOLD, 40))
    if kw > 170:
        raise SystemExit("KEY TOO WIDE (%d): %s" % (kw, key))
    avail = 412 - kw
    lines = title.split("\n")
    for li, line in enumerate(lines):
        tw = TW(line, F(COND_BOLD, 30))
        if tw > avail:
            raise SystemExit("TITLE TOO WIDE (%d>%d): %s" % (tw, avail, line))
        ty = y + (2 if len(lines) > 1 else 3) + li * 31
        if len(lines) == 1:
            ty = y + 3
        T((x+46, ty), line, F(COND_BOLD, 30), WHITE, label="title%d_%d" % (num, li))
    if sub:
        cap_size = 14 if num == 2 else (15 if num == 7 else 16)
        cap_font = F(COND, cap_size)
        sw = TW(sub, cap_font)
        if sw > avail:
            raise SystemExit("SUB TOO WIDE (%d>%d): %s" % (sw, avail, sub))
        T((x+46, y+40 if num == 2 else y+39), sub, cap_font, MUTED, label="sub%d" % num)
    icon(num, x+9, y+47, 16)
    T((x+464, y+16), key, F(COND_BOLD, 40), ACCENT, anchor="ra", label="key%d" % num)

# ---------------------------------------------------------------- briefs
BRIEFS = [
    ("EUROPE", [
        (9, ["Thaci +17 months", "Hague: obstruction"]),
        (10, ["An-12: 19 dead", "technical fault"]),
        (11, ["MiG-29 crash", "Serbia; pilot dead"]),
        (12, ["LPG tanker sinks", "2nd ship in 2 days"]),
        (13, ["Latvia PM approved", "57-34; Kulbergs"]),
        (15, ["Norway 3-2", "Denmark; Haaland", "penalty"]),
    ]),
    ("MIDDLE EAST", [
        (14, ["UK sanctions 8", "Israeli firms", "Saar: hostile act"]),
        (16, ["Gaza: 4+ killed", "health officials:", "Israeli fire; child", "age 6"]),
        (17, ["Oman: 24 crew out", "burning tanker"]),
        (18, ["COP31: Hoekstra", "needs significant", "change"]),
    ]),
    ("ASIA-PACIFIC", [
        (19, ["Mongolia president", "Khurelsukh to quit", "$25m; he denies"]),
        (20, ["Japan: suspected", "air breach; jets", "Fukuoka, Russia"]),
        (21, ["US-Thailand", "trade: substantial", "conclusion"]),
        (22, ["India 2-1 Pakistan", "SAFF champions"]),
    ]),
    ("AMERICAS", [
        (23, ["Court blocks", "trans discharges", "Pentagon"]),
        (24, ["US retail +0.2%", "October"]),
        (25, ["Canada-China deal", "~C$400m tariff cut"]),
        (26, ["Peru: China pledge", "$22.5m El Nino"]),
        (27, ["Brazil fiscal vote", "delayed to Wed."]),
    ]),
    ("AFRICA", [
        (28, ["UN: 1,630+ killed", "civilians by drones", "Jan-Oct"]),
        (29, ["Mozambique trial", "opposition leader", "Mondlane denies"]),
        (30, ["UN Turk: 5 EU", "Rwanda hub worry"]),
    ]),
    ("MARKETS", [
        (31, ["Brent settles", "$93.14"]),
        (32, ["Anthropic $70-78", "IPO; Nasdaq ANT"]),
        (33, ["EU: euro area", "2026 growth 1.2%", "forecast"]),
        (34, ["RBA: 6 of 9 back", "hike to 4.85%"]),
        (35, ["Hungary 5.50%", "rate held", "central bank"]),
    ]),
]
COLX = [14, 182, 350, 518, 686, 854]
COLW = 164
for ci, (heading, items) in enumerate(BRIEFS):
    x = COLX[ci]
    T((x, 718), heading, F(BOLD, 16), ACCENT, label="col%d" % ci)
    d.line([(x, 738), (x + COLW, 738)], fill=RULE, width=1)
    y = 742
    for num, lines in items:
        T((x, y), str(num), F(BOLD, 13), ACCENT, label="bn%d" % num)
        block = []
        for li, line in enumerate(lines):
            f = F(COND, 16)
            if TW(line, f) > COLW - 18:
                raise SystemExit("BRIEF TOO WIDE (%d): %s" % (TW(line, f), line))
            T((x + 20, y), line, f, WHITE if li == 0 else MUTED, label="b%d_%d" % (num, li))
            block.append((x, y, x + 20 + TW(line, f), y + 19))
            y += 20
    if y > 1004:
        raise SystemExit("COLUMN OVERFLOW %s at %d" % (heading, y))

T((24, 1004), "Sources: Reuters, AP, AFP, BBC, WHO, UN, Al Jazeera, DW, Kyodo, Xinhua, CNBC, RNZ",
  F(REG, 14), DIM, label="sources")

# ---------------------------------------------------------------- save
os.makedirs("out", exist_ok=True)
img.save("out/entry_full.png", "PNG", optimize=True)
pal = img.convert("P", palette=Image.Palette.ADAPTIVE, colors=96)
pal.save("out/entry.png", "PNG", optimize=True)
print("canvas ok, boxes:", len(boxes))
print("png bytes:", os.path.getsize("out/entry.png"))
