#!/usr/bin/env bash
# Proves verify.py: seeded-bad inputs must BLOCK (exit 1) with the expected findings; 10 real TwoEleven styles + 6 real
# fixtures (pages/components) must not produce ERRORs except the 2 known live-site bugs listed below.
set -u; cd "$(dirname "$0")/.."; V="python3 -I verify.py"; T=verify-tests
F=../../etch-expert/reference/fixtures; fail=0
ok(){ echo "ok   $1"; }; bad(){ echo "FAIL $1"; fail=1; }
exp(){ # name file expected-substring...
  n=$1; f=$2; shift 2; out=$($V "$f" 2>&1); rc=$?
  [ $rc -eq 1 ] || { bad "$n exit $rc (want 1)"; return; }
  for s in "$@"; do echo "$out" | grep -qF -- "$s" || { bad "$n missing: $s"; return; }; done; ok "$n"; }
exp bad.css $T/bad.css 'var(--primary-trans-10)' 'hsl(var(--x-h' '?not-a-recipe' '3.x syntax "@btn;"' '@import' 'var(--space-3xs)' '.link--primary' 'var(--body-color)' '#2446D8 equals --primary' 'fluid() is a 3.x'
$V $T/bad.css | grep -q 'padding: 24px equals --space-m' && ok 'token warning' || bad 'token warning'
exp bad.html $T/bad.html '<style>' 'rel=stylesheet' '.grid--3' '.gap--m' '.text--primary' '.link--primary' '.stretch' '.btn--tertiary'
$V $T/good.html >/dev/null && ok good.html || bad good.html
$V --classes btn--primary width--60 >/dev/null && ok 'classes present' || bad 'classes present'
$V --classes grid--3 >/dev/null; [ $? -eq 1 ] && ok 'classes absent blocks' || bad 'classes absent blocks'
# real: fixtures (pages, components) with the site's own styles
for f in $F/pages/*.html $F/components/*.html; do
  $V --site-styles $F/styles-used.json "$f" >/dev/null && ok "real $(basename $f)" || { bad "real $(basename $f)"; $V --site-styles $F/styles-used.json "$f" | head -5; }
done
# real: 10 styles from etch_styles; plus the 2 known live-site bugs must be caught
python3 -I - "$F" <<'P' || fail=1
import json,sys,importlib.util,os,tempfile
F=sys.argv[1]; s=importlib.util.spec_from_file_location('v','verify.py'); m=importlib.util.module_from_spec(s); sys.modules['v']=m; s.loader.exec_module(m)
st=json.load(open(F+'/styles-used.json')); gs=json.load(open(F+'/global-stylesheets.json'))
g=os.path.join(tempfile.mkdtemp(),'g.css'); open(g,'w').write('\n'.join(v['css'] for v in gs.values()))
v=m.Verifier.load(site_styles=F+'/styles-used.json',site_css=[g])
known={'.header-wrapper':'--text-color-dark','.site-footer__newsletter':'--space-3xs'}
rc=0; n=0
for k,x in st.items():
    errs=[r['message'] for r in v.check_css(x['css'],x['selector']) if r['severity']=='ERROR']
    if x['selector'] in known:
        hit=any(known[x['selector']] in e for e in errs); print('ok  ' if hit else 'FAIL','known bug caught',x['selector'],known[x['selector']]); rc|=not hit
    else:
        n+=1
        if errs: print('FAIL real style',x['selector'],errs[:2]); rc|=1
print(f'ok   {n} real styles clean' if not rc else 'FAIL real styles')
sys.exit(rc)
P
exit $fail
