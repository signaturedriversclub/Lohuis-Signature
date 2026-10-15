#!/usr/bin/env python3
"""One-time decomposition of the hand-written pages into _build/src/.

Reads the 13 canonical pages at the repository root and splits each into the
parts that differ (title, description, <main>, page-specific schema nodes) and
the shell they all share. Run once; after that build.py is the only script that
touches the root HTML.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(ROOT, "_build", "src")

# slug -> (nav section, nav child).  None means the nav shows no highlight.
PAGES = {
    "index":       (None, None),
    "commissions": ("commissions", None),
    "chauffeur":   ("commissions", "chauffeur"),
    "concierge":   ("commissions", "concierge"),
    "journey":     ("commissions", "journey"),
    "retainer":    ("commissions", "retainer"),
    "fleet":       ("fleet", None),
    "the-house":   ("the-house", None),
    "contact":     (None, None),
    "enquire":     (None, None),
    "faq":         (None, None),
    "privacy":     (None, None),
    "terms":       (None, None),
}
SECTIONS = ["commissions", "fleet", "the-house"]
CHILDREN = ["chauffeur", "concierge", "journey", "retainer"]
LDJSON_OPEN = '<script type="application/ld+json">'


def read(slug):
    with open(os.path.join(ROOT, slug + ".html"), encoding="utf-8") as fh:
        return fh.read()


def between(s, a, b, keep=False):
    i = s.find(a)
    j = s.find(b, i + len(a))
    if i < 0 or j < 0:
        raise SystemExit("marker not found: %r / %r" % (a, b))
    return s[i:j + len(b)] if keep else s[i + len(a):j]


def split_graph(raw):
    """Split the @graph array into its top-level nodes, preserving bytes."""
    lines = raw.split("\n")
    start = next(i for i, l in enumerate(lines) if l.strip() == '"@graph": [')
    end   = next(i for i in range(len(lines) - 1, -1, -1) if lines[i] == "  ]")
    head  = "\n".join(lines[:start + 1])
    tail  = "\n".join(lines[end:])
    nodes, cur, depth = [], [], 0
    for l in lines[start + 1:end]:
        cur.append(l)
        depth += l.count("{") - l.count("}")
        if depth == 0 and cur:
            node = "\n".join(cur)
            nodes.append(node[:-1] if node.endswith(",") else node)
            cur = []
    return head, nodes, tail


def main():
    os.makedirs(os.path.join(SRC, "pages"), exist_ok=True)
    shared_nodes = None
    layout_written = False

    for slug, (section, child) in PAGES.items():
        s = read(slug)
        head, nodes, tail = split_graph(between(s, LDJSON_OPEN, "</script>"))

        # LocalBusiness + Person are byte-identical on every page -> hoist once.
        if shared_nodes is None:
            shared_nodes = nodes[:2]
            with open(os.path.join(SRC, "schema-shared.jsonld"), "w", encoding="utf-8") as fh:
                fh.write(",\n".join(shared_nodes))
        elif nodes[:2] != shared_nodes:
            raise SystemExit("%s: shared schema nodes differ from the rest" % slug)

        title = between(s, "<title>", "</title>")
        desc  = re.search(r'<meta name="description" content="([^"]*)"', s).group(1)
        canon = re.search(r'<link rel="canonical" href="([^"]*)"', s).group(1)

        with open(os.path.join(SRC, "pages", slug + ".main.html"), "w", encoding="utf-8") as fh:
            fh.write(between(s, '<main id="main">', "</main>", keep=True))
        with open(os.path.join(SRC, "pages", slug + ".schema.jsonld"), "w", encoding="utf-8") as fh:
            fh.write(",\n".join(nodes[2:]))
        with open(os.path.join(SRC, "pages", slug + ".json"), "w", encoding="utf-8") as fh:
            json.dump({"title": title, "description": desc, "canonical": canon,
                       "section": section, "child": child},
                      fh, indent=2, ensure_ascii=False)
            fh.write("\n")

        if not layout_written:
            layout = s
            # Order matters: replace the longest / most specific strings first.
            layout = layout.replace(between(s, LDJSON_OPEN, "</script>"),
                                    head + "\n{{SCHEMA}}\n" + tail)
            layout = layout.replace(between(s, '<main id="main">', "</main>", keep=True),
                                    "{{MAIN}}")
            layout = layout.replace("<title>%s</title>" % title, "<title>{{TITLE}}</title>")
            layout = layout.replace('content="%s"' % desc, 'content="{{DESCRIPTION}}"')
            layout = layout.replace('content="%s"' % title, 'content="{{TITLE}}"')
            layout = layout.replace('href="%s"' % canon, 'href="{{CANONICAL}}"')
            layout = layout.replace('content="%s"' % canon, 'content="{{CANONICAL}}"')
            # Nav state becomes tokens so build.py can set it per page.
            for name in SECTIONS:
                layout = re.sub(r'(<a href="%s\.html")( aria-current="page")?( class="s5">)' % re.escape(name),
                                r'\1{{AC:%s}}\3' % name, layout)
                layout = layout.replace('%s<span class="s92">' % _label(name),
                                        '%s<span class="{{SP:%s}}">' % (_label(name), name))
                layout = layout.replace('%s<span class="s6">' % _label(name),
                                        '%s<span class="{{SP:%s}}">' % (_label(name), name))
            for name in CHILDREN:
                layout = re.sub(r'(<a href="%s\.html")( aria-current="page")?(>)' % re.escape(name),
                                r'\1{{AC:%s}}\3' % name, layout)
            with open(os.path.join(SRC, "layout.html"), "w", encoding="utf-8") as fh:
                fh.write(layout)
            layout_written = True

    print("extracted %d pages into %s" % (len(PAGES), os.path.relpath(SRC, ROOT)))


def _label(section):
    return {"commissions": "Commissions", "fleet": "Fleet", "the-house": "The House"}[section]


if __name__ == "__main__":
    main()
