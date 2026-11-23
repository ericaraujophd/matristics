#!/usr/bin/env python3
"""
build.py · assemble the AAR 2026 deck into ONE self-contained index.html.

WHAT IT DOES
    template.html holds the slides, styles and chart code, with {{PLACEHOLDERS}}.
    This script fills them with:
      FONTS ........ Libre Baskerville + Public Sans as base64 @font-face rules
                     (from the fonts/ folder), so the type is right offline
      NOTES_n ...... speaker notes, one "## [Slide n]" section of script.md each
      IMG_* ........ the two portraits, as base64 data URIs
      IMG_THECLA, IMG_EGERIA .. two more portraits from the Matristics site,
                     for the arched portrait fan on the title slide
      QR ........... QR code to ericaraujo.com/matristics (qr.svg)
      BOMBER, SHELF_M, SHELF_O, PIPELINE, ROLLER, LETTERS_ROW,
      CHECKLIST .... the illustrations, drawn below as plain SVG
    and writes index.html. Nothing else is needed to present.

WHY ONE SCRIPT.MD
    There is exactly one copy of the talk. Edit script.md, run this again, and
    the presenter window (key P) shows the new text.

USAGE
    python3 build.py        (run inside this folder)
"""
import base64, html, re
from pathlib import Path

HERE = Path(__file__).parent
MAROON, GOLD, GOLDINK, INK2, PARCH, PARCH2, MUTED = "#6E1C2E", "#C49A2C", "#8A6514", "#4F4448", "#F5F1E8", "#EAE2D0", "#6E6468"


# --------------------------------------------------------------------------
# 1. Speaker notes from script.md
# --------------------------------------------------------------------------
def md_inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"\*(.+?)\*", r"<em>\1</em>", t)
    return t.replace("[click]", '<b class="clk">[click]</b>')

def paragraphs(block):
    out = []
    for p in re.split(r"\n\s*\n", block.strip()):
        p = p.strip()
        if not p or p == "---":
            continue
        if p.startswith("- "):
            out.append("<ul>" + "".join(f"<li>{md_inline(l[2:])}</li>" for l in p.splitlines() if l.startswith("- ")) + "</ul>")
        else:
            out.append(f"<p>{md_inline(' '.join(p.splitlines()))}</p>")
    return "".join(out)

script = (HERE / "script.md").read_text(encoding="utf-8")
main, backup = script.split("## Backup slides", 1)
notes, meta = {}, {}
for m in re.finditer(r"^## \[Slide (\d+)\]([^\n]*)\n(.*?)(?=^## |\Z)", main, re.S | re.M):
    n, head, body = m.groups()
    t = re.search(r"(\d+:\d\d)", head)                 # 20-minute target
    t15 = re.search(r"15 min: (\d+:\d\d|skip)", head)  # 15-minute target, or "skip"
    meta[n] = (t.group(1) if t else "", "READ" in head, t15.group(1) if t15 else "")
    notes[n] = paragraphs(body)
notes["B1"] = paragraphs(re.search(r"\*\*\[B1\][^*]*\*\*(.*?)(?=\*\*\[B2\])", backup, re.S).group(1))
notes["B2"] = (paragraphs(re.search(r"\*\*\[B2\][^*]*\*\*(.*?)(?=\*\*Other likely)", backup, re.S).group(1))
               + "<p><strong>Other likely questions</strong></p>" + paragraphs(backup.split("**Other likely questions**", 1)[1]))


# --------------------------------------------------------------------------
# 2. Illustrations (plain SVG, Calvin palette)
# --------------------------------------------------------------------------
def bomber():
    """John Chrysostom, the photobomber: Eric's watercolor (crown, vestments, waving),
    cut out of its paper background and stored as fan/chrysostom.webp (transparent WebP).
    Embedded as a data URI so the deck still works offline."""
    b64 = base64.b64encode((HERE / "fan/chrysostom.webp").read_bytes()).decode()
    return ('<img src="data:image/webp;base64,' + b64 + '" alt="John Chrysostom waving, '
            'peeking into the slide." style="width:100%;height:auto;display:block">')


