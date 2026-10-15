#!/usr/bin/env python3
"""Assemble the site's HTML from _build/src/.

  python3 _build/build.py            write the pages
  python3 _build/build.py --check    build in memory and report any file whose
                                     bytes differ from what is on disk

--check is the safety net: it proves the generator still reproduces the site
exactly. Run it before committing.

English is served from the site root and Dutch from /nl/. The root pages were
indexed long before Dutch existed, and GitHub Pages cannot issue a real 301, so
moving them would mean replacing live pages with client-side redirect stubs.
Dutch is additive instead: no existing address changes.
"""
import hashlib, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(ROOT, "_build", "src")
BASE = "https://www.lohuissignature.nl/"

SECTIONS = ["commissions", "fleet", "the-house"]
CHILDREN = ["chauffeur", "concierge", "journey", "retainer"]

# Terms and privacy stay English-only for now, so Dutch pages must not claim an
# hreflang="nl" for them: a hreflang pointing at a page that does not exist is
# worse than none at all.
PAGES = ["index", "commissions", "chauffeur", "concierge", "journey", "retainer",
         "fleet", "the-house", "contact", "enquire", "faq", "privacy", "terms"]
ENGLISH_ONLY = {"privacy", "terms"}

LANGS = {
    "en": {"dir": "",    "lang": "en", "locale": "en_GB", "root": ""},
    "nl": {"dir": "nl/", "lang": "nl", "locale": "nl_NL", "root": "../"},
}

# A page's address matches the label a visitor sees on it, so /nl/wagenpark.html
# sits under a nav item reading "Wagenpark". Pages are absent from this map when
# that label is already the same in both languages - chauffeur, concierge,
# retainer, contact - and FAQ, which is a loan abbreviation Dutch uses as its
# own, the way the site already uses roadshow and concierge.
#
# Settled before anything under /nl/ was published: once a URL is indexed,
# changing it costs a redirect stub, which is what we refused to do to the
# English pages.
SLUGS = {
    "en": {},
    "nl": {"commissions": "missies", "journey": "reis", "fleet": "wagenpark",
           "the-house": "het-huis", "enquire": "aanvragen"},
}


def slug_for(lang, page):
    return SLUGS.get(lang, {}).get(page, page)


def slurp(*parts):
    with open(os.path.join(*parts), encoding="utf-8") as fh:
        return fh.read()


def exists(lang, slug):
    return os.path.exists(os.path.join(SRC, "pages", lang, slug + ".main.html"))


def pages_for(lang):
    return [s for s in PAGES if exists(lang, s)]


def url_for(lang, page):
    d = LANGS[lang]["dir"]
    return BASE + d if page == "index" else BASE + d + slug_for(lang, page) + ".html"


def out_path(lang, page):
    return os.path.join(ROOT, LANGS[lang]["dir"], slug_for(lang, page) + ".html")


def hreflang_block(slug):
    """Alternates for one page. x-default is English: it is the fallback for
    visitors who match neither language, not a statement about which matters."""
    langs = [l for l in ("en", "nl") if exists(l, slug)]
    lines = ['<link rel="alternate" hreflang="%s" href="%s">' % (l, url_for(l, slug))
             for l in langs]
    lines.append('<link rel="alternate" hreflang="x-default" href="%s">'
                 % url_for("en", slug))
    return "\n".join(lines)


def asset_version(relpath):
    """?v= derived from the file's own bytes. It changes when the file changes
    and not otherwise, so a stylesheet edit reaches people immediately instead
    of waiting out the ten-minute cache, and an unchanged file stays cached."""
    path = os.path.join(ROOT, relpath)
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as fh:
        return "?v=" + hashlib.sha256(fh.read()).hexdigest()[:8]


def rel_url(from_lang, to_lang, page):
    """Address of `page` in to_lang, relative to a page sitting in from_lang."""
    up = "../" if LANGS[from_lang]["dir"] else ""
    down = LANGS[to_lang]["dir"]
    if page == "index":
        return (up + down) or "index.html"
    return up + down + slug_for(to_lang, page) + ".html"


