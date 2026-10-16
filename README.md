# kalopetrides-geo

Audit tecnico onsite e analisi della concorrenza su Google per Kalopetrides Law LLC (kalopetrideslaw.com). Rilevazione del 2026-10-05; solo richieste GET verso il sito del cliente. Teardown dei concorrenti (siti e fonti esterne) del 2026-10-08.

## Report

| File | Contenuto |
|---|---|
| `reports/AUDIT_TECNICO_2026-10-05.md` | Audit tecnico (IT): accessibilità, test User-Agent, pagine, form, sitemap; ogni punto rimanda a `data/site/` |
| `reports/SERP_CONCORRENZA_2026-10-05.md` | Parte B (IT): 15 SERP raccolte il 06/10 (5 query × EN/DE/RU), domini ricorrenti, giudizio sulla difficoltà; storico dei 403 |
| `reports/KALOPETRIDES_WEBSITE_REVIEW_2026-10-05.md` | Review per il cliente (EN, non tecnica) |
| `reports/KALOPETRIDES_WEBSITE_REVIEW_2026-10-05.docx` | Stessa review in Word |
| `reports/CONCORRENTI_SITI_2026-10-08.md` | Teardown concorrenti, Parte A: siti di 8 studi (struttura, lingue, pagine servizio, crawler, contatti) |
| `reports/CONCORRENTI_FONTI_2026-10-08.md` | Parte B: matrice studi × fonti, schede delle fonti, liste "da prendere" e "da meritare" |
| `reports/CONCORRENTI_SINTESI_2026-10-08.md` | Parte C: sintesi (40 righe) — sito o fonti, caso Philippou, requisiti, 5 fonti prioritarie |

## Dati

| Path | Contenuto |
|---|---|
| `data/site/*.txt` | Risposte HTTP grezze (header + corpo), un file per richiesta: `<url>__<user-agent>[__<tentativo>].txt` |
| `data/site/_index.csv` | Prima passata: url, status, bytes, title, canonical, robots-meta, x-robots-tag, sg-captcha, user-agent, file |
| `data/site/_ua_matrix_rounds.csv` | Tre tornate del test User-Agent su home e privacy-policy.html |
| `data/site/_page_attempts.csv`, `_page_attempts_2.csv` | Tentativi GET ripetuti per pagina (sfida anti-bot intermittente) + quarta tornata UA |
| `data/site/_ua_tally.csv` | Esito di ogni richiesta del test UA (base della tabella UA × status) |
| `data/site/_analysis.json` | Analisi strutturata delle pagine 200 (meta, canonical, hreflang, OG, JSON-LD, titoli, parole, immagini, link, form, script) |
| `data/serp/_first_call_request.json` | Prima richiesta Serper inviata (05/10) |
| `data/serp/_first_call_403.json` | Risposta 403 "Unauthorized" di Serper (05/10) |
| `data/serp/_rerun_2026-10-06_403.json` | Risposta 403 alla riesecuzione di `serp_run.py` (06/10) |
| `data/serp/_debug.txt` | Ultima risposta 403 di Serper (06/10, prima della riuscita), nessun valore di chiave |
| `data/serp/q{n}_{gl}_{hl}.json` | 15 risposte Serper (top 10 organici) del 06/10 |
| `data/competitors/<dominio>/` | HTML grezzo (header in commento iniziale) dei siti concorrenti, 08/10; `_requests.csv` = ogni GET; `_sitemap_urls.json` = URL dalle sitemap |
| `data/competitors/serper/*.json`, `_serper_calls.csv` | Risposte e registro delle chiamate Serper del teardown (54 su 80) |
| `data/competitors/_pages_analysis.jsonl`, `_content_words.csv` | Metriche per pagina (parole, H2, FAQ, JSON-LD, hreflang, fonti esterne, contatti) |
| `data/competitors/_presenze_serper.csv` | Ogni risultato Serper attribuito a uno studio e a una fonte |
| `data/sources/<dominio>/` | Pagine delle fonti (directory, classifiche, enti) aperte per capire come ci si entra; PDF dell'elenco avvocati dell'Ambasciata USA. Nelle due pagine di globallawexperts.com un token Mapbox pubblico del sito è stato oscurato (blocco push protection di GitHub) |

## Script

| File | Funzione |
|---|---|
| `scripts/fetch_site.py` | Prima passata GET: pagine, robots, sitemap, llms.txt, matrice UA, redirect |
| `scripts/fetch_site_lib.py` | Funzione `get()` condivisa (curl, salvataggio grezzo, estrazione title/canonical/robots) |
| `scripts/fetch_retry.py`, `fetch_retry2.py`, `fetch_retry3.py` | GET ripetuti per le pagine ricevute come challenge; redirect http/www |
| `scripts/fetch_assets.py` | GET di `i18n.js` e `main.js` (lingua, form, contatori, bio) |
| `scripts/analyze_pages.py` | Genera `data/site/_analysis.json` |
| `scripts/ua_tally.py` | Genera `data/site/_ua_tally.csv` |
| `scripts/serp_run.py` | Le 15 chiamate Serper della Parte B (`--prova` = una sola; salta quelle già fatte; si ferma al primo 4xx) |
| `scripts/md_to_docx.py` | Conversione Markdown → DOCX (python-docx) |
| `scripts/competitors/crawl_lib.py` | GET educato: robots.txt, ≥2,5 s per dominio, max 40 richieste, salvataggio grezzo |
| `scripts/competitors/step1.py`, `step2.py`, `fetch_sources.py` | Robots/home/GPTBot/sitemap; pagine campione; pagine delle fonti |
| `scripts/competitors/serper.py`, `presence.py`, `presence_firm.py`, `consolidate.py` | Chiamate Serper con budget 80 e registro; ricerche di presenza; consolidamento |
| `scripts/competitors/analyze.py`, `content_words.py`, `blog_dates.py`, `snip.py` | Analisi pagine, parole senza boilerplate, date blog, estratti di testo |
