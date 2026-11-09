"""Genera las páginas de perphect.com con encabezado y pie comunes.
Ejecutar desde la raíz del repo:  python3 tools/generar_sitio.py
Versiona CSS/JS por hash para evitar caché vieja."""
import os, hashlib
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
DOM = 'https://perphect.com'

def _v(f): return hashlib.md5(open(ROOT + f, 'rb').read()).hexdigest()[:8]

# ---- Datos de contacto (completar) ----
WA_NUM = ''          # p. ej. '5215512345678' (solo dígitos, con lada de país). Vacío = sin botón.
WA_TXT = 'Hola%20PerPHect%2C%20me%20gustar%C3%ADa%20agendar%20una%20conversaci%C3%B3n.'
WA_LINK = f'https://wa.me/{WA_NUM}?text={WA_TXT}' if WA_NUM else ''
WA_SVG = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91C21.95 6.45 17.5 2 12.04 2zm5.8 14.03c-.24.68-1.42 1.3-1.95 1.34-.5.05-.97.23-3.27-.68-2.77-1.09-4.51-3.92-4.65-4.1-.13-.18-1.11-1.48-1.11-2.82 0-1.34.7-2 .95-2.27.25-.27.54-.34.72-.34h.52c.17 0 .39-.06.61.47.24.55.79 1.9.86 2.04.07.14.11.3.02.48-.09.18-.14.3-.27.46-.14.16-.29.36-.41.48-.14.14-.28.29-.12.56.16.27.71 1.17 1.52 1.9 1.05.93 1.93 1.22 2.2 1.36.27.14.43.11.59-.07.16-.18.68-.79.86-1.06.18-.27.36-.23.61-.14.25.09 1.59.75 1.86.89.27.14.45.2.52.32.07.11.07.66-.17 1.33z"/></svg>'

CDMX = 'Juan de Acuña 318, Lomas - Virreyes,<br>Lomas de Chapultepec IV Secc,<br>Miguel Hidalgo, 11000, Ciudad de México'
DAL = '3441 Halifax St, Dallas,<br>Texas 75247, EE. UU.'

NAV = [('index.html', 'Inicio'), ('servicios.html', 'Servicios'), ('consejero.html', 'El Consejero'), ('metodologia.html', 'Metodología')]
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fira+Sans:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,400;0,700;1,400;1,700&display=swap">'


def url(fname):
    return DOM + '/' + ('' if fname == 'index.html' else fname.replace('.html', ''))


def page(fname, title, desc, body, home=False, extra_head='', noindex=False):
    links = ''.join(f'<a href="{h}"{" class=\"active\" aria-current=\"page\"" if h == fname else ""}>{t}</a>' for h, t in NAV)
    cta_active = ' active' if fname == 'contacto.html' else ''
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
    <a class="brand" href="/" aria-label="PerPHect, inicio"><img class="dark" src="/assets/logos/perphect-color-sin-lema.svg" alt="PerPHect" width="170" height="47"><img class="light" src="/assets/logos/perphect-blanco-sin-lema.svg" alt="PerPHect" width="170" height="47"></a>
    <button class="burger" aria-label="Abrir menú" aria-expanded="false" aria-controls="menu"><span></span></button>
    <nav class="menu" id="menu" aria-label="Principal">{links}<a href="contacto.html" class="btn btn-line{cta_active}">Contacto</a></nav>
  </div>
</header>
<main>
{body}
</main>
<footer>
  <div class="wrap">
    <div class="fgrid">
      <div class="fl"><img class="flogo" src="/assets/logos/perphect-blanco.svg" alt="PerPHect · Redefining Business Strategy" width="220" height="75" loading="lazy"><p>Firma de consejería empresarial. Gobierno corporativo, empresas familiares e institucionalización: empresarios consultando a empresarios.</p></div>
      <div><h5>Sitio</h5><ul>{''.join(f'<li><a href="{h}">{t}</a></li>' for h, t in NAV[1:])}<li><a href="contacto.html">Contacto</a></li></ul></div>
      <div><h5>Oficinas</h5><div class="addr"><div><b>México, CDMX</b><p>{CDMX}</p></div><div><b>Dallas, TX</b><p>{DAL}</p></div></div></div>
    </div>
    <div class="seal"><img src="/assets/img/sello-mx-us.png" alt="Sello binacional México y Estados Unidos" width="150" height="48" loading="lazy"><span>México · Estados Unidos</span></div>
    <div class="fbottom"><p class="legal">La información de este sitio es de carácter general e informativo. Los alcances, entregables y honorarios de cada servicio se definen en la propuesta económica entregada a cada cliente.</p><div><p>© <span id="yr">2026</span> PerPHect®. Todos los derechos reservados.</p><div class="fbottom-links" style="margin-top:10px"><a href="aviso-privacidad.html">Aviso de privacidad</a><button type="button" data-cookie-settings>Configurar cookies</button></div></div></div>
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


