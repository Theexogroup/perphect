/* PerPHect · preferencias de cookies.
   - "Necesarias" (seguridad del formulario y preferencias) siempre activas.
   - "Analítica y publicidad" (Hotjar, Google Analytics, Meta Pixel…) solo con consentimiento.
   Para activar una herramienta en el futuro, regístrala con:
     window.perphectConsent.onAnalytics(() => { ...cargar script... });
   Se ejecuta solo si el visitante autorizó la analítica y no envía Global Privacy Control. */
(function () {
  'use strict';
  var KEY = 'perphect_cookie_consent_v1';
  var memory = null, started = false, queue = [], lastFocus = null;

  function getChoice() {
    try {
      var v = JSON.parse(localStorage.getItem(KEY) || 'null');
      return v && v.version === 1 && typeof v.analytics === 'boolean' ? v.analytics : memory;
    } catch (_) { return memory; }
  }
  function saveChoice(analytics) {
    memory = analytics;
    try { localStorage.setItem(KEY, JSON.stringify({ version: 1, analytics: analytics, updatedAt: new Date().toISOString() })); } catch (_) {}
  }
  function gpc() { return navigator.globalPrivacyControl === true; }
  function startAnalytics() {
    if (started || gpc()) return;
    started = true;
    queue.splice(0).forEach(function (fn) { try { fn(); } catch (_) {} });
  }
  function clearOptional() {
    try {
      document.cookie.split(';').forEach(function (part) {
        var k = part.split('=')[0].trim();
        if (!/^(_ga|_gid|_gcl|_fbp|_fbc|_hj|hj)/i.test(k)) return;
        ['', '; domain=' + location.hostname, '; domain=.' + location.hostname.split('.').slice(-2).join('.')].forEach(function (d) {
          document.cookie = k + '=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/' + d + '; SameSite=Lax';
        });
      });
    } catch (_) {}
  }

  window.perphectConsent = {
    onAnalytics: function (fn) { if (started) { try { fn(); } catch (_) {} } else queue.push(fn); },
    analyticsAllowed: function () { return getChoice() === true && !gpc(); },
    open: function () { if (window.__perphectCookieDialog) window.__perphectCookieDialog(); }
  };

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text) e.textContent = text;
    return e;
  }

  function setup() {
    var choice = getChoice();
    if (choice === true) startAnalytics();

    var banner = el('aside', 'ck-banner');
    banner.setAttribute('role', 'region');
    banner.setAttribute('aria-label', 'Preferencias de cookies');
    var copy = el('div', 'ck-copy');
    copy.appendChild(el('strong', '', 'Privacidad y cookies'));
    var p = el('p', '', 'Usamos tecnologías necesarias para la seguridad del sitio y del formulario. Solo con tu autorización activaremos herramientas de analítica y publicidad para mejorar tu experiencia y medir nuestras campañas. ');
    var a = el('a', '', 'Aviso de privacidad');
    a.href = '/aviso-privacidad#cookies';
    p.appendChild(a);
    copy.appendChild(p);
    var acts = el('div', 'ck-actions');
    var reject = el('button', 'ck-btn ck-ghost', 'Rechazar opcionales');
    var conf = el('button', 'ck-btn ck-ghost', 'Configurar');
    var accept = el('button', 'ck-btn ck-primary', 'Aceptar');
    [reject, conf, accept].forEach(function (b) { b.type = 'button'; acts.appendChild(b); });
    banner.appendChild(copy);
    banner.appendChild(acts);
    document.body.appendChild(banner);

    var shade = el('div', 'ck-shade');
    shade.hidden = true;
    var panel = el('section', 'ck-panel');
    panel.setAttribute('role', 'dialog');
    panel.setAttribute('aria-modal', 'true');
    panel.setAttribute('aria-labelledby', 'ck-title');
    panel.tabIndex = -1;
    var h = el('h2', '', 'Configurar privacidad');
    h.id = 'ck-title';
    panel.appendChild(h);
    panel.appendChild(el('p', 'ck-desc', 'Elige qué tecnologías pueden utilizarse mientras visitas PerPHect. Puedes cambiar tu decisión en cualquier momento desde el pie de página.'));
    var req = el('div', 'ck-opt');
    var reqT = el('div', '');
    reqT.appendChild(el('strong', '', 'Necesarias'));
    reqT.appendChild(el('p', '', 'Seguridad del sitio, protección del formulario contra bots y guardado de estas preferencias.'));
    req.appendChild(reqT);
    req.appendChild(el('span', 'ck-always', 'Siempre activas'));
    panel.appendChild(req);
    var opt = el('label', 'ck-opt ck-switch');
    var optT = el('span', '');
    optT.appendChild(el('strong', '', 'Analítica y publicidad'));
    optT.appendChild(el('span', 'ck-desc', 'Estadísticas de navegación, mapas de calor y medición de campañas (por ejemplo, Google Analytics, Hotjar o Meta Pixel cuando estén habilitados).'));
    var box = el('input', '');
    box.type = 'checkbox';
    opt.appendChild(optT);
    opt.appendChild(box);
    panel.appendChild(opt);
    var pActs = el('div', 'ck-actions');
    var cancel = el('button', 'ck-btn ck-ghost', 'Cancelar');
    var save = el('button', 'ck-btn ck-primary', 'Guardar preferencias');
    cancel.type = save.type = 'button';
    pActs.appendChild(cancel);
    pActs.appendChild(save);
    panel.appendChild(pActs);
    shade.appendChild(panel);
    document.body.appendChild(shade);

    function hide() {
      shade.hidden = true;
      document.body.classList.remove('ck-open');
      if (lastFocus && lastFocus.isConnected) lastFocus.focus();
    }
    function show() {
      lastFocus = document.activeElement;
      box.checked = getChoice() === true;
      shade.hidden = false;
      document.body.classList.add('ck-open');
      panel.focus();
    }
    window.__perphectCookieDialog = show;
    function choose(allowed) {
      var before = getChoice();
      saveChoice(allowed);
      banner.hidden = true;
      hide();
      if (allowed) startAnalytics();
      else if (before === true || started) { clearOptional(); location.reload(); }
    }
    reject.addEventListener('click', function () { choose(false); });
    accept.addEventListener('click', function () { choose(true); });
    conf.addEventListener('click', show);
    save.addEventListener('click', function () { choose(box.checked); });
    cancel.addEventListener('click', hide);
    shade.addEventListener('click', function (e) { if (e.target === shade) hide(); });
    document.addEventListener('keydown', function (e) {
      if (shade.hidden) return;
      if (e.key === 'Escape') { e.preventDefault(); hide(); }
      if (e.key !== 'Tab') return;
      var f = panel.querySelectorAll('button, input');
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
    document.querySelectorAll('[data-cookie-settings]').forEach(function (b) {
      b.addEventListener('click', function (e) { e.preventDefault(); show(); });
    });
    banner.hidden = choice !== null;
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', setup);
  else setup();
})();
