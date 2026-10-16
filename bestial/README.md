# Web de la marca de burritos (hoy «Bestial»)

Web estática propia de la marca, separada de la del grupo. HTML + CSS + un JS pequeño, sin servidor.

## Cambiar el nombre o el dominio
Todo está en el bloque `CONFIG` al principio de `tools/build.py`:
- `MARCA` y `MARCA_COMPLETA`: el nombre (p. ej. «Brutal» y «Brutal Burritos & Tacos»). Cambia también «Los Bestiales», «Dúo Bestial», etc.
- `LOGO`: con `"logo"` usa `site/assets/img/logo-negro.png` y `logo-blanco.png`. Si cambias de nombre, sustituye esas dos imágenes o pon `""` para usar el nombre en texto.
- `DOMINIO`: la dirección definitiva (p. ej. `https://www.brutalburritos.com`). Con él se generan el enlace canónico y el `sitemap.xml`.
- `EMAIL`, `INSTAGRAM`, `TIKTOK`, `TITULAR`, `CIF`, `DOMICILIO`, `LOCALES`.

Después: `python3 bestial/tools/build.py` y sube los cambios.

## Publicarla en Vercel (gratis) y cambiar la URL cuando quieras
1. En Vercel: Add New → Project → importa este mismo repositorio.
2. En «Root Directory» elige `bestial`. Framework: Other. Deploy.
3. Sale en una dirección provisional `….vercel.app` que puedes renombrar en Settings → General → Project Name.
4. Cuando tengas el dominio: Settings → Domains → añade el dominio y sigue los pasos de DNS. Pon ese dominio en `DOMINIO` y vuelve a generar.

## Estructura
- `src/pages/` — contenido de cada página. `{{MARCA}}` y demás se sustituyen al generar.
- `tools/carta.py` — carta, precios, grupos del montador y valores nutricionales (de Flight Director y del protocolo de cantidades).
- `tools/build.py` — genera `site/` (cabecera, pie, datos de la carta).
- `site/` — lo que se publica.

## Pendiente
Pasarela de pago y flota de reparto (la página de pago muestra el aviso), precio del envío, horarios de los locales, redes, correo, datos legales y vídeos (ver comentario en `src/pages/index.html`).
