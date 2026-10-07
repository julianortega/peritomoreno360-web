// Recibe el formulario de contacto, lo valida y lo pasa al script de Google
// (google-apps-script/Codigo.gs), que envía el correo a info@ y guarda la fila en Google Sheets.
//
// Variables de entorno en Vercel (después, Deployments → Redeploy):
//   APPS_SCRIPT_URL    URL de la aplicación web del script (termina en /exec)
//   APPS_SCRIPT_TOKEN  (opcional) la misma CLAVE que hay en el script

const clip = (s, n) => String(s ?? '').replace(/[\r\n]+/g, ' ').trim().slice(0, n);

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ error: 'method' });
  }

  let body = req.body;
  if (typeof body === 'string') {
    try { body = JSON.parse(body); } catch { body = {}; }
  }
  body = body || {};

  // Campo trampa para bots: si viene relleno, fingimos éxito y no enviamos nada.
  if (body.web) return res.status(200).json({ ok: true });

  const data = {
    nombre: clip(body.nombre, 120),
    email: clip(body.email, 160),
    telefono: clip(body.telefono, 40),
    interes: clip(body.interes, 80),
    origen: clip(body.origen, 120)
  };

  const emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(data.email);
  const telOk = /^[+0-9 ()-]{6,}$/.test(data.telefono);
  if (!data.nombre || !emailOk || !telOk) {
    return res.status(400).json({ error: 'datos' });
  }

  const url = process.env.APPS_SCRIPT_URL;
  const token = process.env.APPS_SCRIPT_TOKEN;
  if (!url) return res.status(503).json({ error: 'sin-configurar' });

  try {
    // Apps Script responde con una redirección; fetch la sigue y devuelve el JSON final.
    const r = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'text/plain;charset=utf-8' },
      body: JSON.stringify(token ? { ...data, token } : data),
      redirect: 'follow'
    });
    const txt = await r.text();
    let out = {};
    try { out = JSON.parse(txt); } catch { /* respuesta no JSON */ }
    if (!r.ok || !out.ok) {
      console.error('Apps Script', r.status, txt.slice(0, 300));
      return res.status(502).json({ error: 'envio' });
    }
    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error('Error enviando el formulario:', err && err.message);
    return res.status(502).json({ error: 'envio' });
  }
}
