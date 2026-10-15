# Build

The pages at the repository root are **generated**. Edit the sources in
`_build/src/`, run the build, commit both.

```bash
python3 _build/build.py          # write the 27 HTML files
python3 _build/gen_sitemap.py    # refresh sitemap.xml
python3 _build/build.py --check  # prove nothing drifted
```

## Why this exists

The 13 pages were 93% identical markup — roughly 11 KB of head, nav, schema and
footer repeated in each one. Changing the navigation meant editing it 13 times
and hoping. That is survivable for one language. It is not survivable for two,
which is what a Dutch version would mean: 26 pages that have to stay in step
through every future redesign.

## What is a source and what is generated

| Path | |
|---|---|
| `src/layout.html` | the shell every page shares |
| `src/schema-shared.jsonld` | the `LocalBusiness` and `Person` nodes, byte-identical on all 13 pages |
| `src/pages/<slug>.main.html` | that page's `<main>` block — the actual content |
| `src/pages/<slug>.json` | title, description, canonical, nav state, sitemap priority |
| `src/pages/<slug>.schema.jsonld` | that page's own schema nodes (breadcrumb, Service, FAQ…) |
| `src/stub-moved.html` | template for an address the old Squarespace site used |
| `src/stub-vanity.html` | template for a short address meant to be printed or handed out |
| `src/stubs.json` | which stub is which kind, and where each one points |
| **root `*.html`** | **generated — do not edit, the next build overwrites it** |

## The check is the point

`build.py --check` rebuilds everything in memory and compares it byte for byte
against what is on disk. It was written before any change was made, and it
proved the generator reproduced all 27 files exactly as they were hand-written.

Run it before every commit. If it reports a difference you did not intend,
someone edited a generated file directly and that edit is about to be lost.

`gen_sitemap.py --check` does the same for `sitemap.xml`.

## Adding a page

1. Create `src/pages/<slug>.main.html`, `.json` and `.schema.jsonld`.
2. Add the slug to `ORDER` in `build.py` and in `gen_sitemap.py`.
3. Build, check, commit.

## Where lastmod comes from

`gen_sitemap.py` reads the last commit that touched a page's **source** files.
Generated HTML changes on every build; the source changes only when the content
does. Before the sitemap was generated it had read `2026-09-11` for 32 days
while the site was actively being edited.
