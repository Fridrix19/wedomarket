# -*- coding: utf-8 -*-
"""Раздел «Исполнители и профиль»: список исполнителей с фильтрами и пагинацией, профиль исполнителя с отзывами.
Figma: секция «Исполнители и профиль» 49:4098 — фреймы 95:779 («Исполнители»), 95:934 («Профиль», с отзывами),
95:999 («Профиль», без отзывов); карточки исполнителя 64:3965 («Вариант 1») и 64:3981 («Вариант 2»)."""
from common import *

SCRIPT = '<script src="js/performers.js"></script>'

# ---------------------------------------------------------------- ОБЩЕЕ
def stars():
    """Пять жёлтых звёзд рейтинга (вектор из макета, 81×13)."""
    return f'<span class="perf-stars" role="img" aria-label="Рейтинг 5 из 5">{icon("perf-stars", "icon perf-stars__icon")}</span>'

AVATAR = 'assets/img/perf-avatar.png'

# ---------------------------------------------------------------- ИСПОЛНИТЕЛИ (95:779)
FILTERS = [
    dict(key='category', label='Категория', options=['Все категории', 'Ремонт и строительство', 'Клининг', 'Сад и участок']),
    dict(key='subcategory', label='Подкатегория', options=['Все подкатегории', 'Кондиционеры', 'Покраска', 'Сантехника']),
    dict(key='rating', label='Рейтинг от', options=['Любой', '3', '4', '5']),
    dict(key='sort', label='Сортировка', options=['По рейтингу', 'По отзывам', 'По имени']),
]

SHORT_DESC = 'Обслуживание системы кондиционирования, Покраска деревянного забора'
LONG_DESC = ('Обслуживание системы кондиционирования, Покраска деревянного забора. Обслуживание системы кондиционирования, '
             'Покраска деревянного забора. Обслуживание системы кондиционирования, Покраска деревянного забора. '
             'Обслуживание системы кондиционирования.')

# 3 карточки «Вариант 1» (64:3965) + 2 карточки «Вариант 2» (64:3981) — как во фрейме 95:779
CANDIDATES = (
    [dict(name='Max Max', reviews='2 отзыва', desc=SHORT_DESC, wide=False)] * 3 +
    [dict(name='Max Max', reviews='0 отзывов', desc=LONG_DESC, wide=True)] * 2
)

def filter_field(f):
    opts = ''.join(f'<option value="{i}">{o}</option>' for i, o in enumerate(f['options']))
    return f'''<div class="perf-filter">
        <label class="perf-filter__label" for="perf-{f['key']}">{f['label']}</label>
        <span class="perf-select">
          <select class="perf-select__control" id="perf-{f['key']}" name="{f['key']}">{opts}</select>
          {icon('perf-chevron', 'icon perf-select__icon')}
        </span>
      </div>'''

def candidate_card(c, i):
    cls = 'perf-card' + (' perf-card--wide' if c['wide'] else '')
    return f'''<li class="perf-item">
      <article class="{cls}" aria-labelledby="perf-name-{i}">
        <img class="perf-card__avatar" src="{AVATAR}" alt="" width="{36 if c['wide'] else 92}" height="{35 if c['wide'] else 89}">
        <h3 class="perf-card__name" id="perf-name-{i}">{c['name']}</h3>
        <div class="perf-card__rating">{stars()}<span class="perf-card__reviews">{c['reviews']}</span></div>
        <p class="perf-card__desc">{c['desc']}</p>
      </article>
      <div class="perf-item__actions">
        <button class="btn btn--primary perf-btn" type="button">Предложить задание</button>
        <a class="btn btn--gray perf-btn perf-btn--gray" href="profile.html">Профиль</a>
      </div>
    </li>'''

def pagination():
    items = [
        ('<', 'Предыдущая страница', False), ('1', None, True), ('2', None, False),
        ('...', None, False), ('31', None, False), ('>', 'Следующая страница', False),
    ]
    out = []
    for text, label, active in items:
        if text == '...':
            out.append('<li><span class="perf-page perf-page--dots" aria-hidden="true">...</span></li>')
            continue
        cls = 'perf-page' + (' is-active' if active else '')
        attrs = f' aria-label="{label}"' if label else ''
        attrs += ' aria-current="page"' if active else ''
        txt = text.replace('<', '&lt;').replace('>', '&gt;')
        out.append(f'<li><a class="{cls}" href="#"{attrs}>{txt}</a></li>')
    return f'''<nav class="perf-pagination" aria-label="Страницы">
    <ul class="perf-pagination__list">{''.join(out)}</ul>
  </nav>'''

def performers():
    body = f'''{m_heading('Исполнители', title_cls='perf-title')}
<section class="perf" aria-labelledby="perf-title">
  <h1 class="h2 d-only perf__title" id="perf-title">Исполнители</h1>
  <form class="perf-filters" action="#" onsubmit="return false">
    <div class="perf-filters__grid">
      {''.join(filter_field(f) for f in FILTERS)}
    </div>
    <div class="perf-filters__actions">
      <button class="btn btn--primary perf-btn" type="submit">Далее</button>
      <button class="btn btn--gray perf-btn perf-btn--gray" type="reset">Сбросить</button>
    </div>
  </form>
  <h2 class="perf__subtitle">Кандидаты</h2>
  <ul class="perf-list">
    {''.join(candidate_card(c, i) for i, c in enumerate(CANDIDATES))}
  </ul>
  {pagination()}
</section>
{SCRIPT}'''
    return page('Исполнители', body, m_active=None, m_deco=True, extra_css=['performers.css'])

