#!/usr/bin/env python3
"""Verify ACSS names in CSS, Etch block markup or JSON before saving. Stdlib only. Blocking: exit 1 on any ERROR.

CLI   python3 -I scripts/verify.py [--index index/acss-index.json] [--site-styles etch_styles.json]
                                   [--site-css global.css ...] [--classes a b c] [--json] FILE...
Lib   import importlib.util; spec = importlib.util.spec_from_file_location('acss_verify', '<skill>/scripts/verify.py')
      v = Verifier.load(); v.known_class('btn--primary'); v.check_classes([...]); v.check_css(text); v.check_text(text)
Rules (lookup order: present first, then absent; docs: whats-new-in-4, "Changes From 3.x" pages)
 ERROR  absent 3.x/removed name (class, var, recipe, in CSS or class attributes); unknown ACSS-shaped class or var
        (not in the build, not defined in the input or site CSS/styles); unknown ?recipe; a new stylesheet
        (<style>, <link rel=stylesheet>, @import, @font-face file); 3.x @-recipes (@btn; @include ...)
 WARN   hard-coded value that equals an ACSS token (palette hex, fixed spacing/radius); 3.x functions fluid()/ctr()
Custom site classes: with --site-styles, one in neither it nor the build is a WARN (unstyled hook or typo), ERROR with --strict-site.
"""
import argparse, json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
# ACSS utilities are BEM-modifier shaped (prefix--x): an unknown one is almost certainly a wrong/3.x name
ACSS_SHAPED = re.compile(r'^(btn|bg|text|section|header|width|grid|gap|pad|margin|col|order|align|justify|flex|content|icon|'
                         r'link|marker|border|divider|box-shadow|on-(?:visible|enter|exit|hover)|overlay|surface|fade|masonry|'
                         r'scheme|focus|sticky|breakout|container|z)--')
LENGTH_PROPS = r'(?:padding|margin|gap|row-gap|column-gap|inset|top|right|bottom|left|border-radius|font-size|max-inline-size|max-width)[\w-]*'

