"""GET di pagine delle fonti (directory, classifiche, enti) in data/sources/<dominio>/, stesse regole del crawler.
Uso: fetch_sources.py <dominio> <base> <url>..."""
import sys
sys.path.insert(0, "scripts/competitors")
from crawl_lib import Site
domain, base, urls = sys.argv[1], sys.argv[2], sys.argv[3:]
s = Site(domain, base, root="data/sources")
if s.rp is None and not (s.dir / "robots_txt.html").exists():
    s.load_robots()
else:
    import urllib.robotparser
    txt = (s.dir / "robots_txt.html").read_text(errors="replace").split("-->\n", 1)[-1]
    s.rp = urllib.robotparser.RobotFileParser(); s.rp.parse(txt.splitlines() if "<html" not in txt.lower()[:300] else [])
for u in urls:
    r = s.get(u)
    print(domain, s.n, u, r[0] if r else "SKIP (robots o limite)", (r[2] if r else ""))
