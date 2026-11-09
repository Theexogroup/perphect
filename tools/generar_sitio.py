"""Genera las páginas de perphect.com con encabezado y pie comunes.
Ejecutar desde la raíz del repo:  python3 tools/generar_sitio.py
Versiona CSS/JS por hash para evitar caché vieja."""
import os, hashlib
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
DOM = 'https://perphect.com'

def _v(f): return hashlib.md5(open(ROOT + f, 'rb').read()).hexdigest()[:8]

# ---- Datos de contacto (completar) ----
WA_NUM = '525588673288'   # solo dígitos, con lada de país
WA_DISPLAY = '+52 55 8867 3288'
WA_TXT = 'Hola%20vi%20el%20sitio%20web%20de%20PerPHect%2C%20me%20gustar%C3%ADa%20conocer%20m%C3%A1s%20informaci%C3%B3n.'
WA_LINK = f'https://wa.me/{WA_NUM}?text={WA_TXT}' if WA_NUM else ''
WA_SVG = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91C21.95 6.45 17.5 2 12.04 2zm5.8 14.03c-.24.68-1.42 1.3-1.95 1.34-.5.05-.97.23-3.27-.68-2.77-1.09-4.51-3.92-4.65-4.1-.13-.18-1.11-1.48-1.11-2.82 0-1.34.7-2 .95-2.27.25-.27.54-.34.72-.34h.52c.17 0 .39-.06.61.47.24.55.79 1.9.86 2.04.07.14.11.3.02.48-.09.18-.14.3-.27.46-.14.16-.29.36-.41.48-.14.14-.28.29-.12.56.16.27.71 1.17 1.52 1.9 1.05.93 1.93 1.22 2.2 1.36.27.14.43.11.59-.07.16-.18.68-.79.86-1.06.18-.27.36-.23.61-.14.25.09 1.59.75 1.86.89.27.14.45.2.52.32.07.11.07.66-.17 1.33z"/></svg>'

CDMX = 'Juan de Acuña 318, Lomas de Chapultepec,<br>Miguel Hidalgo, CDMX, 11000'
DAL = '3441 Halifax St, Dallas,<br>Texas 75247, EE. UU.'

IG = 'https://www.instagram.com/perphect.pro'
LI = 'https://www.linkedin.com/company/perphect'
FB = 'https://www.facebook.com/Perphect.pro'
FB_SVG = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13.5 21v-7.5h2.5l.4-3h-2.9V8.6c0-.9.3-1.5 1.5-1.5h1.6V4.4c-.3 0-1.2-.1-2.3-.1-2.3 0-3.8 1.4-3.8 3.9v2.3H8v3h2.5V21h3z"/></svg>'
IG_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg>'
LI_SVG = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9.75h4V21H3zM9.5 9.75h3.83v1.54h.05c.53-1 1.84-2.06 3.79-2.06 4.05 0 4.8 2.67 4.8 6.13V21h-4v-4.98c0-1.19-.02-2.72-1.66-2.72-1.66 0-1.91 1.3-1.91 2.63V21h-4z"/></svg>'
SOCIAL = f'<div class="social"><a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram de PerPHect">{IG_SVG}</a><a href="{LI}" target="_blank" rel="noopener" aria-label="LinkedIn de PerPHect">{LI_SVG}</a><a href="{FB}" target="_blank" rel="noopener" aria-label="Facebook de PerPHect">{FB_SVG}</a></div>'

NAV = [('/#inicio', 'Inicio'), ('/#consejero', 'El Consejero'), ('/#estructura', 'Estructura'), ('/#innovacion', 'Innovación')]
FONTS = '<link rel="preload" href="/assets/fonts/luiss-sans-regular.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="/assets/fonts/luiss-serif-regular.woff2" as="font" type="font/woff2" crossorigin>'


def url(fname):
    return DOM + '/' + ('' if fname == 'index.html' else fname.replace('.html', ''))


def page(fname, title, desc, body, home=False, extra_head='', noindex=False):
    links = ''.join(f'<a href="{h}">{t}</a>' for h, t in NAV)
    cta_active = ''
    wa = f'<a class="wa" href="{WA_LINK}" target="_blank" rel="noopener" aria-label="Escríbenos por WhatsApp">{WA_SVG}<span>WhatsApp</span></a>' if WA_LINK else ''
    html = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_MX">
