"""Riverside Wharf "Market update" section (Alex, 2026-10-09), on both Riverside Wharf offering pages. Copy verbatim from
site/sources/riverside-wharf-market-update.html (Alex's text); each investment carries a footnote mark linking to its
source note (citations compiled for compliance, open in the evidence register until verified), and the section ends
with the page's own market disclaimer (CLAUDE.md rule 6)."""
import os
from article import Article, _text
from etch import El, Text, section

SOURCE = os.path.join(os.path.dirname(__file__), '..', 'sources', 'riverside-wharf-market-update.html')
src = Article(SOURCE, '<main', '</main>', 'mu-note-', 'mu-ref-')
COPY = src.copy
NOTE_LINKS = {1: [0, 1], 2: [2, 3], 3: [4], 4: [5, 6], 5: [7, 8]}  # note number -> its links (#links, in order)
NON_DESIGN = {str(n) for n in NOTE_LINKS} | {'↩'}  # the footnote marks and the notes' back-links


def _blocks():
    root = src.root
    def find(node, tag, ident):
        if isinstance(node, str):
            return None
        if node[0] == tag and node[1].get('id') == ident:
            return node
        for c in node[2]:
            hit = find(c, tag, ident)
            if hit:
                return hit
    kids = lambda n: [c for c in n[2] if not isinstance(c, str)]
    return kids(find(root, 'section', 'copy')), kids(find(root, 'ol', 'notes')), kids(find(root, 'ul', 'links'))


def build(disclaimer, media=None):
    """disclaimer: the page's market footnote paragraph (an El), shown under the source notes. media: an optional
    rendering figure beside the heading (from tablets up; above the list on phones)."""
    copy, notes, links = _blocks()
    eyebrow, title, intro, items, closing = copy
    link_els = [src.el(next(c for c in li[2] if not isinstance(c, str))) for li in links]
    rows = []
    for n, li in enumerate([c for c in items[2] if not isinstance(c, str)], 1):
        el = src.el(li, 'market-update__item', 'Investment')
        el.children.append(El('sup', 'Footnote ref', 'fn-ref', {'id': f'mu-ref-{n}'},
                              [El('a', 'Note link', None, {'href': f'#mu-note-{n}', 'aria-label': f'See footnote {n}'}, [str(n)])]))
        rows.append(el)
    note_els = []
    for n, li in enumerate(notes, 1):
        el = src.el(li, None, 'Source note', {'id': f'mu-note-{n}'})
        for i in NOTE_LINKS[n]:
            el.children += [Text(' '), link_els[i]]
        el.children += [Text(' '), El('a', 'Back to reference', 'market-update__back', {'href': f'#mu-ref-{n}', 'aria-label': f'Back to footnote reference {n}'}, ['↩'])]
        note_els.append(el)
    head = El('div', 'Head', 'market-update__head', children=[
        src.el(eyebrow, 'eyebrow', 'Eyebrow'),
        El('h2', 'Heading', 'market-update__title', {'id': 'market-update-h'}, [COPY(_text(title).strip())]),
        src.el(intro, 'market-update__intro', 'Intro'),
    ])
    return section('Market update', 'market-update', 'market-update-h', [
        El('div', 'Top', 'market-update__top', children=[head, media]) if media else head,
        El('ul', 'Investments', 'market-update__list', children=rows),
        src.el(closing, 'market-update__closing', 'Closing'),
        El('div', 'Sources', 'footnotes market-update__notes', children=[
            El('ol', 'Source notes', 'market-update__sources', children=note_els), disclaimer]),
    ], attrs={'id': 'market-update'})
