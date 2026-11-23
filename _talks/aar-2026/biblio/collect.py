"""
collect.py
----------
Collect catalog records for books about Macrina the Younger and Olympias of
Constantinople from three open sources, keep only relevant records, and save
them to records.csv for counting by decade.

Sources (all reachable from this workspace, no keys needed):
  1. Open Library search API   - aggregates library MARC records (LoC and
     many others) and Internet Archive scans; one row per *edition year*.
  2. Internet Archive search   - digitized books, strong for 1500-1923.
  3. Crossref works API        - scholarly books and edited volumes with DOIs,
     strong for 1990s onward.

Relevance rules (applied to title + subtitle + catalog subjects):
  Macrina : the text names Macrina / Makrina / Macrinae (Gregory's Vita
            Macrinae counts: an edition of her Life is a book about her).
            Excluded: people merely named Macrina (authors), the Seattle
            "Macrina Bakery" cookbook, Italian libretti with a character Macrina.
  Olympias: the text names Olympias AND a Christian marker (saint, deaconess,
            Chrysostom, Constantinople, diakonissa, letters/epistulae), OR a
            catalog subject naming "Olympias, Saint". Olympias of Macedon
            (mother of Alexander) is excluded.

Each kept record: source, figure, year, title, author, id.
Duplicates across sources are removed later in count.py.
"""
import csv, json, re, time, urllib.parse, urllib.request

UA = {"User-Agent": "Mozilla/5.0 (bibliographic count script)"}

def get(url, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.load(r)
        except Exception as e:                       # network hiccup: wait and retry
            print("retry", i, e, url[:90]); time.sleep(3 + 3 * i)
    return {}

# ---------------------------------------------------------------- relevance tests
MAC = re.compile(r"\bma[ck]rin(a|ae|e|as)\b|makrina|μακριν", re.I)
MAC_NOISE = re.compile(r"bakery|cafe|café|melodramma|dramma|da cantarsi|libretto|opera", re.I)
OLY = re.compile(r"\bolympia[ds]\b|olimpiade|olympiada|ὀλυμπι", re.I)
OLY_CHR = re.compile(r"saint|\bst\.?\b|sancta|santa|heilige|sainte|deacon|diacon|diakon|chrysost|"
                     r"constantinop|epistul|letters to|lettres|briefe|vita|life of|nectarius|sergia", re.I)
OLY_NOISE = re.compile(r"alexander|macedon|philip|aeacid|epirus|ptolem|cleopatra|roxane", re.I)

def which(text):
    """Return 'Macrina', 'Olympias', 'both' or None for a blob of title+subjects."""
    m = bool(MAC.search(text)) and not MAC_NOISE.search(text)
    o = bool(OLY.search(text)) and bool(OLY_CHR.search(text)) and not OLY_NOISE.search(text)
    if m and o: return "both"
    return "Macrina" if m else "Olympias" if o else None

rows = []
def keep(source, fig, year, title, author, rid):
    if fig and year and 1450 <= int(year) <= 2026:
        rows.append(dict(source=source, figure=fig, year=int(year), title=title.strip(), author=author, id=rid))

# ---------------------------------------------------------------- 1. Open Library
# One query per spelling; each edition year of a work is a publication event.
OL_F = "key,title,subtitle,first_publish_year,publish_year,author_name,subject,person"
for q in ["macrina", "makrina", "macrinae", "olympias chrysostom", "olympias deaconess",
          "olympias saint", "olympias diakonisse", "olympiade chrysostome", "person:olympias", "person:macrina"]:
    page = 1
    while True:
        d = get(f"https://openlibrary.org/search.json?q={urllib.parse.quote(q)}&fields={OL_F}&limit=500&page={page}")
        docs = d.get("docs", [])
        for x in docs:
            blob = " ".join([x.get("title", ""), x.get("subtitle", "")] + x.get("subject", []) + x.get("person", []))
            fig = which(blob)
            # count each distinct edition year once per work
            for y in sorted(set(x.get("publish_year", []) or [x.get("first_publish_year")] if x.get("first_publish_year") else [])):
                keep("openlibrary", fig, y, x.get("title", ""), "; ".join(x.get("author_name", [])[:2]), x["key"])
        if len(docs) < 500: break
        page += 1
    print("OL", q, len(rows))

# ---------------------------------------------------------------- 2. Internet Archive
for q in ['title:(macrina OR makrina OR macrinae) AND mediatype:texts',
          'subject:(macrina) AND mediatype:texts',
          'title:(olympias OR olympiade) AND mediatype:texts',
          'subject:(olympias) AND mediatype:texts']:
    d = get("https://archive.org/advancedsearch.php?" + urllib.parse.urlencode(
        {"q": q, "fl[]": ["identifier", "title", "creator", "year", "date", "subject"], "rows": 2000, "output": "json"}, doseq=True))
    for x in d.get("response", {}).get("docs", []):
        subj = x.get("subject", []); subj = subj if isinstance(subj, list) else [subj]
        title = x.get("title", ""); title = title if isinstance(title, str) else " ".join(title)
        y = x.get("year") or (x.get("date") or "")[:4]
        y = re.match(r"\d{4}", str(y)); y = y.group(0) if y else None
        cr = x.get("creator", ""); cr = cr if isinstance(cr, str) else "; ".join(cr[:2])
        keep("archive", which(title + " " + " ".join(subj)), y, title, cr, x["identifier"])
    print("IA", q[:40], len(rows))

# ---------------------------------------------------------------- 3. Crossref (books only)
for q in ["Macrina", "Makrina", "Olympias Chrysostom", "Olympias deaconess"]:
    cursor = "*"
    for _ in range(6):                                   # up to 6 x 1000 records per query
        d = get("https://api.crossref.org/works?" + urllib.parse.urlencode(
            {"query.bibliographic": q, "filter": "type:book,type:monograph,type:edited-book",
             "rows": 1000, "cursor": cursor, "select": "DOI,title,subtitle,author,issued,subject,type"}))
        items = d.get("message", {}).get("items", [])
        for x in items:
            title = " ".join(x.get("title", []) + x.get("subtitle", []))
            y = (x.get("issued", {}).get("date-parts") or [[None]])[0][0]
            au = "; ".join(f"{a.get('family','')}" for a in x.get("author", [])[:2])
            keep("crossref", which(title + " " + " ".join(x.get("subject", []))), y, title, au, x["DOI"])
        cursor = d.get("message", {}).get("next-cursor")
        if len(items) < 1000 or not cursor: break
    print("CR", q, len(rows))

with open("records.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["source", "figure", "year", "title", "author", "id"])
    w.writeheader(); w.writerows(rows)
print("saved", len(rows))
