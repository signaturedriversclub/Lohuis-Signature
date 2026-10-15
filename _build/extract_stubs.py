#!/usr/bin/env python3
"""One-time decomposition of the 14 forwarding stubs into _build/src/.

Two kinds exist and the distinction is deliberate:
  moved   - an address the old Squarespace site used, kept so old links work
  vanity  - a short address meant to be printed or handed out; nothing moved
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(ROOT, "_build", "src")

STUBS = {
    "about":               ("moved",  "the-house.html"),
    "about-us":            ("moved",  "the-house.html"),
    "chauffeur-services":  ("moved",  "chauffeur.html"),
    "concierge-services":  ("moved",  "concierge.html"),
    "contact-us":          ("moved",  "contact.html"),
    "faq-1":               ("moved",  "faq.html"),
    "home":                ("moved",  "index.html"),
    "insights":            ("moved",  "./"),
    "privacy-policy":      ("moved",  "privacy.html"),
    "travel-services":     ("moved",  "journey.html"),
    "amsterdam-chauffeur": ("vanity", "chauffeur.html"),
    "roadshow":            ("vanity", "chauffeur.html"),
    "schiphol-chauffeur":  ("vanity", "chauffeur.html"),
    "wedding-car":         ("vanity", "fleet.html"),
}


def main():
    manifest, templates = {}, {}
    for slug, (kind, target) in STUBS.items():
        s = open(os.path.join(ROOT, slug + ".html"), encoding="utf-8").read()
        canon = re.search(r'rel="canonical" href="([^"]+)"', s).group(1)
        label = re.search(r'<body>.*?<a href="[^"]*">([^<]*)</a>', s, re.S).group(1)
        manifest[slug] = {"kind": kind, "target": target,
                          "canonical": canon, "label": label}
        if kind not in templates:
            # Replace the longest strings first so shorter ones cannot pre-empt them.
            t = s.replace(canon, "{{CANONICAL}}").replace(label, "{{LABEL}}")
            t = t.replace('"%s"' % target, '"{{TARGET}}"')
            t = t.replace("url=%s\"" % target, "url={{TARGET}}\"")
            templates[kind] = t

    for kind, t in templates.items():
        with open(os.path.join(SRC, "stub-%s.html" % kind), "w", encoding="utf-8") as fh:
            fh.write(t)
    with open(os.path.join(SRC, "stubs.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print("extracted %d stubs, %d template(s): %s"
          % (len(STUBS), len(templates), ", ".join(sorted(templates))))


if __name__ == "__main__":
    main()
