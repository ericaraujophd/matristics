---
title: Data Collection
description: Tutorials for collecting LLM responses via API for each model under evaluation.
---

# Data Collection

This section provides step-by-step tutorials for querying each LLM via its API and storing responses in the format required for annotation. Each tutorial is a Jupyter notebook that can be run locally or in Google Colab.

## Models Under Evaluation

| Model | Provider | API | Tutorial |
|-------|----------|-----|----------|
| Claude (claude-opus-4, claude-sonnet-4) | Anthropic | Anthropic API | [](claude) |
| GPT-4o, GPT-4 | OpenAI | OpenAI API | [](openai) |
| Gemini 1.5 Pro / 2.0 | Google | Google AI API | [](gemini) |
| Grok-2 | xAI | xAI API | [](grok) |

## Batch Collection

Once individual API connections are set up, the [](batch-collection.ipynb) notebook runs the full question bank across all models systematically, handling rate limits, logging errors, and saving responses in a consistent JSON format ready for annotation.

## Before You Begin

See [](setup) for environment setup, API key management, and the response storage format.

## Data Format

All responses are stored as JSON with the following structure:

```json
{
  "question_id": "Q19",
  "model": "claude-opus-4-6",
  "model_version": "claude-opus-4-6-20250514",
  "prompt": "Who was Macrina the Younger and what was her relationship...",
  "response": "...",
  "temperature": 0.0,
  "timestamp": "2026-04-19T16:00:00Z",
  "tokens_used": 412
}
```

Using `temperature: 0.0` across all models ensures deterministic responses for replication.
