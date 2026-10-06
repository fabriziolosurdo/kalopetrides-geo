"""A1 quater: plain-GET retries for redirect checks (http/www) and extensionless URLs listed in the sitemap."""
import time, importlib.util
spec = importlib.util.spec_from_file_location("fs", "scripts/fetch_site_lib.py")
fs = importlib.util.module_from_spec(spec); spec.loader.exec_module(fs)
for u in ["http://kalopetrideslaw.com/", "http://www.kalopetrideslaw.com/", "https://www.kalopetrideslaw.com/about-us.html",
          "https://kalopetrideslaw.com/privacy-policy", "https://kalopetrideslaw.com/imprint"]:
    for i in range(1, 6):
        r = fs.get(u, "browser", tag=f"x{i}"); time.sleep(2)
        print(i, r["status"], r["bytes"], r["sg_captcha"], u, r["title"][:40])
        if r["sg_captcha"] != "challenge": break
