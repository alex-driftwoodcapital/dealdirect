"""Split a site/styles/*.css file into etch_styles records: one top-level `.class { ... }` rule = one record whose
css is the rule body (Etch stores nested CSS with &, see fixtures/styles-used.json)."""
import re, textwrap
from etch import style_id


def parse(path: str) -> dict:
    src = re.sub(r'/\*.*?\*/', '', open(path, encoding='utf-8').read(), flags=re.S)
    rules, i = {}, 0
    while True:
        m = re.compile(r'\s*(\.[A-Za-z0-9_-]+)\s*\{').match(src, i)
        if not m:
            if src[i:].strip():
                raise ValueError(f'unparsed CSS near: {src[i:i + 80]!r}')
            return rules
        depth, j = 1, m.end()
        while depth:
            depth += {'{': 1, '}': -1}.get(src[j], 0)
            j += 1
        sel = m.group(1)
        if sel in rules:
            raise ValueError(f'duplicate rule {sel}')
        rules[sel] = textwrap.dedent(src[m.end():j - 1]).strip('\n').strip()
        i = j


def records(classes, rules) -> dict:
    """New-record payload for add-styles.py: {id: {type, selector, collection, css, readonly}}. Classes with no rule
    (ACSS-style hooks, containers) get an empty record, as the builder does."""
    out = {}
    for c in classes:
        sel = '.' + c
        out[style_id(sel)] = {'type': 'class', 'selector': sel, 'collection': 'default', 'css': rules.get(sel, ''), 'readonly': False}
    return out
