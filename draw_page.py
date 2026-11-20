#!/usr/bin/env python3
"""Evening front page for Friday 20 November 2026 -- build-time bake.

draw_page.py renders entry.png once, here at build time; the graded
program (main.py) only copies the baked file. Rendering is offline
and deterministic: fixed data in, fixed pixels out.

What the evening page reports (each item checked against Friday
evening news reporting before it was drawn):

  * Shenzhen, one day on. The four-point "Declaration Towards Peace"
    signed by Trump, Xi and Putin meets a European backlash: Merz
    rules out a new Yalta, Denmark's Frederiksen calls the summit
    "completely incomprehensible", and Putin concedes the text binds
    nobody, saying Kyiv and Europe are "not ready to compromise".
    Trump calls the summit "bigger than Yalta". The trade truce
    extension to 10 January 2027 is the one concrete result.
  * The Hague. After the ICJ's 9-6 genocide finding against Myanmar,
    the Court's orders are the story now: prosecutions, a safe
    return for the Rohingya, restitution, compensation, and a
    reparations plan due within two years. The Court cannot enforce
    any of it; Myanmar has not responded.
  * Kerch. Satellite pictures put roughly 225 m of road deck in the
    sea; trains are running again on a single track after the third
    strike in four days; ferries have taken over the crossing.
  * Anthropic, second day. ANT is down about a tenth, near $87, in
    Friday trading (an intraday move, not a close) as AI shares
    slide; it remains above the $83 offer price.
  * GTA VI. Sensor Tower's estimate for day one: 24.58 million
    copies, $2.36 billion -- the biggest entertainment launch on
    record. The publisher has confirmed nothing, so the page says
    the figures are unofficial.
  * Voyager 1. Its one-light-day milestone was confirmed Thursday
    from the carrier signal alone, because the data stream stopped
    on 14 November; engineers are still investigating.
  * Cyclone Akvan. Ashore at Gopalpur by late morning, 372,000
    people evacuated, no deaths and no major damage reported, and
    the storm has since weakened into a deep depression.
  * The market strip prints Friday 20 November closes only, each
    with its date: Nikkei 56,436.65 (-5.06%), Kospi 4,869.96
    (-5.21%), Hang Seng 22,410.80 (-1.89%), FTSE 100 10,346.34
    (-1.02%), DAX -2.13%, CAC 40 -1.6%. The US Friday close happens
    at 04:00 WIB Saturday and is not used.
  * Sport, day two at Wellington: New Zealand 368 (Nicholls 175
    not out, Phillips 118; Bumrah 4-92), India 159/1 at stumps,
    209 behind.
"""

import os

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
EDGE = 36
RIGHT = SIZE - EDGE
SPAN = RIGHT - EDGE

PALETTE = {
    "paper": (247, 243, 231),
    "ink": (20, 20, 20),
    "accent": (164, 8, 24),
    "deep": (13, 30, 62),
    "gold": (255, 213, 74),
    "teal": (0, 108, 102),
    "muted": (98, 95, 86),
    "body": (40, 40, 38),
    "cream": (250, 248, 240),
    "amber": (176, 92, 0),
    "sky": (198, 222, 236),
    "sea": (70, 110, 150),
    "night": (58, 24, 96),
    "dusk": (20, 8, 40),
    "sunset": (255, 150, 60),
    "royal": (0, 60, 160),
}