def bomber_svg():
    """John Chrysostom, peeking in from the edge: halo, short beard, eyes
    turned sideways, white vestment with a maroon omophorion."""
    return f'''<svg viewBox="0 0 220 260" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Cartoon of John Chrysostom with a halo, peeking in from the side.">
  <circle cx="110" cy="100" r="80" fill="#E2BE63" opacity=".9"/>
  <path d="M8,262 C18,196 68,176 110,176 C152,176 202,196 212,262Z" fill="{PARCH}" stroke="{MAROON}" stroke-width="4"/>
  <path d="M34,232 C76,196 144,196 186,232" stroke="{MAROON}" stroke-width="20" fill="none"/>
  <path d="M70,214 h14 M77,207 v14 M136,214 h14 M143,207 v14" stroke="{PARCH}" stroke-width="4"/>
  <ellipse cx="110" cy="106" rx="46" ry="55" fill="#D9B08C"/>
  <path d="M64,98 C60,52 160,48 156,98 C150,72 128,62 110,62 C92,62 70,72 64,98Z" fill="#5A3A26"/>
  <path d="M66,112 C70,180 150,180 154,112 C148,150 132,140 110,142 C88,140 72,150 66,112Z" fill="#5A3A26"/>
  <ellipse cx="91" cy="102" rx="10" ry="8" fill="#fff"/><ellipse cx="129" cy="102" rx="10" ry="8" fill="#fff"/>
  <circle cx="85" cy="103" r="4.5" fill="#2A1D20"/><circle cx="123" cy="103" r="4.5" fill="#2A1D20"/>
  <path d="M80,86 q11,-8 22,-2 M118,84 q11,-6 22,2" stroke="#5A3A26" stroke-width="4" fill="none" stroke-linecap="round"/>
</svg>'''

def spine(x, w, h, base, fill, label, tcol=PARCH):
    y = base - h
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{fill}"/>'
            f'<text transform="translate({x + w/2 + 9},{base - 14}) rotate(-90)" font-family="Public Sans" font-size="22" font-weight="600" fill="{tcol}">{label}</text>')

def envelope(x, y, w=40, h=28, stroke=MAROON, fill="#fff"):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{fill}" stroke="{stroke}" stroke-width="3"/>'
            f'<path d="M{x+2},{y+3} L{x+w/2},{y+h*0.6} L{x+w-2},{y+3}" fill="none" stroke="{stroke}" stroke-width="3"/>')

def shelf_m():
    base = 196
    return (spine(20, 76, 190, base, MAROON, "Gregory · Life") + spine(106, 76, 190, base, "#8E2F3F", "Gregory · Soul")
            + f'<rect x="0" y="{base}" width="300" height="8" fill="#B9AE98"/>'
            f'<text x="0" y="228" font-family="Public Sans" font-size="22" fill="{MUTED}">one author, two texts</text>')

def shelf_o():
    base = 196
    s = (spine(10, 64, 182, base, "#5B3F8F", "Anon. · Life") + spine(82, 64, 160, base, "#7A62A8", "Palladius")
         + spine(154, 64, 168, base, "#4C3577", "Sozomen"))
    for i in range(17):                       # 17 letters from Chrysostom
        r, c = divmod(i, 6)
        s += envelope(240 + c * 46, 70 + r * 40)
    return (s + f'<rect x="0" y="{base}" width="520" height="8" fill="#B9AE98"/>'
            f'<text x="240" y="228" font-family="Public Sans" font-size="22" fill="{MUTED}">17 letters from Chrysostom</text>')

