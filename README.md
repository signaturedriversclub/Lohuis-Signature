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
images/brand/       Logo, the signature artwork, favicons
images/clients/     Client logos
.nojekyll           Tells GitHub Pages to publish every file untouched
robots.txt          Lets search engines in, and points them at the sitemap
sitemap.xml         The list of pages, for search engines
```

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

### Connecting lohuissignature.nl and lohuissignature.com

Not set up yet, by request. When you are ready it is two steps: add the domain
under **Settings → Pages → Custom domain** (GitHub then creates a `CNAME` file
here), and point the DNS records at GitHub from your Squarespace account.

**GitHub Pages accepts only one custom domain.** So one of the two becomes the
real address and the other must redirect to it, which is set up at the registrar
rather than here. Pick one as the primary — usually the `.nl` for a Netherlands
business — and have the `.com` forward to it.

This matters beyond tidiness: if both domains serve the same pages directly,
search engines see two copies of every page and split the site's standing
between them.

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

### The menu on phones

Below 700px wide the four navigation links move behind a menu button in the top
right and open as a full-screen panel. Above that width the ordinary bar is
used, exactly as before. It is the *same* four links in the page either way —
the stylesheet simply presents them differently — so adding a link adds it to
both.

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
