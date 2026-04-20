---
title: Evaluation Paradigms
description: The three evaluation paradigms used in this project — pairwise comparison, pointwise scoring, and reference-guided scoring — and how they are combined.
---

# Evaluation Paradigms

Three main paradigms dominate the human LLM evaluation literature. This project uses a hybrid of all three, assigning each paradigm to the rubric dimensions where it is best suited.

## Pairwise Comparison

Two LLM responses to the same prompt are shown side by side. Human judges select the better response or declare a tie. This approach is sensitive to subtle quality differences and produces high inter-annotator agreement because the task is comparative rather than absolute.

**Used in this project for**: overall model ranking (Elo-style tournament across models), and as a calibration check on pointwise scores.

## Pointwise Scoring (Likert Scales)

A single response is rated on a 1–5 scale along each rubric dimension independently. This allows fine-grained comparison across models, questions, and figures, and produces data suitable for quantitative analysis.

**Used in this project for**: all seven rubric dimensions (see [](rubric)).

## Reference-Guided Scoring

Annotators compare an LLM response against a gold-standard reference answer prepared by domain experts. The reference provides a shared factual baseline and reduces the burden on annotators who may not independently know the correct answer.

**Used in this project for**: Factual Accuracy, Source Awareness, and Anachronism dimensions. Reference answers for all 42 questions are prepared in advance by the project team and validated against peer-reviewed scholarship.

## Why a Hybrid Approach?

{cite}`zheng2023judging` introduced the LLM-as-judge paradigm and demonstrated that pairwise comparison achieves the highest consistency with human preference rankings — but pairwise comparison alone does not produce the dimension-level scores needed to diagnose *where* a model fails. {cite}`liu2023geval` addressed this by proposing G-Eval, a rubric-based pointwise scoring framework using chain-of-thought reasoning, which achieves better correlation with human judgments than older string-overlap metrics. The hybrid design here draws on both: pairwise comparison for overall model ranking, and pointwise Likert scoring for per-dimension diagnosis.

Reference-guided scoring is added as a third component because the domain-expert knowledge required to evaluate responses on Factual Accuracy, Anachronism, and Source Awareness cannot be assumed of all annotators. Gold-standard reference answers reduce annotator burden and improve reliability on dimensions where the correct answer is determinable from the historical record. {cite}`wang2024survey` provides a comprehensive survey of this combined methodology as of 2024.

```{note}
A key constraint on this project: LLM-as-judge pipelines are not used for the **Gender Bias** dimension.
An LLM judge evaluating another model's treatment of Macrina may reproduce the same androcentric
gaps as the system under evaluation. Human adjudication by domain experts is required for this dimension.
```
