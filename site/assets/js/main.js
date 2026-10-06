// Perito Moreno 360 — menú móvil y formulario de contacto
(function () {
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') { nav.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); }
    });
  }

  var year = document.querySelectorAll('[data-year]');
  year.forEach(function (el) { el.textContent = new Date().getFullYear(); });

  var MAIL = 'info@peritomoreno360.com';

  document.querySelectorAll('form[data-contact]').forEach(function (form) {
    var status = form.querySelector('.form-status');
    var btn = form.querySelector('button[type="submit"]');

    function setStatus(msg, kind) {
      status.className = 'form-status' + (kind ? ' ' + kind : '');
      status.innerHTML = msg;
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;

      var data = {
        nombre: form.nombre.value.trim(),
        email: form.email.value.trim(),
        telefono: form.telefono.value.trim(),
        interes: form.interes ? form.interes.value : '',
        origen: form.dataset.origen || location.pathname,
        web: form.web ? form.web.value : ''
      };

      btn.disabled = true;
      var label = btn.textContent;
      btn.textContent = 'Enviando…';
      setStatus('', '');

      fetch('/api/contacto', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
        .then(function (r) { if (!r.ok) throw new Error(String(r.status)); return r.json(); })
        .then(function () {
          var name = form.querySelector('[data-name]');
          if (name) name.textContent = data.nombre.split(' ')[0];
          form.classList.add('sent');
        })
        .catch(function () {
          var body = 'Nombre: ' + data.nombre + '\nEmail: ' + data.email + '\nTeléfono: ' + data.telefono +
            (data.interes ? '\nInterés: ' + data.interes : '') + '\n\nMe gustaría que me contactéis.';
          var href = 'mailto:' + MAIL + '?subject=' + encodeURIComponent('Contacto desde la web' + (data.interes ? ' · ' + data.interes : '')) +
            '&body=' + encodeURIComponent(body);
          setStatus('No hemos podido enviar el formulario. <a href="' + href + '">Envíanoslo por email</a> o escríbenos a <a href="mailto:' + MAIL + '">' + MAIL + '</a>.', 'err');
        })
        .finally(function () { btn.disabled = false; btn.textContent = label; });
    });
  });
})();
