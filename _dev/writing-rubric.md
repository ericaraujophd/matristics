# Matristics Writing Rubric: AI-Pattern Detection

This rubric checks prose on the Matristics site for the habits that make text read as machine-written. It is a style audit, not a plagiarism or provenance test: it scores what a page *sounds like*, regardless of who or what drafted it. The goal is prose that reads like a careful scholar wrote it for other scholars.

Use it in two passes:

1. **Mechanical pass.** Run `python3 _dev/ai_lint.py` from the repository root. It counts the surface markers in Section A and prints a per-page report. These markers are cheap to detect and cheap to fix.
2. **Reading pass.** Read each page aloud (or close to it) and score Section B by hand. These are the patterns a script cannot see reliably: rhythm, hedging, empty framing.

A page passes when it scores **0 to 4** in total. A score of **5 to 9** means revise the flagged passages. **10 or more** means rewrite the page from the content outward.

---

## Section A. Surface markers (scored by `ai_lint.py`)

Each marker is scored per 1,000 words so long and short pages are compared fairly.

| # | Marker | What it looks like | 0 points | 1 point | 2 points |
|---|--------|--------------------|:-:|:-:|:-:|
| A1 | **Em dashes** | `—` used as an all-purpose connector for asides, lists, and pivots | 0 to 1 per 1k words | 2 to 4 | 5 or more |
| A2 | **Stock vocabulary** | delve, tapestry, landscape, realm, nuanced, multifaceted, pivotal, crucial, robust, leverage, underscore, showcase, foster, navigate, intricate, holistic, testament to, serves as | 0 to 1 per 1k | 2 to 3 | 4 or more |
| A3 | **Signposting filler** | "It is worth noting", "Importantly,", "Notably,", "It should be noted", "In conclusion", "Ultimately,", "In essence", "At its core" | 0 | 1 to 2 | 3 or more |
| A4 | **Negation pivots** | "not X, but Y"; "This is not X. It is Y."; "not only X but also Y"; "less X than Y" | 0 to 1 per page | 2 to 3 | 4 or more |
| A5 | **Bold lead-in bullets** | Bullet lists where every item opens with a bolded phrase and a period or colon, then a sentence restating it | 0 lists | 1 list | 2 or more lists |
| A6 | **Colon reveals** | "The result: ...", "The answer?", "Here's the thing:", "The catch:" | 0 | 1 | 2 or more |
| A7 | **Hedge stacks** | Two or more hedges in one sentence: "may potentially", "could arguably suggest", "seems to perhaps" | 0 | 1 to 2 | 3 or more |

## Section B. Reading-pass patterns (scored by hand)

| # | Pattern | Symptom | 0 points | 1 point | 2 points |
|---|---------|---------|:-:|:-:|:-:|
| B1 | **Triadic rhythm** | Lists of exactly three adjectives, clauses, or examples recurring paragraph after paragraph ("accurate, complete, and fair") | Rare, and only when there really are three | Noticeable on the page | The default shape of most sentences |
| B2 | **Uniform sentence length** | Most sentences run 18 to 25 words; few short ones, few long ones | Varied | Somewhat flat | Metronomic |
| B3 | **Aphoristic closers** | Paragraphs that end on a quotable summary line restating the paragraph ("Silence, in other words, is also data.") | None or one earned line | 2 to 3 | Most paragraphs |
| B4 | **Restating the reader's point** | Telling the reader what they just read, or what a heading already said; recap sentences at the end of short sections | None | Occasional | Systematic |
| B5 | **Inflated stakes** | Claims of significance not supported by the evidence on the page ("a profound demonstration", "the clearest possible evidence") | Claims match evidence | Some overreach | Routine overreach |
| B6 | **Vague attribution** | "Scholars argue", "research shows", "many have noted" with no citation | Every such claim is cited | 1 to 2 uncited | 3 or more |
| B7 | **Generic transitions** | Paragraphs linked by "Moreover", "Furthermore", "Additionally", "In addition" rather than by the argument | Transitions come from content | A few | Most paragraphs |
| B8 | **Symmetric structure** | Every section has the same internal shape (intro sentence, bullets, summary), regardless of content | Shape follows content | Some templating | Fully templated |

---

## How to fix what the rubric finds

- **Em dashes.** Replace with the punctuation the sentence actually needs: a comma for a light aside, parentheses for a true aside, a colon before an explanation or list, or a full stop. Keep en dashes (`–`) in number and date ranges (c. 327–379), which are correct typography and are not counted.
- **Stock vocabulary.** Use the plain word. "Shows" for *underscores*, "important" or nothing for *crucial*, "detailed" or nothing for *nuanced*. Often the sentence is better with the word deleted.
- **Signposting.** Delete the signpost and let the sentence stand. If it does not stand without "Importantly,", it was not important.
- **Negation pivots.** State the positive claim directly. Keep a contrast only when a reader would actually hold the rejected view.
- **Bold lead-in bullets.** Either turn the list into a paragraph, or keep the bullet text plain. Bold only a term being defined.
- **Aphoristic closers.** Cut the last sentence of the paragraph and see whether anything is lost. Usually nothing is.
- **Inflated stakes.** Report the number and let it carry the weight. "Claude corrected the premise in 10 of 10 ratings" needs no adjective.
- **Vague attribution.** Cite, or name the scholar, or remove the claim.

## What the rubric does not penalize

- Technical vocabulary that is the correct term (Krippendorff's α, hagiography, diaconate).
- Numbered steps in a procedure, or tables of data. Lists are fine when the content is a list.
- A single strong sentence that summarizes a section, when it adds a judgement the section did not state.
- Direct quotations from sources, prompts, or model outputs. These are evidence and are excluded from scoring.
