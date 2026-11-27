#!/usr/bin/env python3
"""Genera las páginas HTML de /site a partir de src/pages/*.html y una plantilla común.

Uso:  python3 tools/build.py
Edita el contenido en src/pages/ y la cabecera, el pie o el formulario aquí.
"""
import pathlib, sys, re, html as _html, datetime, hashlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import en as EN

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "site"
BODIES = ROOT / "src" / "pages"
BODIES_EN = ROOT / "src" / "pages-en"
SITE = "https://www.peritomoreno360.com"

def _ver(rel):
    return hashlib.md5((OUT / rel).read_bytes()).hexdigest()[:10]

import json
ORG_LD = '{"@context": "https://schema.org", "@type": "Organization", "name": "Perito Moreno 360", "legalName": "Perito Moreno 360 SL", "taxID": "B-21797493", "url": "https://www.peritomoreno360.com/", "logo": "https://www.peritomoreno360.com/assets/img/pm360-logo.png", "email": "info@peritomoreno360.com", "address": {"@type": "PostalAddress", "streetAddress": "Urbanización Las Dalias 9", "postalCode": "39100", "addressLocality": "Santa Cruz de Bezana", "addressRegion": "Cantabria", "addressCountry": "ES"}, "brand": [{"@type": "Brand", "name": "Bestial Burritos & Tacos"}, {"@type": "Brand", "name": "La Sardinera"}, {"@type": "Brand", "name": "Lolita Bakery"}, {"@type": "Brand", "name": "Rumbo Norte"}, {"@type": "Brand", "name": "Flight Director"}]}'
MV_LD = '{"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "Mi Vestuario", "applicationCategory": "SportsApplication", "operatingSystem": "Web", "description": "App para clubes de fútbol: convocatorias, calendario, pasar lista, cuotas, ropa, liga y rankings para dirección, entrenadores, jugadores y familias.", "url": "https://www.peritomoreno360.com/mi-vestuario", "offers": {"@type": "Offer", "price": "75", "priceCurrency": "EUR"}, "publisher": {"@type": "Organization", "name": "Perito Moreno 360"}}'
MNT_LD = '{"@context": "https://schema.org", "@type": "Service", "name": "Mantenimiento y reparaciones", "serviceType": "Mantenimiento de edificios, oficinas, comercios, comunidades y restaurantes", "provider": {"@type": "Organization", "name": "Rumbo Norte", "parentOrganization": {"@type": "Organization", "name": "Perito Moreno 360"}}, "url": "https://www.peritomoreno360.com/mantenimiento", "areaServed": {"@type": "City", "name": "Madrid"}}'
FD_LD = '{"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "Flight Director", "applicationCategory": "BusinessApplication", "operatingSystem": "Web", "description": "Gestión de locales de hostelería: escandallos, cocina, equipo y turnos, checklists y APPCC, compras y cuenta de resultados en directo.", "url": "https://www.peritomoreno360.com/flight-director", "publisher": {"@type": "Organization", "name": "Perito Moreno 360"}}'

FONTS_BASE = "family=Inter+Tight:ital,wght@0,500;0,600;0,700;0,800;1,700&family=Inter:wght@400;500;600;700;800"  # las letras de la app Flight Director
FONTS = {
    "base": FONTS_BASE,
    "brands": "family=Anton&" + FONTS_BASE,
    "fd": FONTS_BASE,
}

CARET = '<svg class="caret" viewBox="0 0 12 12" width="12" height="12" aria-hidden="true"><path d="M2.5 4.5 6 8l3.5-3.5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>'
MENU_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'

