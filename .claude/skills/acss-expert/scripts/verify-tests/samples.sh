#!/usr/bin/env bash
# 5 sample prompts, run through the skill's three modes. Expected results are asserted.
cd "$(dirname "$0")/.."; S=verify-tests/samples; fail=0
chk(){ [ "$1" = "$2" ] && echo "ok   $3" || { echo "FAIL $3 (got $1 want $2)"; fail=1; }; }
# 1 Style: "pricing card grid, 3 columns, brand button" -> spec CSS verifies clean
python3 -I verify.py $S/1-pricing-grid.css >/dev/null; chk $? 0 "1 style: pricing grid verifies clean"
# 2 Style: "dark CTA band, butter CTA + outline" -> markup classes verify clean
python3 -I verify.py --site-styles ../../etch-expert/reference/fixtures/styles-used.json $S/2-cta-band.html >/dev/null; chk $? 0 "2 style: CTA band verifies clean"
# 3 Lookup: "what does --space-l resolve to?"
python3 -I lookup.py --space-l | grep -q '32px at min viewport to 36px'; chk $? 0 "3 lookup: --space-l = 32 to 36px"
# 4 Lookup: "is there a .grid--3 class?" -> absent with replacement
python3 -I lookup.py .grid--3 | grep -q 'ABSENT.*--grid-N'; chk $? 0 "4 lookup: .grid--3 absent, points to --grid-N"
# 5 Audit: 3.x HSL, .grid--3, hard-coded hex/px -> blocked, with fixes
out=$(python3 -I verify.py $S/5-audit-input.css); rc=$?
chk $rc 1 "5 audit: blocked"
for s in 'hsl(var(--x-h' '.grid--3' '#2446D8 equals --primary' 'padding: 24px equals --space-m'; do echo "$out" | grep -qF -- "$s" && echo "ok   5 audit finds: $s" || { echo "FAIL 5 audit missing: $s"; fail=1; }; done
exit $fail
