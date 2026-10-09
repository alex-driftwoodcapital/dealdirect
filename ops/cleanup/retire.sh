#!/usr/bin/env bash
# Trash the previous build's leftover components/templates on STAGING (ops/cleanup/leftovers.json). Runs last in
# ops/deploy-all.sh, after our templates replaced theirs.
#   bash ops/cleanup/retire.sh             dry run: what would be trashed or kept, and why
#   RUN_YES=1 bash ops/cleanup/retire.sh   backup (JSON on the host), then trash (restorable from WP admin > Trash)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
. "${ETCH_PROFILE:-$ROOT/.claude/skills/etch-page-editor/profiles/dealdirect-staging.env}"
case "$SITE_NAME" in *STAGING*) ;; *) echo "REFUSED: staging profile only ($SITE_NAME)" >&2; exit 3;; esac
r() { eval "$SSH_CMD" "'cd $WP_PATH && $*'" </dev/null; }
up() { eval "$SSH_CMD" "'cat > $1'" < "$2"; }
mkdir -p "$ROOT/build"
python3 -I - "$ROOT" > "$ROOT/build/retire-in.json" <<'PY'
import importlib, json, os, sys
root = sys.argv[1]
sys.path[:0] = [os.path.join(root, 'site', 'pages'), os.path.join(root, 'site', 'lib')]
spec = json.load(open(os.path.join(root, 'ops', 'cleanup', 'leftovers.json')))
ours = [m.META['slug'] for m in (importlib.import_module(f[:-3]) for f in sorted(os.listdir(os.path.join(root, 'site', 'pages'))) if f.endswith('.py'))
        if getattr(m, 'META', {}).get('kind') == 'template']
print(json.dumps({'posts': spec['posts'], 'ours': ours}))
PY
TMP="/tmp/dd-retire-$$"; r "mkdir -p $TMP"
up "$TMP/in.json" "$ROOT/build/retire-in.json"; up "$TMP/retire.php" "$ROOT/ops/cleanup/retire.php"
echo "== $SITE_NAME ($SITE_URL)"
if [ "${RUN_YES:-}" != 1 ]; then r "wp eval-file $TMP/retire.php $TMP/in.json dry; rm -rf $TMP"; echo "dry run OK (set RUN_YES=1 to write)"; exit 0; fi
STAMP=$(date +%Y%m%d-%H%M%S)
r "mkdir -p ~/backups && wp post list --post_type=wp_block,wp_template --post_status=publish,draft,private --fields=ID,post_type,post_name,post_status,post_content --format=json > ~/backups/blocks-templates-$STAMP.json && echo backup: ~/backups/blocks-templates-$STAMP.json"
r "wp eval-file $TMP/retire.php $TMP/in.json write; rm -rf $TMP"
r "$PURGE_CMD" >/dev/null 2>&1 || true
