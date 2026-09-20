# -*- coding: utf-8 -*-
"""Страницы: дашборд, задания, мастер создания задания (десктоп + мобильная версия).
Мобильные макеты (Figma VIosFW7PvQvsQDcEHrvmHN): дашборд 48:3362; мастер 48:785, 64:359, 64:543, 64:917, 144:1063,
64:1039, 64:1243, 64:1653 (+ панель «Совет ИИ» 151:1918 / 151:2068); списки 64:1883, 64:2376, 64:2195; редактирование 48:1022."""
from common import *

TASKS_CSS = ['tasks-mobile.css']
TASKS_JS = '<script src="js/tasks-mobile.js"></script>'

# ---------------------------------------------------------------- SHARED FORM PARTS
def date_field(id_, label, cls='date-field'):
    return f'''<div class="{cls}">
  <div class="input-row">
    <div class="field">
      <label class="field__label" for="{id_}">{label}</label>
      <div class="input--icon">
        <input class="input" type="text" id="{id_}" name="{id_}" placeholder="дд.мм.гггг" inputmode="numeric" autocomplete="off">
        {icon('calendar')}
      </div>
    </div>
    <label class="select-time">
      <select name="{id_}_time" aria-label="Время">
        {''.join(f'<option>{h:02d}:00</option>' for h in range(24))}
      </select>
      {icon('chevron-down')}
    </label>
  </div>
  <div class="quick-dates">
    <button type="button" data-date="today">Сегодня</button>
    <button type="button" data-date="tomorrow">Завтра</button>
  </div>
</div>'''

def radio(name, value, label, checked=False, disabled=False):
    cls = 'radio' + (' radio--disabled' if disabled else '')
    return f'''<label class="{cls}">
  <input type="radio" name="{name}" value="{value}"{' checked' if checked else ''}{' disabled' if disabled else ''}>
  <span class="radio__box"></span>
  <span class="radio__label">{label}</span>
</label>'''

def file_pick(id_):
    return f'''<div class="file-pick">
  <button class="btn btn--pill" type="button">{icon('link', 'icon icon--24')}Выбрать файл</button>
  <input class="visually-hidden" type="file" id="{id_}" name="{id_}" multiple accept=".jpg,.jpeg,.png,.pdf,.doc,.docx" tabindex="-1">
  <p class="file-pick__hint">Разрешенные расширения файлов: .jpg, .jpeg, .png, .pdf, .doc, .docx</p>
</div>'''

REQ = '<span class="task-form__req">*</span>'   # звёздочка обязательного поля (на мобилке скрыта — в макете её нет)

def payment_block(extra_cls='', required=True):
    return f'''<div class="payment{(' ' + extra_cls) if extra_cls else ''}">
  <h3 class="payment__title">Способ оплаты{(" " + REQ) if required else ""}</h3>
  <div class="payment__option">
    {radio('payment', 'safe', 'Сделка без риска', disabled=True)}
    <p class="radio-desc radio-desc--disabled">Оплата банковской картой с гарантией возврата и&nbsp;компенсацией материального ущерба.</p>
  </div>
  <div class="payment__option">
    {radio('payment', 'direct', 'Оплата напрямую', checked=True)}
    <p class="radio-desc">Без гарантий и компенсаций WeDo: вы напрямую договариваетесь с&nbsp;исполнителем об условиях и способе оплаты</p>
  </div>
</div>'''

def m_budget(mode='range'):
    """Мобильный блок «Бюджет»: слайдер + поля «От/До» (редактирование, 48:1022) или «До 400 BYN» (шаг 7, 64:1653)."""
    if mode == 'range':
        fill, inputs = 64, '''<div class="m-budget__inputs">
    <input class="input m-budget__input" type="text" aria-label="Бюджет от" placeholder="От" inputmode="numeric">
    <input class="input m-budget__input" type="text" aria-label="Бюджет до" placeholder="До" inputmode="numeric">
  </div>'''
    else:
        fill, inputs = 46, '''<input class="input m-budget__single" type="text" aria-label="Бюджет до" placeholder="До 400 BYN" inputmode="numeric">'''
    return f'''<div class="m-only m-budget">
  <p class="m-budget__label">Бюджет</p>
  <div class="m-budget__slider" role="slider" aria-valuemin="0" aria-valuemax="100" aria-valuenow="{fill}" aria-label="Бюджет" tabindex="0" style="--fill:{fill}%"><span class="m-budget__knob"></span></div>
  {inputs}
</div>'''

