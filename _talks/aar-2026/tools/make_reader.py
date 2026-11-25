"""
make_reader.py
==============
Builds the READER PDF of the AAR 2026 paper: the version for people who read
it rather than hear it. No slide cues, the full 20-minute text, and figures
where the audience saw charts on the screen.

Input
    talks/aar-2026/_paper.md          the reader text (also included by the web page)
    talks/aar-2026/figures/*.svg      drawn by tools/make_figures.py (run that first)
    _talks/aar-2026/tools/fonts/      Libre Baskerville (text) and Public Sans (labels)

Output
    talks/aar-2026/Araujo_AAR2026_The_Future_of_the_Past.pdf
    (the website links to it; Quarto copies it to the site because index.qmd links to it)

How it works
    1. pandoc turns the Markdown into an HTML fragment (body only).
    2. That fragment is wrapped in a page with our own title block and CSS
       (the CSS is in READER_CSS below; fonts are embedded as base64 so the
       page does not depend on anything installed).
    3. Headless Chromium (Playwright) prints the page to a Letter-size PDF,
       with the page number and a short running title in the footer.

Needs: pandoc, and Python Playwright with Chromium
       (pip install playwright && playwright install chromium).

Run:   python3 tools/make_reader.py        (from any directory)
"""
import base64
import pathlib
import re
import subprocess

# --------------------------------------------------------------------------
# Paths, relative to this file so the script runs from any directory.
# --------------------------------------------------------------------------
TALK = pathlib.Path(__file__).resolve().parent.parent          # _talks/aar-2026
REPO = TALK.parent.parent                                      # repository root
WEB = REPO / "talks" / "aar-2026"                              # website folder
SRC = WEB / "_paper.md"
PDF = WEB / "Araujo_AAR2026_The_Future_of_the_Past.pdf"
HTML = TALK / "reader.html"            # intermediate file, ignored by git (see .gitignore)
FONTS = TALK / "tools" / "fonts"

TITLE = "The Future of the Past"
SUBTITLE = "Evaluating Large Language Model Reliability in Early Christian Historical Studies"
AUTHOR = "Eric Araújo"
AFFIL = "Calvin University · eric.araujo@calvin.edu"
VENUE = "AAR Annual Meeting · Denver · 23 November 2026"

# --------------------------------------------------------------------------
# 1. Markdown -> HTML fragment.
#    The HTML comment at the top of _paper.md (notes for maintainers) is
#    dropped first so it does not end up in the page source.
#    "-implicit_figures" is NOT used: an image alone in a paragraph becomes a
#    <figure> with a <figcaption>, which is what we want.
# --------------------------------------------------------------------------
md = SRC.read_text()
md = re.sub(r"<!--.*?-->", "", md, count=1, flags=re.S)
body = subprocess.run(
    ["pandoc", "-f", "markdown", "-t", "html5", "--wrap=none"],
    input=md, capture_output=True, text=True, check=True).stdout

# The first paragraph (in italics) is the editorial note: give it a class so
# it can be set apart under the title.
body = body.replace("<p><em>This is the paper", '<p class="note"><em>This is the paper', 1)


# --------------------------------------------------------------------------
# 2. Fonts as base64 @font-face rules, so the PDF does not depend on the
#    fonts installed on the machine that builds it.
# --------------------------------------------------------------------------
def face(family, file, weight, style):
    data = base64.b64encode((FONTS / file).read_bytes()).decode()
    return (f"@font-face{{font-family:'{family}';src:url(data:font/woff2;base64,{data}) format('woff2');"
            f"font-weight:{weight};font-style:{style};}}")


FONT_CSS = "".join([
    face("Libre Baskerville", "libre-baskerville-latin-400-normal.woff2", 400, "normal"),
    face("Libre Baskerville", "libre-baskerville-latin-400-italic.woff2", 400, "italic"),
    face("Public Sans", "public-sans-latin-400-normal.woff2", 400, "normal"),
    face("Public Sans", "public-sans-latin-600-normal.woff2", 600, "normal"),
])

