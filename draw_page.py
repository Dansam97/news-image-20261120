#!/usr/bin/env python3
"""Draw the EVENING front page for Friday 20 November 2026 (build time).

Reads nothing from the network. Renders entry.png with Pillow and the
system fonts, 1024x1024, deterministically: same code, same bytes.

Evening edition: the morning page previewed the day; this page reports
how Friday actually ended. Every item below was checked against live
news reporting on Friday evening (WIB) before drawing:

  * Shenzhen, the day after: the four-point "Declaration Towards Peace"
    signed by Trump, Xi and Putin draws a European backlash. Merz
    rejects any new Yalta; Denmark's Frederiksen calls the summit
    "completely incomprehensible"; Putin concedes the text sets no
    ambitious goals and that nobody will be forced to comply, and says
    Europe and Ukraine are "not ready to compromise". Trump calls the
    summit "bigger than Yalta". The one hard result stands: the
    US-China trade truce is extended to 10 January 2027.
  * The Hague, the orders: after the ICJ's 9-6 finding that Myanmar
    committed genocide against the Rohingya, the Court orders
    investigations and prosecutions, a safe and dignified return,
    restitution of property and compensation, with a reparations plan
    due within two years. The Court has no enforcement arm; survivors'
    groups press the Security Council; Myanmar has not replied.
  * Kerch Bridge: satellite imagery shows about 225 m of the road deck
    in the sea; trains resumed Thursday on one of the two tracks after
    the third strike in four days; free ferries now cross the strait.
  * Anthropic, day two: ANT slides about 10% to near $87 in Friday
    trading as AI stocks sell off (intraday, not a close) -- still
    above the $83 IPO price, a day after closing at $97.17.
  * GTA VI: Sensor Tower estimates 24.58m copies and $2.36bn on day
    one (19 Nov) -- the biggest entertainment launch ever, roughly
    three times GTA V's first day. Take-Two has released no official
    figures, so the numbers are labelled estimates.
  * Voyager 1: the one-light-day milestone was confirmed on Thursday
    by carrier signal and trajectory, but the probe's science and
    engineering data stream stopped on 14 Nov; engineers investigate.
  * Cyclone Akvan: landfall near Gopalpur completed by 11:20 on
    Friday, winds 70-80 km/h gusting to 90; 372,000 people evacuated;
    no deaths or major damage reported; the storm weakened to a deep
    depression, with an orange rain alert for 14 districts.
  * Markets strip uses FRIDAY 20 Nov closes only, each labelled:
    Asia (Nikkei 56,436.65 -5.06%, Kospi 4,869.96 -5.21%, Hang Seng
    22,410.80 -1.89%) and Europe (FTSE 100 10,346.34 -1.02%, DAX
    -2.13%, CAC 40 -1.6%). Friday's US close happens at 04:00 WIB on
    Saturday and is deliberately NOT used or invented.
  * Sport, day two at Wellington: New Zealand 368 (Nicholls 175*,
    Phillips 118, Bumrah 4-92); India 159/1 at stumps (Jaiswal 85,
    Rahul 52*), trailing by 209.
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W = H = 1024
M = 34                      # side margin
R = W - M                   # right edge

PAPER = (247, 243, 231)
INK = (18, 18, 18)
RED = (164, 8, 24)
NAVY = (13, 30, 62)
GOLD = (255, 213, 74)
TEAL = (0, 108, 102)
GREY = (98, 95, 86)
FAINT = (40, 40, 38)
CREAM = (250, 248, 240)
AMBER = (176, 92, 0)

BLACK = ["/usr/share/fonts/truetype/noto/NotoSerif-Black.ttf",
         "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"]
BOLD = ["/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"]
REG = ["/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
       "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"]
ITAL = ["/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf"]
SANSB = ["/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
         "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
SANS = ["/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]


def load(paths, size):
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def shrink(paths, text, max_w, start, floor=10):
    """Largest font size at which text fits max_w."""
    size = start
    while size > floor:
        f = load(paths, size)
        if canvas.textlength(text, font=f) <= max_w:
            return f
        size -= 2
    return load(paths, floor)


def centre(text, font, y, fill=INK, track=0):
    if track:
        widths = [canvas.textlength(ch, font=font) + track for ch in text]
        total = sum(widths) - track
        x = (W - total) / 2
        for ch, w in zip(text, widths):
            canvas.text((x, y), ch, font=font, fill=fill)
            x += w
        return
    w = canvas.textlength(text, font=font)
    canvas.text(((W - w) / 2, y), text, font=font, fill=fill)


def flow(text, font, max_w):
    """Greedy word wrap; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if canvas.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(text, font, x, y, max_w, leading, fill=INK, align_left=True):
    for line in flow(text, font, max_w):
        if align_left:
            canvas.text((x, y), line, font=font, fill=fill)
        else:
            canvas.text(((W - canvas.textlength(line, font=font)) / 2, y),
                        line, font=font, fill=fill)
        y += leading
    return y


