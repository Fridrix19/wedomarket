# -*- coding: utf-8 -*-
"""Страницы раздела «Чаты»: список чатов, экран диалога, диалог с открытой панелью вложений.
Figma: секция «Чаты» 164:2123 (фреймы 164:2247, 164:2302, 168:3119, 168:3879 + Photo Picker 168:4424 / 168:5532 / 183:3039)."""
from common import *

SCRIPT = '<script src="js/chats.js"></script>'

# ---------------------------------------------------------------- CHAT LIST
CHATS = [
    dict(name='Max Max', date='28 февраля, 20:58', msg='Разработка маркетинговой стратегии', online=True),
    dict(name='Max Max', date='28 февраля, 20:58', msg='Разработка маркетинговой стратегии'),
    dict(name='Max Max', date='28 февраля, 20:58', msg='Разработка маркетинговой стратегии', unread=4),
]

def chat_card(c):
    online = '<span class="chat-card__online" aria-label="онлайн"></span>' if c.get('online') else ''
    unread = f'<span class="chat-card__unread" aria-label="{c["unread"]} непрочитанных">{c["unread"]}</span>' if c.get('unread') else ''
    return f'''<li class="chats__item" data-name="{c['name'].lower()}">
  <a class="chat-card" href="chat.html">
    <span class="chat-card__avatar">
      <img src="assets/img/chat-avatar.png" alt="" width="31" height="31">
      {online}{unread}
    </span>
    <span class="chat-card__body">
      <span class="chat-card__top">
        <span class="chat-card__name">{c['name']}</span>
        <time class="chat-card__date">{c['date']}</time>
      </span>
      <span class="chat-card__msg">{c['msg']}</span>
    </span>
  </a>
</li>'''

def chats_list():
    body = f'''{m_heading('Чаты')}
<section class="chats" aria-labelledby="chats-title">
  <h1 class="h2 d-only chats__title" id="chats-title">Чаты</h1>
  <form class="chats__search" role="search" action="#" onsubmit="return false">
    <label class="visually-hidden" for="chats-search">Поиск по имени</label>
    <input class="chats__search-input" type="search" id="chats-search" name="q" placeholder="Поиск по имени" autocomplete="off">
  </form>
  <ul class="chats__list" id="chats-list">
    {''.join(chat_card(c) for c in CHATS)}
  </ul>
  <p class="chats__empty" id="chats-empty" hidden>Ничего не найдено</p>
</section>
{SCRIPT}'''
    return page('Чаты', body, m_active='chats', m_deco=True, extra_css=['chats.css'])

# ---------------------------------------------------------------- CHAT SCREEN PARTS
WAVE_GREEN = [13, 20, 13, 20, 13, 9, 16, 18, 8, 13, 18, 17, 17, 12, 16, 13, 18, 17, 18]
WAVE_GRAY = [13, 13, 12, 12, 13, 13, 8, 8, 17, 17, 12, 12, 13, 13, 18, 18, 20, 20, 7, 7, 12, 12, 8, 8, 18, 18]

def voice_wave():
    bars = ''.join(f'<i style="height:{h}px"></i>' for h in WAVE_GREEN)
    bars += ''.join(f'<i class="is-rest" style="height:{h}px"></i>' for h in WAVE_GRAY)
    return f'<span class="voice__wave" aria-hidden="true">{bars}</span>'

def doc_preview(kind, small=False):
    cls = 'doc-preview doc-preview--' + kind + (' doc-preview--sm' if small else '')
    return f'''<span class="{cls}" aria-hidden="true">
  <img class="doc-preview__sticker" src="assets/img/chat-sticker-{kind}.svg" alt="">
  <span class="doc-preview__ext">{kind}</span>
</span>'''

def msg_text(text, own=False, size=14):
    cls = 'msg msg--out' if own else 'msg msg--in'
    sz = ' msg__text--sm' if size == 12 else ''
    return f'<div class="{cls}"><p class="msg__text{sz}">{text}</p></div>'

def msg_voice(own=False, dur='0:25', time='10:25'):
    cls = 'msg msg--voice ' + ('msg--out' if own else 'msg--in')
    return f'''<div class="{cls}">
  <div class="voice">
    <button class="voice__play" type="button" aria-label="Воспроизвести голосовое сообщение"><img src="assets/img/chat-play.svg" alt="" width="48" height="48"></button>
    <div class="voice__body">
      {voice_wave()}
      <span class="voice__dur">{dur}<i class="voice__unread" aria-hidden="true"></i></span>
    </div>
  </div>
  <time class="msg__time">{time}</time>
</div>'''

