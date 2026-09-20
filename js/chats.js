/* WeDo Market — раздел «Чаты»: поиск по списку, отправка сообщения, панель вложений (вкладки Фото/Файлы/Видео) */
(function () {
  'use strict';

  /* ---- Поиск по имени в списке чатов ---- */
  var search = document.getElementById('chats-search');
  var list = document.getElementById('chats-list');
  if (search && list) {
    var empty = document.getElementById('chats-empty');
    var items = Array.prototype.slice.call(list.querySelectorAll('.chats__item'));
    var filter = function () {
      var q = search.value.trim().toLowerCase();
      var shown = 0;
      items.forEach(function (li) {
        var hit = !q || (li.getAttribute('data-name') || '').indexOf(q) !== -1;
        li.classList.toggle('is-hidden', !hit);
        if (hit) shown++;
      });
      if (empty) empty.hidden = shown > 0;
    };
    search.addEventListener('input', filter);
    search.addEventListener('search', filter);
  }

  /* ---- Отправка сообщения ---- */
  var form = document.getElementById('chat-form');
  var thread = document.getElementById('chat-thread');
  if (form && thread) {
    var input = document.getElementById('chat-msg');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var text = input.value.trim();
      if (!text) return;
      var msg = document.createElement('div');
      msg.className = 'msg msg--out';
      var p = document.createElement('p');
      p.className = 'msg__text';
      p.textContent = text;
      msg.appendChild(p);
      thread.appendChild(msg);
      input.value = '';
      window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
    });
  }

  /* ---- Голосовые: имитация play/pause ---- */
  document.querySelectorAll('.voice__play').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var playing = btn.classList.toggle('is-playing');
      btn.setAttribute('aria-label', playing ? 'Пауза' : 'Воспроизвести голосовое сообщение');
    });
  });

  /* ---- Панель вложений (Photo Picker) ---- */
  var picker = document.getElementById('chat-picker');
  if (picker) {
    var overlay = document.getElementById('chat-overlay');
    var attachBtn = document.getElementById('chat-attach-btn');
    var tabs = picker.querySelectorAll('.picker__tab');
    var panes = picker.querySelectorAll('.picker__pane');

    var open = function () {
      picker.hidden = false;
      if (overlay) overlay.hidden = false;
      document.body.classList.add('picker-open');
      if (attachBtn) attachBtn.setAttribute('aria-expanded', 'true');
    };
    var close = function () {
      picker.hidden = true;
      if (overlay) overlay.hidden = true;
      document.body.classList.remove('picker-open');
      if (attachBtn) attachBtn.setAttribute('aria-expanded', 'false');
    };
    var activate = function (key) {
      tabs.forEach(function (t) {
        var on = t.getAttribute('data-tab') === key;
        t.classList.toggle('is-active', on);
        t.setAttribute('aria-selected', on ? 'true' : 'false');
      });
      panes.forEach(function (p) {
        var on = p.id === 'picker-pane-' + key;
        p.classList.toggle('is-active', on);
        p.hidden = !on;
      });
    };

    tabs.forEach(function (t) {
      t.addEventListener('click', function () { activate(t.getAttribute('data-tab')); });
    });
    if (overlay) overlay.addEventListener('click', close);
    if (attachBtn) attachBtn.addEventListener('click', function () { picker.hidden ? open() : close(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !picker.hidden) close(); });

    /* На странице chat-attach.html панель открыта сразу; ?tab=files|video выбирает вкладку */
    var m = /[?&]tab=(photo|files|video)/.exec(location.search);
    activate(m ? m[1] : 'photo');
    open();
  }
})();
