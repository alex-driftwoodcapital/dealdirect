#!/usr/bin/env python3
"""Design spec checker: blocks an Etch build when the design spec is missing anything the builder would have to guess.

CLI   python3 -I scripts/spec-check.py SPEC.yaml [--root DIR] [--acss-index FILE] [--site-styles etch_styles.json]
                                       [--no-acss] [--json]
      SPEC is YAML (needs PyYAML) or JSON. Reference and shot paths resolve against --root (default: the spec's folder).
Exit  0 = no errors (warnings allowed), 1 = errors (do not build), 2 = cannot read the spec.
Format and every rule: formats/design-spec.md. Etch rules behind the checks: etch-expert/reference/guardrails.md.
Stdlib only (plus PyYAML for .yaml); ACSS names are checked with acss-expert/index/acss-index.json.
"""
import argparse, json, pathlib, re, sys

HERE = pathlib.Path(__file__).resolve().parent
SKILLS = HERE.parent.parent  # .../skills (repo) or the folder the skills were unpacked into

ROLES = {'hero', 'intro', 'features', 'split', 'proof', 'quote', 'faq', 'list', 'cta', 'form', 'nav', 'footer',
         'logos', 'story', 'game', 'dialog', 'custom'}
LANDMARKS = {'section', 'header', 'footer', 'aside', 'nav', 'div', 'figure', 'dialog'}
NEEDS_HEADING = {'section', 'aside', 'dialog'}  # docs:/elements/section: every section starts with a heading; no heading -> div
CONTENT_TYPES = {'p', 'kicker', 'h2', 'h3', 'h4', 'h5', 'h6', 'list', 'link', 'button', 'quote', 'cite', 'label', 'embed', 'note'}
MUST_MATCH = {'order', 'copy', 'surface', 'columns', 'heading sizes', 'button roles', 'media', 'spacing', 'states', 'motion'}
LOADING = {'eager', 'lazy'}
FIT = {'cover', 'contain', 'none'}
PLACEHOLDER = re.compile(r'\bTODO\b|\bTBD\b|\bFIXME\b|lorem ipsum|\[\.\.\.\]|\{\{|^\s*(\.\.\.|…)\s*$', re.I)
ID_RE = re.compile(r'^[a-z][a-z0-9-]*$')
VAR_RE = re.compile(r'(?<![\w-])(--[a-z][\w-]*)')
NARROW = range(320, 431)   # a phone width: 375 preferred, 390 accepted (parity audit)
WIDE = range(1280, 1921)   # a desktop width: 1440 preferred


class Report:
    def __init__(self):
        self.items = []

    def err(self, code, where, msg):
        self.items.append(dict(severity='ERROR', code=code, where=where, message=msg))

    def warn(self, code, where, msg):
        self.items.append(dict(severity='WARN', code=code, where=where, message=msg))

    @property
    def errors(self):
        return [i for i in self.items if i['severity'] == 'ERROR']


def load_spec(path):
    text = path.read_text(encoding='utf-8')
    if path.suffix.lower() == '.json':
        return json.loads(text)
    try:
        import yaml
    except ImportError:
        raise SystemExit('spec-check: PyYAML is not installed; pip install pyyaml, or save the spec as .json')
    return yaml.safe_load(text)


class Acss:
    """ACSS 4.0.1 names (present) and site classes, from the acss-expert index and an optional etch_styles export."""

    def __init__(self, index, site_styles=None, extra_classes=()):
        d = json.load(open(index))['entries']
        self.present = {e['name'] for e in d if e['status'] == 'present'}
        self.absent = [(re.compile(e['pattern']), e) for e in d if e['kind'] == 'absent']
        self.site = set(extra_classes)
        if site_styles:
            for v in json.load(open(site_styles)).values():
                self.site |= set(re.findall(r'\.([A-Za-z_][\w-]*)', v.get('selector', '')))

    def var_problem(self, v):
        if v in self.present:
            return None
        for rx, e in self.absent:
            if rx.match(v):
                return f'{v} is not in ACSS 4.0.1; use: {e["replacement"]}'
        return f'{v} is not an ACSS 4.0.1 variable'

    def class_problem(self, c):
        c = c.lstrip('.')
        if '.' + c in self.present or c in self.site:
            return None
        for rx, e in self.absent:
            if rx.match('.' + c):
                return f'.{c} is not in ACSS 4.0.1; use: {e["replacement"]}'
        return f'.{c} is neither an ACSS 4.0.1 class nor a listed site class (site_classes / --site-styles)'

    def token_problem(self, t):
        t = str(t).strip()
        if t.startswith('var('):
            t = t[4:].rstrip(')').strip()
        return self.var_problem(t) if t.startswith('--') else self.class_problem(t)