def task_form(title, required=True, submit='Отправить', with_title=True, m_subtitle='', m_budget_mode='range'):
    r = REQ if required else ''
    rs = ' ' + REQ if required else ''
    return f'''<form class="task-form" action="#" method="post">
  {f'<h1 class="h1 task-form__title d-only">{title}</h1>' if with_title else ''}
  {f'<h2 class="m-only task-form__m-subtitle">{m_subtitle}</h2>' if m_subtitle else ''}
  <div class="field">
    <label class="field__label" for="task-name">Название задания{r}</label>
    <input class="input" type="text" id="task-name" name="name">
  </div>
  <div class="task-form__row">
    <div class="field field--md">
      <label class="field__label" for="task-cat">Категория{r}</label>
      <input class="input" type="text" id="task-cat" name="category">
    </div>
    <div class="field field--lg d-only">
      <label class="field__label" for="task-subcat">Подкатегория{r}</label>
      <input class="input" type="text" id="task-subcat" name="subcategory">
    </div>
  </div>
  <div class="task-form__row">
    <div class="task-form__group field--md">
      <p class="task-form__group-title">Место оказания услуги{rs}</p>
      <div class="radio-group">
        {radio('place', 'remote', 'Удаленно', checked=True)}
        {radio('place', 'address', 'Нужно присутствие по адресу')}
      </div>
    </div>
    <div class="field field--lg d-only">
      <label class="field__label" for="task-budget">Бюджет до{rs}</label>
      <input class="input" type="text" id="task-budget" name="budget" inputmode="numeric">
    </div>
    {m_budget(m_budget_mode)}
  </div>
  <div class="task-form__section">
    <h2 class="h2">Когда нужно приступить к работе</h2>
    <p class="task-form__section-desc">Укажите дату и время, начала и окончания работ(необязательно)</p>
    <div class="date-fields">
      {date_field('date-start', 'Начать работу')}
      {date_field('date-end', 'Закончить работу')}
    </div>
  </div>
  <div class="field field--count">
    <label class="field__label" for="task-desc">Описание задания{rs}</label>
    <textarea class="textarea" id="task-desc" name="description" maxlength="800"></textarea>
    <span class="m-only field__count" aria-live="polite">0/800</span>
  </div>
  {file_pick('task-files')}
  {payment_block(required=required)}
  <button class="btn btn--primary btn--lg task-form__submit" type="submit">{submit}</button>
</form>'''

# ---------------------------------------------------------------- MOBILE PARTS
def m_tabs(active):
    """Мобильные вкладки раздела «Задания»: Создать / Мои / Готовые."""
    items = [('create', 'task-create-step1.html', 'Создать'), ('my', 'my-tasks.html', 'Мои'), ('done', 'my-tasks-done.html', 'Готовые')]
    links = ''
    for k, h, l in items:
        act = ' is-active' if k == active else ''
        cur = ' aria-current="page"' if k == active else ''
        links += f'<a class="m-tabs__tab{act}" href="{h}"{cur}>{l}</a>'
    return f'<nav class="m-tabs tasks-tabs m-only-flex" aria-label="Разделы заданий">{links}</nav>'

def m_task_details(status=None):
    """Строки деталей задания (64:2195 / 64:2376)."""
    st = f'<p class="tcard__status{" tcard__status--" + status[0] if status else ""}">{status[1]}</p>' if status else ''
    return f'''<dl class="tcard__props">
      <dt>Начать</dt><dd>01.01.2026</dd>
      <dt>Адрес</dt><dd>Тикоцкого 36</dd>
      <dt>Оплата</dt><dd>Оплата напрямую исполнителю</dd>
      <dt>Что нужно?</dt><dd>Убрать хорошенько квартиру, на совесть</dd>
      <dt>Бюджет</dt><dd><span class="tcard__price">200 BYN</span></dd>
    </dl>
    {st}'''

