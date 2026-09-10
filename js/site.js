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

    form.addEventListener('submit', function (event) {
      event.preventDefault();

      var value = function (name) {
        var field = form.elements[name];
        return field && field.value ? field.value.trim() : '';
      };

      if (!value('name')) {
        var nameField = form.elements['name'];
        if (nameField) { nameField.focus(); nameField.reportValidity && nameField.reportValidity(); }
        return;
      }

      var isCall = mode === 'call';
      var subject = isCall
        ? 'Request a call — Lohuis Signature'
        : 'Request an email — Lohuis Signature';

      var rows = [
        ['Name', value('name')],
        ['Telephone', value('phone')],
        ['Email', value('email')],
        ['Dates', value('dates')],
        ['Party', value('party')],
        ['Preferred reply', isCall ? 'Telephone' : 'Email']
      ].filter(function (row) {
        return row[1];
      }).map(function (row) {
        return row[0] + ': ' + row[1];
      });

      var message = value('message');
      if (message) rows.push('', message);

      window.location.href = 'mailto:info@lohuissignature.nl' +
        '?subject=' + encodeURIComponent(subject) +
        '&body=' + encodeURIComponent(rows.join('\n'));
    });
  }
})();
