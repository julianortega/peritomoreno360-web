#!/usr/bin/env python3
"""Genera la web de la marca de burritos en bestial/site a partir de bestial/src/pages.

Uso:  python3 bestial/tools/build.py

Para cambiar el NOMBRE de la marca o el DOMINIO, toca solo el bloque CONFIG de abajo y vuelve a
ejecutar este script. En el contenido, {{MARCA}} y {M} se sustituyen por el nombre.
"""
import json, pathlib, re, hashlib, html as _html
from carta import calc_data, shop_data, PRODUCTS

# ============================== CONFIG ==============================
MARCA = "Bestial"                       # nombre corto: logo de texto, títulos, «Los Bestiales», «Dúo Bestial»…
MARCA_COMPLETA = "Bestial Burritos & Tacos"
CIUDAD = "Madrid"
DOMINIO = ""                            # p. ej. "https://www.bestialburritos.com" (vacío mientras no haya dominio)
LOGO = "logo"                           # "logo" usa assets/img/logo-negro.png y logo-blanco.png; "" usa el nombre en texto
EMAIL = "[correo]"                      # p. ej. "hola@bestialburritos.com"
INSTAGRAM = ""                          # URL completa; vacío = icono sin enlace
TIKTOK = ""
TITULAR = "[Razón social]"             # empresa que opera la web (aviso legal y pie)
CIF = "[CIF]"
DOMICILIO = "[Domicilio]"
GRUPO_URL = "https://www.peritomoreno360.com"
APPS_DELIVERY = ["Uber Eats", "[Glovo]", "[Just Eat]"]
PEDIDOS_ONLINE = False                  # False = cartel «muy pronto» en Pide online y Pago (el montador se puede usar igual)
# Locales (de Flight Director). Horarios pendientes. Tipo: "local", "cocina" (solo reparto) o "pronto" (en obras).
LOCALES = [
    ("Melancólicos", "Paseo de los Melancólicos, 7 · Madrid", "[Horario]", "cocina"),
    ("Manuel Becerra", "Calle Vizconde de Matamala, 7 · Madrid", "[Horario]", "local"),
    ("Majadahonda", "Av. Reyes Católicos, 8 · Majadahonda", "Abrimos muy pronto", "pronto"),
    ("San Germán", "Calle San Germán, 11 · Madrid", "Abrimos muy pronto", "pronto"),
]
# Club de clientes (fidelización). Las altas y los sellos los gestiona Flight Director (Club → Ajustes);
# copia aquí los mismos premios. Para otra marca: cambia nombre, enlace (…/unete/<slug>) y premios.
CLUB = {
    "nombre": "Club de los Luchadores",
    "socio": "luchador",                # cómo llamamos a cada socio
    "url": "https://flightdirector.peritomoreno360.com/unete/bestial",
    "icono": "🌯",
    "regalo_alta": 1,                   # sellos de regalo al unirse
    "premios": [(6, "Totopos gratis"), (10, "Burrito gratis")],
    "caducidad_dias": 60,
    # Niveles por sellos acumulados desde siempre (sellos_total en Flight Director). Propuesta: ajusta a gusto.
    # (nombre, sellos para llegar, lema, [recompensas], condición)
    "niveles": [
        ("Novato", 0, "Subes al ring", ["1 sello de regalo al unirte", "Totopos gratis a los 6 sellos", "Burrito gratis a los 10 sellos"], ""),
        ("Luchador", 10, "Ya sabes pelear", ["Todo lo de Novato", "Burrito gratis el día de tu cumpleaños", "Sellos dobles todos los martes"], ""),
        ("Campeón", 25, "Nadie te tumba", ["Todo lo de Luchador", "Guacamole extra gratis en cada pedido", "Pruebas lo nuevo antes que nadie"], ""),
        ("Leyenda", 50, "Comes gratis cada mes", ["Todo lo de Campeón", "1 burrito gratis cada mes", "Bebida gratis en cada pedido", "Tu nombre en el muro de Leyendas"], "Sigues siendo Leyenda con 4 pedidos al mes"),
    ],
}
# ====================================================================

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "site"
SRC = ROOT / "src" / "pages"

