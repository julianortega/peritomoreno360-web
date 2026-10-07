# Web de Perito Moreno 360

Web del grupo (peritomoreno360.com): HTML estático + una función de Vercel para el formulario de contacto.

## Estructura
- `src/pages/` — contenido de cada página (solo el cuerpo).
- `tools/build.py` — genera `site/*.html` añadiendo cabecera, pie y formulario. Ejecuta `python3 tools/build.py` tras editar.
- `site/` — lo que se publica (HTML, `assets/css`, `assets/js`, `assets/img`).
- `api/contacto.js` — recibe el formulario y envía un aviso por email con Resend.
- `vercel.json` — publica `site/` con URLs limpias (`/apps`, `/flight-director`…).

## Formulario de contacto
Pide nombre, correo y teléfono y envía un aviso a info@peritomoreno360.com (grupo de Google que reenvía a los miembros). Si se responde al aviso, la respuesta va directa a la persona interesada.

En Vercel → Project → Settings → Environment Variables (después, Deployments → Redeploy):
- `RESEND_API_KEY` — clave de resend.com. La cuenta de Resend está creada con info@, por eso puede enviar desde onboarding@resend.dev sin verificar el dominio.
- `CONTACT_TO` (opcional) — destinatario, por defecto info@peritomoreno360.com.
- `CONTACT_FROM` (opcional) — remitente. Si se verifica el dominio en Resend: `Web Perito Moreno 360 <web@peritomoreno360.com>`.
- Alternativa: `SMTP_PASS` (+ `SMTP_USER`, `SMTP_HOST`, `SMTP_PORT`) para enviar por SMTP de un buzón con contraseña. Si existe, tiene prioridad sobre Resend.

Sin configurar, la web funciona y el formulario ofrece enviar los datos por email a info@.
