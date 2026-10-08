#!/usr/bin/env bash
# lint with ACSS class names accepted. usage: lint-acss.sh <snapshot_dir> FILE...
S="$1"; shift; H="$(cd "$(dirname "$0")/../.." && pwd)"
CSS="$H/acss-expert/index/automatic.css"; [ -f "$CSS" ] && A=(--acss-css "$CSS") || A=()
V="$H/acss-expert/scripts/verify.py"
rc=0
if [ -f "$V" ] && [ -f "$H/acss-expert/index/acss-index.json" ]; then python3 -I "$V" --site-styles "$S/option-etch_styles.json" "$@" || rc=1; fi
python3 "$H/etch-page-editor/scripts/lint.py" --styles "$S/option-etch_styles.json" --loops "$S/option-etch_loops.json" "${A[@]}" "$@" || rc=1
exit $rc
