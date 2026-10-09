#!/usr/bin/env python3
"""Local preview of a built page (NOT the real Etch render): block markup -> plain HTML + style records as CSS,
on top of an ACSS 4.0.1 stylesheet with DealDirect's brand colours. Good for layout/overflow checks at
375/768/1440 before anything reaches staging; the real check is on staging after deploy.
usage: python3 -I site/preview.py eb5 [--template template_page]   -> build/eb5/preview.html
With --template, the page is shown inside the template, its components (header/footer) expanded in place. SVGs that
can't be fetched here (live site unreachable from some sessions) fall back to the handoff's Driftwood logo."""
import html, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
sys.path[:0] = [os.path.join(HERE, 'lib'), os.path.join(HERE, 'pages')]
import etch

import argparse, svg
ap = argparse.ArgumentParser(); ap.add_argument('page'); ap.add_argument('--template')
args = ap.parse_args()
page = args.page
B = os.path.join(ROOT, 'build', page)
records = json.load(open(os.path.join(B, 'records.json')))
media = json.load(open(os.path.join(B, 'media.json')))
tpl_markup = None
if args.template:
    T = os.path.join(ROOT, 'build', args.template)
    tpl_markup = open(os.path.join(T, 'content.tpl.html')).read()
    for slug_mod in sorted(set(re.findall(r'\{\{ref:([^}]*)\}\}', tpl_markup))):
        mod_dir = os.path.join(ROOT, 'build', slug_mod.replace('-', '_'))
        records.update(json.load(open(os.path.join(mod_dir, 'records.json'))))
        part = open(os.path.join(mod_dir, 'content.tpl.html')).read()
        tpl_markup = re.sub(r'<!-- wp:etch/component \{[^>]*"\{\{ref:%s\}\}"[^>]*-->\s*<!-- /wp:etch/component -->' % re.escape(slug_mod), lambda m: part, tpl_markup)


def fetch_or_standin(url):
    try:
        return svg.fetch(url)
    except Exception:
        return open(os.path.join(ROOT, 'handoff', 'design', 'assets', 'logo-driftwood-capital.svg')).read()
fixtures = os.path.join(ROOT, '.claude', 'skills', 'etch-expert', 'reference', 'fixtures', 'styles-used.json')
builtin = {k: v for k, v in json.load(open(fixtures)).items() if k.startswith('etch-')}
sel2id = {v['selector']: k for k, v in {**records, **builtin}.items()}
# local files render as-is; live-site images (unreachable here) become a labelled grey placeholder
src_of = {}
for slug, m in media.items():
    src = m['src'] if isinstance(m, dict) else m
    src_of[slug] = os.path.relpath(os.path.join(ROOT, src), B) if not src.startswith('http') else ''
body = open(os.path.join(B, 'content.tpl.html')).read()
if tpl_markup:
    body = tpl_markup.replace('<!-- wp:post-content {"align":"full","layout":{"type":"default"}} /-->', body)


def offering_items():
    """Loop data for the preview: every offering module's META (slug + card fields), as Etch would see the posts."""
    import glob, importlib
    items = []
    for f in sorted(glob.glob(os.path.join(HERE, 'pages', 'offering_*.py'))):
        m = importlib.import_module(os.path.basename(f)[:-3])
        meta = dict(m.META.get('fields', {}))
        for k, v in meta.items():
            mm = re.fullmatch(r'\{\{media:([^}]*)\}\}', str(v))
            if mm:
                meta[k] = mm.group(1)
                media.setdefault(mm.group(1), m.MEDIA[mm.group(1)][0])
        items.append({'slug': m.META['slug'], 'permalink': {'relative': f"/offering/{m.META['slug']}/"}, 'meta': meta})
    return items


def expand_loops(markup, loops):
    """Expand etch/loop blocks (nested too) the way the page's LOOPS queries would: meta_query IN on the offerings,
    ordered by home_order, posts_per_page honoured. {item.x.y} and .equal(a, t, f) are evaluated; nothing else is."""
    open_re = re.compile(r'<!-- wp:etch/loop (\{.*?\}) -->')
    m = open_re.search(markup)
    if not m:
        return markup
    depth, i = 1, m.end()
    while depth:
        nxt_open, nxt_close = open_re.search(markup, i), markup.find('<!-- /wp:etch/loop -->', i)
        if nxt_open and nxt_open.start() < nxt_close:
            depth, i = depth + 1, nxt_open.end()
        else:
            depth, i = depth - 1, nxt_close + len('<!-- /wp:etch/loop -->')
    d = json.loads(m.group(1))
    inner = markup[m.end():i - len('<!-- /wp:etch/loop -->')]
    args = loops[d['loopId']]['config']['args']
    want = args['meta_query'][0]['value']
    rows = sorted([it for it in ITEMS if it['meta'].get('offering_status') in want], key=lambda it: it['meta'].get('home_order', 0))
    if args.get('posts_per_page', -1) > 0:
        rows = rows[:args['posts_per_page']]
    var = d['itemId']

    def value(it, path):
        for k in path.split('.'):
            it = it.get(k, '') if isinstance(it, dict) else ''
        return str(it)

    def sub(mm):
        v = value(it, mm.group(1))
        if mm.group(2):
            a = re.findall(r'\\"(.*?)\\"', mm.group(2))
            v = a[1] if v == a[0] else a[2]
        return v.replace('"', '\\"')
    out = []
    for it in rows:
        out.append(re.sub(r'\{' + var + r'\.([A-Za-z_.]+?)(?:\.equal\((.*?)\))?\}', sub, inner))
    return markup[:m.start()] + expand_loops(''.join(out), loops) + expand_loops(markup[i:], loops)


