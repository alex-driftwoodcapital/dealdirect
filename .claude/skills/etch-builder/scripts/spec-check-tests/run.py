#!/usr/bin/env python3
"""Tests for spec-check.py: good/services.yaml must pass; each seeded mutation must fail with its expected code.
Run: python3 -I scripts/spec-check-tests/run.py   (needs PyYAML). Exit 1 on any failed test."""
import copy, importlib.util, io, json, pathlib, sys, tempfile, contextlib

HERE = pathlib.Path(__file__).resolve().parent
spec_mod = importlib.util.spec_from_file_location('spec_check', HERE.parent / 'spec-check.py')
sc = importlib.util.module_from_spec(spec_mod); spec_mod.loader.exec_module(sc)
import yaml

GOOD = yaml.safe_load((HERE / 'good/services.yaml').read_text())


def S(i):  # section i of the copy
    return lambda d: d['sections'][i]


def mut(fn):
    d = copy.deepcopy(GOOD); fn(d); return d


def setp(d, path, val):
    *head, last = path
    for k in head: d = d[k]
    if val is DEL: del d[last]
    else: d[last] = val


DEL = object()
CASES = [  # (name, mutation, expected code)
    ('copy placeholder', lambda d: setp(d, ['sections', 0, 'content', 1, 'text'], 'TODO final intro'), 'E_PLACEHOLDER'),
    ('missing copy text', lambda d: setp(d, ['sections', 1, 'content', 0, 'text'], ''), 'E_CONTENT'),
    ('unknown ACSS token', lambda d: setp(d, ['tokens', 'type', 'body'], '--text-medium'), 'E_TOKEN'),
    ('3.x ACSS class as surface', lambda d: setp(d, ['tokens', 'surfaces', 'light'], 'grid--3'), 'E_TOKEN'),
    ('unknown var in layout', lambda d: setp(d, ['sections', 1, 'layout', 'wide'], 'grid gap var(--gap-xl)'), 'E_TOKEN'),
    ('no layout narrow', lambda d: setp(d, ['sections', 0, 'layout', 'narrow'], DEL), 'E_LAYOUT'),
    ('no responsive intent', lambda d: setp(d, ['sections', 1, 'responsive'], DEL), 'E_RESPONSIVE'),
    ('media by URL', lambda d: setp(d, ['sections', 0, 'media', 0, 'media_id'], 'https://x.org/a.jpg'), 'E_MEDIA'),
    ('image without alt', lambda d: setp(d, ['sections', 0, 'media', 0, 'alt'], DEL), 'E_ALT'),
    ('no wide shot', lambda d: setp(d, ['references', 'shots', 1440], DEL), 'E_SHOTS'),
    ('shot file missing', lambda d: setp(d, ['references', 'shots', 375], 'refs/nope-375.png'), 'E_FILE'),
    ('no shots at all', lambda d: setp(d, ['references', 'shots'], DEL), 'E_SHOTS'),
    ('two h1', lambda d: setp(d, ['sections', 1, 'heading', 'level'], 1), 'E_H1'),
    ('first section not h1', lambda d: setp(d, ['sections', 0, 'heading', 'level'], 2), 'E_H1'),
    ('skipped heading level', lambda d: setp(d, ['sections', 1, 'content', 1, 'type'], 'h4'), 'E_HEADING_ORDER'),
    ('section without heading', lambda d: setp(d, ['sections', 1, 'heading'], DEL), 'E_HEADING'),
    ('link used for on-page action', lambda d: setp(d, ['sections', 0, 'content', 2], {'type': 'link', 'text': 'Open', 'href': '#', 'action': 'open dialog tour-video', 'style': 'btn--secondary'}), 'E_LINK'),
    ('button with href', lambda d: setp(d, ['sections', 0, 'content', 3, 'href'], '/tour/'), 'E_BUTTON'),
    ('no button role', lambda d: setp(d, ['sections', 0, 'content', 2, 'style'], DEL), 'E_STYLE'),
    ('unknown button class', lambda d: setp(d, ['sections', 0, 'content', 2, 'style'], 'btn--yellow'), 'E_STYLE'),
    ('neighbours share a surface', lambda d: setp(d, ['sections', 2, 'surface'], 'ink') or setp(d, ['sections', 1, 'surface'], 'ink'), 'E_SURFACE_NEIGHBOR'),
    ('surface not in tokens', lambda d: setp(d, ['sections', 1, 'surface'], 'lavender'), 'E_SURFACE'),
    ('nested loop same item name', lambda d: setp(d, ['sections', 1, 'data', 'loop', 'inner', 'item'], 'service'), 'E_LOOP'),
    ('loop without source', lambda d: setp(d, ['sections', 1, 'data', 'loop', 'source'], DEL), 'E_LOOP'),
    ('component without ref', lambda d: setp(d, ['sections', 2, 'component', 'ref'], DEL), 'E_COMPONENT'),
    ('dialog nobody opens', lambda d: setp(d, ['sections', 0, 'content', 3, 'action'], 'play video inline'), 'E_DIALOG'),
    ('dialog without close', lambda d: setp(d, ['sections', 3, 'content'], [{'type': 'embed', 'source': 'x'}]), 'E_DIALOG'),
    ('published status', lambda d: setp(d, ['page', 'status'], 'publish'), 'E_STATUS'),
    ('duplicate section id', lambda d: setp(d, ['sections', 1, 'id'], 'services-intro'), 'E_ID'),
    ('no must_match', lambda d: setp(d, ['sections', 2, 'must_match'], DEL), 'E_MUST_MATCH'),
    ('motion without reduced', lambda d: setp(d, ['sections', 0, 'motion'], {'ref': 'site-motion.md#reveal'}), 'E_MOTION'),
    ('scope names unknown section', lambda d: setp(d, ['scope'], ['services-pricing']), 'E_SCOPE'),
]


