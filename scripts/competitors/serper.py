"""Chiamate Serper per il teardown concorrenti (budget 80). Ogni chiamata è registrata in
data/competitors/_serper_calls.csv; la risposta grezza va in data/competitors/serper/<nome>.json.
La chiave è letta da SERPER_API_KEY e passata a curl via stdin (mai in argv).
Uso: python3 scripts/competitors/serper.py <nome> <gl> <hl> <num> <query>"""
import csv, json, os, pathlib, subprocess, sys, time
BUDGET = 80
LOG = pathlib.Path("data/competitors/_serper_calls.csv")
OUT = pathlib.Path("data/competitors/serper"); OUT.mkdir(parents=True, exist_ok=True)
def used():
    return sum(1 for _ in open(LOG)) - 1 if LOG.exists() else 0
def search(name, gl, hl, num, q):
    f = OUT / f"{name}.json"
    if f.exists() and '"organic"' in f.read_text():
        return json.loads(f.read_text())
    if used() >= BUDGET:
        sys.exit("budget Serper esaurito")
    key = os.environ["SERPER_API_KEY"].strip()
    body = json.dumps({"q": q, "gl": gl, "hl": hl, "num": num}, ensure_ascii=False)
    r = subprocess.run(["curl", "-sS", "-m", "60", "-w", "\n%{http_code}", "-X", "POST",
                        "https://google.serper.dev/search", "-H", "Content-Type: application/json",
                        "-H", "@-", "-d", body], input=f"X-API-KEY: {key}\n", capture_output=True, text=True)
    resp, _, code = r.stdout.rpartition("\n")
    new = not LOG.exists()
    with open(LOG, "a", newline="") as fh:
        w = csv.writer(fh)
        if new: w.writerow(["n", "utc", "nome", "gl", "hl", "num", "query", "http", "organici"])
        try: org = len(json.loads(resp).get("organic", []))
        except Exception: org = ""
        w.writerow([used() + 1 if not new else 1, time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), name, gl, hl, num, q, code, org])
    f.write_text(resp)
    if not code.startswith("2"):
        sys.exit(f"Serper HTTP {code}: {resp[:200]}")
    return json.loads(resp)
if __name__ == "__main__":
    name, gl, hl, num, q = sys.argv[1:6]
    d = search(name, gl, hl, int(num), q)
    for i, o in enumerate(d.get("organic", []), 1):
        print(i, o.get("link"), "|", o.get("title"))
