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

  document.querySelectorAll('.dd-btn').forEach(function (b) {
    b.addEventListener('click', function () {
      var dd = b.parentNode, open = !dd.classList.contains('open');
      document.querySelectorAll('.dd.open').forEach(function (o) { o.classList.remove('open'); o.firstElementChild.setAttribute('aria-expanded', 'false'); });
      if (open) { dd.classList.add('open'); b.setAttribute('aria-expanded', 'true'); }
    });
  });
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.dd')) document.querySelectorAll('.dd.open').forEach(function (o) { o.classList.remove('open'); o.firstElementChild.setAttribute('aria-expanded', 'false'); });
  });

  var year = document.querySelectorAll('[data-year]');
  year.forEach(function (el) { el.textContent = new Date().getFullYear(); });

  var MAIL = 'info@peritomoreno360.com';
  var EN = document.documentElement.lang === 'en';
  var T = EN ? {
    sending: 'Sending…', name: 'Name', phone: 'Phone', interest: 'Interest',
    ask: 'I would like you to contact me.', subject: 'Contact from the website (EN)',
    fail: function (href) { return 'We couldn\'t send the form. <a href="' + href + '">Send it to us by email</a> or write to us at <a href="mailto:' + MAIL + '">' + MAIL + '</a>.'; }
  } : {
    sending: 'Enviando…', name: 'Nombre', phone: 'Teléfono', interest: 'Interés',
    ask: 'Me gustaría que me contactéis.', subject: 'Contacto desde la web',
    fail: function (href) { return 'No hemos podido enviar el formulario. <a href="' + href + '">Envíanoslo por email</a> o escríbenos a <a href="mailto:' + MAIL + '">' + MAIL + '</a>.'; }
  };

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
        interes: [form.interes ? form.interes.value : '',
          form.tamano && form.tamano.value.trim() ? (form.tamano.labels[0].textContent.indexOf('equipos') > -1 ? 'equipos: ' : 'locales: ') + form.tamano.value.trim() : '',
          form.cuando ? 'demo: ' + form.cuando.value.toLowerCase() : ''].filter(Boolean).join(' · '),
        origen: form.dataset.origen || location.pathname,
        web: form.web ? form.web.value : ''
      };

      btn.disabled = true;
      var label = btn.textContent;
      btn.textContent = T.sending;
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
          var body = T.name + ': ' + data.nombre + '\nEmail: ' + data.email + '\n' + T.phone + ': ' + data.telefono +
            (data.interes ? '\n' + T.interest + ': ' + data.interes : '') + '\n\n' + T.ask;
          var href = 'mailto:' + MAIL + '?subject=' + encodeURIComponent(T.subject + (data.interes ? ' · ' + data.interes : '')) +
            '&body=' + encodeURIComponent(body);
          setStatus(T.fail(href), 'err');
        })
        .finally(function () { btn.disabled = false; btn.textContent = label; });
    });
  });
})();
