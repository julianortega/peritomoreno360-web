/**
 * Formulario de www.peritomoreno360.com → correo a info@ + fila en esta hoja.
 *
 * Instalación (una sola vez):
 *  1. Crea una hoja de Google Sheets, por ejemplo "Contactos web".
 *  2. Extensiones → Apps Script. Borra lo que haya y pega este archivo. Cambia HOJA_ID por el ID de tu hoja.
 *  3. (Opcional) Pon una CLAVE y la misma en Vercel (APPS_SCRIPT_TOKEN).
 *  4. Implementar → Nueva implementación → Tipo: Aplicación web.
 *       Ejecutar como: Yo.   Quién tiene acceso: Cualquier usuario.
 *     Autoriza los permisos y copia la URL de la aplicación web (termina en /exec).
 *  5. En Vercel: APPS_SCRIPT_URL = esa URL (y APPS_SCRIPT_TOKEN si usas CLAVE). Después, Redeploy.
 */

// Opcional: si pones una clave aquí, pon la misma en Vercel (APPS_SCRIPT_TOKEN).
const CLAVE = '';
// info@ es un grupo: incluimos también tu buzón directamente porque Gmail no muestra
// en tu bandeja los correos que tú mismo envías a un grupo del que eres miembro.
const DESTINO = 'info@peritomoreno360.com, julian.ortega@peritomoreno360.com';
const HOJA = 'Contactos';
// ID de la hoja "Contactos web" (en una aplicación web no hay hoja "activa").
const HOJA_ID = '1RZMOGTY2ckHdPPu0vZnSqJdbL06eXdlbj0BiLHvMb9Y';

function doPost(e) {
  try {
    const d = JSON.parse((e && e.postData && e.postData.contents) || '{}');
    if (CLAVE && d.token !== CLAVE) return json_({ ok: false, error: 'token' });

    const nombre = limpia_(d.nombre, 120);
    const email = limpia_(d.email, 160);
    const telefono = limpia_(d.telefono, 40);
    const interes = limpia_(d.interes, 80);
    const origen = limpia_(d.origen, 120);
    if (!nombre || !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email) || !/^[+0-9 ()-]{6,}$/.test(telefono)) {
      return json_({ ok: false, error: 'datos' });
    }

    const fecha = Utilities.formatDate(new Date(), 'Europe/Madrid', 'dd/MM/yyyy HH:mm');

    // 1) Guardar en la hoja
    const ss = SpreadsheetApp.openById(HOJA_ID);
    let sh = ss.getSheetByName(HOJA) || ss.getSheets()[0];
    if (sh.getLastRow() === 0) {
      sh.appendRow(['Fecha', 'Nombre', 'Email', 'Teléfono', 'Interés', 'Página', 'Estado']);
      sh.setFrozenRows(1);
      sh.getRange('1:1').setFontWeight('bold');
    }
    sh.appendRow([fecha, nombre, email, "'" + telefono, interes, origen, 'Nuevo']);

    // 2) Enviar el aviso
    const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
    const fila = (k, v) => v ? `<tr><td><b>${k}</b></td><td>${v}</td></tr>` : '';
    const html =
      '<div style="font-family:Arial,sans-serif;font-size:15px;color:#17191F">' +
      '<h2 style="margin:0 0 12px">Nueva persona interesada</h2>' +
      '<p style="margin:0 0 16px;color:#55534C">Ha dejado sus datos en la web para que la contactéis. Si respondes a este correo, le llega a ella.</p>' +
      '<table cellpadding="6" style="border-collapse:collapse">' +
      fila('Nombre', esc(nombre)) +
      fila('Email', `<a href="mailto:${esc(email)}">${esc(email)}</a>`) +
      fila('Teléfono', `<a href="tel:${esc(telefono.replace(/\s/g, ''))}">${esc(telefono)}</a>`) +
      fila('Interés', esc(interes)) +
      fila('Página', esc(origen)) +
      fila('Fecha', esc(fecha)) +
      '</table>' +
      `<p style="margin-top:16px;color:#55534C">Guardado también en la hoja <a href="${ss.getUrl()}">${esc(ss.getName())}</a>.</p>` +
      '</div>';

    MailApp.sendEmail({
      to: DESTINO,
      replyTo: email,
      name: 'Web Perito Moreno 360',
      subject: `Contacto web: ${nombre}${interes ? ' · ' + interes : ''}`,
      htmlBody: html,
      body: `Nueva persona interesada\n\nNombre: ${nombre}\nEmail: ${email}\nTeléfono: ${telefono}\nInterés: ${interes}\nPágina: ${origen}\nFecha: ${fecha}`
    });

    return json_({ ok: true });
  } catch (err) {
    console.error(err);
    return json_({ ok: false, error: 'interno', detalle: String(err && err.message || err) });
  }
}

function limpia_(s, n) {
  return String(s == null ? '' : s).replace(/[\r\n]+/g, ' ').trim().slice(0, n);
}

function json_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}

// Prueba manual desde el editor (Ejecutar → probar)
function probar() {
  const r = doPost({ postData: { contents: JSON.stringify({ nombre: 'PRUEBA (puedes borrarla)', email: 'julian.ortega@peritomoreno360.com', telefono: '600000000', interes: 'Otro', origen: 'Prueba desde el editor' }) } });
  console.log(r.getContent());
}
