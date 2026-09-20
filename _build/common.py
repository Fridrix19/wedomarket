# -*- coding: utf-8 -*-
"""Общие части страниц WeDo Market: шапка, футер, сайдбар (десктоп) + мобильная шапка, нижняя навигация, футер."""
import os

import sys
OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

import re as _re
_ICON_CACHE = {}

def icon(name, cls='icon', extra=''):
    """Встраивает SVG из assets/icons/<name>.svg прямо в HTML (работает и при открытии по file://).
    Цвета заменяются на currentColor, чтобы иконка красилась через CSS `color`."""
    if name not in _ICON_CACHE:
        path = os.path.join(OUT, 'assets', 'icons', name + '.svg')
        try:
            svg = open(path, encoding='utf-8').read()
        except OSError:
            _ICON_CACHE[name] = None
        else:
            svg = _re.sub(r'<\?xml[^>]*>|<!--.*?-->', '', svg, flags=_re.S).strip()
            # убираем размеры и служебные атрибуты корня, оставляем viewBox
            svg = _re.sub(r'<svg\b([^>]*)>', lambda m: '<svg' + _re.sub(r'\s(width|height|style|preserveAspectRatio|overflow)="[^"]*"', '', m.group(1)) + '>', svg, count=1)
            # любые цвета заливки/обводки -> currentColor (кроме none и url(...))
            svg = _re.sub(r'(fill|stroke)="(?!none|url\()[^"]*"', r'\1="currentColor"', svg)
            svg = _re.sub(r'<rect\s+width="[^"]*"\s+height="[^"]*"\s+fill="currentColor"\s*/>', '', svg)  # фоновые прямоугольники
            _ICON_CACHE[name] = svg
    svg = _ICON_CACHE[name]
    if not svg:
        return f'<i class="{cls} icon--{name}" aria-hidden="true"{extra}></i>'
    return svg.replace('<svg', f'<svg class="{cls} icon--{name}" aria-hidden="true" focusable="false"{extra}', 1)

# ---------------------------------------------------------------- HEADER
HEADER = '''<header class="header d-only">
  <div class="container header__inner">
    <div class="header__left">
      <a class="header__logo" href="index.html" aria-label="WeDo Market — на главную">
        <img src="assets/img/logo.png" alt="WeDo Market" width="65" height="64">
      </a>
      <nav class="nav" aria-label="Основное меню">
        <a class="nav__link" href="task-create-step1.html">Создать заказ</a>
        <a class="nav__link" href="#">Найти задание</a>
        <a class="nav__link" href="#">Исполнители</a>
      </nav>
    </div>
    <div class="header__right">
      <div class="header__icons">
        <a class="icon-btn icon-btn--bell" href="#" aria-label="Уведомления"><img src="assets/icons/bell.svg" alt="" width="17" height="19"></a>
        <a class="icon-btn" href="#" aria-label="Чаты"><img src="assets/icons/chat.svg" alt="" width="32" height="32"></a>
      </div>
      <div class="user">
        <button class="user__btn" type="button" aria-haspopup="true" aria-expanded="false" aria-label="Меню пользователя">
          <img class="user__avatar" src="assets/icons/avatar.svg" alt="" width="40" height="40">
          <img class="user__chevron" src="assets/icons/chevron-down-sm.svg" alt="" width="16" height="16">
        </button>
        <div class="user__menu" role="menu">
          <a href="index.html" role="menuitem">Дашборд</a>
          <a href="#" role="menuitem">Профиль</a>
          <a href="#" role="menuitem">Настройки</a>
          <a href="#" role="menuitem">Выйти</a>
        </div>
      </div>
    </div>
  </div>
</header>'''

