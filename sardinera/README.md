# Web de La Sardinera

Web estática de la marca, hecha igual que la de Bestial (`bestial/`): HTML + CSS + un JS pequeño, sin servidor.
Colores y tipografías del manual de marca (Brand Identity v3): azul sardinero #0D4765, rojo Mahou #C8102E, arena #F7F2E5; Amarante para títulos y Poppins para texto.

## Cambiar datos
Todo está en el bloque `CONFIG` al principio de `tools/build.py`: dominio, teléfono, correo, Instagram, sociedad titular, fecha de apertura, horario y datos del local.
La carta está en `tools/carta.py` (copiada de Flight Director, marca «La Sardinera», precios de sala).

Después: `python3 sardinera/tools/build.py` y sube los cambios.

## Publicarla en Vercel
1. Vercel → Add New → Project → este repositorio. Root Directory: `sardinera`. Framework: Other. Deploy.
2. Cuando haya dominio: Settings → Domains, y ponerlo en `DOMINIO` (genera canonical y sitemap).

## Pendiente
- Horario del local (`HORARIO`) y teléfono definitivo (ahora el provisional).
- Fotos reales del local y de los platos (de momento la web es tipográfica, sin fotos de banco de imágenes).
- Dominio propio y correo de contacto público.