# Mini-webs de las apps: Flight Director y Mi Vestuario llevan su propia cabecera y menú,
# con un enlace de vuelta al grupo (Julián, 24/11/2026).
PRODUCTOS = {
    "fd": {"home": "/flight-director", "nombre": "Flight Director", "logo": "/assets/img/flightdirector-icono.png",
           "menu": [("/flight-director#modulos", "Funciones"), ("/flight-director/empieza", "Precio"),
                    ("dd", "Guías", [("/app-escandallos-hosteleria", "App de escandallos", "Coste y margen de cada plato"),
                                      ("/control-food-cost-restaurante", "Control del food cost", "Guía paso a paso"),
                                      ("/como-hacer-escandallo", "Cómo hacer un escandallo", "Método y ejemplo completo"),
                                      ("/app-cuadrantes-hosteleria", "Cuadrantes y fichajes", "Turnos y registro de jornada"),
                                      ("/guias", "Todas las guías", "Gestión de restaurantes")])],
           "cta": ("/flight-director/empieza", "Empieza hoy")},
    "club": {"home": "/mi-vestuario", "nombre": "Mi Vestuario", "logo": "/assets/img/club/icono.svg",
             "menu": [("/mi-vestuario#pantallas", "La app"), ("/mi-vestuario#roles", "Para quién"),
                      ("/mi-vestuario#precio", "Precio"), ("/mi-vestuario#preguntas", "Preguntas")],
             "cta": ("/mi-vestuario#contacto", "Pide una demo")},
}

def header_producto(active):
    p = PRODUCTOS[active]
    items = []
    for m in p["menu"]:
        if m[0] == "dd":
            links = "".join(f'<a href="{h}">{t}<small>{d}</small></a>' for h, t, d in m[2])
            items.append(f'<div class="dd"><button class="dd-btn" type="button" aria-expanded="false">{m[1]}{CARET}</button><div class="dd-menu">{links}</div></div>')
        else:
            items.append(f'<a href="{m[0]}">{m[1]}</a>')
    return f'''<header class="site-header prod-header">
<div class="wrap">
<a class="brand prod-brand" href="{p["home"]}" aria-label="{p["nombre"]}, inicio"><img src="{p["logo"]}" alt="" width="40" height="40"><span>{p["nombre"]}<small>de Perito Moreno 360</small></span></a>
<button class="nav-toggle" type="button" aria-label="Abrir menú" aria-expanded="false" aria-controls="menu">{MENU_ICON}</button>
<nav class="nav" id="menu" aria-label="{p["nombre"]}">
{"".join(items)}
<a class="prod-grupo" href="/">Perito Moreno 360</a>
<a class="btn btn-dark" href="{p["cta"][0]}">{p["cta"][1]}</a>
</nav>
</div>
</header>'''

def header(active, has_form=True):
    if active in PRODUCTOS:
        return header_producto(active)
    def a(href, label, key):
        cur = ' aria-current="page"' if key == active else ''
        return f'<a href="{href}"{cur}>{label}</a>'
    return f'''<header class="site-header">
<div class="wrap">
<a class="brand" href="/" aria-label="Perito Moreno 360, inicio"><img src="/assets/img/pm360-logo-transparente.png" alt="Perito Moreno 360" width="137" height="64"></a>
<button class="nav-toggle" type="button" aria-label="Abrir menú" aria-expanded="false" aria-controls="menu">{MENU_ICON}</button>
<nav class="nav" id="menu" aria-label="Principal">
{a("/#grupo", "El grupo", "home")}
<div class="dd{' on' if active in ('areas',) else ''}"><button class="dd-btn" type="button" aria-expanded="false">Áreas de negocio{CARET}</button>
<div class="dd-menu">
<a href="/restauracion">Restauración<small>Bestial, La Sardinera y Lolita Bakery</small></a>
<a href="/operaciones">Operaciones<small>Hacemos tu empresa más eficiente</small></a>
<a href="/mantenimiento">Mantenimiento<small>Rumbo Norte, multiservicios</small></a>
<a href="/apps">Desarrollo de apps<small>Apps a medida para empresas</small></a>
</div></div>
<div class="dd{' on' if active in ('fd','club') else ''}"><button class="dd-btn" type="button" aria-expanded="false">Apps{CARET}</button>
<div class="dd-menu">
<a class="dd-app" href="/flight-director"><img src="/assets/img/flightdirector-icono.png" alt="" width="28" height="28"><span>Flight Director<small>La gestión 360 de tu local de hostelería</small></span></a>
<a class="dd-app" href="/mi-vestuario"><img src="/assets/img/club/icono.svg" alt="" width="28" height="28"><span>Mi Vestuario<small>La app de tu club de fútbol</small></span></a>
</div></div>
<a class="btn btn-dark" href="{"#contacto" if has_form else "/#contacto"}">Hablemos</a>
</nav>
{{LANG}}
</div>
</header>'''

