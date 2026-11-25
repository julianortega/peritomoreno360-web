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
