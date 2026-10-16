"""Passo 2: GET di una lista di URL per un dominio (robots.txt rispettato, stesso limite di 40).
Uso: python3 scripts/competitors/step2.py <dominio> <base> <url>... ; un URL con prefisso 'gptbot:' usa lo UA GPTBot."""
import sys
sys.path.insert(0, "scripts/competitors")
from crawl_lib import Site
domain, base, urls = sys.argv[1], sys.argv[2], sys.argv[3:]
s = Site(domain, base)
s.load_robots_from_file = None
import urllib.robotparser, pathlib, re
txt = (s.dir / "robots_txt.html").read_text(errors="replace").split("-->\n", 1)[-1]
s.rp = urllib.robotparser.RobotFileParser(); s.rp.parse(txt.splitlines() if "<html" not in txt.lower()[:200] else [])
for u in urls:
    ua = "browser"
    if u.startswith("gptbot:"): ua, u = "gptbot", u[7:]
    r = s.get(u, ua=ua, tag="r2" if ua == "gptbot" else "")
    print(domain, s.n, u, r[0] if r else "SKIP")