def m_task_card(idx, expanded=False):
    """Карточка задания в списке «Мои задания» (64:1883) с раскрытием деталей (64:2376)."""
    return f'''<li class="tcard{' is-open' if expanded else ''}" id="tcard-{idx}">
  <article class="tcard__box">
    <div class="tcard__head">
      <h2 class="tcard__title">Генеральная уборка квартиры 100 м2</h2>
      <span class="tcard__price tcard__price--head">200 BYN</span>
    </div>
    <p class="tcard__desc">Убрать хорошенько квартиру, на совесть</p>
    <div class="tcard__map"><img src="assets/img/map.webp" alt="Карта: Тикоцкого 36, Минск"></div>
    <div class="tcard__details" id="tcard-{idx}-details">
      {m_task_details()}
    </div>
  </article>
  <div class="tcard__btns">
    <button class="btn tcard__btn tcard__btn--outline tcard__toggle" type="button" aria-expanded="{'true' if expanded else 'false'}" aria-controls="tcard-{idx}-details" data-open="Подробнее" data-close="Скрыть">{'Скрыть' if expanded else 'Подробнее'}</button>
    <a class="btn btn--primary tcard__btn" href="task-edit.html">Редактировать</a>
  </div>
</li>'''

# ---------------------------------------------------------------- PAGES
def dashboard():
    body = f'''{m_heading('Дашборд', back_label='Главная')}
<div class="layout layout--dashboard">
  {sidebar('dashboard')}
  <div class="layout__content dashboard">
    <h2 class="m-only m-section-title dashboard__m-title dashboard__m-title--finance">Финансы</h2>
    <div class="m-only-flex dashboard__m-btns">
      <a class="btn dashboard__m-btn dashboard__m-btn--outline" href="#">Вывести</a>
      <a class="btn btn--primary dashboard__m-btn" href="#">Пополнить</a>
    </div>
    <h2 class="m-only m-section-title dashboard__m-title dashboard__m-title--tasks">Задания</h2>
    <div class="dashboard__main">
      <section class="chart-block" aria-labelledby="chart-title">
        <h1 class="h2" id="chart-title">Завершенные задания</h1>
        <div class="chart" data-chart="[0,0,0,0,0,0,0,0,0,0,0,0]"></div>
      </section>
      <section class="card recent" aria-labelledby="recent-title">
        <h2 class="recent__title" id="recent-title">Недавно выполненные задания</h2>
        <ul class="recent__list">
          <li class="recent__row"><span class="recent__name">Уборка квартиры 153</span><span class="badge badge--success">Выполнено</span></li>
          <li class="recent__row"><span class="recent__name">Уборка квартиры 153</span><span class="badge badge--success">Выполнено</span></li>
          <li class="recent__row"><span class="recent__name">Уборка квартиры 153</span><span class="badge badge--success">Выполнено</span></li>
        </ul>
        <a class="btn btn--primary btn--block" href="#">Посмотреть все</a>
      </section>
    </div>
    <aside class="dashboard__aside">
      <div class="dashboard__aside-group">
        <div class="card stat stat--balance">
          <img class="stat__icon" src="assets/icons/stat-wallet.svg" alt="" width="64" height="64">
          <div><p class="stat__label">Баланс</p><p class="stat__value">0 BYN</p></div>
        </div>
        <div class="card balance d-only">
          <div class="balance__inner">
            <h2 class="balance__title">Управление балансом</h2>
            <div class="balance__btns">
              <a class="btn btn--primary btn--block" href="#">Пополнить</a>
              <a class="btn btn--gray btn--block" href="#">Вывести</a>
            </div>
          </div>
        </div>
      </div>
      <div class="dashboard__aside-group">
        <div class="card stat stat--wide stat--created">
          <img class="stat__icon" src="assets/icons/stat-created.svg" alt="" width="64" height="64">
          <div><p class="stat__label">Созданные задания</p><p class="stat__value">0</p></div>
        </div>
        <div class="card stat stat--done">
          <img class="stat__icon" src="assets/icons/stat-done.svg" alt="" width="64" height="64">
          <div><p class="stat__label">Выполненные задания</p><p class="stat__value">0</p></div>
        </div>
        <a class="btn btn--primary btn--block dashboard__create" href="task-create-step1.html">Создать новое задание</a>
      </div>
    </aside>
  </div>
</div>'''
    return page('Личный кабинет', body, m_active='home', extra_css=TASKS_CSS)