# --------------------------------------------------------------------------
# The page design. Black text on white, one accent colour (the same red as
# Macrina in the figures) for headings and rules. Text in Libre Baskerville;
# headings, captions, tables and the title block in Public Sans.
# Sizes are for a Letter page with 1-inch side margins (6.5 in of text).
# --------------------------------------------------------------------------
READER_CSS = """
:root{ --ink:#1E1B18; --mute:#5E5850; --rule:#D9D2C4; --red:#B23A2E; }
html{ font-size:10.4pt; }
body{ margin:0; color:var(--ink); font-family:'Libre Baskerville',Georgia,serif; line-height:1.62;
      -webkit-print-color-adjust:exact; print-color-adjust:exact; }
p{ margin:0 0 .72em; text-align:left; hyphens:auto; orphans:3; widows:3; }
em{ font-style:italic; }
a{ color:inherit; text-decoration:none; border-bottom:1px solid var(--rule); }

/* ---------- title block (first page only) ---------- */
header.tb{ margin:0 0 1.6em; padding-bottom:1.2em; border-bottom:1.5px solid var(--ink); }
header.tb .venue{ font:600 8pt/1 'Public Sans',sans-serif; letter-spacing:.14em; text-transform:uppercase; color:var(--red); }
header.tb h1{ font:400 27pt/1.12 'Libre Baskerville',serif; margin:.45em 0 .2em; letter-spacing:-.01em; }
header.tb .sub{ font:italic 400 12.5pt/1.4 'Libre Baskerville',serif; color:var(--mute); margin:0 0 1.1em; }
header.tb .by{ font:600 9.5pt/1.4 'Public Sans',sans-serif; }
header.tb .by span{ font-weight:400; color:var(--mute); }
p.note{ font-size:.92rem; color:var(--mute); border-left:3px solid var(--red); padding:.1em 0 .1em 1em; margin:0 0 1.6em; }

/* ---------- section headings ---------- */
/* The short red rule above each heading is a background image, not a separate
   box, so it can never be left behind at the bottom of a page. */
h2{ font:600 8.6pt/1.3 'Public Sans',sans-serif; letter-spacing:.12em; text-transform:uppercase; color:var(--red);
    margin:1.9em 0 .7em; padding-top:.75em; break-after:avoid; page-break-after:avoid;
    background:linear-gradient(var(--red),var(--red)) no-repeat 0 0 / 2.2em 1.5px; }

/* ---------- quotation of a model answer ---------- */
blockquote{ margin:1em 0 1.1em; padding:.8em 1.1em; background:#F6F1E7; border-left:3px solid var(--ink); font-size:.95rem; break-inside:avoid; }
blockquote p:last-child{ margin-bottom:0; }
.attrib{ display:block; font:400 7.8pt/1.3 'Public Sans',sans-serif; letter-spacing:.06em; text-transform:uppercase; color:var(--mute); margin-top:.2em; }

/* ---------- figures ---------- */
figure{ margin:1.3em 0 1.5em; break-inside:avoid; page-break-inside:avoid; }
figure img{ width:100%; display:block; }
figcaption{ font:400 8.3pt/1.45 'Public Sans',sans-serif; color:var(--mute); margin-top:.55em; padding-top:.5em; border-top:1px solid var(--rule); }
figcaption strong{ color:var(--ink); font-weight:600; }

/* ---------- tables ---------- */
table{ width:100%; border-collapse:collapse; margin:1.2em 0 1.5em; font:400 8.6pt/1.45 'Public Sans',sans-serif; break-inside:avoid; page-break-inside:avoid; }
caption{ caption-side:bottom; text-align:left; font:400 8.3pt/1.45 'Public Sans',sans-serif; color:var(--mute); padding-top:.55em; }
caption strong{ color:var(--ink); font-weight:600; }
thead th{ text-align:left; font-weight:600; border-top:1.5px solid var(--ink); border-bottom:1px solid var(--ink); padding:.45em .6em .45em 0; }
tbody td{ padding:.38em .6em .38em 0; border-bottom:1px solid var(--rule); vertical-align:top; }
tbody tr:last-child td{ border-bottom:1.5px solid var(--ink); }
td em{ color:var(--mute); }

/* ---------- numbered list (the five questions) ---------- */
ol{ margin:.2em 0 1em; padding-left:1.6em; }
ol li{ margin:.15em 0; font-family:'Public Sans',sans-serif; font-size:9.6pt; }
ol li::marker{ color:var(--red); font-weight:600; }

/* ---------- footnotes and references ---------- */
sup, .footnote-ref{ font-size:.7em; line-height:0; border:0; }
.footnotes{ font-size:8.6pt; color:var(--mute); margin-top:1.4em; }
.footnotes hr{ border:0; border-top:1px solid var(--rule); width:30%; margin:0 0 .6em; }
.footnotes ol li{ font-family:'Libre Baskerville',serif; font-size:8.6pt; }
.footnote-back{ display:none; }
h2.refs ~ p{ font-size:.88rem; padding-left:1.6em; text-indent:-1.6em; margin-bottom:.45em; }
"""

title_block = f"""
<header class="tb">
  <div class="venue">{VENUE}</div>
  <h1>{TITLE}</h1>
  <p class="sub">{SUBTITLE}</p>
  <div class="by">{AUTHOR} <span>· {AFFIL}</span></div>
</header>
"""

# Pandoc puts footnotes at the very end, after the references. Move them to
# sit before the References heading, where a reader expects notes.
foot = re.search(r'<(section|aside)[^>]*id="footnotes".*?</(section|aside)>', body, re.S)   # pandoc 3.1 writes <aside>, later versions <section>
refs = re.search(r'<h2[^>]*class="refs"[^>]*>', body)
if foot and refs:
    body = body.replace(foot.group(0), "")
    body = body.replace(refs.group(0), foot.group(0) + "\n" + refs.group(0), 1)

page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>{TITLE} · {AUTHOR}</title>
<base href="{WEB.as_uri()}/">
<style>{FONT_CSS}{READER_CSS}</style></head>
<body>{title_block}{body}</body></html>"""
HTML.write_text(page)

# --------------------------------------------------------------------------
# 3. Print with Chromium. The footer carries a short running title on the
#    left and the page number on the right (Chromium fills the pageNumber
#    and totalPages spans). Fonts in the footer must be system fonts.
# --------------------------------------------------------------------------
from playwright.sync_api import sync_playwright

FOOTER = ("<div style=\"font-family:Helvetica,Arial,sans-serif;font-size:7.5pt;color:#6E6860;width:100%;"
          "padding:0 1in;display:flex;justify-content:space-between\">"
          f"<span>Araújo · {TITLE} · AAR 2026</span>"
          "<span><span class=\"pageNumber\"></span> / <span class=\"totalPages\"></span></span></div>")

with sync_playwright() as p:
    browser = p.chromium.launch()
    pg = browser.new_page()
    pg.goto(HTML.as_uri())
    pg.wait_for_timeout(600)               # let the embedded fonts and SVGs load
    pg.pdf(path=str(PDF), format="Letter", print_background=True,
           margin={"top": "0.85in", "bottom": "0.9in", "left": "1in", "right": "1in"},
           display_header_footer=True, header_template="<span></span>", footer_template=FOOTER)
    browser.close()
print("wrote", PDF)
