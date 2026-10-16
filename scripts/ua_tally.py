"""Tally of every GET to https://kalopetrideslaw.com/ and /privacy-policy.html per User-Agent, from raw files."""
import re, pathlib, collections, csv
rows = collections.OrderedDict()
order = ["browser","googlebot","bingbot","gptbot","claudebot","perplexitybot","oai-searchbot","google-extended","ccbot"]
for ua in order: rows[ua] = collections.Counter()
detail = []
for f in sorted(pathlib.Path("data/site").glob("https_kalopetrideslaw_com_*.txt")):
    m = re.match(r"https_kalopetrideslaw_com(_privacy_policy_html)?__([a-z-]+)(?:__.*)?\.txt$", f.name)
    if not m: continue
    page = "/" if not m.group(1) else "/privacy-policy.html"; ua = m.group(2)
    raw = f.read_text(errors="replace")
    st = re.search(r"<<<CURL status=(\d+)", raw).group(1)
    ch = bool(re.search(r"^sg-captcha:\s*challenge", raw, re.I|re.M))
    key = "200 (page served)" if st=="200" and not ch else (f"{st} challenge" if ch else st)
    rows[ua][key] += 1; detail.append((ua, page, key, f.name))
with open("data/site/_ua_tally.csv","w",newline="") as fh:
    w = csv.writer(fh); w.writerow(["user_agent","page","result","file"]); w.writerows(detail)
for ua,c in rows.items(): print(ua, sum(c.values()), dict(c))