def lang_switch(lang, page, strings):
    """Both labels, always in the same order so the pair does not move when
    used. The current one is inert; the other is the link. A page with no
    counterpart - terms and privacy are English only - points at the other
    language's homepage rather than at nothing."""
    label = strings.get("aria.lang", "")
    other = "nl" if lang == "en" else "en"
    target = page if exists(other, page) else "index"
    href = rel_url(lang, other, target)
    link = ('<a href="%s" class="s258" hreflang="%s" lang="%s" aria-label="%s">%s</a>'
            % (href, other, other, label, other.upper()))
    here = '<span class="s259" aria-current="true">%s</span>' % lang.upper()
    sep = '<span class="s260" aria-hidden="true">&middot;</span>'
    parts = [here, sep, link] if lang == "en" else [link, sep, here]
    return '<span class="s257">%s</span>' % "".join(parts)


def render(lang, slug, layout, shared, strings):
    cfg   = LANGS[lang]
    meta  = json.loads(slurp(SRC, "pages", lang, slug + ".json"))
    main  = slurp(SRC, "pages", lang, slug + ".main.html")
    nodes = slurp(SRC, "pages", lang, slug + ".schema.jsonld")
    graph = shared + (",\n" + nodes if nodes.strip() else "")

    out = layout
    out = out.replace("{{SCHEMA}}", graph)
    out = out.replace("{{MAIN}}", main)
    out = out.replace("{{HREFLANG}}", hreflang_block(slug))
    out = out.replace("{{TITLE}}", meta["title"])
    out = out.replace("{{DESCRIPTION}}", meta["description"])
    out = out.replace("{{CANONICAL}}", url_for(lang, slug))
    out = out.replace("{{LANG}}", cfg["lang"])
    out = out.replace("{{LOCALE}}", cfg["locale"])
    out = out.replace("{{ROOT}}", cfg["root"])

    for key, val in strings.items():
        out = out.replace("{{S:%s}}" % key, val)

    # site.js writes some of its own interface text. English lives in the script
    # as its fallback, so only other languages need to hand it a table.
    out = out.replace("{{LANGSWITCH}}", lang_switch(lang, slug, strings))
    out = out.replace("{{V:css}}", asset_version("css/site.css"))
    out = out.replace("{{V:js}}", asset_version("js/site.js"))

    js = {k: v for k, v in strings.items() if k.startswith("js.")}
    out = out.replace("{{I18N}}", "<script>window.LS_I18N=%s;</script>\n"
                      % json.dumps(js, ensure_ascii=False, sort_keys=True) if js else "")
    for page in PAGES:
        out = out.replace("{{U:%s}}" % page, slug_for(lang, page) + ".html")

    active = {meta.get("section"), meta.get("child")} - {None}
    for name in SECTIONS + CHILDREN:
        out = out.replace("{{AC:%s}}" % name,
                          ' aria-current="page"' if name in active else "")
    for name in SECTIONS:
        out = out.replace("{{SP:%s}}" % name,
                          "s92" if name == meta.get("section") else "s6")
    return out


def render_stub(spec, templates):
    out = templates[spec["kind"]]
    for token, val in (("{{CANONICAL}}", spec["canonical"]),
                       ("{{TARGET}}", spec["target"]),
                       ("{{LABEL}}", spec["label"])):
        out = out.replace(token, val)
    return out


def main():
    check  = "--check" in sys.argv
    layout = slurp(SRC, "layout.html")
    shared = slurp(SRC, "schema-shared.jsonld")
    stubs  = json.loads(slurp(SRC, "stubs.json"))
    templates = {k: slurp(SRC, "stub-%s.html" % k) for k in ("moved", "vanity")}

    targets = []
    for lang in LANGS:
        strings = json.loads(slurp(SRC, "chrome", lang + ".json")) if \
            os.path.exists(os.path.join(SRC, "chrome", lang + ".json")) else {}
        for slug in pages_for(lang):
            targets.append((out_path(lang, slug),
                            render(lang, slug, layout, shared, strings)))
    for slug, spec in sorted(stubs.items()):
        targets.append((os.path.join(ROOT, slug + ".html"),
                        render_stub(spec, templates)))

    differs = []
    for path, built in targets:
        rel = os.path.relpath(path, ROOT)
        if check:
            current = slurp(path) if os.path.exists(path) else None
            if current != built:
                differs.append(rel)
                print("  %-9s %s" % ("NEW" if current is None else "DIFFERS", rel))
            else:
                print("  ok        %s" % rel)
        else:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(built)

    if check:
        if differs:
            print("\n%d of %d file(s) differ: %s"
                  % (len(differs), len(targets), ", ".join(differs)))
            return 1
        print("\nall %d files reproduce byte for byte" % len(targets))
        return 0
    print("wrote %d files" % len(targets))
    return 0


if __name__ == "__main__":
    sys.exit(main())