<meta property="og:site_name" content="PerPHect">
<meta property="og:url" content="{url(fname)}">
<meta property="og:image" content="{DOM}/assets/img/og-perphect.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="PerPHect · Redefining Business Strategy">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1C1D1F">
<link rel="canonical" href="{url(fname)}">{'<meta name="robots" content="noindex,follow">' if noindex else ''}
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<link rel="icon" type="image/png" href="/assets/favicon.png">
<link rel="apple-touch-icon" href="/assets/icono.png">
{FONTS}
<link rel="stylesheet" href="/assets/css/styles.css?v={_v('assets/css/styles.css')}">{extra_head}
</head>
<body{' class="home"' if home else ''}>
<header>
  <div class="wrap nav">
    <a class="brand" href="/" aria-label="PerPHect, inicio"><img class="dark" src="/assets/logos/perphect-color.svg" alt="PerPHect · Redefining Business Strategy" width="210" height="72"><img class="light" src="/assets/logos/perphect-blanco.svg" alt="PerPHect · Redefining Business Strategy" width="210" height="72"></a>
    <button class="burger" aria-label="Abrir menú" aria-expanded="false" aria-controls="menu"><span></span></button>
    <nav class="menu" id="menu" aria-label="Principal">{links}<a href="/#contacto" class="btn btn-line{cta_active}">Contacto</a></nav>
  </div>
</header>
<main>
{body}
</main>
<footer>
  <div class="wrap">
    <div class="fgrid">
      <div class="fl"><img class="flogo" src="/assets/logos/perphect-blanco.svg" alt="PerPHect · Redefining Business Strategy" width="220" height="75" loading="lazy">{SOCIAL}</div>
      <div><h5>Sitio</h5><ul>{''.join(f'<li><a href="{h}">{t}</a></li>' for h, t in NAV[1:])}<li><a href="/#contacto">Contacto</a></li><li><a href="{WA_LINK}" target="_blank" rel="noopener">WhatsApp {WA_DISPLAY}</a></li></ul></div>
      <div><h5>Oficinas</h5><div class="addr"><div><b>CDMX</b><p>{CDMX}</p></div><div><b>Dallas</b><p>{DAL}</p></div></div></div>
    </div>
    <div class="seal"><img src="/assets/img/sello-mx-us.png" alt="Sello binacional México y Estados Unidos" width="150" height="48" loading="lazy"></div>
    <div class="fbottom"><div><p>© <span id="yr">2026</span> PerPHect®. Todos los derechos reservados.</p><div class="fbottom-links" style="margin-top:10px"><a href="aviso-privacidad.html">Aviso de privacidad</a><button type="button" data-cookie-settings>Configurar cookies</button></div></div></div>
  </div>
</footer>
{wa}
<script src="/assets/js/main.js?v={_v('assets/js/main.js')}"></script>
<script src="/assets/js/cookies.js?v={_v('assets/js/cookies.js')}" defer></script>
</body>
</html>
'''
    open(ROOT + fname, 'w').write(html)


def head(label, h1, lead, left=False):
    return f'<section class="page-head{" left" if left else ""}"><div class="wrap"><span class="dots" aria-hidden="true"></span><span class="label">{label}</span><h1>{h1}</h1><p class="lead">{lead}</p></div></section>'


def band(light, bold, dark=False):
    return f'<div class="band{" dark" if dark else ""} rv"><h2>{light} <b>{bold}</b></h2></div>'


def portadilla(title, icons, sid=''):
    imgs = '<span class="plus" aria-hidden="true">+</span>'.join(f'<img src="/assets/img/icon-{i}.png" alt="" width="140" height="140" loading="lazy">' for i in icons)
    return f'''<section class="portadilla"{f' id="{sid}"' if sid else ''} aria-label="{title.replace('<br>', ' ')}">
  <div class="top"><div class="wrap"><span class="dots" aria-hidden="true"></span><h2 class="rv">{title}</h2></div></div>
  <div class="mid"><div class="strip">{imgs}</div></div>
  <div class="bot"></div>
