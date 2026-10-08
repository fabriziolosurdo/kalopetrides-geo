# Teardown concorrenti — Parte A: i siti

Data rilevazione: 2026-10-08, 14:41–14:55 UTC. Metodo: solo GET (`requests`, script in `scripts/competitors/`), robots.txt letto per primo e rispettato per `User-agent: *`, almeno 2,5 s tra due richieste sullo stesso dominio, massimo 40 richieste per dominio (robots, sitemap e test GPTBot inclusi). Nessun form, nessun POST. HTML grezzo con header in `data/competitors/<dominio>/`, registro di ogni richiesta in `data/competitors/<dominio>/_requests.csv`, metriche in `data/competitors/_pages_analysis.jsonl` e `data/competitors/_content_words.csv`.

Richieste per dominio: philippoulaw.com 27 · pavlaw.com 23 · kyprianou.com 23 · connorlegalllc.com 22 · demetriadeslaw.com 20 · gk-lawfirm.com 18 · neo.law 17 · chrysostomides.com 6.

## Due correzioni al brief

1. **"George K. Konstantinou LLC" (n. 3) e "GK Law Firm" (n. 9) sono lo stesso studio**: la ricerca Serper sul nome restituisce `gk-lawfirm.com` in prima posizione, e il sito, il `llms.txt` e la Legal 500 lo chiamano "George K. Konstantinou Law Firm" (ragione sociale George K. Konstantinou LLC, HE321623, Limassol). Gli studi distinti sono quindi **otto**; nelle tabelle compare una sola riga "Konstantinou / GK".
2. **Patrikios Legal = pavlaw.com** (ragione sociale Patrikios Pavlou & Associates LLC, Limassol), trovato con Serper.

## Come leggere i numeri

- **Pagine**: URL nelle sitemap XML scaricate (non è un crawl completo). Dove il sito ha più sitemap per lingua è indicato.
- **Parole**: "parole di contenuto" = testo visibile del `<body>` meno le stringhe che si ripetono in almeno il 60% delle pagine 200 dello stesso dominio (menu, footer, banner). Per le pagine tradotte il valore è sovrastimato (il loro menu tradotto non si ripete altrove).
- **FAQ**: "sì" se c'è un titolo FAQ visibile e/o lo schema `FAQPage` nel JSON-LD; è indicato quale dei due.
- **Data visibile**: testo tipo "Updated: …" nella pagina. `article:modified_time` (metadato non visibile) è indicato a parte.
- **Fonti esterne**: link a gov.cy, cylaw.org, companies.gov.cy, centralbank.cy, mof.gov.cy, dls.moi.gov.cy, Cyprus Bar Association, EUR-Lex.
- **Cadenza**: dalle 10 date più recenti visibili sull'indice blog/notizie (o dai `lastmod` della sitemap articoli, che possono essere date di aggiornamento e non di pubblicazione).

## Tabella riassuntiva