def rule(y, weight=2, fill=INK, x0=None, x1=None):
    canvas.line([(x0 or M, y), (x1 or R, y)], fill=fill, width=weight)


img = Image.new("RGB", (W, H), PAPER)
canvas = ImageDraw.Draw(img)

# ---------------------------------------------------------------- top line
tiny = load(SANSB, 15)
canvas.text((M, 14), "THE WORLD IN ONE PAGE", font=tiny, fill=INK)
right = "No. 20  \u2022  EVENING EDITION"
canvas.text((R - canvas.textlength(right, font=tiny), 14), right,
            font=tiny, fill=INK)
rule(40, 2)

# ---------------------------------------------------------------- masthead
centre("The World in a Day",
       shrink(BLACK, "The World in a Day", R - M, 84), 44)
rule(148, 6)
rule(158, 2)

# ---------------------------------------------------------------- dateline
canvas.rectangle([M, 168, R, 204], fill=INK)
centre("FRIDAY, 20 NOVEMBER 2026", load(SANSB, 22), 175, fill=CREAM,
       track=2)

# ---------------------------------------------------------------- lead
canvas.text((M, 218), "APEC  \u2022  SHENZHEN  \u2022  THE DAY AFTER THE SUMMIT",
            font=load(SANSB, 17), fill=RED)
centre("PEACE ON PAPER,",
       shrink(BLACK, "PEACE ON PAPER,", R - M, 78), 242)
centre("EUROPE UNCONVINCED",
       shrink(BLACK, "EUROPE UNCONVINCED", R - M, 78), 318)
deck = ("A day after Trump, Xi and Putin signed their four-point "
        "\u201cDeclaration Towards Peace\u201d in Shenzhen, Europe refuses "
        "to play along \u2014 and Putin concedes the paper binds no one.")
para(deck, load(ITAL, 21), M + 30, 400, R - M - 60, 27, align_left=False)

# lead lower half: bullets left, three flags right
ly = 462
bullet_f = load(REG, 18)
bullets = [
    "Putin says Kyiv and Europe are \u201cnot ready to compromise\u201d.",
    "Berlin answers back: Merz rejects any new Yalta; Denmark\u2019s "
    "Frederiksen calls the summit \u201ccompletely incomprehensible\u201d.",
    "Trump hails Shenzhen as \u201cbigger than Yalta\u201d. The one hard "
    "result stands: the US\u2013China trade truce now runs to 10 January 2027.",
]
for b in bullets:
    canvas.text((M, ly), "\u2022", font=bullet_f, fill=RED)
    ly = para(b, bullet_f, M + 18, ly, 560, 23)
    ly += 6

fx0, fx1 = 640, R
fy = 462
canvas.rectangle([fx0, fy, fx1, fy + 122], outline=INK, width=2)
flags = [
    ("TRUMP", "UNITED STATES", "us"),
    ("XI", "CHINA", "cn"),
    ("PUTIN", "RUSSIA", "ru"),
]
row_h = 122 // 3
for i, (name, country, code) in enumerate(flags):
    ry = fy + i * row_h
    fw, fh = 92, 26
    fx, fyy = fx0 + 10, ry + 7
    if code == "us":
        for s in range(7):
            canvas.rectangle([fx, fyy + s * 4, fx + fw, fyy + s * 4 + 4],
                             fill=RED if s % 2 == 0 else CREAM)
        canvas.rectangle([fx, fyy, fx + 38, fyy + 14], fill=NAVY)
        for dx in (6, 16, 26):
            for dy in (4, 10):
                canvas.ellipse([fx + dx, fyy + dy, fx + dx + 3,
                                fyy + dy + 3], fill=CREAM)
    elif code == "cn":
        canvas.rectangle([fx, fyy, fx + fw, fyy + fh], fill=RED)
        canvas.ellipse([fx + 8, fyy + 6, fx + 18, fyy + 16], fill=GOLD)
        for dx, dy in ((30, 4), (38, 10), (30, 16), (22, 10)):
            canvas.ellipse([fx + dx, fyy + dy, fx + dx + 4, fyy + dy + 4],
                           fill=GOLD)
    else:
        canvas.rectangle([fx, fyy, fx + fw, fyy + 9], fill=CREAM)
        canvas.rectangle([fx, fyy + 9, fx + fw, fyy + 18], fill=(0, 60, 160))
        canvas.rectangle([fx, fyy + 18, fx + fw, fyy + fh], fill=RED)
    canvas.text((fx + fw + 12, ry + 4), name, font=load(SANSB, 16), fill=INK)
    canvas.text((fx + fw + 12, ry + 22), country, font=load(SANS, 12),
                fill=GREY)
    if i < 2:
        canvas.line([(fx0 + 8, ry + row_h), (fx1 - 8, ry + row_h)],
                    fill=GREY, width=1)