def portadilla(title, icons):
    imgs = '<span class="plus" aria-hidden="true">+</span>'.join(f'<img src="/assets/img/icon-{i}.png" alt="" width="140" height="140" loading="lazy">' for i in icons)
    return f'''<section class="portadilla" aria-label="{title.replace('<br>', ' ')}">
  <div class="top"><div class="wrap"><span class="dots" aria-hidden="true"></span><h2 class="rv">{title}</h2></div></div>
  <div class="mid"><div class="strip">{imgs}</div></div>
  <div class="bot"></div>
</section>'''


def cta(t='Hablemos de la siguiente etapa de tu empresa.', l='Una conversación inicial para entender tus retos, tu estructura y hacia dónde quieres llevar tu organización.'):
    return f'''<section class="cta-gold"><div class="wrap"><div><h2 class="rv">{t}</h2><p class="rv">{l}</p></div><a href="contacto.html" class="btn btn-dark rv">Agenda una conversación</a></div></section>'''


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

# ================= INICIO =================
page('index.html', 'PerPHect | Gobierno corporativo y empresas familiares',
     'Firma de consejería empresarial en Ciudad de México y Dallas. Gobierno corporativo, empresas familiares e institucionalización: empresarios consultando a empresarios.', f'''
<section class="hero">
  <div class="hero-bg" aria-hidden="true"></div>
  <div class="wrap">
    <img class="hero-logo" src="/assets/logos/perphect-blanco.svg" alt="PerPHect · Redefining Business Strategy" width="520" height="177">
    <p class="tag">Gobierno corporativo · Empresas familiares · Institucionalización</p>
    <h1>Empresarios consultando a empresarios</h1>
    <p class="intro">Acompañamos a dueños y familias empresarias en la transición de <b>Dueño-CEO a Dueño-Presidente</b>: transformamos la intención en estructura y la estructura en resultados.</p>
    <div class="ctas"><a href="contacto.html" class="btn btn-gold">Agenda una conversación</a><a href="metodologia.html" class="btn btn-line">Conoce la metodología</a></div>
  </div>
  <div class="cities" aria-hidden="true">Ciudad de México <i></i> Dallas</div>
</section>

<section>
  <div class="wrap">
    {band('Propuesta de', 'valor')}
    <div class="split wide">
      <div><span class="label rv">Por qué PerPHect</span><h2 class="rv">No todas las figuras de acompañamiento generan el mismo impacto.</h2></div>
      <div class="reading rv" style="padding-top:38px"><p>Pasar de dueño a estratega y de estratega a institucionalizador es una de las transiciones más complejas de una empresa. En PerPHect la resolvemos desde la práctica, no desde la teoría: <b>somos empresarios consultando a empresarios</b>.</p></div>
    </div>
    <div class="compare rv">
      <div><small>Consultor</small><h3>Recetas predefinidas</h3><p>Llega con manuales prefabricados que no siempre responden a tu realidad.</p></div>
      <div><small>Coach</small><h3>Enfoque en la persona</h3><p>Trabaja lo personal, pero no construye la estructura de la organización.</p></div>
      <div><small>Consejero tradicional</small><h3>Un rol formal</h3><p>Cumple una función más formal que real dentro del consejo.</p></div>
      <div><small>Consejero PerPHect</small><h3>Estructura y resultados</h3><p>Convierte cada decisión en permanencia, institucionalización y valor sostenible.</p></div>
    </div>
  </div>
</section>

<section class="marmol">
  <div class="wrap">
    <span class="dots" aria-hidden="true"></span>
    <span class="label rv">Servicios</span>
    <h2 class="rv">Gobernanza para empresas que quieren trascender a sus fundadores.</h2>
    <div class="list">
      <div class="item rv"><span class="n">01</span><h3>Gobierno corporativo</h3><p>Constitución y profesionalización del consejo, con protocolos claros de <b>Presentación, Discusión y Aprobación (PDA)</b>.</p></div>
      <div class="item rv"><span class="n">02</span><h3>Empresas familiares</h3><p>Orden entre familia, propiedad y empresa para que el negocio crezca y continúe de una generación a la siguiente.</p></div>
      <div class="item rv"><span class="n">03</span><h3>Institucionalización</h3><p>Convertimos la intuición del dueño en <b>Estrategia, Política y Proceso (EPP)</b>, para que la organización trascienda a las personas.</p></div>
    </div>
    <p class="rv" style="margin-top:40px"><a class="link" href="servicios.html">Ver servicios</a></p>
  </div>
</section>

{portadilla('El Consejero<br>PerPHect', ['estrategia', 'consejero'])}

<section>
  <div class="wrap">
    <div class="split wide">
      <div><span class="label rv">El Consejero PerPHect</span><h2 class="rv">Estrategia más experiencia real.</h2></div>
      <div class="reading rv" style="padding-top:38px"><p>Su legitimidad proviene de haber tomado decisiones bajo presión, asumido riesgos reales y sostenido el crecimiento en contextos cambiantes. Por eso habla <b>desde la práctica</b> y aporta claridad y empatía en cada etapa del proceso.</p><p style="margin-top:26px"><a class="link" href="consejero.html">Conoce al Consejero PerPHect</a></p></div>
    </div>
    <div class="box quote-box rv"><p class="quote">“El consejero se mide por el valor creado, no por el tiempo invertido.”</p></div>
  </div>
</section>

<section class="marmol">
  <div class="wrap">
    <span class="label rv">Conoce PerPHect</span>
    <h2 class="rv">Un sistema de consejería, no una sola voz.</h2>
    <div class="explore">
      <a href="servicios.html" class="rv"><span class="n">01</span><h3>Servicios</h3><p>Gobierno corporativo, empresa familiar e institucionalización, y cómo trabajamos contigo.</p><span class="go">Explorar →</span></a>
      <a href="consejero.html" class="rv"><span class="n">02</span><h3>El Consejero</h3><p>Los cuatro pilares, la vanguardia y la filosofía que lo sustenta.</p><span class="go">Explorar →</span></a>
      <a href="metodologia.html" class="rv"><span class="n">03</span><h3>Metodología</h3><p>Estructura de acompañamiento, PerPHect Impact y la Comisión de Análisis PerPHect.</p><span class="go">Explorar →</span></a>
    </div>
  </div>
</section>

<section>
  <div class="wrap philo">
    <div class="bar" aria-hidden="true"></div>
    <div><span class="label rv">Filosofía</span><h2 class="rv">La filosofía que nos sustenta</h2><p class="motto rv">Desarrollo empresarial<br>para el desarrollo económico,<br><b>para el desarrollo social.</b></p></div>
  </div>
</section>
{cta()}
''', home=True)