| # | Studio (sede) | Dominio | Pagine in sitemap | Pagine servizio EN | Persone (pagine) | Articoli · ultimo | Lingue con URL proprio | hreflang | FAQ + JSON-LD servizi | llms.txt | Home con UA GPTBot | WhatsApp / Telegram | Sedi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Philippou Law Firm (Paphos) | philippoulaw.com | 133 pagine EN + 232 articoli EN; 128 pagine tradotte per ciascuna delle altre 12 lingue | 38 URL `/service/…` | 49 (`/about-us/<nome>`) | 232 · 25/09/2026 | 13: en, el, de, es, it, fr, ru, pl, ro, nl, pt, sv, da | sì (HTML + sitemap) | sì (FAQPage su tutte e 5) + LegalService/Service | sì | 200, pagina vera | sì / no | 1 (Paphos) + pagine "lawyer-in" per Larnaca, Limassol, Nicosia |
| 2 | Patrikios Legal (Limassol) | pavlaw.com | 557 (297 news, 180 pubblicazioni, 50 persone) | 10 aree | 49–50 (`/team/<nome>`) | 180 pubblicazioni · 03/07/2026; news fino all'08/10/2026 | 1: en | no | no FAQ; solo schema Yoast generico | no (404) | 200, pagina vera | no / no | 1 (Limassol) |
| 3+9 | George K. Konstantinou / GK Law Firm (Limassol) | gk-lawfirm.com | 177 (≈78 EN, 63 RU, 36 EL) | 22 URL `practice-areas` | 8 | 29 pubblicazioni EN · aggiornate fino all'08/10/2026 | 3: en, el (`/gr/`), ru | sì | sì (FAQPage + titolo FAQ) + LegalService/Service | sì (4.429 parole) | 200, pagina vera | sì / sì (+ Viber) | 1 (Limassol) |
| 4 | Elias Neocleous & Co (Limassol) | neo.law | 1.721 (1.031 news, 591 pubblicazioni, 71 persone) | 16 aree `expertise` | 71 | 591 pubblicazioni · 29/09/2026 | 1: en | no | FAQPage nel JSON-LD, nessuna FAQ visibile trovata; LegalService/Service | sì | 200, pagina vera | no / no | 7 (Limassol, Nicosia, Paphos, Kiev, Bruxelles, Budapest, Praga) |
| 5 | Chrysostomides (Nicosia) | chrysostomides.com | **non verificato** | non verificato | non verificato | non verificato | non verificato | non verificato | non verificato | non verificato | **403, challenge Cloudflare** | non verificato | non verificato |
| 6 | Andreas Demetriades & Co (Paphos) | demetriadeslaw.com | 82 (46 post, 36 pagine; le versioni /de/ /ru/ non sono in sitemap) | ≈20 (vedi scheda); nessuna pagina tax | 10 | 46 · 10/02/2026 visibile (lastmod sitemap fino al 23/07/2026) | en + traduzioni GTranslate (/de/, /ru/, ebraico) | no | no FAQ, nessun JSON-LD sulle pagine servizio | no (404) | **403 (Apache "Forbidden")** | sì / no | 1 (Paphos) |
| 7 | Michael Kyprianou (Nicosia, Limassol, Paphos + 8 sedi estere) | kyprianou.com | 1.578 (≈1.006+ post, 239 tag; de 47, zh 42, el 15, he 7, ru 7) | pagine per paese; per Cipro ≥ 11 (nessuna immigration trovata) | ≈70 nominativi sulla pagina People; pagine personali non verificate | >1.000 · 06/10/2026 | 6: en, el, ru, de, he, zh-hans (sottoinsieme tradotto) | sì | no FAQ; JSON-LD solo `WebSite` | no (404) | 200, pagina vera | no / no | 11 (Limassol, Nicosia, Paphos, Atene, Londra, Kyiv, Dubai, Varsavia, Malta, Tel Aviv, Francoforte) |
| 8 | Connor Legal (Nicosia) | connorlegalllc.com | 138 (96 post) | 12 aree + pagine "money" (es. `property-lawyer-in-cyprus`) | nessuna pagina persona; solo il fondatore in About | 96 · 10/09/2026 | 47 lingue via GTranslate (incl. de, ru) | sì (47) | no FAQ nella pagina; JSON-LD ricco (LegalService, Person, AggregateRating, Service) | sì (generato da Yoast) | 200, pagina vera | no / no | 1 (Nicosia) |
| — | *Kalopetrides (per confronto, audit 05/10)* | kalopetrideslaw.com | 7 pagine | 0 (9 sezioni in una pagina) | 0 (bio in modale JS) | 0 | 1 (greco solo via JS) | no | no | no (404) | 202 challenge SiteGround nell'80% delle GET | — | 1 (Larnaca) |

## Schede per studio

### 1. Philippou Law Firm — philippoulaw.com

