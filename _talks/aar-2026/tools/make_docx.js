/*
 * make_docx.js
 * ------------
 * Printable backup of the AAR 2026 reading text, built from blocks.json
 * (made from AAR2026_Araujo_paper.md).
 *
 * Design for reading at a lectern:
 *   - US Letter, 0.8 in margins, Georgia 18 pt body, 1.5 line spacing.
 *   - Every slide change is a full-width black bar with white text:
 *       "SLIDE 7  ·  Design            20 min 3:52  ·  15 min 3:10"
 *     The bar stays with the paragraph after it (keepNext), so it never
 *     sits alone at the bottom of a page.
 *   - Every [click] is its own red line, "→ CLICK", before the text it reveals.
 *   - Passages cut from the 15-minute version are in normal black type on a
 *     light tint with a red left rule, opened by "15 MIN: SKIP ▼" and closed by
 *     "15 MIN: RESUME ▲" (both red, small caps), so they are easy to see and
 *     still easy to read.
 *   - Footer: page X of Y.
 */
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, AlignmentType, BorderStyle, ShadingType,
  Footer, PageNumber, TabStopType, LineRuleType,
} = require("docx");

const blocks = JSON.parse(fs.readFileSync("/home/claude/docx/blocks.json", "utf8"));

const BODY = 36;              // 18 pt (docx sizes are half-points)
const FONT = "Georgia";
const SANS = "Arial";
const RED = "B3261E";
const TINT = "EFE9DC";
const CONTENT_W = 12240 - 2 * 1152;   // page width minus 0.8 in margins, in DXA

// ---- helpers ---------------------------------------------------------------
const label = (text, color = RED, size = 22) =>
  new TextRun({ text, font: SANS, bold: true, size, color, characterSpacing: 20 });

function slideBar(b) {
  // Black bar: slide number and title on the left, the two target times on the right.
  return new Paragraph({
    keepNext: true,
    spacing: { before: 360, after: 200 },
    shading: { type: ShadingType.CLEAR, color: "auto", fill: "111111" },
    border: { top: { style: BorderStyle.SINGLE, size: 6, color: "111111", space: 4 },
              bottom: { style: BorderStyle.SINGLE, size: 6, color: "111111", space: 4 } },
    tabStops: [{ type: TabStopType.RIGHT, position: CONTENT_W }],
    children: [
      new TextRun({ text: ` SLIDE ${b.n}`, font: SANS, bold: true, size: 32, color: "FFFFFF" }),
      new TextRun({ text: `   ${b.title}`, font: SANS, size: 28, color: "FFFFFF" }),
      new TextRun({ text: `\t20 min ${b.t}  ·  15 min ${b.t15} `, font: SANS, size: 24, color: "F2B8B0" }),
    ],
  });
}

function clickLine() {
  return new Paragraph({ keepNext: true, spacing: { before: 120, after: 60 },
    children: [label("→ CLICK", RED, 28)] });
}

function skipMark(text) {
  return new Paragraph({ keepNext: text.includes("SKIP"), spacing: { before: 160, after: 80 },
    children: [label(text, RED, 22)] });
}

function bodyPara(b) {
  const runs = b.runs.map(r => new TextRun({ text: r.text, italics: r.italic, font: FONT, size: BODY }));
  const opts = { spacing: { after: 240, line: 360, lineRule: LineRuleType.AUTO }, children: runs };   // 1.5 line spacing
  if (b.skip) {
    // 15-minute cut: readable black text on a light tint with a red left rule
    opts.shading = { type: ShadingType.CLEAR, color: "auto", fill: TINT };
    opts.border = { left: { style: BorderStyle.SINGLE, size: 24, color: RED, space: 10 } };
    opts.indent = { left: 240 };
  }
  return new Paragraph(opts);
}

// ---- document ---------------------------------------------------------------
const children = [
  new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text: "The Future of the Past", font: FONT, bold: true, size: 48 })] }),
  new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text: "Evaluating Large Language Model Reliability in Early Christian Historical Studies", font: FONT, italics: true, size: 28 })] }),
  new Paragraph({ spacing: { after: 240 }, children: [new TextRun({ text: "Eric Araújo · AAR Denver · A23-217 · Monday 23 November 2026 · Room 507", font: SANS, size: 22, color: "444444" })] }),
  new Paragraph({
    spacing: { after: 360 },
    border: { top: { style: BorderStyle.SINGLE, size: 8, color: "111111", space: 6 }, bottom: { style: BorderStyle.SINGLE, size: 8, color: "111111", space: 6 } },
    children: [
      new TextRun({ text: "Black bar = change slide.  ", font: SANS, size: 22, bold: true }),
      new TextRun({ text: "→ CLICK = next build on the same slide.  ", font: SANS, size: 22, bold: true, color: RED }),
      new TextRun({ text: "Tinted passages = leave out for 15 minutes (slide 18 is skipped whole). ", font: SANS, size: 22, bold: true }),
      new TextRun({ text: "Full ≈ 19:47 · short ≈ 15:08.", font: SANS, size: 22 }),
    ],
  }),
];

for (const b of blocks) {
  if (b.type === "slide") children.push(slideBar(b));
  else if (b.type === "click") children.push(clickLine());
  else if (b.type === "skipStart") children.push(skipMark("15 MIN: SKIP ▼"));
  else if (b.type === "skipEnd") children.push(skipMark("15 MIN: RESUME ▲"));
  else if (b.type === "note") children.push(new Paragraph({ keepNext: true, spacing: { before: 80, after: 160 },
      shading: { type: ShadingType.CLEAR, color: "auto", fill: TINT }, children: [label(b.text, RED, 22)] }));
  else if (b.type === "p") children.push(bodyPara(b));
}

const doc = new Document({
  styles: { default: { document: { run: { font: FONT, size: BODY } } } },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1152, bottom: 1152, left: 1152, right: 1152 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT,
      children: [   // each piece is its own run so the page numbers get the small size too
        new TextRun({ text: "page ", font: SANS, size: 20, color: "666666" }),
        new TextRun({ children: [PageNumber.CURRENT], font: SANS, size: 20, color: "666666" }),
        new TextRun({ text: " of ", font: SANS, size: 20, color: "666666" }),
        new TextRun({ children: [PageNumber.TOTAL_PAGES], font: SANS, size: 20, color: "666666" })] })] }) },
    children,
  }],
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync("/home/claude/docx/AAR2026_Araujo_paper_print.docx", buf);
  console.log("wrote AAR2026_Araujo_paper_print.docx");
});