import importlib
page_mod = importlib.import_module(page)
ITEMS = offering_items() if getattr(page_mod, 'LOOPS', None) else []
for slug in list(media):
    m_ = media[slug]
    src = m_['src'] if isinstance(m_, dict) else m_
    src_of[slug] = os.path.relpath(os.path.join(ROOT, src), B) if not src.startswith('http') else ''
body = expand_loops(body, getattr(page_mod, 'LOOPS', {}))
markup = etch.resolve(svg.expand(body, fetch_or_standin), sel2id, {k: k for k in media}, None, src_of)
STATS = {'{options.acf.years_experience}': '30+', '{options.acf.properties}': '78', '{options.acf.aum}': '~$3.5B',
         '{options.acf.employees.numberFormat()}': '6,000', '{options.acf.as_of}': 'September 1, 2026'}

BLOCK = re.compile(r'<!--\s*(/)?wp:([a-z/-]+)\s*(\{.*?\})?\s*(/)?-->', re.S)
VOID = {'img', 'br', 'input'}
out, stack, scripts = [], [], []
for m in BLOCK.finditer(markup):
    close, name, raw, selfc = m.group(1), m.group(2), m.group(3), m.group(4)
    if close:
        tag = stack.pop()
        if tag and tag not in VOID:
            out.append(f'</{tag}>')
        continue
    d = json.loads(raw) if raw else {}
    if name == 'etch/text':
        t = d.get('content', '')
        for k, v in STATS.items():
            t = t.replace(k, v)
        out.append(html.escape(t))
        continue
    attrs = d.get('attributes') or {}
    if name == 'etch/dynamic-image':
        slug = attrs['mediaId']
        s = src_of.get(slug, '')
        if s:
            out.append(f'<img src="{s}" alt="{html.escape(attrs.get("alt", ""))}" loading="{attrs.get("loading")}">')
        else:
            out.append(f'<img alt="{html.escape(attrs.get("alt", ""))}" style="background:#9aa7b4" data-missing="{slug}">')
        stack.append('img')
        continue
    tag = d.get('tag', 'div')
    if d.get('script'):
        import base64
        scripts.append(base64.b64decode(d['script']['code']).decode())
    a = ''.join(f' {k}="{html.escape(str(v))}"' for k, v in attrs.items())
    out.append(f'<{tag}{a}>')
    stack.append(tag)

css = []
for rec in {**builtin, **records}.values():
    if rec['css']:
        css.append(f"{rec['selector']} {{\n{rec['css']}\n}}")
acss = open(os.path.join(ROOT, '.claude', 'skills', 'acss-expert', 'index', 'automatic.css')).read()
brand = """:root{--primary:#0B2B48;--primary-ultra-dark:#061A2E;--primary-semi-dark:#14385B;--secondary:#2468A8;--secondary-dark:#1B5388;
--accent:#6FB0E0;--base:#F5F6F8;--base-light:#E9ECF0;--base-semi-light:#D3D8E0;--base-dark:#2E3744;--white:#fff;
--text-dark:#48535F;--content-width:1334px;--gutter:32px;--primary-semi-light:#22527F}
body{margin:0;font-family:"Plus Jakarta Sans",system-ui,sans-serif;color:#48535F;background:#fff}
h1,h2,h3,h4{font-weight:300;color:var(--primary-ultra-dark)}
@media (width < 768px){:root{--gutter:16px}}"""
doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{page} preview</title><style>{acss}</style><style>{brand}</style><style>{chr(10).join(css)}</style></head>
<body>{''.join(out) if tpl_markup else '<main>' + ''.join(out) + '</main>'}{''.join('<script type="module">' + c + '</script>' for c in scripts)}</body></html>"""
open(os.path.join(B, 'preview.html'), 'w').write(doc)
print(os.path.relpath(os.path.join(B, 'preview.html'), ROOT))
