"""
make_figures.py
===============
Draws the five result figures for the READER EDITION of the AAR 2026 paper
(the version without presentation cues that is published on the website).

Output (SVG, one file per figure) goes to the website folder
    talks/aar-2026/figures/
so that the web page (talks/aar-2026/index.qmd) and the reader PDF
(tools/make_reader.py) use exactly the same pictures.

    fig1-overall.svg     mean overall score per model            (slide 9)
    fig2-dimensions.svg  share of perfect 5s per rubric dimension (slide 10)
    fig3-tags.svg        how often each failure tag was applied   (slide 12)
    fig4-women.svg       Macrina vs Olympias score per model      (slide 16)
    fig5-books.svg       books about each woman, by decade        (slide 17)

Where the numbers come from
---------------------------
Every number below is copied from the DATA block at the bottom of
slides/template.html (which itself comes from the Matristics full report,
Results and Agreement sections) and from BOOK_YEARS in slides/build.py
(which comes from biblio/books_clean.csv). If you change a number in the deck,
change it here too. They are duplicated on purpose so this script has no
dependency on the deck's JavaScript.

Fonts
-----
The figures use Public Sans, the same sans-serif as the reader PDF. The repo
only keeps the fonts as .woff2 (for the web), and matplotlib cannot read
.woff2, so the script converts them to .ttf in a temporary folder first.
That needs:  pip install matplotlib fonttools brotli
All text is then converted to outlines in the SVG (svg.fonttype = "path"), so
the SVGs look identical everywhere, with no font files needed to view them.

Run
---
    python3 tools/make_figures.py      (from any directory)
"""
import pathlib
import tempfile

import matplotlib
matplotlib.use("Agg")                      # no display needed
import matplotlib.pyplot as plt
from matplotlib import font_manager
from fontTools.ttLib import TTFont

# ---------------------------------------------------------------------------
# Paths: everything is relative to this file, so the script runs from anywhere.
#   TALK = _talks/aar-2026      (sources and tools)
#   OUT  = talks/aar-2026/figures  (website folder that Quarto renders)
# ---------------------------------------------------------------------------
TALK = pathlib.Path(__file__).resolve().parent.parent
REPO = TALK.parent.parent
OUT = REPO / "talks" / "aar-2026" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Fonts: convert the .woff2 files to .ttf and register them with matplotlib.
# ---------------------------------------------------------------------------
_tmp = pathlib.Path(tempfile.mkdtemp())
for woff in (TALK / "tools" / "fonts").glob("public-sans-*.woff2"):
    font = TTFont(woff)
    font.flavor = None                     # None = plain TrueType/OpenType, i.e. not WOFF2
    # These web subsets carry the internal family name "Public Sans Thin" and no
    # usable weight, so matplotlib cannot tell 400 from 600. Rename the family to
    # "Public Sans" and set the weight from the file name (…-400-… or …-600-…).
    weight = int(woff.stem.split("-")[3])
    font["OS/2"].usWeightClass = weight
    for rec in font["name"].names:
        if rec.nameID in (1, 16):          # 1 = family, 16 = typographic family
            rec.string = "Public Sans"
    ttf = _tmp / (woff.stem + ".ttf")
    font.save(ttf)
    font_manager.fontManager.addfont(str(ttf))

plt.rcParams.update({
    "font.family": "Public Sans",
    "font.size": 9.5,
    "svg.fonttype": "path",                # text as outlines: no font needed to view the SVG
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.spines.left": False,
    "axes.edgecolor": "#1E1B18",
    "xtick.color": "#4A4540",
    "ytick.color": "#1E1B18",
    "ytick.major.size": 0,                 # no tick marks on the category axis
    "figure.dpi": 100,
})

# ---------------------------------------------------------------------------
# Colours. The same two hues as the deck: red for Macrina and for "the thing to
# look at", blue for Olympias. Greys for everything else. The website shows the
# figures on a light card, so dark text works in both light and dark mode.
# ---------------------------------------------------------------------------
INK = "#1E1B18"      # text and axis
GREY = "#8C857B"     # secondary marks
PALE = "#DDD6CA"     # the "rest" of a stacked bar
RED = "#B23A2E"      # Macrina; highlighted bars
BLUE = "#2E5C8A"     # Olympias
WIDTH = 6.5          # inches: the text width of the reader PDF (Letter, 1in margins)


