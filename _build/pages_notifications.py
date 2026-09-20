# -*- coding: utf-8 -*-
"""Раздел «Уведомления и их настройки»: страница «Настройка уведомлений» с двумя вкладками.
Figma: секция «Уведы» 49:4993 — фреймы 64:3325 (вкладка «Быстрая настройка») и 64:3396 (вкладка «Расширенные»)."""
from common import *

SCRIPT = '<script src="js/notifications.js"></script>'

# ---------------------------------------------------------------- QUICK SETUP (64:3325)
CHANNELS = [
    dict(key='none', label='Не выбрано', icon='notif-ban'),
    dict(key='telegram', label='Telegram', icon='notif-telegram', checked=True),
    dict(key='sms', label='SMS', icon='notif-sms'),
    dict(key='push', label='Push', icon='notif-push', dev=True),
]

def channel_card(c):
    cls = 'notif-channel' + (' notif-channel--dev' if c.get('dev') else '')
    attrs = ' checked' if c.get('checked') else ''
    attrs += ' disabled' if c.get('dev') else ''
    dev = '<span class="notif-channel__dev">В разработке</span>' if c.get('dev') else ''
    return f'''<li>
      <label class="{cls}">
        <input type="radio" name="notif-channel" value="{c['key']}"{attrs}>
        <span class="notif-channel__box">
          {icon(c['icon'], 'icon notif-channel__icon')}
          <span class="notif-channel__label">{c['label']}</span>
        </span>
        {dev}
      </label>
    </li>'''

def quick_pane():
    return f'''<div class="notif__pane is-active" id="notif-pane-quick" role="tabpanel" aria-labelledby="notif-tab-quick">
  <p class="notif__hint">
    {icon('notif-bolt', 'icon notif__hint-icon')}
    <span>Вы будете получать по выбранному каналу только те уведомления, которые могут быть через него отправлены.</span>
  </p>
  <form class="notif-quick" action="#" onsubmit="return false">
    <fieldset class="notif-quick__fieldset">
      <legend class="visually-hidden">Канал уведомлений</legend>
      <ul class="notif-channels">
        {''.join(channel_card(c) for c in CHANNELS)}
      </ul>
    </fieldset>
    <button class="btn btn--primary notif__save" type="submit">Сохранить</button>
  </form>
</div>'''

# ---------------------------------------------------------------- ADVANCED (64:3396)
EVENTS = ['Новый отклик на ваше задание', 'Исполнитель завершил задание', 'Вам оставили отзыв', 'Новое сообщение в чате']

GROUPS = [
    dict(key='telegram', title='Telegram', states=[True, False, False, False]),
    dict(key='sms', title='SMS', states=[True, False, True, True]),
    dict(key='push', title='Push', states=[False, False, False, False], dev=True),
]

def switch_row(group, i, label, on, disabled=False):
    attrs = (' checked' if on else '') + (' disabled' if disabled else '')
    return f'''<li>
        <label class="notif-row">
          <span class="notif-row__label">{label}</span>
          <span class="switch">
            <input type="checkbox" name="notif-{group}" value="{i}"{attrs}>
            <span class="switch__track" aria-hidden="true"></span>
          </span>
        </label>
      </li>'''

def group_block(g):
    cls = 'notif-group' + (' notif-group--dev' if g.get('dev') else '')
    rows = ''.join(switch_row(g['key'], i, label, on, g.get('dev', False))
                   for i, (label, on) in enumerate(zip(EVENTS, g['states'])))
    dev = '<p class="notif-group__dev" aria-hidden="true">В разработке</p>' if g.get('dev') else ''
    return f'''<section class="{cls}" aria-labelledby="notif-group-{g['key']}">
    <h3 class="notif-group__title" id="notif-group-{g['key']}">{g['title']}</h3>
    <p class="notif-group__sub">Заказчик</p>
    <div class="notif-group__body">
      <ul class="notif-group__list">
        {rows}
      </ul>
      {dev}
    </div>
  </section>'''

def advanced_pane():
    return f'''<div class="notif__pane" id="notif-pane-advanced" role="tabpanel" aria-labelledby="notif-tab-advanced" hidden>
  <form class="notif-advanced" action="#" onsubmit="return false">
    {''.join(group_block(g) for g in GROUPS)}
  </form>
</div>'''

# ---------------------------------------------------------------- PAGE
def tab(key, label, active=False):
    cls = 'notif__tab' + (' is-active' if active else '')
    return (f'<button class="{cls}" type="button" role="tab" id="notif-tab-{key}" aria-selected="{"true" if active else "false"}" '
            f'aria-controls="notif-pane-{key}" data-tab="{key}">{label}</button>')

def notification_settings():
    body = f'''{m_heading('Настройка уведомлений')}
<section class="notif" aria-labelledby="notif-title">
  <h1 class="h2 d-only notif__title" id="notif-title">Настройка уведомлений</h1>
  <p class="notif__alert" role="status">Чтобы получать уведомления на email, <a class="notif__alert-link" href="#">укажите email</a> и подтвердите его.</p>
  <h2 class="notif__role">Заказчик</h2>
  <div class="notif__tabs" role="tablist" aria-label="Режим настройки">
    {tab('quick', 'Быстрая настройка', active=True)}
    {tab('advanced', 'Расширенные')}
  </div>
  {quick_pane()}
  {advanced_pane()}
</section>
{SCRIPT}'''
    return page('Настройка уведомлений', body, m_active=None, m_deco=True, extra_css=['notifications.css'])

pages = {
    'notification-settings.html': notification_settings(),
}
