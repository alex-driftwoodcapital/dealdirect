#!/usr/bin/env python3
"""Fill proven section templates from a page spec. usage: fill.py spec.json > content.html
spec: {"sections":[{"type":"page-hero","crumb":..,"eyebrow":..,"heading":..,"highlight":..,"sub":..,"primaryLabel":..,"primaryUrl":..,"secondaryLabel":..,"secondaryUrl":..},
                    {"type":"band","id":"slug","name":"Band","kicker":..,"heading":..,"sub":..}]}
             {"type":"callout-band","name":..,"tone":"ink|butter|blue","kicker":..,"heading":..,"highlight":..,"sub":..,"buttonLabel":..,"buttonUrl":..,"headingId":"slug"}]}
Only section types with a template in ../templates/ (proven by the round-trip pilot) are supported."""
import json, re, sys, os
T = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates')
def esc(v):  # JSON-string-safe, Etch style (< > & as \u escapes)
    return json.dumps(str(v), ensure_ascii=False)[1:-1].replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
spec = json.load(open(sys.argv[1])); out = []
for s in spec['sections']:
    p = os.path.join(T, s['type'] + '.html')
    if not os.path.exists(p): sys.exit(f"no proven template for section type {s['type']!r}")
    t = open(p).read()
    need = set(re.findall(r'__(\w+)__', t)); missing = need - set(s)
    if missing: sys.exit(f"section {s['type']}: missing {sorted(missing)}")
    if s['type'] == 'callout-band' and (s['tone'] not in ('ink','butter','blue') or not re.fullmatch(r'[a-z][a-z0-9-]*', s['headingId'])): sys.exit('callout-band: tone must be ink|butter|blue; headingId lowercase-kebab')
    if s['type'] == 'band' and not re.fullmatch(r'[a-z][a-z0-9-]*', s['id']): sys.exit('band id must be lowercase-kebab')
    out.append(re.sub(r'__(\w+)__', lambda m: esc(s[m.group(1)]), t).strip())
print('\n\n'.join(out))