def find_index(arg):
    if arg:
        return pathlib.Path(arg)
    for p in (SKILLS / 'acss-expert/index/acss-index.json', HERE.parent / 'acss-index.json'):
        if p.exists():
            return p
    return None


def walk_strings(o, where=''):
    if isinstance(o, str):
        yield where, o
    elif isinstance(o, dict):
        for k, v in o.items():
            yield from walk_strings(v, f'{where}.{k}' if where else str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk_strings(v, f'{where}[{i}]')


def nonempty(v):
    return v is not None and v != '' and v != [] and v != {}


def check(spec, root, acss, r):
    if not isinstance(spec, dict):
        r.err('E_FORMAT', '', 'spec must be a mapping'); return

    # 0. placeholders anywhere: the builder never fills gaps by taste
    for where, s in walk_strings(spec):
        if PLACEHOLDER.search(s):
            r.err('E_PLACEHOLDER', where, f'placeholder left in the spec: "{s[:80]}"')

    # 1. page
    page = spec.get('page') or {}
    for k in ('title', 'slug', 'status', 'template'):
        if not nonempty(page.get(k)):
            r.err('E_MISSING', f'page.{k}', 'required')
    if page.get('status') not in (None, 'draft'):
        r.err('E_STATUS', 'page.status', 'builds are drafts; publishing is a separate step on Alex\'s word')
    if page.get('slug') and not re.fullmatch(r'[a-z0-9][a-z0-9-]*', str(page['slug'])):
        r.err('E_FORMAT', 'page.slug', 'lowercase letters, digits and dashes only')
    if not nonempty(spec.get('site_profile')):
        r.err('E_MISSING', 'site_profile', 'required (host, IDs, brand rules)')

    # 2. references: what "exactly" means
    refs = spec.get('references') or {}
    if not nonempty(refs.get('source')):
        r.err('E_MISSING', 'references.source', 'one source of truth for the design (mockup file, Figma link or PNG)')
    elif not re.match(r'https?://', str(refs['source'])) and not (root / str(refs['source']).split('#')[0]).exists():
        r.err('E_FILE', 'references.source', f'not found: {refs["source"]} (relative to {root})')
    shots = refs.get('shots') or {}
    check_shots(shots, 'references.shots', root, r, required=True)

    # 3. tokens: brand names -> ACSS names
    tokens = spec.get('tokens') or {}
    surfaces = tokens.get('surfaces') or {}
    if not surfaces:
        r.err('E_MISSING', 'tokens.surfaces', 'map every surface name used by sections to an ACSS variable or class')
    if surfaces and 'paper' not in surfaces:
        r.err('E_MISSING', 'tokens.surfaces.paper', 'the default surface must be named "paper"')
    if acss:
        for group, m in tokens.items():
            if isinstance(m, dict):
                for name, val in m.items():
                    p = acss.token_problem(val)
                    if p:
                        r.err('E_TOKEN', f'tokens.{group}.{name}', p)

    # 4. sections
    sections = spec.get('sections') or []
    if not sections:
        r.err('E_MISSING', 'sections', 'at least one section'); return
    ids, flow = {}, []
    for i, s in enumerate(sections):
        w = f'sections[{i}]'
        if not isinstance(s, dict):
            r.err('E_FORMAT', w, 'section must be a mapping'); continue
        sid = s.get('id')
        if not sid or not ID_RE.match(str(sid)):
            r.err('E_ID', f'{w}.id', 'required, lowercase kebab-case (becomes data-section and the heading id)')
        elif sid in ids:
            r.err('E_ID', f'{w}.id', f'duplicate id "{sid}" (also {ids[sid]})')
        else:
            ids[sid] = w
        w = f'sections[{sid or i}]'
        check_section(s, w, surfaces, root, acss, r)
        if s.get('landmark') != 'dialog':
            flow.append((w, s))

    scope = spec.get('scope')
    if scope is not None:
        for sid in scope if isinstance(scope, list) else [scope]:
            if sid not in ids:
                r.err('E_SCOPE', 'scope', f'"{sid}" is not a section id in this spec')

    check_headings(sections, r)
    check_surfaces(flow, r)
    check_dialogs(sections, ids, r)
    check_eager(sections, r)


def check_shots(shots, where, root, r, required):
    if not isinstance(shots, dict) or not shots:
        if required:
            r.err('E_SHOTS', where, 'reference screenshots are required at a phone width (375) and a desktop width (1440)')
        return
    widths = []
    for k, path in shots.items():
        try:
            widths.append(int(k))
        except (TypeError, ValueError):
            r.err('E_SHOTS', f'{where}.{k}', 'keys are viewport widths in px (375, 1440)'); continue
        if not nonempty(path):
            r.err('E_SHOTS', f'{where}.{k}', 'no file given')
        elif re.match(r'https?://', str(path)):
            r.err('E_SHOTS', f'{where}.{k}', 'store the screenshot with the spec; a URL can change after sign-off')
        elif not PLACEHOLDER.search(str(path)) and not (root / str(path)).exists():
            r.err('E_FILE', f'{where}.{k}', f'not found: {path} (relative to {root})')
    if required:
        if not any(x in NARROW for x in widths):
            r.err('E_SHOTS', where, 'missing a phone-width shot (375; 320-430 accepted)')
        if not any(x in WIDE for x in widths):
            r.err('E_SHOTS', where, 'missing a desktop-width shot (1440; 1280-1920 accepted)')


def check_section(s, w, surfaces, root, acss, r):
    role, lm = s.get('role'), s.get('landmark')
    if role not in ROLES:
        r.err('E_ROLE', f'{w}.role', f'one of: {", ".join(sorted(ROLES))}')
    if lm not in LANDMARKS:
        r.err('E_LANDMARK', f'{w}.landmark', f'one of: {", ".join(sorted(LANDMARKS))}')
    h = s.get('heading')
    if lm in NEEDS_HEADING and not h:
        r.err('E_HEADING', f'{w}.heading', f'a <{lm}> starts with a heading (docs:/elements/section); with no heading use landmark: div')
    if h:
        if not isinstance(h, dict) or h.get('level') not in (1, 2, 3, 4, 5, 6) or not nonempty(h.get('text')):
            r.err('E_HEADING', f'{w}.heading', 'needs level (1-6) and verbatim text')
        elif h.get('highlight') and str(h['highlight']) not in str(h['text']):
            r.err('E_HEADING', f'{w}.heading.highlight', 'highlight must be a part of the heading text')

    content = s.get('content')
    comp = s.get('component')
    if not content and not comp:
        r.err('E_MISSING', f'{w}.content', 'verbatim copy in order (or a component with its props)')
    for j, it in enumerate(content or []):
        check_item(it, f'{w}.content[{j}]', acss, r)

    lay = s.get('layout') or {}
    for k in ('pattern', 'wide', 'narrow'):
        if not nonempty(lay.get(k)):
            r.err('E_LAYOUT', f'{w}.layout.{k}', 'required (pattern name or "new"; wide and narrow arrangement in words)')

    surf = s.get('surface')
    if not surf:
        r.err('E_SURFACE', f'{w}.surface', 'required (a name from tokens.surfaces)')
    elif surfaces and surf not in surfaces:
        r.err('E_SURFACE', f'{w}.surface', f'"{surf}" is not in tokens.surfaces')

    for j, m in enumerate(s.get('media') or []):
        check_media(m, f'{w}.media[{j}]', r)

    if comp:
        check_component(comp, f'{w}.component', r)

    loop = (s.get('data') or {}).get('loop')
    if loop:
        check_loop(loop, f'{w}.data.loop', set(), r)

    resp = s.get('responsive')
    if not resp or not isinstance(resp, list):
        r.err('E_RESPONSIVE', f'{w}.responsive', 'list what changes and at what container width (or "intrinsic only")')
    else:
        for j, line in enumerate(resp):
            if re.search(r'\b(breakpoints?|tablet|desktop|mobile)\b', str(line), re.I) and not re.search(r'container|\d+\s*(px|rem|em|ch)', str(line)):
                r.warn('W_BREAKPOINT', f'{w}.responsive[{j}]', 'state the width the content needs, not a device or site breakpoint (docs:/responsive-development/philosophy)')

    mm = s.get('must_match')
    if not mm:
        r.err('E_MUST_MATCH', f'{w}.must_match', f'fidelity strictness: some of {", ".join(sorted(MUST_MATCH))}')
    else:
        for x in mm:
            if x not in MUST_MATCH:
                r.err('E_MUST_MATCH', f'{w}.must_match', f'unknown check "{x}"')

    mo = s.get('motion')
    if mo and not (isinstance(mo, dict) and nonempty(mo.get('ref')) and 'reduced_motion' in mo):
        r.err('E_MOTION', f'{w}.motion', 'needs ref (art-director/reference/site-motion.md#...) and reduced_motion')

    if s.get('shots'):
        check_shots(s['shots'], f'{w}.shots', root, r, required=False)

    if acss:  # ACSS variables named in layout/responsive/states
        for where, txt in walk_strings({k: s.get(k) for k in ('layout', 'responsive', 'states', 'tokens')}, w):
            for v in VAR_RE.findall(txt):
                p = acss.var_problem(v)
                if p:
                    r.err('E_TOKEN', where, p)


def check_item(it, w, acss, r):
    if not isinstance(it, dict) or it.get('type') not in CONTENT_TYPES:
        r.err('E_CONTENT', w, f'each item needs type: {", ".join(sorted(CONTENT_TYPES))}'); return
    t = it['type']
    if t == 'list':
        items = it.get('items')
        if not items or not all(isinstance(x, (str, dict)) and x for x in items):
            r.err('E_CONTENT', f'{w}.items', 'a list needs its verbatim items')
    elif t == 'embed':
        if not nonempty(it.get('source')):
            r.err('E_CONTENT', f'{w}.source', 'embed keeps an existing interactive block verbatim: name the post/page and block')
    elif not nonempty(it.get('text')):
        r.err('E_CONTENT', f'{w}.text', 'verbatim copy required')
    if t == 'link':
        if not nonempty(it.get('href')):
            r.err('E_LINK', f'{w}.href', 'a link navigates: href required (on-page actions are buttons, docs:/elements/anchor)')
        if it.get('action'):
            r.err('E_LINK', f'{w}.action', 'a link with an on-page action must be a button (docs:/elements/anchor)')
    if t == 'button':
        if it.get('href'):
            r.err('E_BUTTON', f'{w}.href', 'a button does not navigate; use type: link (docs:/elements/anchor)')
        if not nonempty(it.get('action')):
            r.err('E_BUTTON', f'{w}.action', 'say what the button does on the page (e.g. "open dialog solutions-voting")')
    if t in ('link', 'button'):
        st = it.get('style')
        if not nonempty(st):
            r.err('E_STYLE', f'{w}.style', 'button role required: the classes that style it (e.g. btn--secondary), "text" for a plain text link, or "nested" when the parent class styles it')
        elif acss and st not in ('text', 'nested'):
            for c in str(st).split():
                p = acss.class_problem(c)
                if p:
                    r.err('E_STYLE', f'{w}.style', p)


def check_media(m, w, r):
    if not isinstance(m, dict):
        r.err('E_MEDIA', w, 'media must be a mapping'); return
    mid = m.get('media_id')
    if not isinstance(mid, int) or isinstance(mid, bool) or mid <= 0:
        r.err('E_MEDIA', f'{w}.media_id', 'WordPress media ID (integer); never a URL (docs:/elements/dynamic-image)')
    if m.get('url') or m.get('src'):
        r.err('E_MEDIA', w, 'no image URLs: the builder uses Dynamic Image by media ID')
    alt, deco = m.get('alt'), m.get('decorative') is True
    if deco and alt not in (None, ''):
        r.err('E_ALT', f'{w}.alt', 'decorative images have empty alt')
    if not deco and not nonempty(alt):
        r.err('E_ALT', f'{w}.alt', 'alt text, "library" (use the media library alt), or decorative: true')
    if m.get('loading') not in LOADING:
        r.err('E_MEDIA', f'{w}.loading', 'eager (above the fold only) or lazy')
    if not nonempty(m.get('ratio')):
        r.err('E_MEDIA', f'{w}.ratio', 'aspect ratio the box keeps, e.g. "4/3" or "intrinsic"')
    if m.get('fit') is not None and m.get('fit') not in FIT:
        r.err('E_MEDIA', f'{w}.fit', f'one of {", ".join(sorted(FIT))}')


def check_component(c, w, r):
    if not isinstance(c, dict):
        r.err('E_COMPONENT', w, 'component must be a mapping'); return
    if c.get('use') == 'existing':
        if not isinstance(c.get('ref'), int):
            r.err('E_COMPONENT', f'{w}.ref', 'existing component: the wp_block post ID (integer)')
        if not isinstance(c.get('props'), dict):
            r.err('E_COMPONENT', f'{w}.props', 'prop values the instance sets (mapping); the schema is closed, undeclared props are rejected')
    elif c.get('new'):
        if not isinstance(c.get('props'), list):
            r.err('E_COMPONENT', f'{w}.props', 'new component: list its props (name, type)')
        if 'slots' not in c:
            r.err('E_COMPONENT', f'{w}.slots', 'new component: list its slots ([] for none)')
    else:
        r.err('E_COMPONENT', w, 'either {use: existing, ref, props} or {new: Name, props: [...], slots: [...]}')


def check_loop(loop, w, outer_items, r):
    if not isinstance(loop, dict):
        r.err('E_LOOP', w, 'loop must be a mapping'); return
    for k in ('key', 'source', 'item'):
        if not nonempty(loop.get(k)):
            r.err('E_LOOP', f'{w}.{k}', 'required (loop name, data source, item name)')
    item = loop.get('item')
    if item and item in outer_items:
        r.err('E_LOOP', f'{w}.item', f'"{item}" is already the outer loop\'s item: a same-name inner loop hides the outer (docs:/loops/nested-loops)')
    if loop.get('inner'):
        check_loop(loop['inner'], f'{w}.inner', outer_items | {item}, r)


def headings_of(s):
    out = []
    h = s.get('heading')
    if isinstance(h, dict) and h.get('level') in (1, 2, 3, 4, 5, 6):
        out.append(h['level'])
    for it in s.get('content') or []:
        if isinstance(it, dict) and re.fullmatch(r'h[2-6]', str(it.get('type'))):
            out.append(int(it['type'][1]))
    return out


def check_headings(sections, r):
    page = [s for s in sections if isinstance(s, dict) and s.get('landmark') != 'dialog']
    levels = [(s.get('id'), lv) for s in page for lv in headings_of(s)]
    h1 = [sid for sid, lv in levels if lv == 1]
    if len(h1) != 1:
        r.err('E_H1', 'sections', f'exactly one h1 per page, found {len(h1)}' + (f' ({", ".join(map(str, h1))})' if h1 else ''))
    first = next((s for s in page if headings_of(s)), None)
    if first and headings_of(first)[0] != 1:
        r.err('E_H1', f'sections[{first.get("id")}].heading', 'the first section carries the h1 (docs:/elements/section)')
    prev = 0
    for sid, lv in levels:
        if prev and lv > prev + 1:
            r.err('E_HEADING_ORDER', f'sections[{sid}]', f'h{lv} after h{prev} skips a level')
        prev = lv
    for s in sections:  # dialogs: own outline, start at h2
        if isinstance(s, dict) and s.get('landmark') == 'dialog':
            lv = headings_of(s)
            if lv and lv[0] == 1:
                r.err('E_H1', f'sections[{s.get("id")}].heading', 'a dialog heading is h2, the page keeps its one h1')


def check_surfaces(flow, r):
    for (w1, a), (w2, b) in zip(flow, flow[1:]):
        if a.get('surface') and a.get('surface') == b.get('surface') and a.get('surface') != 'paper':
            r.err('E_SURFACE_NEIGHBOR', w2, f'neighbours never share a non-paper surface ("{a["surface"]}" after {w1}); separate sections by a surface change')


def check_dialogs(sections, ids, r):
    actions = ' '.join(str(it.get('action', '')) for s in sections if isinstance(s, dict)
                       for it in (s.get('content') or []) if isinstance(it, dict))
    for s in sections:
        if isinstance(s, dict) and s.get('landmark') == 'dialog' and s.get('id'):
            if not re.search(r'\b' + re.escape(s['id']) + r'\b', actions):
                r.err('E_DIALOG', f'sections[{s["id"]}]', 'no button opens this dialog (action: "open dialog <id>")')
            if not any(isinstance(it, dict) and it.get('type') == 'button' and re.search(r'\bclose\b', str(it.get('action', '')), re.I)
                       for it in s.get('content') or []):
                r.err('E_DIALOG', f'sections[{s["id"]}]', 'a dialog needs a close button in its content (type: button, action: close)')


def check_eager(sections, r):
    eager = [(s.get('id'), j) for i, s in enumerate(sections) if isinstance(s, dict)
             for j, m in enumerate(s.get('media') or []) if isinstance(m, dict) and m.get('loading') == 'eager']
    if len(eager) > 1:
        r.warn('W_EAGER', 'sections', f'{len(eager)} eager images; only the above-the-fold image loads eager (docs:/elements/image)')
    for sid, _ in eager:
        if sections and isinstance(sections[0], dict) and sid != sections[0].get('id'):
            r.warn('W_EAGER', f'sections[{sid}]', 'eager image below the first section')


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('spec')
    ap.add_argument('--root', help='folder that reference and shot paths are relative to (default: the spec folder)')
    ap.add_argument('--acss-index')
    ap.add_argument('--site-styles', help='etch_styles export (snapshot option-etch_styles.json or fixtures/styles-used.json)')
    ap.add_argument('--no-acss', action='store_true', help='skip ACSS name checks (prints a warning; never for a real build)')
    ap.add_argument('--json', action='store_true')
    a = ap.parse_args(argv)
    path = pathlib.Path(a.spec)
    try:
        spec = load_spec(path)
    except (OSError, ValueError) as e:
        print(f'spec-check: cannot read {path}: {e}', file=sys.stderr); return 2
    root = pathlib.Path(a.root) if a.root else path.resolve().parent
    r = Report()
    acss = None
    if a.no_acss:
        r.warn('W_NO_ACSS', '', 'ACSS names not checked (--no-acss)')
    else:
        idx = find_index(a.acss_index)
        if not idx or not idx.exists():
            r.err('E_NO_ACSS', '', 'acss-expert/index/acss-index.json not found; pass --acss-index')
        else:
            site_styles = a.site_styles or (spec.get('site_styles') if isinstance(spec, dict) else None)
            if site_styles and not pathlib.Path(site_styles).is_absolute():
                site_styles = str((pathlib.Path(a.site_styles) if a.site_styles else path.resolve().parent / site_styles))
            extra = (spec.get('site_classes') or []) if isinstance(spec, dict) else []
            acss = Acss(idx, site_styles, extra)
    check(spec, root, acss, r)
    if a.json:
        print(json.dumps(dict(errors=len(r.errors), items=r.items), indent=1, ensure_ascii=False))
    else:
        for i in r.items:
            print(f"{i['severity']:5} {i['code']:20} {i['where']}: {i['message']}")
        n = len(r.errors)
        print(f'{path.name}: {n} error(s), {len(r.items) - n} warning(s). ' + ('Do not build: fix the spec or ask art-director for the missing data.' if n else 'OK to build.'))
    return 1 if r.errors else 0


if __name__ == '__main__':
    sys.exit(main())
