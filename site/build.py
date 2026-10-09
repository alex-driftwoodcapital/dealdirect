#!/usr/bin/env python3
"""Build a page for deploy: python3 -I site/build.py eb5 [--out build/eb5]
Writes content.tpl.html (Etch markup with {{style:}}/{{media:}} placeholders), records.json (style records for every
class on the page, from site/styles/<page>.css) and media.json (slug -> source). Fails if the copy gate fails."""
import argparse, importlib, json, os, re, subprocess, sys
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
# Font sizes come from ACSS's type tokens (var(--h2), var(--text-m)...; scale in ops/acss/build-settings.py), never
# px/rem/clamp() in page CSS: refuse a literal size so the pages keep following the ACSS scale.
literal = sorted({sel for sel, css in rules.items()
                  for v in re.findall(r'font-size:\s*([^;}]+)', css) if not re.match(r'(var\(--|inherit|1em|100%)', v.strip())})
if literal:
    sys.exit(f'{a.page}: literal font sizes (use an ACSS token, e.g. var(--text-m)): {" ".join(literal)}')
# Spacing likewise comes from ACSS's spacing tokens (var(--space-m), var(--section-space-l), bridge tokens such as
# var(--space-xl-to-l)), never a hand-written clamp(). The one exception is the Home hero's top padding, which clears
# the fixed header rather than following the spacing scale.
CLAMP_OK = {'.home-hero__inner'}
fluid = sorted(sel for sel, css in rules.items() if 'clamp(' in css and sel not in CLAMP_OK)
if fluid:
    sys.exit(f'{a.page}: hand-written clamp() (use an ACSS spacing token, e.g. var(--section-space-m)): {" ".join(fluid)}')
hooks = [c for c in classes if '.' + c not in rules]
# A hook still gets a style record, so a class styled in a sheet this page doesn't load would overwrite that sheet's
# record with empty css on staging (every page deploys every record for its classes): refuse to build.
elsewhere = {}
for f in sorted(os.listdir(os.path.join(HERE, 'styles'))):
    if f.endswith('.css'):
        for sel in styles.parse(os.path.join(HERE, 'styles', f)):
            if sel[1:] in hooks:
                elsewhere.setdefault(f, []).append(sel)
if elsewhere:
    sys.exit(f'{a.page}: classes styled in sheets this page does not load (add them to STYLESHEETS): '
             + '; '.join(f'site/styles/{f}: {" ".join(v[:5])}{" ..." if len(v) > 5 else ""}' for f, v in elsewhere.items()))
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
json.dump(getattr(mod, 'LOOPS', {}), open(os.path.join(out, 'loops.json'), 'w'), indent=1, ensure_ascii=False)
print(f'{a.page}: {len(classes)} classes, {len(mod.MEDIA)} media -> {os.path.relpath(out)}')