class Verifier:
    def __init__(self, entries, site_classes=None, site_vars=None, tokens=None):
        self.present = {e['name'] for e in entries if e['status'] == 'present'}
        self.recipes = {e['name'] for e in entries if e['kind'] == 'recipe'}
        self.absent = [(re.compile(e['pattern']), e) for e in entries if e['kind'] == 'absent']
        self.site_classes, self.site_vars = site_classes, set(site_vars or ())
        self.tokens = tokens or {}  # normalized literal value -> token name (fixed values only)
        self.strict_site = False   # True: classes unknown to etch_styles are ERRORs, not WARNs

    @classmethod
    def load(cls, index=None, site_styles=None, site_css=(), settings=None):
        d = json.load(open(index or ROOT / 'index/acss-index.json'))
        sc, sv = None, set()
        if site_styles:
            sc = set()
            for v in json.load(open(site_styles)).values():
                sc |= set(re.findall(r'\.([A-Za-z_][\w-]*)', v.get('selector', '')))
                sv |= set(re.findall(r'(--[\w-]+)\s*:', v.get('css', '')))  # custom props set by other site styles
                sc |= set(re.findall(r'\.([A-Za-z_][\w-]*)', re.sub(r'/\*.*?\*/|"[^"]*"', '', v.get('css', ''), flags=re.S)))  # classes styled via nested selectors
        for f in site_css:
            t = open(f).read(); sv |= set(re.findall(r'(--[\w-]+)\s*:', t))
            if sc is not None: sc |= set(re.findall(r'\.([A-Za-z_][\w-]*)', t))
        return cls(d['entries'], sc, sv, cls._tokens(settings))

    @staticmethod
    def _tokens(settings):
        """Fixed values worth flagging, from the saved stylesheet: palette hex/oklch and constant clamps."""
        css = pathlib.Path(settings or ROOT / 'index/automatic.css')
        if not css.exists(): return {}
        out = {}
        st = css.parent / 'acss-settings.json'
        if st.exists():  # brand hex entered in the dashboard -> its palette token
            for k, hx in json.load(open(st)).items():
                if re.fullmatch(r'color-(primary|secondary|tertiary|accent|base|neutral)', k) and re.fullmatch(r'#[0-9A-Fa-f]{6}', str(hx)):
                    out[hx.lower()] = '--' + k[6:]
        for n, v in re.findall(r'^\s*(--[\w-]+):\s*([^;]+);', css.read_text(), re.M):
            v = v.strip().lower()
            m = re.fullmatch(r'clamp\(([\d.]+)rem,[^,]*,\s*([\d.]+)rem\)', v)
            if m and abs(float(m[1]) - float(m[2])) < 1e-6:  # constant clamp = fixed value
                px = round(float(m[1]) * 16, 2); v = f'{px:g}px'
            if re.fullmatch(r'(#[0-9a-f]{6}|\d+(\.\d+)?px)', v) and v not in out and v not in ('0px', '1px', '2px', '3px', '4px') and n.count('-') <= 3:
                out.setdefault(v, n)
        return out

    # --- name lookups: present first, then absent
    def _absent(self, name):
        for rx, e in self.absent:
            if rx.match(name): return e
        return None

    def known_class(self, c):
        return c in self.present or (self.site_classes is not None and c in self.site_classes)

    def classify_class(self, c, local=()):
        """None if fine, else (severity, message)."""
        n = '.' + c
        if n in self.present or c in local: return None
        if self.site_classes is not None and c in self.site_classes: return None
        e = self._absent(n)
        if e: return ('ERROR', f'{n} is not in ACSS 4.0.1 (removed/3.x); use: {e["replacement"]}')
        if ACSS_SHAPED.match(c): return ('ERROR', f'{n} looks like an ACSS name but is not in the build (module off or wrong name); see staging-4.0.1-facts.md')
        if self.site_classes is not None: return ('ERROR' if self.strict_site else 'WARN', f'{n} is neither an ACSS class nor in etch_styles (unstyled hook or typo)')
        return None

    def classify_var(self, v, local=()):
        if v in self.present or v in local or v in self.site_vars or v.startswith('--wp-'): return None  # --wp-*: WordPress core
        e = self._absent(v)
        if e: return ('ERROR', f'var({v}) is not in ACSS 4.0.1; use: {e["replacement"]}')
        return ('ERROR', f'var({v}) is not an ACSS variable in the build and is not defined in the input or site CSS')

    @staticmethod
    def _token_fits(prop, name):
        if prop.startswith('border') and 'radius' in prop: return name.startswith(('--radius', '--btn-radius'))
        if prop.startswith('font-size'): return name.startswith(('--text-', '--h'))
        if prop.startswith(('padding', 'margin', 'gap', 'row-gap', 'column-gap')): return name.startswith(('--space-', '--section-space-'))
        return False

    # --- checks
    def check_classes(self, classes, where=''):
        res = []
        for c in classes:
            r = self.classify_class(c)
            if r: res.append(dict(severity=r[0], where=where, message=r[1]))
        return res

    def check_css(self, css, where=''):
        res = []
        css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
        css = re.sub(r'url\([^)]*\)|"[^"]*"|\'[^\']*\'', '""', css)
        local_vars = set(re.findall(r'(--[\w-]+)\s*:', css))
        def add(sev, msg): res.append(dict(severity=sev, where=where, message=msg))
        for v in sorted(set(re.findall(r'var\(\s*(--[\w-]+)', css))):
            r = self.classify_var(v, local_vars)
            if r: add(*r)
        for sel in re.findall(r'([^{};]+)\{', css):
            if sel.strip().startswith('@'): continue
            for c in sorted(set(re.findall(r'\.([A-Za-z_][\w-]*)', sel))):
                r = self.classify_class(c, local=())
                # selector classes: only block ACSS-shaped / absent names, never site-local ones
                if r and (self._absent('.' + c) or (ACSS_SHAPED.match(c) and ('.' + c) not in self.present and c not in (self.site_classes or ()))):
                    add(*r)
        for m in sorted(set(re.findall(r'\?([a-z][a-z0-9-]*)', re.sub(r'\?[^\s;]*\)', '', css)))):
            if '?' + m not in self.recipes: add('ERROR', f'?{m} is not a documented ACSS 4 recipe')
        for m in sorted(set(re.findall(r'(?<![\w-])@(include\s+[\w-]+|[a-z][\w-]*)\s*;', css))):
            add('ERROR', f'3.x syntax "@{m};": 4.x recipes use "?name;" (docs: whats-new-in-4)')
        if re.search(r'@import\b', css): add('ERROR', '@import adds a stylesheet: not allowed (CSS stays on the element)')
        if re.search(r'@font-face\b', css): add('ERROR', '@font-face adds a global stylesheet rule: set fonts in ACSS (Typography > Fonts), not in element CSS')
        for fn in sorted(set(re.findall(r'(?<![\w-])(fluid|ctr|rem|pow|percent)\(', css))):
            if fn == 'rem' or True: add('WARN', f'{fn}() is a 3.x SCSS function (4.x signature unconfirmed); prefer clamp() with ACSS tokens')
        if re.search(r'hsl\(\s*var\(--[\w-]+-h\b', css): add('ERROR', 'hsl(var(--x-h ...)) is 3.x: 4.x palette is OKLCH; use var(--x) or color-mix(in oklch, ...)')
        for prop, val in re.findall(r'(' + LENGTH_PROPS + r')\s*:\s*([^;}]+)', css):
            for tok in re.findall(r'(?<![\w.#-])(\d+(?:\.\d+)?px)\b', val):
                name = self.tokens.get(tok)
                if name and 'var(' not in val and self._token_fits(prop, name):
                    add('WARN', f'{prop}: {tok} equals {name}; use var({name})')
        for hx in sorted(set(re.findall(r'#[0-9a-fA-F]{6}\b', css))):
            if hx.lower() in self.tokens: add('WARN', f'{hx} equals {self.tokens[hx.lower()]}; use var({self.tokens[hx.lower()]})')
        return res

    def check_text(self, text, where='', css_hint=False):
        """Etch block markup, HTML or JSON. Pulls out class lists and CSS strings."""
        res = []
        if css_hint: return self.check_css(text, where)
        t = re.sub(r'\\u002d', '-', text).replace('\\u0026', '&')
        try: obj = json.loads(text)
        except Exception: obj = None
        css_chunks, classes = [], set()
        def walk(o):
            if isinstance(o, dict):
                for k, v in o.items():
                    if k == 'css' and isinstance(v, str): css_chunks.append(v)
                    elif k in ('class', 'classes', 'className') and isinstance(v, str): classes.update(v.split())
                    else: walk(v)
            elif isinstance(o, list): [walk(i) for i in o]
        if obj is not None: walk(obj)
        else:
            classes |= {c for m in re.findall(r'class(?:Name)?=["\']([^"\']*)["\']|"class"\s*:\s*"([^"]*)"', t) for s in m for c in s.split()}
            css_chunks += re.findall(r'<style[^>]*>(.*?)</style>', t, re.S)
            css_chunks += re.findall(r'style=["\']([^"\']*)["\']', t)
        classes = {c for c in classes if not re.search(r'[{}$]', c)}  # skip Etch dynamic {props.x}
        if re.search(r'<style\b', t): res.append(dict(severity='ERROR', where=where, message='<style> block adds a stylesheet: not allowed (use element/class CSS in etch_styles)'))
        if re.search(r'<link\b[^>]*rel=["\']stylesheet', t): res.append(dict(severity='ERROR', where=where, message='<link rel=stylesheet> adds a stylesheet: not allowed'))
        res += self.check_classes(sorted(classes), where)
        for c in css_chunks: res += self.check_css(c, where)
        return res

