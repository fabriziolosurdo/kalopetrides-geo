# Audit tecnico onsite — kalopetrideslaw.com

Data rilevazione: 2026-10-05, 22:31–22:38 UTC (date dagli header `date:` delle risposte).
Metodo: solo richieste HTTP GET con `curl` da una sessione Claude Code in cloud. Nessun form inviato, nessuna modifica.
Ogni affermazione rimanda a un file grezzo in `data/site/` (header + corpo della risposta). Indice: `data/site/_index.csv`, `data/site/_page_attempts.csv`, `data/site/_page_attempts_2.csv`, `data/site/_ua_matrix_rounds.csv`, `data/site/_ua_tally.csv`. Analisi strutturata delle pagine: `data/site/_analysis.json`. Script: `scripts/`.

---

## 0. Sintesi in 10 righe

1. **Il sito è dietro la protezione anti-bot di SiteGround ("Robot Challenge").** Dal cloud, 128 GET su 160 (80%) hanno ricevuto al posto della pagina una risposta `HTTP 202` di 168–191 byte con header `sg-captcha: challenge` e `x-robots-tag: noindex`, che rimanda a `/.well-known/sgcaptcha/` (una prova JavaScript). Il blocco **non dipende dallo User-Agent**: colpisce allo stesso modo browser, Googlebot e bot AI, e varia con l'IP di uscita (il parametro `ipr:` nella risposta riporta l'IP visto dal server).
2. Conseguenza probabile ma **non verificata con gli IP reali dei crawler**: i crawler AI (GPTBot, ClaudeBot, PerplexityBot, OAI-SearchBot, CCBot), che girano da IP di datacenter come i nostri, ricevono spesso la sfida invece del contenuto. Per Googlebot/Bingbot SiteGround dichiara di norma di riconoscere i bot verificati: da qui non è dimostrabile. È il primo punto da chiarire (vedi §1.3).
3. `robots.txt` è permissivo (`User-agent: *` / `Allow: /`), quindi il problema non è nel robots ma nel livello hosting.
4. 7 pagine HTML reali + home; nessuna pagina servizio dedicata: i 9 servizi sono sezioni di `services-overview.html` (107–162 parole ciascuna).
5. **La versione greca non esiste come pagine**: è una traduzione caricata da `assets/js/i18n.js` e scelta via `localStorage`, sullo stesso URL. Nessun hreflang, nessun URL `/el/`. Per i motori esiste solo l'inglese.
6. Nessuna pagina in RU, UK, DE, NL, PL.
7. Bio degli avvocati presenti solo nell'attributo `data-bio` e mostrate in un modale JS: non sono testo visibile e non hanno URL propri.
8. Imprint con i riferimenti normativi austriaci (§5 E-Commerce Act, §14 Corporate Code, §63 Trade Regulation Act, §25 Media Act = ECG, UGB, GewO, MedienG).
9. URL duplicati: ogni pagina risponde sia con `.html` sia senza estensione, e anche su `www` (200 senza redirect). Il canonical punta alla versione senza estensione; i link interni usano `.html`; la sitemap usa la versione senza estensione. `/privacy-policy` (senza estensione, presente in sitemap) ha risposto **403** in 2 tentativi su 2.
10. Form di contatto → servizio terzo **Web3Forms** (`https://api.web3forms.com/submit`, POST via `fetch`), con fallback `mailto:`.

---

## 1. A1 — Inventario e accessibilità

### 1.1 Nota metodologica sulla sfida anti-bot

La prima GET (home, UA browser) ha ricevuto:

```
HTTP/2 202
sg-captcha: challenge
x-robots-tag: noindex
<meta http-equiv="refresh" content="0;/.well-known/sgcaptcha/?r=%2F&y=ipr:160.79.106.139:...">
```

