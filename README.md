# Lohuis Signature — website

The Lohuis Signature website: plain HTML, CSS and JavaScript, with no build step.
Every file in this repository is served to the visitor exactly as it is stored here.

---

## What is where

```
index.html          The homepage
commissions.html    The four commissions, listed
chauffeur.html      Commission I
concierge.html      Commission II
journey.html        Commission III
retainer.html       Commission IV
fleet.html          The fleet
the-house.html      About the house
contact.html        "Request contact" — the ways to reach you
enquire.html        The enquiry form
faq.html            Questions
privacy.html        Privacy
terms.html          Terms
404.html            Shown when someone follows a broken link

css/site.css        All styling
js/site.js          All behaviour (animation, galleries, the form)
fonts/              The two typefaces, served from here rather than Google
images/             Photographs
images/r/           Resized copies of those photographs — see below
images/brand/       Logo, the signature artwork, favicons
images/clients/     Client logos
.nojekyll           Tells GitHub Pages to publish every file untouched
robots.txt          Lets search engines in, and points them at the sitemap
sitemap.xml         The list of pages, for search engines
```

Alongside these sit a number of one-line **forwarding stubs**, which hold no
content of their own and send the visitor to a real page:

```
home.html                 →  index.html          the old site's homepage address
about.html                →  the-house.html
about-us.html             →  the-house.html
chauffeur-services.html   →  chauffeur.html
concierge-services.html   →  concierge.html
travel-services.html      →  journey.html
contact-us.html           →  contact.html
faq-1.html                →  faq.html
privacy-policy.html       →  privacy.html
insights.html             →  index.html

schiphol-chauffeur.html   →  chauffeur.html      short addresses to hand out
amsterdam-chauffeur.html  →  chauffeur.html
roadshow.html             →  chauffeur.html
wedding-car.html          →  fleet.html
```

The first group exists because the old Squarespace site used those addresses and
search engines still hold them. The second group is new: clean addresses for
print, advertising or the telephone.

Each stub carries a `canonical` tag pointing at its destination, which is what
stops it competing with the real page — **and also what stops it ranking on its
own.** They are a convenience, not a source of search traffic. Ranking for
*schiphol chauffeur* or *wedding car* needs real pages with real content on them.

GitHub Pages serves these without the extension too, so `/schiphol-chauffeur`
works as well as `/schiphol-chauffeur.html`.

Every page carries its own address (`https://www.lohuissignature.nl/…`) in a
`canonical` tag, so search engines know which domain is the real one. If the
primary domain ever changes, those tags, `robots.txt` and `sitemap.xml` are the
three places to update.

---

## Publishing it

The site is designed to be served straight from the `main` branch:

1. On GitHub, open **Settings → Pages**.
2. Under *Build and deployment*, set **Source** to *Deploy from a branch*.
3. Choose branch **main** and folder **/ (root)**, then **Save**.

Within a minute or two the site appears at
`https://<your-username>.github.io/Lohuis-Signature/`.

Every link, image and stylesheet uses a **relative path**, so the site works
unchanged at that temporary address and later at your own domain. Nothing needs
editing when the domain is connected.

### The domains

This is now live and correctly arranged. `CNAME` holds `www.lohuissignature.nl`,
and the bare `lohuissignature.nl` issues a 301 to the `www` form at the
registrar, which is exactly right: one address serves the site, the other points
at it, and every page's `canonical` tag agrees with both.

**`lohuissignature.com` does not resolve at all.** Anyone typing it gets nothing.
Either point it at the `.nl` with a 301 at the registrar, or stop giving it out —
but a domain that silently fails is the worst of the three options.

**GitHub Pages accepts only one custom domain**, so any second domain has to
redirect from the registrar rather than from here. This matters beyond tidiness:
if two domains serve the same pages directly, search engines see two copies of
every page and split the site's standing between them.

---

## Making changes

**Text and images** live in the `.html` files. Open one in any text editor,
change the words between the tags, and save.

**Colours and fonts** are set once at the top of `css/site.css`, under
`:root`. Changing `--accent` there, for example, changes every bronze detail on
every page.

Two things worth knowing:

- **The header and footer are repeated in every page file.** That is deliberate —
  it is what keeps the site free of any build step. But it does mean that
  changing a navigation link means changing it in all fourteen files — and on
  phones the same links are used by the menu, so there is nothing separate to
  keep in step.
