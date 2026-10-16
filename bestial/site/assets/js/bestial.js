// Web de la marca: menú móvil, carrito (guardado en el navegador), montador del pedido y calculadora.
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var eur = function (x) { return x.toFixed(2).replace('.', ',') + ' €'; };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };

  // ---------- menú ----------
  var toggle = $('.nav-toggle'), nav = $('.nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) { nav.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); } });
  }
  $$('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });

  // ---------- carrito ----------
  var KEY = 'pedido-v1';
  function load() { try { return JSON.parse(localStorage.getItem(KEY)) || { lines: [], mode: 'domicilio' }; } catch (e) { return { lines: [], mode: 'domicilio' }; } }
  function save(c) { try { localStorage.setItem(KEY, JSON.stringify(c)); } catch (e) { /* sin almacenamiento: el pedido vive solo en esta página */ } }
  var cart = load();
  if (!cart.lines) cart = { lines: [], mode: 'domicilio' };

  function count() { return cart.lines.reduce(function (a, l) { return a + l.qty; }, 0); }
  function subtotal() { return cart.lines.reduce(function (a, l) { return a + l.unit * l.qty; }, 0); }
  function push(line) {
    var ex = cart.lines.filter(function (l) { return l.key === line.key; })[0];
    if (ex) ex.qty += 1; else cart.lines.push(line);
    save(cart); renderCart();
  }
  function step(key, d) {
    cart.lines = cart.lines.map(function (l) { if (l.key === key) l.qty += d; return l; }).filter(function (l) { return l.qty > 0; });
    save(cart); renderCart();
  }
  function renderCart() {
    var n = count();
    $$('[data-cart-count]').forEach(function (el) { el.textContent = n; el.classList.toggle('on', n > 0); });
    $$('[data-count]').forEach(function (el) { el.textContent = n === 1 ? '1 producto' : n + ' productos'; });
    $$('[data-lines]').forEach(function (box) {
      if (!cart.lines.length) { box.innerHTML = '<p class="empty">Tu pedido está vacío. Añade algo rico.</p>'; return; }
      box.innerHTML = cart.lines.map(function (l) {
        return '<div class="line"><div class="qty"><button type="button" data-step="-1" data-key="' + esc(l.key) + '" aria-label="Quitar uno">−</button><span>' + l.qty +
          '</span><button type="button" class="plus" data-step="1" data-key="' + esc(l.key) + '" aria-label="Añadir uno">+</button></div><div class="nm">' + esc(l.name) +
          (l.detail ? '<small>' + esc(l.detail) + '</small>' : '') + '</div><span class="pr">' + eur(l.unit * l.qty) + '</span></div>';
      }).join('');
    });
    var st = subtotal();
    $$('[data-subtotal]').forEach(function (el) { el.textContent = eur(st); });
    $$('[data-total]').forEach(function (el) { el.textContent = eur(st); });
    $$('[data-checkout]').forEach(function (el) { el.classList.toggle('btn-ink', !n); el.textContent = n ? 'Ir a pagar · ' + eur(st) : 'Añade algo para pedir'; if (!n) el.setAttribute('aria-disabled', 'true'); else el.removeAttribute('aria-disabled'); });
    $$('[data-ship-row]').forEach(function (el) { el.style.display = cart.mode === 'recoger' ? 'none' : ''; });
    $$('[data-only="domicilio"]').forEach(function (el) { el.style.display = cart.mode === 'recoger' ? 'none' : ''; });
    $$('[data-mode]').forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.mode === cart.mode ? 'true' : 'false'); });
    var bar = $('[data-cartbar]');
    if (bar) { bar.hidden = !n; $('[data-bar-count]', bar).textContent = 'Ver pedido · ' + n; $('[data-bar-total]', bar).textContent = eur(st); }
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-step]');
    if (b) { step(b.dataset.key, Number(b.dataset.step)); return; }
    var m = e.target.closest('[data-mode]');
    if (m) { cart.mode = m.dataset.mode; save(cart); renderCart(); return; }
    var c = e.target.closest('[data-checkout]');
    if (c && !count()) { e.preventDefault(); }
    var a = e.target.closest('[data-add]');
    if (a && window.CARTA && window.CARTA.products) {
      var p = window.CARTA.products[a.dataset.add];
      if (!p) return;
      push({ key: 'p:' + a.dataset.add, name: p.name, detail: '', unit: p.price, qty: 1 });
      a.classList.add('done'); a.textContent = '✓';
      setTimeout(function () { a.classList.remove('done'); a.textContent = '+'; }, 900);
    }
  });
  window.addEventListener('storage', function (e) { if (e.key === KEY) { cart = load(); renderCart(); } });
  renderCart();

  // ---------- montador (pedir) y calculadora (nutrición) ----------
  var root = $('[data-builder]');
  if (!root || !window.CARTA) return;
  var D = window.CARTA, kind = root.dataset.builder;
  function cloneSel(s) { var o = {}; D.groups.forEach(function (g) { o[g.key] = (s[g.key] || []).slice(); }); return o; }
  function defaults() { var o = {}; D.groups.forEach(function (g) { o[g.key] = g.items.filter(function (i) { return i.def; }).map(function (i) { return i.id; }); }); return o; }
  var sel = cloneSel(kind === 'calc' ? D.presets[0].sel : defaults());
  var label = '';

  function toggleOpt(g, id) {
    var cur = sel[g.key], on = cur.indexOf(id) >= 0;
    if (g.max === 1) sel[g.key] = on && g.min === 0 ? [] : [id];
    else if (on) sel[g.key] = cur.filter(function (x) { return x !== id; });
    else if (cur.length < g.max) sel[g.key] = cur.concat([id]);
    label = ''; render();
  }
  function calc() {
    var t = [0, 0, 0, 0, 0, 0, 0, 0], al = [], names = [], grams = 0, price = D.base || 0, hasProt = false, fmt = 'Burrito';
    D.groups.forEach(function (g) {
      g.items.forEach(function (it) {
        if (sel[g.key].indexOf(it.id) < 0) return;
        it.v.forEach(function (x, i) { t[i] += x; }); grams += it.g; price += it.price || 0;
        it.al.forEach(function (a) { if (al.indexOf(a) < 0) al.push(a); });
        names.push(it.name);
        if (g.key === 'proteina') hasProt = true;
        if (g.key === 'formato') fmt = it.name;
      });
    });
    return { t: t, al: al, names: names, grams: grams, price: price, hasProt: hasProt, fmt: fmt };
  }
  var groupsBox = $('[data-groups]', root), presetsBox = $('[data-presets]', root);
  presetsBox.innerHTML = D.presets.map(function (p, i) { return '<button type="button" data-preset="' + i + '">' + esc(p.name) + '</button>'; }).join('') +
    (kind === 'calc' ? '<button type="button" class="reset" data-preset="-1">Vaciar</button>' : '');
  presetsBox.addEventListener('click', function (e) {
    var b = e.target.closest('[data-preset]'); if (!b) return;
    var i = Number(b.dataset.preset);
    if (i < 0) { sel = cloneSel({}); label = ''; } else {
      var keep = sel.formato; sel = cloneSel(D.presets[i].sel);
      if (kind === 'shop' && keep && keep.length) sel.formato = keep.slice();
      label = D.presets[i].name;
    }
    render();
  });
  groupsBox.addEventListener('click', function (e) {
    var b = e.target.closest('[data-opt]'); if (!b) return;
    var g = D.groups[Number(b.dataset.g)]; toggleOpt(g, b.dataset.opt);
  });

  function render() {
    var c = calc();
    groupsBox.innerHTML = D.groups.map(function (g, gi) {
      var chips = g.items.map(function (it) {
        var on = sel[g.key].indexOf(it.id) >= 0;
        var meta = kind === 'shop'
          ? ((it.price ? '+' + eur(it.price) + ' · ' : (g.key === 'formato' || g.key === 'arroz' || g.key === 'proteina' || g.key === 'picante' ? 'Incluido · ' : '')) + Math.round(it.v[0]) + ' kcal')
          : ((it.g ? it.g + ' g · ' : '') + Math.round(it.v[0]) + ' kcal');
        if (g.key === 'picante') meta = 'Incluido';
        return '<button type="button" class="chip" data-g="' + gi + '" data-opt="' + esc(it.id) + '" aria-pressed="' + on + '">' + esc(it.name) + '<small>' + meta + '</small></button>';
      }).join('');
      return '<div class="grp"><div class="gt"><b><i>' + (gi + 1) + '</i> ' + esc(g.title) + '</b><span>' + esc(g.hint) + '</span></div><div class="chips">' + chips + '</div></div>';
    }).join('');
    var summary = c.names.length ? c.names.join(', ') : 'Elige ingredientes para empezar';
    $$('[data-summary]').forEach(function (el) { el.textContent = summary; });
    if (kind === 'shop') {
      $('[data-kcal]', root).textContent = Math.round(c.t[0]).toLocaleString('es-ES') + ' kcal';
      var btn = $('[data-add-custom]', root);
      btn.textContent = c.hasProt ? 'Añadir al pedido · ' + eur(c.price) : 'Elige una proteína';
      btn.disabled = !c.hasProt;
    } else {
      var IR = [2000, 70, 20, 260, 90, null, 50, 6];
      var L = ['Grasas', 'de las cuales saturadas', 'Hidratos de carbono', 'de los cuales azúcares', 'Fibra', 'Proteínas', 'Sal'];
      var f = function (x) { return (Math.round(x * 10) / 10).toLocaleString('es-ES') + ' g'; };
      var pct = function (x, r) { return r ? Math.round(x / r * 100) + '%' : '—'; };
      var bar = function (x, r) { return r ? Math.min(100, Math.round(x / r * 100)) + '%' : '0%'; };
      $('[data-kcal-big]').textContent = Math.round(c.t[0]).toLocaleString('es-ES');
      $('[data-grams]').textContent = Math.round(c.grams) + ' g · ' + pct(c.t[0], 2000) + ' IR';
      $('[data-kcal-bar]').style.width = bar(c.t[0], 2000);
      $('[data-rows]').innerHTML = L.map(function (l, j) {
        var sub = l.indexOf('de ') === 0;
        return '<div class="nrow"><span style="font-weight:' + (sub ? 500 : 700) + ';color:' + (sub ? '#CFCAC2' : '#fff') + '">' + l + '</span><span class="r"><b>' + f(c.t[j + 1]) +
          '</b><span class="mini"><i style="width:' + bar(c.t[j + 1], IR[j + 1]) + '"></i></span><span class="pct">' + pct(c.t[j + 1], IR[j + 1]) + '</span></span></div>';
      }).join('');
      $('[data-allergens]').textContent = c.al.length ? c.al.join(' · ') : 'Sin alérgenos principales en esta selección [pendiente de verificar]';
    }
  }
  var addBtn = $('[data-add-custom]', root);
  if (addBtn) addBtn.addEventListener('click', function () {
    var c = calc(); if (!c.hasProt) return;
    var name = (label ? label + ' · ' : '') + c.fmt + ' a tu medida';
    push({ key: 'c:' + JSON.stringify(sel), name: name, detail: c.names.slice(1).join(', ') + ' · ' + Math.round(c.t[0]) + ' kcal', unit: Math.round(c.price * 100) / 100, qty: 1 });
    addBtn.textContent = '¡Añadido!';
    setTimeout(render, 900);
  });
  render();
})();