(`data/site/https_kalopetrideslaw_com__browser.txt`). La pagina `/.well-known/sgcaptcha/` contiene una prova di calcolo JavaScript ("Robot Challenge Screen") che un browser risolve in automatico. **Non è stata aggirata né risolta**: il tentativo di eseguirla è stato bloccato dai permessi della sessione e non è stato ripetuto. Le pagine analizzate sono state ottenute ripetendo GET normali (max 8 tentativi per URL): l'egress del cloud usa più IP (osservati `160.79.106.131–140` e `34.57.188.202`) e alcune richieste sono state servite normalmente. Tutti i tentativi, riusciti e no, sono salvati.

Risultato complessivo: **160 GET verso kalopetrideslaw.com, 128 con challenge (80%), 32 servite** (200/301/403/404).

### 1.2 Test User-Agent (home e privacy-policy.html, https non-www)

Ogni UA è stato provato 5 volte sulla home e 4 su `/privacy-policy.html` in 4 tornate (il browser anche nei tentativi di recupero pagine). Fonte: `data/site/_ua_tally.csv` (una riga per file grezzo).

| User-Agent | Richieste | 202 challenge | 200 contenuto servito | Note |
|---|---|---|---|---|
| Browser (Chrome 140) | 18 | 16 | 2 | |
| Googlebot | 9 | 8 | 1 | 200 su privacy-policy.html |
| Bingbot | 9 | 9 | 0 | |
| GPTBot | 9 | 8 | 1 | 200 = stessa home di 53.801 byte |
| ClaudeBot | 9 | 8 | 1 | idem |
| PerplexityBot | 9 | 8 | 1 | idem |
| OAI-SearchBot | 9 | 7 | 2 | idem |
| Google-Extended | 9 | 9 | 0 | (token robots, non un crawler reale: testato come UA per completezza) |
| CCBot | 9 | 8 | 1 | idem |

Lettura:
- **Nessun 403 a un crawler AI** e nessun trattamento diverso per UA: quando la pagina viene servita, è identica (53.801 byte) per tutti gli UA. Non c'è quindi un blocco per User-Agent né nel robots né nel server.
- **C'è invece una sfida anti-bot basata sull'IP/reputazione** che restituisce 202 + pagina vuota + `noindex`. Un crawler che non esegue JavaScript (tutti i crawler AI noti) non può superarla.
- **Non verificato**: cosa ricevono i crawler veri dai loro IP. Il test qui misura il comportamento verso IP di datacenter (Anthropic e Google Cloud), cioè lo stesso tipo di rete da cui operano GPTBot, ClaudeBot, PerplexityBot, CCBot e i fetcher "live" degli assistenti AI. Per chiudere il punto servono: log di accesso del server (SiteGround Site Tools → Statistics/Logs) filtrati per questi UA, il pannello SiteGround Security (anti-bot / "AI Anti-Bot"), e i "Crawl stats" di Google Search Console.

### 1.3 robots.txt

`data/site/https_kalopetrideslaw_com_robots_txt__browser__try6.txt` (200, 73 byte, last-modified 2026-06-04):

```
User-agent: *
Allow: /

Sitemap: https://kalopetrideslaw.com/sitemap.xml
```

Nessuna regola specifica per bot AI, nessun Disallow. Anche `robots.txt` stesso è stato servito con la challenge in 5 tentativi su 6 (file `..._robots_txt__browser*.txt`).

### 1.4 llms.txt

`/llms.txt` → **404** (pagina "Page not found" del sito, `noindex`) — `data/site/https_kalopetrideslaw_com_llms_txt__browser__try5.txt`. Atteso.

### 1.5 Redirect http/https e www/non-www

| Richiesta | Risultato | File |
|---|---|---|
| `http://kalopetrideslaw.com/` | 301 → `https://kalopetrideslaw.com/` | `http_kalopetrideslaw_com__browser__x2.txt` |
| `http://www.kalopetrideslaw.com/` | 301 → `https://www.kalopetrideslaw.com/` (resta su www) | `http_www_kalopetrideslaw_com__browser__x2.txt` |
| `https://www.kalopetrideslaw.com/` | **200, nessun redirect**, stessa home | `https_www_kalopetrideslaw_com__browser__follow.txt` |
| `https://www.kalopetrideslaw.com/about-us.html` | **200, nessun redirect** | `https_www_kalopetrideslaw_com_about_us_html__browser__x1.txt` |

