# Web de Perito Moreno 360

Web del grupo (peritomoreno360.com): HTML estático + una función de Vercel para el formulario de contacto.

## Estructura
- `src/pages/` — contenido de cada página (solo el cuerpo).
- `tools/build.py` — genera `site/*.html` añadiendo cabecera, pie y formulario. Ejecuta `python3 tools/build.py` tras editar.
- `site/` — lo que se publica (HTML, `assets/css`, `assets/js`, `assets/img`).
- `api/contacto.js` — recibe el formulario y envía un aviso por email con Resend.
- `vercel.json` — publica `site/` con URLs limpias (`/apps`, `/flight-director`…).

## Formulario de contacto
Pide nombre, correo y teléfono. Para que llegue el correo a info@, en Vercel → Project → Settings → Environment Variables:
- `RESEND_API_KEY` — clave de resend.com (con el dominio peritomoreno360.com verificado).
- `CONTACT_TO` (opcional) — destinatario. Por defecto `info@peritomoreno360.com`.
- `CONTACT_FROM` (opcional) — remitente. Por defecto `onboarding@resend.dev`, que solo envía al email dueño de la cuenta de Resend (info@). Cuando verifiques el dominio en Resend, pon `Web Perito Moreno 360 <web@peritomoreno360.com>`.

Sin `RESEND_API_KEY` la web funciona, pero el formulario ofrece enviar los datos por email a info@.
