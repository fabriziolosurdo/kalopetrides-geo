"""A1 bis: the SiteGround challenge is intermittent (depends on the egress IP).
Plain GET only: (1) repeat the UA matrix 3 rounds to measure how often each UA gets
the challenge; (2) retry each page up to 4 times with a browser UA and keep the first 200."""
import csv, time, pathlib, sys
sys.path.insert(0, "scripts")
import importlib.util
spec = importlib.util.spec_from_file_location("fs", "scripts/fetch_site_lib.py")
fs = importlib.util.module_from_spec(spec); spec.loader.exec_module(fs)
OUT = pathlib.Path("data/site")
rows = []
for rnd in (1, 2, 3):
    for ua in fs.UAS:
        for p in ["", "privacy-policy.html"]:
            r = fs.get("https://kalopetrideslaw.com/"+p, ua, tag=f"r{rnd}"); r["round"] = rnd; rows.append(r); time.sleep(1)
with open(OUT/"_ua_matrix_rounds.csv","w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
pages = ["", "robots.txt", "llms.txt", "about-us.html", "services-overview.html", "trustgate.html",
         "csr.html", "imprint.html", "privacy-policy.html", "about-us", "services-overview",
         "index-el.html", "el/", "index.html"]
got = []
for p in pages:
    for i in range(1, 5):
        r = fs.get("https://kalopetrideslaw.com/"+p, "browser", tag=f"try{i}"); r["attempt"] = i; got.append(r); time.sleep(1.5)
        if r["sg_captcha"] != "challenge": break
with open(OUT/"_page_attempts.csv","w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(got[0].keys())); w.writeheader(); w.writerows(got)
for r in got: print(r["attempt"], r["status"], r["bytes"], r["sg_captcha"], r["url"], r["title"][:50])
