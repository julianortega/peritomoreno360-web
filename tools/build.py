#!/usr/bin/env python3
"""Genera las páginas HTML de /site a partir de src/pages/*.html y una plantilla común.

Uso:  python3 tools/build.py
Edita el contenido en src/pages/ y la cabecera, el pie o el formulario aquí.
"""
import pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "site"
BODIES = ROOT / "src" / "pages"
SITE = "https://www.peritomoreno360.com"

import json
ORG_LD = '{"@context": "https://schema.org", "@type": "Organization", "name": "Perito Moreno 360", "legalName": "Perito Moreno 360 SL", "taxID": "B-21797493", "url": "https://www.peritomoreno360.com/", "logo": "https://www.peritomoreno360.com/assets/img/pm360-logo.png", "email": "info@peritomoreno360.com", "address": {"@type": "PostalAddress", "streetAddress": "Urb. Las Dalias 9", "postalCode": "39100", "addressLocality": "Bezana", "addressRegion": "Cantabria", "addressCountry": "ES"}, "brand": [{"@type": "Brand", "name": "Bestial Burritos & Tacos"}, {"@type": "Brand", "name": "La Sardinera"}, {"@type": "Brand", "name": "Lolita Bakery"}, {"@type": "Brand", "name": "Rumbo Norte"}, {"@type": "Brand", "name": "Flight Director"}]}'
FD_LD = '{"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "Flight Director", "applicationCategory": "BusinessApplication", "operatingSystem": "Web", "description": "Gestión de locales de hostelería: escandallos, cocina, equipo y turnos, checklists y APPCC, compras y cuenta de resultados en directo.", "url": "https://www.peritomoreno360.com/flight-director", "publisher": {"@type": "Organization", "name": "Perito Moreno 360"}}'

FONTS_BASE = "family=Fraunces:ital,opsz,wght@0,9..144,300..600;1,9..144,300..500&family=Instrument+Sans:wght@400;500;600;700"
FONTS = {
    "base": FONTS_BASE,
    "brands": "family=Anton&" + FONTS_BASE,
    "fd": "family=Caprasimo&family=Noto+Sans:wght@400;600;700&" + FONTS_BASE,
}

MENU_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'

def header(active, has_form=True):
    def a(href, label, key):
        cur = ' aria-current="page"' if key == active else ''
        return f'<a href="{href}"{cur}>{label}</a>'
    return f'''<header class="site-header">
<div class="wrap">
<a class="brand" href="/" aria-label="Perito Moreno 360, inicio"><img src="/assets/img/pm360-logo-transparente.png" alt="Perito Moreno 360" width="137" height="64"></a>
<button class="nav-toggle" type="button" aria-label="Abrir menú" aria-expanded="false" aria-controls="menu">{MENU_ICON}</button>
<nav class="nav" id="menu" aria-label="Principal">
{a("/#grupo", "El grupo", "home")}
{a("/#areas", "Áreas de negocio", "areas")}
{a("/flight-director", "Flight Director", "fd")}
{a("/franquicias", "Franquicias", "franq")}
<a class="btn btn-dark" href="{"#contacto" if has_form else "/#contacto"}">Hablemos</a>
</nav>
</div>
</header>'''

FOOTER = '''<footer class="site-footer">
<div class="wrap">
<div class="foot-top">
<div class="foot-brand">
<b>Perito Moreno 360</b>
<span>Perito Moreno 360 SL · CIF B-21797493</span>
<span>Urb. Las Dalias 9, 39100 Bezana (Cantabria)</span>
<a href="mailto:info@peritomoreno360.com">info@peritomoreno360.com</a>
</div>
<div class="foot-cols">
<div><b>Áreas de negocio</b><a href="/hosteleria">Hostelería</a><a href="/operaciones">Operaciones</a><a href="/mantenimiento">Mantenimiento</a><a href="/apps">Desarrollo de apps</a></div>
<div><b>Más</b><a href="/flight-director">Flight Director</a><a href="/franquicias">Franquicias</a><a href="/#contacto">Contacto</a></div>
<div><b>Legal</b><a href="/aviso-legal">Aviso legal</a><a href="/privacidad">Privacidad</a><a href="/cookies">Cookies</a></div>
</div>
</div>
<div class="foot-bottom">© <span data-year>2026</span> Perito Moreno 360 SL</div>
</div>
</footer>'''

