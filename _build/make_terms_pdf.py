#!/usr/bin/env python3
"""Render the terms as a PDF on Lohuis Signature paper.

  python3 _build/make_terms_pdf.py

Reads the same source the website is built from, so the attachment sent with a
proposal and the page a client reads can never say different things. Writes
terms-en.pdf and terms-nl.pdf into pdf/ at the repository root.

Needs WeasyPrint. It is not in the standard library, so this is the one script
here with a dependency; it lives outside build.py for that reason and is never
called by it.
"""
import html as H
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "_build", "src", "pages")
OUT = os.path.join(ROOT, "pdf")

# Kept to one line: the margin box auto-sizes, and a second line runs under the
# page counter on the right.
FOOT = {
    "en": "Lohuis Signature · Twijnderlaan 19, 1431 DD Aalsmeer · "
          "KvK 76937690 · VAT NL00460544B82",
    "nl": "Lohuis Signature · Twijnderlaan 19, 1431 DD Aalsmeer · "
          "KvK 76937690 · BTW NL00460544B82",
}


def plain(fragment):
    return H.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", fragment))).strip()


def read_terms(lang):
    """Pull the eyebrow, title, lede and every section out of the page source."""
    src = open(os.path.join(SRC, lang, "terms.main.html"), encoding="utf-8").read()
    eyebrow = plain(re.search(r'<div class="s51">(.*?)</div>', src, re.S).group(1))
    title = plain(re.search(r'<h1 class="s240">(.*?)</h1>', src, re.S).group(1))
    lede = plain(re.search(r'<p data-rv="1" class="s242">(.*?)</p>', src, re.S).group(1))
    sections = []
    for block in re.findall(r'<div data-rv="1" data-rv-d="\d+" class="s24[36]">(.*?)</div>',
                            src, re.S):
        head = plain(re.search(r"<h2[^>]*>(.*?)</h2>", block, re.S).group(1))
        paras = [plain(p) for p in re.findall(r'<p class="s245">(.*?)</p>', block, re.S)]
        sections.append((head, paras))
    return eyebrow, title, lede, sections


CSS = """
@font-face { font-family:'Montserrat'; font-weight:100 900; font-style:normal;
             src:url('FONTDIR/montserrat.woff2') format('woff2'); }
@font-face { font-family:'Bodoni Moda'; font-weight:400 900; font-style:italic;
             src:url('FONTDIR/bodoni-moda-italic.woff2') format('woff2'); }

@page {
  size: A4;
  margin: 26mm 22mm 24mm 22mm;
  background: #F2EDE4;
  @bottom-left  { content: "FOOTER"; font-family:'Montserrat'; font-size:5.6pt;
                  letter-spacing:.09em; color:#6B655B; }
  @bottom-right { content: counter(page) " / " counter(pages);
                  font-family:'Montserrat'; font-size:5.6pt;
                  letter-spacing:.14em; color:#6B655B; }
}
@page :first { margin-top: 20mm; }

body { font-family:'Montserrat'; font-weight:300; font-size:8.6pt; line-height:1.85;
       color:#403F3B; margin:0; }

.mark   { width:52mm; margin:0 0 15mm; }
.eyebrow{ font-size:6pt; letter-spacing:.3em; text-transform:uppercase;
          color:#6B655B; margin:0 0 5mm; }
h1      { font-family:'Montserrat'; font-weight:200; font-size:27pt; line-height:1.05;
          letter-spacing:-.015em; color:#141311; margin:0 0 7mm; }
.lede   { font-family:'Bodoni Moda'; font-style:italic; font-weight:400;
          font-size:12pt; line-height:1.6; color:#141311; margin:0 0 10mm;
          padding-bottom:9mm; border-bottom:.4pt solid #DCD5C8; }

section { padding:0 0 6.5mm; margin:0 0 6.5mm; border-bottom:.4pt solid #DCD5C8;
          break-inside:avoid; }
section:last-of-type { border-bottom:0; }
h2      { font-size:6.6pt; font-weight:500; letter-spacing:.26em;
          text-transform:uppercase; color:#6B655B; margin:0 0 3.5mm; }
p       { margin:0 0 2.8mm; }
p:last-child { margin-bottom:0; }
"""

PAGE = """<!doctype html><html lang="{lang}"><head><meta charset="utf-8">
<style>{css}</style></head><body>
<img class="mark" src="{mark}">
<div class="eyebrow">{eyebrow}</div>
<h1>{title}</h1>
<p class="lede">{lede}</p>
{sections}
</body></html>"""


def build(lang):
    eyebrow, title, lede, sections = read_terms(lang)
    css = (CSS.replace("FONTDIR", "file://" + os.path.join(ROOT, "fonts"))
              .replace("FOOTER", FOOT[lang].replace('"', "'")))
    body = "\n".join(
        "<section><h2>%s</h2>%s</section>"
        % (H.escape(h), "".join("<p>%s</p>" % H.escape(p) for p in ps))
        for h, ps in sections)
    return PAGE.format(lang=lang, css=css, eyebrow=H.escape(eyebrow),
                       title=H.escape(title), lede=H.escape(lede), sections=body,
                       mark="file://" + os.path.join(ROOT, "images", "brand",
                                                     "lohuis-signature-logo-ink.svg"))


def main():
    try:
        from weasyprint import HTML
    except ImportError:
        sys.exit("WeasyPrint is not installed in this interpreter.")
    os.makedirs(OUT, exist_ok=True)
    for lang in ("en", "nl"):
        doc = build(lang)
        path = os.path.join(OUT, "terms-%s.pdf" % lang)
        HTML(string=doc, base_url=ROOT).write_pdf(path)
        print("  %-18s %6.1f KB" % (os.path.relpath(path, ROOT),
                                    os.path.getsize(path) / 1024))


if __name__ == "__main__":
    main()
