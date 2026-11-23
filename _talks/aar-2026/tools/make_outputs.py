"""
make_outputs.py
Regenerate, from AAR2026_Araujo_paper.md (the single source of the talk):
  1. slides/script.md - presenter notes for slides/build.py (one "## [Slide n]" section per slide)
  2. AAR2026_Araujo_paper.pdf - large-type reading copy; 15-minute cuts greyed
"""
import re, base64, pathlib, os
# Run from the talk folder (_talks/aar-2026), whatever the current directory is.
ROOT = pathlib.Path(__file__).resolve().parent.parent
os.chdir(ROOT)
paper = pathlib.Path('AAR2026_Araujo_paper.md').read_text()

# ---------- 1. presenter notes ----------
old = pathlib.Path('slides/script.md').read_text()   # previous notes: slide titles + backup section
titles = dict(re.findall(r'^## \[Slide (\d+)\] (.*?)\s+·', old, re.M))   # slide titles from the earlier notes
backup = old.split('## Backup slides', 1)[1]                              # Q&A notes for B1, B2 kept as they were
body = '**[Slide 1 ' + paper.split('**[Slide 1 ', 1)[1].split('\n---\n\n## References')[0]
parts = re.split(r'\*\*\[Slide (\d+) · ([\d:]+) · 15 min: ([\w:]+)\]\*\*', body)
out = ["# The Future of the Past: Evaluating Large Language Model Reliability in Early Christian Historical Studies", "",
       "**Presenter notes · AAR 2026, Session A23-217 · Monday 23 November, 12:30 PM, CCC Room 507**",
       "Eric Araújo, Calvin University", "",
       "These notes are the full text of the paper (AAR2026_Araujo_paper.md), so the presenter view (key P) shows what you read. "
       "Times are cumulative for the 20-minute and the 15-minute versions. [click] marks a build on the same slide. "
       "For 15 minutes, leave out the passages between [15 min: skip ▼] and [15 min: resume ▲], and press through slide 18.", "", "---", ""]
for i in range(1, len(parts), 4):
    n, tf, ts, txt = parts[i:i+4]
    out.append(f"## [Slide {n}] {titles.get(n,'')}  ·  {tf}  ·  15 min: {ts}\n\n{txt.strip().replace('**[click]**','[click]')}\n")
out.append("---\n\n## Backup slides" + backup)
pathlib.Path('slides/script.md').write_text("\n".join(out))

# ---------- 2. reading PDF ----------
import subprocess
subprocess.run(['pandoc','AAR2026_Araujo_paper.md','-s','--css','tools/reading.css','--embed-resources',
                '--metadata','pagetitle=AAR 2026 paper','-o','paper.html'], check=True)
h = pathlib.Path('paper.html').read_text()
res, inside = [], False
for para in re.split(r'(?=<p>)', h):
    if para.startswith('<p><strong>[15 min'):
        para = para.replace('<p>', '<p class="cutmark">', 1)
        if 'skip ▼' in para or 'skip this slide' in para: inside = True
        elif 'resume ▲' in para: inside = False
    elif para.startswith('<p><strong>[Slide'):
        inside = 'skip]' in para          # slide 18 is skipped whole
    elif inside and para.startswith('<p>'):
        para = para.replace('<p>', '<p class="skip">', 1)
    res.append(para)
h = ''.join(res)
fd = pathlib.Path('tools/fonts')   # Libre Baskerville and Public Sans, for the reading copy
def face(fam, file, w, st):
    b = base64.b64encode(next(fd.rglob(file)).read_bytes()).decode()
    return f"@font-face{{font-family:'{fam}';src:url(data:font/woff2;base64,{b}) format('woff2');font-weight:{w};font-style:{st};}}"
css = (face('Libre Baskerville','libre-baskerville-latin-400-normal.woff2',400,'normal') + face('Libre Baskerville','libre-baskerville-latin-400-italic.woff2',400,'italic')
       + face('Public Sans','public-sans-latin-600-normal.woff2',700,'normal') + face('Public Sans','public-sans-latin-400-normal.woff2',400,'normal'))
pathlib.Path('paper.html').write_text(h.replace('</head>', f'<style>{css}</style></head>'))
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(); pg.goto('file://' + str(pathlib.Path('paper.html').resolve())); pg.wait_for_timeout(500)
    pg.pdf(path='AAR2026_Araujo_paper.pdf', format='Letter', margin={'top':'0.8in','bottom':'0.8in','left':'0.9in','right':'0.9in'},
           display_header_footer=True, header_template='<span></span>',
           footer_template='<div style="font-size:9pt;width:100%;text-align:right;padding-right:0.9in;color:#6E6468"><span class="pageNumber"></span> / <span class="totalPages"></span></div>')
print('done')
