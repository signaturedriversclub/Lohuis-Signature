/* ==========================================================================
   Lohuis Signature — site behaviour

   Plain JavaScript, no libraries. Everything here is decoration or
   convenience: the site reads and works perfectly with this file removed.
   ========================================================================== */
(function () {
  'use strict';

  var reduced = window.matchMedia &&
                window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* --- Header ------------------------------------------------------------ */
  /* Goes solid once the hero has scrolled away. */
  var header = document.querySelector('.page > header');
  if (header) {
    var solid = null;
    var syncHeader = function () {
      var on = window.scrollY > 48;
      if (on !== solid) {
        solid = on;
        header.classList.toggle('is-solid', on);
      }
    };
    window.addEventListener('scroll', syncHeader, { passive: true });
    syncHeader();
  }

  /* --- Mobile menu -------------------------------------------------------- */
  var toggle = document.querySelector('.nav-toggle');
  var menu = document.getElementById('site-menu');

  if (toggle && menu) {
    var root = document.documentElement;

    var isOpen = function () {
      return toggle.getAttribute('aria-expanded') === 'true';
    };

    var setMenu = function (open) {
      if (open) { root.setAttribute('data-menu-open', ''); }
      else { root.removeAttribute('data-menu-open'); }
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Menu');
    };

    toggle.addEventListener('click', function () {
      setMenu(!isOpen());
    });

    // Following a link closes the panel — it matters when the link is to the
    // page you are already on, where nothing else would close it.
    menu.addEventListener('click', function (event) {
      if (event.target.closest && event.target.closest('a')) setMenu(false);
    });

    document.addEventListener('keydown', function (event) {
      if (event.key !== 'Escape' || !isOpen()) return;
      setMenu(false);
      toggle.focus();
    });

    // Keep the keyboard inside the panel while it covers the page.
    menu.addEventListener('keydown', function (event) {
      if (event.key !== 'Tab' || !isOpen()) return;
      var stops = [toggle].concat(Array.prototype.slice.call(menu.querySelectorAll('a[href]')));
      var first = stops[0];
      var last = stops[stops.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault(); last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault(); first.focus();
      }
    });

    // The panel is a phone layout; a rotation or resize past the breakpoint
    // must not leave it stranded open.
    window.addEventListener('resize', function () {
      if (isOpen() && window.innerWidth > 700) setMenu(false);
    });
  }

  /* --- Reveal on scroll --------------------------------------------------- */
  var revealables = document.querySelectorAll('[data-rv]');

  if (reduced || !('IntersectionObserver' in window)) {
    // Show everything at once.
    for (var i = 0; i < revealables.length; i++) {
      revealables[i].setAttribute('data-rv-on', '1');
    }
  } else {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        var delay = parseFloat(el.getAttribute('data-rv-d')) || 0;
        el.style.transitionDelay = (delay * 110) + 'ms';
        el.setAttribute('data-rv-on', '1');
        observer.unobserve(el);
      });
    }, { rootMargin: '0px 0px -6% 0px' });

    for (var j = 0; j < revealables.length; j++) {
      observer.observe(revealables[j]);
    }

    // Safety net: never leave anything invisible, whatever happens.
    window.setTimeout(function () {
      var stuck = document.querySelectorAll('[data-rv]:not([data-rv-on])');
      for (var k = 0; k < stuck.length; k++) {
        stuck[k].setAttribute('data-rv-on', '1');
      }
    }, 3000);
  }

  /* --- Parallax ----------------------------------------------------------- */
  var parallax = document.querySelectorAll('[data-par]');
  if (parallax.length && !reduced) {
    var ticking = false;
    var drawParallax = function () {
      ticking = false;
      var y = window.scrollY;
      for (var i = 0; i < parallax.length; i++) {
        var el = parallax[i];
        var factor = parseFloat(el.getAttribute('data-par')) || 0;
        var top = el.getBoundingClientRect().top + y;
        el.style.transform = 'translate3d(0,' + ((y - top) * factor).toFixed(1) + 'px,0)';
      }
    };
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; window.requestAnimationFrame(drawParallax); }
    }, { passive: true });
    drawParallax();
  }

  /* --- Photograph galleries ----------------------------------------------- */
  var galleries = document.querySelectorAll('[data-gal]');

  Array.prototype.forEach.call(galleries, function (gallery, galleryIndex) {
    var images = Array.prototype.filter.call(gallery.children, function (node) {
      return node.tagName === 'IMG';
    });
    if (images.length < 2) return;

    var scrim = document.createElement('div');
    scrim.className = 'gal-scrim';
    gallery.appendChild(scrim);

    var nav = document.createElement('div');
    nav.className = 'gal-nav';
    nav.setAttribute('role', 'tablist');
    nav.setAttribute('aria-label', 'Photographs');

    var current = 0;
    var tabs = [];

    var show = function (next) {
      if (next === current) return;
      images[current].style.opacity = '0';
      images[next].style.opacity = '1';
      tabs[current].setAttribute('aria-selected', 'false');
      tabs[current].setAttribute('tabindex', '-1');
      tabs[next].setAttribute('aria-selected', 'true');
      tabs[next].setAttribute('tabindex', '0');
      current = next;
    };

    images.forEach(function (image, index) {
      image.style.opacity = index === 0 ? '1' : '0';

      var tab = document.createElement('button');
      tab.type = 'button';
      tab.setAttribute('role', 'tab');
      tab.setAttribute('aria-label', 'Photograph ' + (index + 1) + ' of ' + images.length);
      tab.setAttribute('aria-selected', index === 0 ? 'true' : 'false');
      tab.setAttribute('tabindex', index === 0 ? '0' : '-1');
      tab.appendChild(document.createElement('span'));

      tab.addEventListener('click', function (event) {
        event.preventDefault();
        event.stopPropagation();
        show(index);
      });

      // Left/right arrows move between photographs, as a tablist should.
      tab.addEventListener('keydown', function (event) {
        var next = null;
        if (event.key === 'ArrowRight') next = (index + 1) % images.length;
        if (event.key === 'ArrowLeft')  next = (index - 1 + images.length) % images.length;
        if (next === null) return;
        event.preventDefault();
        show(next);
        tabs[next].focus();
      });

      tabs.push(tab);
      nav.appendChild(tab);
    });

    gallery.appendChild(nav);
  });

  /* --- Enquiry form ------------------------------------------------------- */
  var form = document.querySelector('[data-enquiry-form]');
  if (form) {
    /* Each half of the "Reply by" toggle posts to its own Web3Forms form, so
       call requests and email requests arrive separately. The matching key is
       written into the form's hidden access_key field whenever the toggle
       changes — see setMode below. */
    var WEB3FORMS_KEY = {
      call:  'cebafb4f-452f-4a71-8c5c-46de4f214be3',
      email: '20dbeb2d-caf2-45eb-bb36-7bbf2d556fdd'
    };

    var COPY = {
      call: {
        title: 'Request a call',
        intro: 'Leave a number and a time that suits. You will be called by the ' +
               'person who would handle the commission.'
      },
      email: {
        title: 'Request an email',
        intro: 'Tell us what you need in writing. You will have a considered ' +
               'reply, not an automated one.'
      }
    };

    var mode = 'call';
    var titleEl = document.querySelector('[data-form-title]');
    var introEl = document.querySelector('[data-form-intro]');
    var toggles = document.querySelectorAll('[data-mode]');

    var setMode = function (next) {
      if (!COPY[next]) return;
      mode = next;
      if (titleEl) titleEl.textContent = COPY[next].title;
      if (introEl) introEl.textContent = COPY[next].intro;
      for (var i = 0; i < toggles.length; i++) {
        var isOn = toggles[i].getAttribute('data-mode') === next;
        toggles[i].setAttribute('aria-pressed', isOn ? 'true' : 'false');
      }
      document.title = COPY[next].title + ' — Lohuis Signature';

      // Keep the posted fields in step, so a submission without JavaScript
      // still carries the right key and subject.
      var keyField = form.elements['access_key'];
      var subjField = form.elements['subject'];
      if (keyField) keyField.value = WEB3FORMS_KEY[next];
      if (subjField) subjField.value = COPY[next].title + ' — Lohuis Signature';

      // Clear any message left from a previous attempt.
      var st = form.querySelector('[data-form-status]');
      if (st && st.getAttribute('data-state') === 'error') st.hidden = true;
    };

    for (var t = 0; t < toggles.length; t++) {
      (function (button) {
        button.addEventListener('click', function () {
          setMode(button.getAttribute('data-mode'));
        });
      })(toggles[t]);
    }

    // contact.html links here as enquire.html#email
    var applyHash = function () {
      if (window.location.hash === '#email') setMode('email');
      if (window.location.hash === '#call') setMode('call');
    };
    applyHash();
    window.addEventListener('hashchange', applyHash);

    /* --- Sending -------------------------------------------------------- */
    /* Posted to Web3Forms in the background so the visitor stays on the page
       and gets an answer in the site's own voice. If JavaScript is unavailable
       the form still submits normally to the same address — Web3Forms shows
       its own confirmation page in that case. */

    var status = form.querySelector('[data-form-status]');

    var say = function (message, ok) {
      if (!status) return;
      status.textContent = message;
      status.hidden = false;
      status.setAttribute('data-state', ok ? 'ok' : 'error');
    };

    var stop = function (fieldName, message) {
      var field = form.elements[fieldName];
      say(message, false);
      if (field) { field.focus(); }
      return true;
    };

    form.addEventListener('submit', function (event) {
      event.preventDefault();

      var value = function (name) {
        var field = form.elements[name];
        return field && field.value ? field.value.trim() : '';
      };

      if (!value('first_name')) return stop('first_name', 'A first name, please.');
      if (!value('surname'))    return stop('surname', 'A surname, please.');
      // Asking to be telephoned without a number, or written to without an
      // address, leaves us no way to answer.
      if (mode === 'call'  && !value('phone')) return stop('phone', 'A telephone number, so we can call you.');
      if (mode === 'email' && !value('email')) return stop('email', 'An email address, so we can write to you.');

      var button = form.querySelector('button[type="submit"]');
      var original = button ? button.textContent : '';
      if (button) { button.disabled = true; button.textContent = 'Sending'; }
      say('Sending your enquiry.', true);

      var data = {};
      new FormData(form).forEach(function (v, k) { data[k] = v; });
      data.subject = COPY[mode].title + ' \u2014 Lohuis Signature';
      data['Preferred reply'] = mode === 'call' ? 'Telephone' : 'Email';

      fetch(form.action, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(data)
      }).then(function (response) {
        return response.json().then(function (body) { return { ok: response.ok, body: body }; });
      }).then(function (result) {
        if (!result.ok) throw new Error(result.body && result.body.message);
        form.reset();
        setMode(mode);
        say('Thank you — your enquiry is with us. You will hear from one of two people, usually within the day.', true);
        if (button) { button.textContent = 'Sent'; }
      }).catch(function () {
        say('That did not send. Please telephone +31 297 223 448 or write to info@lohuissignature.nl.', false);
        if (button) { button.disabled = false; button.textContent = original; }
      });
    });
  }
})();
