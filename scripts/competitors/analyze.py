"""Analisi di una pagina HTML salvata dal crawler (data/competitors/<dominio>/*.html)."""
import json, re, sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
LANGS = r"\b(English|Greek|Russian|German|French|Italian|Spanish|Hebrew|Arabic|Chinese|Mandarin|Ukrainian|Polish|Romanian|Dutch|Swedish|Danish|Portuguese|Bulgarian|Farsi|Persian|Turkish|Hindi)\b"
NATS = r"\b(British|UK citizens|Israeli|Russian|Ukrainian|Chinese|Lebanese|Indian|American|German|Israelis|third[- ]country nationals|non-EU|EU citizens|expats?|foreigners?|foreign (?:nationals|buyers|investors))\b"
def head_body(path):
    raw = open(path, encoding="utf-8", errors="replace").read()
    i = raw.find("-->\n")
    return raw[:i], raw[i + 4:]
def meta_of(head):
    m = dict(re.findall(r"^(?:<!-- )?(GET|UA|status|final) (.*)$", head, re.M)); return m
def jsonld_types(soup):
    types = []
    for s in soup.find_all("script", type="application/ld+json"):
        try: d = json.loads(s.string or "")
        except Exception: types.append("(JSON non valido)"); continue
        stack = [d]
        while stack:
            x = stack.pop()
            if isinstance(x, list): stack += x
            elif isinstance(x, dict):
                t = x.get("@type")
                if t: types += t if isinstance(t, list) else [t]
                stack += [v for v in x.values() if isinstance(v, (list, dict))]
    return sorted(set(map(str, types)))
def analyze(path):
    head, body = head_body(path)
    m = meta_of(head)
    soup = BeautifulSoup(body, "lxml")
    base = m.get("final", "")
    hre = [(l.get("hreflang"), l.get("href")) for l in soup.find_all("link", hreflang=True)]
    jl = jsonld_types(soup)
    links = [urljoin(base, a.get("href", "")) for a in soup.find_all("a", href=True)]
    for t in soup(["script", "style", "noscript", "svg", "template"]): t.decompose()
    full = re.sub(r"\s+", " ", (soup.body or soup).get_text(" ", strip=True))
    # testo di contenuto: corpo senza header/footer/nav/aside/menu/cookie
    main = soup.body or soup
    for t in main.find_all(["header", "footer", "nav", "aside", "form"]): t.decompose()
    for t in main.find_all(attrs={"role": "navigation"}): t.decompose()
    for t in main.find_all(lambda x: x.has_attr("class") and re.search(r"(^|[-_ ])(menu|navbar|cookie|footer|site-header|breadcrumb)", " ".join(x.get("class") or []), re.I)):
        if not t.decomposed: t.decompose()
    text = re.sub(r"\s+", " ", main.get_text(" ", strip=True))
    h1 = [h.get_text(" ", strip=True) for h in soup.find_all("h1")]
    h2 = [h.get_text(" ", strip=True) for h in main.find_all("h2")]
    dom = urlparse(base).netloc.replace("www.", "")
    ext = sorted({l for l in links if urlparse(l).netloc and dom not in urlparse(l).netloc})
    src = [l for l in ext if re.search(r"gov\.cy|cylaw\.org|cyprusbarassociation|eur-lex|cysec|centralbank\.cy|mfa|oecd|europa\.eu|leginet|gazette", l, re.I)]
    dates = re.findall(r"(?:Updated|Last updated|Last reviewed|Reviewed|Published|Posted|Modified)[^.]{0,25}?(\d{1,2}[ /.-]\w+[ /.-]\d{4}|\w+ \d{1,2},? \d{4}|\d{4}-\d{2}-\d{2})", full, re.I)
    tm = soup.find("meta", property="article:modified_time"); tp = soup.find("meta", property="article:published_time")
    faq_head = [h for h in h2 + [x.get_text(" ", strip=True) for x in main.find_all(["h3", "h4"])] if re.search(r"FAQ|Frequently Asked|Questions|Häufig|Fragen|вопрос", h, re.I)]
    faq = {"jsonld": "FAQPage" in jl, "heading": faq_head[:2]}
    return dict(file=path, url=m.get("GET"), status=m.get("status"), final=base,
        lang=(BeautifulSoup(body, "lxml").html or {}).get("lang") if BeautifulSoup(body, "lxml").html else None,
        title=(BeautifulSoup(body, "lxml").title.string.strip() if BeautifulSoup(body, "lxml").title and BeautifulSoup(body, "lxml").title.string else ""),
        words_main=len(text.split()), words_body=len(full.split()), h1=h1, h2=h2, h2_n=len(h2),
        faq=faq, jsonld=jl, hreflang=hre, dates_visible=dates[:5],
        meta_modified=tm.get("content") if tm else None, meta_published=tp.get("content") if tp else None,
        ext_sources=src[:20], ext_links_n=len(ext),
        langs_mentioned=sorted(set(re.findall(LANGS, full))), nats_mentioned=sorted(set(x.lower() for x in re.findall(NATS, full, re.I))),
        tax2026=bool(re.search(r"(2026).{0,80}(tax reform|reform|amend|changes)|(tax reform|reform).{0,80}2026", full, re.I)),
        whatsapp=sorted({l for l in links if re.search(r"wa\.me|whatsapp", l, re.I)})[:3],
        telegram=sorted({l for l in links if re.search(r"t\.me/|telegram", l, re.I)})[:3],
        viber=sorted({l for l in links if re.search(r"viber", l, re.I)})[:3],
        links=links)
if __name__ == "__main__":
    for p in sys.argv[1:]:
        d = analyze(p); d.pop("links")
        print(json.dumps(d, ensure_ascii=False))