**Struttura.** Sitemap indice con 26 sotto-sitemap (pagine + articoli per 13 lingue). EN: 133 pagine + 232 articoli. Servizi: 38 URL sotto `/service/` (corporate, company incorporation, trust, licenze EMI/CASP/gaming, immigrazione con pagine per Yellow Slip, Pink Slip, PR by investment, cittadinanza, Blue Card; tax per persone fisiche, non-dom, IP box; real estate con acquisto, vendita, locazioni; wills, probate, litigation, family). In più: 7 calcolatori (`/calculators/…`: imposta sul reddito, società, affitti, costo trasferimento immobile, plusvalenze, residenza fiscale, risparmio non-dom), 5 pagine `/compare/`, 4 pagine `/pricing/`, una `editorial-policy`, 5 pagine locali `lawyer-in-<città>`.
**Persone.** 49 schede. Esempio `about-us/polycarpos-philippou`: ruolo (Founding Partner), aree, formazione (LL.B. Atene 1979), "Bar Admissions & Memberships: Cyprus Bar Association", lingue (greco, inglese). La pagina About elenca 5 partner, 14 legali, 14 amministrativi.
**Blog.** 232 articoli EN in sitemap. I 10 `lastmod` più recenti vanno dal 21/08 al 25/09/2026 (≈ 2 a settimana, se coincidono con la pubblicazione); l'indice mostra 25/09, 06/09, 05/09, 04/09, 03/09/2026.
**Lingue.** 13 lingue, ciascuna con URL proprio (`/de/…`, `/ru/…`) e hreflang sia nell'HTML sia nella sitemap; 128 delle 133 pagine EN hanno la versione in ogni lingua. Indizi sulla traduzione: titoli e testi localizzati, non calchi ("Daueraufenthalt in Zypern: Wege & Kosten"; la pagina RU immigrazione ha 14 H2 contro i 13 dell'originale e un lessico naturale). Nel codice c'è un componente `GTranslateRedirectTracker`: indizio di una precedente versione GTranslate reindirizzata. Giudizio sulla qualità: non verificato.
**Pagine campione (EN).**

| Servizio | URL | Parole | H2 | FAQ | Data visibile | Fonti esterne | JSON-LD | Lingue / nazionalità citate | Riforma 2026 |
|---|---|---|---|---|---|---|---|---|---|
| Real estate | `/service/real-estate-and-property-in-cyprus` | 1.429 | 10 | sì (visibile + FAQPage) | no | 0 | Service, FAQPage, BreadcrumbList, WebPage | Greek, English / foreigners, foreign buyers, EU, non-EU | — |
| Corporate | `/service/corporate` | 1.465 | 10 | sì (visibile + FAQPage) | no | 0 | idem | — | — |
| Immigration | `/service/immigration` | 3.355 | 13 | sì (visibile + FAQPage) | no | 0 | + LegalService, Person, AggregateOffer | British, EU citizens, non-EU, third-country nationals | — |
| Banking & finance | nessuna pagina dedicata; la più vicina è `/service/corporate-bank-account` | 2.247 | 14 | sì | "17 March 2025" | 3 (cylaw ×2, companies.gov.cy) | Service, FAQPage | — | — |
| Tax | `/service/tax-services-for-individuals-in-cyprus` | 2.376 | 10 | sì ("Questions before you instruct us" + FAQPage) | no | 0 | + LegalService, Person, AggregateOffer | — | **sì**: regola dei 60 giorni "since the 2026 reform", prima fascia esente €22.000 "from the 2026 tax year", SDC sugli affitti abolita "from 2026", cripto all'8% |

**Crawler.** robots.txt: `User-agent: *` Allow `/`, Disallow `/api`, con `Content-Signal: ai-train=no, search=yes, ai-input=yes`; un secondo blocco autorizza esplicitamente OAI-SearchBot, ChatGPT-User, Claude-SearchBot, Claude-User, PerplexityBot, Perplexity-User, Google-Extended, Bingbot, Amazonbot. GPTBot e ClaudeBot non sono nominati e ricadono in `*` (consentiti). Home con UA GPTBot: 200, 475.486 byte, identica a quella servita al browser. `llms.txt` presente (888 parole, indice di servizi e guide).
**Contatti.** WhatsApp (`wa.me/35726822122`, anche con messaggio precompilato) e Messenger; Telegram no. Una sede (Paphos); le pagine `lawyer-in-larnaca` ecc. non indicano altre sedi.
**Altro visibile in home.** "4.9 · 366+ Google Reviews"; loghi "Featured in": Daily Mail, The Telegraph, Yahoo Finance, Mondaq, Expat Network; logo "Chambers Global Practice Guides: Debt Finance 2026, Cyprus".

### 2. Patrikios Legal — pavlaw.com

