"""Tiny builder for Etch block markup, in the exact shape of the saved fixtures
(.claude/skills/etch-expert/reference/fixtures, catalogue.md):
  <!-- wp:etch/element {"metadata":{"name":..},"tag":..,"attributes":{..},"styles":[..]} --> ... <!-- /wp:etch/element -->
  <!-- wp:etch/text {"metadata":{"name":"Text"},"content":".."} /-->
  <!-- wp:etch/dynamic-image {"metadata":{"name":..},"tag":"img","attributes":{"mediaId":..,"useSrcSet":"true","loading":..,"alt":..}} /-->
Classes carry style-record IDs (the builder adds them on save otherwise; PILOT.md drift #1). Record IDs are
site-specific (ACSS utilities get empty-CSS records too), so the markup holds placeholders resolved at deploy time:
  {{style:.<class>}}  -> id of the etch_styles record with that selector (created first if missing)
  {{media:<slug>}}    -> WordPress attachment ID
  {{mediaurl:<slug>}} -> its URL on the site (video src / poster, which take a URL, not an id)"""
import base64, hashlib, json, re

BUILTIN_STYLES = {'section': 'etch-section-style', 'container': 'etch-container-style'}


def style_id(selector: str) -> str:
    """Deterministic 7-char id for a NEW style record (same shape as Etch's ids, e.g. 'lbdxk83')."""
    h = hashlib.sha1(('dealdirect:' + selector).encode()).hexdigest()
    alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'
    n = int(h, 16)
    out = ''
    for _ in range(7):
        n, r = divmod(n, 36)
        out += alphabet[r]
    return out if out[0].isalpha() else 'd' + out[1:]


def _json(d) -> str:
    # Etch stores -- , < , > , & , " escaped inside block JSON (catalogue.md "Class escape", "Entities").
    s = json.dumps(d, ensure_ascii=False, separators=(',', ':'))
    return (s.replace('--', '\\u002d\\u002d').replace('<', '\\u003c').replace('>', '\\u003e')
             .replace('&', '\\u0026'))


class Node:
    def render(self) -> str: raise NotImplementedError
    def texts(self): return []
    def classes(self): return []


class Text(Node):
    def __init__(self, content: str):
        self.content = content
    def render(self):
        return '<!-- wp:etch/text ' + _json({'metadata': {'name': 'Text'}, 'content': self.content}) + ' /-->'
    def texts(self):
        return [self.content]


class El(Node):
    def __init__(self, tag, name, cls=None, attrs=None, children=(), etch=None, script=None):
        self.tag, self.name, self.cls, self.attrs, self.etch, self.script = tag, name, cls, dict(attrs or {}), etch, script
        self.children = [Text(c) if isinstance(c, str) else c for c in children if c is not None]

    def render(self):
        attrs = {}
        if self.etch:
            attrs['data-etch-element'] = self.etch
        attrs.update(self.attrs)
        styles = []
        if self.etch in BUILTIN_STYLES:
            styles.append(BUILTIN_STYLES[self.etch])
        if self.cls:
            attrs['class'] = self.cls
            styles += ['{{style:.%s}}' % c for c in self.cls.split()]
        d = {'metadata': {'name': self.name}, 'tag': self.tag, 'attributes': attrs or []}
        if styles:
            d['styles'] = styles
        if self.script:
            # stored base64 with a 7-char id (catalogue.md "Scripts"); enqueued in <head> as a deferred module
            d['script'] = {'code': base64.b64encode(self.script.encode()).decode(), 'id': style_id('script:' + self.name)}
        inner = '\n'.join(c.render() for c in self.children)
        return '<!-- wp:etch/element ' + _json(d) + ' -->\n' + (inner + '\n' if inner else '') + '<!-- /wp:etch/element -->'

    def texts(self):
        return [t for c in self.children for t in c.texts()]

    def classes(self):
        own = self.cls.split() if self.cls else []
        return own + [x for c in self.children for x in c.classes()]


class Img(Node):
    """Dynamic image by media id. No class: no fixture shows one on this block, so images are styled from their
    parent (`& img`). Stored as an open/close pair like the fixtures."""
    def __init__(self, name, media, alt, loading='lazy'):
        self.name, self.media, self.alt, self.loading = name, media, alt, loading

    def render(self):
        # media: a slug from the page's MEDIA, or a dynamic expression such as "{item.meta.card_image}"
        mid = self.media if self.media.startswith('{') else '{{media:%s}}' % self.media
        attrs = {'mediaId': mid, 'useSrcSet': 'true', 'loading': self.loading, 'alt': self.alt}
        d = {'metadata': {'name': self.name}, 'tag': 'img', 'attributes': attrs}
        return '<!-- wp:etch/dynamic-image ' + _json(d) + ' -->\n\n<!-- /wp:etch/dynamic-image -->'


