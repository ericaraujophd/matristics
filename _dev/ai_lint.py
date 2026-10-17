#!/usr/bin/env python3
"""
ai_lint.py: mechanical pass of the Matristics writing rubric.

WHAT IT DOES
    Scans every .qmd page in the site and counts the Section A surface
    markers defined in _dev/writing-rubric.md (em dashes, stock vocabulary,
    signposting filler, negation pivots, bold lead-in bullets, colon
    reveals, hedge stacks). It prints one row per page with the raw counts,
    the rubric points for each marker, and the Section A total.

    Section B of the rubric (rhythm, aphoristic closers, inflated stakes,
    and so on) needs a human reader and is NOT scored here.

USAGE
    python3 _dev/ai_lint.py              # summary table for all pages
    python3 _dev/ai_lint.py --show       # also print every flagged line
    python3 _dev/ai_lint.py page.qmd     # restrict to specific files

WHAT IS EXCLUDED FROM SCORING (on purpose)
    - YAML front matter (between the first pair of '---' lines)
    - fenced code blocks (``` ... ```), including ```{=html} raw blocks,
      because markup and code are not prose
    - blockquotes (lines starting with '>'), because on this site they
      hold quotations from sources and model outputs, which are evidence
    - inline code (`...`)
    - HTML comments
    En dashes (–) are never counted: they are the correct mark for ranges
    such as "c. 327–379 CE".
"""

import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Marker definitions. Each is a list of regular expressions; every match
# counts once. Patterns are case-insensitive. Word boundaries (\b) keep
# "crucially" from matching inside unrelated words.
# ---------------------------------------------------------------------------

STOCK_WORDS = [
    r"\bdelv(e|es|ing)\b", r"\btapestr(y|ies)\b", r"\blandscape\b",
    r"\brealm\b", r"\bnuanced\b", r"\bmultifaceted\b", r"\bpivotal\b",
    r"\bcrucial(ly)?\b", r"\brobust(ly)?\b", r"\bleverag(e|es|ing)\b",
    r"\bunderscor(e|es|ing)\b", r"\bshowcas(e|es|ing)\b",
    r"\bfoster(s|ing)?\b", r"\bnavigat(e|es|ing)\b", r"\bintricate\b",
    r"\bholistic\b", r"\btestament to\b", r"\bserves as\b",
    r"\bseamless(ly)?\b", r"\bpowerful\b", r"\bvibrant\b",
]

SIGNPOSTS = [
    r"\bit is worth noting\b", r"\bit's worth noting\b",
    r"\bworth dwelling on\b", r"^\s*importantly,", r"\bnotably,",
    r"\bit should be noted\b", r"\bin conclusion\b", r"^\s*ultimately,",
    r"\bin essence\b", r"\bat its core\b", r"\bin other words\b",
]

NEGATION_PIVOTS = [
    r"\bnot only\b.{0,80}\bbut( also)?\b",
    r"\bis not [^.;]{1,60}[,;] but\b",
    r"\bnot [^.;]{1,40}, but\b",
    r"\bnot [^.]{1,60}\. (it|this|they) (is|are)\b",
    r"\bless [a-z]+ than\b",
]

COLON_REVEALS = [
    r"\bthe result[:?]", r"\bthe answer[:?]", r"\bhere'?s the thing\b",
    r"\bthe catch[:?]", r"\bthe upshot[:?]", r"\bthe short version[:?]",
]

HEDGES = [r"\bmay\b", r"\bmight\b", r"\bcould\b", r"\bperhaps\b",
          r"\bpossibly\b", r"\bpotentially\b", r"\barguably\b",
          r"\bseems?\b", r"\bplausibly\b", r"\bsomewhat\b"]

# A bullet that opens with **bold text** followed by '.' or ':' (inside or
# just after the bold) is a "bold lead-in". Two or more consecutive such
# bullets make one bold lead-in list.
BOLD_LEAD = re.compile(r"^\s*[-*+]\s+\*\*[^*]+[.:]?\*\*[.:]?\s")

# ---------------------------------------------------------------------------
# Rubric thresholds (see writing-rubric.md, Section A). Each entry maps a
# marker to (limit for 0 points, limit for 1 point); anything above the
# second limit earns 2 points. "per_k" means the count is normalised per
# 1,000 words before comparing.
# ---------------------------------------------------------------------------

THRESHOLDS = {
    "A1 em dash":      (1, 4, True),
    "A2 stock words":  (1, 3, True),
    "A3 signposts":    (0, 2, False),
    "A4 neg. pivots":  (1, 3, False),
    "A5 bold lists":   (0, 1, False),
    "A6 colon reveal": (0, 1, False),
    "A7 hedge stacks": (0, 2, False),
}


