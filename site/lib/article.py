"""Verbatim blocks from a public article saved under site/sources/ (ops/sources.txt), for pages that quote it (CLAUDE.md
rule 1: lifted, never retyped). The article's own markup (paragraphs, bold, links, footnote marks, lists, tables) is
turned into Etch elements as it is, so the copy gate sees the source's strings; the page only picks the blocks and adds
classes. Inline styles are dropped; footnote marks and the endnotes' back-links (↩) link to each other on the page."""
import re
from html.parser import HTMLParser
from design import Copy
from etch import El

KEEP = {'p', 'strong', 'em', 'a', 'sup', 'ol', 'ul', 'li', 'table', 'caption', 'thead', 'tbody', 'tr', 'th', 'td', 'h3', 'br'}
VOID = {'br'}


class _Tree(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = ('root', {}, [])
        self.stack = [self.root]
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'svg', 'noscript'):
            self.skip += 1
            return
        node = (tag, dict(attrs), [])
        self.stack[-1][2].append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'svg', 'noscript'):
            self.skip -= 1
            return
        for i in range(len(self.stack) - 1, 0, -1):  # tolerate unclosed tags
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        if not self.skip and data:
            self.stack[-1][2].append(re.sub(r'\s+', ' ', data))


def _text(node):
    return node if isinstance(node, str) else ''.join(_text(c) for c in node[2])


def _walk(node):
    yield node
    if not isinstance(node, str):
        for c in node[2]:
            yield from _walk(c)


class Article:
    """Article(path, start, end): the region between the two markers. .copy is its Copy lookup (for COPY_EXTRA);
    .section(heading) the blocks of the rich-text body under that <h3>; .el(block) one block as Etch elements."""
    def __init__(self, path, start, end, fn_prefix, ref_prefix):
        src = open(path, encoding='utf-8').read()
        region = src[src.index(start):src.index(end)]
        t = _Tree()
        t.feed(region)
        self.root, self.copy, self.fn, self.ref = t.root, Copy(path, start, end), fn_prefix, ref_prefix

    def heading(self, text):
        return next(n for n in _walk(self.root) if not isinstance(n, str) and n[0] in ('h1', 'h3') and _text(n).strip() == text)

    def section(self, heading):
        """The block elements of the rich text that follows the <h3> with this exact text."""
        for n in _walk(self.root):
            if isinstance(n, str):
                continue
            kids = [c for c in n[2] if not isinstance(c, str)]
            for i, c in enumerate(kids):
                if c[0] == 'h3' and _text(c).strip() == heading and i + 1 < len(kids):
                    return [b for b in kids[i + 1][2] if not isinstance(b, str)]
        raise KeyError(heading)

    def endnotes(self):
        """{number: <li> node} of the article's numbered endnotes (li id="footnote-N")."""
        return {int(n[1]['id'].split('-')[1]): n for n in _walk(self.root)
                if not isinstance(n, str) and n[0] == 'li' and re.fullmatch(r'footnote-\d+', n[1].get('id', ''))}

    def el(self, node, cls=None, name=None, attrs=None):
        """One source node as Etch elements: text keeps its edge spaces (inline links), footnote marks become this page's
        fn-ref (id <ref_prefix>N) linking to the endnote (#<fn_prefix>N) and the endnote's ↩ links back; links keep their
        href and the source's aria-label."""
        if isinstance(node, str):
            return node if node.strip() else (' ' if node else None)
        tag, a, kids = node
        if tag == 'sup':
            n = _text(node).strip()
            link = next((k for k in kids if not isinstance(k, str) and k[0] == 'a'), None)
            label = {'aria-label': link[1]['aria-label']} if link and link[1].get('aria-label') else {}
            return El('sup', 'Footnote ref', 'fn-ref', {'id': f'{self.ref}{n}'},
                      [El('a', 'Endnote link', None, {'href': f'#{self.fn}{n}', **label}, [n])])
        if tag == 'a' and a.get('href', '').startswith('#footnote-ref'):
            n = a['href'].rsplit('-', 1)[1]
            label = {'aria-label': a['aria-label']} if a.get('aria-label') else {}
            return El('a', 'Back to reference', None, {'href': f'#{self.ref}{n}', **label}, [_text(node).strip()])
        children = [self.el(k) for k in kids]
        children = [c for c in children if c is not None]
        while children and isinstance(children[0], str) and not children[0].strip():
            children.pop(0)
        while children and isinstance(children[-1], str) and not children[-1].strip():
            children.pop()
        if tag not in KEEP:
            raise ValueError(f'unexpected <{tag}> in the source block')
        at = dict(attrs or {})
        if tag == 'a':
            at['href'] = a['href']
            if a.get('aria-label'):
                at['aria-label'] = a['aria-label']
        if tag in ('th',) and a.get('scope'):
            at['scope'] = a['scope']
        return El(tag, name or tag.capitalize(), cls, at, children)