def m(s):
    """Sustituye el nombre de la marca en textos de datos."""
    return s.replace("{M}", MARCA)

def eur(x):
    return f"{x:.2f}".replace(".", ",") + " €"

def ver(rel):
    return hashlib.md5((OUT / rel).read_bytes()).hexdigest()[:10]

FONTS = "https://fonts.googleapis.com/css2?family=Anton&family=Archivo:wght@400;500;600;700;800&display=swap"
ICON = {
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "bag": '<path d="M6 8h12l-1 12H7L6 8Z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/>',
    "ig": '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/>',
    "mask": '<path d="M12 2.5c4.6 0 8 3.6 8 8.3 0 5.2-3.7 10.7-8 10.7S4 16 4 10.8C4 6.1 7.4 2.5 12 2.5Z"/><path d="M6.5 10.5c1.2-1.4 3.2-1.4 4 .4-.9 1.4-3 1.6-4-.4Zm11 0c-1.2-1.4-3.2-1.4-4 .4.9 1.4 3 1.6 4-.4Z" fill="currentColor"/><path d="M9.5 16.5c1.6 1 3.4 1 5 0"/><path d="M12 2.5v4"/>',
    "tt": '<path d="M14 3v11.5a3.5 3.5 0 1 1-3.5-3.5"/><path d="M14 3c.5 2.6 2.3 4.3 5 4.5"/>',
}
def svg(name, size=20):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[name]}</svg>'

def brand(dark=True):
    if LOGO:
        return f'<img src="/assets/img/{LOGO}-{"negro" if dark else "blanco"}.png" alt="{_html.escape(MARCA_COMPLETA)}" width="101" height="42">'
    return f'<span class="wordmark">{_html.escape(MARCA)}</span>'

def social_links(cls=""):
    out = []
    for name, url, ic in (("Instagram", INSTAGRAM, "ig"), ("TikTok", TIKTOK, "tt")):
        if url:
            out.append(f'<a href="{url}" target="_blank" rel="noopener" aria-label="{name} de {MARCA}">{svg(ic)}</a>')
        else:
            out.append(f'<span title="{name} · próximamente" aria-label="{name} (próximamente)">{svg(ic)}</span>')
    return "".join(out)

def header(active):
    def a(href, label, key):
        cur = ' aria-current="page"' if key == active else ""
        return f'<a href="{href}"{cur}>{label}</a>'
    return f'''<div class="topbar">Nuevo: Inferno, nuestro burrito más picante. <a href="/#inferno">Atrévete →</a></div>
<header class="site-header">
<div class="wrap">
<a class="brand" href="/" aria-label="{_html.escape(MARCA)}, inicio">{brand()}</a>
<a class="icon-btn header-cart" href="/pedir#pedido" aria-label="Tu pedido">{svg("bag")}<span class="cart-count" data-cart-count></span></a>
<button class="nav-toggle" type="button" aria-label="Abrir menú" aria-expanded="false" aria-controls="menu">{svg("menu", 28)}</button>
<nav class="nav" id="menu" aria-label="Principal">
{a("/carta", "Carta", "carta")}
{a("/locales", "Locales", "locales")}
{a("/como-lo-hacemos", "Cómo lo hacemos", "hoy")}
{a("/club", "Club", "club")}
{a("/franquicias", "Franquicias", "franquicias")}
<div class="nav-actions">
<a class="icon-btn" href="/pedir#pedido" aria-label="Tu pedido">{svg("bag")}<span class="cart-count" data-cart-count></span></a>
<a class="btn btn-red" href="/pedir">Pide ahora</a>
</div>
</nav>
</div>
</header>'''