# Redes sociales: pon la URL cuando la tengas; mientras esté vacía se muestra el icono sin enlace.
SOCIAL = [
    ("Instagram", "", '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/>'),
    ("LinkedIn", "", '<rect x="3" y="3" width="18" height="18" rx="3"/><path d="M8 10v7M8 7v.01M12 17v-4a2 2 0 0 1 4 0v4M12 10v7"/>'),
    ("Facebook", "", '<rect x="3" y="3" width="18" height="18" rx="3"/><path d="M15 8h-1.5A2.5 2.5 0 0 0 11 10.5V21M9 13h5"/>'),
]

def _social():
    items = []
    for name, url, path in SOCIAL:
        svg = f'<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{path}</svg>'
        if url:
            items.append(f'<a href="{url}" target="_blank" rel="noopener" aria-label="{name}">{svg}</a>')
        else:
            items.append(f'<span class="soon" title="{name} · próximamente" aria-label="{name} (próximamente)">{svg}</span>')
    return '<div class="foot-social">' + "".join(items) + '</div>'

SOCIAL_HTML = _social()


# Medios de pago aceptados (lo pide Getnet: logotipos de Visa y Mastercard y moneda visibles).
PAGOS = ('<div class="pagos" aria-label="Medios de pago aceptados">'
    '<svg class="pago-logo" viewBox="0 0 64 40" role="img" aria-label="Visa"><rect width="64" height="40" rx="6" fill="#fff"/><text x="32" y="27" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="17" font-weight="900" font-style="italic" fill="#1A1F71">VISA</text></svg>'
    '<svg class="pago-logo" viewBox="0 0 64 40" role="img" aria-label="Mastercard"><rect width="64" height="40" rx="6" fill="#fff"/><circle cx="26" cy="20" r="11" fill="#EB001B"/><circle cx="38" cy="20" r="11" fill="#F79E1B"/><path d="M32 10.8a11 11 0 0 1 0 18.4 11 11 0 0 1 0-18.4z" fill="#FF5F00"/></svg>'
    '<svg class="pago-logo" viewBox="0 0 64 40" role="img" aria-label="Bizum"><rect width="64" height="40" rx="6" fill="#fff"/><text x="32" y="26" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="14" font-weight="700" fill="#05C3DD">bizum</text></svg>'
    '<span>Pago seguro con tarjeta o Bizum · Precios en euros (EUR)</span></div>')

