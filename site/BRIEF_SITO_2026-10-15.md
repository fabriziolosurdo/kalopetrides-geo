# Brief — sito nuovo kalopetrideslaw.com (2026-10-15)

Questo file è la fonte di verità per chiunque scriva contenuti o codice del sito nuovo. Leggerlo per intero prima di scrivere una riga.

## 1. Cosa stiamo facendo e perché

Kalopetrides Law LLC (Larnaca, Cipro) è il primo cliente GEO di Fab (contratto: 3 mesi di solo GEO a €490/mese, accettato il 15/10/2026). Il sito attuale (HTML statico, fatto da un webmaster esterno) non può portare risultati: un'unica pagina per nove servizi, nessuna pagina per lingua, bio in popup, imprint austriaco, contatori a zero per i crawler, hosting SiteGround con sfida anti-bot. Audit completo in `reports/AUDIT_TECNICO_2026-10-05.md`; concorrenza in `reports/CONCORRENTI_SINTESI_2026-10-08.md` (Philippou è il modello).

Rifacciamo il sito da zero come **HTML statico generato** (`site/build.py` → `dist/`). Il webmaster riceverà la cartella `dist/` da caricare sullo stesso hosting, con la cartella `/assets/img/` e `/assets/fonts/` esistenti lasciate al loro posto (le immagini e i font del sito attuale restano identici e vengono referenziati con gli stessi percorsi). DNS invariato.

## 2. Obiettivi del cliente (parole sue)

Essere trovato **solo** da chi cerca, a Cipro: 1) real estate lawyer, 2) corporate lawyer, 3) immigration services, 4) banking and financial services, 5) tax advising. Mercati: Russia, Ucraina, Germania, Austria, Olanda, Polonia (Cina esclusa, Israele e Libano già clienti). Lingue del sito: **EN (base), DE, RU, EL**. Olanda e Polonia leggono l'inglese. Ucraina legge RU o EN.

## 3. Fatti verificati sul cliente (usarli così, non inventare altro)

- Ragione sociale sul sito: **Kalopetrides Law LLC**; alternateName "Savvas Kalopetrides LLC". Usare sempre "Kalopetrides Law LLC" nel testo (mai "Kalopetrides LLC" da solo).
- Sede: Panayioteio Megaro, Gladstonos 1, 2nd floor, Office 205, 6023 Larnaca, Cyprus. Tel. ufficio +357 24 668667. Email info@kalopetrideslaw.com. Orari lun–ven 08:00–13:00 e 14:00–17:00. Coordinate 34.9174, 33.6337.
- Google Business Profile: 36 recensioni, media 5,0 (ottobre 2026). Non si cita il numero nel testo (cambia); si può scrivere "5.0-star Google rating" solo nella pagina contatti con la data "as of October 2026".
- Team (dal sito attuale, `source_site/index.html`, attributo `data-bio`):
  - **Savvas Kalopetrides** — Founder & Managing Director, avvocato, LLB (Hons) University of Reading, membro del Cyprus Bar Association. È **l'unico avvocato interno**.
  - **Angelos Ioannou** — external associate, avvocato (civil & criminal litigation), LLB University of Reading, membro del Cyprus Bar Association.
  - **Theodosis Kokozides** — operations/corporate administration (Hospitality & HR, Canterbury; esperienza in Cipro e Germania). **Non è avvocato.**
  - **Marianna Giannarou** — corporate administration & compliance (UCLan Cyprus). **Non è avvocato.**
  - Anno di iscrizione all'ordine: **non noto** → non scriverlo. Non scrivere "founded in" né l'anno di fondazione dello studio (richiesta di Fab).
  - Lingue parlate in studio: inglese, greco, tedesco, russo (dichiarato dal cliente). Non attribuire una lingua a una persona specifica.