def footer():
    return f'''<footer class="site-footer">
<div class="wrap">
<div class="foot-top">
<div class="foot-brand">
<a href="/" aria-label="Inicio">{brand(False) if LOGO else '<span class="wordmark">' + _html.escape(MARCA) + '</span>'}</a>
<p style="font-weight:800;margin-top:10px">Burritos &amp; Tacos · {CIUDAD}</p>
<div class="social">{social_links()}</div>
</div>
<div class="foot-cols">
<div><b>Comer</b><a href="/carta">Carta</a><a href="/locales">Locales</a><a href="/pedir">Pedir online</a><a href="/nutricion">Nutrición y alérgenos</a></div>
<div><b>{_html.escape(MARCA)}</b><a href="/club">{_html.escape(CLUB["nombre"])}</a><a href="/franquicias">Franquicias</a><a href="/como-lo-hacemos">Cómo lo hacemos</a><a href="mailto:{EMAIL}">Contacto</a></div>
<div><b>Legal</b><a href="/aviso-legal">Aviso legal</a><a href="/privacidad">Privacidad</a><a href="/cookies">Cookies</a></div>
</div>
</div>
<div class="foot-bottom"><span>© <span data-year>2026</span> {_html.escape(MARCA_COMPLETA)} · {TITULAR} · {CIF}</span><a href="{GRUPO_URL}" target="_blank" rel="noopener">Una marca de Perito Moreno 360</a></div>
</div>
</footer>'''

def page(name, body, title, desc, active, extra_head=""):
    canon = f'<link rel="canonical" href="{DOMINIO}/{"" if name == "index" else name}">\n' if DOMINIO else ""
    og_img = f'<meta property="og:image" content="{DOMINIO}/assets/img/hero-burritos.jpg">\n' if DOMINIO else ""
    return f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{_html.escape(title)}</title>
<meta name="description" content="{_html.escape(desc)}">
{canon}<meta property="og:title" content="{_html.escape(title)}">
<meta property="og:description" content="{_html.escape(desc)}">
<meta property="og:type" content="website">
{og_img}<meta name="theme-color" content="#D11F32">
<link rel="icon" href="/assets/img/favicon.png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="/assets/css/bestial.css?v={ver("assets/css/bestial.css")}">
{extra_head}</head>
<body>
<a class="sr" href="#main">Saltar al contenido</a>
{header(active)}
<main id="main">
{body}
</main>
{footer()}
<script src="/assets/js/bestial.js?v={ver("assets/js/bestial.js")}" defer></script>
</body>
</html>
'''

# ---------- bloques generados ----------
TILE = {"tacos": ("#FFC83D", "#E8AF22", "#141414"), "compartir": ("#2E7D4F", "#276B43", "#FFFFFF"),
        "bebidas": ("#2C3A55", "#26324A", "#FFFFFF"), "postres": ("#F2A93B", "#DB962E", "#141414")}

def thumb(sec, name, img):
    if img:
        pos = ' style="object-position:12% center"' if img in ("p-duo", "p-trio", "p-pack") else ""
        return f'<img src="/assets/img/{img}.jpg" alt="{_html.escape(name)}" loading="lazy" width="96" height="96"{pos}>'
    bg, dot, fg = TILE.get(sec, ("#141414", "#2A2A2A", "#FFFFFF"))
    word = name.split(" ")[0]
    size = 22 if len(word) <= 6 else 17 if len(word) <= 8 else 13
    return f'<div class="tile" aria-hidden="true" style="background-color:{bg};background-image:radial-gradient({dot} 2px,transparent 2px);color:{fg};font-size:{size}px">{_html.escape(word)}</div>'

def menu_html(buttons=True):
    out = []
    for sid, title, sub, items in PRODUCTS:
        cards = []
        for pid, name, desc, price, img in items:
            name = m(name)
            d = f'<span class="d">{_html.escape(desc)}</span>' if desc else ""
            btn = f'<button class="add" type="button" data-add="{pid}" aria-label="Añadir {_html.escape(name)}">+</button>' if buttons else ""
            cards.append(f'<article class="item"><div class="th">{thumb(sid, name, img)}</div><div class="info"><h3>{_html.escape(name)}</h3>{d}<span class="p">{eur(price)}</span></div>{btn}</article>')
        s = f'<p class="sub">{_html.escape(m(sub))}</p>' if sub else ""
        out.append(f'<section id="{sid}" class="menu-sec"><h2 class="display">{_html.escape(m(title))}</h2>{s}<div class="items">{"".join(cards)}</div></section>')
    return "\n".join(out)

def subnav(prefix=""):
    links = "".join(f'<a href="#{sid}">{_html.escape(m(t))}</a>' for sid, t, _, _ in PRODUCTS)
    return f'<nav class="subnav" aria-label="Secciones de la carta"><div class="wrap">{prefix}{links}</div></nav>'

def products_json():
    d = {}
    for sid, _, _, items in PRODUCTS:
        for pid, name, desc, price, img in items:
            d[pid] = {"name": m(name), "price": price}
    return d

BADGE = {"local": "Local", "cocina": "Solo a domicilio y recogida", "pronto": "🚧 Próximamente"}

def aviso_pedidos():
    if PEDIDOS_ONLINE:
        return ""
    apps = ", ".join(a for a in APPS_DELIVERY if not a.startswith("["))
    return (f'<div class="soon-bar"><div class="wrap"><b>Muy pronto</b><span>Los pedidos online llegan en unos días. '
            f'Ya puedes montar tu burrito y ver precios; para pedir hoy, usa {apps} o ven a tu {_html.escape(MARCA)}.</span></div></div>')

def locales_html():
    out = []
    for nombre, dir_, horario, tipo in LOCALES:
        q = dir_.replace(" · ", ", ").replace(" ", "+")
        badge = BADGE[tipo]
        if tipo == "pronto":
            out.append(f'''<article class="card soon"><span class="pill">{badge}</span><h3>{_html.escape(nombre)}</h3><p>{_html.escape(dir_)}</p><p class="soon-txt">🚧 Estamos en obras. {horario}.</p>