FOOTER = '''<footer class="site-footer">
<div class="wrap">
<div class="foot-top">
<div class="foot-brand">
<b>Perito Moreno 360</b>
<span>Perito Moreno 360 SL · CIF B-21797493</span>
<span>Urbanización Las Dalias 9, 39100 Santa Cruz de Bezana (Cantabria)</span>
<a href="mailto:info@peritomoreno360.com">info@peritomoreno360.com</a>
''' + SOCIAL_HTML + '''
</div>
<div class="foot-cols">
<div><b>Áreas de negocio</b><a href="/restauracion">Restauración</a><a href="/operaciones">Operaciones</a><a href="/mantenimiento">Mantenimiento</a><a href="/apps">Desarrollo de apps</a></div>
<div><b>Franquicias</b><a href="/franquicias">Condiciones</a><a href="/franquicia-burritos">Franquicia de burritos</a><a href="/franquicia-dark-kitchen">Franquicia dark kitchen</a><a href="/franquicias-hosteleria-royalty-bajo">Royalty bajo</a></div>
<div><b>Apps</b><a href="/flight-director">Flight Director</a><a href="/mi-vestuario">Mi Vestuario</a><a href="/app-escandallos-hosteleria">Escandallos</a><a href="/control-food-cost-restaurante">Control del food cost</a><a href="/app-cuadrantes-hosteleria">Cuadrantes y fichajes</a></div>
<div><b>Guías</b><a href="/guias">Todas las guías</a><a href="/como-hacer-escandallo">Escandallos</a><a href="/control-food-cost-restaurante">Food cost</a><a href="/franquicias-hosteleria-royalty-bajo">Royalty de franquicia</a></div>
<div><b>Legal</b><a href="/aviso-legal">Aviso legal</a><a href="/condiciones-contratacion">Condiciones de contratación</a><a href="/condiciones-contratacion#envio">Envío y entrega</a><a href="/condiciones-contratacion#desistimiento">Desistimiento y devoluciones</a><a href="/privacidad">Privacidad</a><a href="/cookies">Cookies</a></div>
</div>
</div>
''' + PAGOS + '''
<div class="foot-bottom">© <span data-year>2026</span> Perito Moreno 360 SL</div>
</div>
</footer>'''

# Preguntas extra del formulario cuando se pide una demo de una app (se envían dentro de «interés»).
DEMO = {
    "Flight Director": ("¿Cuántos locales tienes?", "Por ejemplo, 1"),
    "Mi Vestuario": ("¿Cuántos equipos tiene el club?", "Por ejemplo, 8"),
}

def contact(origen, interes_default, title="¿Hablamos?", intro="Déjanos tus datos y te contactaremos nosotros.", condiciones=False, lang="es"):
    options = ["Restauración", "Franquicias", "Operaciones", "Mantenimiento", "Desarrollo de apps", "Flight Director", "Mi Vestuario", "Trabajar con vosotros", "Otro"]
    opts = "\n".join(
        (f'<option{" selected" if o == interes_default else ""}>{o}</option>' if lang == "es" else
         f'<option value="{o}"{" selected" if o == interes_default else ""}>{EN.OPTIONS[o]}</option>') for o in options
    )
    cond_html = ('<label class="check"><input type="checkbox" name="acepto_condiciones" required><span>He leído y acepto las '
                 '<a href="/condiciones-contratacion" target="_blank">condiciones de contratación</a>, incluidas las políticas de entrega, '
                 '<a href="/condiciones-contratacion#desistimiento" target="_blank">desistimiento</a> y '
                 '<a href="/condiciones-contratacion#devoluciones" target="_blank">devoluciones</a>.</span></label>') if condiciones else ""
    demo = DEMO.get(interes_default)
    demo_html = ""
    if demo:
        demo_html = (f'<div class="field"><label for="f-tamano">{demo[0]}</label><input id="f-tamano" name="tamano" type="text" inputmode="numeric" maxlength="20" placeholder="{demo[1]}"></div>\n'
                     '<div class="field"><label for="f-cuando">¿Cuándo te viene mejor la demo?</label><select id="f-cuando" name="cuando">'
                     '<option>Me da igual</option><option>Por la mañana</option><option>Por la tarde</option></select></div>\n')
    boton = "Quiero mi demo" if demo else "Quiero que me contactéis"
    gracias = ("Hemos recibido tu petición. Te escribimos en menos de 24 horas laborables para cerrar el día y la hora de la demo." if demo
               else "Hemos recibido tus datos. Te contactaremos nosotros muy pronto.")
    return f'''<section id="contacto" class="wrap section-tight">
<div class="contact-box">
<div class="stack-s">
<h2>{title}</h2>
<p class="intro">{intro}</p>
<p class="intro">Si lo prefieres, escríbenos a <a class="mail" href="mailto:info@peritomoreno360.com">info@peritomoreno360.com</a></p>
</div>
<form class="form" data-contact data-origen="{origen}" novalidate>
<div class="form-fields stack-s">
<div class="field"><label for="f-nombre">Nombre</label><input id="f-nombre" name="nombre" type="text" autocomplete="name" required maxlength="120"></div>
<div class="field"><label for="f-email">Correo electrónico</label><input id="f-email" name="email" type="email" autocomplete="email" required maxlength="160"></div>
<div class="field"><label for="f-tel">Teléfono</label><input id="f-tel" name="telefono" type="tel" autocomplete="tel" inputmode="tel" required pattern="[+0-9 ()\\-]{{6,}}" maxlength="40"></div>
<div class="field"><label for="f-interes">Te interesa</label><select id="f-interes" name="interes">
{opts}
</select></div>
{demo_html}<div class="hp" aria-hidden="true"><label for="f-web">No rellenar</label><input id="f-web" name="web" type="text" tabindex="-1" autocomplete="off"></div>
<label class="check"><input type="checkbox" name="acepto" required><span>He leído y acepto la <a href="/privacidad" target="_blank">política de privacidad</a>.</span></label>{cond_html}
<p class="form-note">No hace falta que nos llames: te contactaremos nosotros por teléfono o por correo.</p>
<button class="btn btn-dark" type="submit">{boton}</button>
<p class="form-status" role="status" aria-live="polite"></p>
</div>
<div class="form-done" role="status">
<b>¡Gracias, <span data-name></span>!</b>
<p>{gracias}</p>
</div>
</form>
</div>
</section>'''

