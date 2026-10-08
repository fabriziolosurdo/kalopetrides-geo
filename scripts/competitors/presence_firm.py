"""Presenza di uno studio sulle fonti: query '"nome" (site:a OR site:b ...)'. Uso: presence_firm.py <nome_file> <nome tra virgolette>"""
import sys, collections
from urllib.parse import urlparse
sys.path.insert(0, "scripts/competitors")
from serper import search
SITES = ["legal500.com", "chambers.com", "lawzana.com", "cypruslawyers.co.uk", "globallawexperts.com", "iflr.com",
         "lawyersincyprus.com", "mondaq.com", "cypruslaw.com", "legalhelpcy.com", "lexology.com", "cyprusbarassociation.org", "cy.usembassy.gov"]
name, q = sys.argv[1], sys.argv[2]
d = search(name, "cy", "en", 20, q + " (" + " OR ".join("site:" + s for s in SITES) + ")")
c = collections.Counter(urlparse(o["link"]).netloc.replace("www.", "") for o in d.get("organic", []))
print(q, dict(c))