</section>'''


def cta(t='Hablemos de la siguiente etapa de tu empresa.'):
    return f'''<section class="cta-gold"><div class="wrap"><div><h2 class="rv">{t}</h2></div><a href="/#contacto" class="btn btn-dark rv">Contacto</a></div></section>'''


def nextp(href, label, title):
    return f'<section class="nextp"><div class="wrap"><span class="small">Siguiente · {label}</span><a class="link" href="{href}">{title} →</a></div></section>'


PYRAMID = '''<svg viewBox="0 0 440 330" role="img" aria-label="Pirámide de la estructura de acompañamiento: Consejero Senior, Consejero Junior, Consultores y Analistas">
<g fill="none" stroke-linejoin="round" stroke-width="1.6">
<polygon points="220,14 176,96 264,96" fill="#b08c52" stroke="#86662f"/>
<line x1="220" y1="14" x2="226" y2="96" stroke="#86662f"/>
<polygon points="168,112 272,112 304,196 136,196" fill="#f6f6f6" stroke="#3a3a3c"/>
<line x1="222" y1="112" x2="226" y2="196" stroke="#3a3a3c"/>
<polygon points="128,212 312,212 360,316 80,316" fill="#f6f6f6" stroke="#3a3a3c"/>
<line x1="224" y1="212" x2="226" y2="316" stroke="#3a3a3c"/>
</g></svg>'''

MESA = '''<svg viewBox="0 0 520 520" role="img" aria-label="Caso de estudio al centro de una mesa colegiada: Consejero Senior, Consejero Junior, Analista y Consultor">
<circle cx="260" cy="260" r="196" fill="none" stroke="#b08c52" stroke-width="1.2"/>
<g fill="#b08c52"><circle cx="122" cy="122" r="5"/><circle cx="398" cy="122" r="5"/><circle cx="122" cy="398" r="5"/><circle cx="398" cy="398" r="5"/></g>
<circle cx="260" cy="260" r="112" fill="#3a3a3c"/>
<circle cx="260" cy="260" r="104" fill="none" stroke="rgba(255,255,255,.15)"/>
<text x="260" y="252" text-anchor="middle" fill="#fff" font-family="Fira Sans, sans-serif" font-weight="700" font-size="22" letter-spacing="2">CASO DE</text>
<text x="260" y="282" text-anchor="middle" fill="#fff" font-family="Fira Sans, sans-serif" font-weight="700" font-size="22" letter-spacing="2">ESTUDIO</text>
<g font-family="Fira Sans, sans-serif" font-weight="700" font-size="14" letter-spacing="1.5" fill="#86662f" text-anchor="middle">
<rect x="185" y="38" width="150" height="54" rx="10" fill="#fff" stroke="#b08c52"/><text x="260" y="62" fill="#86662f">CONSEJERO</text><text x="260" y="80" fill="#86662f">SENIOR</text>
<rect x="400" y="233" width="112" height="54" rx="10" fill="#fff" stroke="#b08c52"/><text x="456" y="257" fill="#86662f">CONSEJERO</text><text x="456" y="275" fill="#86662f">JUNIOR</text>
<rect x="195" y="428" width="130" height="44" rx="10" fill="#fff" stroke="#b08c52"/><text x="260" y="455" fill="#86662f">ANALISTA</text>
<rect x="8" y="238" width="112" height="44" rx="10" fill="#fff" stroke="#b08c52"/><text x="64" y="265" fill="#86662f">CONSULTOR</text>
</g></svg>'''

# ================= INICIO (una sola página) =================
FORM = f'''<form id="leadForm" novalidate>
        <input class="hp" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
        <div class="field"><label for="nombre">Nombre <abbr title="Obligatorio">*</abbr></label><input id="nombre" name="nombre" type="text" autocomplete="name" maxlength="120" placeholder="Tu nombre completo" required><div class="msg">Escribe tu nombre.</div></div>
        <div class="field"><label for="email">Email <abbr title="Obligatorio">*</abbr></label><input id="email" name="email" type="email" autocomplete="email" maxlength="160" placeholder="nombre@empresa.com" required><div class="msg">Escribe un email válido.</div></div>
        <div class="field"><label for="whatsapp">WhatsApp <abbr title="Obligatorio">*</abbr></label><input id="whatsapp" name="whatsapp" type="tel" autocomplete="tel" inputmode="tel" maxlength="25" placeholder="+52 55 1234 5678" required><div class="msg">Escribe tu número con lada (10 a 15 dígitos).</div></div>
        <div class="field"><label for="comentarios">Comentarios</label><textarea id="comentarios" name="comentarios" rows="3" maxlength="1500" placeholder="Opcional"></textarea></div>
        <div class="consents"><label class="consent" for="aceptaPrivacidad"><input id="aceptaPrivacidad" type="checkbox" required><span>He leído el <a href="/aviso-privacidad" target="_blank" rel="noopener">aviso de privacidad</a> y autorizo a PerPHect a usar mis datos para contactarme y atender esta solicitud. <abbr title="Obligatorio">*</abbr></span></label>
        <label class="consent" for="aceptaMarketing"><input id="aceptaMarketing" type="checkbox"><span>Autorizo recibir publicidad, novedades e invitaciones de PerPHect por correo electrónico y WhatsApp.</span></label></div>
        <div class="ts-box" id="perphect-turnstile" aria-label="Verificación de seguridad"></div>
        <noscript><p class="fine">Para enviar este formulario activa JavaScript o escríbenos por <a href="{WA_LINK}">WhatsApp</a>.</p></noscript>
        <button type="submit" class="btn btn-dark">Enviar</button>
        <p class="feedback" id="formFeedback" role="status" aria-live="polite"></p>
        <p class="fine"><abbr>*</abbr> Campos obligatorios. No incluyas contraseñas, datos bancarios ni documentos confidenciales. Formulario protegido con Cloudflare Turnstile.</p>
      </form>'''

page('index.html', 'PerPHect | Redefining Business Strategy',
     'En PerPHect, la asesoría no es una persona: es un sistema de innovación y estrategia al servicio de tu negocio.',
     extra_head='\n<link rel="preconnect" href="https://challenges.cloudflare.com">\n<script src="https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit" async defer></script>', home=True, body=f'''