→ http→https: ok (301). **www→non-www: assente.** Il sito risponde in doppio su due host; il canonical (non-www) mitiga ma non sostituisce il redirect.

Nota rispetto al contesto ricevuto: nell'HTML scaricato oggi **i link interni sono relativi** (`about-us.html`, `services-overview.html#tax`, `index.html#contact`), non assoluti su www. Il problema www esiste comunque perché l'host www serve 200.

### 1.6 Versione greca

| Verifica | Esito | File |
|---|---|---|
| `<link hreflang>` in tutte le pagine | nessuno | `_analysis.json` |
| `/el/` | 404 | `https_kalopetrideslaw_com_el__browser__try1.txt` |
| `/index-el.html` | 404 | `https_kalopetrideslaw_com_index_el_html__browser__try1.txt` |
| Selettore lingua | `<button class="lang-btn" data-lang="el">` con bandiera `flag-gr.svg` | home |
| Meccanismo | `assets/js/i18n.js`: "bilingual engine (English / Greek). English lives in the HTML; this file provides the Greek (el) overrides". La scelta è salvata in `localStorage` (`kl_lang`) e cambia l'attributo `lang` lato client | `https_kalopetrideslaw_com_assets_js_i18n_js_v_20260912_1455__browser__a1.txt` |

→ **La versione greca esiste solo nel browser dell'utente.** Stesso URL, nessun HTML greco servito: per Google e per i motori AI il sito è solo in inglese. Il JSON-LD dichiara `knowsLanguage: ["en","el"]`.

### 1.7 Inventario pagine

| URL | Status | Byte | Title | Canonical | Meta robots | File |
|---|---|---|---|---|---|---|
| `/` (= `/index.html`) | 200 | 53.801 | Kalopetrides Law LLC — Your Trusted Legal Partner in Cyprus | `https://kalopetrideslaw.com/` | — | `..._com__browser__try5.txt` |
| `/about-us.html` (= `/about-us`) | 200 | 13.008 | About Us — Kalopetrides Law LLC | `/about-us` | — | `..._about_us_html__browser__try5.txt` |
| `/services-overview.html` (= `/services-overview`) | 200 | 30.324 | Our Services — Kalopetrides Law LLC | `/services-overview` | — | `..._services_overview_html__browser__try5.txt` |
| `/trustgate.html` (= `/trustgate`) | 200 | 16.316 | TrustGate Corporate Services — Kalopetrides Law LLC | `/trustgate` | — | `..._trustgate_html__browser__try5.txt` |
| `/csr.html` (= `/csr`) | 200 | 10.114 | Corporate Social Responsibility — Kalopetrides Law LLC | `/csr` | — | `..._csr_html__browser__try2.txt` |
| `/imprint.html` (= `/imprint`) | 200 | 9.542 | Imprint — Kalopetrides Law LLC | `/imprint` | **noindex** | `..._imprint_html__browser__try1.txt` |
| `/privacy-policy.html` | 200 | 16.500 | Privacy Policy — Kalopetrides Law LLC | `/privacy-policy` | **noindex** | `..._privacy_policy_html__browser__try4.txt` |
| `/privacy-policy` (senza estensione) | **403** (2/2) | 75.193 | 403 - Forbidden | — | noindex | `..._privacy_policy__browser__try5.txt`, `..._x1.txt` |
| `/sitemap.xml` | 200 | 1.289 | — | — | — | `..._sitemap_xml__browser.txt` |
| `/robots.txt` | 200 | 73 | — | — | — | `..._robots_txt__browser__try6.txt` |
| `/llms.txt`, `/el/`, `/index-el.html` | 404 | 1.747 | Page not found | — | noindex | vedi §1.4, §1.6 |

Team, testimonianze e contatti sono sezioni della home (`#team`, `#testimonials`, `#contact`); tutti i link del menu e del footer puntano a pagine che rispondono 200.

Header di sicurezza (home): HSTS, CSP restrittiva, `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy` presenti. La CSP autorizza `connect-src`/`form-action` verso `api.web3forms.com`, quindi il form non è bloccato dalla CSP.

