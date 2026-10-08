#!/usr/bin/env python3
"""Lookup mode: name -> status, doc, value. python3 -I scripts/lookup.py NAME... (exact, or substring with -s). Stdlib only."""
import json, re, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent

def value_of(css, var):
    m = re.search(r'^\s*' + re.escape(var) + r':\s*([^;]+);', css, re.M)
    if not m: return None
    v = m[1].strip()
    c = re.fullmatch(r'clamp\(([\d.]+)rem,[^,]*,\s*([\d.]+)rem\)', v)
    if c:
        lo, hi = round(float(c[1]) * 16, 1), round(float(c[2]) * 16, 1)
        return f'{v}  (= {lo:g}px at min viewport to {hi:g}px at max)' if abs(lo - hi) > 1e-6 else f'{v}  (= {lo:g}px fixed)'
    return v

def main(argv):
    sub = '-s' in argv; names = [a for a in argv if a != '-s']
    if not names: print(__doc__); return 2
    d = json.load(open(ROOT / 'index/acss-index.json'))['entries']; css = open(ROOT / 'index/automatic.css').read()
    rc = 0
    for n in names:
        hits = [e for e in d if e['status'] == 'present' and (n in e['name'] if sub else e['name'] == n)]
        hits += [e for e in d if e['status'] == 'documented' and (n in e['name'] if sub else e['name'] == n)]
        if not hits:  # absent patterns last
            hits = [e for e in d if e['kind'] == 'absent' and re.match(e['pattern'], n)]
        if not hits: print(f'{n}: not found (not in the 4.0.1 build or docs index)'); rc = 1; continue
        for e in hits[:25 if sub else 1]:
            line = f"{e['name']}: {e['status']}"
            if e['kind'] == 'variable': line += f"  value: {value_of(css, e['name'])}"
            if e['status'] == 'absent': line = f"{n}: ABSENT in 4.0.1 (pattern {e['name']}); use: {e['replacement']}"
            print(f"{line}\n    group: {e['group']}  doc: {e['doc']}")
    return rc

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
