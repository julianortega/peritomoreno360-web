#!/usr/bin/env python3
"""Genera la web de La Sardinera en sardinera/site a partir de sardinera/src/pages.

Uso:  python3 sardinera/tools/build.py

Misma idea que la web de Bestial: el contenido de cada página está en src/pages y aquí se le pone
cabecera, pie, carta y datos para Google. Para cambiar dominio, teléfono, horario o datos legales,
toca solo el bloque CONFIG y vuelve a ejecutar.
"""
import json, pathlib, re, hashlib, html as _html
from carta import CARTA

# ============================== CONFIG ==============================
MARCA = "La Sardinera"
LEMA = "Del norte a la mesa"
DOMINIO = ""                            # p. ej. "https://www.lasardinera.es" (vacío mientras no haya dominio)
EMAIL = ""                              # correo de contacto público; vacío = se contacta por teléfono
TELEFONO = "619 91 59 18"               # provisional hasta tener el del local
INSTAGRAM = "https://www.instagram.com/lasardinera_sdr/"
GRUPO_URL = "https://www.peritomoreno360.com"
# Empresa que opera el local de Majadahonda y vende (aviso legal y pie). La marca es de Perito Moreno 360 S.L.
TITULAR = "Simbasona S.L."
CIF = "B05816426"
DOMICILIO = "Calle Zuloaga 14, 3º D, 28222 Majadahonda (Madrid)"
APERTURA = "2026-12-03"                 # día de apertura (para el aviso y para Google)
APERTURA_TXT = "3 de diciembre"
# Horario por días para Google y para la web. Vacío = «Horario muy pronto».
# Formato: [("Mo","Su","08:00","23:00")] (días de schema.org: Mo Tu We Th Fr Sa Su)
HORARIO = []
LOCAL = {
    "nombre": "Majadahonda",
    "slug": "majadahonda",
    "calle": "Avenida de los Reyes Católicos, 8",
    "cp": "28220",
    "localidad": "Majadahonda",
    "zona": "Majadahonda",
    "texto": ("Nuestra primera Sardinera en Madrid, en la avenida de los Reyes Católicos. Barra de pinchos con la tortilla "
              "de Santander, gildas, conservas del Cantábrico y caña bien tirada, del desayuno a la cena. "
              "También para llevar: tortillas enteras por encargo."),
}
PRECIO = "€€"
# ====================================================================

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "site"
SRC = ROOT / "src" / "pages"
FONTS = "https://fonts.googleapis.com/css2?family=Amarante&family=Poppins:wght@300;400;500;600;700&display=swap"
DIAS = {"Mo": "lunes", "Tu": "martes", "We": "miércoles", "Th": "jueves", "Fr": "viernes", "Sa": "sábado", "Su": "domingo"}
ORDEN = list(DIAS)
DAYS_EN = "Monday Tuesday Wednesday Thursday Friday Saturday Sunday".split()

e = _html.escape

def eur(x):
    return f"{x:.2f}".replace(".", ",") + " €"

def ver(rel):
    return hashlib.md5((OUT / rel).read_bytes()).hexdigest()[:10]

def dir_completa():
    return f'{LOCAL["calle"]}, {LOCAL["cp"]} {LOCAL["localidad"]}'

def maps_q():
    return (dir_completa() + ", Madrid").replace(" ", "+")

def tel_href():
    return "tel:+34" + TELEFONO.replace(" ", "")

def contacto_href():
    return f"mailto:{EMAIL}" if EMAIL else tel_href()

def contacto_txt():
    return f'<a href="mailto:{EMAIL}">{EMAIL}</a> o en el {e(TELEFONO)}' if EMAIL else f'el teléfono <a href="{tel_href()}">{e(TELEFONO)}</a>'

def horario_txt():
    if not HORARIO:
        return f"Abrimos el {APERTURA_TXT}. Horario muy pronto."
    out = []
    for a, b, h1, h2 in HORARIO:
        dias = DIAS[a] if a == b else f"{DIAS[a]} a {DIAS[b]}"
        out.append(f"{dias.capitalize()}: {h1}–{h2}")
    return " · ".join(out)

ICON = {
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "ig": '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/>',
}
def svg(name, size=20):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[name]}</svg>'