class Loop(Node):
    """Etch loop (fixtures/pages/work.html): `loop_id` is the key of its record in the etch_loops option (the page's
    LOOPS, upserted by the deploy); children render once per item, reading `{<item>.field}` expressions."""
    def __init__(self, name, loop_id, item, children):
        self.name, self.loop_id, self.item = name, loop_id, item
        self.children = [Text(c) if isinstance(c, str) else c for c in children]

    def render(self):
        d = {'metadata': {'name': self.name}, 'loopId': self.loop_id, 'itemId': self.item}
        inner = '\n'.join(c.render() for c in self.children)
        return '<!-- wp:etch/loop ' + _json(d) + ' -->\n' + inner + '\n<!-- /wp:etch/loop -->'

    def texts(self):
        return [t for c in self.children for t in c.texts()]

    def classes(self):
        return [x for c in self.children for x in c.classes()]


class Component(Node):
    """Instance of an Etch component (wp_block). ref is a placeholder {{ref:<slug>}} -> numeric post id at deploy."""
    def __init__(self, name, slug, props=None):
        self.name, self.slug, self.props = name, slug, props or []

    def render(self):
        d = {'metadata': {'name': self.name}, 'ref': '{{ref:%s}}' % self.slug, 'attributes': self.props}
        return '<!-- wp:etch/component ' + _json(d) + ' -->\n\n<!-- /wp:etch/component -->'


class Svg(Node):
    """Inline SVG fetched at build/deploy time (WordPress refuses SVG uploads by default). Renders a marker that
    svg.expand() replaces with svg/g/path elements, the form fixtures/parts/footer.html stores."""
    def __init__(self, name, url, label, cls=None):
        self.name, self.url, self.label, self.cls = name, url, label, cls

    def render(self):
        return '<!-- dd:svg ' + _json({'name': self.name, 'url': self.url, 'label': self.label, 'cls': self.cls}) + ' -->'

    def classes(self):
        return self.cls.split() if self.cls else []


def section(name, cls, heading_id, children, attrs=None, tag='section'):
    """Section > Container skeleton (guardrails §2), labelled by its heading. A band without a heading is a div."""
    a = {'aria-labelledby': heading_id} if heading_id else {}
    a.update(attrs or {})
    block = cls.split()[0]  # 'cta-band cta-band--cover' -> container 'cta-band__inner'
    return El(tag, name, cls, a, [El('div', 'Container', block + '__inner', etch='container', children=children)], etch='section')


def page(nodes) -> str:
    return '\n\n'.join(n.render() for n in nodes) + '\n'


def all_texts(nodes):
    return [t for n in nodes for t in n.texts()]


def all_classes(nodes):
    seen = []
    for n in nodes:
        for c in n.classes():
            if c not in seen:
                seen.append(c)
    return seen


_PLACEHOLDER = re.compile(r'\{\{(style|media|mediaurl):([^}]*)\}\}')
_REF = re.compile(r'"\{\{ref:([^}]*)\}\}"')


def resolve(markup: str, sel2id: dict, media2id: dict, ref2id: dict = None, media2url: dict = None) -> str:
    """Swap {{style:.x}} / {{media:slug}} / {{mediaurl:slug}} for real values. Raises on anything unresolved, so nothing
    half-built is written."""
    missing = []

    def sub(m):
        kind, key = m.group(1), m.group(2).replace('\\u002d', '-')
        table = {'style': sel2id, 'media': media2id, 'mediaurl': media2url or {}}[kind]
        if key not in table:
            missing.append(f'{kind}:{key}')
            return m.group(0)
        return str(table[key])

    out = _PLACEHOLDER.sub(sub, markup)

    def ref(m):  # component refs are JSON numbers in saved markup ("ref":143)
        if m.group(1) not in (ref2id or {}):
            missing.append('ref:' + m.group(1))
            return m.group(0)
        return str(int(ref2id[m.group(1)]))

    out = _REF.sub(ref, out)
    if missing:
        raise KeyError('unresolved: ' + ', '.join(sorted(set(missing))))
    return out