- **`css/site.css` has two halves.** The top half is written by hand and is
  commented. The bottom half (`.s1`, `.s2`, …) was generated from the original
  design — one rule for each distinct style in the layout. Those are best left
  alone.

### The strip across the foot of the hero

The homepage hero ends in a row reading *Chauffeur · Concierge · Journeys ·
Retained*. It is **words, not controls** — a caption under the hero, not a
second navigation. Two changes were tried here and both were taken back out on
purpose:

- **Making them links.** Reverted. Leave them as `<div>`s, and keep anything
  that answers a pointer — a hover state, a border, a hand cursor — off them.
- **Renaming them** to *The Chauffeur, The Concierge, The Journey, The
  Retainer*, to match the commission pages. Reverted: four short labels sit
  better in the grid than the same article repeated four times. Worth knowing
  that this row is therefore the one place on the site using *Journeys* and
  *Retained*; every other surface — navigation, cards, footer, structured data
  — uses the long singular names. That is a deliberate difference of register,
  not a mistake to tidy up.

**Also known, and accepted:** the strip sits where the hero's 96deg scrim has
faded to .2, over bright paving. Measured there, the ink at .72 opacity reads
**1.86:1**, and **1.24:1** against a specular highlight in the stones, against
the 4.5:1 type this size would normally want — the right-hand end of the row
does disappear on a bright screen. A backing band at .55 with full-strength ink
was tried and removed; the row reads quieter without it.

If it is ever revisited, the option that changes nothing about the row itself is
to carry the hero's own scrim (`.s10`) further right and let the photograph
absorb the difference.

### The wordmark's minimum size

`.s3` sizes the header lockup. It was `clamp(88px, 12vw, 168px)`; the floor is
now **130px**, set in the last block of `css/site.css`.

At 88px — every viewport under 733px, so every telephone — the "SIGNATURE" line
beneath the script has a cap height of about three pixels and renders as grey
mush. On a standard-density screen the "I" disappears. Rendered from the source
mask at the sizes the header actually uses:

```
 88px   illegible; letters merged, the I gone
110px   borderline; readable, letters beginning to run together
130px   legible; every letter distinct          <- the floor
168px   clean
```

**Drawing the mark as SVG would not fix this.** It is worth doing for other
reasons — crisp edges at every size, and it would retire about 140KB of PNG
mask — but three-pixel letterforms with sub-pixel strokes are unreadable
however they are drawn. This was a sizing problem, not a format one.

The cost is the header's spare room: see the note under *The menu on phones and
tablets* for the current figure at 901px.

### The type scale

The last block in `css/site.css` is **TYPE SCALE — the functional end**. It is
worth knowing why it exists and how to work with it.

The display end of this site was always confident — headlines run to 116px. The
functional end was not. Before that block:

| | was | now |
|---|---|---|
| Footer column headings | 9px | 10.5px |
| Eyebrows, and every form label | 9.5px | 10.5px / **12px** |
| "Read the commission", Privacy headings | 10px | 11.5px |
| **Every button**, the navigation, the tap bar | 10.5px | **12px** (nav 11.5px) |
| Placeholders | browser default, 3.95:1 | `--muted`, **5.70:1** |

So the type a visitor had to read *in order to act* was the smallest type on
the page, uppercase and letterspaced at .28em. For a register of boards,
delegations and private clients — a good share of them reading on a telephone —
that was the wrong way round.

**How the block is built.** It sits at the very end of the file and overrides
by *source order*, not by specificity: every selector in it is a bare class,
exactly as in the generated half. That means two things. Deleting the block
restores the original scale exactly, and nothing in the generated `.sNN` rules
had to be touched.

**Two things to watch.**

- **The navigation is held back on purpose.** At 901px — the narrowest width
  that still shows the bar rather than the menu button — there were 113px
  between the logo and the first item. 11.5px spends 40 of them and leaves 73.
  Raising it further starts eating the margin the bar needs; measure before
  you do.
- **The floor is now 10.5px, and everything at that size is decorative** — the
  hero eyebrow, "Place a commission", "Founder". If you add a *link* or a
  *button* at the old sizes it will look right next to nothing else. Put it in
  this block instead.

Body copy was left alone at 15–16px. Raising it to 17px is a reasonable next
step, but it re-flows every paragraph on the site, so it wants its own pass.

### The menu on phones and tablets

