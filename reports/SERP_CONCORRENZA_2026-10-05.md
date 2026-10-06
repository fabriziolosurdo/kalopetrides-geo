# Concorrenza su Google (Serper) — Kalopetrides Law

Data: 2026-10-05 · aggiornato 2026-10-06 (SERP raccolte la sera del 6 ottobre)

## Esito

Il 2026-10-06 la chiamata di prova (`python3 scripts/serp_run.py --prova`) ha risposto con risultati validi; poi sono state completate le altre 14. **15 SERP su 15 raccolte** (5 query × `cy/en`, `de/de`, `ru/ru`, top 10 organici), JSON in `data/serp/q{n}_{gl}_{hl}.json`.

- **Chiamate Serper usate in tutto: 18 su 60** (3 fallite con 403 il 5–6/10, 15 riuscite il 6/10).
- In questo ambiente `SERPER_API_KEY` risultava impostata, quindi lo script l'ha inviata in `X-API-KEY`; il ramo "senza chiave, la inietta il proxy" non è stato usato.
- **kalopetrideslaw.com non compare in nessuna delle 15 SERP** (top 10).
- legalhelpcy.com compare una volta: posizione 10 in q4 `ru/ru`, con la pagina di ricerca della directory (`/ru/search`), non con una scheda di Kalopetrides.

## Query preparate

| # | gl=cy, hl=en | gl=de, hl=de | gl=ru, hl=ru |
|---|---|---|---|
| 1 | best real estate lawyers in Cyprus for foreigners buying property | beste Anwälte für Immobilienkauf auf Zypern für Ausländer | лучшие юристы на Кипре по покупке недвижимости для иностранцев |
| 2 | corporate lawyers in Cyprus for company formation by non-residents | Anwälte für Firmengründung auf Zypern für Nicht-Residenten | юристы на Кипре по регистрации компании для нерезидентов |
| 3 | immigration lawyers in Cyprus for permanent residency by investment | Anwälte für Daueraufenthaltsgenehmigung auf Zypern durch Investition | иммиграционные юристы на Кипре по ПМЖ за инвестиции |
| 4 | banking and finance law firms in Cyprus | Kanzleien für Bank- und Finanzrecht auf Zypern | юридические фирмы на Кипре по банковскому и финансовому праву |
| 5 | tax lawyers in Cyprus for international tax planning | Steueranwälte auf Zypern für internationale Steuerplanung | налоговые юристы на Кипре по международному налоговому планированию |

Note di traduzione: in tedesco "auf Zypern" è la forma corrente; "Nicht-Residenten" è il termine usato nelle ricerche fiscali/societarie. In russo "ПМЖ" (постоянное место жительства) è il modo naturale in cui si cerca la residenza permanente; "регистрация компании" è più comune di "создание компании".

## Top 5 per query

Domini in ordine di posizione (organici, top 10 raccolti; in q3 `de/de` e q5 `de/de` Google ha restituito 7 risultati).

| # | gl=cy, hl=en | gl=de, hl=de | gl=ru, hl=ru |
|---|---|---|---|
| 1 | cyprusestateagency.com, gk-lawfirm.com, demetriadeslaw.com, primerus.com, argen-law.com | demetriadeslaw.com, connorlegalllc.com, anwalt.de, nikosia.diplo.de, kyprianou.com | gk-lawfirm.com, feodgroup.com, demetriadeslaw.com, connorlegalllc.com, hasporealty.com |
| 2 | efstathioulaw.com, lawyersincyprus.com, agplaw.com, cplawyers.com, philippoulaw.com | zypern-limited.com, firma-ausland.de, gruendungskanzlei.eu, cypruslifehub.com, connorlegalllc.com | gk-lawfirm.com, nsvcons.com, imperiallegal.com, tranio.ru, kiaplaw.ru |
| 3 | gk-lawfirm.com, demetriadeslaw.com, efstathioulaw.com, lawzana.com, diogenouslaw.com | demetriadeslaw.com, propertylawyer-cyprus.com, residencypartners.com, danoslawfirm.com, demetriadeslaw.com | gk-lawfirm.com, feodgroup.com, passportivity.com, hadjivangeli.com, immigrantinvest.com |
| 4 | legal500.com, neo.law, kyprianou.com, paplaw.com.cy, ag-advocates.eu | kyprianou.com, nikosia.diplo.de, connorlegalllc.com, demetriadeslaw.com, kyprianou.com | ru.fidulink.com, connorlegalllc.com, moudouroslaw.com, hadjivangeli.com, demetriadeslaw.com |
| 5 | neo.law, lawyersincyprus.com, legal500.com, mylonas.law, kyprianou.com | kyprianou.com, connorlegalllc.com, rechtsanwalt-zypern.net, my-global-tax.com, kyprianou.com | gk-lawfirm.com, mtargetgroup.com, connorlegalllc.com, hadjivangeli.com, kyprianou.com |

