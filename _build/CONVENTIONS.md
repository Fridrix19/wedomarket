# Конвенции проекта WeDo Market (для вёрстки новых страниц)

Стек: статический HTML + CSS + ванильный JS. Страницы генерируются Python-модулями в `_build/`
(`python _build/build.py` пишет все HTML в корень проекта). Никакого Tailwind/React.

## Как добавить страницы
Создать модуль `_build/pages_<section>.py`:
```python
from common import *        # page(), m_header(), m_heading(), icon(), M_FOOTER, m_nav()
pages = {
  'chats.html': page('Чаты', BODY_HTML, m_active='chats', m_deco=True, extra_css=['chats.css']),
}
```
`page(title, body, main_cls='', m_active='home'|'tasks'|'chats'|'payments'|None, m_progress=None,
      m_deco=False, m_footer=True, extra_css=[...], body_cls='')`
— `body` вставляется внутрь `<main class="page__main"><div class="container">…`.
— Десктопная шапка/футер и мобильные шапка/нижняя навигация/футер добавляются автоматически.
— `m_deco=True` — декоративные светло-фиолетовые круги в мобильной шапке (чаты, исполнители, профиль, уведомления).
— `m_footer=False` — без мобильного футера (экран чата).
— `extra_css` — свои CSS-файлы из папки `css/` (создайте `css/<section>.css`).

## Мобильный заголовок страницы
`m_heading('Чаты')` → `<a class="m-back" href="index.html">← Главная</a><h1 class="m-title">Чаты</h1>` (только на мобилке, класс .m-only).

## Видимость
`.m-only` — только ≤767px (display:block), `.m-only-flex` — то же, но display:flex; `.d-only` — только ≥768px.
Мобильный брейкпоинт: `@media (max-width: 767px)`. Мобильный макет 375px: боковые отступы 17px (контент 342px). `.container` уже даёт эти отступы (переменная --gutter).

## Иконки
SVG-иконки лежат в `assets/icons/` и при сборке встраиваются в HTML (цвета заменяются на `currentColor`, красятся через CSS `color`):
- В HTML: `{icon('имя')}` → `<svg class="icon icon--имя" …>` (16×16 по умолчанию, размер задавайте своим CSS).
- Цветные растровые/многоцветные картинки (аватары, превью, логотипы) — обычный `<img src="assets/img/…">`.
- Имя файла — латиницей, kebab-case, с префиксом раздела (например `chat-play.svg`, `perf-star.svg`).
- Уже есть в проекте (можно переиспользовать): `assets/icons/` — nav-dashboard, nav-tasks, nav-payments, nav-notifications,
  nav-notification-settings, nav-chats, nav-support, nav-settings, nav-logout, nav-chevron, calendar, chevron-down, chevron-down-sm,
  link, return, edit, video, record, captcha-help, check-circle, check, stat-wallet, stat-created, stat-done, visa, mastercard,
  telegram, viber, bell, chat, avatar, radio-on/off/disabled, m-bell, m-home, m-tasks, m-mail, m-card, m-sliders.
  `assets/img/` — logo.png, logo-wordmark.svg, map.webp, webpay.png, belkart.png.

## Дизайн-токены (css/base.css, используйте переменные)
Цвета: --c-primary #52c865; --c-text #212121; --c-text-3 #3f3f3f; --c-muted #b6b6b6; --c-muted-2 #878787; --c-muted-3 #979797;
--c-border #d8d8d8; --c-border-2 #e0e0e0; --c-gray #e8e8e8; --c-gray-bg #fafafa; --c-success-bg #ecfdf3; --c-success-text #027a48; --c-yellow #f9ba39.
Тени: --shadow-card 0 0 2px rgba(82,200,101,.25); --shadow-card-lg 0 0 7.3px rgba(82,200,101,.35). Радиусы: --radius 8px, --radius-lg 12px, --radius-xl 16px.
Шрифт: Gilroy (300 Light / 400 Regular / 500 Medium / 600 SemiBold / 700 Bold) — уже подключён, используйте font-weight.
Готовые классы: `.btn .btn--primary|--gray|--outline|--pill|--lg|--block`, `.card .card--lg`, `.field .field__label .input .textarea`,
`.radio` (см. base.css), `.badge .badge--success`, `.m-tabs .m-tabs__tab .is-active`, `.m-section-title` (20px SemiBold).
Мобильные кнопки в макетах: высота 48px, radius 8px, зелёная заливка (`.btn .btn--primary` + свой класс с height:48px) или
белая с рамкой 0.5px #52c865 и зелёным текстом Light 16.

## Правила
- Верстать семантично (nav/ul/li, button, label+input, h1–h3), классы в BEM-стиле (`.chat__bubble`, `.chat__bubble--own`).
- Никаких абсолютных позиционирований «как в Figma» — flex/grid; размеры/отступы/цвета/шрифты брать точно из макета Figma.
- Один CSS-файл на секцию: `css/<section>.css`. Стили писать так, чтобы на ≥768px страница тоже выглядела прилично
  (контент центрирован, max-width ~600px), но приоритет — мобильная точность.
- Интерактив (табы, переключатели, поиск, отправка сообщения) — небольшой JS в `js/<section>.js`; тег
  `<script src="js/<section>.js"></script>` добавляется в конец `body`-строки страницы (после контента).
- Все тексты — из макета (русский, без изменений).
