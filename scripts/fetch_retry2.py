"""A1 ter: second plain-GET retry pass for pages still challenged, plus a 4th UA-matrix round."""
import csv, time, pathlib, importlib.util
spec = importlib.util.spec_from_file_location("fs", "scripts/fetch_site_lib.py")
fs = importlib.util.module_from_spec(spec); spec.loader.exec_module(fs)
OUT = pathlib.Path("data/site")
got = []
for p in ["robots.txt", "trustgate.html", "trustgate", "llms.txt", "", "about-us.html", "services-overview.html", "csr", "imprint", "privacy-policy"]:
    for i in range(5, 9):
        r = fs.get("https://kalopetrideslaw.com/"+p, "browser", tag=f"try{i}"); r["attempt"] = i; got.append(r); time.sleep(2)
        if r["sg_captcha"] != "challenge": break
for ua in fs.UAS:
    r = fs.get("https://kalopetrideslaw.com/", ua, tag="r4"); r["attempt"] = "r4"; got.append(r); time.sleep(1)
with open(OUT/"_page_attempts_2.csv","w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(got[0].keys())); w.writeheader(); w.writerows(got)
for r in got: print(r["attempt"], r["status"], r["bytes"], r["sg_captcha"], r["user_agent"], r["url"], r["title"][:50])
