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


class Aligned:
    """The same design in another language (the ES/PT EB-5 files mirror the EN one): q(en_prefix) finds the EN string, as
    Copy does, and returns the target design's string at the same position. `extra` lists the target's own strings (by
    position in the target) that have no EN counterpart; they are read with .extra(i). Fails when the two designs stop
    lining up (different counts) or when one EN string maps to different target strings."""
    def __init__(self, en: Copy, path, start='<main', end='</main>', extra=()):
        target = texts(path, start, end)
        self.extras = [target[i] for i in extra]
        self.target = [t for i, t in enumerate(target) if i not in set(extra)]
        self.en = en
        if len(self.target) != len(en.all):
            raise ValueError(f'{path}: {len(self.target)} strings vs {len(en.all)} in EN (after {len(self.extras)} extra)')
        self.all = target  # what the copy gate checks the page against

    def __call__(self, en_prefix: str) -> str:
        s = self.en(en_prefix)
        hits = {self.target[i] for i, t in enumerate(self.en.all) if t == s}
        if len(hits) != 1:
            raise KeyError(f'{en_prefix!r}: maps to {len(hits)} strings {sorted(hits)[:3]}')
        return hits.pop()

    def extra(self, i: int) -> str:
        return self.extras[i]