def task_edit():
    body = f'''{m_heading('Редактирование задания')}
<div class="layout">
  {sidebar('tasks', tasks_open=True, sub_active='create')}
  <div class="layout__content">
    <section class="card card--lg form-card">
      {task_form('Редактирование задания', m_subtitle='Обычное задание', m_budget_mode='range')}
    </section>
  </div>
</div>
{TASKS_JS}'''
    return page('Редактирование задания', body, m_active='tasks', extra_css=TASKS_CSS)

def task_view():
    body = f'''{m_heading('Мои задания')}
{m_tabs('my')}
<div class="layout">
  {sidebar('tasks', tasks_open=True, sub_active='my')}
  <div class="layout__content task-view">
    <a class="back-link d-only" href="index.html"><img src="assets/icons/return.svg" alt="" width="24" height="24">Вернуться</a>
    <article class="card card--lg task-card d-only">
      <div class="task-card__head">
        <h1 class="task-card__title">Генеральная уборка квартиры 100 м<sup>2</sup></h1>
        <a class="edit-btn" href="task-edit.html" aria-label="Редактировать задание"><img src="assets/icons/edit.svg" alt="" width="32" height="32"></a>
      </div>
      <dl class="task-props">
        <dt>Бюджет</dt><dd><span class="badge badge--price">200 BYN</span></dd>
        <dt>Начать</dt><dd>01.10.2025</dd>
        <dt>Адрес</dt><dd>Тикоцкого 36</dd>
        <dt>Тип оплаты</dt><dd>Оплата напрямую исполнителю</dd>
        <dt>Нужно сделать</dt><dd>Убрать хорошенько квартиру, на совесть</dd>
      </dl>
      <div class="task-map"><img src="assets/img/map.webp" alt="Карта: Тикоцкого 36, Минск"></div>
    </article>
    <div class="card card--yellow task-status d-only">Ожидаем откликов исполнителей</div>
    <ul class="m-only tcard-list">
      <li class="tcard is-open is-static">
        <article class="tcard__box">
          <h2 class="tcard__title">Генеральная уборка квартиры 100 м2</h2>
          <div class="tcard__map"><img src="assets/img/map.webp" alt="Карта: Тикоцкого 36, Минск"></div>
          {m_task_details(('wait', 'Ожидаем откликов исполнителей'))}
        </article>
        <div class="tcard__btns">
          <a class="btn btn--primary tcard__btn tcard__btn--full" href="task-edit.html">Редактировать</a>
        </div>
      </li>
    </ul>
  </div>
</div>'''
    return page('Просмотр задания', body, m_active='tasks', extra_css=TASKS_CSS)

def my_tasks():
    body = f'''{m_heading('Мои задания')}
{m_tabs('my')}
<div class="layout">
  {sidebar('tasks', tasks_open=True, sub_active='my')}
  <div class="layout__content tasks-list">
    <h1 class="h2 d-only tasks-list__title">Мои задания</h1>
    <p class="tasks-list__count">Все (2)</p>
    <ul class="tcard-list">
      {m_task_card(1)}
      {m_task_card(2)}
    </ul>
  </div>
</div>
{TASKS_JS}'''
    return page('Мои задания', body, m_active='tasks', extra_css=TASKS_CSS)