# ================= SERVICIOS =================
page('servicios.html', 'Servicios | PerPHect', 'Gobierno corporativo, empresas familiares, institucionalización y consejería estratégica para dueños y familias empresarias.',
     head('Servicios', 'Al servicio de tu negocio', 'Acompañamos a dueños y familias empresarias a construir la estructura que su empresa necesita para crecer, ordenarse y permanecer.') + f'''
<section>
  <div class="wrap">
    {band('Lo que', 'hacemos')}
    <div class="split wide">
      <div><span class="label rv">Nuestro enfoque</span><h2 class="rv">De la intención a la estructura.</h2></div>
      <div class="reading rv" style="padding-top:38px"><p>Cada empresa llega con una historia, una familia y una forma de decidir. Partimos de ahí para diseñar un <b>gobierno a la medida</b>, sin recetas predefinidas, y lo acompañamos hasta que funciona en la práctica.</p></div>
    </div>
    <div class="svc">
      <article class="rv"><span class="n">01</span><h3>Gobierno corporativo</h3><p>Constituimos y profesionalizamos los órganos de decisión de tu empresa para que cada decisión tenga método, continuidad y seguimiento.</p>
        <ul><li>Constitución del consejo de administración</li><li>Integración de consejeros independientes</li><li>Comités y agenda de sesiones</li><li>Protocolo PDA: Presentación, Discusión y Aprobación</li></ul></article>
      <article class="rv"><span class="n">02</span><h3>Empresas familiares</h3><p>Ordenamos la relación entre familia, propiedad y empresa para proteger el patrimonio y la armonía, y asegurar la continuidad del negocio.</p>
        <ul><li>Reglas claras entre familia y empresa</li><li>Órganos de gobierno familiar</li><li>Planeación de la continuidad y la sucesión</li><li>Preparación de la siguiente generación</li></ul></article>
      <article class="rv"><span class="n">03</span><h3>Institucionalización</h3><p>Convertimos la intuición del dueño en procesos estratégicos, de modo que la organización trascienda a las personas y se proyecte hacia el futuro.</p>
        <ul><li>Transición de Dueño-CEO a Dueño-Presidente</li><li>Modelo EPP: Estrategia, Política y Proceso</li><li>Estructura organizacional y roles</li><li>Indicadores de desempeño</li></ul></article>
      <article class="rv"><span class="n">04</span><h3>Consejería estratégica</h3><p>Un Consejero PerPHect se integra a tu mesa de decisiones, respaldado por la Comisión de Análisis PerPHect, para acompañar las decisiones críticas.</p>
        <ul><li>Consejero Senior o Junior según la etapa</li><li>Casos de estudio colegiados</li><li>Seguimiento a la ejecución</li><li>Medición del valor creado</li></ul></article>
    </div>
  </div>
</section>

<section class="on-dark">
  <div class="wrap">
    <span class="label rv">Cómo trabajamos</span>
    <h2 class="rv">Una relación que empieza con una conversación.</h2>
    <div class="flow">
      <div class="rv"><small>Paso 01</small><h3>Conversación</h3><p>Escuchamos tu historia, tus retos y lo que quieres para tu empresa.</p></div>
      <div class="rv"><small>Paso 02</small><h3>Diagnóstico</h3><p>Entendemos cómo se decide hoy y qué estructura hace falta.</p></div>
      <div class="rv"><small>Paso 03</small><h3>Propuesta</h3><p>Te presentamos alcance, nivel de acompañamiento y propuesta económica.</p></div>
      <div class="rv"><small>Paso 04</small><h3>Acompañamiento</h3><p>Implementamos contigo y medimos los avances con indicadores claros.</p></div>
    </div>
  </div>
</section>
''' + nextp('consejero.html', 'El Consejero', 'El Consejero PerPHect') + cta())