# ---------------------------------------------------------------- ПРОФИЛЬ (95:934 / 95:999)
ABOUT = [
    '-Предлагаю профессиональное обслуживание систем кондиционирования и качественную покраску деревянных заборов.',
    'Выполняю диагностику, чистку и мелкий ремонт кондиционеров; подготавливаю поверхность, выбираю подходящую краску '
    'и обеспечиваю долговечную защиту древесины. Работаю аккуратно, с соблюдением сроков и гарантийным обязательством.',
    '-Занимаюсь сервисом кондиционеров и наружными отделочными работами по дереву. Провожу профилактическую чистку, '
    'замену фильтров и дозаправку фреона; для заборов выполняю шлифовку, грунтовку и нанесение износостойкой краски '
    'или защитного масла. Опыт более нескольких сезонов, работаю как с частными домами, так и с коммерческими объектами.',
]

WORKS = [
    'Обслуживание кондиционеров: чистка, замена фильтров, диагностика.',
    'Ремонт кондиционеров: мелкий ремонт, дозаправка, устранение утечек.',
    'Покраска деревянных заборов: подготовка, грунтовка, финишное покрытие.',
    'Реставрация и защита древесины: антисептик, шлифовка, лакировка.',
]

REVIEW_TEXT = ('Cделал все чётко и точно в срок, без лишней воды. На вопросы ответил коротко и точно.<br>'
               'Результат лучше, чем у специалистов, которые сильно много всего предлагают и навязывают.<br>'
               'Будем продолжать сотрудничество при поступлении новых задач!')

REVIEWS = [
    dict(name='Max Max', text=REVIEW_TEXT, date='24.01.2025 в 19:34', dt='2025-01-24T19:34'),
    dict(name='Max Max', text=REVIEW_TEXT, date='24.01.2025 в 19:34', dt='2025-01-24T19:34'),
]

def review_card(r, i):
    return f'''<li class="review">
      <article class="review__card" aria-labelledby="review-name-{i}">
        <header class="review__head">
          <img class="review__avatar" src="{AVATAR}" alt="" width="29" height="28">
          <h4 class="review__name" id="review-name-{i}">{r['name']}</h4>
          {stars()}
        </header>
        <p class="review__text">{r['text']}</p>
      </article>
      <time class="review__date" datetime="{r['dt']}">{r['date']}</time>
    </li>'''

def review_tab(key, label, active=False):
    cls = 'profile-tab' + (' is-active' if active else '')
    return (f'<button class="{cls}" type="button" role="tab" id="profile-tab-{key}" aria-selected="{"true" if active else "false"}" '
            f'aria-controls="profile-pane-{key}" data-tab="{key}">{label}</button>')

def profile():
    about = ''.join(f'<p>{p}</p>' for p in ABOUT)
    works = ''.join(f'<li>-{w}</li>' for w in WORKS)
    body = f'''{m_heading('Профиль', back='performers.html', back_label='← Назад', title_cls='profile-title')}
<section class="profile" aria-labelledby="profile-title">
  <h1 class="h2 d-only profile__title" id="profile-title">Профиль</h1>
  <div class="profile-head">
    <img class="profile-head__avatar" src="{AVATAR}" alt="" width="125" height="121">
    <div class="profile-head__info">
      <h2 class="profile-head__name">Татьяна С</h2>
      <p class="profile-head__desc">Обслуживание системы кондиционирования, Покраска деревянного забора</p>
      <div class="profile-head__rating">{stars()}<span class="profile-head__reviews">2 отзыва</span></div>
    </div>
  </div>
  <button class="btn btn--primary perf-btn profile__offer" type="button">Предложить задание</button>

  <section class="profile-section" aria-labelledby="profile-about">
    <h3 class="profile-section__title" id="profile-about">О себе</h3>
    <div class="profile-section__text profile-about">{about}</div>
  </section>

  <section class="profile-section" aria-labelledby="profile-works">
    <h3 class="profile-section__title" id="profile-works">Виды работ</h3>
    <ul class="profile-section__text profile-works">{works}</ul>
  </section>

  <section class="profile-section profile-reviews" aria-labelledby="profile-reviews-title">
    <h3 class="profile-section__title" id="profile-reviews-title">Отзывы</h3>
    <div class="profile-tabs" role="tablist" aria-label="Роль в отзывах">
      {review_tab('performer', 'Как исполнитель', active=True)}
      {review_tab('customer', 'Как заказчик')}
    </div>
    <div class="profile-pane" id="profile-pane-performer" role="tabpanel" aria-labelledby="profile-tab-performer">
      <p class="profile-pane__count">Все ({len(REVIEWS)})</p>
      <ul class="review-list">
        {''.join(review_card(r, i) for i, r in enumerate(REVIEWS))}
      </ul>
    </div>
    <div class="profile-pane" id="profile-pane-customer" role="tabpanel" aria-labelledby="profile-tab-customer" hidden>
      <p class="profile-pane__count">Все (0)</p>
      <p class="profile-pane__empty">Нет отзывов</p>
    </div>
  </section>
</section>
{SCRIPT}'''
    return page('Профиль', body, m_active=None, m_deco=True, extra_css=['performers.css'])

pages = {
    'performers.html': performers(),
    'profile.html': profile(),
}
