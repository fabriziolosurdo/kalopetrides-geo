# Concorrenza su Google (Serper) — Kalopetrides Law

Data: 2026-10-05

## Esito: Parte B NON eseguita

La prima chiamata di prova a `https://google.serper.dev/search` (POST JSON, senza header `X-API-KEY`, come da brief) ha risposto:

```
HTTP 403
{"message":"Unauthorized.","statusCode":403}
```

File: `data/serp/_first_call_403.json` (risposta) e `data/serp/_first_call_request.json` (richiesta).

Come previsto dal brief ("se la prima chiamata risponde 401 o 403, la credenziale non è attiva: salta tutta la Parte B"), non sono state fatte altre chiamate.

- **Chiamate Serper usate: 1 su 60.**
- Nessun dato SERP raccolto: nessuna tabella query × top 10, nessun dominio ricorrente, nessuna posizione per kalopetrideslaw.com o legalhelpcy.com.
- Nessun giudizio sulla difficoltà: senza SERP osservate non è formulabile senza inventare.

Probabile causa (non verificata): la credenziale Serper dell'ambiente cloud non è attiva o non viene iniettata dal proxy per questa sessione; Serper riceve la richiesta senza chiave valida. Da controllare nelle impostazioni dell'ambiente (credenziale API per `google.serper.dev`).

## Pronto per la riesecuzione

`scripts/serp_run.py` esegue le 15 chiamate (5 query × `cy/en`, `de/de`, `ru/ru`) e salva i JSON in `data/serp/q{n}_{gl}_{hl}.json`; si ferma alla prima risposta 401/403. Query preparate:

| # | gl=cy, hl=en | gl=de, hl=de | gl=ru, hl=ru |
|---|---|---|---|
| 1 | best real estate lawyers in Cyprus for foreigners buying property | beste Anwälte für Immobilienkauf auf Zypern für Ausländer | лучшие юристы на Кипре по покупке недвижимости для иностранцев |
| 2 | corporate lawyers in Cyprus for company formation by non-residents | Anwälte für Firmengründung auf Zypern für Nicht-Residenten | юристы на Кипре по регистрации компании для нерезидентов |
| 3 | immigration lawyers in Cyprus for permanent residency by investment | Anwälte für Daueraufenthaltsgenehmigung auf Zypern durch Investition | иммиграционные юристы на Кипре по ПМЖ за инвестиции |
| 4 | banking and finance law firms in Cyprus | Kanzleien für Bank- und Finanzrecht auf Zypern | юридические фирмы на Кипре по банковскому и финансовому праву |
| 5 | tax lawyers in Cyprus for international tax planning | Steueranwälte auf Zypern für internationale Steuerplanung | налоговые юристы на Кипре по международному налоговому планированию |

Note di traduzione: in tedesco "auf Zypern" è la forma corrente; "Nicht-Residenten" è il termine usato nelle ricerche fiscali/societarie. In russo "ПМЖ" (постоянное место жительства) è il modo naturale in cui si cerca la residenza permanente; "регистрация компании" è più comune di "создание компании".

Dopo la riesecuzione restano da fare (manualmente o in una nuova sessione): classificazione dei risultati, verifica con GET di pagina dedicata e lingue per gli studi legali, domini ricorrenti, giudizio in 5 righe.

## Cosa si può dire senza SERP (dal solo sito, vedi audit tecnico)

Per ciascuna delle 5 query il sito non ha una pagina dedicata che risponda: c'è solo una sezione di 119–162 parole dentro `services-overview.html`, in solo inglese. Per le versioni DE e RU delle query il sito non ha alcun contenuto nella lingua della ricerca.
