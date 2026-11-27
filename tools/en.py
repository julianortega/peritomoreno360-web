"""Textos en inglés de la web (cabecera, pie, formulario y títulos de cada página).

Los cuerpos de las páginas en inglés están en src/pages-en/. Si cambias una página
en español, cambia también su versión en inglés.
"""

# Opciones del formulario: el valor que llega al correo sigue en español.
OPTIONS = {
    "Restauración": "Restaurants", "Franquicias": "Franchises", "Operaciones": "Operations",
    "Mantenimiento": "Maintenance", "Desarrollo de apps": "App development", "Flight Director": "Flight Director",
    "Trabajar con vosotros": "Working with you", "Otro": "Other",
}

# Pares español → inglés para la cabecera, el pie, los medios de pago y el formulario.
CHROME = [
    ('aria-label="Perito Moreno 360, inicio"', 'aria-label="Perito Moreno 360, home"'),
    ('aria-label="Abrir menú"', 'aria-label="Open menu"'),
    ('aria-label="Principal"', 'aria-label="Main"'),
    ('>El grupo<', '>The group<'),
    ('>Áreas de negocio<', '>Business areas<'),
    ('Restauración<small>Bestial, La Sardinera y Lolita Bakery</small>', 'Restaurants<small>Bestial, La Sardinera and Lolita Bakery</small>'),
    ('Operaciones<small>Hacemos tu empresa más eficiente</small>', 'Operations<small>We make your business more efficient</small>'),
    ('Mantenimiento<small>Rumbo Norte, multiservicios</small>', 'Maintenance<small>Rumbo Norte, multi-service</small>'),
    ('Desarrollo de apps<small>Apps a medida para empresas</small>', 'App development<small>Custom apps for businesses</small>'),
    ('<small>La gestión 360 de tu local de hostelería</small>', '<small>360° management for your hospitality business</small>'),
    ('<small>La app de tu club de fútbol</small>', '<small>The app for your football club</small>'),
    ('>Hablemos<', ">Let's talk<"),
    (' · próximamente"', ' · coming soon"'),
    (' (próximamente)"', ' (coming soon)"'),
    ('aria-label="Medios de pago aceptados"', 'aria-label="Accepted payment methods"'),
    ('Pago seguro con tarjeta o Bizum · Precios en euros (EUR)', 'Secure payment by card or Bizum · Prices in euros (EUR)'),
    ('<span>Urbanización Las Dalias 9, 39100 Santa Cruz de Bezana (Cantabria)</span>', '<span>Urbanización Las Dalias 9, 39100 Santa Cruz de Bezana (Cantabria, Spain)</span>'),
    ('<b>Áreas de negocio</b>', '<b>Business areas</b>'),
    ('<a href="/restauracion">Restauración</a>', '<a href="/restauracion">Restaurants</a>'),
    ('<a href="/operaciones">Operaciones</a>', '<a href="/operaciones">Operations</a>'),
    ('<a href="/mantenimiento">Mantenimiento</a>', '<a href="/mantenimiento">Maintenance</a>'),
    ('<a href="/apps">Desarrollo de apps</a>', '<a href="/apps">App development</a>'),
    ('<b>Franquicias</b>', '<b>Franchises</b>'),
    ('<a href="/franquicias">Condiciones</a>', '<a href="/franquicias">Terms</a>'),
    ('<a href="/franquicia-burritos">Franquicia de burritos</a>', '<a href="/franquicia-burritos">Burrito franchise</a>'),
    ('<a href="/franquicia-dark-kitchen">Franquicia dark kitchen</a>', '<a href="/franquicia-dark-kitchen">Dark kitchen franchise</a>'),
    ('<a href="/franquicias-hosteleria-royalty-bajo">Royalty bajo</a>', '<a href="/franquicias-hosteleria-royalty-bajo">Low royalty</a>'),
    ('<a href="/app-escandallos-hosteleria">Escandallos</a>', '<a href="/app-escandallos-hosteleria">Recipe costing</a>'),
    ('<a href="/control-food-cost-restaurante">Control del food cost</a>', '<a href="/control-food-cost-restaurante">Food cost control</a>'),
    ('<a href="/app-cuadrantes-hosteleria">Cuadrantes y fichajes</a>', '<a href="/app-cuadrantes-hosteleria">Rotas and clock-ins</a>'),
    ('<a href="/aviso-legal">Aviso legal</a>', '<a href="/aviso-legal">Legal notice</a>'),
    ('<a href="/condiciones-contratacion">Condiciones de contratación</a>', '<a href="/condiciones-contratacion">Terms of sale</a>'),
    ('<a href="/condiciones-contratacion#envio">Envío y entrega</a>', '<a href="/condiciones-contratacion#envio">Shipping and delivery</a>'),
    ('<a href="/condiciones-contratacion#desistimiento">Desistimiento y devoluciones</a>', '<a href="/condiciones-contratacion#desistimiento">Withdrawal and refunds</a>'),
    ('<a href="/privacidad">Privacidad</a>', '<a href="/privacidad">Privacy</a>'),
    ('<a href="/cookies">Cookies</a>', '<a href="/cookies">Cookies</a>'),
    # Formulario
    ('Si lo prefieres, escríbenos a', 'If you prefer, email us at'),
    ('>Nombre</label>', '>Name</label>'),
    ('>Correo electrónico</label>', '>Email</label>'),
    ('>Teléfono</label>', '>Phone</label>'),
    ('>Te interesa</label>', ">I'm interested in</label>"),
    ('>No rellenar</label>', '>Leave blank</label>'),
    ('He leído y acepto la <a href="/privacidad" target="_blank">política de privacidad</a>.',
     'I have read and accept the <a href="/privacidad" target="_blank">privacy policy</a>.'),
    ('He leído y acepto las <a href="/condiciones-contratacion" target="_blank">condiciones de contratación</a>, incluidas las políticas de entrega, '
     '<a href="/condiciones-contratacion#desistimiento" target="_blank">desistimiento</a> y '
     '<a href="/condiciones-contratacion#devoluciones" target="_blank">devoluciones</a>.',
     'I have read and accept the <a href="/condiciones-contratacion" target="_blank">terms of sale</a>, including the delivery, '
     '<a href="/condiciones-contratacion#desistimiento" target="_blank">withdrawal</a> and '
     '<a href="/condiciones-contratacion#devoluciones" target="_blank">refund</a> policies.'),
    ('No hace falta que nos llames: te contactaremos nosotros por teléfono o por correo.', "No need to call us: we'll get in touch by phone or email."),
    ('>Quiero que me contactéis<', '>Please contact me<'),
    ('<b>¡Gracias, <span data-name></span>!</b>', '<b>Thank you, <span data-name></span>!</b>'),
    ('Hemos recibido tus datos. Te contactaremos nosotros muy pronto.', "We've received your details. We'll be in touch very soon."),
]

