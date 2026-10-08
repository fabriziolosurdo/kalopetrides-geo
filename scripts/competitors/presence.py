"""Presenza degli studi su una fonte: query Serper 'site:<fonte> (nome1 OR nome2 ...)' e conteggio dei risultati per studio.
Uso: presence.py <nome_file> <site-expr>"""
import json, re, sys
sys.path.insert(0, "scripts/competitors")
from serper import search
FIRMS = {"Philippou": r"philippou", "Patrikios": r"patrikios|pavlou", "Konstantinou (GK)": r"konstantinou|gk-law|gk law",
         "Neocleous": r"neocleous", "Chrysostomides": r"chrysostomides", "Demetriades": r"demetriades",
         "Kyprianou": r"kyprianou", "Connor": r"connor", "Kalopetrides": r"kalopetrides"}
Q = '("Philippou Law" OR Patrikios OR Konstantinou OR Neocleous OR Chrysostomides OR "Andreas Demetriades" OR "Michael Kyprianou" OR "Connor Legal" OR Kalopetrides)'
def run(name, site):
    d = search(name, "cy", "en", 20, f"{site} {Q}")
    hits = {k: [] for k in FIRMS}
    for o in d.get("organic", []):
        blob = (o.get("link", "") + " " + o.get("title", "") + " " + o.get("snippet", "")).lower()
        for k, rx in FIRMS.items():
            if re.search(rx, blob): hits[k].append(o["link"])
    return hits
if __name__ == "__main__":
    h = run(sys.argv[1], sys.argv[2])
    print(sys.argv[2], {k: len(v) for k, v in h.items() if v})
