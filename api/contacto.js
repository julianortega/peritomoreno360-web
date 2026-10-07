// Recibe el formulario de contacto y envía un aviso por email.
//
// Opción principal: el buzón de IONOS (SMTP). Variables de entorno en Vercel:
//   SMTP_PASS   (obligatoria)  contraseña del buzón info@peritomoreno360.com
//   SMTP_USER   (opcional)     buzón que envía, por defecto info@peritomoreno360.com
//   SMTP_HOST   (opcional)     por defecto smtp.ionos.es
//   SMTP_PORT   (opcional)     por defecto 465 (SSL)
//   CONTACT_TO  (opcional)     destinatario, por defecto info@peritomoreno360.com
//
// Alternativa: Resend (si no hay SMTP_PASS y sí RESEND_API_KEY).

import nodemailer from 'nodemailer';

const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const clip = (s, n) => String(s ?? '').trim().slice(0, n);
const oneLine = (s) => String(s ?? '').replace(/[\r\n]+/g, ' ');

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

  const nombre = oneLine(clip(body.nombre, 120));
  const email = oneLine(clip(body.email, 160));
  const telefono = oneLine(clip(body.telefono, 40));
  const interes = oneLine(clip(body.interes, 80));
  const origen = oneLine(clip(body.origen, 120));

  const emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email);
  const telOk = /^[+0-9 ()-]{6,}$/.test(telefono);
  if (!nombre || !emailOk || !telOk) {
    return res.status(400).json({ error: 'datos' });
  }

  const to = process.env.CONTACT_TO || 'info@peritomoreno360.com';
  const fecha = new Date().toLocaleString('es-ES', { timeZone: 'Europe/Madrid' });
  const subject = `Contacto web: ${nombre}${interes ? ' · ' + interes : ''}`;

  const html = `
    <div style="font-family:Arial,sans-serif;font-size:15px;color:#17191F">
      <h2 style="margin:0 0 12px">Nueva persona interesada</h2>
      <p style="margin:0 0 16px;color:#55534C">Ha dejado sus datos en la web para que la contactéis. Si respondes a este correo, le llega a ella.</p>
      <table cellpadding="6" style="border-collapse:collapse">
        <tr><td><b>Nombre</b></td><td>${esc(nombre)}</td></tr>
        <tr><td><b>Email</b></td><td><a href="mailto:${esc(email)}">${esc(email)}</a></td></tr>
        <tr><td><b>Teléfono</b></td><td><a href="tel:${esc(telefono.replace(/\s/g, ''))}">${esc(telefono)}</a></td></tr>
        ${interes ? `<tr><td><b>Interés</b></td><td>${esc(interes)}</td></tr>` : ''}
        <tr><td><b>Página</b></td><td>${esc(origen)}</td></tr>
        <tr><td><b>Fecha</b></td><td>${esc(fecha)}</td></tr>
      </table>
    </div>`;

  const text = `Nueva persona interesada\n\nNombre: ${nombre}\nEmail: ${email}\nTeléfono: ${telefono}\n${interes ? `Interés: ${interes}\n` : ''}Página: ${origen}\nFecha: ${fecha}\n\nSi respondes a este correo, le llega a esta persona.`;

  try {
    if (process.env.SMTP_PASS) {
      const user = process.env.SMTP_USER || 'info@peritomoreno360.com';
      const port = Number(process.env.SMTP_PORT || 465);
      const transporter = nodemailer.createTransport({
        host: process.env.SMTP_HOST || 'smtp.ionos.es',
        port,
        secure: port === 465,
        auth: { user, pass: process.env.SMTP_PASS }
      });
      await transporter.sendMail({
        from: `"Web Perito Moreno 360" <${user}>`,
        to,
        replyTo: `"${nombre.replace(/"/g, '')}" <${email}>`,
        subject,
        text,
        html
      });
      return res.status(200).json({ ok: true });
    }

    if (process.env.RESEND_API_KEY) {
      const r = await fetch('https://api.resend.com/emails', {
        method: 'POST',
        headers: { Authorization: `Bearer ${process.env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({
          from: process.env.CONTACT_FROM || 'Web Perito Moreno 360 <onboarding@resend.dev>',
          to: [to],
          reply_to: email,
          subject,
          html,
          text
        })
      });
      if (!r.ok) {
        console.error('Resend', r.status, await r.text());
        return res.status(502).json({ error: 'envio' });
      }
      return res.status(200).json({ ok: true });
    }

    return res.status(503).json({ error: 'sin-configurar' });
  } catch (err) {
    console.error('Error enviando el formulario:', err && err.message);
    return res.status(502).json({ error: 'envio' });
  }
}
