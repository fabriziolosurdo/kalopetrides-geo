#!/usr/bin/env python3
"""Static site generator for kalopetrideslaw.com.

Reads site/config.yaml, site/i18n/<lang>.yaml and site/content/<lang>/*.md (YAML front matter + Markdown),
renders templates in site/templates/ and writes the deployable site to dist/.

Usage:  python3 site/build.py            (from the repo root)
        python3 site/build.py --check    (build + run consistency checks, non-zero exit on failure)
"""
import sys, re, json, shutil, datetime, pathlib, html
import yaml, markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = pathlib.Path(__file__).resolve().parent
REPO = ROOT.parent
DIST = REPO / "dist"
CONFIG = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))
SITE_URL = CONFIG["site_url"].rstrip("/")
TODAY = datetime.date.today().isoformat()

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", re.S)


def load_i18n(lang):
    p = ROOT / "i18n" / f"{lang}.yaml"
    base = yaml.safe_load((ROOT / "i18n" / "en.yaml").read_text(encoding="utf-8"))
    if p.exists():
        base.update(yaml.safe_load(p.read_text(encoding="utf-8")) or {})
    return base


def md_to_html(text):
    return markdown.markdown(
        text,
        extensions=["extra", "sane_lists", "smarty", "toc"],
        extension_configs={"toc": {"toc_depth": "2-3", "permalink": False}},
    )


def slug_url(lang, slug):
    prefix = CONFIG["languages"][lang]["prefix"]
    parts = [p for p in [prefix, slug.strip("/")] if p]
    return "/" + "/".join(parts) + "/" if parts else "/"


def read_pages():
    pages = {}  # (lang, key) -> page dict
    for lang in CONFIG["languages"]:
        d = ROOT / "content" / lang
        if not d.exists():
            continue
        for f in sorted(d.glob("*.md")):
            raw = f.read_text(encoding="utf-8")
            m = FM_RE.match(raw)
            if not m:
                raise SystemExit(f"{f}: missing front matter")
            fm = yaml.safe_load(m.group(1)) or {}
            body = m.group(2)
            if "key" not in fm or "type" not in fm:
                raise SystemExit(f"{f}: front matter needs key and type")
            fm.setdefault("slug", "")
            fm["lang"] = lang
            fm["url"] = slug_url(lang, fm["slug"])
            fm["abs_url"] = SITE_URL + fm["url"]
            fm["body_md"] = body
            fm["body_html"] = md_to_html(body)
            fm["word_count"] = len(re.findall(r"\w+", re.sub(r"<[^>]+>", " ", fm["body_html"])))
            fm["updated"] = str(fm.get("updated") or TODAY)
            fm["source_file"] = str(f.relative_to(REPO))
            pages[(lang, fm["key"])] = fm
    return pages


def add_index_pages(pages):
    """Services and team index pages are generated, not authored."""
    for lang in CONFIG["languages"]:
        t = load_i18n(lang)
        if (lang, "home") not in pages:
            continue
        slugs = {"en": ("services", "team"), "de": ("leistungen", "team"), "ru": ("uslugi", "komanda"), "el": ("ypiresies", "omada")}
        s_slug, t_slug = slugs.get(lang, ("services", "team"))
        for key, slug, title, desc, h1, intro, nav in [
            ("services-index", s_slug, t["services_index_title"], t["services_index_description"], t["services_index_h1"], t["services_index_intro"], t["our_services"]),
            ("team-index", t_slug, t["team_index_title"], t["team_index_description"], t["team_index_h1"], t["team_index_intro"], t["our_team"]),
        ]:
            if (lang, key) in pages:
                continue
            pages[(lang, key)] = {
                "key": key, "type": "index", "slug": slug, "lang": lang, "title": title, "description": desc,
                "h1": h1, "summary": intro, "nav_label": nav, "updated": TODAY, "body_md": "", "body_html": "",
                "url": slug_url(lang, slug), "abs_url": SITE_URL + slug_url(lang, slug), "word_count": 0,
                "source_file": "(generated)",
            }
    return pages


def alternates(pages, key):
    out = []
    for lang in CONFIG["languages"]:
        p = pages.get((lang, key))
        if p:
            out.append({"lang": lang, "hreflang": CONFIG["languages"][lang]["hreflang"], "url": p["abs_url"], "name": CONFIG["languages"][lang]["name"]})
    return out


