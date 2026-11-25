# The Future of the Past (AAR 2026)

Eric Araújo, Calvin University.
AAR Annual Meeting, Denver, History of Christianity Unit, session A23-217,
Monday 23 November 2026, 12:30–2:30 pm, Colorado Convention Center, Room 507.

This folder holds everything for the conference paper: the reading text, the
slide deck, the scripts that build them, and the small catalogue study used on
slide 17.

The folder name starts with an underscore on purpose. Quarto skips files and
folders whose names start with `_`, so nothing here is rendered into the
Matristics website. The public version of the talk lives in `talks/aar-2026/`
(see "On the website" below).

## What to open

| File | What it is |
|---|---|
| `slides/index.html` | **The deck.** One self-contained file (fonts, images and speaker notes are embedded), so it runs offline in any browser. |
| `AAR2026_Araujo_slides_backup.pdf` | All 22 slides as a PDF, for a machine where the HTML will not open. |
| `AAR2026_Araujo_paper.pdf` | Large-type reading copy with slide and 15-minute markers. |
| `AAR2026_Araujo_paper_print.docx` | Printable reading copy for black-and-white printing (15.5 pt, about 15 pages; black bar at every slide change, bold → CLICK lines, grey-tinted 15-minute cuts). Built by `tools/make_docx.js`. |
| `AAR2026_Araujo_paper.md` | The source of the paper. Edit this one. |

### Presenting from `slides/index.html`

| Key | Action |
|---|---|
| → / Space | next build or slide |
| ← | back |
| **P** | open the presenter window (paper text, current passage marked in red, timer, target time, next slide) |
| **M** (in the presenter window) | 15-minute mode: hides the cut passages and shows the 15-minute targets |
| **+ / −** (in the presenter window) | text size |
| click the timer | restart it |

Put the projector on an extended display, keep the presenter window on the
laptop screen, and the deck on the projector.

## How the pieces fit together

```
AAR2026_Araujo_paper.md ──(tools/retime.py)──► slide times and 15-min times written back into the markers
        │
        └─(tools/make_outputs.py)──► AAR2026_Araujo_paper.pdf  (reading copy)
                                 └─► slides/script.md          (speaker notes, one section per slide)

slides/template.html + slides/script.md + slides/fonts, fan, logos, images
        │
        └─(slides/build.py)──► slides/index.html  (the single-file deck)
```

### Markers in the paper

* `**[Slide n · m:ss · 15 min: m:ss]**` means advance to slide *n*. The two times
  say where you should be in the 20-minute and 15-minute versions.
* `**[click]**` means advance a build on the same slide.
* Text between `**[15 min: skip ▼]**` and `**[15 min: resume ▲]**` is left out of
  the 15-minute version. Slide 18 (the invented conspiracy) is skipped entirely
  in the 15-minute version.

### Rebuilding

```
cd _talks/aar-2026
python3 tools/retime.py        # recompute the times in the markers (136 words per minute, plus pauses)
python3 tools/make_outputs.py  # reading PDF and slides/script.md
cd slides && python3 build.py  # slides/index.html
```

Notes on the scripts:

* All three scripts find their files relative to their own location, so they
  run from any directory.
* `tools/make_outputs.py` needs `pandoc` and Python Playwright with Chromium
  (`pip install playwright && playwright install chromium`). The reading copy
  uses the fonts in `tools/fonts/`. It leaves an intermediate `paper.html`,
  which is ignored by git.
* `tools/make_outputs.py` takes the slide titles from the current
  `slides/script.md`, so rename a slide there (the `## [Slide n] Title` line)
  before regenerating.
* The backup PDF is made from screenshots of each slide (Playwright, 1920×1080),
  not by a script kept here.

## On the website (`talks/aar-2026/`)

The site has a Talks page (navbar → Talks) with this talk at
`talks/aar-2026/index.html`: the deck embedded, buttons for the PDFs, and the
paper as a web page.

| File in `talks/aar-2026/` | What it is | Made by |
|---|---|---|
| `_paper.md` | **Reader edition** of the paper: no slide cues, the full 20-minute text, figures and tables where the audience saw the screen. Edit this one for the web and reader PDF. | by hand, from `AAR2026_Araujo_paper.md` |
| `figures/fig1…fig5.svg` | The five result charts | `tools/make_figures.py` |
| `Araujo_AAR2026_The_Future_of_the_Past.pdf` | Reader PDF (11 pages) | `tools/make_reader.py` |
| `slides.html` | Website copy of the deck: speaker notes removed, P (presenter window) disabled | `tools/make_web_slides.py` |
| `Araujo_AAR2026_slides.pdf` | Copy of `AAR2026_Araujo_slides_backup.pdf` | `cp` |
| `index.qmd` | The talk page; includes `_paper.md` | by hand |

Rebuild the website copies:

```
cd _talks/aar-2026
python3 tools/make_figures.py   # needs matplotlib, fonttools, brotli
python3 tools/make_reader.py    # needs pandoc and Playwright (Chromium)
python3 tools/make_web_slides.py  # slides.html without notes or presenter window
cp AAR2026_Araujo_slides_backup.pdf ../../talks/aar-2026/Araujo_AAR2026_slides.pdf
```

`AAR2026_Araujo_paper.md` stays the podium text. A change to the argument has to
be made in both files.

## Slide 17: the catalogue count (`biblio/`)

Slide 17 ("Most of the books are recent") plots one dot per book about Macrina
or Olympias, stacked by decade.

* `biblio/collect.py` queries three open sources (Open Library, Internet Archive,
  Crossref) and keeps records whose title or subjects name the woman. It writes
  `records.csv`.
* `biblio/count.py` removes noise found by reading every record (yearbooks, a
  bakery cookbook, Greek titles where *makrina* means "far away", the same
  edition catalogued twice), classifies each book as an edition of an ancient
  text or a study, and writes `books_clean.csv` (48 books) and `decades.csv`.
* The publication years in `slides/build.py` (`BOOK_YEARS`) are copied from
  `books_clean.csv`.

Limits: open catalogues undercount (few European or pre-1800 books, no
articles). WorldCat would be fuller. Treat the chart as a sketch, not a census.

## Sources of the images

* `slides/macrina.jpg`, `slides/olympias.jpg`, `slides/fan/*`: portraits from
  the Matristics website.
* `slides/fan/chrysostom.webp`: the "photobomber" on slides 3 and 13.
* `slides/logos/*`: the three model logos on slides 2 and 20, supplied by Eric.
  They belong to OpenAI, Anthropic and Google.
