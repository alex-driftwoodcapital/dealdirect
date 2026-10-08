#!/usr/bin/env bash
# usage: diff.sh <snapshot_dir> ; compares live to snapshot. Exit 0 = no change, 1 = changed.
. "$(dirname "$0")/lib.sh"
S="$1"; PROFILE="$(cat "$S/profile")"; . "$PROFILE"; rc=0
while IFS=$'\t' read -r kind key mod sha; do
  if [ "$kind" = post ]; then
    live=$(remote "wp post get $key --field=post_content" | norm); snap=$(norm < "$S/post-$key.html")
    livemod=$(remote "wp post get $key --field=post_modified_gmt")
    if [ "$live" != "$snap" ]; then
      rc=1; echo "CHANGED post $key (modified $mod -> $livemod)"
      diff <(echo "$snap") <(echo "$live") | head -40 || true
      # builder re-save adds style ids / reformats; a new modified time with only styles-id differences = builder save, not a direct edit
      if diff <(echo "$snap" | sed -E 's/,"styles":\[[^]]*\]//g') <(echo "$live" | sed -E 's/,"styles":\[[^]]*\]//g') >/dev/null; then
        echo "  note: only style IDs differ -> looks like a BUILDER SAVE; do not overwrite direct edits without re-reading"
      fi
    else echo "same    post $key"; fi
  else
    live=$(remote "wp option get $key --format=json" | python3 -c 'import json,sys;print(json.dumps(json.load(sys.stdin),sort_keys=True))')
    snap=$(python3 -c 'import json,sys;print(json.dumps(json.load(open(sys.argv[1])),sort_keys=True))' "$S/option-$key.json")
    if [ "$live" != "$snap" ]; then
      rc=1; echo "CHANGED option $key"
      python3 -c '
import json,sys
a=json.load(open(sys.argv[1])); b=json.loads(sys.argv[2])
if isinstance(a,dict) and isinstance(b,dict):
    print("  added:",sorted(set(b)-set(a))); print("  removed:",sorted(set(a)-set(b))); print("  modified:",sorted(k for k in a if k in b and a[k]!=b[k]))' "$S/option-$key.json" "$live"
    else echo "same    option $key"; fi
  fi
done < "$S/manifest.tsv"
exit $rc