<section class="hero" id="inicio">
  <div class="hero-bg" aria-hidden="true"></div>
  <div class="wrap">
    <h1 class="hero-h1"><img class="hero-logo" src="/assets/logos/perphect-blanco.svg" alt="PerPHect · Redefining Business Strategy" width="520" height="177"></h1>
    <img class="hero-seal" src="/assets/img/sello-mx-us.png" alt="México y Estados Unidos" width="300" height="95">
    <nav class="cover-index" aria-label="Contenido">
      <a href="#consejero">El Consejero <b>PerPHect</b></a>
      <a href="#estructura">Estructura de acompañamiento</a>
      <a href="#innovacion">Innovación <b>PerPHect</b></a>
    </nav>
  </div>
</section>

{portadilla('El Consejero<br>PerPHect', ['estrategia', 'consejero'], 'consejero')}

<section>
  <div class="wrap">
    {band('El Consejero', 'PerPHect')}
    <div class="reading rv" style="max-width:860px">
      <p>En PerPHect entendemos que no todas las figuras de acompañamiento empresarial generan el mismo impacto. Existen <b>consultores</b> que llegan con recetas predefinidas, <b>coaches</b> que se enfocan en la persona y <b>consejeros tradicionales</b> que cumplen un rol más formal que real. Sin embargo, ninguno de ellos logra <b>resolver a fondo la compleja transición</b> de pasar de dueño a estratega y de estratega a institucionalizador.</p>
      <p>El <b>Consejero PerPHect</b> es distinto. Su valor radica en ser, ante todo, un <b>empresario consultando a empresarios</b>. La legitimidad de su acompañamiento proviene de haber enfrentado la toma de decisiones bajo presión, de haber asumido riesgos reales y de sostener el crecimiento en contextos cambiantes. Esa experiencia le permite hablar <b>desde la práctica</b> y no <b>desde la teoría</b>, aportando claridad y empatía en cada etapa del proceso.</p>
      <p>A diferencia del consultor que entrega manuales prefabricados o del coach que trabaja únicamente lo personal, el Consejero PerPHect <b>transforma la intención en estructura y la estructura en resultados.</b> Su función no es pasiva ni decorativa, sino la de un agente que asegura que cada decisión se traduzca en permanencia, institucionalización y creación de valor sostenible.</p>
    </div>
  </div>
