/*
 * benchmark.js: interactive charts for the Matristics Benchmark page and
 * the leaderboard teaser on the home page.
 *
 * DATA
 *   Everything comes from window.MATRISTICS, defined in benchmark-data.js,
 *   which _dev/build_benchmark_data.py generates from the scoring workbook.
 *   This file never contains numbers of its own: if a score changes, re-run
 *   the build script and every chart follows.
 *
 * WHAT IT DRAWS (each only if its container exists on the page)
 *   #mx-leaderboard        ranked model cards with dimension mini-bars
 *   #mx-leaderboard-mini   compact version for the home page
 *   #mx-profile            the 35-axis radar "performance profile", one
 *                          axis per question, with model picker, compare
 *                          picker, and a zoom toggle
 *   #mx-multiples          six small radars, one per model, over the
 *                          4 dimensions x 2 figures = 8 axes
 *   #mx-heatmap            model x question grid coloured by mean score
 *
 * LIBRARIES
 *   Chart.js 4 (loaded from cdnjs by the page) for the radars. The
 *   leaderboard and heatmap are plain HTML, which keeps them crisp,
 *   accessible to screen readers, and printable.
 *
 * COLOUR RULES (validated with the dataviz palette checker)
 *   - Selected model:  #8E2159 (the site's bright Tyrian)
 *   - Compare model:   #0079A8 (blue; passes colour-blind separation
 *                      against the Tyrian, deltaE 12.9 deutan)
 *   - Field average:   grey, dashed, so it never competes with a model
 *   - Heatmap:         one hue (Tyrian), light to dark = low to high
 *   A model's colour depends on whether it is "selected" or "compared",
 *   never on its rank.
 */