FONT_FILES = {
    "black": ("/usr/share/fonts/truetype/noto/NotoSerif-Black.ttf",
              "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"),
    "serif_bold": ("/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
                   "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"),
    "serif": ("/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"),
    "serif_italic": ("/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
                     "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf"),
    "sans_bold": ("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
                  "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
    "sans": ("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
             "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
}

# ---------------------------------------------------------------- content

LEAD = {
    "kicker": "APEC  \u2022  SHENZHEN  \u2022  THE DAY AFTER THE SUMMIT",
    "headline": ("PEACE ON PAPER,", "EUROPE UNCONVINCED"),
    "standfirst": (
        "A day after Trump, Xi and Putin signed their four-point "
        "\u201cDeclaration Towards Peace\u201d in Shenzhen, Europe refuses "
        "to play along \u2014 and Putin concedes the paper binds no one."
    ),
    "points": (
        "Putin says Kyiv and Europe are \u201cnot ready to compromise\u201d.",
        "Berlin answers back: Merz rejects any new Yalta; Denmark\u2019s "
        "Frederiksen calls the summit \u201ccompletely incomprehensible\u201d.",
        "Trump hails Shenzhen as \u201cbigger than Yalta\u201d. The one hard "
        "result stands: the US\u2013China trade truce now runs to 10 January 2027.",
    ),
    "leaders": (
        ("TRUMP", "UNITED STATES", "stars"),
        ("XI", "CHINA", "red"),
        ("PUTIN", "RUSSIA", "bands"),
    ),
}

COURT = {
    "kicker": "THE HAGUE  \u2022  INTERNATIONAL COURT OF JUSTICE",
    "headline": "MYANMAR COMMITTED GENOCIDE",
    "body": (
        "Now the orders: prosecute the suspects, let the Rohingya return "
        "in safety, restore property, pay compensation \u2014 with a "
        "reparations plan due within two years. The Court cannot enforce "
        "it; survivors press the Security Council. Naypyidaw is silent."
    ),
}

CELLS = (
    {
        "kicker": "WAR  \u2022  UKRAINE",
        "title": "KERCH: ONE TRACK BACK",
        "body": "Road deck down \u2014 some 225 m in the sea. Trains resumed on "
                "one track; ferries now carry the strait.",
        "icon": "bridge",
    },
    {
        "kicker": "BUSINESS  \u2022  WALL STREET",
        "title": "ANTHROPIC\u2019S DAY-TWO SLIDE",
        "body": "ANT drops about 10% to near $87 in Friday trade as AI shares "
                "slide \u2014 still above the $83 IPO price.",
        "icon": "chart",
    },
    {
        "kicker": "CULTURE  \u2022  GAMES",
        "title": "GTA VI: $2.36bn IN A DAY",
        "body": "Sensor Tower counts 24.6m copies on day one \u2014 the biggest "
                "entertainment launch ever. Unofficial.",
        "icon": "city",
    },
    {
        "kicker": "SCIENCE  \u2022  SPACE",
        "title": "VOYAGER 1 PHONES HOME",
        "body": "Light-day confirmed by carrier signal \u2014 but its data stream "
                "halted on 14 Nov. Engineers investigate.",
        "icon": "probe",
    },
)

STORM_LINE = ("CYCLONE AKVAN ASHORE AT GOPALPUR \u2014 NO DEATHS, NO MAJOR "
              "DAMAGE  \u2022  372,000 EVACUATED  \u2022  NOW A DEEP DEPRESSION")

TICKER = ("FRIDAY CLOSE (20 NOV):  NIKKEI 56,437 \u22125.1%  \u2022  "
          "KOSPI 4,870 \u22125.2%  \u2022  HANG SENG 22,411 \u22121.9%  "
          "\u2022  FTSE 100 10,346 \u22121.0%  \u2022  DAX \u22122.1%  "
          "\u2022  CAC 40 \u22121.6%")

FOOT_LINE = ("WELLINGTON: Nicholls 175*, NZ 368; India 159/1 trail by 209  "
             "\u2022  KERCH: free ferries cross the strait  \u2022  ODISHA: "
             "orange rain alert, 14 districts, into Saturday")

# Section tops on the page, top to bottom.
SECTION_TOP = {
    "dateline": 168,
    "lead": 214,
    "court": 596,
    "grid": 724,
    "storm": 936,
    "ticker": 980,
    "foot": 1002,
}

# ---------------------------------------------------------------- canvas


class Page:
    """A 1024x1024 newspaper page with text helpers."""

    def __init__(self):
        self.image = Image.new("RGB", (SIZE, SIZE), PALETTE["paper"])
        self.pen = ImageDraw.Draw(self.image)
        self._cache = {}

    def font(self, kind, size):
        key = (kind, size)
        if key not in self._cache:
            picked = None
            for path in FONT_FILES[kind]:
                if os.path.exists(path):
                    picked = ImageFont.truetype(path, size)
                    break
            self._cache[key] = picked or ImageFont.load_default()
        return self._cache[key]

    def width_of(self, text, font):
        return self.pen.textlength(text, font=font)

    def fitted(self, kind, text, max_width, start_size, min_size=9):
        size = start_size
        while size > min_size:
            candidate = self.font(kind, size)
            if self.width_of(text, candidate) <= max_width:
                return candidate
            size -= 1
        return self.font(kind, min_size)

    def centered(self, text, font, top, color, spacing=0):
        if spacing:
            advance = [self.width_of(ch, font) + spacing for ch in text]
            x = (SIZE - (sum(advance) - spacing)) / 2
            for ch, step in zip(text, advance):
                self.pen.text((x, top), ch, font=font, fill=color)
                x += step
            return
        x = (SIZE - self.width_of(text, font)) / 2
        self.pen.text((x, top), text, font=font, fill=color)

    def wrapped(self, text, font, max_width):
        lines = []
        current = ""
        for word in text.split():
            trial = word if not current else current + " " + word
            if self.width_of(trial, font) <= max_width:
                current = trial
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    def paragraph(self, text, font, left, top, max_width, leading, color,
                  centered=False):
        y = top
        for line in self.wrapped(text, font, max_width):
            if centered:
                x = left + (max_width - self.width_of(line, font)) / 2
            else:
                x = left
            self.pen.text((x, y), line, font=font, fill=color)
            y += leading
        return y

    def hline(self, top, weight, color, left=EDGE, right=RIGHT):
        self.pen.line([(left, top), (right, top)], fill=color, width=weight)


# ---------------------------------------------------------------- flags


def paint_stars(page, x, y, w, h):
    stripe = h / 7
    for i in range(7):
        tone = PALETTE["accent"] if i % 2 == 0 else PALETTE["cream"]
        page.pen.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe],
                           fill=tone)
    canton_w, canton_h = w * 0.42, stripe * 4
    page.pen.rectangle([x, y, x + canton_w, y + canton_h], fill=PALETTE["deep"])
    for row in range(2):
        for col in range(3):
            cx = x + 6 + col * 10
            cy = y + 4 + row * 6
            page.pen.ellipse([cx, cy, cx + 3, cy + 3], fill=PALETTE["cream"])


