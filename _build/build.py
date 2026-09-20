# -*- coding: utf-8 -*-
"""Сборка всех страниц: python _build/build.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import OUT
import pages_tasks

pages = {}
pages.update(pages_tasks.pages)
for mod in ('pages_chats', 'pages_notifications', 'pages_performers'):
    try:
        m = __import__(mod)
        pages.update(m.pages)
    except ImportError:
        pass

for name, html in pages.items():
    with open(os.path.join(OUT, name), 'w', encoding='utf-8') as f:
        f.write(html)
    print('wrote', name)