## Domini ricorrenti (numero di SERP su 15 in cui compaiono)

| Dominio | SERP | Lingue in cui compare |
|---|---|---|
| demetriadeslaw.com | 9 | EN, DE, RU |
| kyprianou.com | 7 | EN, DE, RU |
| connorlegalllc.com | 7 | DE, RU |
| gk-lawfirm.com | 6 | EN, RU |
| philippoulaw.com | 4 | EN, DE |
| lawzana.com, feodgroup.com, diogenouslaw.com, moudouroslaw.com, hadjivangeli.com | 3 | — |

Osservazioni dai dati (titoli e URL dei risultati):
- I concorrenti che ricorrono sono studi ciprioti con **una pagina per area di pratica in ogni lingua** (es. `demetriadeslaw.com/de/Bank--und-Finanzrecht/`, `gk-lawfirm.com/ru/praktiki/nalogi-na-kipre/`, `kyprianou.com/de/expertises/internationale-steuerplanung-zypern/`). Nelle SERP DE e RU vincono URL in `/de/` e `/ru/` con titolo nella lingua della ricerca.
- In inglese su `gl=cy` i primi posti sono più frammentati (molti studi diversi, più directory come legal500.com, lawzana.com, primerus.com).
- Nelle SERP `de/de` e `ru/ru` occupano spazio anche siti non di studi legali: agenzie di costituzione società (q2 DE quasi tutta), agenzie immobiliari e di immigrazione (q1 e q3 RU), l'ambasciata tedesca (nikosia.diplo.de), anwalt.de, YouTube e Instagram. In q1 DE tre risultati riguardano Cipro Nord.
- Nessun answer box, "People also ask" o AI Overview nei JSON restituiti da Serper; solo in q5 `de/de` ci sono le ricerche correlate.

## Giudizio sulla difficoltà (5 righe)

1. Oggi Kalopetrides è assente da tutte le 15 SERP: si parte da zero in ogni lingua.
2. Inglese (`gl=cy`): difficoltà alta. Le prime posizioni sono divise tra molti studi ciprioti e directory affermate; serve una pagina per servizio più autorevolezza (directory, citazioni).
3. Tedesco: difficoltà media. Gli studi presenti sono pochi e ricorrenti (Demetriades, Kyprianou, Connor, Danos, Philippou) e il resto sono agenzie e portali: una pagina tedesca curata per servizio può entrare in top 10.
4. Russo: difficoltà media-alta. Mercato affollato da studi con pagine russe mature (GK, Demetriades, Hadjivangeli, Moudouros) e agenzie di immigrazione e relocation.
5. In tutte le lingue la condizione minima è la stessa: pagine dedicate per servizio nella lingua della ricerca, che oggi il sito non ha.

## Cosa manca sul sito (dal solo sito, vedi audit tecnico)

Per ciascuna delle 5 query il sito non ha una pagina dedicata che risponda: c'è solo una sezione di 119–162 parole dentro `services-overview.html`, in solo inglese. Per le versioni DE e RU delle query il sito non ha alcun contenuto nella lingua della ricerca.