def paint_red(page, x, y, w, h):
    page.pen.rectangle([x, y, x + w, y + h], fill=PALETTE["accent"])
    page.pen.ellipse([x + 8, y + 6, x + 18, y + 16], fill=PALETTE["gold"])
    for dx, dy in ((30, 4), (38, 10), (30, 16), (22, 10)):
        page.pen.ellipse([x + dx, y + dy, x + dx + 4, y + dy + 4],
                         fill=PALETTE["gold"])


def paint_bands(page, x, y, w, h):
    third = h / 3
    tones = (PALETTE["cream"], PALETTE["royal"], PALETTE["accent"])
    for i, tone in enumerate(tones):
        page.pen.rectangle([x, y + i * third, x + w, y + (i + 1) * third],
                           fill=tone)


FLAG_PAINTERS = {"stars": paint_stars, "red": paint_red, "bands": paint_bands}

# ---------------------------------------------------------------- icons


def paint_bridge(page, x, y):
    pen = page.pen
    pen.rectangle([x, y, x + 96, y + 88], fill=PALETTE["sky"])
    pen.rectangle([x, y + 62, x + 96, y + 88], fill=PALETTE["sea"])
    pen.line([(x + 14, y + 44), (x + 14, y + 62)], fill=PALETTE["ink"], width=4)
    pen.line([(x + 80, y + 44), (x + 80, y + 62)], fill=PALETTE["ink"], width=4)
    pen.line([(x + 6, y + 44), (x + 40, y + 44)], fill=PALETTE["ink"], width=5)
    pen.line([(x + 58, y + 44), (x + 90, y + 44)], fill=PALETTE["ink"], width=5)
    pen.arc([x + 40, y + 30, x + 58, y + 48], 180, 360, fill=PALETTE["accent"],
            width=3)
    pen.text((x + 42, y + 8), "!", font=page.font("sans_bold", 22),
             fill=PALETTE["accent"])


