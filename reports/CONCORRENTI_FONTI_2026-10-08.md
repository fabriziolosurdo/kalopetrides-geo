# Teardown concorrenti — Parte B: dove sono citati fuori dal sito

Data: 2026-10-08. Metodo:
- **Serper** (`gl=cy`, `hl=en`, `num=20`; per Philippou anche `gl=de`/`hl=de` e `gl=ru`/`hl=ru`): una ricerca per nome dello studio tra virgolette (risultati esclusi del dominio dello studio), più ricerche `site:<fonte>` con i nomi degli studi in OR e ricerche "nome studio" su più fonti in OR. Tutte le risposte in `data/competitors/serper/`, registro in `data/competitors/_serper_calls.csv`, risultati attribuiti a ciascuno studio in `data/competitors/_presenze_serper.csv`. Google ha restituito tra 7 e 10 risultati per le ricerche sul nome, non 20.
- **GET** (stesse regole della Parte A) delle pagine delle fonti per capire cosa sono e come ci si entra: `data/sources/<dominio>/`.
- Le citazioni ZeroRank sono quelle del brief (baseline del 07/10, 374 citazioni su 91 risposte); non sono state ricalcolate.

Omonimi esclusi a mano: Andreas Neocleous & Co (neocleous.com, studio diverso da Elias Neocleous), Haviaras & Philippou, Connor Legal (Australia), Chrysses Demetriades & Co, Costas P. Demetriades, Lellos P. Demetriades (studi diversi da Andreas Demetriades), "Kalopetrides Georgios" su cypruslaw.com e G. Kalopetrides & Partners / P. Kalopetrides & Co (non sono il cliente).

## 1. Matrice studi × fonti

Legenda: ✅ presente (URL nei file citati) · ❌ assente, verificato su un elenco completo scaricato · ❔ non trovato con Serper, quindi non verificato · — non applicabile (ente pubblico o sito di un altro studio, nessuno "ci entra").
"Konstantinou/GK" vale per i n. 3 e 9 del brief (stesso studio, vedi Parte A).

Righe ordinate per citazioni ZeroRank, poi per numero di studi trovati.

| Fonte | Citazioni ZeroRank | Studi trovati (su 8) | Philippou | Patrikios | Konstantinou/GK | Neocleous | Chrysostomides | Demetriades | Kyprianou | Connor | **Kalopetrides** |
|---|---|---|---|---|---|---|---|---|---|---|---|
| legal500.com | 48 | 7 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | **❌** |
| chambers.com | 21 | 4 | ❔ | ✅ | ❔ | ✅ | ✅ | ❔ | ✅ | ❔ | **❔** |
| gov.cy | 20 | — | — | — | — | — | — | — | — | — | — |
| practiceguides.chambers.com | 11 | 3 | ❔ (logo sul proprio sito) | ✅ | ✅ | ❔ | ❔ | ❔ | ✅ | ❔ | **❔** |
| lawzana.com | 9 | 8 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **✅** |
| cypruslawyers.co.uk | 6 | 1 | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | **❌** |
| cypruslaw.com.cy | 6 | — (è il sito dello studio Georgiades & Pelides) | — | — | — | — | — | — | — | — | — |
| lawyer.com.cy | 4 | — (è il sito dello studio Christophi & Associates) | — | — | — | — | — | — | — | — | — |
| globallawexperts.com | 2 | 1 | ❔ | ❔ | ❔ | ❔ | ❔ | ❔ | ✅ | ❔ | **❔** |
| mip.gov.cy | 2 | — | — | — | — | — | — | — | — | — | — |
| iflr1000 (iflr.com) | 2 | 3 | ❔ | ✅ | ❔ | ✅ (scheda di Elias Neocleous) | ❔ | ❔ | ✅ | ❔ | **❔** |
| legalhelpcy.com | 1 | 0 | ❔ | ❔ | ❔ | ❔ | ❔ | ❔ | ❔ | ❔ | **✅** |
| linkedin.com | — | 7 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❔ | **✅ (profilo personale + annuncio)** |
| facebook.com | — | 6 | ✅ | ❔ | ✅ | ✅ | ❔ | ✅ | ✅ | ✅ | **✅ (profilo personale)** |
| cypruslaw.com | — | 7 | ❔ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **❔** |
| mondaq.com | — | 6 | ✅ | ✅ | ❔ | ✅ | ✅ | ✅ | ✅ | ❔ | **❔** |
| lawyersincyprus.com | — | 5 | ✅ | ❔ | ✅ | ❔ | ✅ | ❔ | ✅ (articolo) | ✅ | **❔** |
| cy.usembassy.gov (elenco avvocati) | — | 5 | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | **❌** |
| lexology.com | — | 5 | ❔ | ✅ | ❔ | ✅ | ✅ | ✅ | ✅ | ❔ | **❔** |
| cyprusbarassociation.org (annunci di lavoro) | — | 4 | ❔ | ✅ | ❔ | ❔ | ❔ | ✅ | ✅ | ✅ | **❔** |
| ergodotisi.com (lavoro) | — | 3 | ✅ | ❔ | ✅ | ❔ | ✅ | ❔ | ❔ | ❔ | **✅** |
| internationaltaxreview.com | — | 2 | ❔ | ❔ | ❔ | ✅ | ✅ | ❔ | ❔ | ❔ | **❔** |
| cyprus-mail.com | — | 1 | ❔ | ❔ | ❔ | ✅ (10 articoli) | ❔ | ❔ | ❔ | ❔ | **❔** |
| iclg.com | — | 1 | ❔ | ❔ | ❔ | ❔ | ❔ | ✅ | ❔ | ❔ | **❔** |
| telegraph.co.uk, dailymail.co.uk, expatnetwork.com | — | 1 | ✅ | ❔ | ❔ | ❔ | ❔ | ❔ | ❔ | ❔ | **❔** |

