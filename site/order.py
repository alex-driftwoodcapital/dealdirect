#!/usr/bin/env python3
"""Print site/pages modules in deploy order (META['order']; pages default 100): components, templates, pages."""
import glob, importlib, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, 'pages'), os.path.join(HERE, 'lib')]
mods = [os.path.basename(f)[:-3] for f in glob.glob(os.path.join(HERE, 'pages', '*.py'))]
for m in sorted(mods, key=lambda m: (getattr(importlib.import_module(m), 'META', {}).get('order', 100), m)):
    print(m)
