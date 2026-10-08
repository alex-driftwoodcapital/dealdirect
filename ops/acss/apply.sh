#!/usr/bin/env bash
# Apply ops/acss/dealdirect-settings.json to the ACSS settings on STAGING. Run from the repo root on the Mac.
#   bash ops/acss/apply.sh             dry run: lists every key that would change, writes nothing
#   RUN_YES=1 bash ops/acss/apply.sh   backup the option on the host, merge the input keys, save
# After a write, ACSS has to regenerate automatic.css. How it does that from the CLI is not verified yet: the script
# compares the stylesheet before/after and, if unchanged, asks for one click on Save in the ACSS dashboard.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
. "${ETCH_PROFILE:-$ROOT/.claude/skills/etch-page-editor/profiles/dealdirect-staging.env}"
case "$SITE_NAME" in *STAGING*) ;; *) echo "REFUSED: staging profile only ($SITE_NAME)" >&2; exit 3;; esac
r() { eval "$SSH_CMD" "'cd $WP_PATH && $*'" </dev/null; }
up() { eval "$SSH_CMD" "'cat > $1'" < "$2"; }
python3 -I "$ROOT/ops/acss/build-settings.py" >/dev/null
TMP="/tmp/dd-acss-$$"; r "mkdir -p $TMP"
up "$TMP/settings.json" "$ROOT/ops/acss/dealdirect-settings.json"; up "$TMP/apply.php" "$ROOT/ops/acss/apply.php"
css_sha() { r "f=\$(find wp-content/uploads -maxdepth 3 -name automatic.css | head -1); [ -n \"\$f\" ] && sha256sum \$f | cut -c1-16 || echo none"; }
echo "== $SITE_NAME ($SITE_URL)"
before=$(css_sha)
if [ "${RUN_YES:-}" != 1 ]; then r "wp eval-file $TMP/apply.php $TMP/settings.json dry; rm -rf $TMP"; echo "dry run OK (set RUN_YES=1 to write)"; exit 0; fi
STAMP=$(date +%Y%m%d-%H%M%S)
r "mkdir -p ~/backups && wp option list --search=\"*automatic*\" --field=option_name | while read o; do wp option get \$o --format=json > ~/backups/\$o-$STAMP.json; done; ls ~/backups/*-$STAMP.json"
r "wp eval-file $TMP/apply.php $TMP/settings.json write; rm -rf $TMP"
r "$PURGE_CMD" >/dev/null 2>&1 || true
after=$(css_sha)
echo "automatic.css sha: $before -> $after"
[ "$before" != "$after" ] && echo "stylesheet regenerated" || echo "NOT regenerated yet: open WP Admin > Automatic.css dashboard and click Save once, then re-run the inventory to rebuild the index"
echo "rollback: wp option update <option> --format=json < ~/backups/<option>-$STAMP.json (on the host), then Save in the ACSS dashboard"
