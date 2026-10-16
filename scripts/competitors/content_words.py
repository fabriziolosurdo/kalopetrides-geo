"""Parole di contenuto per pagina: testo del body meno le stringhe 'boilerplate' (presenti in >=60%
delle pagine HTML 200 dello stesso dominio, es. menu, footer, banner). Scrive data/competitors/_content_words.csv."""
import collections, csv, glob, re, sys
from bs4 import BeautifulSoup
rows = []
for dom in sorted(glob.glob("data/competitors/*/")):
    pages = {}
    for f in glob.glob(dom + "*.html"):
        if re.search(r"robots_txt|sitemap|llms_txt|__gptbot|__r2", f): continue
        raw = open(f, errors="replace").read()
        if "\nstatus 200\n" not in raw[:600]: continue
        soup = BeautifulSoup(raw.split("-->\n", 1)[-1], "lxml")
        for t in soup(["script", "style", "noscript", "svg", "template"]): t.decompose()
        body = soup.body or soup
        pages[f] = [re.sub(r"\s+", " ", s) for s in body.stripped_strings]
    if len(pages) < 4: continue
    df = collections.Counter(s for v in pages.values() for s in set(v))
    thr = 0.6 * len(pages)
    for f, strs in sorted(pages.items()):
        content = [s for s in strs if df[s] < thr]
        rows.append([dom.split("/")[2], f.split("/")[-1], sum(len(s.split()) for s in strs), sum(len(s.split()) for s in content)])
w = csv.writer(open("data/competitors/_content_words.csv", "w", newline=""))
w.writerow(["dominio", "file", "parole_body", "parole_contenuto"]); w.writerows(rows)
for r in rows: print(*r)
