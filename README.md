# Web de Perito Moreno 360

Web del grupo (peritomoreno360.com): HTML estático + una función de Vercel para el formulario de contacto.

## Estructura
- `src/pages/` — contenido de cada página (solo el cuerpo).
- `tools/build.py` — genera `site/*.html` añadiendo cabecera, pie y formulario. Ejecuta `python3 tools/build.py` tras editar.
- `site/` — lo que se publica (HTML, `assets/css`, `assets/js`, `assets/img`).
- `api/contacto.js` — recibe el formulario y envía un aviso por email con Resend.
- `vercel.json` — publica `site/` con URLs limpias (`/apps`, `/flight-director`…).

## Formulario de contacto
Pide nombre, correo y teléfono. `api/contacto.js` valida los datos y los pasa a un script de Google
(`google-apps-script/Codigo.gs`) que envía el aviso a info@ (grupo de Google) y guarda una fila en Google Sheets.
Si se responde al aviso, la respuesta va directa a la persona interesada.

Instalación del script: ver las instrucciones al principio de `google-apps-script/Codigo.gs`.

En Vercel → Project → Settings → Environment Variables (después, Deployments → Redeploy):
- `APPS_SCRIPT_URL` — URL de la aplicación web del script (termina en `/exec`).
- `APPS_SCRIPT_TOKEN` — la misma CLAVE que hay en el script.

Sin configurar, la web funciona y el formulario ofrece enviar los datos por email a info@.