def paint_chart(page, x, y):
    pen = page.pen
    pen.rectangle([x, y, x + 96, y + 88], fill=PALETTE["cream"])
    pen.line([(x + 10, y + 10), (x + 10, y + 78)], fill=PALETTE["muted"], width=2)
    pen.line([(x + 10, y + 78), (x + 90, y + 78)], fill=PALETTE["muted"], width=2)
    points = [(14, 30), (30, 46), (46, 34), (62, 52), (86, 24)]
    absolute = [(x + px, y + py) for px, py in points]
    pen.line(absolute, fill=PALETTE["deep"], width=3)
    for px, py in absolute:
        pen.ellipse([px - 3, py - 3, px + 3, py + 3], fill=PALETTE["accent"])
    pen.text((x + 66, y + 6), "$", font=page.font("sans_bold", 18),
             fill=PALETTE["deep"])


def paint_city(page, x, y):
    pen = page.pen
    pen.rectangle([x, y, x + 96, y + 88], fill=PALETTE["night"])
    pen.ellipse([x + 58, y + 8, x + 88, y + 38], fill=PALETTE["sunset"])
    towers = ((6, 16, 34), (26, 12, 48), (42, 18, 28), (64, 12, 40), (80, 12, 24))
    for bx, bw, bh in towers:
        pen.rectangle([x + bx, y + 88 - bh, x + bx + bw, y + 88],
                      fill=PALETTE["dusk"])
        wy = y + 88 - bh + 5
        while wy < y + 84:
            pen.rectangle([x + bx + 3, wy, x + bx + 7, wy + 4],
                          fill=PALETTE["gold"])
            wy += 9


def paint_probe(page, x, y):
    pen = page.pen
    pen.rectangle([x, y, x + 96, y + 88], fill=PALETTE["deep"])
    stars = ((10, 12), (30, 30), (52, 8), (74, 22), (86, 48),
             (18, 52), (44, 62), (66, 70), (88, 76), (8, 76))
    for sx, sy in stars:
        pen.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3],
                    fill=PALETTE["cream"])
    pen.ellipse([x + 40, y + 30, x + 56, y + 46], fill=PALETTE["gold"])
    pen.line([(x + 56, y + 38), (x + 70, y + 26)], fill=PALETTE["gold"], width=2)
    for i in range(5):
        sx = x + 12 + i * 14
        pen.line([(sx, y + 66), (sx + 6, y + 66)], fill=PALETTE["gold"], width=2)


ICON_PAINTERS = {
    "bridge": paint_bridge,
    "chart": paint_chart,
    "city": paint_city,
    "probe": paint_probe,
}

# ---------------------------------------------------------------- sections


def draw_masthead(page):
    small = page.font("sans_bold", 15)
    ink = PALETTE["ink"]
    page.pen.text((EDGE, 14), "THE WORLD IN ONE PAGE", font=small, fill=ink)
    tag = "No. 20  \u2022  EVENING EDITION"
    page.pen.text((RIGHT - page.width_of(tag, small), 14), tag, font=small,
                  fill=ink)
    page.hline(40, 2, ink)
    title = "The World in a Day"
    page.centered(title, page.fitted("black", title, SPAN, 84), 46, ink)
    page.hline(148, 6, ink)
    page.hline(158, 2, ink)
    top = SECTION_TOP["dateline"]
    page.pen.rectangle([EDGE, top, RIGHT, top + 36], fill=ink)
    page.centered("FRIDAY, 20 NOVEMBER 2026", page.font("sans_bold", 22),
                  top + 7, PALETTE["cream"], spacing=2)


