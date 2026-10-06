"""Parte B — 15 chiamate Serper (5 query x 3 localizzazioni). NON eseguito il 2026-10-05:
la prima chiamata di prova ha risposto 403 "Unauthorized" (data/serp/_first_call_403.json).
Se SERPER_API_KEY è impostata va nell'header X-API-KEY (via stdin, mai in argv); se non lo è,
nessuna intestazione di autenticazione: la credenziale per google.serper.dev la inietta il proxy. Le query con un file di risultati valido vengono saltate.
Uso: python3 scripts/serp_run.py [--prova] -> scrive data/serp/q{n}_{gl}_{hl}.json"""
import json, os, subprocess, pathlib, sys, time
KEY = os.environ.get("SERPER_API_KEY", "").strip()
# Senza SERPER_API_KEY nessuna intestazione di autenticazione: la credenziale la inietta il proxy.
AUTH = f"X-API-KEY: {KEY}\n" if KEY else ""
ONLY_ONE = "--prova" in sys.argv  # una sola chiamata di prova
QUERIES = {
 1: {"en": "best real estate lawyers in Cyprus for foreigners buying property",
     "de": "beste Anwälte für Immobilienkauf auf Zypern für Ausländer",
     "ru": "лучшие юристы на Кипре по покупке недвижимости для иностранцев"},
 2: {"en": "corporate lawyers in Cyprus for company formation by non-residents",
     "de": "Anwälte für Firmengründung auf Zypern für Nicht-Residenten",
     "ru": "юристы на Кипре по регистрации компании для нерезидентов"},
 3: {"en": "immigration lawyers in Cyprus for permanent residency by investment",
     "de": "Anwälte für Daueraufenthaltsgenehmigung auf Zypern durch Investition",
     "ru": "иммиграционные юристы на Кипре по ПМЖ за инвестиции"},
 4: {"en": "banking and finance law firms in Cyprus",
     "de": "Kanzleien für Bank- und Finanzrecht auf Zypern",
     "ru": "юридические фирмы на Кипре по банковскому и финансовому праву"},
 5: {"en": "tax lawyers in Cyprus for international tax planning",
     "de": "Steueranwälte auf Zypern für internationale Steuerplanung",
     "ru": "налоговые юристы на Кипре по международному налоговому планированию"},
}
LOCALES = [("cy", "en"), ("de", "de"), ("ru", "ru")]
out = pathlib.Path("data/serp"); out.mkdir(parents=True, exist_ok=True)
for n, q in QUERIES.items():
    for gl, hl in LOCALES:
        f = out / f"q{n}_{gl}_{hl}.json"
        if f.exists() and '"organic"' in f.read_text():
            print(f, "già presente, saltato"); continue
        body = json.dumps({"q": q[hl], "gl": gl, "hl": hl, "num": 10}, ensure_ascii=False)
        cmd = ["curl", "-sS", "-m", "60", "-w", "\n%{http_code}", "-X", "POST", "https://google.serper.dev/search",
               "-H", "Content-Type: application/json", "-d", body]
        if AUTH: cmd[-2:-2] = ["-H", "@-"]
        r = subprocess.run(cmd, input=AUTH, capture_output=True, text=True)
        resp, _, code = r.stdout.rpartition("\n")
        r = subprocess.CompletedProcess(r.args, r.returncode, resp, r.stderr + f"HTTP {code}")
        if code.startswith("4") or '"statusCode":40' in r.stdout:
            (out / "_debug.txt").write_text(f"{time.strftime('%Y-%m-%d %H:%M:%S')} q{n}_{gl}_{hl}\n{r.stdout}\n{r.stderr}")
            sys.exit("Serper ha risposto con errore 4xx — risposta salvata in data/serp/_debug.txt, interrotto.")
        f.write_text(r.stdout)
        print(f, len(r.stdout))
        if ONLY_ONE: sys.exit(0)
        time.sleep(1)