# ---------------------------------------------------------------- FOOTER
FOOTER = '''<footer class="footer d-only">
  <div class="container">
    <div class="footer__top">
      <div class="footer__cols">
        <nav class="footer__col" aria-label="О сервисе">
          <a href="#">О компании</a>
          <a href="#">Вопрос ответ</a>
          <a href="#">Блог</a>
          <a href="#">Способ оплаты</a>
          <a href="#">Контакты</a>
        </nav>
        <nav class="footer__col footer__col--docs" aria-label="Документы">
          <a href="#">Пользовательское соглашение</a>
          <a href="#">Политика конфиденциальности</a>
        </nav>
        <div class="footer__col footer__col--social">
          <a class="social-btn social-btn--telegram" href="#"><img src="assets/icons/telegram.svg" alt="" width="18" height="18">Написать в Telegram</a>
          <a class="social-btn social-btn--viber" href="#"><img src="assets/icons/viber.svg" alt="" width="18" height="32">Viber</a>
        </div>
      </div>
      <div class="footer__company">
        <img class="footer__company-logo" src="assets/img/logo.png" alt="WeDo Market" width="88" height="100">
        <p class="footer__company-text">ООО «ВеДу Маркет», Адрес: Республика Беларусь, 220100, Минск, ул. Сурганова, д. 57б, оф. 182.&nbsp; УНП 193662192.. Свидетельство о государственной регистрации № 193662192 выдано 16.12.2022 Минским горисполкомом</p>
      </div>
    </div>
    <div class="footer__payments">
      <img src="assets/img/webpay.png" alt="WebPay" width="130" height="43">
      <img src="assets/icons/visa.svg" alt="Visa" width="50" height="16">
      <img src="assets/icons/mastercard.svg" alt="Mastercard" width="103" height="16">
      <img src="assets/img/belkart.png" alt="Белкарт" width="129" height="31">
    </div>
    <p class="footer__copy">2025 © Все права защищены WeDo Market - сервис подбора исполнителей</p>
  </div>
</footer>'''

# ---------------------------------------------------------------- SIDEBAR
def sidebar(active='dashboard', tasks_open=False, sub_active=None, wizard=False):
    def li(key, href, ic, label, two=False):
        cls = 'sidebar__item' + (' is-active' if active == key else '')
        lcls = 'sidebar__link' + (' sidebar__link--two-lines' if two else '')
        return f'<li class="{cls}"><a class="{lcls}" href="{href}">{icon(ic)}<span>{label}</span></a></li>'

    tasks_cls = 'sidebar__item' + (' is-open' if tasks_open else '') + (' is-active' if active == 'tasks' and not tasks_open else '')
    def sub(key, href, label):
        c = ' class="is-active"' if sub_active == key else ''
        return f'<li><a href="{href}"{c}>{label}</a></li>'
    tasks = f'''<li class="{tasks_cls}">
        <button class="sidebar__link sidebar__toggle" type="button" aria-expanded="{'true' if tasks_open else 'false'}">
          <span class="sidebar__toggle-left">{icon('nav-tasks')}<span>Задания</span></span>
          {icon('nav-chevron', 'icon icon--chevron')}
        </button>
        <ul class="sidebar__sub">
          {sub('create', 'task-create-step1.html', 'Создать задание')}
          {sub('my', 'task-view.html', 'Мои задания')}
          {sub('done', '#', 'Завершенные задания')}
        </ul>
      </li>'''

    top = [li('dashboard', 'index.html', 'nav-dashboard', 'Дашборд'), tasks, li('payments', '#', 'nav-payments', 'Все платежи')]
    if wizard:
        top += [li('notifications', '#', 'nav-notifications', 'Уведомления'),
                li('notif-settings', '#', 'nav-notification-settings', 'Настройка<br>уведомлений', two=True)]
    top += [li('chats', '#', 'nav-chats', 'Чаты')]
    bottom = [li('support', '#', 'nav-support', 'Тех поддержка'), li('settings', '#', 'nav-settings', 'Настройки'), li('logout', '#', 'nav-logout', 'Выйти')]
    cls = 'sidebar' + (' sidebar--wizard' if wizard else '')
    return f'''<aside class="{cls}" aria-label="Меню личного кабинета">
      <ul class="sidebar__group">{''.join(top)}</ul>
      <ul class="sidebar__group sidebar__group--bottom">{''.join(bottom)}</ul>
    </aside>'''

# ---------------------------------------------------------------- MOBILE SHELL
def m_header(deco=False):
    cls = 'm-header m-only-flex' + (' m-header--deco' if deco else '')
    return f'''<header class="{cls}">
  <a class="m-header__logo" href="index.html" aria-label="WeDo Market — на главную"><img src="assets/img/logo-wordmark.svg" alt="WeDo Market" width="65" height="19"></a>
  <a class="m-header__bell" href="notification-settings.html" aria-label="Уведомления">{icon('m-bell')}<span class="m-header__dot" aria-hidden="true"></span></a>
</header>'''