def file_row(name, size, kind, action=True, radio=None):
    right = ''
    if action:
        right = f'<button class="file-row__more" type="button" aria-label="Действия с файлом">{icon("chat-dots")}</button>'
    if radio is not None:
        right = f'''<label class="file-row__pick">
      <input type="radio" name="attach-file" value="{name}"{' checked' if radio else ''}>
      <span class="file-row__radio" aria-hidden="true"></span>
      <span class="visually-hidden">Выбрать {name}</span>
    </label>'''
    return f'''<div class="file-row">
  {doc_preview(kind)}
  <div class="file-row__info">
    <p class="file-row__name">{name}</p>
    <p class="file-row__size">{size}</p>
  </div>
  {right}
</div>'''

def msg_file(own=True, time='00:25'):
    cls = 'msg msg--file ' + ('msg--out' if own else 'msg--in')
    return f'''<div class="{cls}">
  {file_row('Last_School_Essay.zip', '1 MB', 'zip')}
  <time class="msg__time">{time}</time>
</div>'''

def msg_reply(own=True, time='00:25'):
    cls = 'msg msg--reply ' + ('msg--out' if own else 'msg--in')
    return f'''<div class="{cls}">
  <div class="msg__quote">
    <span class="msg__quote-line" aria-hidden="true"></span>
    {doc_preview('zip', small=True)}
    <span class="msg__quote-body">
      <span class="msg__quote-name">Last_School_Essay.zip</span>
      <span class="msg__quote-type">file</span>
    </span>
  </div>
  <p class="msg__text">Ознакомьтесь с файлами проекта, тут указаны все требования</p>
  <time class="msg__time">{time}</time>
</div>'''

def msg_image(own=True, time='00:25'):
    cls = 'msg msg--image ' + ('msg--out' if own else 'msg--in')
    return f'''<div class="{cls}">
  <a class="msg__image" href="assets/img/chat-photo-attach.jpg"><img src="assets/img/chat-photo-attach.jpg" alt="Скриншот: папки Bevels, Materials, Models" width="251" height="255"></a>
  <p class="msg__text">Тут найдете ТЗ и описание! </p>
  <time class="msg__time">{time}</time>
</div>'''

def chat_thread():
    return f'''<div class="chat__thread" id="chat-thread" aria-live="polite">
  <p class="chat__date">28 февраля</p>
  {msg_text('Привет! Готов выполнить. Подскажите, коротко: целевая аудитория, бюджет и ожидания по KPI?', size=12)}
  {msg_text('ЦА — 18–35 лет, в городах, интересы: гаджеты и лайфстайл. Бюджет на маркетинг 2 000 000 ₽ за первые 3 месяца. Ждём рост узнаваемости и минимум 3000 лидов за квартал.', own=True)}
  {msg_text('Понял. Предлагаю план на 12 недель: 1) исследование и УТП — 2 недели; 2) контент и креативы — 4 недели; 3) тесты рекламы и лендинг — 2 недели; 4) предзапуск и сбор лидов — 2 недели; 5) запуск и оптимизация — 2 недели. Подходит?')}
  {msg_text('Подходит. Нужно, чтобы у каждой стадии были ответственные и конкретные дедлайны. Кто будет в команде?', own=True)}
  {msg_voice(own=True)}
  {msg_voice(own=False)}
  {msg_file()}
  {msg_reply()}
  {msg_image()}
</div>'''

def chat_bar():
    return f'''<header class="chat__bar">
  <a class="chat__back" href="chats.html" aria-label="Назад к чатам">{icon('chat-back')}</a>
  <img class="chat__avatar" src="assets/img/chat-avatar.png" alt="" width="40" height="40">
  <div class="chat__who">
    <p class="chat__name">Max Max <img class="chat__emoji" src="assets/img/chat-status-emoji.png" alt="" width="20" height="20"></p>
    <p class="chat__status">онлайн</p>
  </div>
  <button class="chat__more" type="button" aria-label="Меню чата" aria-haspopup="true">{icon('chat-more')}</button>
</header>'''

