---
title: Inter-Annotator Agreement Metrics
description: How inter-annotator reliability is measured and reported in this project.
---

# Inter-Annotator Agreement Metrics

Measuring annotator reliability is a core validity requirement, not an optional step. This page describes the metrics used, how to interpret them, and how they are reported.

## Krippendorff's Alpha (α)

Krippendorff's alpha ({cite}`krippendorff2011agreement`) is the primary metric for this project. It is preferred over Cohen's kappa because:

- It handles **any number of annotators** (this project uses three or more).
- It is appropriate for **ordinal scales** (the 1–5 Likert scales used in the rubric), treating a disagreement between scores of 1 and 5 as worse than a disagreement between 3 and 4.
- It can be calculated even with **missing data** (if an annotator is unable to score a particular item).

**Interpretation:**

| Alpha | Interpretation |
|-------|----------------|
| α < 0.20 | Slight agreement — unusable |
| 0.20 – 0.40 | Fair agreement |
| 0.40 – 0.60 | Moderate agreement |
| 0.60 – 0.80 | Substantial agreement — minimum threshold for this project |
| 0.80 – 1.00 | Near-perfect agreement |

## Cohen's Kappa (κ)

Cohen's kappa is reported as a supplementary metric for pairs of annotators on categorical judgements (e.g., the binary evasive/non-evasive coding). It is not the primary metric because it is limited to two annotators.

## Spearman's Rank Correlation

Spearman's rank correlation is used as a cross-check when comparing annotator pairs on Likert-scale dimensions. It does not assume interval spacing and is therefore more appropriate than Pearson's r for ordinal data.

## Reporting Standards

All agreement statistics are reported **per dimension**, not only as aggregates. A project that reports only an overall alpha may obscure the fact that raters agree well on Factual Accuracy but disagree substantially on Gender Bias — a distinction that is central to this project's research questions.

Agreement is also reported **per figure** for the Macrina and Olympias items, to identify whether certain questions or figures are inherently harder to evaluate consistently.

## Calculation

<!-- TODO: Add Python code snippet showing how to calculate Krippendorff's alpha
using the krippendorff package, with example input format. -->
