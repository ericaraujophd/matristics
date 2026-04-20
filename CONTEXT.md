# Project Context: LLM Evaluation in Early Church History

This document provides full context for any agent or collaborator picking up work on this project. Read it before touching any file.

---

## What This Project Is

A research project by Eric Araujo (CS faculty, eric.araujo@calvin.edu) that evaluates multiple large language models on their knowledge of **women in early Christianity** (1st–5th centuries CE). The central question is not only whether models are factually accurate, but whether they reproduce the same androcentric silences and distortions that have historically characterized the scholarly record.

The project has three deliverables:

1. **A replicable evaluation methodology** — rubric, annotation protocol, question bank, inter-annotator agreement procedures
2. **A public benchmark** — a panel comparing model performance across figures, rubric dimensions, and question difficulty
3. **A MyST-based website** — where all methodology, data, and results are published so other researchers can replicate or extend the evaluation

---

## Models Under Evaluation

- **Claude** (Anthropic) — via `anthropic` Python SDK
- **ChatGPT / GPT-4** (OpenAI) — via `openai` Python SDK
- **Gemini** (Google) — via `google-generativeai` SDK
- **Grok** (xAI) — via OpenAI-compatible client, `base_url="https://api.x.ai/v1"`

All models are queried at `temperature=0.0` with a shared system prompt to ensure replicability.

---

## The 7-Dimension Evaluation Rubric

Each LLM response is scored 1–5 on seven independent dimensions by domain-expert human annotators:

| # | Dimension | What It Measures |
|---|-----------|-----------------|
| 1 | Factual Accuracy | Correct names, dates, roles, relationships, texts |
| 2 | Completeness | Coverage of major aspects of the question |
| 3 | Gender Bias | Minimization, erasure, or androcentric framing of the female figure |
| 4 | Hallucination | Invented details asserted with confidence |
| 5 | Anachronism | Projection of later frameworks onto the early period |
| 6 | Source Awareness | Distinction between canonical, apocryphal, patristic, hagiographic sources |
| 7 | Depth & Nuance | Engagement with scholarly debates and gaps in the record |

**Critical design note:** LLM-as-judge is not used for the Gender Bias dimension. An LLM judge may reproduce the same androcentric gaps as the model under evaluation. Human domain-expert adjudication is required for this dimension.

**Evasive non-answers:** A response that deflects a historically answerable question about a female figure's role by citing "ongoing theological debate" is scored **2** on Gender Bias (not treated as appropriately cautious hedging).

---

## The Question Bank

42 questions across 14 female figures (3 questions per figure: Basic / Intermediate / Advanced). Currently **two figures are active**; the rest are placeholders waiting for historical research to be conducted.

Each question is submitted verbatim as a user prompt to each model. Questions are assigned IDs (Q1–Q42).

### Active Figures (with full pages)

| Figure | Period | Questions | Page |
|--------|--------|-----------|------|
| Macrina the Younger | c. 327–379 CE | Q19, Q20, Q21 | `website/figures/macrina.md` |
| Olympias of Constantinople | c. 360–408 CE | Q25, Q26, Q27 | `website/figures/olympias.md` |

### Planned Figures (stubs in the question bank index)
Perpetua, Felicitas, Mary Magdalene, Junia, Priscilla, Thecla, Phoebe, Egeria, Melania the Elder, Melania the Younger, Paula, Blandina (and others to be added).

---

## Website: Technical Stack

The website is built with **MyST** (`mystmd.org`), a scientific/academic static site generator.

- **Config:** `website/myst.yml` — site title, author, TOC, bibliography pointer
- **Bibliography:** `website/references.bib` — 25 BibTeX entries, DOIs wherever available
- **Site template:** `book-theme`
- **Build output:** `website/_build/` — do not edit manually

### MyST Syntax Used in This Project

```
{cite}`key`          — inline citation (renders with bibliography)
{doc}`path`          — cross-link to another page
{term}`word`         — link to glossary term
{list-table}         — structured table directive
{note} / {warning}   — admonition callout boxes
{bibliography}       — renders the full reference list (only in references.md)
{glossary}           — defines cross-referenceable terms
```

### Citation Convention

- All citations use `{cite}`key`` roles in the text
- The bibliography is rendered **once only**, in `website/references.md`, using the `{bibliography}` directive
- Do not add `{bibliography}` directives to individual pages — MyST will throw a duplication error
- All `{cite}` keys must exist in `website/references.bib`

---

## Directory Structure

