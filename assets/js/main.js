/* Canvas Systems — shared front-end behaviour (loaded by every page) */
(function () {
  'use strict';

  // --- Mobile menu -----------------------------------------------------
  var navToggle = document.getElementById('navToggle');
  var navLinks = document.getElementById('navLinks');

  if (navToggle && navLinks) {
    navToggle.addEventListener('click', function () {
      var isOpen = navLinks.classList.toggle('open');
      navToggle.setAttribute('aria-expanded', String(isOpen));
    });
    navLinks.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        navLinks.classList.remove('open');
        navToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // --- Dropdowns: hover on desktop, tap to expand on mobile ------------
  var MOBILE = '(max-width: 820px)';
  document.querySelectorAll('.nav-item > button').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      if (!window.matchMedia(MOBILE).matches) return;
      e.preventDefault();
      var item = btn.parentElement;
      var wasOpen = item.classList.contains('open');
      document.querySelectorAll('.nav-item.open').forEach(function (o) { o.classList.remove('open'); });
      if (!wasOpen) item.classList.add('open');
      btn.setAttribute('aria-expanded', String(!wasOpen));
    });
  });

  // Close any open dropdown when clicking elsewhere (desktop keyboard users)
  document.addEventListener('click', function (e) {
    if (e.target.closest('.nav-item')) return;
    document.querySelectorAll('.nav-item.open').forEach(function (o) {
      o.classList.remove('open');
      var b = o.querySelector('button');
      if (b) b.setAttribute('aria-expanded', 'false');
    });
  });

  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    document.querySelectorAll('.nav-item.open').forEach(function (o) { o.classList.remove('open'); });
    if (navLinks) navLinks.classList.remove('open');
  });

  // --- Scroll reveal ---------------------------------------------------
  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && reveals.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('in'); });
  }

  // --- Footer year -----------------------------------------------------
  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();

  // --- Contact form ----------------------------------------------------
  // Submissions are emailed via formsubmit.co to the address in the form's
  // action attribute (set once in build.py). One-time setup: the recipient
  // inbox must click the "Activate Form" link formsubmit emails it after
  // the first submission. If JS is unavailable the form posts natively to
  // the same endpoint and formsubmit shows its own thank-you page.
  var form = document.getElementById('contactForm');
  var success = document.getElementById('formSuccess');
  var failure = document.getElementById('formError');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var btn = form.querySelector('button[type="submit"]');
      var ajaxUrl = form.action.replace('formsubmit.co/', 'formsubmit.co/ajax/');
      if (success) success.style.display = 'none';
      if (failure) failure.style.display = 'none';
      if (btn) { btn.disabled = true; btn.textContent = 'Sending…'; }
      fetch(ajaxUrl, {
        method: 'POST',
        headers: { 'Accept': 'application/json' },
        body: new FormData(form)
      }).then(function (res) {
        if (!res.ok) throw new Error('HTTP ' + res.status);
        return res.json();
      }).then(function (data) {
        // formsubmit returns 200 even on failure; success is "true"/"false"
        if (String(data.success) !== 'true') throw new Error(data.message || 'rejected');
        if (success) success.style.display = 'block';
        form.reset();
      }).catch(function () {
        if (failure) failure.style.display = 'block';
      }).then(function () {
        if (btn) { btn.disabled = false; btn.textContent = 'Send message'; }
      });
    });
  }
})();