FD_DESC = "Management for hospitality businesses: recipe costing, kitchen, team and rotas, checklists and HACCP, purchasing and a live P&L."

ASK = "Leave us your details and we'll get in touch."
DEMO = "Leave us your details and we'll get in touch to give you a demo."

# slug → (título, descripción, formulario)  · formulario: (origen, interés, título, texto, condiciones)
PAGES = {
    "index": ("Perito Moreno 360 · Business group", "Business group with restaurant brands, operations consulting, maintenance and custom app development.",
              ("Inicio · EN", "Otro", "Shall we talk?", ASK)),
    "restauracion": ("Restaurants · Perito Moreno 360", "Our own organised restaurant brands: Bestial Burritos & Tacos, La Sardinera and Lolita Bakery.",
                     ("Restauración · EN", "Restauración", "Shall we talk?", ASK)),
    "operaciones": ("Operations · Perito Moreno 360", "We study your company in depth to make it more efficient: operations manuals, weak points found and monthly support.",
                    ("Operaciones · EN", "Operaciones", "Want your company to run better?", ASK)),
    "mantenimiento": ("Maintenance · Rumbo Norte · Perito Moreno 360", "Maintenance and repairs for buildings, offices, shops, residential communities and restaurants: electrical, plumbing, HVAC, carpentry, locksmith and painting with Rumbo Norte.",
                      ("Mantenimiento · EN", "Mantenimiento", "Ask for a quote", "Leave us your details and we'll get in touch to prepare your quote, free and with no obligation.")),
    "apps": ("App development · Perito Moreno 360", "Custom web and mobile apps for businesses, with clear prices: free study, demo module and full app with a price cap.",
             ("Desarrollo de apps · EN", "Desarrollo de apps", "Got an idea for an app?", ASK, True)),
    "franquicias": ("Franchises · Perito Moreno 360", "Open one of our brands with a 2% royalty in year one and 4% after that, with no increases.",
                    ("Franquicias · EN", "Franquicias", "Shall we talk about your franchise?", ASK)),
    "flight-director": ("Flight Director · 360° management for your hospitality business", "Recipe costing, kitchen, team, checklists, purchasing and a live P&L for hospitality businesses.",
                        ("Flight Director · EN", "Flight Director", "Shall we try it in your venue?", "Leave us your details and we'll get in touch to show you Flight Director.")),
    "flight-director/empieza": ("Start today with Flight Director · Sign up · Perito Moreno 360", "Sign up for Flight Director in two minutes: €75/month per venue, all included. No lock-in. Pay by card or Bizum.", None),
    "mi-vestuario": ("Mi Vestuario · The app for your football club · Perito Moreno 360", "Call-ups, calendar, attendance, fees, kit, league and rankings for your football club in one app for the board, coaches, players and families.",
                     ("Mi Vestuario · EN", "Desarrollo de apps", "Shall we try it in your club?", "Leave us your details and we'll show you Mi Vestuario with your club's teams.")),
    "franquicia-burritos": ("Burrito and taco franchise · Bestial Burritos & Tacos", "Open a Bestial burrito and taco franchise: 100% natural Mexican fast casual, as a dark kitchen, a venue or a flagship. 2% royalty in year one.",
                            ("Franquicia de burritos · EN", "Franquicias", "Shall we open a Bestial in your city?", ASK)),
    "franquicia-dark-kitchen": ("Burrito dark kitchen franchise · Low investment · Bestial", "Dark kitchen franchise: start with delivery only in 15–50 m², test your area with a small investment and grow into a venue. 2% royalty in year one.",
                                ("Franquicia dark kitchen · EN", "Franquicias", "Shall we talk about your dark kitchen?", ASK)),
    "franquicias-hosteleria-royalty-bajo": ("Low-royalty hospitality franchises: 2% and 4%", "Hospitality franchises with one of the lowest royalties: 2% in year one and 4% after that, fixed and with no increases. Clear terms, no small print.",
                                            ("Royalty bajo · EN", "Franquicias", "Shall we talk about your franchise?", ASK)),
    "app-escandallos-hosteleria": ("Recipe costing app for hospitality · Flight Director", "Recipe costs that update themselves: cost per portion, food cost and margin for dine-in and delivery, including the platform commission.",
                                   ("App de escandallos · EN", "Flight Director", "Shall we show you your recipe costs in Flight Director?", DEMO)),
    "control-food-cost-restaurante": ("How to calculate and control a restaurant's food cost · Guide", "What food cost is, how to calculate it with an example, what percentage is good and 7 ways to control it in your restaurant.",
                                      ("Guía food cost · EN", "Flight Director", "Want to control your food cost without Excel?", "Leave us your details and we'll show you how Flight Director does it.")),
    "app-cuadrantes-hosteleria": ("Rota and clock-in app for hospitality · Flight Director", "Shift rotas based on forecast sales, staff cost before you publish and clock-ins for the working-hours record. App for restaurants.",
                                  ("App de cuadrantes · EN", "Flight Director", "Shall we show you your rotas in Flight Director?", DEMO)),
    "aviso-legal": ("Legal notice · Perito Moreno 360", "Legal notice of the Perito Moreno 360 SL website.", None),
    "condiciones-contratacion": ("Terms of sale · Perito Moreno 360", "Terms of sale for Perito Moreno 360 SL services: prices, payment, timeframes, withdrawal and refunds.", None),
    "privacidad": ("Privacy policy · Perito Moreno 360", "Privacy policy of Perito Moreno 360 SL.", None),
    "cookies": ("Cookie policy · Perito Moreno 360", "Cookie policy of the Perito Moreno 360 SL website.", None),
    "404": ("Page not found · Perito Moreno 360", "The page you are looking for doesn't exist.", None),
}

FLAG_ES = '<svg viewBox="0 0 30 20" aria-hidden="true"><rect width="30" height="20" fill="#AA151B"/><rect y="5" width="30" height="10" fill="#F1BF00"/></svg>'
FLAG_EN = ('<svg viewBox="0 0 60 30" aria-hidden="true"><clipPath id="uk-t"><path d="M30 15h30v15zv15H0zH0V0zV0h30z"/></clipPath>'
           '<path d="M0 0v30h60V0z" fill="#012169"/><path d="M0 0l60 30m0-30L0 30" stroke="#fff" stroke-width="6"/>'
           '<path d="M0 0l60 30m0-30L0 30" clip-path="url(#uk-t)" stroke="#C8102E" stroke-width="4"/>'
           '<path d="M30 0v30M0 15h60" stroke="#fff" stroke-width="10"/><path d="M30 0v30M0 15h60" stroke="#C8102E" stroke-width="6"/></svg>')