def run(spec):
    with tempfile.NamedTemporaryFile('w', suffix='.json', dir=HERE / 'good', delete=False) as f:
        json.dump(spec, f); p = f.name
    out = io.StringIO()
    try:
        with contextlib.redirect_stdout(out):
            rc = sc.main([p, '--json'])
    finally:
        pathlib.Path(p).unlink()
    return rc, json.loads(out.getvalue())


def main():
    fails = 0
    rc, res = run(GOOD)
    ok = rc == 0 and not res['items']
    print(('PASS' if ok else 'FAIL') + '  good/services.yaml passes clean' + ('' if ok else f'  {res["items"]}'))
    fails += not ok
    for name, fn, code in CASES:
        rc, res = run(mut(fn))
        codes = {i['code'] for i in res['items'] if i['severity'] == 'ERROR'}
        ok = rc == 1 and code in codes
        print(('PASS' if ok else 'FAIL') + f'  {name}: expects {code}' + ('' if ok else f'  got rc={rc} {sorted(codes)}'))
        fails += not ok
    total = len(CASES) + 1
    repo = HERE.parents[3]  # repo root when run from the twoeleven-studio checkout
    home = HERE.parents[1] / 'examples/home-v117/home.yaml'
    if (repo / 'etch-build/mockup-v117.zip').exists() and home.exists():
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = sc.main([str(home), '--root', str(repo), '--json'])
        got = sorted((i['code'], i['where']) for i in json.loads(out.getvalue())['items'])
        want = [('E_PLACEHOLDER', 'references.shots.1440'), ('E_PLACEHOLDER', 'references.shots.375')]
        ok = rc == 1 and got == want
        print(('PASS' if ok else 'FAIL') + '  examples/home-v117: only the two missing full-page shots are open' + ('' if ok else f'  got {got}'))
        fails += not ok; total += 1
    print(f'{total - fails}/{total} passed')
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