def my_tasks_done():
    body = f'''{m_heading('Мои задания')}
{m_tabs('done')}
<div class="layout">
  {sidebar('tasks', tasks_open=True, sub_active='done')}
  <div class="layout__content tasks-list">
    <h1 class="h2 d-only tasks-list__title">Завершенные задания</h1>
    <ul class="tcard-list">
      <li class="tcard is-open is-static">
        <article class="tcard__box">
          <h2 class="tcard__title">Генеральная уборка квартиры 100 м2</h2>
          <div class="tcard__map"><img src="assets/img/map.webp" alt="Карта: Тикоцкого 36, Минск"></div>
          {m_task_details(('done', 'Завершено'))}
        </article>
        <div class="tcard__btns">
          <a class="btn tcard__btn tcard__btn--outline tcard__btn--full" href="task-view.html">Подробности</a>
        </div>
      </li>
    </ul>
  </div>
</div>'''
    return page('Завершенные задания', body, m_active='tasks', extra_css=TASKS_CSS)

STEPS = [
    (1, 'Что нужно сделать?', 8),
    (2, 'Выбор адреса', 21.5),
    (3, 'Когда нужно сделать?', 39),
    (4, 'Уточнение деталей', 58),
    (5, 'Описание и файлы', 82),
    (6, 'Бюджет и способ оплаты', 94),
    (7, 'Просмотр задания', 100),
]
# Мобильные заголовки шагов и проценты «Прогресс создания» (из макета; шаги без блока прогресса — 1/5/6/7 — интерполированы)
M_STEPS = {
    1: ('1. Создать задание', 10),
    2: ('2. Выбор адреса', 20),
    3: ('3. Когда нужно сделать?', 30),
    4: ('4. Уточнение деталей', 55),
    5: ('5. Описание и файлы', 70),
    6: ('6. Бюджет и способ оплаты', 85),
    7: ('7. Просмотр задания', 100),
}

def wizard_footer(n):
    prev = f'task-create-step{n-1}.html' if n > 1 else 'index.html'
    nxt = f'task-create-step{n+1}.html' if n < 7 else '#'
    return f'''<div class="wizard__footer d-only">
  <a class="btn btn--outline btn--back" href="{prev}">Назад</a>
  <button class="btn btn--outline btn--draft" type="button">Сохранить черновик</button>
  <a class="btn btn--primary btn--next" href="{nxt}">Далее</a>
</div>'''

def m_draft():
    return '<a class="wiz-m__draft" href="#">Сохранить как черновик</a>'

def m_wizard_footer(n, back=True):
    """Мобильные кнопки «Назад» / «Далее» + ссылка «Сохранить как черновик»."""
    prev = f'task-create-step{n-1}.html' if n > 1 else 'index.html'
    nxt = f'task-create-step{n+1}.html' if n < 7 else '#'
    back_html = f'<a class="btn wiz-m__back" href="{prev}">Назад</a>' if back else ''
    return f'''<div class="m-only wiz-m__footer">
  <div class="wiz-m__btns">{back_html}<a class="btn btn--primary wiz-m__next" href="{nxt}">Далее</a></div>
  {m_draft()}
</div>'''

def step1_m_body():
    """Шаг 1, мобильный порядок (48:785)."""
    return f'''<div class="m-only step1-m">
  <div class="field">
    <label class="field__label step1-m__label" for="step1-title-m">Название задания</label>
    <input class="input step1__input" type="text" id="step1-title-m" name="title_m" placeholder="Пример: Починка стиральной машины...">
  </div>
  {m_wizard_footer(1, back=False)}
  <h3 class="step1-m__subtitle">Cоздать задание с помощью видео</h3>
  <div class="dropzone step1-m__dropzone" role="button" tabindex="0" aria-label="Загрузить видео для автоматического заполнения формы">
    <img class="dropzone__icon" src="assets/icons/video.svg" alt="" width="36" height="24">
    <p class="dropzone__text">Запиши видео до 1 мин и мы сделаем задание со всеми подробностями</p>
    <p class="dropzone__sub">MP4, WebM, MOV</p>
    <input class="visually-hidden" type="file" name="video_m" accept="video/mp4,video/webm,video/quicktime" tabindex="-1">
  </div>
  <p class="step1-m__or">или</p>
  <button class="btn btn--primary dropzone__btn step1-m__record" type="button"><img src="assets/icons/record.svg" alt="" width="18" height="18">Записать видео</button>
  <p class="step1__hint step1-m__hint">ИИ расшифрует речь и изображение<br>и автоматически заполнит заголовок, описание и другие поля.</p>
  <p class="captcha-label">Подтвердите, что вы не робот</p>
  <div class="captcha">
    <div class="captcha__box" role="checkbox" aria-checked="false" tabindex="0" aria-label="Я не робот"></div>
    <div>
      <p class="captcha__title">Я не робот</p>
      <p class="captcha__text">Нажмите, чтобы продолжить</p>
      <p class="captcha__brand">Yandex SmartCaptcha</p>
    </div>
    <img class="captcha__help" src="assets/icons/captcha-help.svg" alt="" width="20" height="20">
  </div>
  {m_wizard_footer(1, back=False)}
</div>'''

