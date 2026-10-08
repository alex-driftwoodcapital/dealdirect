#!/usr/bin/env python3
"""Build a page for deploy: python3 -I site/build.py eb5 [--out build/eb5]
Writes content.tpl.html (Etch markup with {{style:}}/{{media:}} placeholders), records.json (style records for every
class on the page, from site/styles/<page>.css) and media.json (slug -> source). Fails if the copy gate fails."""
import argparse, importlib, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, 'pages'), os.path.join(HERE, 'lib')]
import etch, styles

ap = argparse.ArgumentParser()
ap.add_argument('page')
ap.add_argument('--out')
a = ap.parse_args()
if subprocess.run([sys.executable, '-I', os.path.join(HERE, 'check_copy.py'), a.page]).returncode:
    sys.exit('copy gate failed')
mod = importlib.import_module(a.page)
out = a.out or os.path.join(HERE, '..', 'build', a.page)
os.makedirs(out, exist_ok=True)
rules = styles.parse(os.path.join(HERE, 'styles', a.page + '.css'))
classes = etch.all_classes(mod.PAGE)
unused = [s for s in rules if s[1:] not in classes]
if unused:
    sys.exit(f'rules for classes not on the page: {unused}')
open(os.path.join(out, 'content.tpl.html'), 'w').write(etch.page(mod.PAGE))
json.dump(styles.records(classes, rules), open(os.path.join(out, 'records.json'), 'w'), indent=1, ensure_ascii=False)
json.dump(mod.MEDIA, open(os.path.join(out, 'media.json'), 'w'), indent=1)
json.dump(getattr(mod, 'META', {}), open(os.path.join(out, 'meta.json'), 'w'), indent=1, ensure_ascii=False)
print(f'{a.page}: {len(classes)} classes, {len(mod.MEDIA)} media -> {os.path.relpath(out)}')
