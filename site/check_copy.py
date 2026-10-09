#!/usr/bin/env python3
"""Copy gate: every design string is on the page and every page string is design copy (or listed as non-design).
usage: python3 -I site/check_copy.py eb5"""
import html, importlib, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, 'pages'), os.path.join(HERE, 'lib')]
import etch
from design import norm

mod = importlib.import_module(sys.argv[1])
mine = [norm(t) for t in etch.all_texts(mod.PAGE)]
design = set(mod.q.all) if mod.q else set()  # q None: a part with no visible copy (header logo, template)
# COPY_EXTRA: more design regions whose strings may be used (not all required); DYNAMIC_COPY: design strings that the
# page renders with a runtime value in place of the design's sample (e.g. the offering name), so not required verbatim.
for extra_copy in getattr(mod, 'COPY_EXTRA', []):
    design |= set(extra_copy.all)
# A text that is one dynamic expression ({item.title}, {item.meta.x.equal("a", "Open", "Closed")}) is data, not copy;
# but every quoted literal in it is shown text, so it must be verbatim in the design source (identifiers such as
# field values "coming_soon" excepted). Same for an offering's card field values (META['fields'], Home design data).
SOURCE = os.path.join(HERE, '..', 'handoff', 'design', getattr(mod, 'COPY_SOURCE', ''))
raw = html.unescape(open(SOURCE, encoding='utf-8').read()) if getattr(mod, 'COPY_SOURCE', None) else ''
def in_source(lit):
    return re.fullmatch(r'[a-z_]*', lit) or lit in raw
expr = [t for t in mine if re.fullmatch(r'\{[^{}]*(\{[^{}]*\}[^{}]*)*\}', t) and not t.startswith('{options.')]
literals = [l for t in expr for l in re.findall(r'"([^"]*)"', t) if not in_source(l)]
field_vals = [v for v in getattr(mod, 'META', {}).get('fields', {}).values()
              if isinstance(v, str) and not v.startswith('{{') and not in_source(v)]
extra = [t for t in mine if t and t not in design and t not in mod.NON_DESIGN and not t.startswith('{options.') and t not in expr]
extra += [f'expression literal {l!r}' for l in literals] + [f'card field value {v!r}' for v in field_vals]
missing = [t for t in (mod.q.all if mod.q else []) if t not in set(mine) and t not in getattr(mod, 'DYNAMIC_COPY', set())]
banned = [t for t in mine if 'shovel' in t.lower()]  # CLAUDE.md rule 2
for label, items in (('not design copy', extra), ('design copy missing from page', missing), ('banned wording', banned)):
    for t in items:
        print(f'{label}: {t[:100]}')
print(f'{len(mine)} strings checked, {len(extra) + len(missing) + len(banned)} problem(s)')
sys.exit(1 if extra or missing or banned else 0)
