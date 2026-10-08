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
css = os.path.join(HERE, 'styles', a.page + '.css')
classes = etch.all_classes(mod.PAGE)
rules = styles.parse(css) if os.path.exists(css) else {}
unused = [s for s in rules if s[1:] not in classes]
if unused:
    sys.exit(f'rules for classes not on the page: {unused}')
# Library sheets (site/styles/shared.css, offering.css, ...) hold classes used by more than one page: each page takes
# the rules for its own classes from there, so every page deploys the same css for a class. A selector may live in
# one sheet only.
seen = set(rules)
for lib in getattr(mod, 'STYLESHEETS', ['shared']):
    sheet = styles.parse(os.path.join(HERE, 'styles', lib + '.css'))
    dup = sorted(seen & set(sheet))
    if dup:
        sys.exit(f'{a.page}: {dup} defined twice (site/styles/{lib}.css and another sheet); keep one')
    seen |= set(sheet)
    rules.update({s: r for s, r in sheet.items() if s[1:] in classes})
if classes and not rules:
    sys.exit(f'{a.page}: classes on the page but no {os.path.relpath(css)}')
hooks = [c for c in classes if '.' + c not in rules]
if hooks:
    print(f'{a.page}: {len(hooks)} class hook(s) without css (containers, ACSS utilities, or a typo?): {" ".join(hooks)}')
open(os.path.join(out, 'content.tpl.html'), 'w').write(etch.page(mod.PAGE))
json.dump(styles.records(classes, rules), open(os.path.join(out, 'records.json'), 'w'), indent=1, ensure_ascii=False)
media = {}
for slug, v in mod.MEDIA.items():
    src, coll, name = (tuple(v) + (None,))[:3] if isinstance(v, tuple) else (v, None, None)
    if not coll:
        sys.exit(f'{a.page}: media {slug} has no Asset Manager collection (MEDIA = {{slug: (source, collection[, filename])}})')
    media[slug] = {'src': src, 'collection': coll, **({'name': name} if name else {})}
json.dump(media, open(os.path.join(out, 'media.json'), 'w'), indent=1)
json.dump(getattr(mod, 'META', {}), open(os.path.join(out, 'meta.json'), 'w'), indent=1, ensure_ascii=False)
print(f'{a.page}: {len(classes)} classes, {len(mod.MEDIA)} media -> {os.path.relpath(out)}')
