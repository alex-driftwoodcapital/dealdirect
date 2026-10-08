#!/usr/bin/env bash
# One safe write. usage:
#   edit-run.sh <post_id> <content.html> --expect-sha <16hex> [--verify <url>...]
#   edit-run.sh --new "<title>" <slug> <content.html> [--verify <url>...]      (creates a DRAFT page)
# Steps: snapshot -> lint (errors stop) -> protected/conflict check -> write -> purge -> diff -> verify. Dry run unless RUN_YES=1.
. "$(dirname "$0")/lib.sh"
HERE="$(cd "$(dirname "$0")" && pwd)"
if [ "$1" = --new ]; then NEWTITLE="$2"; SLUG="$3"; FILE="$4"; shift 4; ID=""; else ID="$1"; FILE="$2"; shift 2; fi
EXPECT=""; VERIFY=()
while [ $# -gt 0 ]; do case "$1" in --expect-sha) EXPECT="$2"; shift 2;; --verify) shift; while [ $# -gt 0 ] && [[ "$1" != --* ]]; do VERIFY+=("$1"); shift; done;; *) echo "bad arg $1" >&2; exit 2;; esac; done
echo "== site: $SITE_NAME ($SITE_URL)"
if [ -n "$ID" ]; then
  for p in $PROTECTED_IDS; do [ "$ID" = "$p" ] && { echo "REFUSED: $ID is protected" >&2; exit 3; }; done
  [ -n "$EXPECT" ] || { echo "REFUSED: --expect-sha required for an existing page (sha of the content you based your edit on; see manifest.tsv)" >&2; exit 3; }
  SNAP=$("$HERE/snapshot.sh" "$ID" | tail -1)
  LIVE=$(awk -F'\t' -v i="$ID" '$1=="post"&&$2==i{print $4}' "$SNAP/manifest.tsv")
  [ "$LIVE" = "$EXPECT" ] || { echo "STOP: page changed since you read it (live $LIVE, expected $EXPECT). Re-read and merge." >&2; exit 4; }
else SNAP=$("$HERE/snapshot.sh" | tail -1); fi
echo "snapshot: $SNAP"
"$HERE/../../etch-builder/scripts/lint-acss.sh" "$SNAP" "$FILE" || { echo "STOP: lint errors" >&2; exit 5; }
[ "${RUN_YES:-}" = 1 ] || { echo "dry run OK (set RUN_YES=1 to write)"; exit 0; }
if [ -n "$ID" ]; then
  eval "$SSH_CMD" "'cd $WP_PATH && wp post update $ID -'" < "$FILE" | tail -1
else
  ID=$(eval "$SSH_CMD" "'cd $WP_PATH && wp post create --post_type=page --post_status=draft --post_title=\"$NEWTITLE\" --post_name=$SLUG --porcelain -'" < "$FILE"); echo "created draft page $ID"
fi
remote "$PURGE_CMD" >/dev/null 2>&1 || true
echo "== diff vs snapshot (expected: only your change)"; [ -f "$SNAP/post-$ID.html" ] && { "$HERE/diff.sh" "$SNAP" | grep -E "^(CHANGED post|same    post|[<>])" | head -20 || true; }  # diff.sh exits 1 when something changed, which is the point here
if [ ${#VERIFY[@]} -gt 0 ]; then node "$HERE/verify/verify.mjs" "${SNAP}/verify" "${VERIFY[@]}" || { echo "verify FAILED" >&2; echo "post id: $ID   rollback: RESTORE_YES=1 $HERE/restore.sh $SNAP post $ID"; exit 6; }; fi
echo "post id: $ID   rollback: RESTORE_YES=1 $HERE/restore.sh $SNAP post $ID"
exit 0