def faq_ld(body):
    items = re.findall(r"<details><summary>(.*?)</summary><p>(.*?)</p></details>", body, re.S)
    if not items:
        return ""
    strip = lambda t: _html.unescape(re.sub(r"<[^>]+>", "", t)).strip()
    data = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in items]}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + '</script>'

def path_es(slug):
    return "/" if slug == "index" else "/" + slug

def path_en(slug):
    return "/en" if slug == "index" else "/en/" + slug

def tr_chrome(s):
    for es, en in EN.CHROME:
        s = s.replace(es, en)
    return s

def en_links(s):
    """En las páginas en inglés, los enlaces internos apuntan a /en/…"""
    def f(m):
        path, frag = m.group(1), m.group(2) or ""
        if path == "":
            return f'href="/en{frag}"'
        if path in EN.PAGES and path != "404":
            return f'href="/en/{path}{frag}"'
        return m.group(0)
    return re.sub(r'href="/([A-Za-z0-9/-]*)(#[^"]*)?"(?! lang="es")', f, s)  # lang="es": enlace a la versión en español

def lang_switch(slug, lang):
    def item(code, label, href, flag, name):
        cur = ' aria-current="true"' if code == lang else ''
        return f'<a href="{href}" hreflang="{code}" lang="{code}"{cur} title="{name}">{flag}<span>{label}</span></a>'
    aria = "Idioma" if lang == "es" else "Language"
    return (f'<div class="lang" role="group" aria-label="{aria}">'
            + item("es", "ES", path_es(slug), EN.FLAG_ES, "Español")
            + item("en", "EN", path_en(slug) if slug in EN.PAGES else path_en("index"), EN.FLAG_EN, "English") + '</div>')