# ---------------------------------------------------------------- ICJ band
iy0, iy1 = 596, 712
canvas.rectangle([M, iy0, R, iy1], fill=NAVY)
canvas.text((M + 16, iy0 + 10), "THE HAGUE  \u2022  INTERNATIONAL COURT OF JUSTICE",
            font=load(SANSB, 15), fill=GOLD)
centre("MYANMAR COMMITTED GENOCIDE",
       shrink(BOLD, "MYANMAR COMMITTED GENOCIDE", R - M - 32, 38),
       iy0 + 30, fill=CREAM)
icj = ("Now the orders: prosecute the suspects, let the Rohingya return "
       "in safety, restore property, pay compensation \u2014 with a "
       "reparations plan due within two years. The Court cannot enforce "
       "it; survivors press the Security Council. Naypyidaw is silent.")
para(icj, load(REG, 16), M + 16, iy0 + 72, R - M - 32, 19, fill=CREAM)

# ---------------------------------------------------------------- picture grid
gy = 724
col_w = (R - M - 24) // 2
cell_h = 96
lab_f = load(SANSB, 13)
head_f = load(BOLD, 20)
body_f = load(REG, 15)


def cell(x0, y0, label, head, body, draw_icon):
    canvas.rectangle([x0, y0, x0 + 96, y0 + cell_h - 8], outline=INK, width=1)
    draw_icon(x0, y0)
    tx = x0 + 108
    canvas.text((tx, y0 + 2), label, font=lab_f, fill=RED)
    canvas.text((tx, y0 + 20),
                head if canvas.textlength(head, font=head_f) <= col_w - 108
                else head, font=shrink(BOLD, head, col_w - 108, 20), fill=INK)
    yy = y0 + 46
    for ln in flow(body, body_f, col_w - 108)[:2]:
        canvas.text((tx, yy), ln, font=body_f, fill=FAINT)
        yy += 18


def icon_kerch(x0, y0):
    canvas.rectangle([x0, y0, x0 + 96, y0 + 88], fill=(198, 222, 236))
    canvas.rectangle([x0, y0 + 62, x0 + 96, y0 + 88], fill=(70, 110, 150))
    canvas.line([(x0 + 6, y0 + 44), (x0 + 40, y0 + 44)], fill=INK, width=5)
    canvas.line([(x0 + 58, y0 + 44), (x0 + 90, y0 + 44)], fill=INK, width=5)
    canvas.line([(x0 + 14, y0 + 44), (x0 + 14, y0 + 62)], fill=INK, width=4)
    canvas.line([(x0 + 80, y0 + 44), (x0 + 80, y0 + 62)], fill=INK, width=4)
    canvas.arc([x0 + 40, y0 + 30, x0 + 58, y0 + 48], 180, 360, fill=RED,
               width=3)
    canvas.text((x0 + 42, y0 + 8), "!", font=load(SANSB, 22), fill=RED)


def icon_anthropic(x0, y0):
    canvas.rectangle([x0, y0, x0 + 96, y0 + 88], fill=CREAM)
    bars = [(8, 30), (24, 44), (40, 58), (56, 40), (72, 28)]
    for bx, bh in bars:
        canvas.rectangle([x0 + bx, y0 + 78 - bh, x0 + bx + 12, y0 + 78],
                         fill=TEAL if bx < 56 else RED)
    canvas.line([(x0 + 6, y0 + 18), (x0 + 30, y0 + 34), (x0 + 52, y0 + 20),
                 (x0 + 88, y0 + 52)], fill=NAVY, width=3)
    canvas.text((x0 + 8, y0 + 4), "$", font=load(SANSB, 18), fill=NAVY)