**Struttura.** 557 URL: 297 news, 180 pubblicazioni, 50 persone, 11 aree di pratica (10 + indice), 5 pagine "about". Aree: real estate/trust/asset protection, dispute resolution, corporate/M&A, banking & finance, restructuring, direct & indirect tax, capital markets, private client, ship & aircraft finance, regulatory/sanctions. **Nessuna pagina immigrazione** (la pagina private client, 400 parole, non menziona residenza o immigrazione).
**Persone.** 49 link sulla pagina People. Scheda campione (`team/stylianos-trillides`): ruolo (Partner – Commercial and Real Estate), email, telefono, bio, "Admitted to the Cyprus Bar Association, 2012", memberships, raccomandazioni nelle classifiche. Lingue parlate: non indicate nella scheda.
**Blog.** Pubblicazioni: 10 più recenti dal 11/03 al 03/07/2026 (≈ 0,6 a settimana). News: `lastmod` più recente 08/10/2026.
**Lingue.** Solo inglese. Nessun hreflang, nessun URL di lingua (nel codice compaiono riferimenti WPML, senza versioni pubblicate trovate).
**Pagine campione (EN).**

| Servizio | URL | Parole | H2 | FAQ | Data | Fonti | JSON-LD | Lingue / nazionalità | Riforma 2026 |
|---|---|---|---|---|---|---|---|---|---|
| Real estate | `/practice-areas/real-estate-trusts-asset-protection/` | 1.227 | 7 | no | no (modified 23/05/2025) | 0 | WebPage, Breadcrumb, Organization, WebSite (Yoast) | — / non-EU | — |
| Corporate | `/practice-areas/corporate-commercial-and-ma/` | 993 | 13 | no | no (modified 24/09/2026) | 0 | idem | German, Greek / German | — |
| Immigration | nessuna pagina | — | — | — | — | — | — | — | — |
| Banking & finance | `/practice-areas/banking-finance/` | 869 | 9 | no | no (modified 24/09/2026) | 0 | idem | English, French, Greek / American | — |
| Tax | `/practice-areas/direct-and-indirect-tax-law/` | 1.461 | 8 | no | no (modified 24/09/2026) | 0 | idem | Greek | **no** |

**Crawler.** robots.txt Yoast: `User-agent: *` / `Disallow:` vuoto (tutto consentito), nessuna regola per bot AI. GPTBot: 200, 207.574 byte, identica. `llms.txt`: 404.
**Contatti.** Nessun WhatsApp/Telegram. Una sede (Limassol).

### 3 + 9. George K. Konstantinou / GK Law Firm — gk-lawfirm.com

