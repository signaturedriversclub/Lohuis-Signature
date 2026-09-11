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

### The menu on phones and tablets

Below 900px wide the five navigation items move behind a menu button in the top
right and open as a full-screen panel. Above that width the ordinary bar is
used, exactly as before. They are the *same* five items in the page either way —
the stylesheet simply presents them differently — so adding one adds it to both.

900px is where the bar runs out of room rather than a round number. Measured on
the homepage, the space left between the logo and the far edge is 13px at 768px
wide, 57px at 834px and 102px at 900px. So a tablet held upright folds the menu
away; a tablet turned on its side (1024px, with 185px to spare) keeps the full
bar. Raising the value folds the landscape tablet too.

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
- The six client logos on The House — shown with the clients' permission. The
  FAQ says discretion holds "unless a client has specifically agreed
  otherwise", which is what those logos rely on.

Camera, editing and copyright data has been stripped from every photograph.
That removes serial numbers and location traces that have no business on a
public site, and trims the download — but it also means the files themselves no
longer evidence where they came from. The list above is now the record.

Two things are settled and correct as they stand: the contact address
**info@lohuissignature.nl** matches this site's own domain, and the seventeen
**Signature Drivers Club** links point to `signaturedriversclub.nl`, which is
the sibling house and a genuinely separate site.
