# CodeLab — многостраничный сайт IT-школы (Лабораторная работа №2)

**Сайт:** https://arsenfatkhullin21.github.io/webdesign-lab2/ · **UI Kit:** https://arsenfatkhullin21.github.io/webdesign-lab2/uikit.html

Адаптивный сайт на 7 страниц с дизайн-системой, тёмной темой и микроанимациями. Без сборщиков и зависимостей: чистые HTML/CSS/JS.

## Запуск

Откройте `index.html` в браузере или поднимите сервер: `python3 -m http.server 8000`.

## Структура

```
index.html  courses.html  course.html  teachers.html  blog.html  post.html  contacts.html  uikit.html
css/   tokens.css  base.css  layout.css  components.css  pages.css
js/    theme.js  menu.js  scroll.js
img/   logo.svg, favicon.svg, photos/ (SVG-иллюстрации)
tools/build.py   генератор страниц (шапка/подвал/крошки — единый шаблон)
report/          ОТЧЁТ.md (источник отчёта), скриншоты, замеры Lighthouse/WAVE/WebAIM
```

## Как менять страницы

HTML генерируется скриптом: правьте `tools/build.py` и запускайте `python3 tools/build.py`. Так шапка, подвал и мобильное меню гарантированно одинаковы на всех страницах, а активный пункт меню ставится автоматически.

## Что реализовано

- Дизайн-токены: примитивные и семантические (цвета, типографика, отступы, радиусы, тени, переходы).
- Тёмная тема: `data-theme` на `<html>`, переключатель в шапке, `localStorage`, автоопределение через `prefers-color-scheme`, ранний inline-скрипт без «вспышки».
- Анимации: hover на кнопках/карточках/ссылках, появление при скролле (IntersectionObserver), прогресс-бар прокрутки, `scroll-behavior: smooth`, плавное мобильное меню, `prefers-reduced-motion`.
- Доступность: skip-link, `aria-current`, `aria-expanded`, `aria-pressed`, подписи к полям, видимый фокус, Esc закрывает меню.