def org_jsonld(lang):
    a = CONFIG["address"]
    d = {
        "@type": "LegalService",
        "@id": SITE_URL + "/#organization",
        "name": CONFIG["firm_name"],
        "alternateName": CONFIG["alternate_name"],
        "url": SITE_URL + "/",
        "logo": SITE_URL + CONFIG["logo"],
        "image": SITE_URL + CONFIG["og_image"],
        "telephone": CONFIG["phone_e164"],
        "email": CONFIG["email"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": f"{a['building']}, {a['street']}",
            "addressLocality": a["city"],
            "postalCode": a["postal_code"],
            "addressCountry": a["country_code"],
        },
        "geo": {"@type": "GeoCoordinates", "latitude": CONFIG["geo"]["lat"], "longitude": CONFIG["geo"]["lng"]},
        "hasMap": CONFIG["map_embed"].split("&z=")[0],
        "areaServed": [{"@type": "Country", "name": "Cyprus"}],
        "knowsLanguage": CONFIG["languages_spoken"],
        "founder": {"@type": "Person", "@id": SITE_URL + "/team/savvas-kalopetrides/#person", "name": "Savvas Kalopetrides", "jobTitle": "Lawyer"},
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": CONFIG["hours"]["days"], "opens": o, "closes": c}
            for o, c in CONFIG["hours"]["ranges"]
        ],
    }
    if CONFIG.get("same_as"):
        d["sameAs"] = CONFIG["same_as"]
    return d


def page_jsonld(page, pages, t):
    graph = [org_jsonld(page["lang"])]
    crumbs = [{"@type": "ListItem", "position": 1, "name": t["breadcrumb_home"], "item": SITE_URL + slug_url(page["lang"], "")}]
    if page["type"] in ("service", "person", "page", "legal", "index"):
        parent = None
        if page["type"] == "service":
            parent = pages.get((page["lang"], "services-index"))
        elif page["type"] == "person":
            parent = pages.get((page["lang"], "team-index"))
        if parent:
            crumbs.append({"@type": "ListItem", "position": 2, "name": parent["nav_label"], "item": parent["abs_url"]})
        crumbs.append({"@type": "ListItem", "position": len(crumbs) + 1, "name": page.get("nav_label") or page["h1"], "item": page["abs_url"]})
    if len(crumbs) > 1:
        graph.append({"@type": "BreadcrumbList", "itemListElement": crumbs})
    graph.append({
        "@type": "WebPage", "@id": page["abs_url"] + "#webpage", "url": page["abs_url"], "name": page["title"],
        "description": page.get("description", ""), "inLanguage": page["lang"], "dateModified": page["updated"],
        "isPartOf": {"@id": SITE_URL + "/#website"}, "about": {"@id": SITE_URL + "/#organization"},
    })
    if page["type"] == "service":
        graph.append({
            "@type": "Service", "@id": page["abs_url"] + "#service", "name": page["h1"], "description": page.get("summary", ""),
            "url": page["abs_url"], "serviceType": page.get("service_type") or page["h1"],
            "provider": {"@id": SITE_URL + "/#organization"}, "areaServed": {"@type": "Country", "name": "Cyprus"},
            "availableLanguage": CONFIG["languages_spoken"],
        })
        if page.get("faq"):
            graph.append({
                "@type": "FAQPage", "@id": page["abs_url"] + "#faq",
                "mainEntity": [
                    {"@type": "Question", "name": q["q"], "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", md_to_html(q["a"]))}}
                    for q in page["faq"]
                ],
            })
    if page["type"] == "person" and page.get("person"):
        p = page["person"]
        d = {"@type": "Person", "@id": page["abs_url"] + "#person", "name": p["name"], "jobTitle": p.get("jobTitle", ""),
             "url": page["abs_url"], "worksFor": {"@id": SITE_URL + "/#organization"}, "description": page.get("summary", "")}
        if p.get("image"):
            d["image"] = SITE_URL + p["image"]
        if p.get("alumniOf"):
            d["alumniOf"] = {"@type": "CollegeOrUniversity", "name": p["alumniOf"]}
        if p.get("memberOf"):
            d["memberOf"] = {"@type": "Organization", "name": p["memberOf"]}
        graph.append(d)
    graph.insert(1, {"@type": "WebSite", "@id": SITE_URL + "/#website", "url": SITE_URL + "/", "name": CONFIG["firm_name"], "publisher": {"@id": SITE_URL + "/#organization"}, "inLanguage": [l for l in CONFIG["languages"]]})
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)