---

## 2. A2 — Analisi per pagina (pagine 200)

Fonte: `data/site/_analysis.json` (generato da `scripts/analyze_pages.py`). JSON-LD validato con `json.loads` (parser locale): valido.

### 2.1 Meta, canonical, social, dati strutturati

| Pagina | Title (car.) | Meta description (car.) | hreflang | OG / Twitter | JSON-LD | Parole visibili |
|---|---|---|---|---|---|---|
| Home | 59 | 155 | no | 9 / 2 | `LegalService` (valido) | 1.097 |
| About us | 31 | 127 | no | 9 / 2 | no | 455 |
| Services overview | 35 | 186 (lunga) | no | 9 / 2 | no | 1.481 |
| TrustGate | 51 | 160 | no | 9 / 2 | no | 423 |
| CSR | 54 | 172 (lunga) | no | 9 / 2 | no | 303 |
| Imprint | 30 | 86 | no | 9 / 2 | no | 197 |
| Privacy policy | 37 | 154 | no | 9 / 2 | no | 891 |

Tutte le pagine: `<html lang="en">`.

**JSON-LD home** (`LegalService`, `@id https://kalopetrideslaw.com/#organization`): name, alternateName "Savvas Kalopetrides LLC", description, url, image, logo, telephone, email, priceRange, address (Gladstonos 1, Office 205, 6023 Larnaca, CY), geo, hasMap, areaServed (Cyprus, European Union), `knowsLanguage ["en","el"]`, founder (Person: Savvas Kalopetrides), knowsAbout (9 aree), openingHoursSpecification. **Assenti**: `sameAs` (nessun collegamento a profili esterni / Google Business Profile), persone del team diverse dal founder, `Service`/`hasOfferCatalog`, recensioni. Nessun JSON-LD sulle altre pagine (nessun `Service`, `Person`, `BreadcrumbList`).

### 2.2 Struttura titoli

