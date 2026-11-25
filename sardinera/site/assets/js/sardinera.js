// Web de La Sardinera: menú móvil, año del pie y sección activa en la carta.
(function () {
  var t = document.querySelector('.nav-toggle'), n = document.getElementById('menu');
  if (t && n) t.addEventListener('click', function () {
    var o = n.classList.toggle('open'); t.setAttribute('aria-expanded', o ? 'true' : 'false');
  });
  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
  var links = document.querySelectorAll('.subnav a');
  if (links.length && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (!en.isIntersecting) return;
        links.forEach(function (a) {
          var on = a.getAttribute('href') === '#' + en.target.id;
          a.classList.toggle('on', on);
          if (on && a.scrollIntoView) a.parentNode.scrollTo({ left: a.offsetLeft - 16, behavior: 'smooth' });
        });
      });
    }, { rootMargin: '-40% 0px -55% 0px' });
    document.querySelectorAll('.menu-sec').forEach(function (s) { io.observe(s); });
  }
})();

// ---------- Pide online: cesta, modo (domicilio / recoger) y pago ----------
(function () {
  var C = window.SARDINERA, shop = document.querySelector('[data-shop]');
  var eur = function (n) { return n.toFixed(2).replace('.', ',') + ' €'; };
  var get = function (k, d) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } };
  var put = function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} };

  // Página de vuelta del pago
  var est = document.querySelector('[data-estado]');
  if (est) {
    var q = new URLSearchParams(location.search), r = q.get('r'), t = q.get('t');
    var cual = r === 'ok' ? 'ok' : r === 'espera' ? 'espera' : 'ko';
    est.querySelector('.estado-' + cual).hidden = false;
    if (cual === 'ok') put('sard_cesta', {});
    var re = est.querySelector('[data-retry]');
    if (re && t && /^[a-f0-9]{32}$/.test(t) && C) re.href = C.api + '/pedido-web/' + t;
    return;
  }
  if (!shop || !C) return;

  var items = {};
  shop.querySelectorAll('li[data-id]').forEach(function (li) {
    items[li.dataset.id] = { li: li, name: li.querySelector('h4').textContent, sala: +li.dataset.sala, dom: li.dataset.dom === '' ? null : +li.dataset.dom };
  });
  var cesta = get('sard_cesta', {}), modo = C.domicilio ? get('sard_modo', 'domicilio') : 'recoger';
  Object.keys(cesta).forEach(function (id) { if (!items[id]) delete cesta[id]; });
  var precio = function (it) { return modo === 'domicilio' ? it.dom : it.sala; };

  var $ = function (s) { return document.querySelectorAll(s); };
  var form = document.querySelector('[data-checkout]'), err = document.querySelector('[data-err]'), warn = document.querySelector('[data-warn]');

  // Horas: cada 15 min desde dentro de 30 min hasta las 23:30 (el local confirma si no llega).
  var sel = document.getElementById('p-hora');
  (function () {
    var d = new Date(Date.now() + 45 * 60000); d.setMinutes(Math.ceil(d.getMinutes() / 15) * 15, 0, 0);
    var fin = new Date(); fin.setHours(23, 30, 0, 0);
    for (; d <= fin; d = new Date(d.getTime() + 15 * 60000)) {
      var h = String(d.getHours()).padStart(2, '0') + ':' + String(d.getMinutes()).padStart(2, '0');
      var o = document.createElement('option'); o.value = h; o.textContent = 'Hoy a las ' + h; sel.appendChild(o);
    }
  })();

  function pinta() {
    $('[data-mode]').forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.mode === modo ? 'true' : 'false'); if (b.dataset.mode === 'domicilio' && !C.domicilio) b.hidden = true; });
    var info = document.querySelector('[data-mode-info]');
    if (info) info.textContent = modo === 'domicilio' ? 'Llevamos a ' + C.cps.join(', ') + ' · envío ' + eur(C.envio) + ' · pedido mínimo ' + eur(C.minimo) : 'Pide ahora y pasa a recogerlo por Av. de los Reyes Católicos, 8. Sin esperas.';
    $('[data-only="domicilio"]').forEach(function (el) { el.hidden = modo !== 'domicilio'; });
    var lines = document.querySelector('[data-lines]'), html = '', sub = 0, n = 0, fuera = [];
    Object.keys(items).forEach(function (id) {
      var it = items[id], p = precio(it), q = cesta[id] || 0;
      it.li.classList.toggle('off', p === null);
      it.li.querySelector('.p').textContent = eur(p === null ? it.sala : p);
      it.li.classList.toggle('in', q > 0);
      if (!q) return;
      if (p === null) { fuera.push(it.name); return; }
      sub += p * q; n += q;
      html += '<div class="line"><span class="q"><button type="button" data-menos="' + id + '" aria-label="Quitar uno">−</button><b>' + q + '</b><button type="button" data-mas="' + id + '" aria-label="Añadir uno">+</button></span><span class="nm">' + it.name + '</span><span class="pr">' + eur(p * q) + '</span></div>';
    });
    lines.innerHTML = html || '<p class="mut">Todavía no has añadido nada. ¡Empieza por un pincho de tortilla!</p>';
    var envio = modo === 'domicilio' && n ? C.envio : 0, total = sub + envio;
    document.querySelector('[data-subtotal]').textContent = eur(sub);
    document.querySelector('[data-ship-row]').hidden = modo !== 'domicilio';
    $('[data-total]').forEach(function (el) { el.textContent = eur(total); });
    var w = '';
    if (fuera.length) w = 'A domicilio no llevamos: ' + fuera.join(', ') + '. Se quedan en la cesta si eliges recoger.';
    else if (modo === 'domicilio' && n && sub < C.minimo) w = 'Te faltan ' + eur(C.minimo - sub) + ' para el pedido mínimo a domicilio.';
    warn.hidden = !w; warn.textContent = w;
    form.hidden = !n;
    var bar = document.querySelector('[data-cartbar]');
    bar.hidden = !n;
    document.querySelector('[data-bar-count]').textContent = n + (n === 1 ? ' producto' : ' productos');
    document.querySelector('[data-bar-total]').textContent = 'Ver pedido · ' + eur(total);
    put('sard_cesta', cesta); put('sard_modo', modo);
    return { sub: sub, n: n };
  }

  shop.addEventListener('click', function (ev) {
    var b = ev.target.closest('.add'); if (!b) return;
    var li = b.closest('li'), it = items[li.dataset.id];
    if (precio(it) === null) return;
    cesta[li.dataset.id] = (cesta[li.dataset.id] || 0) + 1;
    li.classList.remove('pop'); void li.offsetWidth; li.classList.add('pop');
    pinta();
  });
  document.querySelector('[data-lines]').addEventListener('click', function (ev) {
    var mas = ev.target.closest('[data-mas]'), menos = ev.target.closest('[data-menos]');
    if (mas) cesta[mas.dataset.mas] = Math.min(30, (cesta[mas.dataset.mas] || 0) + 1);
    if (menos) { var id = menos.dataset.menos; cesta[id] = (cesta[id] || 0) - 1; if (cesta[id] <= 0) delete cesta[id]; }
    pinta();
  });
  $('[data-mode]').forEach(function (b) { b.addEventListener('click', function () { modo = b.dataset.mode; pinta(); }); });

  var metodo = 'tarjeta';
  form.querySelectorAll('[data-pay]').forEach(function (b) { b.addEventListener('click', function () { metodo = b.dataset.pay; }); });
  form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    var f = new FormData(form), estado = pinta(), fallo = '';
    var lineas = Object.keys(cesta).filter(function (id) { return precio(items[id]) !== null; }).map(function (id) { return { id: id, cantidad: cesta[id] }; });
    if (!C.online) fallo = 'Los pedidos online empiezan muy pronto. Mientras, llámanos.';
    else if (!lineas.length) fallo = 'Tu pedido está vacío.';
    else if (!String(f.get('nombre')).trim()) fallo = 'Pon tu nombre.';
    else if (String(f.get('telefono')).replace(/\D/g, '').length < 9) fallo = 'Pon un teléfono para avisarte.';
    else if (modo === 'domicilio' && !String(f.get('direccion')).trim()) fallo = 'Falta la dirección de entrega.';
    else if (modo === 'domicilio' && C.cps.indexOf(String(f.get('cp')).trim()) < 0) fallo = 'De momento llevamos a ' + C.cps.join(', ') + '. Puedes elegir recoger.';
    else if (modo === 'domicilio' && estado.sub < C.minimo) fallo = 'El pedido mínimo a domicilio es de ' + eur(C.minimo) + '.';
    else if (!f.get('acepto')) fallo = 'Acepta las condiciones para seguir.';
    err.hidden = !fallo; err.textContent = fallo;
    if (fallo) return;
    var btns = form.querySelectorAll('[data-pay]'); btns.forEach(function (b) { b.disabled = true; });
    fetch(C.api + '/api/pedidos-web', {
      method: 'POST', headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ marca: C.marca, modo: modo, nombre: f.get('nombre'), telefono: f.get('telefono'), email: f.get('email'),
        direccion: f.get('direccion'), cp: f.get('cp'), hora: f.get('hora'), alergia: f.get('alergia'), nota: f.get('nota'), lineas: lineas })
    }).then(function (r) { return r.json(); }).then(function (d) {
      if (!d || !d.url) throw new Error((d && d.error) || 'No hemos podido hacer el pedido.');
      location.href = d.url + (metodo === 'bizum' ? '?metodo=bizum' : '');
    }).catch(function (e) {
      err.hidden = false; err.textContent = e.message && e.message !== 'Failed to fetch' ? e.message : 'No hemos podido conectar. Inténtalo otra vez o llámanos.';
      btns.forEach(function (b) { b.disabled = false; });
    });
  });
  pinta();
})();
