# kalopetrides-geo

Audit tecnico onsite e analisi della concorrenza su Google per Kalopetrides Law LLC (kalopetrideslaw.com). Rilevazione del 2026-10-05; solo richieste GET verso il sito del cliente.

## Report

| File | Contenuto |
|---|---|
| `reports/AUDIT_TECNICO_2026-10-05.md` | Audit tecnico (IT): accessibilità, test User-Agent, pagine, form, sitemap; ogni punto rimanda a `data/site/` |
| `reports/SERP_CONCORRENZA_2026-10-05.md` | Parte B (IT): non eseguita (Serper 403); query EN/DE/RU pronte per la riesecuzione |
| `reports/KALOPETRIDES_WEBSITE_REVIEW_2026-10-05.md` | Review per il cliente (EN, non tecnica) |
| `reports/KALOPETRIDES_WEBSITE_REVIEW_2026-10-05.docx` | Stessa review in Word |

## Dati

| Path | Contenuto |
|---|---|
| `data/site/*.txt` | Risposte HTTP grezze (header + corpo), un file per richiesta: `<url>__<user-agent>[__<tentativo>].txt` |
| `data/site/_index.csv` | Prima passata: url, status, bytes, title, canonical, robots-meta, x-robots-tag, sg-captcha, user-agent, file |
| `data/site/_ua_matrix_rounds.csv` | Tre tornate del test User-Agent su home e privacy-policy.html |
| `data/site/_page_attempts.csv`, `_page_attempts_2.csv` | Tentativi GET ripetuti per pagina (sfida anti-bot intermittente) + quarta tornata UA |
| `data/site/_ua_tally.csv` | Esito di ogni richiesta del test UA (base della tabella UA × status) |
| `data/site/_analysis.json` | Analisi strutturata delle pagine 200 (meta, canonical, hreflang, OG, JSON-LD, titoli, parole, immagini, link, form, script) |
| `data/serp/_first_call_request.json` | Unica richiesta Serper inviata |
| `data/serp/_first_call_403.json` | Risposta 403 "Unauthorized" di Serper |

## Script

| File | Funzione |
|---|---|
| `scripts/fetch_site.py` | Prima passata GET: pagine, robots, sitemap, llms.txt, matrice UA, redirect |
| `scripts/fetch_site_lib.py` | Funzione `get()` condivisa (curl, salvataggio grezzo, estrazione title/canonical/robots) |
| `scripts/fetch_retry.py`, `fetch_retry2.py`, `fetch_retry3.py` | GET ripetuti per le pagine ricevute come challenge; redirect http/www |
| `scripts/fetch_assets.py` | GET di `i18n.js` e `main.js` (lingua, form, contatori, bio) |
| `scripts/analyze_pages.py` | Genera `data/site/_analysis.json` |
| `scripts/ua_tally.py` | Genera `data/site/_ua_tally.csv` |
| `scripts/serp_run.py` | Le 15 chiamate Serper della Parte B (non eseguite) |
| `scripts/md_to_docx.py` | Conversione Markdown → DOCX (python-docx) |