def pipeline():
    xs = [150, 495, 840, 1185, 1530]
    nums = ["35", "6", "210", "2", "420"]
    labs = ["questions", "models", "answers", "annotators", "ratings"]
    icons = [
        # stacked question cards
        lambda x: f'<rect x="{x-62}" y="62" width="104" height="132" rx="10" fill="{PARCH2}" stroke="#B9AE98" stroke-width="3"/>'
                  f'<rect x="{x-46}" y="50" width="104" height="132" rx="10" fill="#fff" stroke="{MAROON}" stroke-width="4"/>'
                  f'<text x="{x+6}" y="146" text-anchor="middle" font-family="Libre Baskerville" font-size="84" fill="{MAROON}">?</text>',
        # six model chips
        lambda x: "".join(f'<rect x="{x-80+(i%3)*56}" y="{66+(i//3)*58}" width="46" height="46" rx="8" fill="{[MAROON,GOLD,"#3E7D6B","#4C7FA8","#8E2F3F",INK2][i]}"/>' for i in range(6)),
        # cloud of answer bubbles
        lambda x: f'<path d="M{x-80},60 h110 a12,12 0 0 1 12,12 v50 a12,12 0 0 1 -12,12 h-70 l-22,20 v-20 h-18 a12,12 0 0 1 -12,-12 v-50 a12,12 0 0 1 12,-12z" fill="{PARCH2}"/>'
                  f'<path d="M{x-30},104 h106 a12,12 0 0 1 12,12 v50 a12,12 0 0 1 -12,12 h-18 v20 l-22,-20 h-66 a12,12 0 0 1 -12,-12 v-50 a12,12 0 0 1 12,-12z" fill="#fff" stroke="{MAROON}" stroke-width="4"/>'
                  f'<path d="M{x-12},132 h70 M{x-12},152 h46" stroke="{MAROON}" stroke-width="5" stroke-linecap="round"/>',
        # two annotators
        lambda x: "".join(f'<circle cx="{x+dx}" cy="92" r="26" fill="{c}"/><path d="M{x+dx-46},196 C{x+dx-44},140 {x+dx-26},126 {x+dx},126 C{x+dx+26},126 {x+dx+44},140 {x+dx+46},196Z" fill="{c}"/>'
                          for dx, c in [(-44, MAROON), (44, GOLD)]),
        # rating squares
        lambda x: "".join(f'<rect x="{x-84+(i%5)*35}" y="{70+(i//5)*35}" width="28" height="28" rx="4" fill="{GOLD if i % 4 else PARCH2}"/>' for i in range(20)),
    ]
    out = []
    for k, x in enumerate(xs):
        out.append(icons[k](x))
        out.append(f'<text x="{x}" y="340" text-anchor="middle" font-family="Libre Baskerville" font-size="110" fill="{MAROON}">{nums[k]}</text>')
        out.append(f'<text x="{x}" y="398" text-anchor="middle" font-family="Public Sans" font-size="34" fill="{INK2}">{labs[k]}</text>')
        if k < 4:
            ax = x + 120
            out.append(f'<path d="M{ax},130 h100 m-18,-14 l18,14 l-18,14" stroke="{GOLD}" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    return "".join(out)

def roller():
    """A road roller flattening a stack of sources into one strip."""
    return (f'<rect x="0" y="232" width="600" height="6" fill="#E2BE63" opacity=".5"/>'
            # already flattened: one thin strip behind the roller
            f'<rect x="0" y="222" width="250" height="10" rx="3" fill="#EADCCB"/>'
            # not yet flattened: three slips of different kinds
            f'<rect x="440" y="150" width="130" height="80" rx="6" fill="#EADCCB"/><text x="505" y="198" text-anchor="middle" font-family="Public Sans" font-size="22" fill="{MAROON}">Life</text>'
            f'<rect x="455" y="96" width="100" height="56" rx="6" fill="#E2BE63"/><text x="505" y="132" text-anchor="middle" font-family="Public Sans" font-size="20" fill="{MAROON}">letter</text>'
            f'<rect x="465" y="54" width="80" height="44" rx="6" fill="#C9A3AE"/><text x="505" y="83" text-anchor="middle" font-family="Public Sans" font-size="16" fill="{MAROON}">study</text>'
            # roller
            f'<rect x="250" y="80" width="150" height="90" rx="10" fill="#C49A2C"/>'
            f'<rect x="300" y="30" width="80" height="60" rx="8" fill="#E2BE63"/><rect x="314" y="42" width="52" height="34" rx="4" fill="#5A1625"/>'
            f'<circle cx="250" cy="172" r="62" fill="#EADCCB"/><circle cx="250" cy="172" r="20" fill="#5A1625"/>'
            f'<circle cx="372" cy="196" r="36" fill="#EADCCB"/><circle cx="372" cy="196" r="12" fill="#5A1625"/>')

def refusal_grid():
    """Slide 11: one square per answer (15 x 14 = 210). All squares are the same
    pale tone because no model refused any question. (The annotators' single
    [evasion] tag, on O13 for Gemini, was on an answer that did answer the question.)"""
    cols, rows, step, size = 15, 14, 30, 24
    out = []
    for r in range(rows):
        for c in range(cols):
            out.append(f'<rect x="{c*step}" y="{r*step}" width="{size}" height="{size}" fill="#F3EFE6" opacity=".28"/>')
    out.append(f'<text x="0" y="{rows*step+30}" font-family="Libre Franklin" font-size="22" fill="#BDB5A6">Each square is one answer · 210 in all · none refused</text>')
    return "".join(out)

def letters_row():
    """Slide 16, first row: the 17 surviving letters Chrysostom wrote to Olympias.
    Flat newsprint envelopes (square corners, thin black rule), evenly spaced so
    the row lines up with the plot area of the chart above (1020 px wide)."""
    out = []
    for i in range(17):
        x, y, w, h = i * 60 + 2, 4, 46, 32
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#FBF9F4" stroke="#111" stroke-width="2"/>'
                   f'<path d="M{x},{y} L{x+w/2},{y+h*0.58} L{x+w},{y}" fill="none" stroke="#111" stroke-width="2"/>')
    return "".join(out)

