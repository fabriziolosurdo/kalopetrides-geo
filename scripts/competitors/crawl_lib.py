"""GET educato verso i siti dei concorrenti.
Regole: solo GET; >= 2,5 s tra due richieste sullo stesso dominio; max 40 richieste per dominio
(robots.txt e sitemap inclusi); robots.txt rispettato per User-agent '*' (ogni URL vietato è annotato
e non scaricato). Ogni risposta grezza (header + corpo) va in data/competitors/<dominio>/,
ogni richiesta in data/competitors/<dominio>/_requests.csv."""
import csv, datetime, hashlib, pathlib, re, time, urllib.robotparser
import requests
from urllib.parse import urlparse
BROWSER = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
GPTBOT = "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; GPTBot/1.1; +https://openai.com/gptbot)"
MAX, DELAY = 40, 2.5
ROOT = pathlib.Path("data/competitors")

def slug(url):
    p = urlparse(url)
    s = re.sub(r"[^A-Za-z0-9]+", "_", (p.path or "/") + ("?" + p.query if p.query else "")).strip("_") or "home"
    if len(s) > 90: s = s[:80] + "_" + hashlib.md5(s.encode()).hexdigest()[:8]
    return s

class Site:
    def __init__(self, domain, base, root=ROOT):
        self.domain, self.base = domain, base.rstrip("/")
        self.dir = pathlib.Path(root) / domain; self.dir.mkdir(parents=True, exist_ok=True)
        self.log = self.dir / "_requests.csv"
        self.n = sum(1 for _ in open(self.log)) - 1 if self.log.exists() else 0
        self.last = 0.0
        self.rp = None
        self.s = requests.Session()

    def _wait(self):
        d = time.time() - self.last
        if d < DELAY: time.sleep(DELAY - d)

    def allowed(self, url):
        return True if self.rp is None else self.rp.can_fetch("*", url)

    def get(self, url, ua="browser", tag="", check_robots=True):
        if check_robots and not self.allowed(url):
            self._row(url, ua, "ROBOTS_DISALLOW", 0, "", "")
            return None
        if self.n >= MAX:
            print(f"[{self.domain}] limite 40 raggiunto, salto {url}"); return None
        self._wait()
        t0 = datetime.datetime.utcnow().isoformat() + "Z"
        try:
            r = self.s.get(url, headers={"User-Agent": BROWSER if ua == "browser" else GPTBOT,
                                         "Accept-Language": "en"}, timeout=40, allow_redirects=True)
            status, body, final = r.status_code, r.text, r.url
            hdrs = "\n".join(f"{k}: {v}" for k, v in r.headers.items())
            hist = " -> ".join(f"{h.status_code} {h.url}" for h in r.history)
            if "pdf" in r.headers.get("content-type", ""):
                (self.dir / (slug(url) + ".pdf")).write_bytes(r.content); body = "(PDF salvato come .pdf)"
        except Exception as e:
            status, body, final, hdrs, hist = "ERR", "", url, str(e), ""
        self.last = time.time(); self.n += 1
        fn = self.dir / f"{slug(url)}{'__'+ua if ua!='browser' else ''}{'__'+tag if tag else ''}.html"
        fn.write_text(f"<!-- GET {url}\nUA {ua}\nfetched {t0}\nstatus {status}\nfinal {final}\nredirects {hist}\n{hdrs}\n-->\n{body}", errors="replace")
        self._row(url, ua, status, len(body.encode('utf-8', 'replace')), final, fn.name)
        return status, body, final

    def _row(self, url, ua, status, size, final, fn):
        new = not self.log.exists()
        with open(self.log, "a", newline="") as fh:
            w = csv.writer(fh)
            if new: w.writerow(["utc", "url", "ua", "status", "bytes", "final", "file"])
            w.writerow([datetime.datetime.utcnow().isoformat() + "Z", url, ua, status, size, final, fn])

    def load_robots(self):
        res = self.get(self.base + "/robots.txt", check_robots=False)
        self.rp = urllib.robotparser.RobotFileParser()
        txt = res[1] if res and res[0] == 200 else ""
        self.rp.parse(txt.splitlines())
        return txt
