#!/usr/bin/env python3
"""Render entry.png for news-image-20261124: the world news of Tuesday
24 November 2026 in one 1024x1024 image. Data: stories.json (same dir).
Design: teal / coral / paper, huge date top-left, coral story-count block,
wide hero panel, 12 story panels, dark dotted world map with numbered pins,
'AlSO TODAY' ticker and a sources footer. Rendered at 2x and downscaled."""

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
DATA = json.loads((HERE / "stories.json").read_text())

S = 2  # supersample
W = 1024

PAPER = (246, 241, 231)
CARD = (255, 253, 247)
INK = (20, 42, 48)
TEAL = (12, 91, 92)
TEAL_DARK = (7, 47, 54)
MAP_BG = (9, 43, 51)
CORAL = (240, 100, 60)
CORAL_DARK = (199, 60, 30)
SAND = (233, 223, 201)
MUT = (96, 112, 114)
LAND = (88, 158, 148)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
_fonts = {}


def F(name, size):
    key = (name, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(f"{FONT_DIR}/{name}", size * S)
    return _fonts[key]


def SANS(size):
    return F("DejaVuSans.ttf", size)


def BOLD(size):
    return F("DejaVuSans-Bold.ttf", size)


def SERIFB(size):
    return F("DejaVuSerif-Bold.ttf", size)


img = Image.new("RGB", (W * S, W * S), PAPER)
d = ImageDraw.Draw(img)


def xy(v):
    return v * S


def wrap(text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = f"{cur} {w_}".strip()
        if d.textlength(t, font=font) <= maxw * S:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def text(x, y, s, font, fill=INK, anchor="la"):
    d.text((xy(x), xy(y)), s, font=font, fill=fill, anchor=anchor)


def rrect(x, y, w, h, r, fill=None, outline=None, width=1):
    d.rounded_rectangle([xy(x), xy(y), xy(x + w), xy(y + h)], radius=xy(r),
                        fill=fill, outline=outline, width=width * S)


# ---------------------------------------------------------------- header
M = 28
text(M, 6, "24", SERIFB(118), TEAL_DARK)
text(186, 34, "NOVEMBER 2026", BOLD(41), INK)
text(188, 88, "T U E S D A Y", BOLD(26), CORAL_DARK)
text(188, 122, "THE WORLD IN ONE IMAGE", BOLD(16), TEAL)
text(478, 126, "All the news that mattered, on one page", SANS(15), MUT)

# coral story-count block
rrect(806, 22, 190, 118, 10, fill=CORAL)
text(901, 34, str(DATA["story_count"]), BOLD(58), WHITE, anchor="ma")
text(901, 100, "STORIES", BOLD(20), WHITE, anchor="ma")
text(901, 124, "ONE DAY · ONE IMAGE", BOLD(11), WHITE, anchor="ma")

d.line([xy(M), xy(152), xy(W - M), xy(152)], fill=TEAL, width=3 * S)

# ---------------------------------------------------------------- hero
HY, HH = 164, 168
rrect(M, HY, W - 2 * M, HH, 12, fill=TEAL_DARK)
text(M + 22, HY + 14, DATA["hero"]["kicker"], BOLD(17), CORAL)
hero_lines = wrap(DATA["hero"]["headline"], BOLD(37), 690)
for i, ln in enumerate(hero_lines[:2]):
    text(M + 22, HY + 42 + i * 43, ln, BOLD(37), WHITE)
brief_lines = wrap(DATA["hero"]["brief"], SANS(16), 700)
for i, ln in enumerate(brief_lines[:3]):
    yy = HY + 126 + i * 21
    if yy + 16 <= HY + HH - 4:
        text(M + 22, yy, ln, SANS(16), (226, 238, 236))

# hero art: tanker, naval mine and waves (geometric, right side)
ax, ay = 756, HY + 30
# naval mine: spiked circle floating in the water beside the hull
mx, my, mr = ax + 196, ay + 88, 11
for a in range(0, 360, 45):
    import math
    x1 = mx + mr * 0.8 * math.cos(math.radians(a))
    y1 = my + mr * 0.8 * math.sin(math.radians(a))
    x2 = mx + (mr + 7) * math.cos(math.radians(a))
    y2 = my + (mr + 7) * math.sin(math.radians(a))
    d.line([xy(x1), xy(y1), xy(x2), xy(y2)], fill=CORAL, width=3 * S)
d.ellipse([xy(mx - mr), xy(my - mr), xy(mx + mr), xy(my + mr)], outline=CORAL,
          width=3 * S)
# small flame on the stern
d.polygon([(xy(ax + 44), xy(ay + 58)), (xy(ax + 36), xy(ay + 40)),
           (xy(ax + 44), xy(ay + 46)), (xy(ax + 50), xy(ay + 38)),
           (xy(ax + 52), xy(ay + 58))], fill=CORAL)
# hull
d.polygon([(xy(ax + 30), xy(ay + 78)), (xy(ax + 205), xy(ay + 78)),
           (xy(ax + 188), xy(ay + 102)), (xy(ax + 48), xy(ay + 102))],
          fill=(214, 226, 222))
# containers
for i, cx in enumerate((58, 96, 134)):
    rrect(ax + cx, ay + 58, 34, 20, 2, fill=CORAL if i % 2 else SAND)
rrect(ax + 172, ay + 50, 22, 28, 2, fill=SAND)
# waves
for r in range(3):
    for cx in range(ax + 26, ax + 210, 26):
        d.arc([xy(cx), xy(ay + 108 + r * 10), xy(cx + 18), xy(ay + 120 + r * 10)],
              180, 360, fill=LAND, width=2 * S)

# ---------------------------------------------------------------- panels
PY = 344
PH = 452
cols, rows = 3, 4
gap = 10
cw = (W - 2 * M - (cols - 1) * gap) / cols
ch = (PH - (rows - 1) * gap) / rows
for idx, p in enumerate(DATA["panels"]):
    cx = M + (idx % cols) * (cw + gap)
    cy = PY + (idx // cols) * (ch + gap)
    rrect(cx, cy, cw, ch, 8, fill=CARD, outline=SAND, width=1)
    # number chip
    rrect(cx + 10, cy + 9, 23, 23, 5, fill=CORAL)
    text(cx + 21.5, cy + 12, str(p["n"]), BOLD(14), WHITE, anchor="ma")
    text(cx + 41, cy + 13, p["place"], BOLD(12), TEAL)
    hl = wrap(p["headline"], BOLD(14), cw - 20)
    for i, ln in enumerate(hl[:2]):
        text(cx + 10, cy + 35 + i * 16.5, ln, BOLD(14), INK)
    bfont, blh = SANS(11), 13.5
    bl = wrap(p["brief"], bfont, cw - 20)
    if len(bl) > 3:
        bfont = SANS(10)
        bl = wrap(p["brief"], bfont, cw - 20)
    by = cy + 35 + len(hl[:2]) * 16.5 + 3
    for i, ln in enumerate(bl[:3]):
        if by + i * blh + 11 <= cy + ch - 3:
            text(cx + 10, by + i * blh, ln, bfont, (52, 66, 70))

# ---------------------------------------------------------------- map band
MY, MH = 806, 104
rrect(M, MY, W - 2 * M, MH, 12, fill=MAP_BG)
text(724, MY + 14, "WHERE IT", BOLD(19), WHITE)
text(724, MY + 36, "HAPPENED", BOLD(19), WHITE)
text(724, MY + 62, "13 pins, one day.", SANS(13), (178, 205, 200))
text(724, MY + 82, "Lead story: Hormuz.", SANS(13), CORAL)

# dotted world map from land spans (col,row) on a 100x50 grid,
# lon -180..180, lat 78..-59
SPANS = {
    0: [(9, 11), (14, 16), (19, 21), (28, 32), (56, 60), (66, 70), (78, 84), (90, 94)],
    1: [(1, 6), (9, 24), (28, 33), (50, 58), (63, 72), (80, 96)],
    2: [(0, 7), (9, 26), (29, 33), (47, 52), (55, 70), (74, 97)],
    3: [(0, 8), (10, 27), (29, 32), (46, 53), (56, 72), (76, 97)],
    4: [(1, 8), (10, 28), (30, 31), (47, 53), (55, 75), (78, 96)],
    5: [(2, 6), (11, 29), (31, 31), (46, 54), (56, 78), (80, 95)],
    6: [(2, 5), (12, 18), (22, 28), (45, 46), (47, 56), (58, 80), (83, 94)],
    7: [(3, 5), (13, 27), (45, 47), (48, 58), (60, 82), (85, 94)],
    8: [(14, 26), (44, 47), (48, 59), (61, 84), (87, 93)],
    9: [(14, 25), (44, 46), (47, 58), (60, 86), (88, 92)],
    10: [(13, 25), (44, 47), (48, 57), (59, 62), (64, 88), (89, 92)],
    11: [(12, 25), (44, 48), (49, 55), (57, 63), (65, 87), (89, 91)],
    12: [(12, 24), (43, 47), (48, 53), (54, 59), (60, 69), (70, 86), (87, 89)],
    13: [(12, 24), (43, 46), (48, 53), (54, 61), (61, 68), (69, 85), (87, 88)],
    14: [(12, 23), (43, 47), (48, 53), (55, 63), (62, 69), (70, 84), (87, 88)],
    15: [(12, 22), (42, 48), (49, 54), (55, 62), (63, 71), (71, 83)],
    16: [(11, 16), (20, 21), (41, 47), (48, 55), (55, 61), (63, 70), (71, 81), (82, 82)],
    17: [(11, 15), (40, 46), (47, 55), (56, 60), (63, 70), (71, 80)],
    18: [(11, 14), (39, 45), (46, 53), (55, 60), (63, 69), (71, 78), (80, 81)],
    19: [(12, 13), (38, 44), (45, 51), (63, 68), (71, 77), (79, 80)],
    20: [(37, 43), (44, 50), (52, 57), (64, 66), (72, 77), (80, 80)],
    21: [(36, 42), (43, 49), (50, 55), (72, 76)],
    22: [(35, 41), (42, 48), (50, 55), (73, 77), (79, 84)],
    23: [(18, 23), (36, 42), (43, 48), (49, 54), (74, 78), (80, 87)],
    24: [(17, 24), (37, 43), (44, 48), (49, 53), (74, 79), (81, 89)],
    25: [(17, 25), (38, 43), (44, 48), (49, 52), (75, 82), (84, 93)],
    26: [(17, 26), (38, 44), (46, 48), (49, 51), (77, 84), (87, 92)],
    27: [(18, 27), (39, 44), (46, 48), (49, 50)],
    28: [(18, 27), (39, 44), (46, 48), (49, 50)],
    29: [(18, 26), (39, 45), (46, 48), (50, 51)],
    30: [(18, 26), (39, 45), (46, 48), (50, 51), (84, 90)],
    31: [(18, 25), (39, 44), (50, 50), (80, 86), (88, 93)],
    32: [(19, 25), (39, 44), (50, 50), (79, 85), (87, 93)],
    33: [(19, 24), (39, 43), (50, 50), (79, 85), (87, 92)],
    34: [(19, 24), (39, 43), (50, 50), (80, 85), (87, 91)],
    35: [(19, 23), (39, 42), (80, 85), (86, 90)],
    36: [(19, 23), (39, 42), (81, 85), (86, 89)],
    37: [(20, 22), (39, 41), (82, 85), (86, 88)],
    38: [(20, 22), (39, 41), (83, 86), (95, 96)],
    39: [(20, 21), (39, 40), (83, 86), (95, 95)],
    40: [(20, 21), (94, 95)],
    41: [(20, 21), (94, 95)],
    42: [(20, 21)],
    43: [(20, 21)],
    44: [(20, 20)],
    45: [(20, 20)],
    46: [(20, 20)],
}
MAPX, MAPY, MAPW, MAPH = M + 16, MY + 7, 672, MH - 14


def proj(lon, lat):
    x = MAPX + (lon + 180) / 360 * MAPW
    y = MAPY + (78 - lat) / 137 * MAPH
    return x, y


for r, spans in SPANS.items():
    if r % 2:
        continue  # every second row: a dotted, not striped, map
    for c0, c1 in spans:
        for c in range(c0, c1 + 1):
            lon = -180 + 3.6 * c + 1.8
            lat = 78 - 2.76 * r - 1.38
            x, y = proj(lon, lat)
            d.ellipse([xy(x - 1.9), xy(y - 1.9), xy(x + 1.9), xy(y + 1.9)], fill=LAND)


def pin(lon, lat, label, hero=False):
    x, y = proj(lon, lat)
    r = 9 if hero else 7.5
    d.ellipse([xy(x - r), xy(y - r), xy(x + r), xy(y + r)], fill=CORAL,
              outline=WHITE, width=1 * S)
    text(x, y - (6 if hero else 5), label, BOLD(10 if hero else 9), WHITE,
         anchor="ma")


pin(DATA["hero"]["lon"], DATA["hero"]["lat"], "★", hero=True)
for p in DATA["panels"]:
    pin(p["lon"], p["lat"], str(p["n"]))

# ---------------------------------------------------------------- ticker
TY = 924
text(M, TY, "ALSO TODAY", BOLD(13), CORAL_DARK)
ticker = "  ·  ".join(DATA["ticker"])
tl = wrap(ticker, SANS(11), W - 2 * M - 96)
for i, ln in enumerate(tl[:3]):
    text(M + 96, TY + 1 + i * 14, ln, SANS(11), (52, 66, 70))

# ---------------------------------------------------------------- footer
d.line([xy(M), xy(978), xy(W - M), xy(978)], fill=SAND, width=2 * S)
text(W / 2, 984, DATA["sources_footer"], SANS(11), MUT, anchor="ma")

img = img.resize((W, W), Image.LANCZOS)
img.save(HERE / "entry.png", optimize=True)
print("saved", HERE / "entry.png", img.size)
