"""
count.py
--------
Clean records.csv by hand-checked rules, classify each book, and count by decade.

Cleaning (each rule removes catalog noise found by reading every record):
  - duplicates: same figure + normalized title + year from different sources
  - not about the saint: school yearbooks (Mt. Saint Macrina Academy), the
    Macrina Bakery cookbook, Greek titles using "makrina" ("far away"),
    a 19th-c. Polish nun named Macrina, a modern nun "Mother Macrina"
    (Zaleski), an art-show catalogue, an ERIC health article, a Wikipedia dump,
    a Geronda Makrina quote book
  - reprints of one multi-volume church history (Böhringer 1873-79) count once
Classification:
  source  = an edition or translation of an ancient text about her
            (Gregory's Life of Macrina / On the Soul; Chrysostom's letters to Olympias)
  study   = a modern book about her (or with her as a main subject)
Output: decades.csv and books_clean.csv
"""
import csv, re, collections, unicodedata
rows = list(csv.DictReader(open("records.csv")))
for r in rows:                      # NFC so "à" and "ö" match however the catalog encoded them
    for k in ("title", "author"): r[k] = unicodedata.normalize("NFC", r[k])
norm = lambda t: re.sub(r"[^a-z]", "", t.lower())[:40]
uniq = {}
for r in rows:
    uniq.setdefault((r["figure"], norm(r["title"]), r["year"]), r)
NOISE = re.compile(r"yearbook|bakery|macrina dolly|mieczyslawska|mother macrina|zaleski|ERIC |wikipedia|"
                   r"makrina taxidia|makrina phōta|merē makrina|makrina aristourgēmata|gerondissa|more from macrina", re.I)
SOURCE = re.compile(r"life of (saint |st\. )?macrina|vie de sainte macrine|vita (di )?s(an)?\w*\.? ?macrin|leben der heiligen makrina$|"
                    r"de (inmortalitate|immortalitate|anima)|gespräch mit seiner schwester|vida de macrina|z.?hytti|viata sfintei|"
                    r"lettres? (à|a) olymp|letters to (saint |deaconess )?olympi|lettere a olimp|dall'esilio|exhortations|livre de l'esp|"
                    r"lettre d'exil|^st\. gregory of nyssa", re.I)
keep, seen_boehr = [], False
for r in uniq.values():
    blob = r["title"] + " " + r["author"]
    if NOISE.search(blob): continue
    if "Böhringer" in r["author"]:
        if seen_boehr: continue
        seen_boehr = True
    if r["title"].startswith("Das Leben der heiligen Makrina") or r["title"].startswith("Ascetism"):
        r["kind"] = "study"            # Albrecht 1986 and Wong 2016 are studies of the Life, not editions
    else: r["kind"] = "source" if SOURCE.search(r["title"]) else "study"
    keep.append(r)
# Final de-duplication.
#  - source editions: several catalog records in one year for the same text are
#    almost always one edition catalogued twice (e.g. Lowther Clarke's 1916 Life of
#    Macrina appears under three titles), so keep one per figure and year.
#  - studies: one per normalized title and year.
final = {}
for r in keep:
    key = (r["figure"], "src", r["year"]) if r["kind"] == "source" else (r["figure"], norm(r["title"])[:20], r["year"])
    final.setdefault(key, r)
keep = sorted(final.values(), key=lambda r: (r["figure"], int(r["year"])))
with open("books_clean.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["figure", "kind", "year", "title", "author", "source", "id"])
    w.writeheader(); [w.writerow({k: r[k] for k in w.fieldnames}) for r in keep]
c = collections.Counter((r["figure"], r["kind"], int(r["year"]) // 10 * 10) for r in keep)
decades = sorted({d for _, _, d in c})
with open("decades.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["decade", "Macrina_source", "Macrina_study", "Olympias_source", "Olympias_study"])
    for d in decades:
        w.writerow([d] + [c[(fg, k, d)] for fg in ("Macrina", "Olympias") for k in ("source", "study")])
for r in keep: print(r["figure"][:3], r["kind"][:5], r["year"], r["title"][:70])
print(open("decades.csv").read())