<div class="actions"><a class="link" href="https://www.google.com/maps/search/?api=1&query={dir_.replace(" · ", ", ").replace(" ", "+")}" target="_blank" rel="noopener">Dónde estará →</a></div></article>''')
            continue
        out.append(f'''<article class="card"><span class="pill">{badge}</span><h3>{_html.escape(nombre)}</h3><p>{_html.escape(dir_)}</p><p class="mut">{horario}</p>
<div class="actions"><a class="link" href="https://www.google.com/maps/search/?api=1&query={q}" target="_blank" rel="noopener">Cómo llegar →</a><a class="link" href="/pedir">Pedir →</a></div></article>''')
    return "\n".join(out)

def club_card(sellos=0):
    """Tarjeta de sellos como la de Flight Director: una casilla por sello y un regalo en cada premio."""
    total = max(n for n, _ in CLUB["premios"])
    premios = {n for n, _ in CLUB["premios"]}
    cells = []
    for k in range(1, total + 1):
        if k <= sellos:
            cells.append(f'<span class="st on" aria-hidden="true">{CLUB["icono"]}</span>')
        elif k in premios:
            cells.append(f'<span class="st gift" aria-hidden="true">🎁</span>')
        else:
            cells.append(f'<span class="st" aria-hidden="true">{k}</span>')
    nxt = min(n for n, _ in CLUB["premios"])
    label = f"Tarjeta de ejemplo con {sellos} de {total} sellos"
    return (f'<div class="club-card" role="img" aria-label="{label}"><div class="cc-top"><span>{_html.escape(CLUB["nombre"])}</span>{brand(False)}</div>'
            f'<div class="stamps">{"".join(cells)}</div><p class="cc-foot">{sellos} de {total} sellos · te faltan {nxt - sellos} para {_html.escape(CLUB["premios"][0][1].lower())}</p></div>')

def club_niveles():
    out = []
    n = len(CLUB["niveles"])
    for i, (nom, sellos, lema, perks, cond) in enumerate(CLUB["niveles"]):
        li = "".join(f"<li>{_html.escape(p)}</li>" for p in perks)
        req = "Al unirte" if sellos == 0 else f"{sellos} sellos"
        c = f'<p class="cond">{_html.escape(cond)}</p>' if cond else ""
        top = '<span class="crown">El nivel más alto</span>' if i == n - 1 else ""
        out.append(f'<article class="lvl lvl-{i + 1}">{top}<div class="lv-head"><span class="mask">{svg("mask", 30)}</span><span class="req">Nivel {i + 1} · {req}</span></div>'
                   f'<h3>{_html.escape(nom)}</h3><p class="lema">{_html.escape(lema)}</p><ul>{li}</ul>{c}</article>')
    return "".join(out)

def club_premios():
    return "".join(f'<div><b>{n}</b><span>sellos</span><p>{_html.escape(pr)}</p></div>' for n, pr in sorted(CLUB["premios"]))

def locales_mini():
    return "".join(f'<a class="loc-mini" href="/locales"><b>{_html.escape(n)}</b><span>{_html.escape(d)}</span>'
                   f'<em>{BADGE[t]}</em></a>' for n, d, h, t in LOCALES)

def data_script(obj):
    return '<script>window.CARTA=' + json.dumps(obj, ensure_ascii=False).replace("</", "<\\/") + ';</script>\n'

def tokens(s):
    rep = {
        "MARCA": _html.escape(MARCA), "MARCA_COMPLETA": _html.escape(MARCA_COMPLETA), "CIUDAD": CIUDAD,
        "EMAIL": EMAIL, "TITULAR": TITULAR, "CIF": CIF, "DOMICILIO": DOMICILIO, "N_LOCALES": str(len(LOCALES)),
        "LOCALES": locales_html(), "AVISO_PEDIDOS": aviso_pedidos(), "LOCALES_MINI": locales_mini(), "GRUPO_URL": GRUPO_URL, "MENU": menu_html(False), "MENU_SHOP": menu_html(True),
        "SUBNAV": subnav(), "SUBNAV_SHOP": subnav('<a href="#medida" class="on">A tu medida</a>'),
        "SOCIAL": social_links(), "APPS": "".join(f"<span>{a}</span>" for a in APPS_DELIVERY),
        "CLUB": _html.escape(CLUB["nombre"]), "CLUB_URL": CLUB["url"], "CLUB_SOCIO": CLUB["socio"],
        "CLUB_ICONO": CLUB["icono"], "CLUB_REGALO": str(CLUB["regalo_alta"]), "CLUB_CADUCA": str(CLUB["caducidad_dias"]),
        "CLUB_CARD": club_card(4), "CLUB_PREMIOS": club_premios(),
        "CLUB_NIVELES": club_niveles(), "CLUB_TOP": _html.escape(CLUB["niveles"][-1][0]),
        "CLUB_TOP_SELLOS": str(CLUB["niveles"][-1][1]),
        "CLUB_TOTAL": str(max(n for n, _ in CLUB["premios"])),
        "DOMINIO_O_WEB": DOMINIO.replace("https://", "") if DOMINIO else "esta web",
    }
    return re.sub(r"\{\{([A-Z_]+)\}\}", lambda mo: rep[mo.group(1)], s)

PAGES = {
    # nombre: (título, descripción, activo, datos para JS)
    "index": (f"{MARCA_COMPLETA} · Burritos y tacos hechos al momento en {CIUDAD}",
              f"Burritos, bowls y tacos recién hechos. Monta el tuyo, pide online sin comisiones o ven a uno de nuestros locales en {CIUDAD}.", "home", None),
    "carta": (f"Carta · {MARCA_COMPLETA}", "Burritos, bowls, tacos, quesadillas, nachos, bebidas y postres con sus precios.", "carta", None),
    "pedir": (f"Pide online · {MARCA_COMPLETA}", "Monta tu burrito o bowl y pide a domicilio o para recoger, sin comisiones de app.", "medida", "shop"),
    "pago": (f"Tu pedido · {MARCA_COMPLETA}", "Revisa tu pedido y tus datos de entrega.", "", "shop"),
    "nutricion": (f"Calculadora nutricional · {MARCA_COMPLETA}", "Calorías, nutrientes y alérgenos de tu burrito o bowl.", "", "calc"),
    "locales": (f"Locales · {MARCA_COMPLETA}", f"Nuestros locales en {CIUDAD}: dirección, horario y cómo pedir.", "locales", None),
    "como-lo-hacemos": (f"Cómo lo hacemos · {MARCA_COMPLETA}", "Producto del día y cada burrito montado al momento, a la vista.", "hoy", None),
    "franquicias": (f"Franquicias · {MARCA_COMPLETA}", f"Abre tu {MARCA}: 2% de royalty el primer año y 4% desde el segundo, sin letra pequeña.", "franquicias", None),
    "club": (f"{CLUB['nombre']} · {MARCA_COMPLETA}", f"Únete gratis al {CLUB['nombre']}: cada pedido suma un sello y los sellos se convierten en comida gratis.", "club", None),
    "aviso-legal": (f"Aviso legal · {MARCA_COMPLETA}", "Aviso legal.", "", None),
    "privacidad": (f"Privacidad · {MARCA_COMPLETA}", "Política de privacidad.", "", None),
    "cookies": (f"Cookies · {MARCA_COMPLETA}", "Política de cookies.", "", None),
    "404": (f"Página no encontrada · {MARCA_COMPLETA}", "Esta página no existe.", "", None),
}

def make_favicon():
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return
    for size, name in ((64, "favicon.png"), (180, "apple-touch-icon.png")):
        im = Image.new("RGB", (size, size), "#D11F32")
        d = ImageDraw.Draw(im)
        try:
            f = ImageFont.truetype("DejaVuSans-Bold.ttf", int(size * .62))
        except OSError:
            f = ImageFont.load_default()
        t = MARCA[0].upper()
        b = d.textbbox((0, 0), t, font=f)
        d.text(((size - b[2] - b[0]) / 2, (size - b[3] - b[1]) / 2), t, fill="#FFFFFF", font=f)
        im.save(OUT / "assets" / "img" / name)

def main():
    make_favicon()
    shop = shop_data()
    calc = json.loads(calc_data())
    for g in shop["groups"] + calc["groups"]:
        g["title"] = m(g["title"])
        for it in g["items"]:
            it["name"] = m(it["name"])
    for name, (title, desc, active, data) in PAGES.items():
        body = tokens((SRC / f"{name}.html").read_text())
        head = ""
        if data == "shop":
            head = data_script({"groups": shop["groups"], "presets": shop["presets"], "base": shop["base"], "products": products_json()})
        elif data == "calc":
            head = data_script({"groups": calc["groups"], "presets": calc["presets"]})
        (OUT / f"{name}.html").write_text(page(name, body, title, desc, active, head))
    if DOMINIO:
        urls = "".join(f"<url><loc>{DOMINIO}/{'' if n == 'index' else n}</loc></url>" for n in ("index", "carta", "pedir", "nutricion", "club", "locales", "como-lo-hacemos", "franquicias"))
        (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
        (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {DOMINIO}/sitemap.xml\n")
    else:
        (OUT / "robots.txt").write_text("User-agent: *\nAllow: /\n")
        sm = OUT / "sitemap.xml"
        if sm.exists():
            sm.unlink()
    print(f"ok · {len(PAGES)} páginas · marca «{MARCA}» · dominio {DOMINIO or '(sin dominio)'}")

if __name__ == "__main__":
    main()
