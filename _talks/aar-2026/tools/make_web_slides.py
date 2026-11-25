"""
make_web_slides.py
==================
Makes the WEBSITE copy of the deck: talks/aar-2026/slides.html.

The deck in slides/index.html is the one used at the podium. It has a
presenter window (key P) that shows the speaker notes: the podium text with
slide cues and timings. The public copy should show the slides only, so this
script takes slides/index.html and

  1. empties every <aside class="notes">…</aside> block, so the speaker notes
     are not in the public file at all (not just hidden);
  2. disables the P key, so the presenter window cannot be opened;
  3. removes "P presenter view" from the on-screen key hint.

Everything else (slides, animations, arrows, F for full screen) is unchanged.
slides/index.html itself is never modified.

Run after rebuilding the deck (slides/build.py):
    python3 tools/make_web_slides.py        (from any directory)

The script stops with an error if any of the three edits finds nothing to
change, which would mean the deck's code changed and this script needs updating.
"""
import pathlib
import re

TALK = pathlib.Path(__file__).resolve().parent.parent           # _talks/aar-2026
SRC = TALK / "slides" / "index.html"                            # podium deck (read only)
OUT = TALK.parent.parent / "talks" / "aar-2026" / "slides.html"  # website copy

page = SRC.read_text(encoding="utf-8")

# 1. Speaker notes: keep the empty <aside> so the deck's script still finds
#    the element it expects, but drop its content.
page, n_notes = re.subn(r'(<aside class="notes">).*?(</aside>)', r"\1\2", page, flags=re.S)

# 2. The P key. In the deck's keydown handler this is the line
#       else if (k === "p" || k === "P") openPresenter();
#    It is replaced by a comment, so P does nothing.
page, n_key = re.subn(r'else if \(k === "p" \|\| k === "P"\) openPresenter\(\);',
                      '/* P (presenter window) is disabled in the website copy */', page)

# 3. The key hint shown at the bottom of the screen.
page, n_hint = re.subn(r" · P presenter view", "", page)

for what, n in (("speaker notes", n_notes), ("P key handler", n_key), ("P in the key hint", n_hint)):
    if n == 0:
        raise SystemExit(f"make_web_slides.py: found no {what} to change in {SRC}; check the deck's code.")

OUT.write_text(page, encoding="utf-8")
print(f"wrote {OUT}  ({n_notes} note blocks emptied, P key disabled)")