def build():
    pages = add_index_pages(read_pages())
    env = Environment(loader=FileSystemLoader(str(ROOT / "templates")), autoescape=select_autoescape(["html"]), trim_blocks=True, lstrip_blocks=True)
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    shutil.copytree(ROOT / "static", DIST, dirs_exist_ok=True)

    by_lang = {}
    for (lang, key), p in pages.items():
        by_lang.setdefault(lang, {})[key] = p

    for (lang, key), page in pages.items():
        t = load_i18n(lang)
        lp = by_lang[lang]
        ctx = {
            "cfg": CONFIG, "t": t, "page": page, "lang": lang, "lang_cfg": CONFIG["languages"][lang],
            "pages": lp, "alternates": alternates(pages, key), "home_url": slug_url(lang, ""),
            "nav": [lp[k] for k in CONFIG["nav_keys"] if k in lp],
            "services_primary": [lp[k] for k in CONFIG["service_keys_primary"] if k in lp],
            "services_secondary": [lp[k] for k in CONFIG["service_keys_secondary"] if k in lp],
            "persons": [lp[k] for k in CONFIG["person_keys"] if k in lp],
            "jsonld": page_jsonld(page, pages, t), "faq_html": [(q["q"], md_to_html(q["a"])) for q in page.get("faq", [])],
            "site_url": SITE_URL, "today": TODAY,
            "x_default": (pages.get(("en", key)) or page)["abs_url"],
        }
        tpl = env.get_template({"home": "home.html", "service": "service.html", "person": "person.html", "index": "index.html"}.get(page["type"], "page.html"))
        out = DIST / page["url"].strip("/") / "index.html" if page["url"] != "/" else DIST / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(tpl.render(**ctx), encoding="utf-8")

    write_sitemap(pages)
    write_robots()
    write_llms(pages)
    write_404(env)
    return pages