# ================= CONSEJERO =================
page('consejero.html', 'El Consejero PerPHect | PerPHect', 'El Consejero PerPHect: empresarios consultando a empresarios. Disciplina en la gobernanza, estructura con propósito, independencia e impacto medible.',
     head('El Consejero PerPHect', 'El Consejero PerPHect', 'Su valor radica en ser, ante todo, un empresario consultando a empresarios.') + f'''
<section>
  <div class="wrap split wide">
    <div><span class="label rv">Un consejero distinto</span><h2 class="rv">Transforma la intención en estructura y la estructura en resultados.</h2></div>
    <div class="reading rv" style="padding-top:38px">
      <p>En PerPHect entendemos que no todas las figuras de acompañamiento empresarial generan el mismo impacto. Existen <b>consultores</b> que llegan con recetas predefinidas, <b>coaches</b> que se enfocan en la persona y <b>consejeros tradicionales</b> que cumplen un rol más formal que real. Ninguno logra <b>resolver a fondo la compleja transición</b> de pasar de dueño a estratega y de estratega a institucionalizador.</p>
      <p>La legitimidad del <b>Consejero PerPHect</b> proviene de haber enfrentado la toma de decisiones bajo presión, de haber asumido riesgos reales y de sostener el crecimiento en contextos cambiantes. Esa experiencia le permite hablar <b>desde la práctica</b> y no desde la teoría.</p>
      <p>Su función no es pasiva ni decorativa: es la de un agente que asegura que cada decisión se traduzca en <b>permanencia, institucionalización y creación de valor sostenible</b>.</p>
    </div>
  </div>
</section>

<section class="on-dark">
  <div class="wrap">
    <span class="label rv">Los pilares del Consejero PerPHect</span>
    <h2 class="rv">Cuatro principios en cada decisión.</h2>
    <div class="pillars">
      <div class="pillar rv"><h3><span class="dot"></span>Disciplina en la gobernanza</h3><p>Toda decisión se conduce bajo protocolos claros de Presentación, Discusión y Aprobación (PDA). Así se evita que las decisiones sean aisladas o impulsivas, y se garantiza la continuidad.</p></div>
      <div class="pillar rv"><h3><span class="dot"></span>Estructura con propósito</h3><p>Convierte la intuición del dueño en procesos estratégicos, de forma que la organización trascienda a las personas y se proyecte hacia el futuro.</p></div>
      <div class="pillar rv"><h3><span class="dot"></span>Independencia y visión integral</h3><p>Actúa con autonomía, sin complacencias ni conflictos de interés, con una visión que conecta estrategia, sostenibilidad y permanencia.</p></div>
      <div class="pillar rv"><h3><span class="dot"></span>Impacto medible</h3><p>Cada decisión debe generar avances concretos, con indicadores claros. <b style="color:#fff">El consejero se mide por el valor creado, no por el tiempo invertido.</b></p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    {band('El consejero y la', 'vanguardia')}
    <div class="split wide">
      <div class="rv" style="display:flex;justify-content:center"><img src="/assets/img/icon-vanguardia.png" alt="" width="200" height="200" style="width:170px;filter:brightness(.72)" loading="lazy"></div>
      <div class="reading rv">
        <p>El <b>Consejero PerPHect</b> vive en la vanguardia porque entiende que los retos actuales necesitan <b>velocidad y precisión</b>. No basta con estructuras sólidas: hoy la diferencia está en responder con agilidad sin perder profundidad en las decisiones.</p>
        <p>Su rol es asegurar que la empresa avance con paso firme, pero también con rapidez, adaptándose a entornos cambiantes y tomando decisiones oportunas que no dejen escapar oportunidades. Esta combinación de <b>disciplina y velocidad</b> lo convierte en un aliado estratégico distinto a cualquier otro.</p>
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
      <div class="reading rv" style="margin-top:34px"><p>Un desarrollo empresarial sólido, construido sobre gobernanza y disciplina, se convierte en motor de desarrollo económico sostenible. Y ese crecimiento, proyectado más allá de la empresa, se traduce en desarrollo social que beneficia a colaboradores, familias y comunidades.</p></div>
    </div>
  </div>
  <div class="wrap"><div class="box rv"><p style="font-size:19px;color:var(--suave)">Así, el Consejero PerPHect resuelve el <b style="color:var(--carbon)">dilema de la dueñitud</b>: acompaña al dueño en su transición hacia un modelo institucional que combina experiencia práctica, estructura clara y una visión de trascendencia que impacta a la empresa, a la economía y a la sociedad.</p></div></div>
</section>
''' + nextp('metodologia.html', 'Metodología', 'Estructura de acompañamiento') + cta())