def prose_lines(text):
    """Yield (line_number, line) for lines that count as prose.

    A small state machine walks the file once: it skips front matter,
    fenced blocks, and HTML comments, and drops blockquotes. Line numbers
    are 1-based so they match an editor.
    """
    lines = text.splitlines()
    i = 0
    # Front matter: only if the very first line is '---'.
    if lines and lines[0].strip() == "---":
        i = 1
        while i < len(lines) and lines[i].strip() != "---":
            i += 1
        i += 1
    in_fence = False
    in_comment = False
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
        elif in_fence:
            pass
        elif "<!--" in stripped and "-->" not in stripped:
            in_comment = True
        elif in_comment:
            if "-->" in stripped:
                in_comment = False
        elif stripped.startswith(">"):
            pass  # quotation: evidence, not our prose
        else:
            # Remove inline code so `--` in code spans is ignored.
            yield i + 1, re.sub(r"`[^`]*`", "", line)
        i += 1


def count(patterns, line):
    """Total matches of any pattern in the list on one line."""
    return sum(len(re.findall(p, line, flags=re.I)) for p in patterns)


def points(name, raw, words):
    """Convert a raw count into 0, 1 or 2 rubric points."""
    zero_max, one_max, per_k = THRESHOLDS[name]
    value = raw * 1000 / max(words, 1) if per_k else raw
    if value <= zero_max:
        return 0
    if value <= one_max:
        return 1
    return 2


def lint(path, show=False):
    text = path.read_text(encoding="utf-8")
    counts = {k: 0 for k in THRESHOLDS}
    flagged = []
    words = 0
    bold_run = 0  # consecutive bold lead-in bullets seen so far

    for n, line in prose_lines(text):
        words += len(re.findall(r"\b\w+\b", line))
        hits = []

        dashes = line.count("—")
        if dashes:
            counts["A1 em dash"] += dashes
            hits.append(f"em dash x{dashes}")
        for key, pats in (("A2 stock words", STOCK_WORDS),
                          ("A3 signposts", SIGNPOSTS),
                          ("A4 neg. pivots", NEGATION_PIVOTS),
                          ("A6 colon reveal", COLON_REVEALS)):
            c = count(pats, line)
            if c:
                counts[key] += c
                hits.append(f"{key.split(' ', 1)[1]} x{c}")

        # Hedge stacks: split into sentences and look for 2+ hedges in one.
        for sentence in re.split(r"(?<=[.!?])\s+", line):
            if count(HEDGES, sentence) >= 2:
                counts["A7 hedge stacks"] += 1
                hits.append("hedge stack")

        # Bold lead-in lists: count a list once, when its 2nd item appears.
        if BOLD_LEAD.match(line):
            bold_run += 1
            if bold_run == 2:
                counts["A5 bold lists"] += 1
                hits.append("bold lead-in list")
        elif line.strip():
            bold_run = 0

        if hits:
            flagged.append((n, ", ".join(hits), line.strip()))

    pts = {k: points(k, v, words) for k, v in counts.items()}
    if show and flagged:
        print(f"\n== {path} ==")
        for n, what, line in flagged:
            print(f"  {n:>4}  [{what}]  {line[:110]}")
    return words, counts, pts


def main(argv):
    show = "--show" in argv
    targets = [Path(a) for a in argv if not a.startswith("--")]
    root = Path(__file__).resolve().parent.parent
    if not targets:
        # Skip build output and tooling folders, but DO include
        # report/_sections/, which holds most of the site's prose.
        skip = ("_site", "_dev", "_includes", ".quarto", ".git")
        targets = sorted(p for p in root.rglob("*.qmd")
                         if p.relative_to(root).parts[0] not in skip)
    rows = []
    for p in targets:
        words, counts, pts = lint(p, show)
        rows.append((str(p.relative_to(root) if p.is_absolute() else p),
                     words, counts, pts))

    short = [k.split(" ")[0] for k in THRESHOLDS]
    print(f"\n{'page':34} {'words':>6}  " +
          "  ".join(f"{s:>6}" for s in short) + "   A-total")
    for name, words, counts, pts in rows:
        cells = "  ".join(f"{counts[k]:>3}/{pts[k]}" + " " for k in THRESHOLDS)
        print(f"{name:34} {words:>6}  {cells}   {sum(pts.values()):>3}")
    print("\nCells are raw count / rubric points. Section B is scored by hand.")


if __name__ == "__main__":
    main(sys.argv[1:])