def page(slug, title, desc, active, fonts, body, form=None, lang="es"):
    canonical = SITE + (path_es(slug) if lang == "es" else path_en(slug))
    form_html = contact(*form, lang=lang) if form else ""
    ld = ""
    if slug == "index": ld = f'<script type="application/ld+json">{ORG_LD}</script>'
    if slug == "flight-director": ld = f'<script type="application/ld+json">{FD_LD if lang == "es" else FD_LD.replace(json.loads(FD_LD)["description"], EN.FD_DESC).replace("/flight-director", "/en/flight-director")}</script>'
    if slug == "mi-vestuario": ld = f'<script type="application/ld+json">{MV_LD}</script>'
    if slug == "mantenimiento": ld = f'<script type="application/ld+json">{MNT_LD}</script>'
    ld += faq_ld(body)
    robots = '<meta name="robots" content="noindex">\n' if slug == "404" else ""
    alternates = "" if (slug == "404" or slug not in EN.PAGES) else (f'<link rel="alternate" hreflang="es" href="{SITE}{path_es(slug)}">\n'
        f'<link rel="alternate" hreflang="en" href="{SITE}{path_en(slug)}">\n'
        f'<link rel="alternate" hreflang="x-default" href="{SITE}{path_es(slug)}">')
    head = header(active, bool(form))
    foot = FOOTER
    if lang == "en":
        head, foot, form_html = (en_links(tr_chrome(x)) for x in (head, foot, form_html))
        body = en_links(body)
    head = head.replace("{LANG}", lang_switch(slug, lang))
    html = f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}
