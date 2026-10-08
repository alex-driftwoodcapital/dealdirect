#!/usr/bin/env python3
"""Build index/acss-index.json from the saved staging stylesheet (read-only input).

Usage: python3 -I scripts/build-index.py [--css index/automatic.css] [--out index/acss-index.json]
Inputs : index/automatic.css (compiled ACSS), reference/*.md (recipes), reference/staging-4.0.1-facts.md (absent-names table)
Output : flat list of entries. Never writes a stylesheet; the index is data for verify.py and lookups.
Entry  : {name, kind, group, status, since, doc, replacement, pattern(absent only: regex a name must match to be flagged)}
  kind   variable | class | recipe | absent
  verify.py rule: check "present" before "absent" (absent patterns like .text--{weight} are broad).
  status present (in the compiled stylesheet) | documented (4.x docs, not checkable in CSS, e.g. recipes) | absent (documented or 3.x name the build does not output)
  since  4.x for all present entries; 3.x for absent names that came from 3.x
"""
import argparse, json, re, sys, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
D = 'https://docs.automaticcss.com/'
DOCS = [  # keyword in "/* Feat: ... */" group -> official doc page
    ('Palette', 'colors/palette-intro'), ('Space', 'spacing/spacing-variables'), ('Section', 'spacing/section-spacing'),
    ('Smart Spacing', 'spacing/smart-spacing'), ('Contextual', 'spacing/contextual-spacing'), ('Gap', 'spacing/automatic-spacing'),
    ('Text', 'typography/fluid-text'), ('Heading', 'typography/fluid-headings'), ('Width', 'dimension/width-utilities'),
    ('Content Grid', 'grids/content-grid'), ('Grid', 'grids/grid-variables'), ('Column', 'columns/css-columns'),
    ('Button', 'buttons/button-variables'), ('Icon', 'icons/icon-framework'), ('Link', 'links/link-styling'),
    ('Focus', 'accessibility/focus-styling'), ('Border', 'borders-dividers/global-border-system'),
    ('Divider', 'borders-dividers/global-divider-system'), ('Shadow', 'shadow-filters/shadows-overview'),
    ('Radius', 'borders-dividers/global-border-system'), ('Overlay', 'overlays/overlay-classes'),
    ('Transition', 'effects/transition'), ('Sticky', 'effects/sticky'), ('Header', 'dimension/header-height'),
    ('Blockquote', 'elements/blockquotes'), ('Is Background', 'backgrounds/is-background-is-bg'),
    ('Position', 'effects/sticky'), ('Section Padding', 'spacing/section-padding-classes'),
    ('Default Section', 'spacing/section-spacing'), ('Body', 'typography/default-typography-styling'),
    ('Reset', 'setup/whats-new-in-4'),
]
PREFIX = [  # name prefix -> doc page (checked before the Feat group; more reliable)
    ('btn--', 'buttons/button-classes'), ('btn-', 'buttons/button-variables'), ('section-space', 'spacing/section-spacing'),
    ('section--', 'spacing/section-padding-classes'), ('header--', 'spacing/header-padding-classes'),
    ('space-', 'spacing/spacing-variables'), ('gutter', 'spacing/spacing-variables'), ('width-', 'dimension/width-utilities'),
    ('width--', 'dimension/width-utilities'), ('content-width', 'dimension/content-width'), ('content--', 'grids/content-grid'),
    ('content-grid', 'grids/content-grid'), ('grid-auto', 'grids/auto-grids'), ('grid-', 'grids/grid-variables'),
    ('container-gap', 'spacing/contextual-spacing'), ('content-gap', 'spacing/contextual-spacing'),
    ('text-', 'typography/fluid-text'), ('h', 'typography/fluid-headings'), ('heading-', 'typography/typography-variables'),
    ('icon', 'icons/icon-framework'), ('smart-spacing', 'spacing/smart-spacing'), ('box-shadow', 'shadow-filters/box-shadows'),
    ('drop-shadow', 'shadow-filters/drop-shadows'), ('ease-', 'effects/easing-presets'), ('focus-', 'accessibility/focus-styling'),
    ('radius', 'borders-dividers/global-border-system'), ('sticky', 'effects/sticky'), ('overlay', 'overlays/overlay-classes'),
    ('visible-', 'effects/visible-effects'), ('is-bg', 'backgrounds/is-background-is-bg'), ('link-', 'links/link-styling'),
    ('blockquote', 'elements/blockquotes'), ('blockquote-', 'elements/blockquotes'), ('col-', 'columns/css-columns'),
    ('border', 'borders-dividers/global-border-system'), ('divider', 'borders-dividers/global-divider-system'),
    ('header-height', 'dimension/header-height'), ('bg-', 'color-assignments/background-text-assignments'),
    ('palette', 'colors/palette-intro'),
]
def doc_for(group, name):
    n = name.lstrip('.-')
    for k, p in PREFIX:
        if n.startswith(k) and not (k == 'h' and not re.match(r'h[1-6]\b', n)): return D + p
    if re.match(r'(primary|secondary|tertiary|accent|base|neutral|white|black)\b', n): return D + 'colors/palette-intro'
    if n.startswith(('bg--', 'text--dark', 'text--light')): return D + 'color-assignments/background-text-assignments'
    if n.startswith('text--'): return D + 'typography/text-classes'
    if n.startswith(('on-visible', 'on-enter', 'on-exit')): return D + 'effects/visible-effects'
    if n.startswith('scheme--'): return D + 'color-scheme/implementing-color-scheme'
    if n.startswith(('hidden-accessible', 'skip-link')): return D + 'accessibility/hidden-accessible-class'
    if n.startswith('unrelate'): return D + 'buttons/button-styling'
    for k, p in DOCS:
        if k.lower() in group.lower(): return D + p
    return D + 'setup/whats-new-in-4'

