/* Refreshome — remplace jQuery + Blocksy + Elementor + plugins de l'ancien WordPress, en reproduisant leurs comportements. */
(function () {
  'use strict';
  var d = document, body = d.body, html = d.documentElement;
  var $$ = function (s, c) { return Array.prototype.slice.call((c || d).querySelectorAll(s)); };
  var settings = function (el) { try { return JSON.parse(el.getAttribute('data-settings') || '{}'); } catch (e) { return {}; } };
  var io = function (cb, margin) {
    if (!('IntersectionObserver' in window)) return { observe: function (el) { cb(el); } };
    var o = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { o.unobserve(e.target); cb(e.target); } });
    }, { rootMargin: margin || '0px' });
    return o;
  };

  /* 1. Fonds différés Elementor (.e-con.e-parent -> .e-lazyloaded), comme Elementor */
  var lazy = io(function (el) { el.classList.add('e-lazyloaded'); }, '200px 0px 200px 0px');
  $$('.e-con.e-parent').forEach(function (el) { lazy.observe(el); });

  /* 2. Animations d'entrée Elementor (slideInUp, etc.) */
  var anim = io(function (el) {
    var s = settings(el), name = s._animation || s.animation, delay = parseInt(s._animation_delay || s.animation_delay || 0, 10);
    setTimeout(function () {
      el.classList.remove('elementor-invisible');
      el.classList.add('animated', name);
    }, delay);
  });
  $$('.elementor-invisible:not([data-anim])').forEach(function (el) {
    var s = settings(el);
    if (s._animation || s.animation) anim.observe(el); else el.classList.remove('elementor-invisible');
  });

  /* 3. En-tête collant Blocksy « shrink » */
  var interp = function (x0, x1, y0, y1, x) { x = Math.max(x0, Math.min(x1, x)); return x1 === x0 ? y1 : y0 + (y1 - y0) * (x - x0) / (x1 - x0); };
  var stickies = $$('header [data-device] [data-sticky]');
  var cache = new WeakMap();
  function measure(el) {
    if (cache.has(el)) return cache.get(el);
    var rows = $$('[data-row]', el), total = 0, info = { rows: [] };
    rows.forEach(function (row) {
      var inner = row.firstElementChild && row.firstElementChild.firstElementChild ? row.firstElementChild.firstElementChild : row.firstElementChild;
      var h = inner ? inner.getBoundingClientRect().height : row.getBoundingClientRect().height;
      var cs = getComputedStyle(row), pct = parseFloat(cs.getPropertyValue('--sticky-shrink')) || 100;
      var logo = row.querySelector('[data-id="logo"] .site-logo-container'), lmax = 50, lsh = 1;
      if (logo) {
        var ls = getComputedStyle(logo);
        lmax = parseFloat(ls.getPropertyValue('--logo-max-height')) || 50;
        lsh = parseFloat((ls.getPropertyValue('--logo-sticky-shrink') || '1').toString().replace(',', '.')) || 1;
      }
      var rh = parseFloat(cs.getPropertyValue('--height')) || row.getBoundingClientRect().height;
      total += rh;
      info.rows.push({ row: row, initial: h, sticky: row.dataset.row.indexOf('middle') > -1 ? h * pct / 100 : h, logo: logo, lmax: lmax, lsh: lsh });
    });
    info.total = total;
    cache.set(el, info);
    return info;
  }
  var lastY = null;
  function onScroll() {
    var y = window.scrollY || html.scrollTop;
    if (y === lastY) return; lastY = y;
    stickies.forEach(function (el) {
      if (!el.offsetParent && getComputedStyle(el).position !== 'fixed') return;
      var info = measure(el);
      if (!el.parentNode.style.height && info.total) el.parentNode.style.height = info.total + 'px';
      var comps = el.dataset.sticky.split(':').filter(function (c) { return c !== 'yes' && c !== 'no' && c !== 'fixed'; });
      if (y > 0) {
        if (el.dataset.sticky.indexOf('yes') === -1) {
          $$('[data-row][data-transparent-row]', el).forEach(function (r) { r.dataset.transparentRow = 'no'; });
          el.dataset.sticky = ['yes'].concat(comps).join(':');
        }
        info.rows.forEach(function (r) {
          if (r.initial !== r.sticky) r.row.style.setProperty('--shrink-height', Math.round(interp(0, Math.abs(r.initial - r.sticky), r.initial, r.sticky, y)) + 'px');
          if (r.logo && r.lsh !== 1) {
            var range = Math.abs(r.initial === r.sticky ? r.lmax - r.lmax * r.lsh : r.initial - r.sticky);
            r.logo.style.setProperty('--logo-shrink-height', interp(0, range, 1, r.lsh, y) * r.lmax + 'px');
          }
        });
      } else {
        info.rows.forEach(function (r) { r.row.removeAttribute('style'); if (r.logo) r.logo.removeAttribute('style'); });
        $$('[data-row][data-transparent-row]', el).forEach(function (r) { r.dataset.transparentRow = 'yes'; });
        el.dataset.sticky = ['fixed'].concat(comps).join(':');
      }
    });
    setTimeout(function () {
      var h = body.dataset.header || '';
      if (y > 0 && h.indexOf('shrink') === -1) body.dataset.header = h + ':shrink';
      if (y <= 0 && h.indexOf('shrink') > -1) body.dataset.header = h.replace(':shrink', '');
    }, 300);
  }
  if (stickies.length) {
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', function () { cache = new WeakMap(); lastY = null; stickies.forEach(function (el) { el.parentNode.style.height = ''; }); onScroll(); });
    onScroll();
  }

  /* 4. Sous-menu desktop Blocksy (survol) */
  $$('[data-interaction*="hover"] .menu-item-has-children').forEach(function (li) {
    var t;
    li.addEventListener('mouseenter', function () { clearTimeout(t); li.classList.add('ct-active'); var b = li.querySelector('.ct-toggle-dropdown-desktop-ghost'); if (b) b.setAttribute('aria-expanded', 'true'); });
    li.addEventListener('mouseleave', function () { t = setTimeout(function () { li.classList.remove('ct-active'); var b = li.querySelector('.ct-toggle-dropdown-desktop-ghost'); if (b) b.setAttribute('aria-expanded', 'false'); }, 50); });
    var ghost = li.querySelector('.ct-toggle-dropdown-desktop-ghost');
    if (ghost) ghost.addEventListener('click', function () { li.classList.toggle('ct-active'); ghost.setAttribute('aria-expanded', li.classList.contains('ct-active')); });
  });

  /* 5. Panneau mobile Blocksy (offcanvas) */
  var panel = d.getElementById('offcanvas');
  var triggers = $$('[data-toggle-panel="#offcanvas"]');
  function openPanel() {
    if (!panel) return;
    body.dataset.panel = 'in';
    panel.classList.add('active'); panel.removeAttribute('inert'); panel.setAttribute('aria-modal', 'true');
    triggers.forEach(function (t) { t.setAttribute('aria-expanded', 'true'); });
  }
  function closePanel() {
    if (!panel || !panel.classList.contains('active')) return;
    body.dataset.panel = 'out';
    triggers.forEach(function (t) { t.setAttribute('aria-expanded', 'false'); });
    setTimeout(function () {
      panel.classList.remove('active'); panel.setAttribute('inert', ''); panel.removeAttribute('aria-modal');
      body.removeAttribute('data-panel');
    }, 250);
  }
  triggers.forEach(function (t) { t.addEventListener('click', function (e) { e.preventDefault(); panel.classList.contains('active') ? closePanel() : openPanel(); }); });
  if (panel) {
    $$('.ct-toggle-close', panel).forEach(function (b) { b.addEventListener('click', closePanel); });
    $$('a', panel).forEach(function (a) { a.addEventListener('click', closePanel); });
    panel.addEventListener('click', function (e) { if (e.target === panel) closePanel(); });
  }
  d.addEventListener('keydown', function (e) { if (e.key === 'Escape') closePanel(); });

  /* 6. Carrousels d'images Elementor (Swiper 8, mêmes réglages qu'Elementor) */
  function initCarousels() {
    if (!window.Swiper) return;
    $$('.elementor-widget-image-carousel').forEach(function (w) {
      var s = settings(w), el = w.querySelector('.swiper');
      if (!el || el.swiper) return;
      var num = function (v, f) { var n = parseInt(v, 10); return isNaN(n) ? f : n; };
      var sp = function (k) { var v = s[k]; return v && v.size !== '' && v.size !== undefined ? num(v.size, null) : null; };
      var desk = num(s.slides_to_show, 3), laptop = num(s.slides_to_show_laptop, desk), tab = num(s.slides_to_show_tablet, laptop), mob = num(s.slides_to_show_mobile, tab);
      var gD = sp('image_spacing_custom'); gD = gD === null ? 20 : gD;
      var gL = sp('image_spacing_custom_laptop'); gL = gL === null ? gD : gL;
      var gT = sp('image_spacing_custom_tablet'); gT = gT === null ? gL : gT;
      var gM = sp('image_spacing_custom_mobile'); gM = gM === null ? gT : gM;
      var single = desk === 1;
      var opts = {
        slidesPerView: mob, spaceBetween: gM, loop: s.infinite === 'yes', speed: num(s.speed, 500),
        breakpoints: {
          768: { slidesPerView: tab, slidesPerGroup: single ? 1 : 1, spaceBetween: gT },
          1025: { slidesPerView: laptop, spaceBetween: gL },
          1367: { slidesPerView: desk, spaceBetween: gD }
        },
        handleElementorBreakpoints: true, a11y: { enabled: false }
      };
      if (s.autoplay === 'yes') opts.autoplay = { delay: num(s.autoplay_speed, 5000), disableOnInteraction: s.pause_on_interaction === 'yes' };
      if (s.navigation === 'both' || s.navigation === 'arrows') opts.navigation = { prevEl: w.querySelector('.elementor-swiper-button-prev'), nextEl: w.querySelector('.elementor-swiper-button-next') };
      if (s.navigation === 'both' || s.navigation === 'dots') opts.pagination = { el: w.querySelector('.swiper-pagination'), type: 'bullets', clickable: true };
      var sw = new window.Swiper(el, opts);
      if (s.autoplay === 'yes' && s.pause_on_hover !== 'no' && num(s.autoplay_speed, 5000) > 0) {
        el.addEventListener('mouseenter', function () { sw.autoplay.stop(); });
        el.addEventListener('mouseleave', function () { sw.autoplay.start(); });
      }
    });
  }
  if (window.Swiper) initCarousels(); else window.addEventListener('load', initCarousels);

  /* 7. Accordéon FAQ (Unlimited Elements : un seul ouvert, glissement 400 ms) */
  function slide(el, open, ms) {
    el.style.overflow = 'hidden';
    var start = open ? 0 : el.scrollHeight;
    if (open) { el.style.display = 'block'; }
    var end = open ? el.scrollHeight : 0;
    el.style.height = start + 'px';
    el.offsetHeight; // reflow
    el.style.transition = 'height ' + ms + 'ms ease';
    el.style.height = end + 'px';
    setTimeout(function () { el.style.transition = ''; el.style.height = ''; el.style.overflow = ''; if (!open) el.style.display = 'none'; }, ms);
  }
  $$('.uc_content_accordion, [id^="uc_content_accordion"]').forEach(function (acc) {
    var ms = parseInt(acc.getAttribute('data-transition-duration') || 400, 10), closeOthers = acc.getAttribute('data-closeothers') !== 'false';
    $$('.uc_ac_box', acc).forEach(function (box) {
      var content = box.querySelector(':scope > .uc_content');
      if (box.classList.contains('uc-item-active') && content) content.style.display = 'block';
      var trig = box.querySelector(':scope > .uc_trigger');
      if (!trig || !content) return;
      trig.addEventListener('click', function (e) {
        e.preventDefault();
        if (box.classList.contains('uc-item-active')) { box.classList.remove('uc-item-active'); slide(content, false, ms); return; }
        if (closeOthers) $$('.uc_ac_box.uc-item-active', acc).forEach(function (o) {
          if (o.parentNode !== box.parentNode) return;
          o.classList.remove('uc-item-active'); var c = o.querySelector(':scope > .uc_content'); if (c) slide(c, false, ms);
        });
        box.classList.add('uc-item-active'); slide(content, true, ms);
      });
    });
  });

  /* 8. Avis Google (widget Trustindex d'origine), chargé à l'approche de la section */
  var ti = d.querySelector('[data-src*="trustindex.io/loader.js"]');
  if (ti) io(function () {
    var s = d.createElement('script'); s.src = 'https://cdn.trustindex.io/loader.js?ver=1'; s.defer = true; d.body.appendChild(s);
  }, '600px 0px').observe(ti.parentNode);

  /* 9. Formulaire : prestation pré-cochée via ?service=, libellé des photos */
  var f = d.getElementById('devisForm');
  if (f) {
    var q = new URLSearchParams(location.search).get('service');
    if (q) $$('input[name="Besoin[]"]', f).forEach(function (c) { if (c.value === q) c.checked = true; });
  }
})();
