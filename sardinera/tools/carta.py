"""Carta de La Sardinera.

Precios e ids salen de `fd_carta.tsv` (copia de Flight Director, marca «La Sardinera», productos activos):
id | nombre en FD | precio en sala | precio a domicilio («-» = no se vende a domicilio).
Para actualizarla: vuelve a sacar ese listado de Flight Director y `python3 sardinera/tools/build.py`.

Cada plato de CARTA es (nombre en la web, descripción, referencia):
  · referencia = nombre en Flight Director → precio de FD y se puede pedir online (salvo los de SOLO_BARRA);
  · referencia = número → solo se enseña en la carta con ese precio (p. ej. «Tés e infusiones»).
El servidor de Flight Director vuelve a calcular todos los precios al pedir: la web solo los enseña.
"""
import pathlib

FD = {}
for linea in (pathlib.Path(__file__).parent / "fd_carta.tsv").read_text().splitlines():
    if not linea or linea.startswith("#"):
        continue
    pid, nombre, sala, dom = linea.split("|")
    FD[nombre] = (pid, float(sala), None if dom == "-" else float(dom))

# Se sirven en la barra pero no tiene sentido pedirlos para llevar.
SOLO_BARRA = {
    "Caña", "Doble", "Clara", "Vermut rojo de grifo", "Tinto de verano", "Copa de fino", "Pedro Ximénez", "Montadito de barra",
    "Copa de tinto de la casa", "Copa de blanco de la casa", "Copa de Rioja", "Copa de Ribera roble", "Copa de Verdejo",
    "Copa de Albariño", "Copa de rosado", "Copa de cava", "Gin tonic", "Ron cola", "Whisky cola", "Vodka naranja o limón",
    "Café solo", "Café cortado", "Café con leche", "Café americano", "Capuchino", "Flat white", "Matcha latte", "Chai latte",
    "ColaCao", "Vaso de leche",
}