def parse_css(path):
    css = open(path).read()
    ver = re.search(r'Version:\s*([\d.]+)', css)
    group, out, primary = 'Unknown', {}, {}
    # walk top-level so selectors and declarations keep their feature group
    for m in re.finditer(r'/\*\s*Feat:\s*([^*]+?)\s*\*/|([^{}/]+)\{([^{}]*)\}', css):
        if m.group(1): group = m.group(1); continue
        sel, body = m.group(2), m.group(3)
        for v in re.findall(r'^\s*(--[\w-]+)\s*:', body, re.M):
            out.setdefault((v, 'variable'), group)
        if not sel.strip().startswith(':root'):
            lead = re.match(r'\s*\.([A-Za-z][\w-]*)', sel)  # group where the class is the main selector wins
            for c in re.findall(r'\.([A-Za-z][\w-]*)', sel):
                if lead and lead.group(1) == c: primary[('.' + c, 'class')] = primary.get(('.' + c, 'class'), group)
                out.setdefault(('.' + c, 'class'), group)
    out.update(primary)
    return ver.group(1) if ver else 'unknown', out

def recipes():
    names = set()
    for f in (ROOT / 'reference').glob('*.md'):
        if f.name.startswith('staging'): continue
        names |= set(re.findall(r'\?([a-z][a-z0-9-]*(?:-\{[a-z-]+\})?)(?=[;\s`,)\]]|$)', f.read_text()))
    names |= {f'grid-{i}' for i in range(1, 13)}
    skip = {'recipe', 'name'}
    return sorted(n for n in names if n not in skip and not n.endswith('-clr') and '{' not in n)

def to_regex(n):
    """Pattern for an absent name: N = digits, * or {..} = anything, trailing -- = any suffix."""
    W = r'[\w-]+'
    out, i = '', 0
    while i < len(n):
        c = n[i]
        if c == '{':
            i = n.index('}', i); out += W
        elif c == '*': out += r'[\w-]*'
        elif c == 'N': out += r'\d+'
        else: out += re.escape(c)
        i += 1
    if n.endswith('--'): out += W
    return '^' + out + '$'

def absent():
    t = (ROOT / 'reference' / 'staging-4.0.1-facts.md').read_text()
    sec = t.split('## Documented but absent in 4.0.1', 1)[1].split('\n## ', 1)[0]
    rows = []
    for line in sec.splitlines():
        if not line.startswith('|') or line.startswith('|---') or 'Documented name' in line: continue
        cells = [c.strip() for c in line.strip('|').split('|')]
        if len(cells) < 3: continue
        for n in re.findall(r'`([^`]+)`', cells[0]):
            n = n.split(' ')[0]
            if n[0] in '.?' or n.startswith('--'): rows.append((n, cells[2]))
    return rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--css', default=str(ROOT / 'index/automatic.css'))
    ap.add_argument('--out', default=str(ROOT / 'index/acss-index.json'))
    a = ap.parse_args()
    ver, found = parse_css(a.css)
    entries = []
    for (name, kind), grp in sorted(found.items()):
        if kind == 'class':  # the stylesheet's Feat comments are unreliable for class selectors: group by docs section
            grp = doc_for(grp, name)[len(D):].split('/')[0].replace('-', ' ').title()
        entries.append(dict(name=name, kind=kind, group=grp, status='present', since='4.x', doc=doc_for(grp, name), replacement=None))
    for r in recipes():
        entries.append(dict(name='?' + r, kind='recipe', group='Recipes', status='documented', since='4.x',
                            doc=D + 'recipes', replacement=None))
    for n, rep in absent():
        entries.append(dict(name=n, kind='absent', group='Not in 4.0.1 build', status='absent', since='3.x',
                            doc=D + 'setup/whats-new-in-4', replacement=rep, pattern=to_regex(n)))
    meta = dict(acss_version=ver, source=pathlib.Path(a.css).name, built=datetime.date.today().isoformat(),
                counts={k: sum(1 for e in entries if e['kind'] == k) for k in ('variable', 'class', 'recipe', 'absent')},
                note='Names ending in "-" or containing N/{...} in absent entries are patterns. Do not deploy; read-only reference.')
    json.dump(dict(meta=meta, entries=entries), open(a.out, 'w'), indent=1)
    print(json.dumps(meta['counts']), 'ACSS', ver)

if __name__ == '__main__':
    sys.exit(main())
