#!/usr/bin/env python3
"""
build_benchmark_data.py: turn the scoring workbook into the data file that
drives the interactive charts on the Benchmark page.

WHY THIS SCRIPT EXISTS
    The Benchmark page draws radar profiles, a leaderboard and a heatmap in
    the browser. Those charts need numbers, but the annotation dataset itself
    (every individual rating, annotator by annotator) is NOT yet public; see
    the "Data release" note on the Data Collection page. So this script
    reads the private workbook and writes out ONLY aggregates:

        - per model: overall mean, mean per rubric dimension, mean per
          figure, mean per dimension *within* each figure, false-premise
          results, and tag counts
        - per model and question: the mean over both annotators' four
          dimension scores (that is, 2 annotators x 4 dimensions = 8 numbers
          averaged into one)
        - per question: its text, figure, difficulty, flags, and field mean

    No annotator identity and no individual rating leaves this script.

USAGE
    python3 _dev/build_benchmark_data.py path/to/Scoring_Template.xlsx

    Export the Google Sheet "Scoring Template" as .xlsx first (File >
    Download > Microsoft Excel). The script reads the sheets "Raw Data" and
    "Question Bank". It writes benchmark/benchmark-data.js, which the
    Benchmark page loads with a plain <script> tag (a .js file rather than
    .json so the page also works when opened straight from disk, where
    browsers block fetch()).

WHEN TO RE-RUN
    Every time scores change or a new figure is added. Commit the regenerated
    benchmark-data.js; never edit it by hand.
"""

import json
import sys
from pathlib import Path

import pandas as pd

# The four rubric dimensions, as they are spelled in the workbook columns,
# paired with the short keys used in the JavaScript.
DIMS = {
    "Historical Accuracy": "HA",
    "Coverage": "COV",
    "Framing and Agency": "FA",
    "Epistemic Quality": "EQ",
}

# The workbook uses short model labels. The site shows the full product
# name and provider. ORDER MATTERS: it is the fixed order models appear in
# selectors, so a model's position never depends on its rank.
MODELS = [
    ("Claude",   "Claude Sonnet 5",  "Anthropic"),
    ("ChatGPT",  "GPT-5.5",          "OpenAI"),
    ("Gemini",   "Gemini 3.5 Flash", "Google"),
    ("Grok",     "Grok 4.5",         "xAI"),
    ("DeepSeek", "DeepSeek v4 Pro",  "DeepSeek"),
    ("GLM",      "GLM 5.2",          "Z.ai"),
]

FIGURES = {"Macrina the Younger": "M", "Olympias of Constantinople": "O"}

# Tag columns hold typed error tags such as "source-conflation"; "N/A" and
# blanks mean no tag.
TAG_COLS = ["HA Tag 1", "HA Tag 2", "HA Tag 3", "EQ Tag 1", "EQ Tag 2"]


def r2(x):
    """Round for display; None stays None so JSON gets null, not NaN."""
    return None if pd.isna(x) else round(float(x), 3)


def qsort_key(qid):
    """Sort M1, M2, ..., M18, O1, ... numerically within each figure."""
    return (qid[0], int(qid[1:]))


def main(xlsx):
    raw = pd.read_excel(xlsx, sheet_name="Raw Data")
    bank = pd.read_excel(xlsx, sheet_name="Question Bank")

    # Scores arrive as numbers or strings; coerce, so a stray blank (there
    # is one missing Coverage score) becomes NaN and is skipped by mean().
    for col in DIMS:
        raw[col] = pd.to_numeric(raw[col], errors="coerce")
    # A rating's overall score = mean of its four dimensions. This is the
    # same definition as the workbook's "Average Score" column.
    raw["overall"] = raw[list(DIMS)].mean(axis=1)

    questions = []
    for _, q in bank.sort_values("Question ID", key=lambda s: s.map(qsort_key)).iterrows():
        qid = q["Question ID"]
        rows = raw[raw["Question ID"] == qid]
        questions.append({
            "id": qid,
            "figure": FIGURES[q["Figure"]],
            "category": q["Category"],
            "difficulty": q["Difficulty"],
            "flagged": str(q["Bias-Probe / Adversarial Flag"]).strip().upper() == "Y",
            "text": q["Question"],
            "mean": r2(rows["overall"].mean()),
        })

    # The five false-premise items (see benchmark page, "Adversarial").
    premise_ids = ["M11", "M16", "O11", "O16", "O17"]

    models = []
    for key, name, provider in MODELS:
        m = raw[raw["Model"] == key]
        tags = {}
        for col in TAG_COLS:
            for t in m[col].dropna().astype(str):
                t = t.strip().strip("[]")
                if t and t.upper() != "N/A":
                    tags[t] = tags.get(t, 0) + 1
        prem = m[m["Question ID"].isin(premise_ids)]
        models.append({
            "key": key,
            "name": name,
            "provider": provider,
            "overall": r2(m["overall"].mean()),
            "dims": {k: r2(m[c].mean()) for c, k in DIMS.items()},
            "figures": {f: r2(m[m["Figure"] == full]["overall"].mean())
                        for full, f in FIGURES.items()},
            # Mean of each dimension within each figure: 8 numbers, used
            # by the "dimension x figure" radar.
            "dimFig": {f"{k}-{f}": r2(m[m["Figure"] == full][c].mean())
                       for full, f in FIGURES.items() for c, k in DIMS.items()},
            "premise": {
                "corrected": int((prem["Response-Level Tag"].astype(str)
                                  .str.contains("false-premise", case=False)).sum()),
                "of": int(len(prem)),
                "mean": r2(prem["overall"].mean()),
            },
            "tags": tags,
            "perQuestion": {q["id"]: r2(m[m["Question ID"] == q["id"]]["overall"].mean())
                            for q in questions},
            "n": int(len(m)),
        })

    field = {
        "overall": r2(raw["overall"].mean()),
        "dims": {k: r2(raw[c].mean()) for c, k in DIMS.items()},
        "dimFig": {f"{k}-{f}": r2(raw[raw["Figure"] == full][c].mean())
                   for full, f in FIGURES.items() for c, k in DIMS.items()},
    }

    data = {
        "generated": pd.Timestamp.now().strftime("%Y-%m-%d"),
        "ratings": int(len(raw)),
        "responses": int(len(raw) // 2),
        "dimensions": [{"key": k, "name": c.replace(" and ", " & ")} for c, k in DIMS.items()],
        "figures": [{"key": f, "name": full} for full, f in FIGURES.items()],
        "questions": questions,
        "models": models,
        "field": field,
    }

    out = Path(__file__).resolve().parent.parent / "benchmark" / "benchmark-data.js"
    out.write_text(
        "// GENERATED by _dev/build_benchmark_data.py. Do not edit by hand.\n"
        "// Aggregates only: no individual ratings or annotator identities.\n"
        "window.MATRISTICS = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n",
        encoding="utf-8",
    )
    print(f"wrote {out} ({len(models)} models, {len(questions)} questions)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