CARTA = [
    ("para-empezar", "Para empezar", "Gildas, pan y el primer bocado del norte.", [
        ("Gildas", [
            ("Gilda de anchoa", "Aceituna, piparra y anchoa del Cantábrico.", "Gilda de anchoa"),
            ("Gilda de boquerón", "", "Gilda de boquerón"),
            ("Gilda con queso", "", "Gilda con queso"),
            ("Gilda con gambas", "", "Gilda con gambas"),
            ("Gilda con huevo de codorniz", "", "Gilda con huevo de codorniz"),
        ]),
        ("Para picar", [
            ("Sardina Picantona", "Pan con sardina sobre salsa brava.", "Sardina Picantona"),
            ("Cesta de pan con mantequilla ahumada", "", "Cesta de pan con mantequilla ahumada"),
        ]),
    ]),
    ("pinchos", "Pinchos", "La tortilla de Santander, jugosa y poco hecha.", [
        ("Tortillas", [
            ("Pincho de tortilla con cebolla", "", "Tortilla con cebolla"),
            ("Pincho de tortilla con bonito y mayonesa", "", "Tortilla con bonito y mayonesa"),
            ("Pincho de tortilla con jamón y queso", "", "Tortilla con jamón y queso"),
            ("Tortilla entera (mediana)", "Para compartir o para llevar a casa.", "Tortilla entera (mediana)"),
        ]),
        ("Tostas y montados", [
            ("Sardinera", "Montado de ensaladilla y anchoa sobre pan marinera.", "Sardinera"),
            ("Sardinero", "Montado de ensaladilla y boquerón sobre pan marinera.", "Sardinero"),
            ("Tosta de anchoa con mantequilla ahumada", "", "Tosta de anchoa con mantequilla ahumada"),
            ("Tiradito de sobao pasiego con anchoa", "", "Tiradito de sobao pasiego con anchoa"),
            ("Bocatín de tortilla en pan de cristal", "", "Bocatín de tortilla en pan de cristal"),
        ]),
        ("De la barra", [
            ("Coca de sardinas con queso feta", "Coca salada recién horneada.", "Coca de sardinas con queso feta"),
            ("Montadito de barra", "Los del día, expuestos en barra.", "Montadito de barra"),
        ]),
    ]),
    ("lata", "Te damos la lata", "Conservas del Cantábrico y de las rías, servidas en su lata.", [
        ("Pescados", [
            ("Octavillo de anchoas", "", "Octavillo de anchoas"),
            ("Ventresca con mantequilla", "", "Ventresca con mantequilla"),
        ]),
        ("Mejillones y berberechos", [
            ("Mejillones en oliva", "", "Mejillones en oliva"),
            ("Mejillones picantes", "", "Mejillones picantes"),
            ("Berberechos en oliva", "", "Berberechos en oliva"),
        ]),
        ("Mariscos", [
            ("Zamburiñas ajo-guindilla", "", "Zamburiñas ajo-guindilla"),
        ]),
    ]),
    ("raciones", "Nuestras raciones", "Para compartir en la mesa.", [
        ("Del mar", [
            ("Ración de anchoas", "9-10 unidades.", "Ración de anchoas"),
            ("Boquerones en vinagre", "Con el toque de la casa.", "Ración de boquerones en vinagre"),
            ("Ventresca con pimientos confitados", "", "Ración de ventresca con pimientos confitados"),
        ]),
        ("Elaboradas", [
            ("Ensaladilla", "Coronada con sardinilla.", "Ración de ensaladilla"),
            ("Empanada gallega", "Ración.", "Ración de empanada gallega"),
        ]),
        ("Ensaladas y untables", [
            ("Ensalada de tomate con ventresca", "Tomate natural, ventresca, piparras y cebolla.", "Ensalada de tomate con ventresca"),
            ("Pastel de cabracho", "Con pan tostado.", "Pastel de cabracho"),
            ("Untable de morcilla con queso", "Con pan tostado.", "Untable de morcilla con queso"),
            ("Foie", "Con pan tostado.", "Foie"),
        ]),
        ("Ibéricos y quesos", [
            ("Jamón de cebo ibérico", "Ración.", "Ración de jamón de cebo ibérico"),
            ("Cecina de León", "Ración.", "Ración de cecina de León"),
            ("Tabla de embutidos mixta", "Jamón, cecina, chorizo y lomo.", "Tabla de embutidos mixta"),
            ("Tabla de quesos", "Selección de quesos.", "Tabla de quesos"),
            ("Queso de cabra horneado para mojar", "Ración.", "Queso de cabra horneado especial para mojar"),
        ]),
    ]),
    ("desayunos", "Desayunos", "Café de especialidad, tostadas y sobao pasiego.", [
        ("Para comer", [
            ("Tostada de mantequilla y mermelada", "", "Tostada de mantequilla y mermelada"),
            ("Tostada de tomate", "Aceite de oliva virgen extra y tomate rallado natural.", "Tostada de tomate"),
            ("Tostada de aguacate y semillas", "", "Tostada de aguacate y semillas"),
            ("Tostada de jamón ibérico y tomate", "", "Tostada de jamón ibérico y tomate"),
            ("Cesta especial desayuno", "2 variedades de pan y 1 sobao tradicional.", "Cesta especial desayuno"),
            ("Bowl de yogur con granola", "Yogur griego, granola, fruta fresca y miel.", "Bowl de yogur con granola"),
        ]),
        ("Cafés", [
            ("Café solo", "", "Café solo"), ("Café cortado", "", "Café cortado"), ("Café con leche", "", "Café con leche"),
            ("Café americano", "", "Café americano"), ("Capuchino", "", "Capuchino"), ("Flat white", "Doble espresso de especialidad.", "Flat white"),
            ("Matcha latte", "", "Matcha latte"), ("Chai latte", "", "Chai latte"),
        ]),
        ("Y además", [
            ("Zumo de naranja natural", "Recién exprimido.", "Zumo de naranja natural"), ("ColaCao", "", "ColaCao"), ("Vaso de leche", "", "Vaso de leche"),
            ("Tés e infusiones", "Negro, Earl Grey, verde, rojo, rooibos, manzanilla, poleo o tila.", 1.80),
        ]),
    ]),
    ("bebidas", "Bebidas", "Caña bien tirada, vermut de grifo y vinos de casa y de D.O.", [
        ("Cervezas", [
            ("Caña", "200 ml.", "Caña"), ("Doble", "330 ml.", "Doble"), ("Clara", "Con gaseosa de limón.", "Clara"),
            ("Tercio", "33 cl.", "Tercio"), ("Botellín 18/70 La Rubia", "33 cl.", "Botellín 18/70 La Rubia"),
            ("Session IPA sin gluten", "33 cl.", "Bestial Session IPA sin gluten"), ("Cerveza sin alcohol 0,0", "", "Cerveza sin alcohol 0,0"),
        ]),
        ("Vermut y generosos", [
            ("Vermut rojo de grifo", "Con hielo, naranja y aceituna.", "Vermut rojo de grifo"), ("Vermut Doña Tomasa", "Artesano.", "Vermut Doña Tomasa"),
            ("Tinto de verano", "", "Tinto de verano"), ("Copa de fino", "Socaire.", "Copa de fino"), ("Pedro Ximénez", "", "Pedro Ximénez"),
        ]),
        ("Vinos por copa", [
            ("Tinto de la casa", "", "Copa de tinto de la casa"), ("Blanco de la casa", "", "Copa de blanco de la casa"),
            ("Rioja", "Campo Aldea, D.O.Ca. Rioja.", "Copa de Rioja"), ("Ribera roble", "Finca Engalia, D.O. Ribera del Duero.", "Copa de Ribera roble"),
            ("Verdejo", "Alijares, D.O. Rueda.", "Copa de Verdejo"), ("Albariño", "Rectoral do Umia, D.O. Rías Baixas.", "Copa de Albariño"),
            ("Rosado", "Viña Campus, D.O. Navarra.", "Copa de rosado"), ("Cava", "Jaume Serra brut nature.", "Copa de cava"),
        ]),
        ("Vinos por botella", [
            ("Botella de Rioja crianza", "El Coto, 75 cl.", "Botella de Rioja crianza"), ("Botella de Ribera roble", "Finca Engalia, 75 cl.", "Botella de Ribera roble"),
            ("Botella de Verdejo", "Cuatro Rayas, 75 cl.", "Botella de Verdejo"), ("Botella de Albariño", "Rectoral do Umia, 75 cl.", "Botella de Albariño"),
            ("Botella de rosado", "Zarzales, 75 cl.", "Botella de rosado"), ("Botella de cava", "Jaume Serra brut nature, 75 cl.", "Botella de cava"),
        ]),
        ("Refrescos y agua", [
            ("Coca-Cola", "", "Coca-Cola"), ("Coca-Cola Zero", "", "Coca-Cola Zero"), ("Fanta Naranja", "", "Fanta Naranja"),
            ("Fanta Limón", "", "Fanta Limón"), ("Sprite", "", "Sprite"), ("Fuze Tea", "", "Fuze Tea"), ("Aquarius limón", "", "Aquarius limón"),
            ("Tónica", "", "Tónica"), ("Red Bull", "", "Red Bull"), ("Mosto", "200 ml.", "Mosto"),
            ("Zumo de melocotón", "", "Zumo de melocotón"), ("Zumo de piña", "", "Zumo de piña"), ("Zumo de tomate", "", "Zumo de tomate"),
            ("Agua mineral", "50 cl.", "Agua mineral 50 cl"), ("Agua con gas", "Vichy Catalán, 30 cl.", "Agua con gas"),
        ]),
        ("Copas y chupitos", [
            ("Gin tonic", "", "Gin tonic"), ("Ron, whisky o vodka con refresco", "", 8.00),
            ("Chupitos", "Orujo de hierbas, crema de orujo, orujo blanco, pacharán, licor de café o limoncello.", 2.50),
        ]),
    ]),
    ("postres", "Postres", "", [
        ("", [
            ("Tarta de queso", "1 porción.", "Tarta de queso"),
            ("Helado de nata", "", "Helado de nata"), ("Helado de chocolate", "", "Helado de chocolate"), ("Helado mantecado", "", "Helado mantecado"),
        ]),
    ]),
]


def plato(ref):
    """(precio sala, id online o None, precio domicilio o None) de una referencia de CARTA."""
    if not isinstance(ref, str):
        return float(ref), None, None
    pid, sala, dom = FD[ref]          # KeyError = el nombre ya no está en Flight Director: revisa fd_carta.tsv
    if ref in SOLO_BARRA:
        return sala, None, None
    return sala, pid, dom
