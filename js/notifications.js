/* WeDo Market — раздел «Уведомления»: вкладки «Быстрая настройка» / «Расширенные» */
(function () {
  'use strict';

  var root = document.querySelector('.notif');
  if (!root) return;

  var tabs = root.querySelectorAll('.notif__tab');
  var panes = root.querySelectorAll('.notif__pane');

  var activate = function (key) {
    tabs.forEach(function (t) {
      var on = t.getAttribute('data-tab') === key;
      t.classList.toggle('is-active', on);
      t.setAttribute('aria-selected', on ? 'true' : 'false');
    });
    panes.forEach(function (p) {
      var on = p.id === 'notif-pane-' + key;
      p.classList.toggle('is-active', on);
      p.hidden = !on;
    });
  };

  tabs.forEach(function (t) {
    t.addEventListener('click', function () {
      activate(t.getAttribute('data-tab'));
      if (history.replaceState) history.replaceState(null, '', '#' + t.getAttribute('data-tab'));
    });
  });

  /* #advanced в адресе открывает вкладку «Расширенные» */
  var m = /^#(quick|advanced)$/.exec(location.hash);
  if (m) activate(m[1]);
})();
