"""Verbatim copy from the handoff design files: text is looked up, never retyped (CLAUDE.md rule 1)."""
import re
from html.parser import HTMLParser


class _Texts(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'iframe'):
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'iframe'):
            self.skip -= 1

    def handle_data(self, data):
        d = norm(data)
        if not self.skip and d and '{{' not in d:
            self.out.append(d)


def norm(s: str) -> str:
    return re.sub(r'\s+', ' ', s).strip()


def texts(path: str, start='<main', end='</main>') -> list:
    src = open(path, encoding='utf-8').read()
    p = _Texts()
    p.feed(src[src.index(start):src.index(end)])
    return p.out


class Copy:
    """q('Access the path') -> the one design string starting with that prefix (error if 0 or >1 match).
    start/end bound the region read (default <main>…</main>; the footer is '<footer', '</footer>')."""
    def __init__(self, path, start='<main', end='</main>'):
        self.all = texts(path, start, end)

    def __call__(self, prefix: str) -> str:
        if prefix in self.all:  # an exact string wins over longer strings sharing the prefix
            return prefix
        hits = sorted({t for t in self.all if t.startswith(prefix)})
        if len(hits) != 1:
            raise KeyError(f'{prefix!r}: {len(hits)} matches {hits[:3]}')
        return hits[0]
