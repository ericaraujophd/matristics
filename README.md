# LLM Evaluation in Early Church History

A research project by **Eric Araujo** (Calvin University) evaluating large language models on their knowledge of women in early Christianity — with a focus on factual accuracy, gender bias, hallucination, and depth of historical understanding.

Live site: **ericaraujo.com/matristics**

---

## Project Proposal

### Research Problem

Large language models are increasingly used as educational tools, research aids, and reference systems. Yet the accuracy, depth, and fairness of their historical knowledge is poorly understood — particularly for domains where the documentary record is sparse, contested, or structurally biased.

Early church history is a revealing test case. The first five centuries of Christian history produced a substantial number of women who led communities, developed theology, wrote texts, exercised prophetic authority, and founded institutions. Most of them remain unknown to a general audience. The surviving record was overwhelmingly produced by men, and the modern scholarly literature on women in this period has undergone significant revision over the past four decades — creating a gap between older popular accounts and current specialist knowledge.

This project asks: **what do LLMs actually know about these women, and what systematic patterns shape what they get wrong?**

### Research Questions

1. How accurately do leading LLMs represent the historical roles of documented female figures in early Christianity?
2. Do LLMs reproduce androcentric framings from their training data — minimizing women's agency, foregrounding male figures, or defaulting to "patron" and "supporter" descriptions where the evidence supports stronger claims?
3. How do LLMs handle epistemic uncertainty in this domain — genuine scholarly debates, contested translations, and questions that intersect with contemporary theological controversy?
4. How does model performance vary across figures with different levels of documentation (well-attested vs. obscure)?
5. How does model performance vary by question difficulty (basic identification, intermediate synthesis, advanced critical analysis)?

### Why This Matters

LLMs trained on the existing web inherit its silences. The Wikipedia gender gap, the dominance of androcentric primary sources in digitized corpora, and the centuries-long tradition of minimizing women's authority in church history all flow into training data — and from there into model outputs. Understanding the magnitude and structure of these gaps is a precondition for addressing them.

This project contributes a domain-specific benchmark with a gender-bias focus, a replicable evaluation methodology, and a public question bank that other researchers can use, extend, or critique.

---

## Methodology Overview

### Models Evaluated

| Model | Provider | API |
|-------|----------|-----|
| Claude (Opus / Sonnet) | Anthropic | `anthropic` Python SDK |
| GPT-4 | OpenAI | `openai` Python SDK |
| Gemini | Google | `google-generativeai` SDK |
| Grok | xAI | OpenAI-compatible, `base_url="https://api.x.ai/v1"` |

All models are queried at `temperature=0.0` with a shared system prompt for replicability.

### Question Bank

42 questions across 14 female figures (3 per figure: Basic / Intermediate / Advanced). Each question is submitted verbatim as a user prompt. Currently active figures: **Macrina the Younger** and **Olympias of Constantinople**.

### Evaluation Rubric

Human domain-expert annotators score each response on 7 dimensions (1–5 Likert scale):

| Dimension | What It Measures |
|-----------|-----------------|
| Factual Accuracy | Correct names, dates, roles, relationships |
| Completeness | Coverage of major aspects of the question |
| Gender Bias | Minimization, erasure, or androcentric framing |
| Hallucination | Invented details presented as fact |
| Anachronism | Projection of later frameworks onto the early period |
| Source Awareness | Distinction between canonical, apocryphal, patristic sources |
| Depth & Nuance | Engagement with scholarly debate and uncertainty |

**Note:** LLM-as-judge is not used for the Gender Bias dimension. An LLM judge may reproduce the same androcentric gaps as the model being evaluated. Human adjudication by domain experts is required for this dimension.

### Annotation Protocol

- Minimum two expert annotators (graduate-level knowledge of patristics or feminist historiography of religion)
- Three phases: onboarding → pilot round (gate: Krippendorff's α ≥ 0.60 on all dimensions) → production
- Each item rated by at least three annotators; responses blinded to model identity

---

## Project Status

| Component | Status |
|-----------|--------|
| Methodology documentation | Complete |
| Question bank (42 questions) | Complete |
| Data collection notebooks (4 models) | Complete |
| Figures: Macrina the Younger | Complete |
| Figures: Olympias of Constantinople | Complete |
| Remaining 12 figures | Planned |
| Data collection (LLM responses) | Not yet started |
| Annotation | Not yet started |
| Benchmark results | Not yet available |

---

## Running the Site Locally

This site is built with [MyST](https://mystmd.org).

**Prerequisites:** Node.js 18+

```bash
# Install MyST
npm install -g mystmd

# From this directory (website/):
myst start        # development server with live reload
myst build        # static build → _build/
```

The site will be available at `http://localhost:3000`.

---

## Repository Structure

```
website/
├── myst.yml                    # Site configuration and table of contents
├── references.bib              # BibTeX bibliography (25 entries, DOIs where available)
├── index.md                    # Home page
├── about.md                    # About the project
├── glossary.md                 # Key terms
├── references.md               # Full bibliography (rendered)
├── _static/
│   └── fractio_panis.jpg       # Header image (Catacomb of Priscilla, 2nd–4th c.)
├── background/
│   ├── historical-context.md   # Women in early Christianity
│   └── llm-evaluation-context.md  # Prior work on LLM evaluation and bias
├── methodology/
│   ├── index.md
│   ├── evaluation-paradigms.md # Pairwise, pointwise, reference-guided scoring
│   ├── rubric.md               # Full 7-dimension rubric with scoring scales
│   ├── annotation-protocol.md  # 3-phase annotation workflow
│   └── agreement-metrics.md    # Krippendorff's alpha, kappa, Spearman
├── biases/
│   ├── index.md
│   ├── hallucination.md        # Hallucination in sparse historical domains
│   ├── androcentric-bias.md    # Training data gender gap
│   └── contested-scholarship.md # Evasive non-answers and contested claims
├── figures/
│   ├── index.md                # Master question bank (all 42 questions)
│   ├── macrina.md              # Macrina the Younger (Q19–Q21)
│   └── olympias.md             # Olympias of Constantinople (Q25–Q27)
├── data-collection/
│   ├── index.md
│   ├── setup.md                # Environment setup
│   ├── claude.ipynb            # Anthropic SDK tutorial
│   ├── openai.ipynb            # OpenAI SDK tutorial
│   ├── gemini.ipynb            # Google Generativeai SDK tutorial
│   ├── grok.ipynb              # xAI API tutorial
│   └── batch-collection.ipynb  # Runs all 4 models, saves JSONL
├── benchmark/
│   ├── index.md
│   ├── by-model.md             # Per-model scores (placeholder)
│   ├── by-dimension.md         # Per-dimension analysis (placeholder)
│   └── by-figure.md            # Per-figure heatmap (placeholder)
└── replicate/
    └── index.md                # Replication instructions
```

---

## Adding a New Figure

1. Create `figures/<name>.md` following the template of `figures/macrina.md`
2. Add three questions (Basic / Intermediate / Advanced) to `figures/index.md` with the next available Q-numbers
3. Add the new file to the `Figures` section in `myst.yml`
4. Add any new bibliography entries to `references.bib` (DOI preferred)

---

## Citation

If you use the question bank, rubric, or methodology from this project, please cite:

> Araujo, Eric. *LLM Evaluation in Early Church History*. 2026. ericaraujo.com/matristics

---

## License

Site content: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Header image (*Fractio Panis*): public domain via [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Catacombe_di_Priscilla,_Rome_-_Fresco_of_a_Christian_Agape_feast_-_Fractio_panis_-_Greek_chapel_-_2nd_-_4th_century.jpg).