</section>

<section class="on-dark">
  <div class="wrap">
    <h2 class="rv">Los pilares del Consejero PerPHect</h2>
    <div class="pillars">
      <div class="pillar rv"><h3><span class="dot"></span>Disciplina en la gobernanza</h3><p>Toda decisión se conduce bajo protocolos claros de presentación, discusión y aprobación (PDA). Con ello se evita que las decisiones sean aisladas o impulsivas, y se garantiza la continuidad.</p></div>
      <div class="pillar rv"><h3><span class="dot"></span>Estructura con propósito</h3><p>Convierte la intuición del dueño en procesos estratégicos, de forma que la organización trascienda a las personas y se proyecte hacia el futuro.</p></div>
      <div class="pillar rv"><h3><span class="dot"></span>Independencia y visión integral</h3><p>El consejero actúa con autonomía, sin complacencias ni conflictos de interés, aportando una visión que conecta estrategia, sostenibilidad y permanencia.</p></div>
      <div class="pillar rv"><h3><span class="dot"></span>Impacto medible</h3><p>Cada decisión debe generar avances concretos, con indicadores claros. <b style="color:#fff">El consejero se mide por el valor creado, no por el tiempo invertido.</b></p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    {band('El Consejero PerPHect y la', 'vanguardia')}
    <div class="split wide">
      <div class="rv" style="display:flex;justify-content:center"><img src="/assets/img/icon-vanguardia.png" alt="" width="200" height="200" style="width:170px;filter:brightness(.72)" loading="lazy"></div>
      <div class="reading rv">
        <p>El <b>Consejero PerPHect</b> vive en la vanguardia, porque entiende que los retos actuales necesitan <b>velocidad y precisión.</b> No basta con estructuras sólidas; hoy la diferencia está en la capacidad de responder con agilidad, sin perder profundidad en las decisiones. Su rol es asegurar que la empresa avance con paso firme, pero también con rapidez, adaptándose a entornos cambiantes y tomando decisiones oportunas que no dejen escapar oportunidades. Esta combinación de <b>disciplina y velocidad</b> es lo que convierte al Consejero PerPHect en un aliado estratégico distinto a cualquier otro.</p>
      </div>
    </div>
  </div>
</section>

<section class="marmol">
  <div class="wrap philo">
    <div class="bar" aria-hidden="true"></div>
    <div>
      <h2 class="rv">La filosofía que lo sustenta</h2>
      <p class="motto rv">Desarrollo empresarial<br>para el desarrollo económico,<br><b>para el desarrollo social.</b></p>
      <div class="reading rv" style="margin-top:34px"><p>El Consejero PerPHect encarna esta filosofía porque entiende que un desarrollo empresarial sólido, construido sobre gobernanza y disciplina, se convierte en motor de desarrollo económico sostenible. Y este crecimiento, proyectado más allá de la empresa, se traduce en desarrollo social que beneficia a colaboradores, familias y comunidades.</p></div>
    </div>
  </div>
  <div class="wrap"><div class="box rv"><p style="font-size:19px;color:var(--suave)">Así, el Consejero PerPHect resuelve el <b style="color:var(--carbon)">dilema de la dueñitud</b>: acompaña al dueño en su transición hacia un modelo institucional que combina experiencia práctica, estructura clara y una visión de trascendencia que impacta a la empresa, a la economía y a la sociedad.</p></div></div>
</section>

{portadilla('Estructura de<br>acompañamiento', ['piramide'], 'estructura')}

