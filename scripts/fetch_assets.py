"""A1/A2/A3: plain GET of the site's JS files (language switcher, form handler, counters)."""
import time, importlib.util
spec = importlib.util.spec_from_file_location("fs", "scripts/fetch_site_lib.py")
fs = importlib.util.module_from_spec(spec); spec.loader.exec_module(fs)
for u in ["https://kalopetrideslaw.com/assets/js/i18n.js?v=20260912-1455", "https://kalopetrideslaw.com/assets/js/main.js"]:
    for i in range(1, 6):
        r = fs.get(u, "browser", tag=f"a{i}"); time.sleep(2)
        print(i, r["status"], r["bytes"], r["sg_captcha"], u)
        if r["sg_captcha"] != "challenge": break
