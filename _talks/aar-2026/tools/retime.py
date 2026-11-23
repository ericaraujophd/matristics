"""
retime.py
Recompute the slide-marker times in AAR2026_Araujo_paper.md.
Pace: 136 words a minute, plus 2 s per [click] and 3 s per slide change.
In the 15-minute version, passages between the skip/resume markers and all of slide 18 are left out
(slide 18's two clicks and change are pressed through quickly).
"""
import re, pathlib
# The paper sits one folder up from tools/.
p = pathlib.Path(__file__).resolve().parent.parent / 'AAR2026_Araujo_paper.md'; s = p.read_text()
RATE, CLICK, CHANGE = 136.0, 2.0, 3.0
SKIP = 18   # the conspiracy slide, skipped in the 15-minute version
head, rest = s.split('**[Slide 1 ', 1)
body, refs = ('**[Slide 1 ' + rest).split('\n---\n\n## References', 1)
chunks = re.split(r'(\*\*\[Slide \d+ · [\d:]+ · 15 min: [\w:]+\]\*\*)', body)
wc = lambda x: len(re.findall(r"[A-Za-z0-9][\w'.,-]*", re.sub(r'\*\*\[.*?\]\*\*( \(.*?\)\*\*)?', '', x)))
def mmss(sec): sec = int(round(sec)); return f"{sec//60}:{sec%60:02d}"
tf = ts = 0.0; out = []; full_w = short_w = 0
for i in range(1, len(chunks), 2):
    n = int(re.search(r'Slide (\d+)', chunks[i]).group(1)); txt = chunks[i+1]
    out.append(f"**[Slide {n} · {mmss(tf)} · 15 min: {'skip' if n == SKIP else mmss(ts)}]**" + txt)
    inside = n == SKIP
    for para in txt.split('\n\n'):
        if '[15 min: skip ▼]' in para: inside = True; continue
        if '[15 min: resume ▲]' in para: inside = False; continue
        w = wc(para); c = para.count('[click]'); sec = w / RATE * 60 + c * CLICK
        tf += sec; full_w += w
        if not inside: ts += sec; short_w += w
        elif c: ts += c * 1.0
    tf += CHANGE; ts += CHANGE if n != SKIP else 1.0
s = head + ''.join(out) + '\n---\n\n## References' + refs
s = re.sub(r"About [\d,]+ words in full, [\d,]+ in the 15-minute version\.", f"About {full_w:,} words in full, {short_w:,} in the 15-minute version.", s)
p.write_text(s)
print('full end', mmss(tf - CHANGE), '| 15-min end', mmss(ts - CHANGE), '| words', full_w, short_w)
