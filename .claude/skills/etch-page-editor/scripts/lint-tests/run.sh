#!/usr/bin/env bash
# fixtures must pass (0 errors), seeded bad markup must fail with every expected error. Usage: lint-tests/run.sh <etch_styles.json> <etch_loops.json>
cd "$(dirname "$0")/.."; ok=0
FIX=../../etch-expert/reference/fixtures
python3 lint.py --styles "$1" --loops "$2" $FIX/*/*.html >/dev/null && echo "PASS fixtures lint clean" || { echo "FAIL fixtures"; ok=1; }
out=$(python3 lint.py --styles "$1" --loops "$2" lint-tests/bad.html); rc=$?
[ $rc -eq 1 ] || { echo "FAIL seeded file did not fail"; ok=1; }
for want in "not in etch_styles" "plain img" "inline event handler" "unsafe raw HTML" "unknown block type" "dynamic-image without mediaId" "not in etch_loops" "condition needs both" "invalid JSON" "numeric ref" "never closed"; do
  echo "$out" | grep -q "$want" && echo "  caught: $want" || { echo "  MISSED: $want"; ok=1; }
done
exit $ok