def ai_switch(name, checked=False):
    return f'''<label class="ai-switch">
        <span class="ai-switch__label">ИИ рекомендация</span>
        <input type="checkbox" name="{name}"{' checked' if checked else ''}>
        <span class="ai-switch__track" aria-hidden="true"><span class="ai-switch__knob">{icon('task-plane')}</span></span>
      </label>'''

def ai_panel():
    """Панель «Совет ИИ» (151:1918 / 151:2068), только мобилка, открывается кнопкой «Посмотреть рекомендации»."""
    return f'''<div class="m-only ai-overlay" id="ai-panel" hidden>
  <section class="ai-panel" role="dialog" aria-modal="true" aria-labelledby="ai-panel-title">
    <div class="ai-panel__head">
      <h2 class="ai-panel__title" id="ai-panel-title">Совет ИИ {icon('task-plane', 'icon ai-panel__plane')}</h2>
      <button class="ai-panel__close" type="button" aria-label="Закрыть" data-ai-close>{icon('task-close')}</button>
    </div>
    <p class="ai-panel__text">Задание требует значительных улучшений в описании, заголовке и&nbsp;категории.</p>

    <section class="ai-section">
      <h3 class="ai-section__title">1. Описание</h3>
      <p class="ai-section__text">Необходимо более детально описать задачи и ожидания от выполнения задания.</p>
      <div class="ai-field ai-field--area" data-ai-field data-user="Разработать маркетинговую стратегию для нового продукта" data-ai="Разработать маркетинговую стратегию для нового продукта, включая анализ целевой аудитории, конкурентов и определение ключевых каналов продвижения.">
        <p class="ai-field__text">Разработать маркетинговую стратегию для нового продукта, <span class="ai-field__ghost">включая анализ целевой аудитории, конкурентов и определение ключевых каналов продвижения.</span></p>
        <span class="ai-field__count">122/800</span>
      </div>
      {ai_switch('ai-desc')}
      <button class="btn btn--primary ai-section__save" type="button">Сохранить изменения</button>
    </section>

    <section class="ai-section">
      <h3 class="ai-section__title">2. Заголовок</h3>
      <p class="ai-section__text">Заголовок должен быть более конкретным и отражать суть задачи.</p>
      <div class="ai-field ai-field--input" data-ai-field data-user="Разработка маркетинговой стратегии" data-ai="Разработка маркетинговой стратегии для нового продукта с указанием задач и сроков">
        <p class="ai-field__text">Разработка маркетинговой стратегии</p>
      </div>
      <p class="ai-score"><span>Оценка: Плохо</span></p>
      {ai_switch('ai-title')}
      <button class="btn btn--primary ai-section__save" type="button">Сохранить изменения</button>
    </section>

    <section class="ai-section">
      <h3 class="ai-section__title">3. Категория</h3>
      <p class="ai-section__text">Категория не совсем соответствует заданию, лучше использовать более подходящую.</p>
      <div class="ai-field ai-field--input"><p class="ai-field__text">Рекомендация: маркетинг</p></div>
      <button class="btn btn--primary ai-section__save" type="button">Сохранить изменения</button>
    </section>

    <section class="ai-section">
      <h3 class="ai-section__title">4. Прикрепите файлы</h3>
      <p class="ai-section__text">Так исполнителям будет проще понять задачу.</p>
      <div class="ai-section__row">
        <button class="btn ai-section__attach" type="button">Прикрепить фото</button>
        <button class="btn ai-section__attach" type="button">Прикрепить видео</button>
      </div>
      <button class="btn btn--primary ai-section__save" type="button">Сохранить изменения</button>
    </section>
  </section>
</div>'''