def chat_input(with_mic=False):
    mic = f'<button class="chat__round-btn chat__mic" type="button" aria-label="Записать голосовое сообщение">{icon("chat-mic")}</button>' if with_mic else ''
    attach = ('<button class="chat__round-btn chat__attach" type="button" id="chat-attach-btn" aria-label="Прикрепить файл" aria-expanded="true" aria-controls="chat-picker">'
              if with_mic else
              '<a class="chat__round-btn chat__attach" href="chat-attach.html" aria-label="Прикрепить файл">')
    attach_end = '</button>' if with_mic else '</a>'
    return f'''<form class="chat__input{' chat__input--mic' if with_mic else ''}" id="chat-form" action="#" autocomplete="off">
  <button class="chat__round-btn chat__emoji-btn" type="button" aria-label="Эмодзи">{icon('chat-emoji')}</button>
  <label class="chat__field">
    <span class="visually-hidden">Сообщение</span>
    <input class="chat__msg" type="text" name="message" placeholder="Сообщение" id="chat-msg">
  </label>
  {attach}{icon('chat-paperclip')}{attach_end}
  {mic}
</form>'''

# ---------------------------------------------------------------- PHOTO PICKER
PHOTOS = list(range(1, 13))

def picker_grid(kind):
    tiles = []
    for i in PHOTOS:
        if i == 1:
            tiles.append(f'''<li class="picker__tile picker__tile--camera">
      <button type="button" aria-label="Снять {'видео' if kind == 'video' else 'фото'}">
        <img class="picker__img" src="assets/img/chat-photo-{i}.jpg" alt="">
        <img class="picker__camera" src="assets/img/chat-camera.svg" alt="" width="36" height="36">
      </button>
    </li>''')
            continue
        dur = '<span class="picker__dur">0:25</span>' if kind == 'video' else ''
        tiles.append(f'''<li class="picker__tile">
      <label>
        <input type="checkbox" name="attach-{kind}" value="{i}">
        <img class="picker__img" src="assets/img/chat-photo-{i}.jpg" alt="{'Видео' if kind == 'video' else 'Фото'} {i}">
        <span class="picker__check" aria-hidden="true"></span>
        {dur}
      </label>
    </li>''')
    return f'<ul class="picker__grid">{"".join(tiles)}</ul>'

def picker_files():
    groups = []
    for g in range(3):
        groups.append(f'''<li class="picker__file-group">
      {file_row('Last_School_Essay.pdf', '1 MB', 'pdf', action=False, radio=(g == 0))}
      {file_row('Last_School_Essay.zip', '1 MB', 'zip', action=False, radio=False)}
    </li>''')
    return f'<ul class="picker__files">{"".join(groups)}</ul>'

def picker_tab(key, label, active=False, composite=True):
    cls = 'picker__tab' + (' is-active' if active else '')
    ic = f'<span class="picker__tab-ic picker__tab-ic--box picker__tab-ic--{key}">{icon("chat-tab-" + key)}</span>'
    return f'''<button class="{cls}" type="button" role="tab" id="picker-tab-{key}" aria-selected="{'true' if active else 'false'}" aria-controls="picker-pane-{key}" data-tab="{key}">
      {ic}
      <span class="picker__tab-label">{label}</span>
    </button>'''

def photo_picker():
    return f'''<div class="chat-overlay" id="chat-overlay" hidden></div>
<section class="picker" id="chat-picker" aria-label="Прикрепить вложение" hidden>
  <span class="picker__handle" aria-hidden="true"></span>
  <div class="picker__panes">
    <div class="picker__pane is-active" id="picker-pane-photo" role="tabpanel" aria-labelledby="picker-tab-photo">{picker_grid('photo')}</div>
    <div class="picker__pane" id="picker-pane-files" role="tabpanel" aria-labelledby="picker-tab-files" hidden>{picker_files()}</div>
    <div class="picker__pane" id="picker-pane-video" role="tabpanel" aria-labelledby="picker-tab-video" hidden>{picker_grid('video')}</div>
  </div>
  <div class="picker__bottom">
    <div class="picker__tabs" role="tablist" aria-label="Тип вложения">
      {picker_tab('photo', 'Фото', active=True)}
      {picker_tab('files', 'Файлы')}
      {picker_tab('video', 'Видео', composite=False)}
    </div>
    <span class="picker__home" aria-hidden="true"></span>
  </div>
</section>'''

# ---------------------------------------------------------------- PAGES
def chat_screen(attach=False):
    body = f'''<div class="chat{' chat--attach' if attach else ''}">
  {chat_bar()}
  {chat_thread()}
  {chat_input(with_mic=attach)}
</div>
{photo_picker() if attach else ''}
{SCRIPT}'''
    title = 'Чат — вложения' if attach else 'Чат'
    return page(title, body, m_active='chats', m_deco=False, m_footer=False, extra_css=['chats.css'],
                body_cls='no-mnav chat-page' + (' chat-page--attach' if attach else ''))

pages = {
    'chats.html': chats_list(),
    'chat.html': chat_screen(),
    'chat-attach.html': chat_screen(attach=True),
}
