#!/usr/bin/env python3
"""Copy gate: every design string is on the page and every page string is design copy (or listed as non-design).
usage: python3 -I site/check_copy.py eb5"""
import importlib, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, 'pages'), os.path.join(HERE, 'lib')]
import etch
from design import norm

mod = importlib.import_module(sys.argv[1])
mine = [norm(t) for t in etch.all_texts(mod.PAGE)]
design = set(mod.q.all)
extra = [t for t in mine if t and t not in design and t not in mod.NON_DESIGN and not t.startswith('{options.')]
missing = [t for t in mod.q.all if t not in set(mine)]
banned = [t for t in mine if 'shovel' in t.lower()]  # CLAUDE.md rule 2
for label, items in (('not design copy', extra), ('design copy missing from page', missing), ('banned wording', banned)):
    for t in items:
        print(f'{label}: {t[:100]}')
print(f'{len(mine)} strings checked, {len(extra) + len(missing) + len(banned)} problem(s)')
sys.exit(1 if extra or missing or banned else 0)