def ai_card():
    """Зелёная карточка «Совет ИИ» с кнопкой «Посмотреть рекомендации» (64:1653)."""
    return f'''<div class="m-only ai-card">
  <div class="ai-card__head"><h3 class="ai-card__title">Совет ИИ</h3>{icon('task-plane', 'icon ai-card__plane')}</div>
  <p class="ai-card__text">Задание требует значительных улучшений в описании, заголовке и&nbsp;категории.</p>
  <p class="ai-score ai-score--card"><span>Оценка: Плохо</span></p>
</div>
<button class="m-only btn btn--primary ai-card__btn" type="button" data-ai-open aria-controls="ai-panel" aria-expanded="false">Посмотреть рекомендации</button>'''

def step_body(n, error=False):
    if n == 1:
        return f'''<div class="wizard__body d-only">
  <div>
    <label class="step1__label" for="step1-title">Опишите одним предложением</label>
    <input class="input step1__input" type="text" id="step1-title" name="title" placeholder="Пример: Починка стиральной машины">
    <h3 class="step1__subtitle">Не хотите заполнять форму вручную?</h3>
    <p class="step1__hint">Загрузите короткое видео (до 1 минуты) с описанием задачи — ИИ расшифрует речь и изображение<br>и автоматически заполнит заголовок, описание и другие поля.</p>
    <div class="dropzone" role="button" tabindex="0" aria-label="Загрузить видео для автоматического заполнения формы">
      <img class="dropzone__icon" src="assets/icons/video.svg" alt="" width="40" height="40">
      <p class="dropzone__text">Перетащите видео сюда или нажмите для выбора файла</p>
      <p class="dropzone__sub">MP4, WebM, MOV · до 1 мин</p>
      <button class="btn btn--primary dropzone__btn" type="button"><img src="assets/icons/record.svg" alt="" width="18" height="18">Записать видео</button>
      <input class="visually-hidden" type="file" name="video" accept="video/mp4,video/webm,video/quicktime" tabindex="-1">
    </div>
    <p class="captcha-label">Подтвердите, что вы не робот</p>
    <div class="captcha">
      <div class="captcha__box" role="checkbox" aria-checked="false" tabindex="0" aria-label="Я не робот"></div>
      <div>
        <p class="captcha__title">Я не робот</p>
        <p class="captcha__text">Нажмите, чтобы продолжить</p>
        <p class="captcha__brand">Yandex SmartCaptcha</p>
      </div>
      <img class="captcha__help" src="assets/icons/captcha-help.svg" alt="" width="20" height="20">
    </div>
  </div>
</div>
{step1_m_body()}'''
    if n == 2:
        return f'''<div class="wizard__body">
  <div class="step2__options">
    <div class="step2__option">{radio('place', 'remote', 'Удаленно', checked=True)}</div>
    <div class="step2__option">{radio('place', 'address', 'Нужно присутствие по адресу')}</div>
  </div>
</div>
{m_wizard_footer(2)}'''
    if n == 3:
        return f'''<div class="wizard__body">
  <div class="step3__row">
    {date_field('date-start', 'Начать работу')}
    {date_field('date-end', 'Закончить работу')}
  </div>
</div>
{m_wizard_footer(3)}'''
    if n == 4:
        if error:
            result = '''<div class="step4__result step4__result--error" role="status">
    <div class="step4__sad" aria-hidden="true"><i class="step4__eye"></i><i class="step4__eye"></i><i class="step4__mouth"></i></div>
    <p class="step4__text">Пожалуйста заполните описание вручную</p>
    <p class="step4__sub">В данный момент возникли трудности<br>с расшифровкой, но мы уже решаем это!</p>
  </div>'''
        else:
            result = '''<div class="step4__result" role="status">
    <div class="step4__check">
      <img src="assets/icons/check-circle.svg" alt="" width="80" height="80">
      <img class="step4__tick" src="assets/icons/check.svg" alt="" width="28" height="31">
    </div>
    <p class="step4__text">Ваше описание достаточно подробное. Можно перейти к следующему шагу.</p>
  </div>'''
        return f'''<div class="wizard__body">
  {result}
</div>
{m_wizard_footer(4)}'''
    if n == 5:
        return f'''<div class="wizard__body">
  <div class="field field--count">
    <label class="field__label" for="task-desc">Описание задания {REQ}</label>
    <textarea class="textarea" id="task-desc" name="description" maxlength="800"></textarea>
    <span class="m-only field__count" aria-live="polite">0/800</span>
  </div>
  <div class="file-pick file-pick--step5">
    <button class="btn btn--pill" type="button">{icon('link', 'icon icon--24')}Выбрать файл</button>
    <input class="visually-hidden" type="file" id="task-files" name="task-files" multiple accept=".jpg,.jpeg,.png,.pdf,.doc,.docx" tabindex="-1">
    <p class="file-pick__hint">Разрешенные расширения файлов: .jpg, .jpeg, .png, .pdf, .doc, .docx</p>
    <button class="m-only file-pick__m-link" type="button">Файлы: <i class="file-pick__info" aria-hidden="true">i</i></button>
  </div>
</div>
{m_wizard_footer(5)}'''
    if n == 6:
        return f'''<div class="wizard__body">
  <div>
    <div class="field">
      <label class="field__label" for="budget">Ваш бюджет до</label>
      <div class="budget__row">
        <input class="input" type="text" id="budget" name="budget" placeholder="Например: 400BYN" inputmode="numeric">
        <input class="input budget__cur" type="text" value="BYN" readonly aria-label="Валюта">
      </div>
    </div>
    <span class="budget__hint">Рекомендуемый бюджет: 0 – 0 BYN</span>
  </div>
  {payment_block('step6__payment')}
</div>
{m_wizard_footer(6)}'''
    if n == 7:
        return f'''<div class="wizard__body">
  {ai_card()}
  {task_form('', required=False, with_title=False, m_budget_mode='single')}
</div>
{ai_panel()}'''

