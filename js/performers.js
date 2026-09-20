/* WeDo Market — раздел «Исполнители и профиль»: сброс фильтров, вкладки отзывов «Как исполнитель» / «Как заказчик» */
(function () {
  'use strict';

  /* ---- Исполнители: «Сбросить» возвращает селекты к первому значению ---- */
  var filters = document.querySelector('.perf-filters');
  if (filters) {
    filters.addEventListener('reset', function (e) {
      e.preventDefault();
      filters.querySelectorAll('select').forEach(function (s) { s.selectedIndex = 0; });
    });
  }

  /* ---- Профиль: вкладки отзывов ---- */
  var reviews = document.querySelector('.profile-reviews');
  if (!reviews) return;

  var tabs = reviews.querySelectorAll('.profile-tab');
  var panes = reviews.querySelectorAll('.profile-pane');

  var activate = function (key) {
    tabs.forEach(function (t) {
      var on = t.getAttribute('data-tab') === key;
      t.classList.toggle('is-active', on);
      t.setAttribute('aria-selected', on ? 'true' : 'false');
    });
    panes.forEach(function (p) {
      p.hidden = p.id !== 'profile-pane-' + key;
    });
  };

  tabs.forEach(function (t) {
    t.addEventListener('click', function () {
      activate(t.getAttribute('data-tab'));
      if (history.replaceState) history.replaceState(null, '', '#' + t.getAttribute('data-tab'));
    });
  });

  /* #customer в адресе открывает вкладку «Как заказчик» */
  var m = /^#(performer|customer)$/.exec(location.hash);
  if (m) activate(m[1]);
})();
