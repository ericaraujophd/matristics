---
title: LLM Evaluation Context
description: Why evaluating LLMs on early church history is a meaningful research problem, and what prior work exists.
---

# LLM Evaluation Context

Large language models are increasingly used as educational tools, research aids, and reference systems. Understanding the limits of their historical knowledge — and the systematic biases in how that knowledge is distributed — is a research problem with practical consequences.

## Why Early Church History?

Early church history is a particularly revealing test case for several reasons that are developed fully in the [](../biases/index) section:

- The domain has **sparse and contested primary sources**, creating high hallucination risk.
- The textual tradition is **deeply androcentric**: the surviving record was overwhelmingly produced by men.
- The scholarship on women in this period has **undergone significant revision** over the past four decades, creating a gap between older popular accounts and current specialist knowledge.
- Several key questions (women's ordained ministry, apostolic authority) are **theologically contested** in contemporary Christianity, creating pressure on LLMs to avoid or distort historically answerable questions.

## Prior Work on LLM Evaluation

The foundational methodology for this project draws on several key papers. {cite}`zheng2023judging` introduced the LLM-as-judge paradigm and the MT-Bench benchmark, establishing pairwise comparison as a scalable evaluation approach. {cite}`liu2023geval` proposed G-Eval, a rubric-based scoring framework using chain-of-thought reasoning that informs our own dimension rubric. {cite}`wang2024survey` and {cite}`chen2024llmjudges` provide comprehensive surveys of the field as of 2024, covering the strengths and failure modes of automated evaluation.

<!-- TODO: Expand with discussion of:
- General LLM evaluation frameworks (HELM, BIG-Bench, MMLU)
- Domain-specific evaluations (IslamicMMLU, historical knowledge benchmarks)
-->

## Prior Work on LLM Bias

On the bias side, {cite}`unesco2023genderai` documents alarming evidence of regressive gender stereotypes in major generative AI systems. {cite}`kotek2023genderbias` demonstrates that LLMs are 3–6 times more likely to assign occupations stereotypically aligned with a person's gender. {cite}`navigli2023biases` provides a systematic taxonomy of bias origins in large language models, from training data selection through reinforcement learning with human feedback.

<!-- TODO: Expand with discussion of:
- Cultural and religious bias (differential treatment across traditions)
- Historical content hallucination
- The Wikipedia gender gap as a training data problem
-->

## What This Project Adds

<!-- TODO: Articulate the contribution: a domain-specific benchmark for early church history
with a gender-bias focus, a replicable methodology, and a public question bank. -->
