# Maintaining the Matristics site

This folder holds the tools behind the site. Quarto ignores folders whose names start with `_`, so nothing here is published.

## Site structure

| Path | What it is |
|------|------------|
| `index.qmd` | Home page. Mostly charts, with a short headline and links into the rest of the site. |
| `benchmark/index.qmd` | The interactive benchmark: radar explorer, heatmap, figure comparison, error tags, leaderboard. |
| `benchmark/benchmark-data.js` | Aggregated scores. **Generated; do not edit by hand.** |
| `assets/mx-charts.js` | Every chart on Home and Benchmark. It reads only `benchmark-data.js`. |
| `figures/` | One page per scored figure, plus the figures grid. |
| `report/` | The full report: `index.qmd` (landing page with the PDF link), seven section pages, and `print.qmd` (every section on one page, used only to make the PDF). |
| `report/_sections/` | The text of each report section. Each section page and the print edition `include` these files, so every section's text lives in one place. Edit here. |
| `report/matristics-full-report.pdf` | The downloadable PDF. **Generated; committed so the deploy needs no browser.** |
| `theme-dark.scss`, `theme-light.scss` | Colour tokens for each mode. Dark is the default. |
| `theme.scss` | All shared rules: typography, components, charts, animation, reduced motion, print. |
| `_includes/head.html` | Applies the saved text size and motion setting before the page paints. |
| `_includes/site.html` | Accessibility toolbar, skip link, scroll-reveal animations, count-ups, theme-change event. |

Old URLs (`/background/`, `/methodology/`, `/biases/`, `/data-collection/`) still work: the report sections declare them as `aliases`, and Quarto writes redirect pages there.

## Accessibility and motion

- **Text size:** the A− and A+ buttons in the navbar give four steps, from 17 px to 23.5 px. The setting is saved in `localStorage` (`mx-text`).
- **Reduce motion:** the pause button in the navbar turns off every animation. Animations are also off when the operating system asks for reduced motion, unless the reader switches them back on. Saved as `mx-motion`.
- **Dark/light:** this is Quarto's own toggle. The charts redraw in the new colours when the `mx:theme` event fires.
- Everything works without JavaScript. Animations only start once `head.html` has added `.mx-js` to `<html>`.

## Updating the scores

1. Export the Google Sheet "Scoring Template" as `.xlsx`.
2. Run `python3 _dev/build_benchmark_data.py path/to/Scoring_Template.xlsx`.
3. Update any numbers quoted in `report/_sections/results.qmd`.

## Rebuilding the PDF

Rebuild it after any change to a report section:

```bash
quarto render
node _dev/build_report_pdf.js     # needs: npm i playwright
quarto render                     # copies the new PDF into _site/
```

## Checking the prose

```bash
python3 _dev/ai_lint.py           # mechanical pass of writing-rubric.md
python3 _dev/ai_lint.py --show    # list every flagged line
```

Then read the changed pages against Section B of `writing-rubric.md`.