def letters_lost():
    """Slide 16, second row: Olympias's letters to Chrysostom. None survive,
    so one dashed red envelope, crossed out (same sign as 'lost' on slide 5)."""
    x, y, w, h = 2, 4, 46, 32
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="#B3261E" stroke-width="2" stroke-dasharray="5 4"/>'
            f'<path d="M{x},{y} L{x+w/2},{y+h*0.58} L{x+w},{y}" fill="none" stroke="#B3261E" stroke-width="2" stroke-dasharray="5 4"/>'
            f'<path d="M{x+8},{y-2} L{x+w-8},{y+h+2} M{x+w-8},{y-2} L{x+8},{y+h+2}" stroke="#B3261E" stroke-width="3"/>')

# Publication years of the 48 books about each woman found in open library
# catalogues (Open Library, Internet Archive, Crossref), cleaned by hand.
# Source file: biblio/books_clean.csv. Editions of the ancient texts and modern
# studies are both counted: each is a book about her.
BOOK_YEARS = {
    "Macrina": [1557, 1738, 1837, 1858, 1916, 1969, 1971, 1975, 1976, 1979, 1983, 1986, 1987, 1988,
                1989, 1993, 1994, 1996, 2001, 2005, 2007, 2008, 2009, 2013, 2016, 2020, 2021, 2021, 2022, 2026],
    "Olympias": [1873, 1876, 1885, 1933, 1947, 1957, 1964, 1968, 1976, 1982, 1996, 1997, 2016, 2016,
                 2018, 2019, 2021, 2022],
}

def books_timeline():
    """Slide 17: a dot histogram on a time axis from 1550 to 2030.
    Each dot is one book. Books are grouped by decade and stacked upward, Macrina
    (red) first, then Olympias (blue). The years since 1970 are shaded, with the
    count written in the band: 34 of the 48 books fall there.
    Geometry: 48 decades across 1440 px (30 px per decade); dots r = 11 on a 25 px step."""
    X0, W, BASE = 150, 1440, 330           # left edge of the axis, axis width, baseline y
    per_decade = W / 48
    x_of = lambda year: X0 + (year - 1550) / 480 * W
    out = []
    # shaded band for 1970-2030 and its label
    out.append(f'<rect x="{x_of(1970):.1f}" y="40" width="{x_of(2030) - x_of(1970):.1f}" height="{BASE - 40}" fill="#B3261E" opacity=".08"/>')
    out.append(f'<text x="{x_of(1970) - 14:.1f}" y="70" text-anchor="end" font-family="Bodoni Moda" font-size="40" font-weight="600" fill="#B3261E">34 of 48</text>')
    out.append(f'<text x="{x_of(1970) - 14:.1f}" y="102" text-anchor="end" font-family="Libre Franklin" font-size="24" fill="#3a3631">books appeared since 1970</text>')
    # dots, stacked per decade: Macrina first (bottom), then Olympias
    stack = {}
    for fig, color in (("Macrina", "#B3261E"), ("Olympias", "#1F4E79")):
        for y in BOOK_YEARS[fig]:
            d = y // 10 * 10
            k = stack.get(d, 0); stack[d] = k + 1
            cx = x_of(d) + per_decade / 2
            out.append(f'<circle cx="{cx:.1f}" cy="{BASE - 14 - k * 25}" r="11" fill="{color}"/>')
    # axis with a tick and label every 50 years
    out.append(f'<line x1="{X0}" y1="{BASE}" x2="{X0 + W}" y2="{BASE}" stroke="#111" stroke-width="2"/>')
    for yr in range(1550, 2031, 50):
        x = x_of(yr)
        out.append(f'<line x1="{x:.1f}" y1="{BASE}" x2="{x:.1f}" y2="{BASE + 10}" stroke="#111" stroke-width="2"/>'
                   f'<text x="{x:.1f}" y="{BASE + 40}" text-anchor="middle" font-family="Libre Franklin" font-size="22" fill="#3a3631">{yr}</text>')
    # legend, top left
    out.append('<circle cx="160" cy="58" r="11" fill="#B3261E"/><text x="180" y="66" font-family="Libre Franklin" font-size="24" fill="#111">Macrina (30)</text>'
               '<circle cx="360" cy="58" r="11" fill="#1F4E79"/><text x="380" y="66" font-family="Libre Franklin" font-size="24" fill="#111">Olympias (18)</text>')
    return "".join(out)