def frame(fig, height):
    """Give every figure the same margins, in inches, so that the plotting area
    starts at the same x position and the text is the same size in all five
    figures once they are scaled to the page width. (bbox_inches="tight" would
    crop each figure differently, and then a figure with short labels would be
    scaled up more than one with long labels.)"""
    fig.subplots_adjust(left=1.35 / WIDTH, right=1 - 0.75 / WIDTH,
                        bottom=0.55 / height, top=1 - 0.08 / height)


def save(fig, name):
    """Write one figure as SVG with a transparent background."""
    fig.savefig(OUT / name, format="svg", transparent=True)
    plt.close(fig)
    print("wrote", OUT / name)


# ---------------------------------------------------------------------------
# Figure 1 (slide 9): mean overall score per model, 70 ratings each.
# A lollipop chart. The axis starts at 4.0, NOT 0, and the caption and the
# text both say so, because this exaggerates differences of under 0.2.
# ---------------------------------------------------------------------------
overall = [("Claude Sonnet 5", 4.73), ("GPT-5.5", 4.72), ("Grok 4.5", 4.68),
           ("Gemini 3.5 Flash", 4.61), ("DeepSeek v4 Pro", 4.58), ("GLM 5.2", 4.56)]

fig, ax = plt.subplots(figsize=(WIDTH, 2.5))
frame(fig, 2.5)
for i, (model, v) in enumerate(overall):
    y = len(overall) - 1 - i               # first model at the top
    ax.hlines(y, 4.0, v, color=GREY, lw=1.4)
    ax.plot(v, y, "o", ms=8, color=INK)
    ax.text(v + 0.025, y, f"{v:.2f}", va="center", fontsize=9.5, color=INK)
ax.set_yticks(range(len(overall)), [m for m, _ in reversed(overall)])
ax.set_xlim(4.0, 5.0)
ax.set_ylim(-0.6, len(overall) - 0.4)
ax.set_xticks([4.0, 4.2, 4.4, 4.6, 4.8, 5.0])
ax.set_xlabel("Mean overall score, scale 1 to 5 (the axis starts at 4.0)", color="#4A4540")
save(fig, "fig1-overall.svg")

# ---------------------------------------------------------------------------
# Figure 2 (slide 10): for each rubric dimension, the share of the 420 ratings
# that were a perfect 5 (red) and the rest (pale), with the mean written at the
# end of each bar. Epistemic Quality is the lowest on both counts.
# ---------------------------------------------------------------------------
dims = [("Historical Accuracy", 84, 4.75), ("Coverage", 78, 4.71),
        ("Framing & Agency", 72, 4.66), ("Epistemic Quality", 57, 4.46)]

fig, ax = plt.subplots(figsize=(WIDTH, 2.0))
frame(fig, 2.0)
for i, (name, pct5, mean) in enumerate(dims):
    y = len(dims) - 1 - i
    ax.barh(y, pct5, color=RED, height=0.62)
    ax.barh(y, 100 - pct5, left=pct5, color=PALE, height=0.62)
    ax.text(pct5 - 1.5, y, f"{pct5}%", va="center", ha="right", color="white", fontsize=9.5, weight="semibold")
    ax.text(101.5, y, f"mean {mean:.2f}", va="center", fontsize=9.5, color=INK)
ax.set_yticks(range(len(dims)), [d for d, _, _ in reversed(dims)])
ax.set_xlim(0, 100)
ax.set_xticks([0, 25, 50, 75, 100], ["0%", "25%", "50%", "75%", "100%"])
ax.set_xlabel("Share of ratings that were a 5 (red), out of 420 per dimension", color="#4A4540")
save(fig, "fig2-dimensions.svg")

# ---------------------------------------------------------------------------
# Figure 3 (slide 12): how many times each failure tag was applied across the
# 420 ratings. The two flattening tags are red; the four tags for plain factual
# error are grey. The single "evasion" tag (O13, Gemini) is left out: that
# answer did answer the question, which is why the paper says "no refusals".
# ---------------------------------------------------------------------------
tags = [("source conflation", 25, True), ("debate flattened", 24, True),
        ("hallucination", 13, False), ("anachronism", 6, False),
        ("imprecision", 6, False), ("misattribution", 3, False)]

fig, ax = plt.subplots(figsize=(WIDTH, 2.3))
frame(fig, 2.3)
for i, (name, n, flat) in enumerate(tags):
    y = len(tags) - 1 - i
    ax.barh(y, n, color=RED if flat else GREY, height=0.62)
    ax.text(n + 0.4, y, str(n), va="center", fontsize=9.5, color=INK)
