"""Carta de La Sardinera (copia de Flight Director, marca «La Sardinera», productos activos, precio de sala).

Para actualizarla: cambia aquí precios o platos y vuelve a generar con `python3 sardinera/tools/build.py`.
Formato: (id, título, subtítulo, [(grupo, [(nombre, descripción, precio), …]), …])
"""

CARTA = [
    ("para-empezar", "Para empezar", "Gildas, pan y el primer bocado del norte.", [
        ("Gildas", [
            ("Gilda de anchoa", "Aceituna, piparra y anchoa del Cantábrico.", 2.80),
            ("Gilda de boquerón", "", 2.20),
            ("Gilda con queso", "", 2.20),
            ("Gilda con gambas", "", 2.80),
            ("Gilda con huevo de codorniz", "", 2.30),
        ]),
        ("Para picar", [
            ("Sardina Picantona", "Pan con sardina sobre salsa brava.", 4.50),
            ("Cesta de pan con mantequilla ahumada", "", 4.50),
        ]),
    ]),
    ("pinchos", "Pinchos", "La tortilla de Santander, jugosa y poco hecha.", [
        ("Tortillas", [
            ("Tortilla con cebolla", "Pincho.", 3.00),
            ("Tortilla con bonito y mayonesa", "Pincho.", 3.50),
            ("Tortilla con jamón y queso", "Pincho.", 3.50),
        ]),
        ("Tostas y montados", [
            ("Sardinera", "Montado de ensaladilla y anchoa sobre pan marinera.", 3.50),
            ("Sardinero", "Montado de ensaladilla y boquerón sobre pan marinera.", 3.20),
            ("Tosta de anchoa con mantequilla ahumada", "", 3.50),
            ("Tiradito de sobao pasiego con anchoa", "", 3.20),
            ("Bocatín de tortilla en pan de cristal", "", 2.80),
        ]),
        ("De la barra", [
            ("Coca de sardinas con queso feta", "Coca salada recién horneada.", 7.50),
            ("Montadito de barra", "Los del día, expuestos en barra.", 2.80),
        ]),
    ]),
    ("lata", "Te damos la lata", "Conservas del Cantábrico y de las rías, servidas en su lata.", [
        ("Pescados", [
            ("Octavillo de anchoas", "", 9.50),
            ("Ventresca con mantequilla", "", 12.50),
        ]),
        ("Mejillones y berberechos", [
            ("Mejillones en oliva", "", 7.50),
            ("Mejillones picantes", "", 8.50),
            ("Berberechos en oliva", "", 12.00),
        ]),
        ("Mariscos", [
            ("Zamburiñas ajo-guindilla", "", 12.00),
        ]),
    ]),
    ("raciones", "Nuestras raciones", "Para compartir en la mesa.", [
        ("Del mar", [
            ("Ración de anchoas", "9-10 unidades.", 14.00),
            ("Boquerones en vinagre", "Con el toque de la casa.", 7.50),
            ("Ventresca con pimientos confitados", "", 13.50),
        ]),
        ("Elaboradas", [
            ("Ensaladilla", "Coronada con sardinilla.", 8.50),
            ("Empanada gallega", "Ración.", 4.50),
            ("Tortilla entera (mediana)", "También por encargo para llevar.", 14.00),
        ]),
        ("Ensaladas y untables", [
            ("Ensalada de tomate con ventresca", "Tomate natural, ventresca, piparras y cebolla.", 12.50),
            ("Pastel de cabracho", "Con pan tostado.", 7.50),
            ("Untable de morcilla con queso", "Con pan tostado.", 6.50),
            ("Foie", "Con pan tostado.", 12.00),
        ]),
        ("Ibéricos y quesos", [
            ("Jamón de cebo ibérico", "Ración.", 18.00),
            ("Cecina de León", "Ración.", 13.00),
            ("Tabla de embutidos mixta", "Jamón, cecina, chorizo y lomo.", 16.00),
            ("Tabla de quesos", "Selección de quesos.", 14.00),
            ("Queso de cabra horneado para mojar", "Ración.", 9.50),
        ]),
    ]),
    ("desayunos", "Desayunos", "Café de especialidad, tostadas y sobao pasiego.", [
        ("Para comer", [
            ("Tostada de mantequilla y mermelada", "", 2.80),
            ("Tostada de tomate", "Aceite de oliva virgen extra y tomate rallado natural.", 3.00),
            ("Tostada de aguacate y semillas", "", 3.90),
            ("Tostada de jamón ibérico y tomate", "", 7.00),
            ("Cesta especial desayuno", "2 variedades de pan y 1 sobao tradicional.", 8.95),
            ("Bowl de yogur con granola", "Yogur griego, granola, fruta fresca y miel.", 4.90),
        ]),
        ("Cafés", [
            ("Café solo", "", 1.50), ("Café cortado", "", 1.60), ("Café con leche", "", 1.80),
            ("Café americano", "", 1.70), ("Capuchino", "", 2.50), ("Flat white", "Doble espresso de especialidad.", 2.80),
            ("Matcha latte", "", 3.50), ("Chai latte", "", 3.50),
        ]),
        ("Y además", [
            ("Zumo de naranja natural", "Recién exprimido.", 3.50), ("ColaCao", "", 2.20), ("Vaso de leche", "", 1.30),
            ("Tés e infusiones", "Negro, Earl Grey, verde, rojo, rooibos, manzanilla, poleo o tila.", 1.80),
        ]),
    ]),
    ("bebidas", "Bebidas", "Caña bien tirada, vermut de grifo y vinos de casa y de D.O.", [
        ("Cervezas", [
            ("Caña", "200 ml.", 2.20), ("Doble", "330 ml.", 3.20), ("Clara", "Con gaseosa de limón.", 2.40),
            ("Tercio", "33 cl.", 3.00), ("Botellín 18/70 La Rubia", "33 cl.", 3.50),
            ("Session IPA sin gluten", "33 cl.", 3.95), ("Cerveza sin alcohol 0,0", "", 3.00),
        ]),
        ("Vermut y generosos", [
            ("Vermut rojo de grifo", "Con hielo, naranja y aceituna.", 2.80), ("Vermut Doña Tomasa", "Artesano.", 3.80),
            ("Tinto de verano", "", 3.00), ("Copa de fino", "Socaire.", 2.80), ("Pedro Ximénez", "", 3.50),
        ]),
        ("Vinos por copa", [
            ("Tinto o blanco de la casa", "", 2.80), ("Rioja", "Campo Aldea, D.O.Ca. Rioja.", 3.50),
            ("Ribera roble", "Finca Engalia, D.O. Ribera del Duero.", 3.50), ("Verdejo", "Alijares, D.O. Rueda.", 3.20),
            ("Albariño", "Rectoral do Umia, D.O. Rías Baixas.", 3.80), ("Rosado", "Viña Campus, D.O. Navarra.", 3.00),
            ("Cava", "Jaume Serra brut nature.", 3.50),
        ]),
        ("Vinos por botella", [
            ("Rioja crianza", "El Coto, 75 cl.", 22.00), ("Ribera roble", "Finca Engalia, 75 cl.", 20.00),
            ("Verdejo", "Cuatro Rayas, 75 cl.", 18.00), ("Albariño", "Rectoral do Umia, 75 cl.", 24.00),
            ("Rosado", "Zarzales, 75 cl.", 16.00), ("Cava", "Jaume Serra brut nature, 75 cl.", 20.00),
        ]),
        ("Refrescos y agua", [
            ("Refrescos", "Coca-Cola, Zero, Fanta, Sprite, Fuze Tea, Aquarius o tónica.", 2.50),
            ("Zumos", "Melocotón, piña o tomate.", 2.50), ("Mosto", "200 ml.", 2.20), ("Red Bull", "", 3.50),
            ("Agua mineral", "50 cl.", 1.80), ("Agua con gas", "Vichy Catalán, 30 cl.", 2.50),
        ]),
        ("Copas y chupitos", [
            ("Gin tonic", "", 8.50), ("Ron, whisky o vodka con refresco", "", 8.00),
            ("Chupitos", "Orujo de hierbas, crema de orujo, orujo blanco, pacharán, licor de café o limoncello.", 2.50),
        ]),
    ]),
    ("postres", "Postres", "", [
        ("", [
            ("Tarta de queso", "1 porción.", 4.50),
            ("Helado", "Nata, chocolate o mantecado.", 3.50),
        ]),
    ]),
]