- **Home**: H1 "Your Trusted Legal Partner in Cyprus." → H2 servizi → 9 H3 (Real Estate & Investment, Banking & Finance, Corporate & Commercial, Immigration Services, Tax Advising, Wills & Probate, Intellectual Property, Professional Litigation, Civil Marriages & Partnerships) → H2 valori → H2 testimonianze → H2 team con 4 H3 (Savvas Kalopetrides, Angelos Ioannou, Theodosis Kokozides, Marianna Giannarou) → H2 contatti → H3 "Send us a message" → **un H3 vuoto** (è l'H3 del modale bio, riempito via JS).
- **Services overview**: H1 "Full-service legal expertise in Cyprus" → 9 H3 (indice) → 9 H2 (le sezioni). L'ordine H3 prima degli H2 è un indice a schede; nessun contenuto oltre le sezioni.
- **About us**: H1 + 4 H2 + 3 H3. **TrustGate**: H1 + 4 H2 + 4 H3. **CSR**: H1 + 1 H2. **Imprint**: H1 + 2 H2 + 2 H3. **Privacy**: H1 + 12 H2 + 7 H3.
- Un solo H1 per pagina ovunque.

### 2.3 Contenuto dei 5 servizi obiettivo (sezioni di services-overview.html)

| Servizio | Ancora | Parole | Cosa dice / cosa manca rispetto alle query del cliente |
|---|---|---|---|
| Real estate | `#real-estate` | 157 | testo generico su transazioni, title search, zoning; non nomina acquirenti stranieri come procedura (permesso del Consiglio dei Ministri, due diligence, trasferimento titolo) |
| Corporate | `#corporate` | 162 | company formation, M&A, governance; rimanda a TrustGate per i servizi nominee |
| Immigration | `#immigration` | 145 | residency permit, citizenship, work visa, investor visa, "long-term residency"; nessun riferimento esplicito al permesso di residenza permanente per investimento |
| Banking & finance | `#banking` | 130 | loan agreements, security, insolvency, CySEC e Central Bank |
| Tax | `#tax` | 119 | pianificazione, trattati, VAT, transfer pricing; **nessuna aliquota citata** su nessuna pagina (cercati "12.5", "15%", "tax rate" anche in i18n.js): non c'è un dato obsoleto da correggere, ma nemmeno un riferimento alla riforma 2026 (aliquota societaria 15% dal 1/1/2026) |

Ogni servizio è quindi un blocco di ~120–160 parole dentro una pagina condivisa, raggiungibile solo con ancora `#`. Nessun URL proprio, nessun title/description propri.

### 2.4 Immagini senza alt

| Pagina | Immagini | alt vuoto/assente |
|---|---|---|
| Home | 24 | 9: emblema (3, decorativo), **5 loghi clienti** (`client-dhl.png`, `client-rise.png`, `client-gig.png`, `client-jimmy.png`, `client-cotton.png`), 1 `src` vuoto (immagine del modale bio) |
| About us | 9 | 3 (emblema) |
| Services overview | 7 | 2 (emblema) |
| TrustGate | 9 | 3 (emblema ×2, `flag-gr.svg`) |
| CSR, Imprint | 7 | 2 (emblema) |
| Privacy | 6 | 1 (emblema) |

I loghi clienti senza alt sono la sola perdita reale (sono un segnale di fiducia); l'emblema è decorativo.

### 2.5 Link interni in uscita

Tutte le pagine condividono menu e footer: `about-us.html`, `services-overview.html`, `trustgate.html`, `csr.html`, `imprint.html`, `privacy-policy.html`, `index.html#welcome|#team|#testimonials|#contact`, `mailto:info@kalopetrideslaw.com`, `tel:+35724668667`. La home linka anche le 9 ancore `services-overview.html#…`. **Nessun link esterno** su nessuna pagina (nessun profilo social, Google Maps solo nel JSON-LD, nessun Cyprus Bar Association).

### 2.6 Date visibili

Solo l'anno nel footer (2026); la privacy policy cita anche 2025. Nessuna data di aggiornamento dei contenuti. Header `last-modified`: home 2026-09-12; tutte le altre pagine 2026-06-13.

### 2.7 Testo che dipende da JavaScript

| Elemento | Nell'HTML grezzo | Con JS | Fonte |
|---|---|---|---|
| Contatori home | `<span data-count="9">0</span> Practice Areas`, `<span data-count="500">0</span>+ Clients Advised` | conta fino a 9 e 500 (`main.js`, "Count-up stats") | home, `..._assets_js_main_js__browser__a1.txt` |
| Bio del team ("Read bio") | testo completo **solo nell'attributo `data-bio`** dei 4 `div.member`; il modale (`[data-modal]`) è vuoto | `main.js` copia `data-bio` nel modale al click | home |
| Testimonianze | **9 testimonianze presenti come testo nell'HTML** (carosello `testi__slide`) | il JS gestisce solo lo scorrimento | home |
| Versione greca | assente | `i18n.js` sostituisce i testi `data-i18n` | §1.6 |
| Tab dei servizi | contenuto presente nell'HTML (sezioni `#real-estate` ecc.) | — | services-overview |

Per un crawler senza JS: i contatori valgono "0 Practice Areas" e "0+ Clients Advised"; le bio non sono testo di pagina (attributo HTML, in genere non indicizzato come contenuto); le testimonianze sono leggibili.

---

## 3. A3 — Form di contatto

Fonte: home (`<form data-contact-form>`) e `main.js` righe ~220–290.

- `action="https://api.web3forms.com/submit"`, `method="post"`, `novalidate`.
- Campi: `access_key` (hidden, chiave pubblica Web3Forms), `subject` (hidden: "New enquiry — kalopetrideslaw.com"), `from_name` (hidden), `botcheck` (checkbox honeypot), `name`, `email`, `company`, `message`, `website` (secondo honeypot).
- Invio: `main.js` intercetta il submit e fa `fetch(action, {method:"POST", body: FormData, headers:{Accept:"application/json"}})`; considera riuscito `{success:true}` (commento nel codice: "Legacy contact.php returned {ok:true}").
- In caso di errore: messaggio con link `mailto:info@kalopetrideslaw.com` e, in un ramo, apertura di `mailto:` precompilato.
- **Destinazione delle submission**: servizio terzo Web3Forms, che le inoltra per email all'indirizzo associato alla access key (non visibile dal sito; presumibilmente info@kalopetrideslaw.com — **non verificato**). Nessun invio di prova effettuato.
- Da valutare con il cliente (non tecnico): i dati dei potenziali clienti transitano da un fornitore terzo; la privacy policy andrebbe verificata su questo punto.

---

## 4. A4 — Sitemap

`data/site/https_kalopetrideslaw_com_sitemap_xml__browser.txt` (200, servita senza challenge, last-modified 2026-06-04).

| URL in sitemap | lastmod | Stato osservato |
|---|---|---|
| `https://kalopetrideslaw.com/` | 2026-06-04 | 200 (ma file modificato 2026-09-12) |
| `/about-us` | 2026-06-04 | 200 |
| `/services-overview` | 2026-06-04 | 200 |
| `/trustgate` | 2026-06-04 | 200 |
| `/csr` | 2026-06-04 | 200 |
| `/imprint` | 2026-06-04 | 200, **ma `noindex`** |
| `/privacy-policy` | 2026-06-04 | **403** (2/2), e la versione `.html` è `noindex` |

- Pagine nel sito e assenti dalla sitemap: nessuna (le versioni `.html` sono duplicati delle stesse pagine).
- URL in sitemap che non dovrebbero esserci: `/imprint` e `/privacy-policy` (noindex; la seconda risponde 403).
- `lastmod` identico per tutti e non aggiornato dopo la modifica della home del 12/09.
- Incoerenza di formato: sitemap e canonical senza estensione, link interni con `.html`. Entrambe le forme rispondono 200 (tranne `/privacy-policy`).

---

## 5. Cosa non è stato possibile verificare

| Punto | Perché |
|---|---|
| Cosa ricevono i crawler reali (Googlebot, GPTBot, ClaudeBot, ecc.) dai loro IP | Il test usa IP del cloud; la sfida SiteGround è basata su IP/reputazione. Servono log server o pannello SiteGround |
| Contenuto della pagina di challenge SiteGround oltre l'header | Risolverla/aggirarla è stato bloccato dai permessi della sessione; non ritentato |
| Copie storiche (Wayback Machine, Common Crawl) | `web.archive.org` e `index.commoncrawl.org`: connessione chiusa; `archive.org`: 429 Too Many Requests |
| Destinatario finale delle email Web3Forms | Configurato nell'account Web3Forms, non visibile dal sito |
| Indicizzazione attuale in Google (`site:`) | Serper non attivo (403), vedi `reports/SERP_CONCORRENZA_2026-10-05.md` |
| Google Business Profile | Fuori dal perimetro della sessione (lo integra Fab) |

## 6. Priorità (per Fab)

1. **Sfida anti-bot SiteGround**: verificare in Site Tools → Security (Bot protection / AI Anti-Bot) e nei log se GPTBot, ClaudeBot, PerplexityBot, OAI-SearchBot, Googlebot, Bingbot ricevono 202. Se sì, eccezioni per i bot verificati. È il prerequisito di tutto il resto.
2. Pagine dedicate per i 5 servizi obiettivo (oggi ~120–160 parole ciascuno dentro una pagina condivisa).
3. Pagine reali per lingua (RU, UK, DE, NL, PL; EL come HTML e non via JS) con hreflang.
4. Pagine avvocato con bio come testo e `Person` in JSON-LD; `sameAs` verso Google Business Profile.
5. Imprint conforme al diritto cipriota.
6. Redirect www → non-www; un solo formato URL (con o senza `.html`) allineato tra link, canonical e sitemap; togliere dalla sitemap le pagine noindex; sistemare il 403 di `/privacy-policy`.
7. Contatori: valori reali nell'HTML. Alt sui loghi clienti.
8. Contenuto fiscale che citi la riforma 2026 (aliquota societaria 15%).