ax.set_yticks(range(len(tags)), [t for t, _, _ in reversed(tags)])
ax.set_xlim(0, 28)
ax.set_xlabel("Times the tag was applied. Red: flattening, 49 in all. Grey: factual errors, 28 in all.",
              color="#4A4540")
save(fig, "fig3-tags.svg")

# ---------------------------------------------------------------------------
# Figure 4 (slide 16): mean overall score on Macrina (red) and on Olympias
# (blue), per model, joined by a line. In five of six rows the blue dot is to
# the left, i.e. the better-documented woman scores lower.
# ---------------------------------------------------------------------------
women = [("Claude Sonnet 5", 4.74, 4.71), ("GPT-5.5", 4.83, 4.59), ("Grok 4.5", 4.67, 4.68),
         ("Gemini 3.5 Flash", 4.62, 4.60), ("DeepSeek v4 Pro", 4.65, 4.51), ("GLM 5.2", 4.61, 4.51)]

fig, ax = plt.subplots(figsize=(WIDTH, 2.6))
frame(fig, 2.6)
for i, (model, m, o) in enumerate(women):
    y = len(women) - 1 - i
    ax.hlines(y, min(m, o), max(m, o), color=PALE, lw=3.5)
    ax.plot(m, y, "o", ms=8.5, color=RED, label="Macrina" if i == 0 else None)
    ax.plot(o, y, "o", ms=8.5, color=BLUE, label="Olympias" if i == 0 else None)
ax.set_yticks(range(len(women)), [w for w, _, _ in reversed(women)])
ax.set_xlim(4.4, 4.9)
ax.set_ylim(-1.5, len(women) - 0.4)   # room under the last row for the legend
ax.set_xlabel("Mean overall score (axis runs from 4.4 to 4.9). Overall: Macrina 4.69, Olympias 4.60",
              color="#4A4540")
ax.legend(loc="lower right", frameon=False, ncol=2, handletextpad=0.3, columnspacing=1.2)
save(fig, "fig4-women.svg")

# ---------------------------------------------------------------------------
# Figure 5 (slide 17): one dot per book about Macrina (red) or Olympias (blue),
# grouped by decade and stacked upward (Macrina's books first in each decade).
# The years since 1970 are shaded: 34 of the 48 books fall there.
# Years copied from BOOK_YEARS in slides/build.py (from biblio/books_clean.csv).
# ---------------------------------------------------------------------------
BOOK_YEARS = {
    "Macrina": [1557, 1738, 1837, 1858, 1916, 1969, 1971, 1975, 1976, 1979, 1983, 1986, 1987, 1988,
                1989, 1993, 1994, 1996, 2001, 2005, 2007, 2008, 2009, 2013, 2016, 2020, 2021, 2021, 2022, 2026],
    "Olympias": [1873, 1876, 1885, 1933, 1947, 1957, 1964, 1968, 1976, 1982, 1996, 1997, 2016, 2016,
                 2018, 2019, 2021, 2022],
}
assert sum(len(v) for v in BOOK_YEARS.values()) == 48
assert sum(y >= 1970 for v in BOOK_YEARS.values() for y in v) == 34

fig, ax = plt.subplots(figsize=(WIDTH, 2.2))
frame(fig, 2.2)
fig.subplots_adjust(left=0.25 / WIDTH, right=1 - 0.25 / WIDTH)   # no category labels here: use the full width
ax.axvspan(1970, 2030, color="#EFE9DE", zorder=0)         # the "since 1970" band
ax.text(1962, 5.6, "34 of the 48 books\nappeared since 1970", ha="right", va="center", fontsize=9.5, color=INK, weight="semibold")
stack = {}                                               # decade -> how many dots already stacked
for name, colour in (("Macrina", RED), ("Olympias", BLUE)):
    for year in BOOK_YEARS[name]:
        decade = year // 10 * 10
        k = stack.get(decade, 0)
        stack[decade] = k + 1
        ax.plot(decade + 5, k + 0.55, "o", ms=5.6, color=colour,
                label=name if (year == BOOK_YEARS[name][0]) else None, zorder=2)
ax.set_xlim(1550, 2030)
ax.set_ylim(0, 7.6)
ax.set_yticks([])
ax.spines["bottom"].set_position(("data", 0))
ax.set_xticks(range(1550, 2031, 50))
ax.set_xlabel("Decade of publication (each dot is one book)", color="#4A4540")
ax.legend(loc="upper left", frameon=False, ncol=2, handletextpad=0.3, columnspacing=1.2)
save(fig, "fig5-books.svg")
