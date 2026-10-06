"""Parte B — 15 chiamate Serper (5 query x 3 localizzazioni). NON eseguito il 2026-10-05:
la prima chiamata di prova ha risposto 403 "Unauthorized" (data/serp/_first_call_403.json).
La chiave si legge da SERPER_API_KEY e va nell'header X-API-KEY (passato a curl via stdin,
mai in argv né in output). Le query con un file di risultati valido vengono saltate.
Uso: python3 scripts/serp_run.py  -> scrive data/serp/q{n}_{gl}_{hl}.json"""
import json, os, subprocess, pathlib, sys, time
KEY = os.environ.get("SERPER_API_KEY", "").strip()
if not KEY:
    sys.exit("1. La variabile SERPER_API_KEY non è impostata in questo ambiente: "
             "puoi aggiungerla ai secret dell'ambiente e riavviare la sessione? (nessuna chiamata a Serper eseguita)")
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
        r = subprocess.run(["curl", "-sS", "-m", "60", "-X", "POST", "https://google.serper.dev/search",
                            "-H", "Content-Type: application/json", "-H", "@-", "-d", body],
                           input=f"X-API-KEY: {KEY}\n", capture_output=True, text=True)
        if '"statusCode":403' in r.stdout or '"statusCode":40' in r.stdout:
            (out / "_debug.txt").write_text(f"{time.strftime('%Y-%m-%d %H:%M:%S')} q{n}_{gl}_{hl}\n{r.stdout}\n{r.stderr}")
            sys.exit("Serper ha risposto con errore 4xx — risposta salvata in data/serp/_debug.txt, interrotto.")
        f.write_text(r.stdout)
        print(f, len(r.stdout)); time.sleep(1)