**Struttura.** Una sitemap (`gk-sitemap.xml`, 177 URL): EN ≈ 78 (22 aree di pratica con sottopagine, 29 pubblicazioni, 9 persone, guide di primo livello come `divorce-in-cyprus`, `cyprus-tax-residency`), RU 63, EL 36. Aree: immobiliare, immigrazione (con sottopagine PR, Pink Slip, permesso di lavoro, Yellow Slip, Blue Card, residenza per investimento, categoria F), diritto societario + costituzione, tax, famiglia, contenzioso, danni alla persona, successioni, IP, cittadinanza.
**Persone.** 8 schede. Campione (`people/george-konstantinou`): ruolo (Founder, Legal Consultant), contatti, LinkedIn, bio, formazione (LLB Salonicco 1981), aree. Lingue e iscrizione all'ordine non nella scheda; il `llms.txt` dichiara "Regulator: Cyprus Bar Association, Limassol Bar Association" e "Working languages: Greek, English, Russian".
**Blog.** 29 pubblicazioni EN in sitemap. L'indice e la sitemap mostrano date dal 27/09 all'08/10/2026, ma sulle pagine sono etichettate "Updated": misurano gli aggiornamenti, non le nuove pubblicazioni. Cadenza di pubblicazione: non verificata.
**Lingue.** en, el (`/gr/`), ru, con hreflang (`x-default`, `en`, `el`, `ru`). In russo 25 pagine `praktiki` con slug traslitterati (`/ru/praktiki/nalogi-na-kipre/`): quasi tutti i servizi sono tradotti. Indizi: testo russo naturale e adattato (la pagina tax RU ha 9 H2 contro i 7 dell'EN), quindi non una traduzione automatica letterale.
**Pagine campione (EN).**

| Servizio | URL | Parole | H2 | FAQ | Data visibile | Fonti | JSON-LD | Lingue / nazionalità | Riforma 2026 |
|---|---|---|---|---|---|---|---|---|---|
| Real estate | `/practice-areas/cyprus-property-real-estate-lawyers-in-limassol/` | 2.730 | 8 | sì (visibile + FAQPage) | "Updated: October 04, 2026" | 0 | LegalService, Service, FAQPage, Organization… | — / EU, non-EU, expats, foreigners | — |
| Corporate | `/practice-areas/cyprus-companies-law/` | 1.902 | 8 | sì | "October 05, 2026" | 3 (companies.gov.cy ×2, cylaw.org) | + Article | English, Greek | — |
| Immigration | `/practice-areas/immigration-law/` | 2.864 | 7 | sì | "October 04, 2026" | 5 (companies.gov.cy, gov.cy/bsc, gov.cy) | + ItemList | English, Greek, Russian / Russian, non-EU, third-country nationals | — |
| Banking & finance | nessuna pagina; la più vicina è `/publications/how-to-open-cyprus-bank-account/` | 3.905 | 8 | sì | "September 26, 2026" | 1 (centralbank.cy) | + Article, Person | English, Greek / British, EU, non-EU… | — |
| Tax | `/practice-areas/cyprus-tax/` | 764 | 7 | sì | "July 19, 2026" | 0 | LegalService, Service, FAQPage | — | **sì**: "what changed in the 2026 reform", "incorporation test that applies from the 2026 tax year", nuovi poteri del Tax Department; rimanda alla guida `publications/cyprus-tax-system/` (3.221 parole) |

**Crawler.** robots.txt blocca solo bot SEO e archivi (ia_archiver, AhrefsBot, DotBot, rogerbot, Scrapy, OnCrawl, MJ12bot, Botify) e alcune cartelle tecniche; nessun blocco per i bot AI. GPTBot: 200, 132.537 byte, identica. `llms.txt` presente e lungo (4.429 parole): ragione sociale, numero di registrazione, ordine, indirizzo, orari, lingue, tariffe, indice di tutte le pagine nelle tre lingue.
**Contatti.** WhatsApp (`wa.me/35799929393`), Telegram (`telegram.me/GKLawFirm_MariosK`), Viber. Una sede (Limassol).

### 4. Elias Neocleous & Co — neo.law

**Struttura.** 1.721 URL in sitemap: 1.031 news, 591 pubblicazioni, 71 persone, 17 pagine expertise (16 aree + indice), più rankings, about, careers, CSR, contact. Aree: admiralty, banking & finance, corporate, privacy, employment, energy, EU/competition, financial services, immigration, IP, litigation, private client, real estate, tax, tech, criminal.
**Persone.** 71 schede. Campione (`people/alexandros-neofytou`): ruolo (Associate), sede, email, telefono diretto, LinkedIn, vCard, formazione, "Cyprus Bar Exams 2025", "Associate Since 2025", lingue (English, Greek).
**Blog.** Pubblicazioni: le 10 più recenti dal 20/07 al 29/09/2026 (≈ 1 a settimana). News: ultima 07/10/2026 (l'indice mostra anche un evento datato 23/10/2026).
**Lingue.** Solo inglese; nessun hreflang.
**Pagine campione (EN).**

| Servizio | URL | Parole | H2 | FAQ | Data | Fonti | JSON-LD | Lingue / nazionalità | Riforma 2026 |
|---|---|---|---|---|---|---|---|---|---|
| Real estate | `/expertise/real-estate` | 349 | 0 | solo FAQPage nel JSON-LD | no | 0 | LegalService, Service, OfferCatalog, FAQPage, BreadcrumbList | — | — |
| Corporate | `/expertise/corporate-and-commercial` | 524 | 0 | idem | no | 0 | idem | — / non-EU | — |
| Immigration | `/expertise/immigration-law` | 459 | 0 | idem | no | 0 | idem | Turkish, Ukrainian / Ukrainian, non-EU | — |
| Banking & finance | `/expertise/banking-and-finance` | 545 | 0 | idem | no | 0 | idem | — | — |
| Tax | `/expertise/tax-law-tax-planning-and-advanced-business-structuring` | 1.004 | 0 | idem | no | 0 | idem | — / foreign investors | **solo come titolo di una pubblicazione collegata** ("…Following the January 1, 2026 Tax Reform", 15/05/2026), non nel testo della pagina |

**Crawler.** robots.txt con il commento "AI Crawlers — explicitly welcome" e `Allow: /` per GPTBot, ChatGPT-User, Claude-Web, ClaudeBot, PerplexityBot, Google-Extended, Applebot-Extended, CCBot, Amazonbot, anthropic-ai. GPTBot: 200, 115.328 byte (browser 115.624: differenza di token dinamici). `llms.txt` presente (232 parole: sedi, numero di professionisti, aree, classifiche).
**Contatti.** Nessun WhatsApp/Telegram. 7 sedi: Limassol, Nicosia, Paphos, Kiev, Bruxelles, Budapest, Praga.

### 5. Chrysostomides — chrysostomides.com

**Accesso bloccato.** Tutte le 6 GET (robots.txt, home ×2, home con GPTBot, sitemap.xml, sitemap_index.xml) hanno ricevuto `403` con `Cf-Mitigated: challenge` e pagina "Just a moment…" di Cloudflare (`data/competitors/chrysostomides.com/`). La sfida non è stata aggirata. robots.txt non leggibile, quindi nessuna altra pagina è stata richiesta.
**Cosa si sa senza il sito.** Una ricerca Serper `site:chrysostomides.com` restituisce home, disclaimer, careers, `/sector/`, `/sitemap/`, `/news/`, pagine tag e `/seniority/director/`, `/seniority/associate/` (`data/competitors/serper/chrysostomides_site.json`). Struttura, lingue, pagine campione, contatti: **non verificati**.
**Crawler.** Da IP di datacenter sia il browser sia GPTBot ricevono la sfida Cloudflare. Cosa ricevano i crawler AI dai loro IP: non verificato. Nella classifica ZeroRank fornita il dominio non compare (meno di 2 citazioni o nessuna), pur essendo lo studio nominato dai motori AI: viene citato attraverso altre fonti (vedi Parte B).

### 6. Andreas Demetriades & Co — demetriadeslaw.com

**Struttura.** 82 URL in sitemap (46 post, 36 pagine). Le versioni `/de/…` e `/ru/…` (che vincono nelle SERP del 06/10) e una pagina in ebraico non sono in sitemap. Aree (pagina `practice-areas`): real estate investments, commercial & corporate, banking & finance, immigration con sottopagine (permanent residency programme, PR by investment, Pink Slip, Yellow Slip, temporary residence, MEU1), civil litigation, criminal litigation, family, employment, wills & probate, arbitration/ADR. **Nessuna pagina servizio tax**: il fisco è coperto da articoli (`how-to-get-non-dom-status-in-cyprus`, tax residency, plusvalenze) e da due calcolatori (imposta d'acquisto immobile, imposta sul reddito).
**Persone.** 10 schede. Campione (`andreas-demetriades`): ruolo (Advocate – Founding Partner), bio (ex Ministro della Giustizia 1980-82), formazione, lingue (greco, inglese), contatti. Iscrizione all'ordine: non indicata esplicitamente.
**Blog.** 46 post. Le 10 date visibili più recenti vanno dal 26/08/2025 al 10/02/2026 (≈ 2 al mese, poi fermo); il `lastmod` più recente nella sitemap post è il 23/07/2026.
**Lingue.** Inglese + traduzioni GTranslate (widget `gtranslate` nel codice) con URL `/de/`, `/ru/`. Nessun hreflang. Indizi di traduzione automatica: la pagina DE banking ha lo stesso contenuto ridotto dell'EN (163 contro 168 parole di contenuto) e frasi sgrammaticate ("…erkläre ich mich … einverstanden und bestätige, dass ich mit den AGB und ich habe gelesen, Datenschutzbestimmungen").
**Pagine campione (EN).**

| Servizio | URL | Parole | H2 | FAQ | Data | Fonti | JSON-LD | Lingue / nazionalità | Riforma 2026 |
|---|---|---|---|---|---|---|---|---|---|
| Real estate | `/real-estate-investments/` | 1.137 | 11 | no | no | 0 | nessuno | — / non-EU | — |
| Corporate | `/commercial-corporate/` | 257 | 0 | no | no | 0 | nessuno | — | — |
| Immigration | `/cyprus-immigration-lawyers/` | 507 | 5 | no | no | 0 | nessuno | — / non-EU | — |
| Banking & finance | `/banking-finance-law/` | 320 | 0 | no | no | 0 | nessuno | — | — |
| Tax | nessuna pagina servizio | — | — | — | — | — | — | — | — |

(La home ha JSON-LD LegalService/Organization; le pagine servizio no.)
**Crawler.** robots.txt senza regole per bot AI. **Home con UA GPTBot: 403** ("Forbidden", Apache, 312 byte) in 2 prove su 2 (14:42 e 14:54 UTC), mentre il browser riceve 200 e GPTBot riceve 200 su `robots.txt`: è un blocco per User-Agent a livello server, non nel robots. ClaudeBot e PerplexityBot non sono stati provati (il brief chiedeva GPTBot). `llms.txt`: 404.
**Contatti.** WhatsApp (`wa.me/35799936421`); Telegram no. Una sede (Paphos).

### 7. Michael Kyprianou — kyprianou.com

**Struttura.** Indice `sitemaps.xml` con 5 sotto-sitemap, 1.578 URL: ≈ 1.006+ post (due sitemap post), 239 tag, 47 URL `de`, 42 `zh-hans`, 15 `el`, 7 `he`, 7 `ru`. Le pagine expertise sono per paese (`/expertises/<area>-cyprus/`, `-germany/`, `-greece/`…) e non sono in sitemap; la pagina `expertise-listing` si popola via JavaScript. Per Cipro trovate (Serper `site:`): data protection, gaming, sanctions, media, IP, corporate, competition, AML, shipping, immovable property, banking & finance, international tax planning. **Immigration Cipro: non trovata** (2 URL ipotizzati → 404; non nelle prime 10 della ricerca `site:`).
**Persone.** La pagina People elenca circa 70 nominativi (70 occorrenze di "contact via email") con ruolo e telefono; non linka schede individuali. Pagine persona: non verificate.
**Blog.** Oltre 1.000 post. Le 10 date più recenti sull'indice news (escluso un evento futuro, 31/12/2026) vanno dal 04/08 al 06/10/2026 (≈ 1 a settimana).
**Lingue.** en, el, ru, de, he, zh-hans con hreflang (WPML). Solo un sottoinsieme è tradotto (vedi conteggi sopra). La pagina DE banking ha lunghezza paragonabile all'EN (1.527 parole di contenuto contro 1.414; il valore DE è sovrastimato, vedi sopra), è in tedesco corretto con un refuso umano ("spezialiserten"): indizio di traduzione non automatica.
**Pagine campione (EN).**

| Servizio | URL | Parole | H2 | FAQ | Data | Fonti | JSON-LD | Lingue / nazionalità | Riforma 2026 |
|---|---|---|---|---|---|---|---|---|---|
| Real estate | `/expertises/immovable-property-law-cyprus/` | 1.283 | 6 | no | no | 0 | solo WebSite | — | — |
| Corporate | `/expertises/corporate-and-commercial-cyprus/` | 2.071 | 6 | no | no | 0 | solo WebSite | Chinese, Dutch, English, French, Polish / Chinese, Indian | — |
| Immigration | non trovata | — | — | — | — | — | — | — | — |
| Banking & finance | `/expertises/banking-and-finance-cyprus/` | 1.414 | 6 | no | no | 0 | solo WebSite | Chinese, Greek / Chinese, EU, Israeli | — |
| Tax | `/expertises/international-tax-planning-cyprus/` | 879 | 6 | no | no | 0 | solo WebSite | — | **no** |

**Crawler.** robots.txt: Disallow solo `/wp-admin/` e upload WPForms; nessuna regola AI. GPTBot: 200, 460.407 byte, identica. `llms.txt`: 404.
**Contatti.** Nessun WhatsApp/Telegram. 11 sedi in pagina contatti: Limassol, Nicosia, Paphos, Atene, Londra, Kyiv, Dubai, Varsavia, Malta, Tel Aviv, Francoforte.

### 8. Connor Legal — connorlegalllc.com

**Struttura.** 138 URL (96 post, ≈ 29 pagine, categorie e tag). 12 aree di pratica (banking & finance, corporate/M&A, dispute resolution, employment, EU & competition, immigration, IP, maritime, personal injury, real estate & construction, tax) più pagine costruite sulle ricerche ("property-lawyer-in-cyprus", "best-corporate-lawyer-in-nicosia", "best-commercial-lawyer-in-cyprus-how-to-choose-2026"), `how-we-charge`.
**Persone.** Nessuna pagina persona. About presenta solo il fondatore, Nicolas Connor Georgiades (LLM BPTC, City University London, ammesso al Bar di Inghilterra e Galles; il JSON-LD `Person` lo indica "registered with the Cyprus Bar").
**Blog.** 96 post. Pubblicazioni: 10 date più recenti dal 17/07 al 10/09/2026 (≈ 1,25 a settimana).
**Lingue.** 47 hreflang generati da GTranslate (dall'afrikaans al vietnamita), con slug tradotti (`/de/Praxisbereiche-Zypern/Steueranwälte-Zypern/`). Indizi di traduzione automatica: numero di lingue, plugin GTranslate, testo DE/RU che ricalca l'inglese frase per frase. Ma le pagine DE/RU sono quelle che vincono 7 SERP su 15.
**Pagine campione (EN).**

| Servizio | URL | Parole | H2 | FAQ | Data | Fonti | JSON-LD | Lingue / nazionalità | Riforma 2026 |
|---|---|---|---|---|---|---|---|---|---|
| Real estate | `/practice-areas-cyprus/real-estate-construction/` | 548 | 4 | no (solo link "FAQ" nel menu) | no (modified 23/09/2026) | 0 | LegalService, Person, Organization, Breadcrumb… | — / foreign buyers | — |
| Corporate | `/practice-areas-cyprus/commercial-corporate-ma/` | 576 | 4 | no | no | 0 | idem | — | — |
| Immigration | `/practice-areas-cyprus/immigration/` | 389 | 4 | no | no | 0 | idem | — | — |
| Banking & finance | `/practice-areas-cyprus/banking-finance/` | 544 | 3 | no | no | 1 (portal.dls.moi.gov.cy) | idem | — | — |
| Tax | `/practice-areas-cyprus/tax-cyprus-lawyers/` | 453 | 4 | no | no | 1 (mof.gov.cy) | idem | — | **solo come titolo di una pubblicazione collegata** ("Cyprus Tax Reform 2026 – What Businesses, Directors & Investors Must Know") |

(Home: JSON-LD con 26 tipi, tra cui AggregateRating, Person, OfferCatalog, NewsArticle.)
**Crawler.** robots.txt `User-agent: *` / `Allow: /`. GPTBot: 200, 593.905 byte (browser 594.208). `llms.txt` presente, generato da Yoast SEO (165 parole, elenco pagine e post).
**Contatti.** Nessun link WhatsApp/Telegram trovato nelle pagine scaricate. Una sede (Nicosia).

## Chi ha bloccato o limitato l'accesso

| Dominio | Cosa è successo |
|---|---|
| chrysostomides.com | 403 + challenge Cloudflare su tutte le 6 GET, robots.txt incluso. Sito non analizzabile. |
| demetriadeslaw.com | 403 alla home solo con UA GPTBot (2/2); pagine servite normalmente al browser. |
| lawzana.com (fonte, Parte B) | robots.txt 200, poi 403 + challenge Cloudflare su 4 pagine su 4. |
| mip.gov.cy (fonte, Parte B) | errore TLS: certificato scaduto (anche su robots.txt). Nessuna pagina letta. |
| legalhelpcy.com (fonte) | `/user/register` vietato da robots.txt (`Disallow: /user/register`): non scaricato. |
| Tutti gli altri | nessun blocco; robots.txt rispettato. |
