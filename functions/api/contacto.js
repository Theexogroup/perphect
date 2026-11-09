/*
 * PERPHECT · Redefining Business Strategy — recepción de contactos con Resend.
 * Cada solicitud requiere Turnstile válido antes de enviarse a Resend.
 * No almacenar claves aquí: RESEND_API_KEY y TURNSTILE_SECRET_KEY
 * se configuran en Cloudflare Pages → Settings → Variables and Secrets.
 */
const MAIL_FROM = 'PerPHect <notificaciones@send.theexogroup.com>';
const MAIL_TO = 'buzon1.exogroup@gmail.com';
const SUBJECT = '[WEB PERPHECT] Nuevo contacto';
const TURNSTILE_ACTION = 'perphect_contact';
const JSON_HEADERS = {
  'Content-Type': 'application/json; charset=utf-8',
  'Cache-Control': 'no-store',
  'X-Robots-Tag': 'noindex'
};

const reply = (status, body) =>
  new Response(JSON.stringify(body), { status, headers: JSON_HEADERS });

const escapeHtml = (value) =>
  String(value).replace(/[&<>"']/g, (s) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  })[s]);

const text = (value, limit) => typeof value === 'string'
  ? value.trim().slice(0, limit + 1)
  : '';

export async function onRequestPost({ request, env }) {
  const url = new URL(request.url);
  // El navegador debe solicitar este endpoint desde el mismo dominio del sitio.
  if (request.headers.get('Origin') !== url.origin) {
    return reply(403, { ok: false, error: 'Origen no autorizado.' });
  }
  if (!request.headers.get('Content-Type')?.toLowerCase().startsWith('application/json')) {
    return reply(415, { ok: false, error: 'Formato de solicitud no admitido.' });
  }
  const length = Number(request.headers.get('Content-Length') || '0');
  if (length > 12000) {
    return reply(413, { ok: false, error: 'Solicitud demasiado extensa.' });
  }

  let body;
  try {
    const raw = await request.text();
    if (raw.length > 12000) return reply(413, { ok: false, error: 'Solicitud demasiado extensa.' });
    body = JSON.parse(raw);
    if (!body || typeof body !== 'object' || Array.isArray(body)) throw new Error('Invalid JSON');
  } catch {
    return reply(400, { ok: false, error: 'Datos no válidos.' });
  }

  // Honeypot: la solicitud de bots que rellenan este campo se rechaza.
  if (body.website) return reply(400, { ok: false, error: 'Solicitud no válida.' });

  const nombre = text(body.nombre, 120);
  const whatsapp = text(body.whatsapp, 25);
  const correo = text(body.correo, 160).toLowerCase();
  const comentario = text(body.comentario || '', 1500);
  const digitos = whatsapp.replace(/\D/g, '');
  const aceptaPrivacidad = body.aceptaPrivacidad === true;
  const aceptaMarketing = body.aceptaMarketing === true;

  if (nombre.length < 2 || nombre.length > 120 ||
      digitos.length < 10 || digitos.length > 15 ||
      correo.length > 160 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(correo) ||
      comentario.length > 1500 || !aceptaPrivacidad) {
    return reply(400, { ok: false, error: 'Revisa tus datos y la aceptación del aviso de privacidad.' });
  }

  // Fallar de forma segura: no aceptar envíos sin las credenciales configuradas.
  if (!env?.RESEND_API_KEY || !env?.TURNSTILE_SECRET_KEY) {
    return reply(503, { ok: false, error: 'El formulario está en preparación. Escríbenos por WhatsApp o por correo.' });
  }
  const token = text(body.turnstileToken, 2048);
  if (!token || token.length > 2048) {
    return reply(400, { ok: false, error: 'Completa la validación de seguridad.' });
  }

  try {
    const check = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        secret: env.TURNSTILE_SECRET_KEY,
        response: token,
        remoteip: request.headers.get('CF-Connecting-IP') || undefined
      })
    });
    if (!check.ok) return reply(502, { ok: false, error: 'No se pudo verificar la solicitud.' });
    const checkResult = await check.json();
    if (!checkResult.success || checkResult.hostname !== url.hostname ||
        checkResult.action !== TURNSTILE_ACTION) {
      return reply(403, { ok: false, error: 'La validación de seguridad no fue aprobada.' });
    }
  } catch {
    return reply(502, { ok: false, error: 'No se pudo completar la validación de seguridad.' });
  }

  const fecha = new Date().toISOString();
  const html = `<!doctype html><html lang="es"><body style="font-family:Arial,sans-serif;color:#1C1D1F">
    <h2 style="color:#1C1D1F">Nuevo contacto desde la web de PerPHect</h2>
    <table cellpadding="9" cellspacing="0" style="border-collapse:collapse;max-width:650px;width:100%;text-align:left">
    <tr><th>Nombre</th><td>${escapeHtml(nombre)}</td></tr>
    <tr><th>Correo</th><td>${escapeHtml(correo)}</td></tr>
    <tr><th>WhatsApp</th><td>${escapeHtml(whatsapp)}</td></tr>
    <tr><th>Comentario</th><td style="white-space:pre-wrap">${escapeHtml(comentario || 'Sin comentario')}</td></tr>
    <tr><th>Aviso de privacidad</th><td>Aceptado para ser contactado con sus datos</td></tr>
    <tr><th>Publicidad y comunicaciones comerciales</th><td>${aceptaMarketing ? 'Autorizadas' : 'No autorizadas'}</td></tr>
    <tr><th>Fecha (UTC)</th><td>${fecha}</td></tr>
    </table>
    <p style="font-size:12px;color:#6B6B6E">Origen: WEB PERPHECT · perphect.com. No reenviar ni divulgar datos sin autorización.</p>
    </body></html>`;

  const plain = [
    'Nuevo contacto desde la web de PerPHect',
    'Nombre: ' + nombre,
    'Correo: ' + correo,
    'WhatsApp: ' + whatsapp,
    'Comentario: ' + (comentario || 'Sin comentario'),
    'Aviso de privacidad: Aceptado para ser contactado con sus datos',
    'Publicidad y comunicaciones comerciales: ' + (aceptaMarketing ? 'Autorizadas' : 'No autorizadas'),
    'Fecha (UTC): ' + fecha
  ].join('\n');

  try {
    const sent = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + env.RESEND_API_KEY,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        from: MAIL_FROM,
        to: [MAIL_TO],
        reply_to: correo,
        subject: SUBJECT,
        html,
        text: plain,
        tags: [{ name: 'origen', value: 'web_perphect' }]
      })
    });
    if (!sent.ok) {
      return reply(502, { ok: false, error: 'No se pudo registrar tu solicitud. Intenta de nuevo o escríbenos por WhatsApp.' });
    }
    const result = await sent.json();
    if (!result?.id) {
      return reply(502, { ok: false, error: 'No se pudo confirmar la recepción de tu solicitud.' });
    }
    return reply(200, { ok: true, reference: result.id });
  } catch {
    return reply(502, { ok: false, error: 'No se pudo enviar la solicitud. Intenta de nuevo o escríbenos por WhatsApp.' });
  }
}

export function onRequestGet() {
  return reply(405, { ok: false, error: 'Método no permitido.' });
}
