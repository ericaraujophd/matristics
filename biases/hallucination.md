---
title: Hallucination in Historical Content
description: How and why LLMs hallucinate in sparse historical domains, with examples from early church history.
---

# Hallucination in Historical Content

LLMs are trained to produce fluent, coherent text by predicting likely continuations. In sparse or contested historical domains, this mechanism produces "confident hallucination" — responses that sound like historical scholarship but assert invented or misattributed details.

## Common Hallucination Patterns in This Domain

**Biographical invention:** Fabricated birthdates, precise geographic origins, family compositions, or death circumstances for figures whose historical records are fragmentary. Example: a model may invent that Thecla was "born in Iconium in approximately 10 CE" when no such date is documented.

**Anachronistic institutional projection:** Applying later institutional categories to early figures. Example: describing Phoebe as "ordained a deaconess in the formal sense defined by the Council of Chalcedon" when she predates these definitions by four centuries.

**Attribution errors:** Misattributing texts, sermons, or theological positions. Example: Mary Magdalene conflated with the unnamed sinner of Luke 7 — a conflation invented by Pope Gregory I in 591 CE that has been officially corrected by the Roman Catholic Church but persists in some LLM outputs.

**Simplified narratives:** Reproducing the dominant male-centered narrative without acknowledging the substantial scholarly revision of this picture over the past four decades.

## Adversarial Questions in the Question Bank

Several questions in the question bank are designed specifically to invite hallucination — prompts containing a false premise that the model should identify and correct. Example:

> *"Tell me about Egeria's ordination as a deacon."*

The historically accurate answer requires the model to recognize that Egeria's ordained status is not documented — she is documented as a pilgrim and writer, not an ordained minister — and to correct the premise rather than confabulate an ordination narrative.

<!-- TODO: Expand with specific documented hallucination examples from collected responses. -->
