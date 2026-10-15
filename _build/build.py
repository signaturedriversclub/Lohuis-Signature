#!/usr/bin/env python3
"""Assemble the site's HTML pages from _build/src/.

  python3 _build/build.py            write the pages to the repository root
  python3 _build/build.py --check    build in memory and report any page whose
                                     bytes differ from what is on disk

--check is the safety net: it is what proves the generator still reproduces the
site exactly. Run it before committing.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(ROOT, "_build", "src")

SECTIONS = ["commissions", "fleet", "the-house"]
CHILDREN = ["chauffeur", "concierge", "journey", "retainer"]
ORDER = ["index", "commissions", "chauffeur", "concierge", "journey", "retainer",
         "fleet", "the-house", "contact", "enquire", "faq", "privacy", "terms"]


def slurp(*parts):
    with open(os.path.join(*parts), encoding="utf-8") as fh:
        return fh.read()


def render(slug, layout, shared):
    meta   = json.loads(slurp(SRC, "pages", slug + ".json"))
    main   = slurp(SRC, "pages", slug + ".main.html")
    nodes  = slurp(SRC, "pages", slug + ".schema.jsonld")
    graph  = shared + (",\n" + nodes if nodes.strip() else "")

    out = layout
    out = out.replace("{{SCHEMA}}", graph)
    out = out.replace("{{MAIN}}", main)
    out = out.replace("{{TITLE}}", meta["title"])
    out = out.replace("{{DESCRIPTION}}", meta["description"])
    out = out.replace("{{CANONICAL}}", meta["canonical"])

    active = {meta.get("section"), meta.get("child")} - {None}
    for name in SECTIONS + CHILDREN:
        out = out.replace("{{AC:%s}}" % name,
                          ' aria-current="page"' if name in active else "")
    for name in SECTIONS:
        out = out.replace("{{SP:%s}}" % name,
                          "s92" if name == meta.get("section") else "s6")
    return out


def render_stub(slug, spec, templates):
    out = templates[spec["kind"]]
    out = out.replace("{{CANONICAL}}", spec["canonical"])
    out = out.replace("{{TARGET}}", spec["target"])
    out = out.replace("{{LABEL}}", spec["label"])
    return out


def main():
    check = "--check" in sys.argv
    layout = slurp(SRC, "layout.html")
    shared = slurp(SRC, "schema-shared.jsonld")
    stubs = json.loads(slurp(SRC, "stubs.json"))
    templates = {k: slurp(SRC, "stub-%s.html" % k) for k in ("moved", "vanity")}

    targets = [(slug, render(slug, layout, shared)) for slug in ORDER]
    targets += [(slug, render_stub(slug, spec, templates))
                for slug, spec in sorted(stubs.items())]

    differs = []
    for slug, built in targets:
        path  = os.path.join(ROOT, slug + ".html")
        if check:
            current = slurp(path) if os.path.exists(path) else None
            if current != built:
                differs.append(slug)
                print("  DIFFERS  %s.html" % slug)
            else:
                print("  ok       %s.html" % slug)
        else:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(built)

    if check:
        if differs:
            print("\n%d of %d file(s) differ: %s" % (len(differs), len(targets), ", ".join(differs)))
            return 1
        print("\nall %d files reproduce byte for byte" % len(targets))
        return 0
    print("wrote %d files (%d pages, %d stubs)" % (len(targets), len(ORDER), len(stubs)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
