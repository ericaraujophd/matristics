---
title: Annotation Protocol
description: The three-phase annotation workflow, annotator requirements, calibration procedure, and quality control measures.
---

# Annotation Protocol

The quality of human evaluation is only as strong as the annotation protocol. This project follows a three-phase workflow based on best practices from the evaluation literature ({cite}`chen2024llmjudges`).

## Annotator Requirements

**Expert annotators (minimum two):** Graduate-level training in early Christianity, patristics, or feminist historiography of religion. They annotate all items for all seven dimensions.

**Secondary annotators (optional):** Graduate students in history or religious studies, trained on the rubric. May be used for Completeness and Hallucination dimensions after a calibration round.

No crowdsourcing platforms (Mechanical Turk, Prolific) are used for this project. Agreement rates between LLM judges and domain experts drop to 64–68% on expert-knowledge tasks; non-expert crowdsourcing is insufficient for a domain that requires knowledge of patristic literature and feminist historiography.

## Phase 1 — Onboarding

Annotators receive:

1. A copy of the full rubric ({doc}`rubric`) with definitions and scoring examples.
2. A set of **golden standard** examples: five question–response pairs with model scores and written justifications. These establish shared calibration before any live annotation begins.
3. A **reference answer document**: gold-standard answers for all 42 questions, prepared by the project team and validated against peer-reviewed scholarship. Annotators use these as the baseline for Factual Accuracy, Source Awareness, and Anachronism scoring.
4. A brief reading list on early church history covering the figures in the question bank.

## Phase 2 — Pilot Round

Before production annotation begins:

1. All annotators independently score a **pilot set of 10 items** (drawn from the question bank, covering both well-known and lesser-known figures, and all three difficulty levels).
2. Krippendorff's alpha ({cite}`krippendorff2011agreement`) is calculated per dimension.
3. Annotators discuss all disagreements together to identify rubric ambiguities.
4. The rubric is revised if necessary, and a second pilot round is conducted if alpha falls below 0.60 on any dimension.

**Gate**: Production annotation begins only when alpha ≥ 0.60 on all dimensions. An 80% accuracy threshold on known-answer items is also required.

## Phase 3 — Production Annotation

- Each item is rated by **at least three annotators**.
- Consensus is established via **averaged scores** (Likert dimensions).
- **Weekly calibration sessions** review a random sample of 5% of completed items; annotators discuss disagreements and update shared understanding of edge cases.
- Any item where the range of scores across annotators exceeds 2 points on any dimension is flagged for **discussion and re-annotation**.

## Quality Control

<!-- TODO: Add details on:
- Blinding: annotators do not know which model produced a response
- Response randomization: order of model responses is randomized per item
- Fatigue management: maximum items per session
-->
