"""Passo 1 per dominio: robots.txt, home (browser), home (GPTBot), sitemap (indice + max 5 sotto-sitemap)."""
import re, sys, json, pathlib
sys.path.insert(0, "scripts/competitors")
from crawl_lib import Site
domain, base = sys.argv[1], sys.argv[2]
s = Site(domain, base)
robots = s.load_robots()
s.get(base + "/")
s.get(base + "/", ua="gptbot")
maps = re.findall(r"(?im)^sitemap:\s*(\S+)", robots) or [base + "/sitemap.xml", base + "/sitemap_index.xml"]
seen, urls, queue = set(), [], list(dict.fromkeys(maps))
while queue and len(seen) < 7:
    m = queue.pop(0)
    if m in seen: continue
    seen.add(m)
    r = s.get(m)
    if not r or r[0] != 200: continue
    locs = re.findall(r"<loc>\s*(.*?)\s*</loc>", r[1])
    if "<sitemapindex" in r[1]:
        # preferisci sotto-sitemap di pagine/post/servizi/team
        locs.sort(key=lambda u: (0 if re.search(r"page|post|service|practice|team|people|lawyer|expert|area|news|blog|insight", u, re.I) else 1))
        queue += locs
    else:
        urls += locs
pathlib.Path(f"data/competitors/{domain}/_sitemap_urls.json").write_text(json.dumps({"sitemaps": sorted(seen), "urls": urls}, indent=1))
print(domain, "richieste", s.n, "url in sitemap", len(urls))
