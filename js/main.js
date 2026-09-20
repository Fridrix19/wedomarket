/* WeDo Market — интерактив: меню пользователя, аккордеон сайдбара, график, дропзона, капча */
(function () {
  'use strict';

  /* ---- Выпадающее меню пользователя ---- */
  document.querySelectorAll('.user').forEach(function (user) {
    var btn = user.querySelector('.user__btn');
    if (!btn) return;
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      user.classList.toggle('is-open');
      btn.setAttribute('aria-expanded', user.classList.contains('is-open'));
    });
  });
  document.addEventListener('click', function () {
    document.querySelectorAll('.user.is-open').forEach(function (u) {
      u.classList.remove('is-open');
      var b = u.querySelector('.user__btn');
      if (b) b.setAttribute('aria-expanded', 'false');
    });
  });

  /* ---- Мобильная нижняя навигация: меню «ещё» ---- */
  document.querySelectorAll('.m-nav').forEach(function (nav) {
    var more = nav.querySelector('.m-nav__btn--more');
    if (!more) return;
    more.addEventListener('click', function (e) {
      e.stopPropagation();
      nav.classList.toggle('is-open');
      more.setAttribute('aria-expanded', nav.classList.contains('is-open'));
    });
    document.addEventListener('click', function (e) {
      if (!nav.contains(e.target)) { nav.classList.remove('is-open'); more.setAttribute('aria-expanded', 'false'); }
    });
  });

  /* ---- Аккордеон "Задания" в сайдбаре ---- */
  document.querySelectorAll('.sidebar__toggle').forEach(function (toggle) {
    toggle.addEventListener('click', function () {
      var item = toggle.closest('.sidebar__item');
      item.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', item.classList.contains('is-open'));
    });
  });

  /* ---- График "Завершенные задания" ---- */
  document.querySelectorAll('[data-chart]').forEach(function (el) {
    var values;
    try { values = JSON.parse(el.getAttribute('data-chart')); } catch (e) { values = []; }
    var labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    if (values.length !== 12) values = new Array(12).fill(0);
    var W = 683, H = 278, padL = 40, padR = 12, padT = 12, padB = 32;
    var max = Math.max(5, Math.ceil(Math.max.apply(null, values)));
    var stepsY = 5;
    var x = function (i) { return padL + (W - padL - padR) * i / 11; };
    var y = function (v) { return padT + (H - padT - padB) * (1 - v / max); };
    var svg = '<svg viewBox="0 0 ' + W + ' ' + H + '" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="График завершенных заданий по месяцам">';
    for (var i = 0; i <= stepsY; i++) {
      var v = max * i / stepsY, yy = y(v);
      svg += '<line class="chart__grid" x1="' + padL + '" y1="' + yy + '" x2="' + (W - padR) + '" y2="' + yy + '"/>';
      svg += '<text class="chart__label" x="' + (padL - 8) + '" y="' + (yy + 4) + '" text-anchor="end">' + v.toFixed(1) + '</text>';
    }
    for (var j = 0; j < 12; j++) {
      svg += '<line class="chart__grid" x1="' + x(j) + '" y1="' + padT + '" x2="' + x(j) + '" y2="' + (H - padB) + '"/>';
      svg += '<text class="chart__label" x="' + x(j) + '" y="' + (H - 10) + '" text-anchor="middle">' + labels[j] + '</text>';
    }
    var d = values.map(function (v, k) { return (k ? 'L' : 'M') + x(k) + ' ' + y(v); }).join(' ');
    svg += '<path class="chart__line" d="' + d + '"/>';
    values.forEach(function (v, k) { svg += '<circle class="chart__dot" cx="' + x(k) + '" cy="' + y(v) + '" r="5"/>'; });
    svg += '</svg>';
    el.innerHTML = svg;
  });

  /* ---- Быстрые даты "Сегодня / Завтра" ---- */
  function fmt(d) {
    var p = function (n) { return (n < 10 ? '0' : '') + n; };
    return p(d.getDate()) + '.' + p(d.getMonth() + 1) + '.' + d.getFullYear();
  }
  document.querySelectorAll('.quick-dates button').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var wrap = btn.closest('.date-field');
      var input = wrap && wrap.querySelector('input');
      if (!input) return;
      var d = new Date();
      if (btn.dataset.date === 'tomorrow') d.setDate(d.getDate() + 1);
      input.value = fmt(d);
    });
  });

  /* ---- Дропзона видео ---- */
  document.querySelectorAll('.dropzone').forEach(function (zone) {
    var input = zone.querySelector('input[type="file"]');
    zone.addEventListener('click', function (e) {
      if (e.target.closest('.dropzone__btn')) return;
      if (input) input.click();
    });
    ['dragenter', 'dragover'].forEach(function (ev) {
      zone.addEventListener(ev, function (e) { e.preventDefault(); zone.classList.add('is-dragover'); });
    });
    ['dragleave', 'drop'].forEach(function (ev) {
      zone.addEventListener(ev, function (e) { e.preventDefault(); zone.classList.remove('is-dragover'); });
    });
    zone.addEventListener('drop', function (e) {
      if (input && e.dataTransfer && e.dataTransfer.files.length) {
        input.files = e.dataTransfer.files;
        showFile(zone, input.files[0]);
      }
    });
    if (input) input.addEventListener('change', function () { if (input.files[0]) showFile(zone, input.files[0]); });
  });
  function showFile(zone, file) {
    var t = zone.querySelector('.dropzone__text');
    if (t) t.textContent = file.name;
  }

  /* ---- Кнопка выбора файла (шаг 5 / форма) ---- */
  document.querySelectorAll('.file-pick').forEach(function (fp) {
    var btn = fp.querySelector('.btn--pill');
    var input = fp.querySelector('input[type="file"]');
    var hint = fp.querySelector('.file-pick__hint');
    if (!btn || !input) return;
    btn.addEventListener('click', function () { input.click(); });
    input.addEventListener('change', function () {
      if (!hint) return;
      var names = Array.prototype.map.call(input.files, function (f) { return f.name; });
      if (names.length) hint.textContent = 'Выбрано: ' + names.join(', ');
    });
  });

  /* ---- Капча (имитация) ---- */
  document.querySelectorAll('.captcha').forEach(function (c) {
    var box = c.querySelector('.captcha__box');
    if (!box) return;
    box.addEventListener('click', function () {
      box.classList.toggle('is-checked');
      box.setAttribute('aria-checked', box.classList.contains('is-checked'));
    });
  });
})();