def wizard(n, title, progress, error=False):
    footer = wizard_footer(n) if n < 7 else ''
    m_title, m_progress = M_STEPS[n]
    body = f'''<nav class="breadcrumbs d-only" aria-label="Хлебные крошки"><a href="index.html">Главная</a><span>/</span><span>Создание задания</span></nav>
<h1 class="page-title d-only">Создание задания</h1>
{m_heading('Задания')}
{m_tabs('create')}
<h2 class="m-only wiz-m__title">{m_title}</h2>
<div class="layout">
  {sidebar(None, wizard=True)}
  <div class="layout__content">
    <section class="card card--lg wizard-card" aria-labelledby="step-title">
      <div class="wizard__head d-only"><span class="wizard__num">{n}</span><h2 class="wizard__title" id="step-title">{title}</h2></div>
      <div class="wizard__progress d-only" role="progressbar" aria-valuemin="1" aria-valuemax="7" aria-valuenow="{n}"><div class="wizard__progress-bar" style="--progress:{progress}%"></div></div>
      {step_body(n, error)}
      {footer}
    </section>
  </div>
</div>
{TASKS_JS}'''
    return page(f'Создание задания — шаг {n}', body, 'page__main--wizard', m_active='tasks', m_progress=m_progress, extra_css=TASKS_CSS)


# ---------------------------------------------------------------- WRITE
pages = {
    'index.html': dashboard(),
    'task-edit.html': task_edit(),
    'task-view.html': task_view(),
    'my-tasks.html': my_tasks(),
    'my-tasks-done.html': my_tasks_done(),
}
for n, t, p in STEPS:
    pages[f'task-create-step{n}.html'] = wizard(n, t, p)
pages['task-create-step4-error.html'] = wizard(4, 'Уточнение деталей', 58, error=True)