def checklist():
    s = f'stroke="{MAROON}" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    icons = [
        (f'<circle cx="70" cy="70" r="42" {s}/><path d="M102 102 L150 150" {s} stroke-width="14"/>', "Which source says this?"),
        (f'<rect x="20" y="30" width="70" height="110" rx="6" {s}/><path d="M34 60h42M34 80h42M34 100h30" {s} stroke-width="5"/>'
         f'<rect x="102" y="64" width="64" height="46" rx="4" {s}/><path d="M104 68 L134 92 L164 68" {s} stroke-width="5"/>', "What kind of source is it?"),
        (f'<path d="M85 22 V150 M45 150 h80 M30 50 h110" {s}/><path d="M30 50 L12 104 h36 Z M140 50 L122 104 h36 Z" {s} stroke-width="6"/>', "Is it settled?"),
        (f'<path d="M20 26 h130 a12 12 0 0 1 12 12 v76 a12 12 0 0 1 -12 12 h-80 l-30 26 v-26 h-20 a12 12 0 0 1 -12 -12 v-76 a12 12 0 0 1 12 -12z" {s}/>'
         f'<circle cx="85" cy="56" r="13" fill="{GOLD}"/><path d="M85 72 L63 112 h44 Z" fill="{GOLD}"/>', "Whose sentence is she in?"),
        (f'<path d="M58 54 q0 -32 30 -32 q30 0 30 28 q0 22 -28 32 v20" {s} stroke-width="12"/><circle cx="90" cy="138" r="8" fill="{MAROON}"/>', "What did my question assume?"),
    ]
    return "".join(f'<div class="iarch"><div class="frame"><svg viewBox="0 0 170 170" aria-hidden="true">{svg}</svg></div><p>{lab}</p></div>' for svg, lab in icons)


# --------------------------------------------------------------------------
# 3. Fonts and images
# --------------------------------------------------------------------------
FONTDIR = HERE / "fonts"
def font_face(family, file, weight, style):
    p = next(FONTDIR.rglob(file))
    b64 = base64.b64encode(p.read_bytes()).decode()
    return f"@font-face{{font-family:'{family}';font-style:{style};font-weight:{weight};font-display:block;src:url(data:font/woff2;base64,{b64}) format('woff2')}}"

# Broadsheet look (22 Nov 2026): Bodoni Moda for headlines and numbers, Libre Franklin for text.
# The old Libre Baskerville / Public Sans files stay in fonts/ but are no longer embedded.
fonts = "\n".join([
    font_face("Bodoni Moda", "bodoni-moda-latin-400-normal.woff2", 400, "normal"),
    font_face("Bodoni Moda", "bodoni-moda-latin-400-italic.woff2", 400, "italic"),
    font_face("Bodoni Moda", "bodoni-moda-latin-600-normal.woff2", 600, "normal"),
    font_face("Libre Franklin", "libre-franklin-latin-400-normal.woff2", 400, "normal"),
    font_face("Libre Franklin", "libre-franklin-latin-400-italic.woff2", 400, "italic"),
    font_face("Libre Franklin", "libre-franklin-latin-500-normal.woff2", 500, "normal"),
    font_face("Libre Franklin", "libre-franklin-latin-700-normal.woff2", 700, "normal"),
])

