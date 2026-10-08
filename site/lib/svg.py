"""Expand <!-- dd:svg {...} --> markers into native Etch svg/g/path elements (fixtures/parts/footer.html form).
The SVG is fetched once and cached in build/assets/; it is sanitized: only drawing elements and presentation
attributes are kept, never scripts, styles, event handlers, external references or foreignObject."""
import json, os, re, urllib.request
import xml.etree.ElementTree as ET
from etch import El

ALLOWED = {'svg', 'g', 'path', 'rect', 'circle', 'ellipse', 'polygon', 'polyline', 'line', 'defs', 'clipPath',
           'linearGradient', 'radialGradient', 'stop', 'title'}
ATTRS = {'d', 'fill', 'fill-rule', 'clip-rule', 'stroke', 'stroke-width', 'stroke-linecap', 'stroke-linejoin',
         'stroke-miterlimit', 'opacity', 'fill-opacity', 'stroke-opacity', 'transform', 'x', 'y', 'width', 'height',
         'rx', 'ry', 'cx', 'cy', 'r', 'x1', 'y1', 'x2', 'y2', 'points', 'id', 'offset', 'stop-color', 'stop-opacity',
         'gradientUnits', 'gradientTransform', 'clip-path', 'viewBox', 'preserveAspectRatio'}
MARKER = re.compile(r'<!-- dd:svg (\{.*?\}) -->')
CACHE = os.path.join(os.path.dirname(__file__), '..', '..', 'build', 'assets')


def fetch(url: str) -> str:
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, re.sub(r'[^A-Za-z0-9._-]', '_', url.split('/')[-1]))
    if not os.path.exists(path):
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (DealDirect build)'})
        with urllib.request.urlopen(req, timeout=30) as r:
            open(path, 'wb').write(r.read())
    return open(path, encoding='utf-8').read()


def _local(tag):
    return tag.split('}', 1)[-1]


def _convert(node, name):
    tag = _local(node.tag)
    if tag not in ALLOWED:
        raise ValueError(f'unsupported SVG element <{tag}>')
    attrs = {}
    for k, v in node.attrib.items():
        k = _local(k)
        if k == 'style':  # inline style="fill:#fff" -> presentation attributes we allow
            for decl in v.split(';'):
                if ':' in decl:
                    pk, pv = (x.strip() for x in decl.split(':', 1))
                    if pk in ATTRS:
                        attrs[pk] = pv
            continue
        if k in ATTRS and not v.strip().lower().startswith(('javascript:', 'url(http', 'data:')):
            attrs[k] = v
    if tag == 'title':
        return None
    children = [c for c in (_convert(ch, 'Part') for ch in node) if c is not None]
    return El(tag, name if tag == 'svg' else tag.capitalize(), attrs=attrs, children=children)


def element(svg_text: str, name: str, label: str, cls: str = None) -> El:
    root = ET.fromstring(re.sub(r'<!DOCTYPE[^>]*>', '', svg_text))
    if _local(root.tag) != 'svg':
        raise ValueError('not an SVG document')
    if root.find('.//{*}style') is not None:
        raise ValueError('SVG uses a <style> block: convert its classes to attributes first')
    el = _convert(root, name)
    el.attrs = {k: v for k, v in el.attrs.items() if k in ('viewBox', 'preserveAspectRatio', 'width', 'height')}
    el.attrs.update({'xmlns': 'http://www.w3.org/2000/svg', 'role': 'img', 'aria-label': label})
    if 'viewBox' not in el.attrs and {'width', 'height'} <= set(el.attrs):
        el.attrs['viewBox'] = f"0 0 {el.attrs['width']} {el.attrs['height']}"
    el.attrs.pop('width', None)
    el.attrs.pop('height', None)
    el.cls = cls
    return el


def expand(markup: str, fetcher=fetch) -> str:
    def sub(m):
        spec = json.loads(m.group(1))
        return element(fetcher(spec['url']), spec['name'], spec['label'], spec.get('cls')).render()
    return MARKER.sub(sub, markup)