def m_heading(title, back='index.html', back_label='← Главная', title_cls=''):
    """Мобильная крошка + заголовок страницы."""
    back_html = f'<a class="m-back" href="{back}">{back_label}</a>' if back else ''
    tc = 'm-title' + (' ' + title_cls if title_cls else '')
    return f'<div class="m-only">{back_html}<h1 class="{tc}">{title}</h1></div>'

M_NAV_ITEMS = [
    ('home', 'index.html', 'm-home', 'Дашборд'),
    ('tasks', 'task-create-step1.html', 'm-tasks', 'Задания'),
    ('chats', 'chats.html', 'm-mail', 'Чаты'),
    ('payments', '#', 'm-card', 'Платежи'),
]

def m_nav(active='home', progress=None):
    """Нижняя навигация. progress=(percent) добавляет блок «Прогресс создания»."""
    parts = []
    for key, href, ic, label in M_NAV_ITEMS:
        act = ' is-active' if active == key else ''
        cur = ' aria-current="page"' if active == key else ''
        parts.append(f'<a class="m-nav__btn{act}" href="{href}" aria-label="{label}"{cur}>{icon(ic)}</a>')
    btns = ''.join(parts)
    prog = ''
    if progress is not None:
        prog = f'''<div class="m-nav__progress" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="{progress}">
    <div class="m-nav__progress-row"><span>Прогресс создания</span><span>{progress}%</span></div>
    <div class="m-nav__progress-bar"><span style="--progress:{progress}%"></span></div>
  </div>'''
    return f'''<nav class="m-nav m-only" aria-label="Мобильная навигация">
  {prog}
  <div class="m-nav__menu" id="m-nav-menu" role="menu">
    <ul>
      <li><a href="#" role="menuitem">О компании</a></li>
      <li><a href="#" role="menuitem">Вопрос-ответ</a></li>
      <li><a href="#" role="menuitem">Блог</a></li>
      <li><a href="#" role="menuitem">Способ оплаты</a></li>
      <li><a href="#" role="menuitem">Контакты</a></li>
      <li><a class="is-accent" href="#" role="menuitem">{icon('m-settings')}Настройки</a></li>
      <li><a class="is-accent" href="notification-settings.html" role="menuitem">{icon('nav-notification-settings')}Настройка уведомлений</a></li>
      <li><a class="is-accent" href="#" role="menuitem">{icon('m-support')}Тех поддержка</a></li>
    </ul>
  </div>
  <div class="m-nav__pill">
    {btns}
    <button class="m-nav__btn m-nav__btn--more" type="button" aria-label="Ещё" aria-haspopup="true" aria-expanded="false" aria-controls="m-nav-menu">{icon('m-dots')}</button>
  </div>
</nav>'''

M_FOOTER = '''<footer class="m-footer m-only">
  <div class="m-footer__links">
    <a href="#">Пользовательское соглашение</a>
    <a href="#">Политика конфиденциальности</a>
  </div>
  <p class="m-footer__company">ООО «ВеДу Маркет», Адрес: Республика Беларусь, 220100, Минск, ул. Сурганова, д. 57б, оф. 182. УНП 193662192.. Свидетельство о государственной регистрации № 193662192выдано 16.12.2022 Минским горисполкомом</p>
  <p class="m-footer__copy">©2026 Все права защищены WeDo Market</p>
</footer>'''

# ---------------------------------------------------------------- PAGE SHELL
def page(title, body, main_cls='', m_active='home', m_progress=None, m_deco=False, m_footer=True, extra_css=None, body_cls=''):
    """Страница целиком. body — контент внутри .container (общий для десктопа и мобилки;
    мобильные/десктопные фрагменты помечаются классами .m-only / .d-only)."""
    css = ''.join(f'\n  <link rel="stylesheet" href="css/{c}">' for c in (extra_css or []))
    return f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — WeDo Market</title>
  <link rel="icon" href="assets/img/logo.png">
  <link rel="stylesheet" href="css/base.css">
  <link rel="stylesheet" href="css/layout.css">
  <link rel="stylesheet" href="css/pages.css">
  <link rel="stylesheet" href="css/mobile.css">{css}
</head>
<body{(' class="' + body_cls + '"') if body_cls else ''}>
<div class="page">
{HEADER}
{m_header(m_deco)}
<main class="page__main{(' ' + main_cls) if main_cls else ''}">
  <div class="container">
{body}
  </div>
</main>
{FOOTER}
{M_FOOTER if m_footer else ''}
{m_nav(m_active, m_progress)}
</div>
<script src="js/main.js"></script>
</body>
</html>
'''