# ================= METODOLOGÍA =================
page('metodologia.html', 'Metodología | PerPHect', 'Estructura de acompañamiento en tres niveles, la métrica PerPHect Impact y la Comisión de Análisis PerPHect.',
     head('Metodología', 'Estructura de acompañamiento', 'Una estructura clara y funcional que evita la dependencia de una sola persona y asegura resultados consistentes.') + f'''
<section>
  <div class="wrap">
    {band('Estructura de', 'acompañamiento')}
    <div class="reading rv"><p>En PerPHect diseñamos un modelo que combina <b>simplicidad organizacional</b> con una métrica propia de desempeño: el <b>PerPHect Impact</b>. Este indicador refleja cómo cada integrante del equipo contribuye a los logros de nuestros clientes, destacando no solo la magnitud de los proyectos, sino la relevancia y sostenibilidad de los resultados.</p></div>
    <div class="impact rv"><b>PerPHect Impact</b> <span class="op">=</span> Casos de éxito <span class="op">×</span> Tamaño de la empresa <span class="op">÷</span> Impacto generado en el cliente</div>
    <div class="pyramid">
      <div class="rv">{PYRAMID}</div>
      <div class="levels">
        <div class="level l1 rv"><span class="tagl"><i>1.</i> Consejero Senior</span><p>Máxima figura de la firma. Su PerPHect Impact se mide en los casos de éxito emblemáticos y en su capacidad para consolidar una <b>visión estratégica global</b>.</p></div>
        <div class="level l2 rv"><span class="tagl"><i>2.</i> Consejero Junior</span><p>Empresarios con experiencia comprobada que acompañan al cliente en decisiones críticas y <b>lideran proyectos clave</b>. Su PerPHect Impact se vincula al tamaño de las empresas que asesoran y a las transformaciones exitosas que impulsan.</p></div>
        <div class="level l3 rv"><span class="tagl"><i>3.</i> Consultores y Analistas</span><p>Base técnica y operativa. Aportan análisis, reportes e investigación que <b>fortalecen la labor de los consejeros</b> y multiplican la capacidad de convertir estrategias en resultados concretos.</p></div>
      </div>
    </div>
  </div>
</section>

{portadilla('Innovación<br>PerPHect', ['cerebro', 'comision', 'vanguardia'])}

<section>
  <div class="wrap split wide">
    <div><span class="label rv">Comisión de Análisis PerPHect</span><h2 class="rv">El poder de una estructura colegiada.</h2></div>
    <div class="reading rv" style="padding-top:38px"><p>La verdadera innovación de PerPHect está en no depender de la voz de un solo socio. Por ello creamos la <b>Comisión de Análisis PerPHect</b>, un mecanismo que asegura decisiones de alto impacto a través de un proceso estructurado. Cada proyecto se convierte en un <b>caso de estudio</b>.</p></div>
  </div>
</section>

<section class="on-dark">
  <div class="wrap">
    <span class="label rv">El caso de estudio en cuatro pasos</span>
    <h2 class="rv">Del reto a la ejecución medida.</h2>
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
  <div class="wrap split">
    <div class="table-diagram rv">{MESA}</div>
    <div>
      <span class="label rv">Beneficios para el cliente</span>
      <h2 class="rv">Un sistema de consejería que escala sin perder calidad.</h2>
      <ul class="benefits rv">
        <li>Flexibilidad en los niveles de servicio.</li>
        <li>Resultados consistentes, sin importar quién comunique o ejecute.</li>
        <li>Acceso a un modelo innovador que combina visión empresarial con metodología clara.</li>
      </ul>
    </div>
  </div>
  <div class="wrap"><div class="box quote-box rv" style="margin-top:72px"><p class="quote">“En PerPHect, la asesoría no es una persona: es un sistema de innovación y estrategia al servicio de tu negocio.”</p></div></div>
</section>
''' + cta())