def icon_gta(x0, y0):
    canvas.rectangle([x0, y0, x0 + 96, y0 + 88], fill=(58, 24, 96))
    canvas.ellipse([x0 + 58, y0 + 8, x0 + 88, y0 + 38], fill=(255, 150, 60))
    for bx, bw, bh in ((6, 16, 34), (26, 12, 48), (42, 18, 28),
                       (64, 12, 40), (80, 12, 24)):
        canvas.rectangle([x0 + bx, y0 + 88 - bh, x0 + bx + bw, y0 + 88],
                         fill=(20, 8, 40))
        for wy in range(y0 + 88 - bh + 5, y0 + 84, 9):
            canvas.rectangle([x0 + bx + 3, wy, x0 + bx + 7, wy + 4],
                             fill=GOLD)


def icon_voyager(x0, y0):
    canvas.rectangle([x0, y0, x0 + 96, y0 + 88], fill=NAVY)
    for sx, sy in ((10, 12), (30, 30), (52, 8), (74, 22), (86, 48),
                   (18, 52), (44, 62), (66, 70), (88, 76), (8, 76)):
        canvas.ellipse([x0 + sx, y0 + sy, x0 + sx + 3, y0 + sy + 3],
                       fill=CREAM)
    for i in range(5):
        canvas.line([(x0 + 12 + i * 14, y0 + 66), (x0 + 18 + i * 14, y0 + 66)],
                    fill=GOLD, width=2)
    canvas.ellipse([x0 + 40, y0 + 30, x0 + 56, y0 + 46], fill=GOLD)
    canvas.line([(x0 + 56, y0 + 38), (x0 + 70, y0 + 26)], fill=GOLD, width=2)


cell(M, gy, "WAR  \u2022  UKRAINE", "KERCH: ONE TRACK BACK",
     "Road deck down \u2014 some 225 m in the sea. Trains resumed on "
     "one track; ferries now carry the strait.", icon_kerch)
cell(M + col_w + 24, gy, "BUSINESS  \u2022  WALL STREET",
     "ANTHROPIC\u2019S DAY-TWO SLIDE",
     "ANT drops about 10% to near $87 in Friday trade as AI shares "
     "slide \u2014 still above the $83 IPO price.", icon_anthropic)
cell(M, gy + cell_h + 8, "CULTURE  \u2022  GAMES", "GTA VI: $2.36bn IN A DAY",
     "Sensor Tower counts 24.6m copies on day one \u2014 the biggest "
     "entertainment launch ever. Unofficial.", icon_gta)
cell(M + col_w + 24, gy + cell_h + 8, "SCIENCE  \u2022  SPACE",
     "VOYAGER 1 PHONES HOME",
     "Light-day confirmed by carrier signal \u2014 but its data stream "
     "halted on 14 Nov. Engineers investigate.", icon_voyager)

# ---------------------------------------------------------------- Akvan strip
ay = 936
canvas.rectangle([M, ay, R, ay + 34], fill=AMBER)
akvan = ("CYCLONE AKVAN ASHORE AT GOPALPUR \u2014 NO DEATHS, NO MAJOR DAMAGE  "
         "\u2022  372,000 EVACUATED  \u2022  NOW A DEEP DEPRESSION")
centre(akvan, shrink(SANSB, akvan, R - M, 15, floor=11), ay + 9, fill=CREAM)

# ---------------------------------------------------------------- markets
my = 980
tick = ("FRIDAY CLOSE (20 NOV):  NIKKEI 56,437 \u22125.1%  \u2022  "
        "KOSPI 4,870 \u22125.2%  \u2022  HANG SENG 22,411 \u22121.9%  "
        "\u2022  FTSE 100 10,346 \u22121.0%  \u2022  DAX \u22122.1%  "
        "\u2022  CAC 40 \u22121.6%")
centre(tick, shrink(SANS, tick, R - M, 14), my, fill=FAINT)

# ---------------------------------------------------------------- footer briefs
fy = 1002
brief = ("WELLINGTON: Nicholls 175*, NZ 368; India 159/1 trail by 209  "
         "\u2022  KERCH: free ferries cross the strait  \u2022  ODISHA: "
         "orange rain alert, 14 districts, into Saturday")
centre(brief, shrink(SANS, brief, R - M, 12), fy, fill=GREY)

img.save(OUT, optimize=True)
print("saved", OUT)