def contact(origen, interes_default, title="¿Hablamos?", intro="Déjanos tus datos y te contactaremos nosotros."):
    options = ["Hostelería", "Franquicias", "Operaciones", "Mantenimiento", "Desarrollo de apps", "Flight Director", "Otro"]
    opts = "\n".join(
        f'<option{" selected" if o == interes_default else ""}>{o}</option>' for o in options
    )
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
<div class="hp" aria-hidden="true"><label for="f-web">No rellenar</label><input id="f-web" name="web" type="text" tabindex="-1" autocomplete="off"></div>
<label class="check"><input type="checkbox" name="acepto" required><span>He leído y acepto la <a href="/privacidad" target="_blank">política de privacidad</a>.</span></label>
<p class="form-note">No hace falta que nos llames: te contactaremos nosotros por teléfono o por correo.</p>
<button class="btn btn-dark" type="submit">Quiero que me contactéis</button>
<p class="form-status" role="status" aria-live="polite"></p>
</div>
<div class="form-done" role="status">
<b>¡Gracias, <span data-name></span>!</b>
<p>Hemos recibido tus datos. Te contactaremos nosotros muy pronto.</p>
</div>
</form>
</div>
</section>'''

def page(slug, title, desc, active, fonts, body, form=None):
    canonical = SITE + ("/" if slug == "index" else "/" + slug)
    form_html = contact(*form) if form else ""
    ld = ""
    if slug == "index": ld = f'<script type="application/ld+json">{ORG_LD}</script>'
    if slug == "flight-director": ld = f'<script type="application/ld+json">{FD_LD}</script>'
    robots = '<meta name="robots" content="noindex">\n' if slug == "404" else ""
    html = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/assets/img/pm360-logo.png">
<meta name="theme-color" content="#F6F2EA">
<link rel="icon" href="/assets/img/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{FONTS[fonts]}&display=swap">
<link rel="stylesheet" href="/assets/css/styles.css">
{ld}
</head>
<body>
{header(active, bool(form))}
<main id="main">
{body}
{form_html}
</main>
{FOOTER}
<script src="/assets/js/main.js" defer></script>
</body>
</html>
'''
    (OUT / f"{slug}.html").write_text(html, encoding="utf-8")
    print("ok", slug)

def body(name):
    return (BODIES / f"{name}.html").read_text(encoding="utf-8")

PAGES = [
    ("index", "Perito Moreno 360 · Grupo empresarial", "Grupo empresarial con marcas de restauración, consultoría de operaciones, mantenimiento y desarrollo de apps a medida.", "home", "base", "index", ("Inicio", "Otro")),
    ("hosteleria", "Hostelería · Perito Moreno 360", "Marcas propias de restauración organizada: Bestial Burritos & Tacos, La Sardinera y Lolita Bakery.", "areas", "brands", "hosteleria", ("Hostelería", "Hostelería")),
    ("operaciones", "Operaciones · Perito Moreno 360", "Estudiamos tu empresa a fondo para hacerla más eficiente: manuales de operaciones, puntos débiles detectados y apoyo mensual.", "areas", "base", "operaciones", ("Operaciones", "Operaciones", "¿Quieres que tu empresa funcione mejor?")),
    ("mantenimiento", "Mantenimiento · Rumbo Norte · Perito Moreno 360", "Mantenimiento preventivo y correctivo de locales e instalaciones con Rumbo Norte, para que tu negocio no pare.", "areas", "base", "mantenimiento", ("Mantenimiento", "Mantenimiento", "Pide presupuesto", "Déjanos tus datos y te contactaremos nosotros para preparar tu presupuesto, gratis y sin compromiso.")),
    ("apps", "Desarrollo de apps · Perito Moreno 360", "Apps web y móviles a medida para empresas, con precios claros: estudio sin coste, módulo de demostración y app completa con precio máximo.", "areas", "base", "apps", ("Desarrollo de apps", "Desarrollo de apps", "¿Tienes una idea para una app?")),
    ("franquicias", "Franquicias · Perito Moreno 360", "Abre una de nuestras marcas con un royalty del 2 % el primer año y del 4 % después, sin subidas.", "franq", "base", "franquicias", ("Franquicias", "Franquicias", "¿Hablamos de tu franquicia?")),
    ("flight-director", "Flight Director · La gestión 360 de tu local de hostelería", "Escandallos, cocina, equipo, checklists, compras y cuenta de resultados en directo para locales de hostelería.", "fd", "fd", "flight-director", ("Flight Director", "Flight Director", "¿Lo probamos en tu local?", "Déjanos tus datos y te contactaremos nosotros para enseñarte Flight Director.")),
    ("aviso-legal", "Aviso legal · Perito Moreno 360", "Aviso legal del sitio web de Perito Moreno 360 SL.", "", "base", "aviso-legal", None),
    ("privacidad", "Política de privacidad · Perito Moreno 360", "Política de privacidad de Perito Moreno 360 SL.", "", "base", "privacidad", None),
    ("cookies", "Política de cookies · Perito Moreno 360", "Política de cookies del sitio web de Perito Moreno 360 SL.", "", "base", "cookies", None),
    ("404", "Página no encontrada · Perito Moreno 360", "La página que buscas no existe.", "", "base", "404", None),
]

for slug, title, desc, active, fonts, b, form in PAGES:
    page(slug, title, desc, active, fonts, body(b), form)