# ================= CONTACTO =================
page('contacto.html', 'Contacto | PerPHect', 'Agenda una conversación con PerPHect. Oficinas en Ciudad de México y Dallas, Texas.',
     extra_head='\n<link rel="preconnect" href="https://challenges.cloudflare.com">\n<script src="https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit" async defer></script>', body=f'''
<section class="page-head left plain" style="padding-bottom:110px">
  <div class="wrap split" style="display:grid;text-align:left;align-items:start">
    <div>
      <span class="dots" aria-hidden="true"></span>
      <span class="label">Contacto</span>
      <h1>Agenda una conversación</h1>
      <p class="lead">Cuéntanos sobre tu empresa y el momento que vive. Un Consejero PerPHect te contactará para entender tus retos y explorar cómo podemos acompañarte.</p>
      <div class="offices">
        <div><span>México, CDMX</span><p>{CDMX}</p></div>
        <div><span>Dallas, TX</span><p>{DAL}</p></div>
        {f'<div><span>WhatsApp</span><a href="{WA_LINK}" target="_blank" rel="noopener">Escríbenos por WhatsApp</a></div>' if WA_LINK else ''}
      </div>
    </div>
    <div class="form">
      <form id="leadForm" novalidate>
        <input class="hp" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
        <div class="field"><label for="nombre">Nombre <abbr title="Obligatorio">*</abbr></label><input id="nombre" name="nombre" type="text" autocomplete="name" maxlength="120" placeholder="Tu nombre completo" required><div class="msg">Escribe tu nombre.</div></div>
        <div class="field"><label for="email">Email <abbr title="Obligatorio">*</abbr></label><input id="email" name="email" type="email" autocomplete="email" maxlength="160" placeholder="nombre@empresa.com" required><div class="msg">Escribe un email válido.</div></div>
        <div class="field"><label for="whatsapp">WhatsApp <abbr title="Obligatorio">*</abbr></label><input id="whatsapp" name="whatsapp" type="tel" autocomplete="tel" inputmode="tel" maxlength="25" placeholder="+52 55 1234 5678" required><div class="msg">Escribe tu número con lada (10 a 15 dígitos).</div></div>
        <div class="field"><label for="comentarios">Comentarios</label><textarea id="comentarios" name="comentarios" rows="3" maxlength="1500" placeholder="Cuéntanos sobre tu empresa y qué te gustaría resolver"></textarea></div>
        <div class="consents"><label class="consent" for="aceptaPrivacidad"><input id="aceptaPrivacidad" type="checkbox" required><span>He leído el <a href="aviso-privacidad.html" target="_blank" rel="noopener">aviso de privacidad</a> y autorizo a PerPHect a usar mis datos para contactarme y atender esta solicitud. <abbr title="Obligatorio">*</abbr></span></label>
        <label class="consent" for="aceptaMarketing"><input id="aceptaMarketing" type="checkbox"><span>Autorizo recibir publicidad, novedades e invitaciones de PerPHect por correo electrónico y WhatsApp.</span></label></div>
        <div class="ts-box" id="perphect-turnstile" aria-label="Verificación de seguridad"></div>
        <noscript><p class="fine">Para enviar este formulario activa JavaScript.</p></noscript>
        <button type="submit" class="btn btn-dark">Enviar</button>
        <p class="feedback" id="formFeedback" role="status" aria-live="polite"></p>
        <p class="fine"><abbr>*</abbr> Campos obligatorios. No incluyas contraseñas, datos bancarios ni documentos confidenciales. Formulario protegido con Cloudflare Turnstile.</p>
      </form>
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
    <p class="intro">La página que buscas cambió de lugar o ya no está disponible. Vuelve al inicio o agenda una conversación con nosotros.</p>
    <div class="ctas"><a href="/" class="btn btn-gold">Volver al inicio</a><a href="/contacto" class="btn btn-line">Contacto</a></div>
  </div>
</section>''', home=True)

