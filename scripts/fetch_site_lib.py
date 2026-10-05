"""A1: GET-only fetch of kalopetrideslaw.com with several User-Agents.
Saves raw responses (headers + body) to data/site/ and writes data/site/_index.csv."""
import csv, re, subprocess, sys, time, pathlib, datetime
OUT = pathlib.Path("data/site"); OUT.mkdir(parents=True, exist_ok=True)
UAS = {
 "browser": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
 "googlebot": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
 "bingbot": "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
 "gptbot": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; GPTBot/1.1; +https://openai.com/gptbot)",
 "claudebot": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; ClaudeBot/1.0; +claudebot@anthropic.com)",
 "perplexitybot": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot)",
 "oai-searchbot": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; OAI-SearchBot/1.0; +https://openai.com/searchbot)",
 "google-extended": "Google-Extended",
 "ccbot": "CCBot/2.0 (https://commoncrawl.org/faq/)",
}
def slug(url):
    return re.sub(r"[^A-Za-z0-9]+", "_", url).strip("_")
def get(url, ua_key, follow=False, tag=''):
    fn = OUT / f"{slug(url)}__{ua_key}{'__follow' if follow else ''}{'__'+tag if tag else ''}.txt"
    args = ["curl","-sS","-m","40","-D","-","-A",UAS[ua_key],"-w","\n<<<CURL status=%{http_code} bytes=%{size_download} final=%{url_effective} redirects=%{num_redirects}>>>\n"]
    if follow: args += ["-L"]
    r = subprocess.run(args+[url], capture_output=True, text=True, errors="replace")
    raw = f"# GET {url}\n# UA {ua_key}: {UAS[ua_key]}\n# fetched {datetime.datetime.utcnow().isoformat()}Z\n" + r.stdout + r.stderr
    fn.write_text(raw)
    m = re.search(r"<<<CURL status=(\d+) bytes=(\d+)", raw)
    status, size = (m.group(1), m.group(2)) if m else ("ERR","0")
    t = re.search(r"<title>(.*?)</title>", raw, re.S|re.I)
    can = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]*href=["\']([^"\']+)', raw, re.I)
    rob = re.search(r'<meta[^>]+name=["\']robots["\'][^>]*content=["\']([^"\']+)', raw, re.I)
    xr = re.search(r"^x-robots-tag:\s*(.*)$", raw, re.I|re.M)
    cap = "challenge" if re.search(r"^sg-captcha:\s*challenge", raw, re.I|re.M) else ""
    return dict(url=url, status=status, bytes=size, title=(t.group(1).strip() if t else ""),
                canonical=(can.group(1) if can else ""), robots_meta=(rob.group(1) if rob else ""),
                x_robots_tag=(xr.group(1).strip() if xr else ""), sg_captcha=cap, user_agent=ua_key, file=fn.name)