Below 900px wide the five navigation items move behind a menu button in the top
right and open as a full-screen panel. Above that width the ordinary bar is
used, exactly as before. They are the *same* five items in the page either way —
the stylesheet simply presents them differently — so adding one adds it to both.

900px is where the bar runs out of room rather than a round number. It was
measured when the original design was set, with 102px of clear space left at
900px.

**Two later changes have spent most of that margin, and it is now worth
knowing the current figure before touching either.** The navigation went from
10.5px to 11.5px (see *The type scale*), and the wordmark gained a 130px floor
(see *The wordmark's minimum size*). Re-measured on the homepage at 901px, the
space between the mark and the first navigation item is now **51px**.

That still fits, and nothing overflows — but the bar is close to its limit.
Anything that widens the mark, the navigation, or the two buttons needs
re-measuring at 901px first, and if it goes negative the answer is to raise the
breakpoint rather than to shrink the type back down.

**Four media queries share that number** — the menu block, the short-screen
block for a handset held sideways, the `min-width` block that forces the panel
shut on wider screens, and the tap bar. Change one and change all four. The
other `700px` queries in the file are about banner heights at phone width and
have nothing to do with the menu; leave those alone.

Two of the five are buttons: **Call us** and **Request contact**. In the panel
they are held to a common width so they stack as a pair, which is what the
`min-width` on `.nav-call` is for — it is set wider than the longer of the two
labels, so both take it rather than only the shorter one. Rewording either
button means checking that value still clears the longer label.

### The Commissions submenu

"Commissions" carries the four commissions beneath it. One block of markup in
each of the fourteen files serves both presentations, the way the main
navigation does:

- **Above 900px** the stylesheet drops a panel from the bar on hover, and on
  keyboard focus. No JavaScript is involved, so it works with scripting off.
  The panel's `padding-top` is the bridge the pointer crosses between the link
  and the card — take it away and the panel closes in the gap.
- **Below 900px** an arrow sits at the right of "Commissions" inside the
  full-screen panel. Pressing it turns the arrow a quarter-turn clockwise and
  opens the four in place. `grid-template-rows: 0fr → 1fr` animates to the
  content's own height, so adding a fifth commission needs no number changed.

Two things to know before editing it:

- **`nav[data-ls-nav]` must not be an overflow container above 900px.** The bar
  scrolls sideways on narrow screens, and an overflow container would clip the
  panel. There is room to spare at that width, so the scrolling is turned off
  there.
- **"Commissions" no longer matches `nav > a.s5`.** It sits inside
  `.nav-group`, so the 7px optical correction described further down has a
  second selector written for it. A new rule aimed at the bar's links needs
  both.

Each commission page marks its own entry with `aria-current="page"`, which is
what lights it in the list.

**Both panels are smoked glass**, on the same terms as the tap bar at the foot
of the page: the page behind is dimmed by `brightness` in the backdrop filter
rather than covered with paint, so its shapes and warmth still come through and
the black layer stays thin.

Three numbers set how much shows through, and they are the ones to change:

```
background: rgba(12, 12, 11, .20)      how much black is painted over the page
brightness(.6)                         how far the page itself is dimmed
blur(12px) / blur(14px)                how far the page is smeared
```

`blur` is worth knowing about separately: it changes how *recognisable* the page
behind is without changing how *light* it is, so lowering it makes the panel
read as more see-through at no cost to legibility. The other two both trade
legibility for lightness.

**Where these currently stand.** Against the lightest thing a panel can cross —
the bone ground, `#F1EDE5` — the composited backdrop is about `#767570`, and:

| | contrast |
|---|---|
| Main links, `#F1EDE5` | ≈ 4.0:1 |
| Submenu links, the same ink at `.92` | ≈ 3.6:1 |

Both clear the 3:1 the accessibility guidelines ask of large text and **neither
clears the 4.5:1 asked of type this size.** Over every dark backdrop — the
heroes, the footer — they are far above it; it is only the cream sections where
they fall short. This was a deliberate choice for a lighter panel, made with the
numbers in front of us, not an oversight.

To put it back inside 4.5:1, the ceiling is roughly `rgba(12,12,11,.25)` with
`brightness(.55)`, which composites to about `#6B6B6B`. There is no setting
lighter than that which keeps pale type over a cream page compliant — the only
way to have both is to invert the panel: a pale frost with dark ink, which
reads as far lighter again and measures better on every backdrop.

The solid colours stay in place as the fallback for a browser without backdrop
filters.

### What search engines and AI assistants read

Every content page carries a block of **structured data** — a `<script
type="application/ld+json">` at the end of its `<head>`. It restates in machine
form what the page already says in prose: the name, address, telephone number,
the countries worked in, the four commissions, and who the founder is.

Two things are worth knowing before touching it.

**It must stay in the HTML.** It would be tidier to write it once and have
`js/site.js` insert it into every page. Don't. Google runs JavaScript before
reading a page, but most of the crawlers behind AI assistants do not — and they
are a large part of why the block exists at all. Written into the file, it is
read by everything.

**Do not add a star rating to it.** `aggregateRating` is only permitted for
reviews collected on this site. Copying the Google Business Profile rating into
the markup breaches Google's guidelines and can earn a manual penalty. The
profile is linked from `sameAs` instead, which is the sanctioned way.

Beyond that, the FAQ page's eleven questions are repeated as `FAQPage` data and
the fleet page's vehicles as an `ItemList`, which is what makes them quotable.
After editing either page's text, update the block to match — or the two
disagree, and the machine-readable half is the one that gets believed.

To check a change, paste the page's source into
[validator.schema.org](https://validator.schema.org/). All thirteen pages
currently report zero errors and zero warnings.

### The quote band

Two of the commission pages carry a **quote band**: a full-bleed dark section
holding a label and one line of italic display type, and nothing else.

It exists because those pages run for screens at a time on the bone ground with
nothing for the eye to rest on. Measured at 1440px, between the foot of the hero
and the foot of the page:

| | unbroken |
|---|---|
| Chauffeur | **2,546px** — near three screens |
| Retainer | 1,664px |
| Concierge | 1,166px |

The raw numbers overstate it for two of the three. The Retainer's run is a 3x3
grid of numbered tiles and the Concierge's is a four-column band — both already
give the eye structure. **Only the Chauffeur page is genuinely a wall of
prose**, which is why it is the one that needed breaking.

The Concierge has one anyway, for a different reason: the best piece of
evidence on the site — a client who telephoned from the gate an hour before
boarding — was buried in 13px type in the last of four columns. The band lifts
the punchline out and leaves the full story where it was.

Two things worth knowing:

- **It is deliberately not the homepage's commission band** (`.s47`), which is a
  photograph with a line laid over it. These pages argue rather than display,
  and a band made only of type says so. It also needs no photograph — which is
  the thing these pages do not have.
- **Every line in a band is already in the page's prose.** A pull-quote repeats
  what the body said; that is what a pull-quote is for. If you rewrite a
  paragraph, check whether the band above it still quotes something that exists.

Current lines, both lifted verbatim:

```
chauffeur.html   Commission No. I                     In the background unless you want otherwise.
concierge.html   Commission No. II - from the gate    It was arranged in thirty minutes.
```

The Retainer has no band. Its opening line — *"The same face, the same car,
week after week"* — already does that job, and a second statement so close to
the first would only compete with it.

### Photographs and their resized copies

The pages do not load the photographs in `images/` directly. Each `<img>` carries
a `srcset` listing copies at 640, 1024, 1600 and 2400 pixels wide, held in
`images/r/`, and the browser takes whichever fits the screen it is on. The
original stays as the `src`, so anything that cannot read the list still works.

This matters more than it sounds. The fleet page was sending 7.2 MB of
photographs to every visitor, phones included; it now sends about 1 MB. The
homepage went from roughly 3 MB to 275 KB.

The `sizes` attribute next to each `srcset` tells the browser how wide the image
will actually be *before* the stylesheet has loaded. Those values were measured
in a browser at 375px and 1600px wide rather than estimated — if you change a
layout enough to alter an image's width, the matching `sizes` value needs
revisiting or the browser will choose badly.

**After adding a photograph**, regenerate the copies:

```bash
mkdir -p images/r
for w in 640 1024 1600 2400; do
  cwebp -q 76 -m 6 -resize $w 0 images/YOUR-IMAGE.jpg -o images/r/YOUR-IMAGE-$w.webp
done
cwebp -q 76 -m 6 images/YOUR-IMAGE.jpg -o images/r/YOUR-IMAGE-full.webp
```

Skip any width larger than the original — enlarging a photograph only makes the
file bigger. `cwebp` comes from `brew install webp`.

### Previewing before you publish

From this folder, run:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000` in a browser. Press `Ctrl+C` to stop.

---

## The enquiry form

The form on `enquire.html` posts to **Web3Forms**, so enquiries arrive in your
inbox and every visitor can send one — no email program required.

It is one form serving two requests. The "Reply by" toggle at the top decides
which, and the footer buttons across the site open it with the choice already
made:

| Link | Opens | Reply by |
|---|---|---|
| Request a call | `enquire.html#call` | Telephone |
| Request an email | `enquire.html#email` | Email |

**Fields:** first name, surname (both required), telephone, email, dates, party,
the commission. A call request requires a telephone number and an email request
requires an email address — asking to be reached with no way of reaching you
helps nobody.

Every message carries a **Preferred reply** line saying Telephone or Email, and
the subject follows the choice too.

### The form service and the privacy page

The form backend is **Web3Forms**, operated by Web3Creative from **India**. What
that means, and what the privacy page now discloses:

- Transfers leave the EEA; the Standard Contractual Clauses cover them.
- Retention is set to **thirty days** in the Web3Forms dashboard, and the
  privacy page says thirty days. See the caution below.
- Each submission's IP address and email also reach **CleanTalk** and
  **Akismet** (both US) for spam filtering.
- Their session-replay sub-processor never sees your visitors — your pages load
  no script of theirs; the form posts straight to their API.

Their DPA is at web3forms.com/dpa. It binds on use, but accept it in the
dashboard so there is a dated record. You are the controller, they are the
processor.

**Worth confirming.** Their DPA says submission data has "a physical
time-to-live of three years, with dashboard visibility governed by the
Customer's plan". That wording suggests the setting you control may govern how
long a submission stays *visible* rather than when it is actually deleted. Ask
them which the thirty-day setting does. If it only hides the submission, the
privacy page understates the retention and should say something closer to
"thirty days, and cleared from its systems within three years".

### Keys

The Web3Forms access key lives in two places, both of which must match:

- `enquire.html` — the hidden `access_key` field (used if JavaScript is off)
- `js/site.js` — the `WEB3FORMS_KEY` block near the enquiry-form section

`WEB3FORMS_KEY` holds one key per half of the toggle, so call requests and
email requests arrive in separate Web3Forms forms:

```
call   cebafb4f-452f-4a71-8c5c-46de4f214be3
email  20dbeb2d-caf2-45eb-bb36-7bbf2d556fdd
```

The hidden field in `enquire.html` starts on the call key and the script swaps
it when the toggle changes. With JavaScript switched off the toggle cannot
move, so the form stays on "Request a call" and posts the call key — which is
the honest outcome rather than a mismatch.

### If it fails

The visitor sees "That did not send. Please telephone…" with your number, and
nothing they typed is lost. A hidden field catches bots; a real person never
sees it.

---

## Details to confirm

- The footer reads **© 2026 Lohuis Signature**.

### Content Credentials in eight image files — outstanding

Eight files carry an embedded **C2PA manifest** naming Claude in their
provenance chain. All eight are published: five are photographs the pages
reference, and three are the brand artwork the stylesheet loads on every page.

```
images/brand/sig-mask.png              the wordmark, drawn in the header and footer
images/brand/sig-script-mask.png       the script, drawn on every hero
images/brand/logo-source.png           cited as the organisation logo in the structured data
images/charlie-detailing.webp          the-house.html
images/fleet-eclass-interior.avif      fleet.html
images/fleet-luggage.avif              fleet.html
images/fleet-minicoach-exterior.webp   fleet.html
images/fleet-sprinter-interior.webp    fleet.html
```

**Be precise about what they say.** The assertion is
*"Claude provided this file at the request of a user and may have created or
modified the file contents"*, with `origin-confidence: unknown` and an action of
`c2pa.opened` plus `com.anthropic.claude.provided`. That is a **handled-by**
record, not a generated-by one — there is no `trainedAlgorithmicMedia` claim in
any of them. It is what gets written when a file passes through an assistant,
most likely during an earlier conversion.

**Why it is worth clearing anyway.** The manifest is publicly inspectable by
anyone with a Content Credentials tool, and three of the eight are the logo.
On a site that keeps a written rights record for every photograph, a
machine-readable note saying an AI touched the wordmark is an odd thing to
leave in.

**It is not a weight problem.** Measured on `charlie-detailing.webp`, the
manifest costs a few kilobytes; re-encoding at a quality that preserved the
image actually produced a slightly *larger* file. This is about the record.

**The fix** is a re-encode, which drops the metadata — `cwebp` and `sips` both
write nothing of their own. Decode to PNG, encode back at high quality, check
with `grep -la c2pa <file>`. The resized copies in `images/r/` are already
clean, because they were generated rather than passed through; it is only the
originals in `images/` and `images/brand/` that carry it.

Note that `images/brand/*.png` are masks, not photographs — they must stay PNG
with their alpha channel intact, so re-encode them with a PNG tool rather than
`cwebp`.

One more, unused and so not urgent: `images/Concierge pointing.jpg` carries the
same manifest. It is the butler stock photograph, not referenced by any page.

### The telephone number, off this site

The site uses **+31 297 223 448** — in the footer, the new header link, the tap
bar on phones, the enquiry form's failure message and the structured data. All
fourteen pages agree.

Everything Google still publishes shows **+31 (0) 297 233 488**, the retired
number from the old site. That is Google's index being stale, and it will clear
as the new pages are recrawled — but the **Google Business Profile is a separate
thing and will not fix itself.** Check which number it carries; if it is the old
one, it is misdirecting callers from the most visible surface the house owns, and
the mismatch against this site also weakens local ranking, which rewards the same
name, address and telephone number appearing identically everywhere.

### Image rights

All confirmed and on record:

- `images/home-concierge.jpg` — Shutterstock, ID **2300154693**, Jeremy Walter.
  Licence held. Keep the licence receipt somewhere you can find it; stock
  libraries audit, and the file itself no longer carries the proof.
- `images/spirit-of-ecstasy.webp` — used with the photographer's agreement.
- `images/chauffeur-hero.webp` — the Rolls-Royce Ghost under the magnolia, used
  as the Chauffeur banner. Photographed by **Carphotographs Overdiep**. Used
  with the photographer's agreement, and with their agreement that the
  watermark along the foot of the frame be cropped away — which is what the
  2,845px height is: the original is 2,925px and the mark sat in the last
  eighty. Keep a note of that conversation; the file no longer evidences it.
  The camera original is `images/IMG_1607.jpeg`, which is git-ignored.
- The six client logos on The House — shown with the clients' permission. The
  FAQ says discretion holds "unless a client has specifically agreed
  otherwise", which is what those logos rely on.

**Two entries are not confirmed and need to be.**

- `images/journey-strasbourg.webp` — Château de Pourtalès, used on the Journey
  page for *Amsterdam to Rome*. It replaced a photograph of our own, and its
  provenance has not been established. It was not taken by the house. Framing,
  light and dimensions are consistent with a freely-licensed encyclopedia
  photograph, which would carry an attribution condition, and it may instead be
  the property's own press image, which would need their permission.

  Pourtalès is a client and is on the logo wall, so this is a short
  conversation rather than a problem — but until someone has had it, the entry
  stays here rather than in the list above. The better answer is to photograph
  our own car on that gravel and retire the question entirely.

- `images/concierge-hero.webp` — a card passed across a counter, used as the
  Concierge banner and as the social preview for the Concierge, Contact and
  Enquire pages. A stock photograph, supplied without a library, an ID or a
  photographer. `home-concierge.jpg` two entries above shows the standard: the
  library, the image number and the photographer's name, so the licence can be
  produced if anyone asks. This one needs the same before it is safe.

  **It is also only 600x400.** The banner runs full-bleed, so on a 1440px screen
  it is scaled up about two and a half times, and about five on a high-density
  screen. It survives because the photograph is shallow-focus almost everywhere
  and the softness reads as depth of field rather than as a small file — but it
  is a compromise, and the licensed full-resolution original should replace it.

  The better answer remains a photograph of our own: one of our written
  proposals on our own letterhead, on a dark table, in raking window light. It
  needs no licence and no entry here at all.

Camera, editing and copyright data has been stripped from every photograph.
That removes serial numbers and location traces that have no business on a
public site, and trims the download — but it also means the files themselves no
longer evidence where they came from. The list above is now the record.

Two things are settled and correct as they stand: the contact address
**info@lohuissignature.nl** matches this site's own domain, and the seventeen
**Signature Drivers Club** links point to `signaturedriversclub.nl`, which is
the sibling house and a genuinely separate site.
