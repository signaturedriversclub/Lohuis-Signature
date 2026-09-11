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

## The enquiry form — please read

The form on `enquire.html` does **not** send anything by itself. A static site
has no server, so when a visitor presses *Send the enquiry* their own email
program opens with the details already filled in, ready for them to send.

**This works, but not for everybody.** A visitor whose device has no email
program set up — common on phones, and for anyone using Gmail in a browser —
will press the button and see nothing happen. They will assume the enquiry was
sent. **You would never know they tried.**

Fixing it takes about ten minutes and costs nothing:

1. Create a free account at [formspree.io](https://formspree.io) and add a new
   form. It gives you an address that looks like `https://formspree.io/f/abcdwxyz`.
2. In `enquire.html`, find the line beginning `<form data-enquiry-form` and
   change it to:
   `<form action="https://formspree.io/f/abcdwxyz" method="POST"`
   (using your own address, and removing `data-enquiry-form`).
3. In `js/site.js`, delete the block that begins `form.addEventListener('submit'`
   — the form then submits normally instead.

Enquiries will arrive in your inbox, and every visitor can send one. The
WhatsApp button and the email addresses elsewhere on the site are unaffected.

---

## Details to confirm

- The footer reads **© 2026 Lohuis Signature**.

Two things are settled and correct as they stand: the contact address
**info@lohuissignature.nl** matches this site's own domain, and the seventeen
**Signature Drivers Club** links point to `signaturedriversclub.nl`, which is
the sibling house and a genuinely separate site.
