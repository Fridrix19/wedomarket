/* WeDo Market — раздел «Задания» (мобилка): панель «Совет ИИ», переключатели ИИ-рекомендаций,
   раскрытие карточек «Подробнее», счётчики символов, слайдер бюджета, ссылка «Файлы» */
(function () {
  'use strict';
  var isMobile = window.matchMedia('(max-width: 767px)');

  /* ---- Панель «Совет ИИ» (шаг 7) ---- */
  var panel = document.getElementById('ai-panel');
  if (panel) {
    var openBtns = document.querySelectorAll('[data-ai-open]');
    function setPanel(open) {
      panel.hidden = !open;
      document.body.classList.toggle('ai-open', open);
      openBtns.forEach(function (b) { b.setAttribute('aria-expanded', open); });
      if (open) {
        panel.scrollTop = 0;
        var close = panel.querySelector('[data-ai-close]');
        if (close) close.focus();
      }
    }
    openBtns.forEach(function (b) { b.addEventListener('click', function () { setPanel(true); }); });
    panel.querySelectorAll('[data-ai-close]').forEach(function (b) { b.addEventListener('click', function () { setPanel(false); }); });
    panel.addEventListener('click', function (e) { if (e.target === panel) setPanel(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !panel.hidden) setPanel(false); });

    /* Переключатель «ИИ рекомендация»: подставляет текст рекомендации в поле (151:2428 / 151:2543) */
    panel.querySelectorAll('.ai-switch input').forEach(function (input) {
      var section = input.closest('.ai-section');
      var field = section && section.querySelector('[data-ai-field]');
      if (!field) return;
      var text = field.querySelector('.ai-field__text');
      var count = field.querySelector('.ai-field__count');
      var original = text.innerHTML;
      input.addEventListener('change', function () {
        var value = input.checked ? field.dataset.ai : field.dataset.user;
        if (input.checked) text.textContent = value; else text.innerHTML = original;
        if (count) count.textContent = value.length + '/800';
      });
    });
  }

  /* ---- Карточки заданий: «Подробнее» / «Скрыть» ---- */
  document.querySelectorAll('.tcard__toggle').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var card = btn.closest('.tcard');
      var open = !card.classList.contains('is-open');
      card.classList.toggle('is-open', open);
      btn.setAttribute('aria-expanded', open);
      btn.textContent = open ? btn.dataset.close : btn.dataset.open;
    });
  });

  /* ---- Счётчик символов у textarea (0/800) ---- */
  document.querySelectorAll('.field--count').forEach(function (field) {
    var ta = field.querySelector('textarea');
    var out = field.querySelector('.field__count');
    if (!ta || !out) return;
    var max = ta.getAttribute('maxlength') || 800;
    var update = function () { out.textContent = ta.value.length + '/' + max; };
    ta.addEventListener('input', update);
    update();
  });

  /* ---- Шаг 5: ссылка «Файлы: (i)» открывает выбор файла ---- */
  document.querySelectorAll('.file-pick__m-link').forEach(function (link) {
    var input = link.closest('.file-pick').querySelector('input[type="file"]');
    if (input) link.addEventListener('click', function () { input.click(); });
  });

  /* ---- Слайдер бюджета (перетаскивание) ---- */
  document.querySelectorAll('.m-budget__slider').forEach(function (slider) {
    function setFromEvent(e) {
      var rect = slider.getBoundingClientRect();
      var x = (e.touches ? e.touches[0].clientX : e.clientX) - rect.left;
      var pct = Math.max(0, Math.min(100, Math.round(x / rect.width * 100)));
      slider.style.setProperty('--fill', pct + '%');
      slider.setAttribute('aria-valuenow', pct);
    }
    var dragging = false;
    slider.addEventListener('pointerdown', function (e) { dragging = true; slider.setPointerCapture(e.pointerId); setFromEvent(e); });
    slider.addEventListener('pointermove', function (e) { if (dragging) setFromEvent(e); });
    slider.addEventListener('pointerup', function () { dragging = false; });
    slider.addEventListener('pointercancel', function () { dragging = false; });
    slider.addEventListener('keydown', function (e) {
      var v = parseInt(slider.getAttribute('aria-valuenow'), 10) || 0;
      if (e.key === 'ArrowLeft' || e.key === 'ArrowDown') v -= 5;
      else if (e.key === 'ArrowRight' || e.key === 'ArrowUp') v += 5;
      else return;
      e.preventDefault();
      v = Math.max(0, Math.min(100, v));
      slider.style.setProperty('--fill', v + '%');
      slider.setAttribute('aria-valuenow', v);
    });
  });

  /* ---- Плейсхолдеры полей формы только на мобилке (макет 48:1022 / 64:1653) ---- */
  function applyPlaceholders() {
    var ph = isMobile.matches ? 'Пример: Починка стиральной машины...' : '';
    ['task-name', 'task-cat'].forEach(function (id) {
      var el = document.getElementById(id);
      if (el) el.placeholder = ph;
    });
  }
  applyPlaceholders();
  if (isMobile.addEventListener) isMobile.addEventListener('change', applyPlaceholders);
})();