<section>
  <div class="wrap">
    <div class="reading rv"><p>En PerPHect hemos diseñado una estructura clara y funcional que <b>evita la dependencia de una sola persona y asegura resultados consistentes.</b> Nuestro modelo combina simplicidad organizacional con una métrica propia de desempeño: el <b>PerPHect Impact.</b></p></div>
    <div class="impact rv"><b>PerPHect Impact</b> <span class="op">=</span> Casos de éxito <span class="op">×</span> Tamaño de la empresa <span class="op">÷</span> Impacto generado en el cliente.</div>
    <p class="muted rv" style="margin-top:22px;max-width:var(--ancho-lectura)">Este indicador refleja cómo cada integrante del equipo contribuye a los logros de nuestros clientes, destacando no solo la magnitud de los proyectos, sino la relevancia y sostenibilidad de los resultados.</p>
    <div class="pyramid">
      <div class="rv">{PYRAMID}</div>
      <div class="levels">
        <p class="muted rv">La estructura operativa de la firma se organiza en tres niveles:</p>
        <div class="level l1 rv"><span class="tagl"><i>1.</i> Consejero Senior</span><p>Máxima figura de la firma. Su PerPHect Impact se mide en los casos de éxito emblemáticos y en su capacidad para consolidar una <b>visión estratégica global.</b></p></div>
        <div class="level l2 rv"><span class="tagl"><i>2.</i> Consejero Junior</span><p>Empresarios con experiencia comprobada que acompañan al cliente en decisiones críticas y <b>lideran proyectos clave.</b> Su PerPHect Impact se vincula al tamaño de las empresas que asesoran y al número de transformaciones exitosas que impulsan.</p></div>
        <div class="level l3 rv"><span class="tagl"><i>3.</i> Consultores y Analistas</span><p>Base técnica y operativa. Aportan análisis, reportes e investigación que <b>fortalecen la labor de los consejeros.</b> Su PerPHect Impact refleja la calidad del soporte brindado, multiplicando la capacidad de convertir estrategias en resultados concretos.</p></div>
      </div>
    </div>
    <div class="box rv" style="margin-top:64px"><p style="font-size:19px;color:var(--suave)">Con este modelo, PerPHect une lo mejor de dos mundos: una estructura sencilla y ágil con una métrica única que garantiza que cada esfuerzo se traduzca en transformaciones reales y duraderas.</p></div>
  </div>
</section>

{portadilla('Innovación<br>PerPHect', ['cerebro', 'comision', 'vanguardia'], 'innovacion')}

<section>
  <div class="wrap">
    <div class="reading rv" style="max-width:860px"><p>La verdadera innovación de PerPHect está en no depender de la voz de un solo socio, sino en el poder de una estructura colegiada. Por ello hemos creado la <b>Comisión de Análisis PerPHect</b>, un mecanismo que asegura decisiones de alto impacto a través de un proceso estructurado.</p></div>
  </div>
</section>

<section class="on-dark">
  <div class="wrap">
    <h2 class="rv">Cada proyecto se convierte en un <em>caso de estudio</em> que se analiza siguiendo cuatro pasos:</h2>
    <div class="steps4">
      <div class="rv"><span class="n">01</span><h3>Problema</h3><p>Identificación clara del reto.</p></div>
      <div class="rv"><span class="n">02</span><h3>Oportunidad</h3><p>Reconocer áreas de crecimiento o mejora.</p></div>
      <div class="rv"><span class="n">03</span><h3>Acción</h3><p>Definir la estrategia precisa.</p></div>
      <div class="rv"><span class="n">04</span><h3>Resultado</h3><p>Asegurar la ejecución y medir logros.</p></div>
    </div>
    <p class="rv" style="margin-top:48px;max-width:760px">El comité genera el consenso estratégico y una persona designada se encarga de comunicarlo y llevarlo a ejecución. Con este esquema, los clientes acceden a un sistema robusto de consejería que escala sin perder calidad.</p>
  </div>
</section>

<section>
  <div class="wrap split" style="align-items:center">
    <div>
      <h2 class="rv">Beneficios para el cliente</h2>
      <ul class="benefits rv">
        <li>Flexibilidad en los niveles de servicio y honorarios.</li>
        <li>Resultados consistentes, sin importar quién comunique o ejecute.</li>
        <li>Acceso a un modelo innovador que combina visión empresarial con metodología clara.</li>
      </ul>
      <div class="box rv"><p class="quote" style="font-size:24px">En PerPHect, la asesoría no es una persona: es un <b>sistema de innovación y estrategia</b> al servicio de tu negocio.</p></div>
    </div>
    <div class="table-diagram rv">{MESA}</div>
  </div>