Da fare ancora (manualmente): verifica con GET delle pagine dei concorrenti principali (numero di lingue, lunghezza, dati strutturati) e controllo se legalhelpcy.com ha una scheda di Kalopetrides.

## Storico: tentativi falliti del 5–6 ottobre

La prima chiamata di prova a `https://google.serper.dev/search` (POST JSON, senza header `X-API-KEY`, come da brief) ha risposto:

```
HTTP 403
{"message":"Unauthorized.","statusCode":403}
```

File: `data/serp/_first_call_403.json` (risposta) e `data/serp/_first_call_request.json` (richiesta).

Come previsto dal brief ("se la prima chiamata risponde 401 o 403, la credenziale non è attiva: salta tutta la Parte B"), non sono state fatte altre chiamate.

- **Chiamate Serper usate: 3 su 60** (1 il 05/10, 2 il 06/10: vedi sotto).
- Nessun dato SERP raccolto: nessuna tabella query × top 10, nessun dominio ricorrente, nessuna posizione per kalopetrideslaw.com o legalhelpcy.com.
- Nessun giudizio sulla difficoltà: senza SERP osservate non è formulabile senza inventare.

Probabile causa (non verificata): la credenziale Serper dell'ambiente cloud non è attiva o non viene iniettata dal proxy per questa sessione; Serper riceve la richiesta senza chiave valida. Da controllare nelle impostazioni dell'ambiente (credenziale API per `google.serper.dev`).

### Riesecuzione del 2026-10-06

1. `python3 scripts/serp_run.py`: la prima delle 15 chiamate (q1, `gl=cy`, `hl=en`) ha di nuovo risposto `403 {"message":"Unauthorized.","statusCode":403}` e lo script si è fermato. File: `data/serp/_rerun_2026-10-06_403.json`.
2. Una sola chiamata di diagnosi con `curl -v`, stessa query. Output completo in `data/serp/_debug.txt`; eventuali righe con chiavi sarebbero oscurate, ma nessuna era presente.

Cosa mostra `_debug.txt`:

| Fase | Header |
|---|---|
| Tunnel verso il proxy locale | `CONNECT google.serper.dev:443` → `HTTP/1.1 200 Connection Established` |
| Richiesta inviata dal client | `POST /search`, `Host: google.serper.dev`, `User-Agent: curl/8.5.0`, `Accept: */*`, `Content-Type: application/json`, `Content-Length: 102`. **Nessun `X-API-KEY`**, come da brief |
| Risposta di Serper | `HTTP/1.1 403 Forbidden`, `Server: Google Frontend`, `Via: 1.1 google`, `Content-Type: application/json`, corpo `{"message":"Unauthorized.","statusCode":403}` |

Lettura:
- La risposta arriva davvero da Serper (`Server: Google Frontend`, corpo JSON di Serper). Il proxy non blocca l'host: un blocco del proxy darebbe un errore sul `CONNECT`, che invece riceve 200.
- **Non verificabile dal container**: se il proxy aggiunga l'header `X-API-KEY`. L'iniezione avverrebbe a valle del tunnel TLS, quindi `curl -v` vede solo gli header inviati dal client. La pagina di stato del proxy non elenca credenziali per `google.serper.dev` e non registra errori per quell'host.
- In entrambi i casi il risultato è lo stesso: Serper riceve la richiesta senza una chiave valida. O la credenziale non è configurata o iniettata per questo ambiente, o la chiave salvata non è valida o non ha più crediti.
- Rimedio (Fab): nelle impostazioni dell'ambiente cloud (menu dell'ambiente nella barra del titolo della sessione → Edit), verificare o aggiungere la API credential per `google.serper.dev`, poi aprire una **nuova** sessione. In alternativa si può salvare la chiave come variabile d'ambiente (es. `SERPER_API_KEY`) e adattare `scripts/serp_run.py` per leggerla. La chiave non va mai incollata in chat. Conviene anche controllare dalla dashboard di serper.dev che la chiave sia attiva e abbia crediti.
