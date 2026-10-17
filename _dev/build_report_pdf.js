#!/usr/bin/env node
/*
 * build_report_pdf.js: turn the print edition of the report into the PDF
 * that every report page offers for download.
 *
 * WHAT IT DOES
 *   1. Serves the rendered site (_site/) on a local port with a tiny
 *      built-in static server, so links and fonts resolve as they do online.
 *   2. Opens report/print.html in headless Chromium, in LIGHT mode, with
 *      motion switched off (so no element is caught mid-animation).
 *   3. Prints it to report/matristics-full-report.pdf (US Letter, page
 *      numbers in the footer).
 *
 * The PDF is written into the SOURCE folder report/, not into _site/, and is
 * committed to the repository. Quarto copies it into _site/ on every render
 * (it is listed under `project: resources` in _quarto.yml), so the GitHub
 * deploy workflow does not need a browser.
 *
 * WHEN TO RUN
 *   After changing any report section:
 *       quarto render
 *       node _dev/build_report_pdf.js
 *       quarto render          # copies the new PDF into _site/
 *
 * REQUIREMENTS
 *   Node 18+ and Playwright with Chromium (npm i playwright).
 */
const http = require("http");
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

const ROOT = path.resolve(__dirname, "..");
const SITE = path.join(ROOT, "_site");
const OUT = path.join(ROOT, "report", "matristics-full-report.pdf");

const TYPES = { ".html": "text/html", ".css": "text/css", ".js": "text/javascript", ".json": "application/json",
  ".jpg": "image/jpeg", ".png": "image/png", ".svg": "image/svg+xml", ".woff": "font/woff", ".woff2": "font/woff2", ".pdf": "application/pdf" };

// Minimal static file server for _site/. Directory requests serve index.html.
function serve() {
  return new Promise((resolve) => {
    const server = http.createServer((req, res) => {
      let p = decodeURIComponent(req.url.split("?")[0]);
      let file = path.join(SITE, p);
      if (!file.startsWith(SITE)) { res.writeHead(403); return res.end(); }
      if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, "index.html");
      fs.readFile(file, (err, buf) => {
        if (err) { res.writeHead(404); return res.end("not found"); }
        res.writeHead(200, { "Content-Type": TYPES[path.extname(file)] || "application/octet-stream" });
        res.end(buf);
      });
    });
    server.listen(0, "127.0.0.1", () => resolve(server));
  });
}

(async () => {
  if (!fs.existsSync(path.join(SITE, "report", "print.html"))) {
    console.error("Render the site first: quarto render");
    process.exit(1);
  }
  const server = await serve();
  const port = server.address().port;
  const browser = await chromium.launch();
  const context = await browser.newContext();
  // Light colour scheme and no motion, set before any page script runs.
  await context.addInitScript(() => {
    try { localStorage.setItem("quarto-color-scheme", "default"); localStorage.setItem("mx-motion", "off"); } catch (e) {}
  });
  const page = await context.newPage();
  await page.goto(`http://127.0.0.1:${port}/report/print.html`, { waitUntil: "networkidle" });
  await page.emulateMedia({ media: "print" });
  await page.evaluate(() => document.fonts && document.fonts.ready);
  await page.pdf({
    path: OUT,
    format: "Letter",
    printBackground: true,
    margin: { top: "0.8in", bottom: "0.8in", left: "0.85in", right: "0.85in" },
    displayHeaderFooter: true,
    headerTemplate: "<span></span>",
    footerTemplate:
      '<div style="width:100%;font:8px sans-serif;color:#777;padding:0 0.85in;display:flex;justify-content:space-between">' +
      '<span>Matristics · Full report</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>',
  });
  await browser.close();
  server.close();
  console.log("wrote", path.relative(ROOT, OUT), (fs.statSync(OUT).size / 1024).toFixed(0) + " KB");
})();