(function () {
  "use strict";

  const D = window.MATRISTICS;
  if (!D) {
    console.warn("benchmark.js: window.MATRISTICS missing; did benchmark-data.js load?");
    return;
  }

  // ---------------------------------------------------------------------
  // Shared constants and helpers
  // ---------------------------------------------------------------------

  const COLOR = {
    primary: "#8E2159",
    compare: "#0079A8",
    field: "#8A7F74",
    grid: "rgba(90, 79, 69, 0.16)",
    ink: "#2C241D",
    inkSoft: "#5A4F45",
    figureBand: { M: "rgba(176, 138, 62, 0.55)", O: "rgba(102, 2, 60, 0.35)" },
  };
  const FONT = '"Inter", -apple-system, "Segoe UI", Roboto, sans-serif';

  // Two decimals, rounding half up. The tiny epsilon fixes binary floating
  // point: 4.725 is stored as 4.72499999..., which toFixed would round DOWN
  // to 4.72 while the tables (rounded in a spreadsheet) say 4.73.
  const fmt = (x) => (x == null ? "n/a" : (x + 1e-9).toFixed(2));
  const byKey = (k) => D.models.find((m) => m.key === k);
  const qById = Object.fromEntries(D.questions.map((q) => [q.id, q]));
  const figName = Object.fromEntries(D.figures.map((f) => [f.key, f.name]));

  // Models sorted by overall mean, best first. Used for ranks only; the
  // pickers keep the fixed order from the data file.
  const ranked = [...D.models].sort((a, b) => b.overall - a.overall);
  const rankOf = Object.fromEntries(ranked.map((m, i) => [m.key, i + 1]));

  // Hex colour with alpha, for translucent radar fills.
  function alpha(hex, a) {
    const n = parseInt(hex.slice(1), 16);
    return `rgba(${(n >> 16) & 255}, ${(n >> 8) & 255}, ${n & 255}, ${a})`;
  }

  // Tiny element builder: el("div", {class: "x"}, child, "text", ...)
  function el(tag, attrs, ...kids) {
    const e = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs || {})) {
      if (k === "class") e.className = v;
      else if (k === "text") e.textContent = v;
      else if (k.startsWith("on")) e.addEventListener(k.slice(2), v);
      else e.setAttribute(k, v);
    }
    for (const k of kids) if (k != null) e.append(k);
    return e;
  }

  // Map a score onto a 0-100% bar width, using the same truncated axis
  // (4.0 to 5.0) as the original bar chart so small gaps stay visible.
  // Values below 4.0 are clamped to an empty bar, never a negative one.
  const BAR_MIN = 4.0;
  const barPct = (x) => Math.max(0, Math.min(1, (x - BAR_MIN) / (5 - BAR_MIN))) * 100;

  // Shared floating tooltip for the HTML (non-Chart.js) charts.
  let tip;
  function showTip(evt, html) {
    if (!tip) {
      tip = el("div", { class: "mx-tip", role: "tooltip" });
      document.body.append(tip);
    }
    tip.innerHTML = html;
    tip.style.display = "block";
    const pad = 14;
    const r = tip.getBoundingClientRect();
    let x = evt.clientX + pad;
    let y = evt.clientY + pad;
    if (x + r.width > window.innerWidth - 8) x = evt.clientX - r.width - pad;
    if (y + r.height > window.innerHeight - 8) y = evt.clientY - r.height - pad;
    tip.style.left = x + "px";
    tip.style.top = y + "px";
  }
  function hideTip() {
    if (tip) tip.style.display = "none";
  }

  // The page-wide "selected model". Clicking a leaderboard card sets it,
  // and the profile radar listens for the change.
  const listeners = [];
  let selected = ranked[0].key;
  function select(key, scroll) {
    selected = key;
    listeners.forEach((fn) => fn(key));
    document.querySelectorAll(".mx-card").forEach((c) =>
      c.classList.toggle("is-selected", c.dataset.key === key));
    if (scroll) {
      const target = document.getElementById("mx-profile");
      if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }

  // ---------------------------------------------------------------------
  // 1. Leaderboard
  // ---------------------------------------------------------------------

  function renderLeaderboard(root, compact) {
    const list = el("ol", { class: "mx-board" + (compact ? " is-compact" : "") });
    ranked.forEach((m) => {
      const dims = D.dimensions.map((d) =>
        el("div", { class: "mx-dim" },
          el("span", { class: "mx-dim-name", text: d.name }),
          el("span", { class: "mx-dim-track" },
            el("span", { class: "mx-dim-fill", style: `width:${barPct(m.dims[d.key])}%` })),
          el("span", { class: "mx-dim-val", text: fmt(m.dims[d.key]) })));

      const card = el(compact ? "a" : "li", {
        class: "mx-card",
        "data-key": m.key,
        ...(compact ? { href: "benchmark/index.html#mx-profile" } : { tabindex: "0", role: "button",
          "aria-label": `Show performance profile for ${m.name}` }),
      },
        el("span", { class: "mx-rank", text: "#" + rankOf[m.key] }),
        el("span", { class: "mx-id" },
          el("span", { class: "mx-name", text: m.name }),
          el("span", { class: "mx-provider", text: m.provider })),
        el("span", { class: "mx-overall" },
          el("span", { class: "mx-overall-val", text: fmt(m.overall) }),
          el("span", { class: "mx-overall-lbl", text: "overall" })),
        compact ? null : el("div", { class: "mx-dims" }, ...dims),
        compact ? null : el("div", { class: "mx-facts" },
          el("span", {}, "Macrina ", el("b", { text: fmt(m.figures.M) })),
          el("span", {}, "Olympias ", el("b", { text: fmt(m.figures.O) })),
          el("span", {}, "False premises corrected ",
            el("b", { text: `${m.premise.corrected}/${m.premise.of}` }))));

      if (!compact) {
        card.addEventListener("click", () => select(m.key, true));
        card.addEventListener("keydown", (e) => {
          if (e.key === "Enter" || e.key === " ") { e.preventDefault(); select(m.key, true); }
        });
      }
      list.append(compact ? el("li", {}, card) : card);
    });
    root.append(list);
    if (!compact) {
      root.append(el("p", { class: "mx-note",
        text: "Bars run from 4.0 to 5.0 so the differences are visible; the rubric scale runs from 1. Select a model to see its profile." }));
    }
  }

  // ---------------------------------------------------------------------
  // 2. Radar helpers (Chart.js)
  // ---------------------------------------------------------------------

  // Chart.js plugin: draws a thin coloured arc just outside the radar for
  // each figure's block of axes, with the figure's name, so a reader can
  // see where the Macrina questions end and the Olympias questions begin.
  // `groups` is a list of {from, to, label, color} in axis-index units.
  const figureArcs = {
    id: "figureArcs",
    afterDraw(chart, _args, opts) {
      if (!opts || !opts.groups) return;
      const r = chart.scales.r;
      const n = chart.data.labels.length;
      const ctx = chart.ctx;
      // Chart.js puts axis 0 at the top (-90 degrees) and goes clockwise.
      const ang = (i) => -Math.PI / 2 + (i * 2 * Math.PI) / n;
      const half = Math.PI / n;
      const radius = r.drawingArea + (opts.offset || 6);
      ctx.save();
      opts.groups.forEach((g) => {
        ctx.beginPath();
        ctx.strokeStyle = g.color;
        ctx.lineWidth = 4;
        ctx.lineCap = "round";
        ctx.arc(r.xCenter, r.yCenter, radius, ang(g.from) - half + 0.02, ang(g.to) + half - 0.02);
        ctx.stroke();
      });
      ctx.restore();
    },
  };

  function radarOptions(min, max, opts) {
    return {
      responsive: true,
      maintainAspectRatio: true,
      animation: { duration: 350 },
      layout: { padding: opts.padding ?? 8 },
      interaction: { mode: "index", intersect: false },
      scales: {
        r: {
          min, max,
          ticks: {
            stepSize: opts.step || 0.5,
            backdropColor: "rgba(255, 253, 249, 0.85)",
            color: COLOR.inkSoft,
            font: { family: FONT, size: 10 },
            display: opts.ticks !== false,
            z: 2,
          },
          grid: { color: COLOR.grid },
          angleLines: { color: COLOR.grid },
          pointLabels: {
            color: COLOR.ink,
            font: { family: FONT, size: opts.labelSize || 11, weight: 500 },
            padding: opts.labelPad ?? 6,
          },
        },
      },
      plugins: {
        legend: { display: false }, // we draw our own legend in HTML
        figureArcs: opts.arcs ? { groups: opts.arcs, offset: opts.arcOffset } : false,
        tooltip: {
          backgroundColor: "#FFFDF9",
          titleColor: COLOR.ink,
          bodyColor: COLOR.ink,
          borderColor: "#E2D8C8",
          borderWidth: 1,
          padding: 10,
          titleFont: { family: FONT, weight: 600 },
          bodyFont: { family: FONT },
          callbacks: opts.tooltip || {},
        },
      },
    };
  }

  function series(label, values, color, kind) {
    const isField = kind === "field";
    return {
      label,
      data: values,
      borderColor: color,
      backgroundColor: isField ? "transparent" : alpha(color, kind === "compare" ? 0.10 : 0.16),
      borderWidth: 2,
      borderDash: isField ? [5, 4] : [],
      pointRadius: isField ? 0 : 3,
      pointHoverRadius: isField ? 0 : 5,
      pointBackgroundColor: color,
      pointBorderColor: "#FFFDF9",
      pointBorderWidth: 1.5,
      fill: !isField,
    };
  }

  // ---------------------------------------------------------------------
  // 3. Performance profile: one axis per question
  // ---------------------------------------------------------------------

  function renderProfile(root) {
    const qs = D.questions;
    const labels = qs.map((q) => q.id);
    const fieldVals = qs.map((q) => q.mean);
    const valsFor = (m) => qs.map((q) => m.perQuestion[q.id]);

    // Axis index ranges for each figure, for the arcs plugin.
    const arcs = D.figures.map((f) => {
      const idx = qs.map((q, i) => (q.figure === f.key ? i : -1)).filter((i) => i >= 0);
      return { from: idx[0], to: idx[idx.length - 1], color: COLOR.figureBand[f.key], label: f.name };
    });

    // --- controls ------------------------------------------------------
    const modelSel = el("select", { id: "mx-model", class: "mx-select", "aria-label": "Model" });
    const compareSel = el("select", { id: "mx-compare", class: "mx-select", "aria-label": "Compare with" });
    compareSel.append(el("option", { value: "", text: "No comparison" }));
    D.models.forEach((m) => {
      modelSel.append(el("option", { value: m.key, text: m.name }));
      compareSel.append(el("option", { value: m.key, text: m.name }));
    });
    const zoomBtn = el("button", { class: "mx-toggle", type: "button", "aria-pressed": "true",
      text: "Axis 3–5" });

    const legend = el("div", { class: "mx-legend" });
    const summary = el("p", { class: "mx-profile-summary" });

    root.append(
      el("div", { class: "mx-controls" },
        el("label", {}, el("span", { text: "Model" }), modelSel),
        el("label", {}, el("span", { text: "Compare with" }), compareSel),
        zoomBtn),
      el("div", { class: "mx-profile-body" },
        el("div", { class: "mx-radar-wrap" }, el("canvas", { id: "mx-profile-canvas",
          role: "img", "aria-label": "Radar chart of mean score on each of the 35 questions for the selected model" })),
        el("div", { class: "mx-profile-side" }, legend, summary,
          el("div", { class: "mx-figkey" },
            ...D.figures.map((f) => el("span", {},
              el("i", { style: `background:${COLOR.figureBand[f.key]}` }), f.name))))));

    // --- chart ---------------------------------------------------------
    let zoomed = true;
    const chart = new Chart(document.getElementById("mx-profile-canvas"), {
      type: "radar",
      data: { labels, datasets: [] },
      plugins: [figureArcs],
      options: radarOptions(3, 5, {
        arcs, arcOffset: 4, labelSize: 10, labelPad: 10, padding: 4,
        tooltip: {
          title: (items) => {
            const q = qById[labels[items[0].dataIndex]];
            return `${q.id} · ${figName[q.figure]} · ${q.difficulty}${q.flagged ? " · flagged" : ""}`;
          },
          beforeBody: (items) => wrap(qById[labels[items[0].dataIndex]].text, 52),
          label: (item) => ` ${item.dataset.label}: ${fmt(item.raw)}`,
        },
      }),
    });

    function update() {
      const m = byKey(modelSel.value);
      const c = compareSel.value ? byKey(compareSel.value) : null;
      const ds = [series(m.name, valsFor(m), COLOR.primary, "primary")];
      if (c && c.key !== m.key) ds.push(series(c.name, valsFor(c), COLOR.compare, "compare"));
      ds.push(series("Average of all models", fieldVals, COLOR.field, "field"));
      chart.data.datasets = ds;
      chart.options.scales.r.min = zoomed ? 3 : 1;
      chart.options.scales.r.ticks.stepSize = zoomed ? 0.5 : 1;
      chart.update();

      // HTML legend: identity never depends on colour alone, because each
      // swatch also differs in line style and sits next to the name.
      legend.replaceChildren(...ds.map((d) => el("span", { class: "mx-leg" },
        el("i", { class: d.borderDash.length ? "is-dashed" : "", style: `border-color:${d.borderColor}` }),
        d.label)));

      // A short factual readout: best and worst questions for the model.
      const pq = qs.map((q) => ({ q, v: m.perQuestion[q.id], gap: m.perQuestion[q.id] - q.mean }));
      const low = [...pq].sort((a, b) => a.v - b.v).slice(0, 3);
      const above = pq.filter((x) => x.gap > 0.001).length;
      summary.replaceChildren(
        el("strong", { text: m.name }), ` scores above the all-model average on ${above} of ${qs.length} questions. ` +
        "Lowest: " + low.map((x) => `${x.q.id} (${fmt(x.v)})`).join(", ") + ".");
    }

    // Keep the pickers in sync with the page-wide selection.
    listeners.push((key) => {
      modelSel.value = key;
      if (compareSel.value === key) compareSel.value = "";
      update();
    });
    modelSel.addEventListener("change", () => select(modelSel.value));
    compareSel.addEventListener("change", update);
    zoomBtn.addEventListener("click", () => {
      zoomed = !zoomed;
      zoomBtn.setAttribute("aria-pressed", String(zoomed));
      zoomBtn.textContent = zoomed ? "Axis 3–5" : "Axis 1–5";
      update();
    });
    modelSel.value = selected;
    update();
  }

  // Split a long question into tooltip lines of at most `n` characters.
  function wrap(text, n) {
    const out = [];
    let line = "";
    text.split(" ").forEach((w) => {
      if ((line + " " + w).trim().length > n) { out.push(line); line = w; }
      else line = (line + " " + w).trim();
    });
    if (line) out.push(line);
    return out;
  }

  // ---------------------------------------------------------------------
  // 4. Small multiples: 4 dimensions x 2 figures per model
  // ---------------------------------------------------------------------

  function renderMultiples(root) {
    // Axis order: the four dimensions for Macrina, then the same four for
    // Olympias. Labels carry an "M"/"O" suffix so the halves are readable.
    const short = { HA: "Accuracy", COV: "Coverage", FA: "Framing", EQ: "Epistemic" };
    const keys = [];
    const labels = [];
    D.figures.forEach((f) => D.dimensions.forEach((d) => {
      keys.push(`${d.key}-${f.key}`);
      labels.push(`${short[d.key]} ${f.key}`);
    }));
    const arcs = [
      { from: 0, to: 3, color: COLOR.figureBand.M },
      { from: 4, to: 7, color: COLOR.figureBand.O },
    ];
    const fieldVals = keys.map((k) => D.field.dimFig[k]);

    const grid = el("div", { class: "mx-multiples" });
    root.append(grid);
    ranked.forEach((m) => {
      const id = `mx-mult-${m.key}`;
      grid.append(el("figure", { class: "mx-mult" },
        el("figcaption", {},
          el("span", { class: "mx-mult-name", text: m.name }),
          el("span", { class: "mx-mult-score", text: fmt(m.overall) })),
        el("canvas", { id, role: "img",
          "aria-label": `${m.name}: mean score per rubric dimension for Macrina and for Olympias` })));
      new Chart(document.getElementById(id), {
        type: "radar",
        data: {
          labels,
          datasets: [
            series(m.name, keys.map((k) => m.dimFig[k]), COLOR.primary, "primary"),
            series("Average of all models", fieldVals, COLOR.field, "field"),
          ],
        },
        plugins: [figureArcs],
        options: radarOptions(4, 5, {
          arcs, arcOffset: 3, ticks: false, labelSize: 9.5, labelPad: 4, padding: 2, step: 0.25,
          tooltip: { label: (item) => ` ${item.dataset.label}: ${fmt(item.raw)}` },
        }),
      });
    });
    root.append(el("div", { class: "mx-legend mx-legend-row" },
      el("span", { class: "mx-leg" }, el("i", { style: `border-color:${COLOR.primary}` }), "Model"),
      el("span", { class: "mx-leg" }, el("i", { class: "is-dashed", style: `border-color:${COLOR.field}` }), "Average of all models"),
      ...D.figures.map((f) => el("span", { class: "mx-leg" },
        el("i", { class: "is-band", style: `background:${COLOR.figureBand[f.key]}` }),
        `${f.key} = ${f.name}`))));
  }

  // ---------------------------------------------------------------------
  // 5. Heatmap: models (rows) x questions (columns)
  // ---------------------------------------------------------------------

  // Sequential ramp in one hue, light (low score) to dark (high score).
  // Steps are interpolated linearly in RGB between these stops; the domain
  // 3.0 to 5.0 covers every per-question mean in the data (lowest 3.25).
  const RAMP = ["#F6ECEF", "#E3BFD0", "#C47FA2", "#9A3F72", "#66023C"];
  const H_MIN = 3.0, H_MAX = 5.0;
  function rampColor(v) {
    const t = Math.max(0, Math.min(1, (v - H_MIN) / (H_MAX - H_MIN))) * (RAMP.length - 1);
    const i = Math.min(RAMP.length - 2, Math.floor(t));
    const f = t - i;
    const a = parseInt(RAMP[i].slice(1), 16), b = parseInt(RAMP[i + 1].slice(1), 16);
    const mix = (s) => Math.round(((a >> s) & 255) * (1 - f) + ((b >> s) & 255) * f);
    return `rgb(${mix(16)}, ${mix(8)}, ${mix(0)})`;
  }

  function renderHeatmap(root) {
    const qs = D.questions;
    const table = el("table", { class: "mx-heat" });
    const thead = el("thead");

    // Row 1: figure spans. Row 2: question ids, with a marker on flagged
    // (bias-probe / adversarial) questions.
    const spans = el("tr", {}, el("th", { class: "mx-heat-corner" }));
    D.figures.forEach((f) => {
      const n = qs.filter((q) => q.figure === f.key).length;
      spans.append(el("th", { colspan: String(n), class: `mx-heat-fig fig-${f.key}`, text: f.name }));
    });
    const ids = el("tr", {}, el("th", { class: "mx-heat-corner", scope: "col", text: "Model" }));
    qs.forEach((q) => ids.append(el("th", { scope: "col",
      class: "mx-heat-q" + (q.flagged ? " is-flagged" : "") + (q.id === "O1" ? " fig-start" : ""),
      title: q.text, text: q.id })));
    thead.append(spans, ids);

    const tbody = el("tbody");
    ranked.forEach((m) => {
      const tr = el("tr", {}, el("th", { scope: "row", class: "mx-heat-model", text: m.name }));
      qs.forEach((q) => {
        const v = m.perQuestion[q.id];
        const td = el("td", { class: q.id === "O1" ? "fig-start" : "",
          style: `background:${rampColor(v)}`, "aria-label": `${m.name}, ${q.id}: ${fmt(v)}` });
        td.addEventListener("mousemove", (e) => showTip(e,
          `<b>${m.name} · ${q.id}</b><br><span class="mx-tip-q">${q.text}</span>` +
          `<br>Score <b>${fmt(v)}</b> · all-model average ${fmt(q.mean)}`));
        td.addEventListener("mouseleave", hideTip);
        tr.append(td);
      });
      tbody.append(tr);
    });
    table.append(thead, tbody);

    // Legend: the ramp with its end values, plus the flagged-question key.
    const legend = el("div", { class: "mx-heat-legend" },
      el("span", { text: H_MIN.toFixed(1) }),
      el("span", { class: "mx-heat-ramp",
        style: `background:linear-gradient(90deg, ${RAMP.join(", ")})` }),
      el("span", { text: H_MAX.toFixed(1) }),
      el("span", { class: "mx-heat-flagkey" }, el("i"), "bias-probe or adversarial question"));

    root.append(el("div", { class: "mx-heat-scroll" }, table), legend);
  }

  // ---------------------------------------------------------------------
  // Boot: draw whatever containers this page has.
  // ---------------------------------------------------------------------

  function boot() {
    const lb = document.getElementById("mx-leaderboard");
    const lbm = document.getElementById("mx-leaderboard-mini");
    const pr = document.getElementById("mx-profile");
    const mu = document.getElementById("mx-multiples");
    const hm = document.getElementById("mx-heatmap");
    const hasChart = typeof window.Chart !== "undefined";
    if (hasChart) {
      Chart.defaults.font.family = FONT;
      Chart.defaults.color = COLOR.inkSoft;
    }
    if (lb) renderLeaderboard(lb, false);
    if (lbm) renderLeaderboard(lbm, true);
    if (pr && hasChart) renderProfile(pr);
    if (mu && hasChart) renderMultiples(mu);
    if (hm) renderHeatmap(hm);
    if (lb) select(selected, false);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