Come è stato verificato ogni ❌:
- legal500.com: pagina `legal500.com/c/cyprus/directory` (88 studi linkati), scaricata: Connor e Kalopetrides non ci sono; più 2 ricerche Serper senza risultati.
- cypruslawyers.co.uk: pagina `/directory` scaricata: un solo studio in elenco (Andreas Demetriades & Co LLC).
- cy.usembassy.gov: PDF "List of Attorneys – Republic of Cyprus" (aggiornato a novembre 2024, 32 studi), scaricato in `data/sources/cy.usembassy.gov/`: presenti George K. Konstantinou, Elias Neocleous, Dr. K. Chrysostomides, Michael Kyprianou (2 voci), N. Connor; assenti Philippou, Patrikios, Andreas Demetriades, Kalopetrides. Per Larnaca il PDF elenca 3 studi.

Ricerche sul nome — domini trovati per studio (esclusi il sito dello studio e gli omonimi), classificati:

| Studio | Classifica | Directory | Ente | Testata / editoriale | Associazione | Social / UGC | Altro |
|---|---|---|---|---|---|---|---|
| Philippou (cy) | legal500 | lawyersincyprus, ergodotisi (lavoro) | — | mondaq | — | linkedin, facebook | — |
| Philippou (de) | legal500 | lawyersincyprus, ergodotisi, carierista (lavoro) | — | mondaq | — | linkedin, facebook | — |
| Philippou (ru) | legal500 | lawyersincyprus, lawzana, ergodotisi | — | mondaq | — | linkedin, facebook | — |
| Patrikios | legal500, chambers, iflr1000 | cyprusprofile (registro privato) | cyprusbarassociation (annuncio) | practicallaw (Thomson Reuters) | laworld (rete) | linkedin | — |
| Konstantinou/GK | legal500 | lawyersincyprus, ergodotisi, jccsmart | cy.usembassy.gov | — | cyhrma.org | linkedin, facebook | — |
| Neocleous | chambers, internationaltaxreview | — | — | — | — | linkedin, facebook | wikipedia |
| Chrysostomides | internationaltaxreview | lawyersincyprus, cypruslaw.com, lawcrossing, ergodotisi | — | occrp.org (inchiesta) | — | linkedin | mystrikingly (pagina vetrina) |
| Demetriades | legal500, iclg | — | — | israel.imhbusiness | irglobal (rete) | linkedin, facebook | — |
| Kyprianou | legal500, chambers | — | cy.usembassy.gov | — | — | linkedin, facebook | shiparrested.com (rete) |
| Connor | — | lawzana, lawyersincyprus, cypruslaw.com | cyprusbarassociation (annuncio) | — | — | facebook | — |
| Kalopetrides | — | lawzana, legalhelpcy, cyprusprocurement, ergodotisi, cypruswork | — | — | israel-cyprus.co.il (camera di commercio) | linkedin, instagram, facebook | ioannoullc.com (scheda "Savvas Kalopetrides" su un altro studio), lumetri-media.com (portfolio di un'agenzia) |

## 2. Scheda per fonte

### Classifiche ("si entra per merito")

**legal500.com** — classifica Legal 500 (EMEA) con profili di studio e avvocato. Si entra con la *submission* nel ciclo di ricerca annuale (modelli scaricabili, portale, calendario per giurisdizione) più feedback di clienti e colleghi raccolto dai ricercatori (`the-legal-500-submission-information`). Costo della submission: non indicato nella pagina letta. Lingua: EN. **48 citazioni ZeroRank** (prima fonte assoluta; 8 in tedesco, 4 in russo). Studi presenti: 7 su 8; mancano Connor e Kalopetrides. Profili con ranking verificati via URL `rankings/ranking/c-cyprus/…`: Patrikios (banking and finance), Chrysostomides (dispute resolution), Demetriades (real estate and construction), Kyprianou (employment, IP), Neocleous (IP). Philippou ha un profilo "about" in cui dichiara "(Ranked in Legal 500 EMEA 2026)": testo dello studio, ranking non verificato.

**chambers.com** — classifica Chambers and Partners (Europe, Global, High Net Worth). "Submitting to Chambers is free" (`chambers.com/info/submissions`): submission su modello + ricerca indipendente. Lingua: EN. **21 citazioni ZeroRank** (4 in tedesco, 3 in russo). Presenti: Patrikios (Europe, Global, HNW), Neocleous, Chrysostomides, Kyprianou. Il profilo Patrikios riporta lingue dello studio (EN, FR, DE, EL, IT, RU, SK), numero di partner e avvocati.

**practiceguides.chambers.com** — Chambers Global Practice Guides: capitoli per paese ("Law and Practice", "Trends and Developments"). Come si entra (dalla home): "For every guide we select Contributing Editors who are ranked in the relevant Chambers Guides…; the individual contributors … are selected on the same basis". Quindi su invito e collegato al ranking Chambers. Lingua: EN. **11 citazioni ZeroRank**. Presenti: Patrikios (Corporate Tax 2026), Konstantinou/GK (Real Estate 2026 Cyprus, autrice Stalo Konstantinou), Kyprianou (Corporate Governance, Dispute Resolution 2026). GK compare anche se non risulta su chambers.com: il requisito "ranked" sopra vale per i Contributing Editors, per i contributori dei capitoli "Trends and Developments" la regola effettiva non è verificata.

**iflr1000 (iflr.com/iflr1000)** — classifica finanziaria e societaria di IFLR (Legal Benchmarking Ltd). Schede studio con numero di avvocati, partner, lingue, reti. Processo di inserimento: non leggibile nelle pagine scaricate (non verificato). **2 citazioni ZeroRank**. Presenti: Patrikios, Kyprianou, Elias Neocleous (scheda personale).

**internationaltaxreview.com (ITR World Tax)** — classifica fiscale. Processo: non verificato. 0 citazioni ZeroRank nell'elenco. Presenti: Neocleous, Chrysostomides.

### Directory

**lawzana.com** — directory internazionale di avvocati con pagine per area e città ("The 10 best Immigration Lawyers in Cyprus (2026)"). Sito dietro challenge Cloudflare: 4 GET su 4 respinte, quindi **condizioni d'ingresso e prezzi non verificati**. Lingue: EN, EL (URL `/el/…`), altre non verificate. **9 citazioni ZeroRank** (3 in tedesco). Presenti tutti e 9, Kalopetrides incluso ("SAVVAS KALOPETRIDES LLC", Larnaca); nelle liste Serper Kalopetrides compare a pagina 9 (immigration) e 10 (golden visa).

**cypruslawyers.co.uk** — directory cipriota nuova: "List Your Law Firm in Cyprus — Free". Inserimento **gratuito** ("€0 to list … Free, forever"), con verifica dell'iscrizione all'ordine e dell'identità ("We check Bar membership and identity"); visibilità a pagamento opzionale: **€19 una settimana, €34 due settimane, €59 quattro settimane** in cima a una categoria (`/pricing`). Dichiara profili "indexed for Google and AI search". Il giorno della verifica la directory elenca **un solo studio** (Andreas Demetriades). Lingua: EN. **6 citazioni ZeroRank** (verosimilmente le sue guide: ha una sezione `publications`; non verificato quali pagine siano citate).

**lawyersincyprus.com** — portale "Cyprus Legal Portal" con schede studio e articoli. Pacchetti (`/list-your-firm/`): **"Basic Yearly Subscription FREE"** (nome, sede, telefono, città) e pacchetti Premium / Premium Blog / Featured Blog a preventivo ("Request Quote", prezzi non pubblicati). Lingua: EN. 0 citazioni ZeroRank nell'elenco, ma nelle SERP Google del 06/10 compare in seconda posizione in q2 e in q5 `cy/en` (con un articolo e con la categoria "taxation law"). Presenti: Philippou, Konstantinou/GK, Chrysostomides, Connor, Kyprianou (con un articolo).

**legalhelpcy.com** — directory cipriota con prenotazione di consulenze (EN, EL, RU). Registrazione con account, poi profilo (`/help/add-profile`); costo: non indicato nelle pagine lette (`/user/register` vietato da robots.txt, non scaricato). **1 citazione ZeroRank.** Kalopetrides è presente ("KALOPETRIDES LLC", Gladstonos 1, Office 205, 6023 Larnaca; lingue EN, EL, RU; pubblicato il 15/09/2026); la pagina di ricerca mostra 16 profili, nessuno dei concorrenti.

**cypruslaw.com** — directory del network CyprusNet ("Cyprus Law"), schede per città. Inserimento: esistono schede "Free Listing" (es. Michael Kyprianou) e pubblicità a pagamento (`article/advertise.html`, prezzi non pubblicati); in home compaiono come inserzionisti Elias Neocleous, Patrikios, Chrysses Demetriades, Kinanis, Frangos. Lingue: EN, alcune schede in DE. 0 citazioni ZeroRank. Presenti 7 su 8.

**globallawexperts.com** — rete/directory internazionale a membership: "fill out the below form and a member of our team will contact you to discuss our selection process and pricing" (`/join/`). Quindi **a pagamento e con selezione** (prezzo non pubblico). Lingua: EN. **2 citazioni ZeroRank.** Presente con certezza Kyprianou (articoli e news); altri studi compaiono negli snippet di articoli, non verificato.

**cy.usembassy.gov — List of Attorneys** — elenco PDF dell'Ambasciata USA (sezione consolare) per città; "information … provided directly by the lawyers"; inclusione non è un endorsement. Come ci si entra: la procedura non è descritta nelle pagine lette (non verificato); il contatto della sezione consolare è nel PDF. Lingua: EN. Presenti 5 su 8.

**ergodotisi.com, cypruswork.com, carierista.com, jccsmart.com, cyprusprofile.com, cyprusprocurement.com** — portali di lavoro, registri commerciali privati e appalti: la scheda nasce pubblicando annunci o dai registri. Kalopetrides è già su ergodotisi, cypruswork, cyprusprocurement.

### Enti

**gov.cy** — portale del governo cipriota (in greco ed inglese): servizi, moduli, informazioni dei dipartimenti. Non elenca studi: **non ci si entra**, lo si cita. **20 citazioni ZeroRank** (3 in tedesco, 3 in russo): i motori AI lo usano come fonte primaria su residenza, tasse, società. Per il cliente conta come link in uscita dalle proprie pagine (GK e Philippou linkano gov.cy, companies.gov.cy, cylaw.org).

**mip.gov.cy** — dominio storico del Dipartimento Anagrafe e Migrazione (oggi anche `gov.cy/mip-md`, linkato da Philippou). L'8/10 risponde con certificato TLS scaduto: nessuna pagina letta. Non ci si entra. **2 citazioni ZeroRank.**

**cyprusbarassociation.org** — ordine degli avvocati. Le occorrenze trovate sono annunci di lavoro (Patrikios, Demetriades, Kyprianou, Connor). Albo e ricerca avvocati: non verificati.

### Testate ed editoriali

**mondaq.com** — piattaforma di articoli legali con profilo studio e pagine autore (Philippou, Patrikios, Neocleous, Chrysostomides, Demetriades, Kyprianou). Condizioni (programma contributor): non verificate. 0 citazioni ZeroRank nell'elenco. Philippou lo mostra tra i loghi "Featured in".

**lexology.com** — piattaforma di articoli e "Lexology Index" (riconoscimenti). Profili: Patrikios, Neocleous, Chrysostomides, Demetriades, Kyprianou. Condizioni: non verificate.

**cyprus-mail.com** — quotidiano in inglese. 10 risultati su 10 della ricerca congiunta sono su Elias Neocleous (premi, sponsorizzazioni, operazioni). Se si tratti di contenuti a pagamento: non verificato.

**telegraph.co.uk, dailymail.co.uk, expatnetwork.com** — Philippou è citato come fonte esperta: Telegraph ("Eleni Philippou, of Philippou Law Firm in Paphos, said…"), Daily Mail ("Experts at Philippou Law say…"), Expat Network ("New research from the immigration lawyers at Philippou Law, has dived into Google search data…"). È digital PR basata su dati propri.

### Siti di altri studi citati dai motori AI (non sono fonti in cui "entrare")

**cypruslaw.com.cy** è il sito dello studio Georgiades & Pelides LLC; **lawyer.com.cy** è il sito di Christophi & Associates (Nicosia). Il brief li elencava tra le fonti non-studio: verificato aprendo la home, sono concorrenti (6 e 4 citazioni ZeroRank).

## 3. Lista "da prendere"

Fonti dove Kalopetrides non c'è, ottenibili senza classifica. Ordine: numero di concorrenti presenti; a parità, prima quelle citate dai motori AI.

| # | Fonte | Concorrenti presenti | Citata dai motori AI | Costo | Cosa serve |
|---|---|---|---|---|---|
| 1 | cypruslaw.com | 7 | no (nell'elenco ZeroRank) | scheda gratuita + pubblicità a pagamento (prezzo non pubblico) | Registrarsi ("Register"), creare la scheda dello studio a Larnaca, chiedere il listino pubblicitario; verificare che non si confonda con la voce "Kalopetrides Georgios". |
| 2 | mondaq.com | 6 | no | non verificato | Profilo studio + articoli firmati (es. riforma fiscale 2026, residenza): chiedere le condizioni del programma contributor. |
| 3 | lawyersincyprus.com | 5 | no (ma in SERP Google) | Basic gratis; Premium a preventivo | Compilare `/list-your-firm/` con il pacchetto Basic; valutare "Premium Blog" per pubblicare articoli. |
| 4 | Elenco avvocati Ambasciata USA | 5 | no | non verificato (nessun prezzo indicato) | Chiedere l'inserimento alla sezione consolare (contatto nel PDF) con aree, lingue, indirizzo di Larnaca; nella sezione Larnaca oggi ci sono 3 studi. |
| 5 | lexology.com | 5 | no | non verificato | Profilo studio e contributi; chiedere le condizioni. |
| 6 | cypruslawyers.co.uk | 1 | **sì, 6 citazioni** | **gratis** (boost opzionale €19–59) | Form di 2 minuti su `/list-your-firm` (nome, anno, team, città, fino a 6 aree, contatti); verifica dell'iscrizione all'ordine. Oggi elenca un solo studio. |
| 7 | globallawexperts.com | 1 verificato | **sì, 2 citazioni** | a pagamento, con selezione (prezzo non pubblico) | Richiesta di membership da `/join/`; poi articoli pubblicati sul sito. |

Già presenti, da sistemare:
- **lawzana.com** (9 citazioni ZeroRank): scheda "SAVVAS KALOPETRIDES LLC". Completare aree, lingue e descrizione; non verificabile da qui (Cloudflare).
- **legalhelpcy.com**: scheda "KALOPETRIDES LLC". Il nome differisce sia da "Kalopetrides Law LLC" (titolo del sito) sia da "Savvas Kalopetrides LLC" (lawzana, Instagram, ergodotisi): uniformare nome, indirizzo e telefono su tutte le fonti.

## 4. Lista "da meritare"

| Fonte | Citazioni ZeroRank | Concorrenti presenti | Cosa richiede |
|---|---|---|---|
| Legal 500 | 48 | 7 | Submission annuale per area (modelli e calendario Cipro sulla pagina submissions), referenze di clienti contattati dai ricercatori, lavori documentabili. Per il cliente le aree plausibili sono real estate, corporate, banking (dove sono classificati Demetriades, Patrikios). |
| Chambers (Europe/Global/HNW) | 21 | 4 | Submission gratuita su modello (dichiarato da Chambers) + ricerca indipendente con referenze; classifica più selettiva (4 su 8). |
| Chambers Global Practice Guides | 11 | 3 | Invito: i Contributing Editors sono scelti tra i classificati Chambers. |
| IFLR1000 | 2 | 3 | Classifica su finanza e societario; processo non verificato. |
| ITR World Tax | 0 | 2 | Classifica fiscale; processo non verificato. |
| Cyprus Mail | 0 | 1 | Notizie su premi, operazioni, eventi (Neocleous ne ha 10); se a pagamento: non verificato. |
| Telegraph, Daily Mail, Expat Network | 0 | 1 | Commenti esperti e ricerche con dati propri proposti ai giornalisti (modello Philippou: analisi delle ricerche Google dei britannici che si trasferiscono). |
| Lexology Index, Who's Who Legal, Citywealth, Best Lawyers | 0 | 1+ | Riconoscimenti citati da Kyprianou nei propri post (non verificati sulle fonti). |