def brand(dark=True):
    return f'<img src="/assets/img/logo-{"azul" if dark else "blanco"}.png" alt="{e(MARCA)}" width="173" height="30">'

def header(active):
    def a(href, label, key):
        cur = ' aria-current="page"' if key == active else ""
        return f'<a href="{href}"{cur}>{label}</a>'
    return f'''<div class="topbar">Abrimos en Majadahonda el {APERTURA_TXT}. <a href="/locales/{LOCAL["slug"]}">Dónde estamos →</a></div>
<header class="site-header">
<div class="wrap">
<a class="brand" href="/" aria-label="{e(MARCA)}, inicio">{brand()}</a>
<button class="nav-toggle" type="button" aria-label="Abrir menú" aria-expanded="false" aria-controls="menu">{svg("menu", 28)}</button>
<nav class="nav" id="menu" aria-label="Principal">
{a("/carta", "Carta", "carta")}
{a("/locales/" + LOCAL["slug"], "Majadahonda", "local")}
{a("/encargos", "Para llevar", "encargos")}
{a("/nosotros", "Del norte", "nosotros")}
{a("/franquicias", "Franquicias", "franquicias")}
<div class="nav-actions"><a class="btn btn-blue" href="/carta">Ver la carta</a></div>
</nav>
</div>
</header>'''

def footer():
    ig = f'<a href="{INSTAGRAM}" target="_blank" rel="noopener" aria-label="Instagram de {e(MARCA)}">{svg("ig")}</a>' if INSTAGRAM else ""
    return f'''<footer class="site-footer">
<div class="wrap">
<div class="foot-top">
<div class="foot-brand">
<a href="/" aria-label="Inicio">{brand(False)}</a>
<p class="lema">{e(LEMA)}</p>
<p>{e(dir_completa())}<br><a href="{tel_href()}">{e(TELEFONO)}</a></p>
<div class="social">{ig}</div>
</div>
<div class="foot-cols">
<div><b>Comer</b><a href="/carta">Carta</a><a href="/locales/{LOCAL["slug"]}">Majadahonda</a><a href="/encargos">Para llevar y encargos</a></div>
<div><b>{e(MARCA)}</b><a href="/nosotros">Del norte</a><a href="/franquicias">Franquicias</a><a href="{contacto_href()}">Contacto</a></div>
<div><b>Legal</b><a href="/aviso-legal">Aviso legal</a><a href="/privacidad">Privacidad</a><a href="/cookies">Cookies</a></div>
</div>
</div>
<div class="foot-bottom"><span>© <span data-year>2026</span> {e(MARCA)} · {e(TITULAR)} · {CIF}</span><a href="{GRUPO_URL}" target="_blank" rel="noopener">Una marca de Perito Moreno 360</a></div>
</div>
</footer>'''

NOINDEX = {"404"}

def page(name, body, title, desc, active):
    path = "" if name == "index" else name
    canon = f'<link rel="canonical" href="{DOMINIO}/{path}">\n<meta property="og:url" content="{DOMINIO}/{path}">\n<meta property="og:image" content="{DOMINIO}/assets/img/og.jpg">\n' if DOMINIO else ""
    robots = '<meta name="robots" content="noindex">\n' if name in NOINDEX else ""
    return f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{canon}<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_ES">
