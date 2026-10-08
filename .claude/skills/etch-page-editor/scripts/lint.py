#!/usr/bin/env python3
"""Lint Etch block markup (post_content) against what real saved markup looks like.
usage: lint.py [--styles etch_styles.json] [--loops etch_loops.json] [--acss-css automatic.css] [--component] [--json] FILE...
Errors fail (exit 1); warnings do not. Rules derive from etch-expert/reference/fixtures/catalogue.md (Etch 1.6.8)."""
import re, sys, json, os, argparse

KNOWN = {'etch/element','etch/text','etch/component','etch/slot-content','etch/slot-placeholder','etch/condition',
         'etch/loop','etch/dynamic-image','etch/raw-html','post-content'}
SELF_CLOSING_OK = {'etch/text','etch/raw-html','post-content'}
FIX = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'etch-expert', 'reference', 'fixtures')
BLOCK = re.compile(r'<!--\s*(/)?wp:([a-z][a-z0-9/-]*)\s*(\{.*?\})?\s*(/)?-->', re.S)

def load(path, default):
    try: return json.load(open(path))
    except Exception: return default

def lint(text, styles, loops, acss, component):
    errs, warns = [], []
    def E(i, m): errs.append((i, m))
    def W(i, m): warns.append((i, m))
    sel2id = {v.get('selector'): k for k, v in styles.items()}
    stack, h1 = [], 0
    for n, m in enumerate(BLOCK.finditer(text), 1):
        close, name, raw, selfc = bool(m.group(1)), m.group(2), m.group(3), bool(m.group(4))
        where = f'block#{n} {name}'
        if close:
            if not stack or stack[-1][0] != name: E(where, f'closing wp:{name} does not match open block {stack[-1][0] if stack else "none"}')
            else: stack.pop()
            continue
        try: j = json.loads(raw) if raw else {}
        except Exception as e: E(where, f'invalid JSON: {e}'); j = {}
        if name not in KNOWN: E(where, 'unknown block type (not in catalogue)'); 
        if name.startswith('etch/') and name not in ('etch/slot-content','etch/slot-placeholder') and not (j.get('metadata') or {}).get('name'):
            W(where, 'missing metadata.name (builder tree label)')
        if selfc and name not in SELF_CLOSING_OK and name != 'etch/element': E(where, 'self-closing but this block normally has children')
        if not selfc: stack.append((name, j))
        parent = stack[-2] if not selfc and len(stack) > 1 else (stack[-1] if selfc and stack else None)
        if name == 'etch/text':
            if 'content' not in j: E(where, 'etch/text without content')
            if not parent or parent[0] not in ('etch/element',): W(where, 'text outside an etch/element')
        if name == 'etch/element':
            tag, attrs = j.get('tag'), j.get('attributes', None)
            if not tag: E(where, 'etch/element without tag')
            if tag == 'img': E(where, 'plain img element: use etch/dynamic-image bound by media ID')
            if attrs is None: E(where, 'missing attributes (use {} or [])')
            attrs = attrs if isinstance(attrs, dict) else {}
            if tag == 'h1': h1 += 1
            for a in attrs:
                if a == 'style': W(where, 'inline style attribute: only per-instance custom properties belong here; otherwise use a class/style record')
                if a.lower().startswith('on'): E(where, f'inline event handler {a}: use a data-* hook and a script')
            ids = j.get('styles', [])
            for sid in ids:
                if styles and sid not in styles: E(where, f'style id {sid} not in etch_styles')
            have = {styles[s].get('selector') for s in ids if s in styles}
            for c in str(attrs.get('class', '')).replace('\\u002d', '-').split():
                if not styles: break
                if '.' + c in have: continue
                if '.' + c in sel2id: W(where, f'class {c} has a style record but its id is not in "styles" (builder will add it on save)')
                elif acss is not None and c in acss: pass
                else: W(where, f'class {c} not in etch_styles' + ('' if acss is not None else ' (no ACSS list given)') )
            if 'id' in attrs and isinstance(attrs['id'], str) and not component:
                pass
            if 'script' in j and not (isinstance(j['script'], dict) and j['script'].get('code') and j['script'].get('id')): E(where, 'script needs code and id')
            if attrs.get('data-etch-element') == 'section': stack[-1][1]['_sec'] = True
            if not selfc and parent and parent[0] == 'etch/element' and parent[1].get('_sec') and attrs.get('data-etch-element') != 'container':
                W(where, 'direct child of a section should be the data-etch-element="container" div (Etch connector guide)')
            if not selfc and parent and parent[0] == 'etch/element' and parent[1].get('_sec'): parent[1]['_kids'] = parent[1].get('_kids', 0) + 1
        if name == 'etch/dynamic-image':
            a = j.get('attributes') or {}
            if not a.get('mediaId'): E(where, 'dynamic-image without mediaId')
            if j.get('tag') != 'img': W(where, 'dynamic-image tag is normally "img"')
        if name == 'etch/raw-html':
            if str(j.get('unsafe')) == 'true': E(where, 'unsafe raw HTML is disabled in this site\'s Etch settings')
            else: W(where, 'raw-html: use native elements if Etch can express it')
        if name == 'etch/condition':
            if not j.get('condition') or not j.get('conditionString'): E(where, 'condition needs both condition and conditionString')
        if name == 'etch/loop':
            if not j.get('loopId') or not j.get('itemId'): E(where, 'loop needs loopId and itemId')
            elif loops and j['loopId'] not in loops and not any(v.get('key') == j['loopId'] for v in loops.values()): E(where, f'loopId {j["loopId"]} not in etch_loops')
        if name == 'etch/component':
            if not isinstance(j.get('ref'), int): E(where, 'component without numeric ref')
            if not isinstance(j.get('attributes', []), (dict, list)): E(where, 'component attributes must be an object')
        if name in ('etch/slot-content', 'etch/slot-placeholder') and not j.get('name'): E(where, 'slot without name')
        if selfc and name == 'etch/element': pass
    if len(re.findall(r'<!--\s*/?wp:', text)) != len(BLOCK.findall(text)): E('page', 'malformed block comment (invalid JSON or missing -->): invalid JSON')
    for name, j in stack: E(f'wp:{name}', 'block never closed')
    if not component and re.search(r'\{props\.', text): W('page', '{props.*} used outside a component definition (use --component for component files)')
    if not component and h1 > 1: W('page', f'{h1} h1 elements')
    return errs, warns

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('files', nargs='+')
    ap.add_argument('--styles', default=os.path.join(FIX, 'styles-used.json')); ap.add_argument('--loops', default=os.path.join(FIX, 'loops-used.json'))
    ap.add_argument('--acss-css'); ap.add_argument('--component', action='store_true'); ap.add_argument('--json', action='store_true')
    a = ap.parse_args()
    styles, loops = load(a.styles, {}), load(a.loops, {})
    acss = None
    if a.acss_css: acss = set(re.findall(r'\.([A-Za-z_][\w-]*)', open(a.acss_css).read()))
    bad = 0; out = []
    for f in a.files:
        comp = a.component or '/components/' in os.path.abspath(f)
        errs, warns = lint(open(f).read(), styles, loops, acss, comp)
        bad += bool(errs); out.append({'file': f, 'errors': errs, 'warnings': warns})
        if not a.json:
            print(f'{"FAIL" if errs else "ok  "} {f}  ({len(errs)} errors, {len(warns)} warnings)')
            for i, m in errs: print(f'   ERROR {i}: {m}')
            for i, m in warns[:int(os.environ.get('LINT_MAX_WARN', 8))]: print(f'   warn  {i}: {m}')
    if a.json: print(json.dumps(out, indent=1))
    sys.exit(1 if bad else 0)
main()