<link rel="canonical" href="{canonical}">
{alternates}
<meta property="og:type" content="website">
<meta property="og:locale" content="{"es_ES" if lang == "es" else "en_GB"}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/assets/img/pm360-logo.png">
<meta name="theme-color" content="#F6F2EA">
<meta name="google-site-verification" content="K6yYI_6NLHTueWK6bNe2ToRdarshQfltA1QFdewTcZE">
<link rel="icon" href="/assets/img/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{FONTS[fonts]}&display=swap">
<link rel="stylesheet" href="/assets/css/styles.css?v={_ver("assets/css/styles.css")}">
{ld}
<script defer src="/_vercel/insights/script.js"></script>
</head>
<body>
{head}
<main id="main">
{body}
{form_html}
</main>
{foot}
<script src="/assets/js/main.js?v={_ver("assets/js/main.js")}" defer></script>
</body>
</html>
'''
    rel = f"{slug}.html" if lang == "es" else ("en.html" if slug == "index" else f"en/{slug}.html")
    (OUT / rel).parent.mkdir(parents=True, exist_ok=True)
    (OUT / rel).write_text(html, encoding="utf-8")
    print("ok", lang, slug)

def body(name, lang="es"):
    src = BODIES if lang == "es" else BODIES_EN
    return (src / f"{name}.html").read_text(encoding="utf-8").replace("{{PAGOS}}", PAGOS if lang == "es" else tr_chrome(PAGOS))

PAGES = [
    ("index", "Perito Moreno 360 · Grupo empresarial", "Grupo empresarial con marcas de restauración, consultoría de operaciones, mantenimiento y desarrollo de apps a medida.", "home", "base", "index", ("Inicio", "Otro")),
    ("restauracion", "Marcas de restauración: Bestial, La Sardinera y Lolita · PM360", "Marcas propias de restauración organizada: Bestial Burritos & Tacos, La Sardinera y Lolita Bakery.", "areas", "brands", "restauracion", ("Restauración", "Restauración")),
    ("operaciones", "Consultoría de operaciones para empresas · Perito Moreno 360", "Estudiamos tu empresa a fondo para hacerla más eficiente: manuales de operaciones, puntos débiles detectados y apoyo mensual.", "areas", "base", "operaciones", ("Operaciones", "Operaciones", "¿Quieres que tu empresa funcione mejor?")),
    ("mantenimiento", "Mantenimiento de locales y comunidades en Madrid · Rumbo Norte", "Mantenimiento y reparaciones en Madrid para edificios, oficinas, comercios, comunidades y restaurantes: electricidad, fontanería y más. Presupuesto gratis.", "areas", "base", "mantenimiento", ("Mantenimiento", "Mantenimiento", "Pide presupuesto", "Déjanos tus datos y te contactaremos nosotros para preparar tu presupuesto, gratis y sin compromiso.")),
    ("apps", "Desarrollo de apps a medida para empresas · Perito Moreno 360", "Apps web y móviles a medida para empresas, con precios claros: estudio sin coste, módulo de demostración y app completa con precio máximo.", "areas", "base", "apps", ("Desarrollo de apps", "Desarrollo de apps", "¿Tienes una idea para una app?", "Déjanos tus datos y te contactaremos nosotros.", True)),
    ("franquicias", "Franquicias · Perito Moreno 360", "Abre una de nuestras marcas con un royalty del 2 % el primer año y del 4 % después, sin subidas.", "areas", "base", "franquicias", ("Franquicias", "Franquicias", "¿Hablamos de tu franquicia?")),
    ("flight-director", "Flight Director · La gestión 360 de tu local de hostelería", "Escandallos, cocina, equipo, checklists, compras y cuenta de resultados en directo para locales de hostelería.", "fd", "fd", "flight-director", ("Flight Director", "Flight Director", "Pide una demo de Flight Director", "Déjanos tus datos y te enseñamos Flight Director en 30 minutos por videollamada, con tus propios platos. Si prefieres empezar ya, <a href=\"/flight-director/empieza\">date de alta aquí</a>.")),
    ("flight-director/empieza", "Empieza hoy con Flight Director · Date de alta · Perito Moreno 360", "Date de alta en Flight Director en dos minutos: 75 €/mes por local, todo incluido. Sin permanencia. Paga con tarjeta o Bizum.", "fd", "fd", "empieza", None),
    ("mi-vestuario", "Mi Vestuario · La app de tu club de fútbol · Perito Moreno 360", "Convocatorias, calendario, pasar lista, cuotas, ropa, liga y rankings de tu club de fútbol en una sola app para dirección, entrenadores, jugadores y familias.", "club", "base", "mi-vestuario", ("Mi Vestuario", "Mi Vestuario", "Pide una demo de Mi Vestuario", "Déjanos tus datos y te enseñamos Mi Vestuario en 30 minutos por videollamada, con los equipos de tu club.")),
    ("franquicia-burritos", "Franquicia de burritos y tacos · Bestial Burritos & Tacos", "Abre una franquicia de burritos y tacos Bestial: fast casual mexicano 100 % natural, en formato dark kitchen, local o flagship. Royalty del 2 % el primer año.", "areas", "base", "franquicia-burritos", ("Franquicia de burritos", "Franquicias", "¿Abrimos un Bestial en tu ciudad?")),
    ("franquicia-dark-kitchen", "Franquicia dark kitchen de burritos · Poca inversión · Bestial", "Franquicia dark kitchen: empieza solo con delivery en 15–50 m², valida tu zona con poca inversión y crece a local. Royalty del 2 % el primer año.", "areas", "base", "franquicia-dark-kitchen", ("Franquicia dark kitchen", "Franquicias", "¿Hablamos de tu dark kitchen?")),
    ("franquicias-hosteleria-royalty-bajo", "Franquicias de hostelería con royalty bajo: 2 % y 4 %", "Franquicias de hostelería con uno de los royalties más bajos: 2 % el primer año y 4 % después, fijo y sin subidas. Condiciones claras y sin letra pequeña.", "areas", "brands", "franquicias-hosteleria-royalty-bajo", ("Royalty bajo", "Franquicias", "¿Hablamos de tu franquicia?")),
    ("app-escandallos-hosteleria", "App de escandallos para hostelería · Flight Director", "Escandallos que se recalculan solos: coste por ración, food cost y margen en sala y en delivery, con la comisión de la plataforma.", "fd", "fd", "app-escandallos-hosteleria", ("App de escandallos", "Flight Director", "¿Te enseñamos tus escandallos en Flight Director?", "Déjanos tus datos y te contactaremos nosotros para hacerte una demo.")),
    ("control-food-cost-restaurante", "Cómo calcular y controlar el food cost de un restaurante · Guía", "Qué es el food cost, cómo se calcula con un ejemplo, qué porcentaje es bueno y 7 formas de controlarlo en tu restaurante.", "fd", "fd", "control-food-cost-restaurante", ("Guía food cost", "Flight Director", "¿Quieres controlar tu food cost sin Excel?", "Déjanos tus datos y te enseñamos cómo lo hace Flight Director.")),
    ("como-hacer-escandallo", "Cómo hacer un escandallo paso a paso, con ejemplo · Guía", "Qué es un escandallo, cómo calcular el coste por ración con la merma, un ejemplo completo y los errores más habituales en sala y delivery.", "fd", "fd", "como-hacer-escandallo", ("Guía escandallo", "Flight Director", "¿Quieres tus escandallos sin Excel?", "Déjanos tus datos y te enseñamos cómo lo hace Flight Director.")),
    ("guias", "Guías de gestión para restaurantes · Perito Moreno 360", "Guías prácticas para gestionar un restaurante: escandallos, food cost, cuadrantes de personal y franquicias, escritas desde nuestros propios locales.", "fd", "fd", "guias", None),
    ("app-cuadrantes-hosteleria", "App de cuadrantes y fichajes para hostelería · Flight Director", "Cuadrantes de turnos según la venta prevista, coste de personal antes de publicar y fichajes para el registro de jornada. App para restaurantes.", "fd", "fd", "app-cuadrantes-hosteleria", ("App de cuadrantes", "Flight Director", "¿Te enseñamos tus cuadrantes en Flight Director?", "Déjanos tus datos y te contactaremos nosotros para hacerte una demo.")),
    ("aviso-legal", "Aviso legal · Perito Moreno 360", "Aviso legal del sitio web de Perito Moreno 360 SL.", "", "base", "aviso-legal", None),
    ("condiciones-contratacion", "Condiciones de contratación · Perito Moreno 360", "Condiciones de contratación de los servicios de Perito Moreno 360 SL: precios, forma de pago, plazos, desistimiento y devoluciones.", "", "base", "condiciones-contratacion", None),
    ("privacidad", "Política de privacidad · Perito Moreno 360", "Política de privacidad de Perito Moreno 360 SL.", "", "base", "privacidad", None),
    ("cookies", "Política de cookies · Perito Moreno 360", "Política de cookies del sitio web de Perito Moreno 360 SL.", "", "base", "cookies", None),
    ("404", "Página no encontrada · Perito Moreno 360", "La página que buscas no existe.", "", "base", "404", None),
]

SLUGS = {slug for slug, *_ in PAGES}
assert set(EN.PAGES) <= SLUGS, set(EN.PAGES) - SLUGS  # páginas solo en español (guías): sin versión /en

for slug, title, desc, active, fonts, b, form in PAGES:
    page(slug, title, desc, active, fonts, body(b), form)
    if slug not in EN.PAGES:
        continue
    t_en, d_en, f_en = EN.PAGES[slug]
    page(slug, t_en, d_en, active, fonts, body(b, "en"), f_en, "en")

# Sitemap y robots
PRIORITY = {"index": "1.0", "franquicias": "0.9", "flight-director": "0.9", "flight-director/empieza": "0.9", "aviso-legal": "0.2", "privacidad": "0.2", "cookies": "0.2"}
today = datetime.date.today().isoformat()
urls = []
for slug, *_ in PAGES:
    if slug == "404":
        continue
    has_en = slug in EN.PAGES
    alt = (f'<xhtml:link rel="alternate" hreflang="es" href="{SITE}{path_es(slug)}"/>'
           f'<xhtml:link rel="alternate" hreflang="en" href="{SITE}{path_en(slug)}"/>') if has_en else ""
    for loc in ((SITE + path_es(slug), SITE + path_en(slug)) if has_en else (SITE + path_es(slug),)):
        urls.append(f"  <url><loc>{loc}</loc>{alt}<lastmod>{today}</lastmod><priority>{PRIORITY.get(slug, '0.8')}</priority></url>")
(OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(urls) + "\n</urlset>\n", encoding="utf-8")
(OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
print("ok sitemap", len(urls))
