"""A2-A4: parse the raw 200 responses saved in data/site/ and write data/site/_analysis.json."""
import json, re, pathlib
from bs4 import BeautifulSoup, Comment
SITE = pathlib.Path("data/site")
PAGES = {
 "/ (home)": "https_kalopetrideslaw_com__browser__try5.txt",
 "/about-us.html": "https_kalopetrideslaw_com_about_us_html__browser__try5.txt",
 "/services-overview.html": "https_kalopetrideslaw_com_services_overview_html__browser__try5.txt",
 "/trustgate.html": "https_kalopetrideslaw_com_trustgate_html__browser__try5.txt",
 "/csr.html": "https_kalopetrideslaw_com_csr_html__browser__try2.txt",
 "/imprint.html": "https_kalopetrideslaw_com_imprint_html__browser__try1.txt",
 "/privacy-policy.html": "https_kalopetrideslaw_com_privacy_policy_html__browser__try4.txt",
 "404 page (/llms.txt)": "https_kalopetrideslaw_com_llms_txt__browser__try5.txt",
}
def body_of(raw):
    i = raw.lower().find("<!doctype"); i = i if i >= 0 else raw.lower().find("<html")
    j = raw.rfind("<<<CURL"); return raw[i:j]
def headers_of(raw):
    blocks = raw.split("\n\n"); h = [b for b in blocks if b.startswith("HTTP/2") or b.startswith("HTTP/1.1 3")]
    return h[-1] if h else ""
out = {}
for name, fn in PAGES.items():
    raw = (SITE/fn).read_text(errors="replace"); html = body_of(raw)
    s = BeautifulSoup(html, "lxml")
    d = {"file": f"data/site/{fn}"}
    d["html_lang"] = s.html.get("lang") if s.html else None
    t = s.title.get_text(strip=True) if s.title else ""
    d["title"] = t; d["title_len"] = len(t)
    md = s.find("meta", attrs={"name": "description"}); md = md.get("content","") if md else ""
    d["meta_description"] = md; d["meta_description_len"] = len(md)
    c = s.find("link", rel="canonical"); d["canonical"] = c.get("href") if c else None
    d["hreflang"] = [(l.get("hreflang"), l.get("href")) for l in s.find_all("link", hreflang=True)]
    d["meta_robots"] = [m.get("content") for m in s.find_all("meta", attrs={"name": re.compile("robots", re.I)})]
    d["og"] = {m.get("property"): m.get("content") for m in s.find_all("meta", property=re.compile("^og:"))}
    d["twitter"] = {m.get("name"): m.get("content") for m in s.find_all("meta", attrs={"name": re.compile("^twitter:")})}
    lds = []
    for sc in s.find_all("script", type="application/ld+json"):
        try:
            j = json.loads(sc.string); lds.append({"valid_json": True, "type": j.get("@type"), "keys": sorted(j.keys()), "data": j})
        except Exception as e:
            lds.append({"valid_json": False, "error": str(e)})
    d["jsonld"] = lds
    d["headings"] = [(h.name, re.sub(r"\s+"," ",h.get_text(" ",strip=True))) for h in s.find_all(re.compile("^h[1-3]$"))]
    d["h1_count"] = sum(1 for h in d["headings"] if h[0]=="h1")
    imgs = s.find_all("img"); d["img_total"] = len(imgs)
    d["img_alt_missing_or_empty"] = [i.get("src") for i in imgs if not (i.get("alt") or "").strip()]
    links = [a.get("href") for a in s.find_all("a", href=True)]
    d["links_internal"] = sorted(set(h for h in links if not re.match(r"^(https?:|mailto:|tel:)", h) or "kalopetrideslaw.com" in h))
    d["links_external"] = sorted(set(h for h in links if re.match(r"^https?:", h) and "kalopetrideslaw.com" not in h))
    d["links_mailto_tel"] = sorted(set(h for h in links if re.match(r"^(mailto:|tel:)", h)))
    forms = []
    for f in s.find_all("form"):
        forms.append({"action": f.get("action"), "method": f.get("method"), "id": f.get("id"), "attrs": dict(f.attrs),
                      "fields": [(i.name, i.get("type"), i.get("name")) for i in f.find_all(["input","textarea","select"])]})
    d["forms"] = forms
    d["scripts"] = [sc.get("src") for sc in s.find_all("script") if sc.get("src")]
    d["inline_scripts"] = [ (sc.get("type"), len(sc.string or "")) for sc in s.find_all("script") if not sc.get("src")]
    d["data_count_attrs"] = [ (el.name, {k:v for k,v in el.attrs.items() if k.startswith("data-")}, el.get_text(strip=True)) for el in s.find_all(attrs=lambda a: a and any(k.startswith("data-count") or k.startswith("data-target") for k in a)) ][:20]
    d["dates_visible"] = sorted(set(re.findall(r"(?:Last (?:updated|modified)[^<\n]{0,40}|\b(?:19|20)\d{2}\b)", s.get_text(" "))))[:30]
    for x in s(["script","style","noscript","template"]): x.decompose()
    for x in s.find_all(string=lambda t: isinstance(t, Comment)): x.extract()
    text = re.sub(r"\s+"," ", s.body.get_text(" ") if s.body else "")
    d["word_count_visible"] = len(re.findall(r"\b[\w’'-]+\b", text))
    d["lang_markers"] = sorted(set(re.findall(r"(?:lang|language|flag)[-_ ]?[a-z]{0,6}", html, re.I)))[:30]
    d["headers"] = headers_of(raw)
    out[name] = d
(SITE/"_analysis.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
for n,d in out.items():
    print(f"== {n}: lang={d['html_lang']} title({d['title_len']})={d['title']!r}\n desc({d['meta_description_len']}) canon={d['canonical']} hreflang={d['hreflang']} robots={d['meta_robots']}\n og={len(d['og'])} tw={len(d['twitter'])} jsonld={[ (l.get('type'),l.get('valid_json')) for l in d['jsonld']]} words={d['word_count_visible']} imgs={d['img_total']} alt_missing={d['img_alt_missing_or_empty']}\n H={d['headings']}\n forms={d['forms']}\n scripts={d['scripts']} inline={d['inline_scripts']}\n internal={d['links_internal']}\n external={d['links_external']} mt={d['links_mailto_tel']}\n dates={d['dates_visible']}\n counts={d['data_count_attrs']}")