# ================= AVISO (pendiente del documento) =================
page('aviso-privacidad.html', 'Aviso de privacidad | PerPHect', 'Aviso de privacidad y política de cookies de PerPHect.',
     head('Legal', 'Aviso de privacidad', 'Tratamiento de datos personales y uso de cookies en perphect.com.', left=True) + '''
<section style="padding-top:72px">
  <div class="wrap legal-doc">
    <div class="meta"><span><b>Responsable:</b> PerPHect</span><span><b>Sitio web:</b> <a href="https://perphect.com/">https://perphect.com/</a></span><span><b>Domicilio:</b> Juan de Acuña 318, Lomas - Virreyes, Lomas de Chapultepec IV Secc, Miguel Hidalgo, 11000, Ciudad de México</span></div>
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
    <p class="lead">Un Consejero PerPHect se pondrá en contacto contigo muy pronto por correo electrónico o WhatsApp para agendar una conversación.</p>
    <div class="ctas"><a href="/" class="btn btn-dark">Volver al inicio</a><a href="/metodologia" class="btn btn-line">Conoce la metodología</a></div>
  </div>
</section>''', noindex=True)

# sitemap
pages = ['index.html', 'servicios.html', 'consejero.html', 'metodologia.html', 'contacto.html', 'aviso-privacidad.html']
open(ROOT + 'sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{url(p)}</loc></url>\n' for p in pages) + '</urlset>\n')
print('ok')
