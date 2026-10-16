"""Raccoglie tutti i risultati Serper (data/competitors/serper/*.json), attribuisce ogni URL a uno studio
(per URL/titolo/snippet) e scrive data/competitors/_presenze_serper.csv (fonte, studio, url, titolo, query)."""
import csv, glob, json, re
from urllib.parse import urlparse
FIRMS = {"Philippou": (r"philippou law|philippoulaw|polycarpos philippou", "philippoulaw.com"),
         "Patrikios": (r"patrikios|pavlaw", "pavlaw.com"),
         "Konstantinou/GK": (r"konstantinou|gk-law|gk law", "gk-lawfirm.com"),
         "Neocleous": (r"elias neocleous|neo\.law|elias-neocleous", "neo.law"),
         "Chrysostomides": (r"chrysostomides", "chrysostomides.com"),
         "Demetriades": (r"andreas demetriades|demetriadeslaw|andreas-demetriades", "demetriadeslaw.com"),
         "Kyprianou": (r"michael kyprianou|kyprianou\.com|michael-kyprianou|m-kyprianou", "kyprianou.com"),
         "Connor": (r"connor legal|n\. connor|connorlegal|n-connor", "connorlegalllc.com"),
         "Kalopetrides": (r"savvas kalopetrides|kalopetrides law|kalopetrideslaw|savvas-kalopetrides|kalopetrides-llc|kalopetrides llc", "kalopetrideslaw.com")}
rows = []
for f in sorted(glob.glob("data/competitors/serper/*.json")):
    d = json.load(open(f)); q = d.get("searchParameters", {}).get("q", "")
    for o in d.get("organic", []):
        url = o["link"]; dom = urlparse(url).netloc.lower().replace("www.", "")
        blob = (url + " " + o.get("title", "") + " " + o.get("snippet", "")).lower()
        for k, (rx, own) in FIRMS.items():
            if re.search(rx, blob) and not dom.endswith(own):
                rows.append([dom, k, url, o.get("title", ""), f.split("/")[-1]])
w = csv.writer(open("data/competitors/_presenze_serper.csv", "w", newline=""))
w.writerow(["fonte", "studio", "url", "titolo", "file_serper"])
seen = set()
for r in rows:
    if (r[1], r[2]) in seen: continue
    seen.add((r[1], r[2])); w.writerow(r)
print(len(seen), "righe")
