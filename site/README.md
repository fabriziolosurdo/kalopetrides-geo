# kalopetrideslaw.com — new site (static, generated)

- `site/content/<lang>/*.md` — one file per page: YAML front matter + Markdown. Rules and format: `site/BRIEF_SITO_2026-10-15.md`.
- `site/i18n/<lang>.yaml` — interface strings (menu, form, footer) per language.
- `site/config.yaml` — firm data used everywhere (address, phone, hours, form key, logos, languages).
- `site/templates/` — Jinja2 templates; `site/static/` — CSS, JS and `.htaccess` copied as-is into `dist/`.
- `site/build.py` — generator. `python3 site/build.py --check` builds `dist/` and runs consistency checks
  (required pages per language, broken internal links, JSON-LD validity, images without alt, title/description lengths).

## Build

```
pip install jinja2 markdown pyyaml   # once
python3 site/build.py --check
```

## Deploy (for the webmaster)

1. Keep the existing `/assets/` folder on the server exactly as it is (images and fonts are referenced from it).
2. Delete the old `*.html` files from the web root, upload the whole content of `dist/` to the web root
   (including the hidden `.htaccess`, `robots.txt`, `sitemap.xml`, `llms.txt`, `404.html` and the `site/` folder with CSS/JS).
3. In SiteGround Site Tools → Security, make sure the anti-bot challenge does not apply to verified search and AI crawlers,
   or disable it: the audit of 5 October 2026 showed 80% of automated requests receiving the challenge page instead of the site.
4. Nothing changes in DNS. Old URLs (`about-us.html`, `services-overview.html`, …) are redirected by `.htaccess`.