def write_sitemap(pages):
    keys = sorted({k for (_, k) in pages})
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for key in keys:
        alts = alternates(pages, key)
        for lang in CONFIG["languages"]:
            p = pages.get((lang, key))
            if not p or p["type"] == "legal":
                continue
            lines.append("  <url>")
            lines.append(f"    <loc>{p['abs_url']}</loc>")
            lines.append(f"    <lastmod>{p['updated']}</lastmod>")
            for a in alts:
                lines.append(f'    <xhtml:link rel="alternate" hreflang="{a["hreflang"]}" href="{a["url"]}"/>')
            en = pages.get(("en", key))
            if en:
                lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{en["abs_url"]}"/>')
            lines.append("  </url>")
    lines.append("</urlset>")
    (DIST / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_robots():
    bots = ["Googlebot", "Bingbot", "GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User",
            "PerplexityBot", "Perplexity-User", "Google-Extended", "Applebot", "Applebot-Extended", "CCBot", "DuckAssistBot", "Amazonbot", "meta-externalagent"]
    out = ["# kalopetrideslaw.com — search engines and AI assistants are welcome to read this site.", ""]
    for b in bots:
        out += [f"User-agent: {b}", "Allow: /", ""]
    out += ["User-agent: *", "Allow: /", "", f"Sitemap: {SITE_URL}/sitemap.xml", ""]
    (DIST / "robots.txt").write_text("\n".join(out), encoding="utf-8")


def write_llms(pages):
    a = CONFIG["address"]
    en = {k: p for (l, k), p in pages.items() if l == "en"}
    out = [f"# {CONFIG['firm_name']}", "",
           f"> Law firm in Larnaca, Cyprus. Real estate, corporate and commercial, immigration, banking and finance, tax, wills and probate, intellectual property, litigation, civil marriages. Founder and managing director: Savvas Kalopetrides, member of the Cyprus Bar Association. Office: {a['building']}, {a['street']}, {a['postal_code']} {a['city']}, Cyprus. Phone {CONFIG['phone_display']}. Email {CONFIG['email']}. Languages: English, Greek, German, Russian. Site languages: " + ", ".join(CONFIG["languages"][l]["name"] for l in CONFIG["languages"]) + ".", ""]
    out += ["## Services", ""]
    for k in CONFIG["service_keys_primary"] + CONFIG["service_keys_secondary"]:
        p = en.get(k)
        if p:
            out.append(f"- [{p['h1']}]({p['abs_url']}): {p.get('summary','').strip()}")
    out += ["", "## People", ""]
    for k in CONFIG["person_keys"]:
        p = en.get(k)
        if p:
            out.append(f"- [{p['h1']}]({p['abs_url']}): {p.get('summary','').strip()}")
    out += ["", "## Other pages", ""]
    for k in ["about", "larnaca", "contact", "trustgate", "csr", "imprint", "privacy"]:
        p = en.get(k)
        if p:
            out.append(f"- [{p['h1']}]({p['abs_url']}): {p.get('summary','').strip()}")
    out += ["", "## Other languages", ""]
    for lang in CONFIG["languages"]:
        if lang == "en":
            continue
        for k in ["home"] + CONFIG["service_keys_primary"]:
            p = pages.get((lang, k))
            if p:
                out.append(f"- [{p['h1']}]({p['abs_url']}) ({CONFIG['languages'][lang]['name']})")
    out += ["", f"Updated: {TODAY}", ""]
    (DIST / "llms.txt").write_text("\n".join(out), encoding="utf-8")


def write_404(env):
    t = load_i18n("en")
    tpl = env.get_template("404.html")
    (DIST / "404.html").write_text(tpl.render(cfg=CONFIG, t=t, lang="en", lang_cfg=CONFIG["languages"]["en"], home_url="/", site_url=SITE_URL, page={"title": "Page not found", "url": "/404.html", "abs_url": SITE_URL + "/404.html", "noindex": True, "updated": TODAY, "h1": "Page not found"}, alternates=[], nav=[], pages={}, services_primary=[], services_secondary=[], persons=[], jsonld="", faq_html=[], today=TODAY), encoding="utf-8")


def check(pages):
    """Consistency checks: required keys per language, internal links, title/description lengths, JSON-LD parse."""
    errors, warnings = [], []
    required_en = ["home", "about", "contact", "larnaca", "service-real-estate", "service-corporate", "service-immigration", "service-banking", "service-tax",
                   "service-wills", "service-ip", "service-litigation", "service-civil-marriages", "trustgate", "csr", "imprint", "privacy",
                   "person-savvas", "person-angelos", "person-theodosis", "person-marianna"]
    required_other = ["home", "about", "contact", "service-real-estate", "service-corporate", "service-immigration", "service-banking", "service-tax", "imprint", "privacy"]
    for k in required_en:
        if ("en", k) not in pages:
            errors.append(f"missing en/{k}")
    for lang in CONFIG["languages"]:
        if lang == "en" or not any(l == lang for (l, _) in pages):
            continue
        for k in required_other:
            if (lang, k) not in pages:
                errors.append(f"missing {lang}/{k}")
    urls = {p["url"] for p in pages.values()}
    for p in pages.values():
        if len(p.get("title", "")) > 65:
            warnings.append(f"{p['source_file']}: title {len(p['title'])} chars")
        d = p.get("description", "")
        if not (100 <= len(d) <= 165):
            warnings.append(f"{p['source_file']}: description {len(d)} chars")
        if p["type"] == "service" and p["lang"] == "en" and p["key"] in CONFIG["service_keys_primary"] and p["word_count"] < 1400:
            warnings.append(f"{p['source_file']}: only {p['word_count']} words")
        for href in re.findall(r'href="(/[^"#?]*)', p["body_html"]):
            if href.startswith("/assets/"):
                continue
            h = href if href.endswith("/") else href + "/"
            if h not in urls:
                errors.append(f"{p['source_file']}: broken internal link {href}")
    for f in DIST.rglob("*.html"):
        s = f.read_text(encoding="utf-8")
        for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
            try:
                json.loads(m.group(1))
            except Exception as e:
                errors.append(f"{f}: invalid JSON-LD: {e}")
        for href in re.findall(r'href="(/[^"#?]*)', s):
            if href.startswith("/assets/") or href in ("/sitemap.xml", "/robots.txt", "/llms.txt"):
                continue
            h = href if href.endswith("/") else href + "/"
            if h not in urls:
                errors.append(f"{f.relative_to(DIST)}: broken link {href}")
        for a in re.findall(r"<img(?![^>]*\balt=)[^>]*>", s):
            errors.append(f"{f.relative_to(DIST)}: img without alt: {a[:80]}")
    for w in warnings:
        print("WARN", w)
    for e in sorted(set(errors)):
        print("ERROR", e)
    print(f"{len(pages)} pages, {len(set(errors))} errors, {len(warnings)} warnings")
    return not errors


if __name__ == "__main__":
    pages = build()
    print(f"built {len(pages)} pages into {DIST}")
    if "--check" in sys.argv:
        sys.exit(0 if check(pages) else 1)
