---
title: Androcentric Bias
description: How androcentric training data shapes LLM knowledge of women in early Christianity.
---

# Androcentric Bias

LLMs are trained predominantly on web-scraped text. The major sources — Wikipedia, digitized books, academic repositories — systematically underrepresent women as historical agents. In early church history, this structural bias is compounded by the nature of the primary sources themselves. {cite}`navigli2023biases` provides a systematic taxonomy of how bias enters LLMs at every stage of the pipeline, from training data curation through reinforcement learning with human feedback.

## Training Data Sources

**Wikipedia gender gap:** Women in church history have shorter, less detailed Wikipedia articles than their male contemporaries. Wikipedia's historically male editorial workforce (around 90% in most surveys) has direct consequences for the factual density of LLM knowledge about women. A model asked about Basil of Caesarea draws on far richer training material than one asked about his sister Macrina, who arguably shaped his theological development (see {cite}`cohick2017women` for a comprehensive survey of female figures from the second through fifth centuries and the disparity in their documentation).

**Patristic source dominance:** The primary surviving written record of the early church was produced almost entirely by men. LLMs trained on this corpus naturally replicate the perspective embedded in it, including the tendency to treat women's roles as secondary, exceptional, or requiring male authorization.

**Gender-role stereotyping:** {cite}`unesco2023genderai` documents alarming evidence of regressive gender stereotypes in major generative AI systems, and {cite}`kotek2023genderbias` demonstrates that LLMs are 3–6 times more likely to assign occupations stereotypically aligned with a person's gender. In early church history, this manifests as a tendency to describe women primarily as "supporters" or "patrons" rather than as theologians, leaders, or apostles.

**Erasure through omission:** Perhaps the most significant bias is absence. LLMs may fail to mention female figures entirely, or mention them only as appendages to better-documented male figures ("Priscilla, wife of Aquila, who was a colleague of Paul").

## Detecting Androcentric Bias in Evaluation

The Gender Bias dimension of the rubric ([](../methodology/rubric)) is the primary instrument for detecting androcentric bias. The annotation protocol also includes **paired question design**: for each female figure, a parallel question is asked about a male contemporary of equal or lesser historical significance, allowing systematic comparison of response depth and completeness.

<!-- TODO: Add results once data collection is complete. -->
