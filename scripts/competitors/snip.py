"""Stampa frammenti di testo visibile attorno a una regex. Uso: snip.py <regex> <file>..."""
import re, sys
from bs4 import BeautifulSoup
rx = re.compile(sys.argv[1], re.I)
for f in sys.argv[2:]:
    raw = open(f, errors="replace").read().split("-->\n", 1)[-1]
    s = BeautifulSoup(raw, "lxml")
    for t in s(["script", "style", "noscript"]): t.decompose()
    txt = re.sub(r"\s+", " ", s.get_text(" "))
    hits = [txt[max(0, m.start()-110):m.end()+110] for m in rx.finditer(txt)]
    print(f"== {f} ({len(hits)})")
    seen = set()
    for h in hits[:6]:
        if h[:60] in seen: continue
        seen.add(h[:60]); print("  …" + h + "…")