- Società affiliata: **TrustGate Corporate Services Ltd** (corporate administration, nominee, registered office, company secretarial). Testi in `source_site/trustgate.html`.
- 9 testimonianze reali (in `source_site/index.html`, sezione testimonials) e 5 loghi clienti (DHL, Rise Hotel, GIG, Jimmy's Suites, Cotton). Si riusano tali e quali.
- Form di contatto: Web3Forms, access key `ffeecfb8-97a1-42a8-9a01-f1b220b3e8d7`, con fallback mailto. Si riusa identico.
- Cellulare di Savvas per WhatsApp/Telegram: **da confermare con Fab prima della pubblicazione** → nel codice il numero sta in `site/config.yaml` (`whatsapp_number`), se vuoto i pulsanti non vengono renderizzati.
- Savvas è socio della Israel-Cyprus Chamber of Commerce (dichiarato). Si può citare nella pagina about.

## 4. Regole sui contenuti (vincolanti)

1. **Nessun fatto giuridico o fiscale senza fonte primaria verificata oggi con WebSearch/WebFetch** (gov.cy, mof.gov.cy, tax.gov.cy, cylaw.org, companies.gov.cy, moi.gov.cy, cba.org.cy, eur-lex). Ogni pagina servizio ha una sezione finale "Sources" con i link usati. Se un dato non si riesce a verificare: non si scrive, oppure si scrive in modo generico ("subject to the thresholds in force"). **Mai cifre, aliquote, articoli di legge o scadenze a memoria.**
2. Riforma fiscale 2026: l'aliquota societaria è 15% dal 1/1/2026 (verificare e citare la fonte). Per il resto della riforma (fasce IRPEF, regola dei 60 giorni, non-dom, ecc.) scrivere solo ciò che risulta in vigore o approvato alla data della ricerca, con data.
3. Niente promesse ("guaranteed", "fastest", "best law firm"), niente superlativi non verificabili, niente "leading law firm". Tono: avvocato che spiega a un cliente straniero cosa succede davvero, passo per passo.
4. Struttura di ogni pagina servizio (EN, 1.500–2.500 parole):
   - BLUF: 2–3 frasi che rispondono subito alla domanda "cosa fa questo studio per me e come funziona a Cipro".
   - H2 "How it works in Cyprus" con i passaggi reali della procedura.
   - H2 specifici per il mercato estero (es. real estate: acquirenti extra-UE e permesso del Consiglio dei Ministri; immigration: permanent residence per investimento, digital nomad, ecc. — solo se verificati).
   - H2 "What we do for you" (servizi concreti dello studio, ripresi/estesi dal testo attuale in `source_site/services-overview.html`).
   - H2 "Fees and timeline": solo se ci sono dati verificabili (tasse e bolli ufficiali); nessun onorario dello studio.
   - H2 "Frequently asked questions": 6–10 domande vere, risposte di 40–120 parole, nel front matter `faq:` (diventano FAQPage).
   - H2 "Sources": link alle fonti primarie.
   - CTA finale verso contatti.
5. Pagine persona: solo ciò che c'è nelle bio attuali, riscritto come testo di pagina. Nessuna qualifica aggiunta.
6. Imprint: diritto cipriota (Cyprus Bar Association; legge sul commercio elettronico cipriota — verificare numero e titolo; GDPR + Law 125(I)/2018 se verificata). Eliminare ogni riferimento austriaco.
7. Lingue: DE/RU/EL sono **adattamenti** della versione EN finale (stessa struttura, stessi fatti, stesse fonti), scritti per il lettore di quel mercato (es. in tedesco si spiega cosa cambia rispetto al Grundbuch; in russo si tratta con cura il tema sanzioni: la pagina RU la rivedrà Savvas parola per parola). Slug localizzati. Nessuna traduzione automatica parola per parola.
8. Data "Updated" visibile su ogni pagina = data del front matter.

## 5. Formato dei contenuti

`site/content/<lang>/<file>.md` con front matter YAML:

```yaml
---
key: service-real-estate        # stesso valore in tutte le lingue della stessa pagina (hreflang)
type: service                    # home | page | service | person | legal
slug: services/real-estate-lawyer-cyprus   # path pubblico senza lingua; EN alla radice, le altre sotto /de/ /ru/ /el/
title: Real Estate Lawyer in Cyprus — Kalopetrides Law LLC   # <title>, max 60 car.
description: ...                 # meta description, 120–155 car.
h1: Real Estate Lawyer in Cyprus
summary: ...                     # 2–3 frasi BLUF, usate anche nelle card e nel JSON-LD
updated: 2026-10-15
nav_label: Real Estate           # etichetta corta per menu/card
faq:
  - q: ...
    a: ...
sources:
  - title: ...
    url: https://...
person:                          # solo type: person
  name: ...
  jobTitle: ...
  image: /assets/img/team-savvas.jpg
  alumniOf: ...
  memberOf: Cyprus Bar Association
---
Corpo in Markdown (H2/H3, liste, tabelle).
```

Chiavi obbligatorie delle pagine (identiche in tutte le lingue): `home`, `about`, `contact`, `larnaca`, `service-real-estate`, `service-corporate`, `service-immigration`, `service-banking`, `service-tax`, `service-wills`, `service-ip`, `service-litigation`, `service-civil-marriages`, `trustgate`, `csr`, `imprint`, `privacy`, `person-savvas`, `person-angelos`, `person-theodosis`, `person-marianna`. Le lingue DE/RU/EL devono avere almeno: home, about, contact, i 5 servizi obiettivo, imprint (breve rimando alla versione EN va bene), privacy (breve rimando alla EN).

## 6. Cosa fa il generatore (non ripeterlo nei contenuti)

Header/footer/nav per lingua, language switcher via `key`, hreflang + x-default, canonical, OG/Twitter, JSON-LD (LegalService su tutte, BreadcrumbList, Service+FAQPage sui servizi, Person sulle schede), sitemap.xml con hreflang, robots.txt con i bot AI nominati, llms.txt, .htaccess (www→non-www, https, trailing slash, header di sicurezza), data "Updated", pulsanti WhatsApp/Telegram, form Web3Forms, contatori con valori reali nell'HTML, alt su tutte le immagini.
