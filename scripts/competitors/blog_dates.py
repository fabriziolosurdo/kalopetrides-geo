"""Date visibili nelle pagine indice blog/notizie e lastmod delle sitemap articoli."""
import re, sys, datetime, json
from bs4 import BeautifulSoup
M = "Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec|January|February|March|April|June|July|August|September|October|November|December"
PATS = [rf"\b(\d{{1,2}}) ({M})\.?,? (\d{{4}})\b", rf"\b({M})\.? (\d{{1,2}}),? (\d{{4}})\b", r"\b(\d{1,2})[./](\d{1,2})[./](\d{4})\b"]
def parse(s):
    out = []
    for m in re.finditer(PATS[0], s):
        try: out.append(datetime.datetime.strptime(f"{m[1]} {m[2][:3]} {m[3]}", "%d %b %Y").date())
        except ValueError: pass
    for m in re.finditer(PATS[1], s):
        try: out.append(datetime.datetime.strptime(f"{m[2]} {m[1][:3]} {m[3]}", "%d %b %Y").date())
        except ValueError: pass
    for m in re.finditer(PATS[2], s):
        try: out.append(datetime.date(int(m[3]), int(m[2]), int(m[1])))
        except ValueError: pass
    return out
for f in sys.argv[1:]:
    raw = open(f, errors="replace").read().split("-->\n", 1)[-1]
    if "<urlset" in raw:
        ds = sorted({d[:10] for d in re.findall(r"<lastmod>(.*?)</lastmod>", raw)}, reverse=True)
        n = len(re.findall(r"<url>", raw))
        print(f, "url", n, "lastmod piu recenti", ds[:10]); continue
    soup = BeautifulSoup(raw, "lxml")
    for t in soup(["script", "style"]): t.decompose()
    ds = sorted(set(parse(soup.get_text(" "))), reverse=True)
    print(f, "date visibili (10 piu recenti):", [str(d) for d in ds[:10]])
