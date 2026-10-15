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
import json, os, sys

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


def slurp(*parts):
    with open(os.path.join(*parts), encoding="utf-8") as fh:
        return fh.read()


def exists(lang, slug):
    return os.path.exists(os.path.join(SRC, "pages", lang, slug + ".main.html"))


def pages_for(lang):
    return [s for s in PAGES if exists(lang, s)]


def url_for(lang, slug):
    d = LANGS[lang]["dir"]
    return BASE + d if slug == "index" else BASE + d + slug + ".html"


def out_path(lang, slug):
    return os.path.join(ROOT, LANGS[lang]["dir"], slug + ".html")


def hreflang_block(slug):
    """Alternates for one page. x-default is English: it is the fallback for
    visitors who match neither language, not a statement about which matters."""
    langs = [l for l in ("en", "nl") if exists(l, slug)]
    lines = ['<link rel="alternate" hreflang="%s" href="%s">' % (l, url_for(l, slug))
             for l in langs]
    lines.append('<link rel="alternate" hreflang="x-default" href="%s">'
                 % url_for("en", slug))
    return "\n".join(lines)


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
