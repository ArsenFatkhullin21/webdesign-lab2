#!/usr/bin/env python3
"""Генерирует таблицы отчёта (report/_gen/*.md) из замеров report/data.json."""
import json
from pathlib import Path

R = Path(__file__).resolve().parent
d = json.loads((R / 'data.json').read_text(encoding='utf-8'))
G = R / '_gen'; G.mkdir(exist_ok=True)
NAMES = {'index': 'Главная', 'courses': 'Курсы', 'course': 'Карточка курса', 'teachers': 'Преподаватели',
         'blog': 'Блог', 'post': 'Статья', 'contacts': 'Контакты', 'uikit': 'UI Kit'}
import re
fmt = lambda v: re.sub(r'(\d)\s*s$', r'\1 с', re.sub(r'(\d)\s*ms$', r'\1 мс', v)) if isinstance(v, str) else v

lh = {(x['page'], x['device']): x for x in d['lighthouse']}
rows = ['| Страница | Устройство | Performance | Accessibility | Best Practices | SEO | LCP | CLS | TBT |', '|---|---|---|---|---|---|---|---|---|']
for pg in NAMES:
    for dev, dn in (('mobile', 'Mobile'), ('desktop', 'Desktop')):
        x = lh[(pg, dev)]
        rows.append(f'| {NAMES[pg]} | {dn} | {x["performance"]} | {x["accessibility"]} | {x["bestPractices"]} | {x["seo"]} | {fmt(x["lcp"])} | {x["cls"]} | {fmt(x["tbt"])} |')
(G / 'lighthouse.md').write_text('\n'.join(rows) + '\n', encoding='utf-8')

avg = lambda key, dev: round(sum(lh[(p, dev)][key] for p in NAMES) / len(NAMES))
summary = {dev: {k: avg(k, dev) for k in ('performance', 'accessibility', 'bestPractices', 'seo')} for dev in ('mobile', 'desktop')}
(G / 'lighthouse-summary.md').write_text(
    f'Средние баллы по {len(NAMES)} страницам: mobile — Performance {summary["mobile"]["performance"]}, Accessibility {summary["mobile"]["accessibility"]}, '
    f'Best Practices {summary["mobile"]["bestPractices"]}, SEO {summary["mobile"]["seo"]}; desktop — Performance {summary["desktop"]["performance"]}, '
    f'Accessibility {summary["desktop"]["accessibility"]}, Best Practices {summary["desktop"]["bestPractices"]}, SEO {summary["desktop"]["seo"]}.\n', encoding='utf-8')

rows = ['| Страница | Errors | Contrast Errors | Alerts | Features | Structure | ARIA | AIM Score |', '|---|---|---|---|---|---|---|---|']
for x in d['wave']:
    rows.append(f'| {NAMES[x["page"]]} | {x["errors"]} | {x["contrast"]} | {x["alerts"]} | {x["features"]} | {x["structure"]} | {x["aria"]} | {x["aim"]} / 10 |')
(G / 'wave.md').write_text('\n'.join(rows) + '\n', encoding='utf-8')

rows = ['| Пара цветов | Текст | Фон | Контраст (WebAIM) | WCAG AA (обычный текст ≥ 4.5:1) |', '|---|---|---|---|---|']
for x in d['contrast']:
    ok = float(x['ratio'].split(':')[0]) >= 4.5
    rows.append(f'| {x["label"]} | `#{x["fg"]}` | `#{x["bg"]}` | **{x["ratio"]}** | {"пройдено" if ok else "не пройдено"} |')
(G / 'contrast.md').write_text('\n'.join(rows) + '\n', encoding='utf-8')

if 'contrastBefore' in d:
    rows = ['| Исходная пара | Текст | Фон | Контраст (WebAIM) | Итог |', '|---|---|---|---|---|']
    for x in d['contrastBefore']:
        rows.append(f'| {x["label"]} | `#{x["fg"]}` | `#{x["bg"]}` | {x["ratio"]} | не проходит AA → токен изменён |')
    (G / 'contrast-before.md').write_text('\n'.join(rows) + '\n', encoding='utf-8')