def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('files', nargs='*'); ap.add_argument('--index'); ap.add_argument('--site-styles'); ap.add_argument('--site-css', nargs='*', default=[])
    ap.add_argument('--stylesheet', help='saved compiled ACSS (for token-match warnings)'); ap.add_argument('--classes', nargs='*', default=[]); ap.add_argument('--json', action='store_true'); ap.add_argument('--strict-site', action='store_true', help='classes unknown to --site-styles are errors')
    a = ap.parse_args()
    if not a.files and not a.classes: ap.error('give FILE... or --classes')
    v = Verifier.load(a.index, a.site_styles, a.site_css, a.stylesheet)
    v.strict_site = a.strict_site
    res = v.check_classes(a.classes, 'classes') if a.classes else []
    for f in a.files:
        p = pathlib.Path(f); txt = p.read_text()
        res += v.check_text(txt, f, css_hint=p.suffix == '.css')
    seen, out = set(), []
    for r in res:
        k = (r['severity'], r['where'], r['message'])
        if k not in seen: seen.add(k); out.append(r)
    errs = sum(r['severity'] == 'ERROR' for r in out)
    if a.json: print(json.dumps(dict(errors=errs, warnings=len(out) - errs, findings=out), indent=1))
    else:
        for r in out: print(f"{r['severity']:5} {r['where']}: {r['message']}")
        print(f'{errs} error(s), {len(out) - errs} warning(s)' + ('  BLOCKED: fix errors before saving' if errs else '  OK'))
    return 1 if errs else 0

if __name__ == '__main__':
    sys.exit(main())
