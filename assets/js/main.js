/* PerPHect · scripts globales */

/* ===== Formulario =====
   Se procesa en Cloudflare Pages Functions (/api/contacto) con Resend y Turnstile.
   La Site Key de Turnstile es pública: reemplazar al crear el widget PERPHECT-FORM. */
const TURNSTILE_SITEKEY = "PENDIENTE_SITEKEY";
const TURNSTILE_ACTION = "perphect_contact";

document.addEventListener('DOMContentLoaded', () => {
  const y = document.getElementById('yr'); if (y) y.textContent = new Date().getFullYear();

  const header = document.querySelector('header');
  const burger = document.querySelector('.burger');
  const onScroll = () => header.classList.toggle('solid', scrollY > 40);
  addEventListener('scroll', onScroll, { passive: true }); onScroll();
  burger.addEventListener('click', () => {
    const o = header.classList.toggle('open');
    burger.setAttribute('aria-expanded', o);
    burger.setAttribute('aria-label', o ? 'Cerrar menú' : 'Abrir menú');
    document.body.style.overflow = o ? 'hidden' : '';
  });

  const els = document.querySelectorAll('.rv');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(es => es.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    }), { threshold: .1, rootMargin: '0px 0px -40px 0px' });
    els.forEach(el => io.observe(el));
  } else els.forEach(el => el.classList.add('in'));

  initForm();
});

function initForm() {
  const form = document.getElementById('leadForm');
  if (!form) return;
  const feedback = document.getElementById('formFeedback');
  const btn = form.querySelector('button[type=submit]');
  const btnText = btn.textContent;
  const privacy = form.querySelector('#aceptaPrivacidad');
  const marketing = form.querySelector('#aceptaMarketing');
  const rules = {
    nombre: v => v.trim().length >= 2,
    email: v => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()),
    whatsapp: v => { const d = v.replace(/\D/g, '').length; return d >= 10 && d <= 15; }
  };
  Object.keys(rules).forEach(k => form[k].addEventListener('input', () => form[k].classList.remove('err')));
  privacy.addEventListener('change', () => privacy.closest('.consent').classList.remove('err'));

  // Turnstile (invisible salvo que requiera interacción)
  let widgetId = null;
  const box = document.getElementById('perphect-turnstile');
  const renderWidget = () => {
    if (widgetId !== null || !box || typeof window.turnstile?.render !== 'function') return;
    try {
      widgetId = window.turnstile.render(box, {
        sitekey: TURNSTILE_SITEKEY, action: TURNSTILE_ACTION,
        appearance: 'interaction-only', language: 'es'
      });
    } catch (_) { /* se reintenta al enviar */ }
  };
  window.addEventListener('load', renderWidget);
  renderWidget();
  const resetWidget = () => { try { if (widgetId !== null) window.turnstile.reset(widgetId); } catch (_) {} };

  const say = (msg, bad) => { feedback.textContent = msg; feedback.classList.toggle('bad', !!bad); };

  form.addEventListener('submit', async e => {
    e.preventDefault();
    say('');
    let ok = true;
    for (const k in rules) {
      const valid = rules[k](form[k].value);
      form[k].classList.toggle('err', !valid);
      if (!valid && ok) { form[k].focus(); ok = false; }
    }
    if (!privacy.checked) {
      privacy.closest('.consent').classList.add('err');
      if (ok) privacy.focus();
      ok = false;
    }
    if (!ok) { say('Revisa los campos marcados.', true); return; }

    renderWidget();
    const token = widgetId !== null && typeof window.turnstile?.getResponse === 'function'
      ? window.turnstile.getResponse(widgetId) : '';
    if (!token) { say('Estamos verificando la seguridad del envío. Espera unos segundos e inténtalo de nuevo.', true); return; }

    const data = {
      nombre: form.nombre.value.trim(),
      correo: form.email.value.trim(),
      whatsapp: form.whatsapp.value.trim(),
      comentario: form.comentarios.value.trim(),
      aceptaPrivacidad: privacy.checked === true,
      aceptaMarketing: marketing.checked === true,
      website: form.website.value,
      turnstileToken: token
    };
    btn.disabled = true; btn.textContent = 'Enviando…';
    try {
      const r = await fetch('/api/contacto', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(data)
      });
      const res = await r.json().catch(() => ({}));
      if (!r.ok || !res.ok) throw new Error(res.error || 'No se pudo enviar tu solicitud.');
      window.location.assign('/gracias');
    } catch (err) {
      resetWidget();
      btn.disabled = false; btn.textContent = btnText;
      say((err && err.message ? err.message : 'No se pudo enviar tu solicitud.') + ' También puedes escribirnos por WhatsApp.', true);
    }
  });
}
