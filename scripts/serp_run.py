"""Parte B — 15 chiamate Serper (5 query x 3 localizzazioni). NON eseguito il 2026-10-05:
la prima chiamata di prova ha risposto 403 "Unauthorized" (data/serp/_first_call_403.json).
Il proxy dell'ambiente cloud aggiunge da solo l'header X-API-KEY: non inserire chiavi qui.
Uso: python3 scripts/serp_run.py  -> scrive data/serp/q{n}_{gl}_{hl}.json"""
import json, subprocess, pathlib, sys, time
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
        body = json.dumps({"q": q[hl], "gl": gl, "hl": hl, "num": 10}, ensure_ascii=False)
        r = subprocess.run(["curl", "-sS", "-m", "60", "-X", "POST", "https://google.serper.dev/search",
                            "-H", "Content-Type: application/json", "-d", body], capture_output=True, text=True)
        f = out / f"q{n}_{gl}_{hl}.json"; f.write_text(r.stdout)
        if '"statusCode":40' in r.stdout:
            sys.exit(f"Serper ha risposto {r.stdout.strip()} — credenziale non attiva, interrotto.")
        print(f, len(r.stdout)); time.sleep(1)