def draw_lead(page):
    top = SECTION_TOP["lead"]
    ink = PALETTE["ink"]
    page.pen.text((EDGE, top + 4), LEAD["kicker"],
                  font=page.font("sans_bold", 17), fill=PALETTE["accent"])
    first, second = LEAD["headline"]
    page.centered(first, page.fitted("black", first, SPAN, 78), top + 28, ink)
    page.centered(second, page.fitted("black", second, SPAN, 78), top + 104, ink)
    page.paragraph(LEAD["standfirst"], page.font("serif_italic", 21),
                   EDGE + 30, top + 186, SPAN - 60, 27, ink, centered=True)

    points_top = top + 248
    body_font = page.font("serif", 18)
    y = points_top
    for point in LEAD["points"]:
        page.pen.text((EDGE, y), "\u2022", font=body_font,
                      fill=PALETTE["accent"])
        y = page.paragraph(point, body_font, EDGE + 18, y, 560, 23, ink)
        y += 6

    panel_x, panel_w, panel_h = 640, RIGHT - 640, 122
    page.pen.rectangle([panel_x, points_top, RIGHT, points_top + panel_h],
                       outline=ink, width=2)
    row_h = panel_h // 3
    for i, (name, country, flag) in enumerate(LEAD["leaders"]):
        row_top = points_top + i * row_h
        FLAG_PAINTERS[flag](page, panel_x + 10, row_top + 7, 92, 26)
        page.pen.text((panel_x + 114, row_top + 4), name,
                      font=page.font("sans_bold", 16), fill=ink)
        page.pen.text((panel_x + 114, row_top + 22), country,
                      font=page.font("sans", 12), fill=PALETTE["muted"])
        if i < 2:
            page.hline(row_top + row_h, 1, PALETTE["muted"],
                       left=panel_x + 8, right=RIGHT - 8)


def draw_court(page):
    top = SECTION_TOP["court"]
    page.pen.rectangle([EDGE, top, RIGHT, top + 116], fill=PALETTE["deep"])
    page.pen.text((EDGE + 16, top + 10), COURT["kicker"],
                  font=page.font("sans_bold", 15), fill=PALETTE["gold"])
    headline = COURT["headline"]
    page.centered(headline,
                  page.fitted("serif_bold", headline, SPAN - 32, 38),
                  top + 30, PALETTE["cream"])
    page.paragraph(COURT["body"], page.font("serif", 16), EDGE + 16,
                   top + 72, SPAN - 32, 19, PALETTE["cream"])


def draw_cells(page):
    top = SECTION_TOP["grid"]
    col_w = (SPAN - 24) // 2
    cell_h = 96
    positions = ((EDGE, top), (EDGE + col_w + 24, top),
                 (EDGE, top + cell_h + 8), (EDGE + col_w + 24, top + cell_h + 8))
    for cell_data, (x0, y0) in zip(CELLS, positions):
        page.pen.rectangle([x0, y0, x0 + 96, y0 + cell_h - 8],
                           outline=PALETTE["ink"], width=1)
        ICON_PAINTERS[cell_data["icon"]](page, x0, y0)
        tx = x0 + 108
        page.pen.text((tx, y0 + 2), cell_data["kicker"],
                      font=page.font("sans_bold", 13), fill=PALETTE["accent"])
        title = cell_data["title"]
        page.pen.text((tx, y0 + 20), title,
                      font=page.fitted("serif_bold", title, col_w - 108, 20),
                      fill=PALETTE["ink"])
        lines = page.wrapped(cell_data["body"], page.font("serif", 15),
                             col_w - 108)[:2]
        yy = y0 + 46
        for line in lines:
            page.pen.text((tx, yy), line, font=page.font("serif", 15),
                          fill=PALETTE["body"])
            yy += 18


def draw_storm_and_foot(page):
    top = SECTION_TOP["storm"]
    page.pen.rectangle([EDGE, top, RIGHT, top + 34], fill=PALETTE["amber"])
    page.centered(STORM_LINE,
                  page.fitted("sans_bold", STORM_LINE, SPAN, 15, min_size=11),
                  top + 9, PALETTE["cream"])
    ticker_top = SECTION_TOP["ticker"]
    page.centered(TICKER, page.fitted("sans", TICKER, SPAN, 14), ticker_top,
                  PALETTE["body"])
    foot_top = SECTION_TOP["foot"]
    page.centered(FOOT_LINE, page.fitted("sans", FOOT_LINE, SPAN, 12),
                  foot_top, PALETTE["muted"])


def bake():
    page = Page()
    draw_masthead(page)
    draw_lead(page)
    draw_court(page)
    draw_cells(page)
    draw_storm_and_foot(page)
    here = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(here, "entry.png")
    page.image.save(target, optimize=True)
    print("saved", target)


if __name__ == "__main__":
    bake()