def data_uri(name):
    return "data:image/jpeg;base64," + base64.b64encode((HERE / name).read_bytes()).decode()

# --------------------------------------------------------------------------
# Optional logos for the pub slide (slide 2).
# Claude does not draw or download the companies' logos. If you want them,
# save the official files yourself as
#     slides/logos/chatgpt.svg   (or .png)
#     slides/logos/claude.svg    (or .png)
#     slides/logos/gemini.svg    (or .png)
# and run build.py again. Each file found is embedded as a data URI and shown
# before the model's name on slide 2; a missing file simply leaves the name alone.
# --------------------------------------------------------------------------
def logo(name):
    for ext, mime in (("svg", "image/svg+xml"), ("png", "image/png")):
        f = HERE / "logos" / f"{name}.{ext}"
        if f.exists():
            uri = f"data:{mime};base64," + base64.b64encode(f.read_bytes()).decode()
            return f'<img class="logo" src="{uri}" alt="">'
    return ""

qr = (HERE / "qr.svg").read_text()
qr = re.sub(r'width="[^"]+" height="[^"]+" ', "", qr[qr.index("<svg"):], count=1)


# --------------------------------------------------------------------------
# 4. Assemble
# --------------------------------------------------------------------------
page = (HERE / "template.html").read_text(encoding="utf-8")
fills = {
    "FONTS": fonts, "QR": qr,
    "IMG_THECLA": data_uri("fan/thecla.jpg"), "IMG_EGERIA": data_uri("fan/egeria.jpg"),
    "IMG_MACRINA": data_uri("macrina.jpg"), "IMG_OLYMPIAS": data_uri("olympias.jpg"),
    "BOMBER": bomber(), "SHELF_M": shelf_m(), "SHELF_O": shelf_o(),
    "LOGO_CHATGPT": logo("chatgpt"), "LOGO_CLAUDE": logo("claude"), "LOGO_GEMINI": logo("gemini"),
    "PIPELINE": pipeline(), "ROLLER": roller(), "REFUSALS": refusal_grid(), "LETTERS_ROW": letters_row(), "BOOKS_TIMELINE": books_timeline(), "LETTERS_LOST": letters_lost(), "CHECKLIST": checklist(),
}
fills.update({f"NOTES_{k}": v for k, v in notes.items()})
for k, v in fills.items():
    page = page.replace("{{" + k + "}}", v)

def add_meta(m):                       # target time + READ flag for the presenter window
    n = re.search(r'aria-label="Slide (\d+):', m.group(0))
    if not n or n.group(1) not in meta:
        return m.group(0)
    t, read, t15 = meta[n.group(1)]
    return m.group(0).replace("<section", f'<section data-target="{t}" data-target15="{t15}"' + (' data-read="1"' if read else ""), 1)
page = re.sub(r"<section[^>]*>", add_meta, page)

BROADSHEET = {
    "#6E1C2E": "#111111", "#5A1625": "#111111",            # Calvin maroon -> newsprint black
    "#C49A2C": "#B3261E", "#8A6514": "#B3261E",            # Calvin gold   -> press red
    "#E2BE63": "#E8453A", "#F07A6E": "#E8453A",            # light gold on dark -> bright press red on black (was a paler #F07A6E)
    "#F5F1E8": "#F3EFE6", "#EAE2D0": "#E4DDCF",            # parchment     -> newsprint
    "#B9AE98": "#BDB5A6", "#5B3F8F": "#1F4E79",            # neutral bars; Olympias violet -> ink blue
    "rgba(196,154,44,.35)": "rgba(179,38,30,.22)",
}
for old, new in BROADSHEET.items():
    page = page.replace(old, new).replace(old.lower(), new)
page = page.replace("Libre Baskerville", "Bodoni Moda").replace("Public Sans", "Libre Franklin")

left = re.findall(r"\{\{[A-Z_0-9]+\}\}", page)
assert not left, f"unfilled: {left}"
(HERE / "index.html").write_text(page, encoding="utf-8")
print(f"wrote index.html ({len(page)//1024} KB), notes for {len(notes)} slides")
