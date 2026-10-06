// Recibe el formulario de contacto y envía un aviso por email con Resend.
// Variables de entorno en Vercel:
//   RESEND_API_KEY  (obligatoria)  clave de https://resend.com
//   CONTACT_TO      (opcional)     destinatario, por defecto info@peritomoreno360.com
//   CONTACT_FROM    (opcional)     remitente verificado en Resend, por defecto web@peritomoreno360.com

const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const clip = (s, n) => String(s ?? '').trim().slice(0, n);

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

  const nombre = clip(body.nombre, 120);
  const email = clip(body.email, 160);
  const telefono = clip(body.telefono, 40);
  const interes = clip(body.interes, 80);
  const origen = clip(body.origen, 120);

  const emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email);
  const telOk = /^[+0-9 ()-]{6,}$/.test(telefono);
  if (!nombre || !emailOk || !telOk) {
    return res.status(400).json({ error: 'datos' });
  }

  const key = process.env.RESEND_API_KEY;
  if (!key) return res.status(503).json({ error: 'sin-configurar' });

  const to = process.env.CONTACT_TO || 'info@peritomoreno360.com';
  const from = process.env.CONTACT_FROM || 'Web Perito Moreno 360 <web@peritomoreno360.com>';
  const fecha = new Date().toLocaleString('es-ES', { timeZone: 'Europe/Madrid' });

  const html = `
    <div style="font-family:Arial,sans-serif;font-size:15px;color:#17191F">
      <h2 style="margin:0 0 12px">Nueva persona interesada</h2>
      <p style="margin:0 0 16px;color:#55534C">Ha dejado sus datos en la web para que la contactéis.</p>
      <table cellpadding="6" style="border-collapse:collapse">
        <tr><td><b>Nombre</b></td><td>${esc(nombre)}</td></tr>
        <tr><td><b>Email</b></td><td><a href="mailto:${esc(email)}">${esc(email)}</a></td></tr>
        <tr><td><b>Teléfono</b></td><td><a href="tel:${esc(telefono.replace(/\s/g, ''))}">${esc(telefono)}</a></td></tr>
        ${interes ? `<tr><td><b>Interés</b></td><td>${esc(interes)}</td></tr>` : ''}
        <tr><td><b>Página</b></td><td>${esc(origen)}</td></tr>
        <tr><td><b>Fecha</b></td><td>${esc(fecha)}</td></tr>
      </table>
    </div>`;

  const text = `Nueva persona interesada\n\nNombre: ${nombre}\nEmail: ${email}\nTeléfono: ${telefono}\n${interes ? `Interés: ${interes}\n` : ''}Página: ${origen}\nFecha: ${fecha}`;

  try {
    const r = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        from,
        to: [to],
        reply_to: email,
        subject: `Contacto web: ${nombre}${interes ? ' · ' + interes : ''}`,
        html,
        text
      })
    });
    if (!r.ok) {
      console.error('Resend', r.status, await r.text());
      return res.status(502).json({ error: 'envio' });
    }
    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error(err);
    return res.status(502).json({ error: 'envio' });
  }
}
