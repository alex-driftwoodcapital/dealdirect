#!/usr/bin/env bash
# usage: restore.sh <snapshot_dir> post <id> | option <name>   (dry run unless RESTORE_YES=1)
. "$(dirname "$0")/lib.sh"
S="$1"; kind="$2"; key="$3"; PROFILE="$(cat "$S/profile")"; . "$PROFILE"
for p in $PROTECTED_IDS; do [ "$kind" = post ] && [ "$key" = "$p" ] && { echo "REFUSED: $key is protected; needs Alex's typed OK" >&2; exit 3; }; done
echo "site: $SITE_NAME; restoring $kind $key from $S"
[ "${RESTORE_YES:-}" = 1 ] || { echo "dry run (set RESTORE_YES=1 to write)"; exit 0; }
if [ "$kind" = post ]; then
  scp_tmp="/tmp/etch-restore-$$.html"
  eval "$SSH_CMD" "'cat > $scp_tmp'" < "$S/post-$key.html"
  remote "wp post update $key $scp_tmp && rm -f $scp_tmp"
else
  scp_tmp="/tmp/etch-restore-$$.json"
  eval "$SSH_CMD" "'cat > $scp_tmp'" < "$S/option-$key.json"
  remote "wp option update $key --format=json < $scp_tmp && rm -f $scp_tmp"
fi
remote "$PURGE_CMD" >/dev/null 2>&1 || true; echo restored