</section>

{cta()}

<section class="contact-sec" id="contacto">
  <div class="wrap split" style="align-items:start">
    <div>
      <span class="dots" aria-hidden="true"></span>
      <h2 class="rv" style="text-transform:uppercase">Contacto</h2>
      <div class="offices rv">
        <div><span>WhatsApp</span><a href="{WA_LINK}" target="_blank" rel="noopener">{WA_DISPLAY}</a></div>
        <div><span>CDMX</span><p>{CDMX}</p></div>
        <div><span>Dallas</span><p>{DAL}</p></div>
        <div><span>Redes</span>{SOCIAL}</div>
      </div>
    </div>
    <div class="form">
      {FORM}
    </div>
  </div>
</section>''')

# ================= 404 =================
page('404.html', 'Página no encontrada | PerPHect', 'La página que buscas no existe.', '''
<section class="hero err404">
  <div class="hero-bg" aria-hidden="true"></div>
  <div class="wrap">
    <span class="label">Error 404</span>
    <h1>Esta página no existe</h1>
    <p class="intro">La página que buscas cambió de lugar o ya no está disponible. Vuelve al inicio o escríbenos.</p>
    <div class="ctas"><a href="/" class="btn btn-gold">Volver al inicio</a><a href="/#contacto" class="btn btn-line">Contacto</a></div>
  </div>
</section>''', home=True)

# ================= AVISO (pendiente del documento) =================
page('aviso-privacidad.html', 'Aviso de privacidad | PerPHect', 'Aviso de privacidad y política de cookies de PerPHect.',
     head('Legal', 'Aviso de privacidad', 'Tratamiento de datos personales y uso de cookies en perphect.com.', left=True) + '''
<section style="padding-top:72px">
  <div class="wrap legal-doc">
    <div class="meta"><span><b>Responsable:</b> PerPHect</span><span><b>Sitio web:</b> <a href="https://perphect.com/">https://perphect.com/</a></span><span><b>Domicilio:</b> Juan de Acuña 318, Lomas de Chapultepec, Miguel Hidalgo, CDMX, 11000</span></div>
    <p class="notice">El aviso de privacidad integral se publicará en esta página. Mientras tanto, los datos que nos compartes a través del formulario se usan únicamente para contactarte y atender tu solicitud.</p>
    <h2 id="cookies">Cookies y tecnologías similares</h2>
    <p>Usamos tecnologías necesarias para la seguridad del sitio y del formulario. Solo con tu autorización activaremos herramientas de analítica y publicidad.</p>
    <table><thead><tr><th>Tipo</th><th>Finalidad</th><th>¿Requiere autorización?</th></tr></thead><tbody>
      <tr><td>Necesarias</td><td>Seguridad del sitio, protección del formulario contra bots (Cloudflare Turnstile) y guardado de tus preferencias.</td><td>No</td></tr>
      <tr><td>Analítica y publicidad</td><td>Estadísticas de navegación y medición de campañas (por ejemplo, Google Analytics o Meta Pixel cuando estén habilitados).</td><td>Sí</td></tr>
    </tbody></table>
    <p style="margin-top:32px"><button type="button" class="btn btn-dark" data-cookie-settings>Configurar cookies</button></p>
  </div>
</section>''')

# ================= GRACIAS =================
page('gracias.html', 'Gracias | PerPHect', 'Recibimos tu solicitud.', '''
<section class="page-head left" style="border:0;padding-bottom:140px">
  <div class="wrap" style="max-width:820px">
    <span class="dots" aria-hidden="true"></span>
    <span class="label">Solicitud recibida</span>
    <h1>Gracias, recibimos tus datos</h1>
    <p class="lead">Nos pondremos en contacto contigo muy pronto por correo electrónico o WhatsApp.</p>
    <div class="ctas"><a href="/" class="btn btn-dark">Volver al inicio</a></div>
  </div>
</section>''', noindex=True)

# sitemap
pages = ['index.html', 'aviso-privacidad.html']
open(ROOT + 'sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{url(p)}</loc></url>\n' for p in pages) + '</urlset>\n')
print('ok')
