# Web de Perito Moreno 360

Web del grupo (peritomoreno360.com): HTML estático + una función de Vercel para el formulario de contacto.

## Estructura
- `src/pages/` — contenido de cada página (solo el cuerpo).
- `tools/build.py` — genera `site/*.html` añadiendo cabecera, pie y formulario. Ejecuta `python3 tools/build.py` tras editar.
- `site/` — lo que se publica (HTML, `assets/css`, `assets/js`, `assets/img`).
- `api/contacto.js` — recibe el formulario y envía un aviso por email con Resend.
- `vercel.json` — publica `site/` con URLs limpias (`/apps`, `/flight-director`…).

## Formulario de contacto
Pide nombre, correo y teléfono y envía un aviso a info@ desde el propio buzón de IONOS.
En Vercel → Project → Settings → Environment Variables:
- `SMTP_PASS` — contraseña del buzón info@peritomoreno360.com (obligatoria).
- `SMTP_USER`, `SMTP_HOST`, `SMTP_PORT`, `CONTACT_TO` (opcionales) — por defecto info@peritomoreno360.com, smtp.ionos.es, 465 e info@peritomoreno360.com.

Tras añadir o cambiar una variable hay que volver a desplegar (Deployments → Redeploy).
Sin configurar, la web funciona y el formulario ofrece enviar los datos por email a info@.