```
LLM + Early Church History/
├── CONTEXT.md                     ← this file
├── literature_review.md           ← literature review (Markdown)
├── literature_review.docx         ← literature review (Word)
├── llm_early_church_history.pdf   ← full website exported to PDF
└── website/
    ├── myst.yml                   ← site config and TOC
    ├── references.bib             ← all bibliography entries
    ├── index.md                   ← site home page
    ├── references.md              ← bibliography page (contains {bibliography})
    ├── about.md                   ← project about page
    ├── glossary.md                ← 15 defined terms
    ├── background/
    │   ├── historical-context.md  ← women in early Christianity (overview)
    │   └── llm-evaluation-context.md  ← prior work on LLM eval and bias
    ├── methodology/
    │   ├── index.md               ← methodology overview
    │   ├── evaluation-paradigms.md  ← pairwise / pointwise / reference-guided
    │   ├── rubric.md              ← full 7-dimension scoring rubric
    │   ├── annotation-protocol.md  ← 3-phase annotation workflow
    │   └── agreement-metrics.md   ← Krippendorff's alpha, kappa, Spearman
    ├── biases/
    │   ├── index.md               ← bias overview
    │   ├── hallucination.md       ← hallucination in sparse historical domains
    │   ├── androcentric-bias.md   ← training data gender gap
    │   └── contested-scholarship.md  ← evasive non-answers, contested claims
    ├── figures/
    │   ├── index.md               ← master question bank (all 42 questions)
    │   ├── macrina.md             ← Macrina the Younger (full page)
    │   └── olympias.md            ← Olympias of Constantinople (full page)
    ├── data-collection/
    │   ├── index.md               ← data collection overview
    │   ├── setup.md               ← environment setup instructions
    │   ├── claude.ipynb           ← Anthropic SDK tutorial notebook
    │   ├── openai.ipynb           ← OpenAI SDK tutorial notebook
    │   ├── gemini.ipynb           ← Google Generativeai SDK tutorial notebook
    │   ├── grok.ipynb             ← xAI (OpenAI-compatible) tutorial notebook
    │   └── batch-collection.ipynb ← runs all 4 models, saves JSONL output
    ├── benchmark/
    │   ├── index.md               ← benchmark overview
    │   ├── by-model.md            ← per-model scores (placeholder)
    │   ├── by-dimension.md        ← per-dimension analysis (placeholder)
    │   └── by-figure.md           ← per-figure heatmap (placeholder)
    └── replicate/
        └── index.md               ← replication instructions
```

---

## Response Data Format

LLM responses are stored as JSONL (one JSON object per line), with the following fields:

```json
{
  "question_id": "Q19",
  "figure": "macrina",
  "model": "claude",
  "model_version": "claude-opus-4-6",
  "prompt": "Who was Macrina the Younger...",
  "response": "...",
  "temperature": 0.0,
  "timestamp": "2026-04-20T12:00:00Z",
  "tokens_used": 512
}
```

---

## Annotation Protocol Summary

- **Minimum two expert annotators** with graduate-level knowledge of early Christianity / patristics / feminist historiography of religion
- **No crowdsourcing** (Mechanical Turk, Prolific) — expert knowledge required
- **Three phases:** Onboarding → Pilot round (gate: Krippendorff's α ≥ 0.60) → Production
- **Each item rated by at least three annotators**; items with score range > 2 points are flagged for re-annotation
- **Annotators are blinded** to which model produced each response

---

## Key Scholarly Sources

The project draws on two bodies of literature:

**LLM Evaluation:**
- Zheng et al. (2023) — MT-Bench / LLM-as-judge paradigm
- Liu et al. (2023) — G-Eval rubric-based scoring framework
- Wang et al. (2024) — survey of LLM-as-judge methods
- Chen et al. (2024) — comprehensive survey of LLM evaluation

**Women in Early Christianity:**
- Cohick & Hughes (2017) — comprehensive survey of female figures, 2nd–5th century
- Madigan & Osiek (2005) — documentary history of ordained women
- Torjesen (1993) — argument for women's priestly leadership pre-Nicaea
- Elm (1994) — female asceticism in late antiquity
- Kraemer & D'Angelo (1999) — feminist historiography of Christian origins
- Clark (1983) — patristic primary sources on women

Full BibTeX in `website/references.bib`.

---

## How to Add a New Figure

1. Create `website/figures/<name>.md` following the template of `macrina.md` or `olympias.md`. Each figure page includes: Historical Profile, Primary Sources (list-table), Scholarly Debates, Evaluation Questions (list-table with Q-numbers), and a Benchmark Results placeholder.
2. Add three questions (Basic / Intermediate / Advanced) to `website/figures/index.md` with the next available Q-numbers.
3. Add the new figure page to the TOC in `website/myst.yml` under the `Figures` section.
4. Add any new bibliography entries to `website/references.bib` with DOI where available.

---

## Current Status (as of April 2026)

| Component | Status |
|-----------|--------|
| Website scaffolding | Complete |
| Methodology pages | Complete (with citations) |
| Bias pages | Complete (with citations) |
| Figures: Macrina | Complete (profile + Q19–Q21 + citations) |
| Figures: Olympias | Complete (profile + Q25–Q27 + citations) |
| Remaining 12 figures | Placeholder entries in question bank |
| Data collection notebooks | Complete (Claude, OpenAI, Gemini, Grok, batch) |
| Benchmark pages | Placeholder — awaiting data collection |
| Actual LLM responses | Not yet collected |
| Annotation | Not yet started |
| Results / benchmark panel | Not yet available |