<meta property="og:site_name" content="{e(MARCA)}">
<meta name="twitter:card" content="summary_large_image">
{robots}<meta name="theme-color" content="#0D4765">
<link rel="icon" href="/assets/img/favicon.png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="/assets/css/sardinera.css?v={ver("assets/css/sardinera.css")}">
{ld_script(jsonld(name))}</head>
<body>
<a class="sr" href="#main">Saltar al contenido</a>
{header(active)}
<main id="main">
{body}
</main>
{footer()}
<script src="/assets/js/sardinera.js?v={ver("assets/js/sardinera.js")}" defer></script>
</body>
</html>
'''

# ---------- carta ----------
def carta_html():
    out = []
    for sid, title, sub, grupos in CARTA:
        gs = []
        for gname, items in grupos:
            rows = "".join(
                f'<li><div><h4>{e(n)}</h4>{f"<p>{e(d)}</p>" if d else ""}</div><span class="p">{eur(p)}</span></li>' for n, d, p in items)
            h = f'<h3>{e(gname)}</h3>' if gname else ""
            gs.append(f'<div class="grp">{h}<ul>{rows}</ul></div>')
        s = f'<p class="sub">{e(sub)}</p>' if sub else ""
        out.append(f'<section id="{sid}" class="menu-sec"><div class="menu-head"><h2 class="display">{e(title)}</h2>{s}</div><div class="grps">{"".join(gs)}</div></section>')
    return "\n".join(out)

def subnav():
    return '<nav class="subnav" aria-label="Secciones de la carta"><div class="wrap">' + "".join(
        f'<a href="#{sid}">{e(t)}</a>' for sid, t, _, _ in CARTA) + '</div></nav>'

def destacados():
    """Lo más nuestro, para la portada (nombres exactos de la carta)."""
    want = ["Tortilla con cebolla", "Gilda de anchoa", "Sardinera", "Ración de anchoas", "Ventresca con mantequilla", "Coca de sardinas con queso feta", "Vermut rojo de grifo"]
    idx = {n: p for _, _, _, gs in CARTA for _, its in gs for n, _d, p in its}
    return "".join(f'<li><span>{e(n)}</span><i></i><b>{eur(idx[n])}</b></li>' for n in want if n in idx)

# ---------- datos estructurados (schema.org) ----------
def url(p=""):
    return f"{DOMINIO}/{p}"

def org():
    o = {"@type": "Organization", "@id": url("#marca"), "name": MARCA, "url": url(), "logo": url("assets/img/icon-512.png"),
         "slogan": LEMA, "parentOrganization": {"@type": "Organization", "name": "Perito Moreno 360", "url": GRUPO_URL}}
    if INSTAGRAM:
        o["sameAs"] = [INSTAGRAM]
    return o

def restaurante():
    r = {"@type": "Restaurant", "@id": url(f'locales/{LOCAL["slug"]}#local'), "name": f'{MARCA} {LOCAL["nombre"]}',
         "url": url(f'locales/{LOCAL["slug"]}'), "image": url("assets/img/og.jpg"), "telephone": "+34 " + TELEFONO,
         "servesCuisine": ["Española", "Tapas", "Cántabra"], "priceRange": PRECIO,
         "address": {"@type": "PostalAddress", "streetAddress": LOCAL["calle"], "postalCode": LOCAL["cp"],
                     "addressLocality": LOCAL["localidad"], "addressRegion": "Comunidad de Madrid", "addressCountry": "ES"},
         "areaServed": LOCAL["zona"], "hasMenu": url("carta"), "acceptsReservations": False, "brand": {"@id": url("#marca")},
         "foundingDate": APERTURA}
    if HORARIO:
        r["openingHoursSpecification"] = [{"@type": "OpeningHoursSpecification",
            "dayOfWeek": [f"https://schema.org/{d}" for d in DAYS_EN[ORDEN.index(a):ORDEN.index(b) + 1]],
            "opens": h1, "closes": h2} for a, b, h1, h2 in HORARIO]
    return r

def carta_ld():
    secs = [{"@type": "MenuSection", "name": t, "hasMenuItem": [
        {"@type": "MenuItem", "name": n, **({"description": d} if d else {}),
         "offers": {"@type": "Offer", "price": f"{p:.2f}", "priceCurrency": "EUR"}} for _, its in gs for n, d, p in its]}
        for _, t, _, gs in CARTA]
    return {"@type": "Menu", "@id": url("carta#menu"), "name": f"Carta de {MARCA}", "url": url("carta"), "inLanguage": "es", "hasMenuSection": secs}

def migas(*pares):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": url(p)} for i, (n, p) in enumerate(pares)]}

def jsonld(name):
    g = []
    if name == "index":
        g = [{"@type": "WebSite", "@id": url("#web"), "name": MARCA, "url": url(), "inLanguage": "es"}, org(), restaurante()]
    elif name == "carta":
        g = [carta_ld(), migas(("Inicio", ""), ("Carta", "carta"))]
    elif name == f'locales/{LOCAL["slug"]}':
        g = [restaurante(), migas(("Inicio", ""), (LOCAL["nombre"], name))]
    elif name in ("encargos", "nosotros", "franquicias"):
        g = [migas(("Inicio", ""), (PAGES[name][0].split(" · ")[0], name))]
    return {"@context": "https://schema.org", "@graph": g} if g else None

def ld_script(obj):
    if not obj:
        return ""
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False).replace("</", "<\\/") + '</script>\n'

def tokens(s):
    rep = {
        "MARCA": e(MARCA), "LEMA": e(LEMA), "TELEFONO": e(TELEFONO), "TEL_HREF": tel_href(),
        "CONTACTO_HREF": contacto_href(), "CONTACTO": contacto_txt(),
        "TITULAR": e(TITULAR), "CIF": CIF, "DOMICILIO": e(DOMICILIO), "GRUPO_URL": GRUPO_URL,
        "CARTA": carta_html(), "SUBNAV": subnav(), "DESTACADOS": destacados(),
        "DIRECCION": e(dir_completa()), "MAPS_Q": maps_q(), "HORARIO": e(horario_txt()),
        "APERTURA_TXT": APERTURA_TXT, "LOCAL_TEXTO": e(LOCAL["texto"]), "LOCAL_SLUG": LOCAL["slug"],
        "DOMINIO_O_WEB": DOMINIO.replace("https://", "") if DOMINIO else "esta web", "INSTAGRAM": INSTAGRAM,
    }
    return re.sub(r"\{\{([A-Z_]+)\}\}", lambda mo: rep[mo.group(1)], s)

PAGES = {
    # nombre (= ruta; el fichero es src/pages/<nombre>.html, con «locales/x» como «local-x»): (título, descripción, activo)
    "index": (f"{MARCA} · Tortilla de Santander, gildas y conservas en Majadahonda",
              f"{MARCA}: un poco de norte en Majadahonda. Pinchos de tortilla de Santander, gildas, anchoas y conservas del Cantábrico, vermut y caña. Abrimos el {APERTURA_TXT}.", "home"),
    "carta": (f"Carta · {MARCA} Majadahonda", "La carta de La Sardinera: tortilla de Santander, gildas, anchoas, conservas del Cantábrico, raciones, desayunos, vermut y vinos, con precios.", "carta"),
    f'locales/{LOCAL["slug"]}': (f"Bar de pinchos y tortilla en Majadahonda · {MARCA}",
              f"{MARCA} Majadahonda, en {LOCAL['calle']}: pinchos de tortilla, gildas, conservas y raciones del norte. Dirección, horario y teléfono.", "local"),
    "encargos": (f"Tortilla de Santander para llevar · {MARCA}", "Tortilla entera por encargo, pinchos y conservas para llevar desde nuestro local de Majadahonda.", "encargos"),
    "nosotros": (f"Del norte a la mesa · {MARCA}", "Qué es La Sardinera: la barra de pinchos de Santander, con tortilla poco hecha, gildas y conservas del Cantábrico.", "nosotros"),
    "franquicias": (f"Franquicias · {MARCA}", "Abre una Sardinera: un concepto de barra del norte, pequeño y muy afinado, del Grupo Perito Moreno 360.", "franquicias"),
    "aviso-legal": (f"Aviso legal · {MARCA}", "Aviso legal.", ""),
    "privacidad": (f"Privacidad · {MARCA}", "Política de privacidad.", ""),
    "cookies": (f"Cookies · {MARCA}", "Política de cookies.", ""),
    "404": (f"Página no encontrada · {MARCA}", "Esta página no existe.", ""),
}

def main():
    for name, (title, desc, active) in PAGES.items():
        src = SRC / (name.replace("locales/", "local-") + ".html")
        body = tokens(src.read_text())
        dest = OUT / f"{name}.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(page(name, body, title, desc, active))
    pub = ("index", "carta", f'locales/{LOCAL["slug"]}', "encargos", "nosotros", "franquicias")
    if DOMINIO:
        urls = "".join(f"<url><loc>{DOMINIO}/{'' if n == 'index' else n}</loc></url>" for n in pub)
        (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
        (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {DOMINIO}/sitemap.xml\n")
    else:
        (OUT / "robots.txt").write_text("User-agent: *\nAllow: /\n")
        sm = OUT / "sitemap.xml"
        if sm.exists():
            sm.unlink()
    print(f"ok · {len(PAGES)} páginas · {sum(len(i) for *_, gs in CARTA for _, i in gs)} platos · dominio {DOMINIO or '(sin dominio)'}")

if __name__ == "__main__":
    main()
