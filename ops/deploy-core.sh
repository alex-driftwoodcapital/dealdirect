#!/usr/bin/env bash
# Deploy wp-content/plugins/dealdirect-core to STAGING. Run from the repo root on the Mac.
#   bash ops/deploy-core.sh            dry run: shows what would change, writes nothing
#   RUN_YES=1 bash ops/deploy-core.sh  deploy
# Steps: backup of the current plugin dir on the host -> activate Secure Custom Fields (installed on staging; installed here only if missing) ->
# upload plugin -> activate -> seed Platform stats (empty fields only) -> flush rewrites -> read-back checks.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PROFILE="${ETCH_PROFILE:-$ROOT/.claude/skills/etch-page-editor/profiles/dealdirect-staging.env}"
. "$PROFILE"
case "$SITE_NAME" in *STAGING*) ;; *) echo "REFUSED: staging profile only ($SITE_NAME)" >&2; exit 3;; esac
r() { eval "$SSH_CMD" "'cd $WP_PATH && $*'" </dev/null; }
echo "== $SITE_NAME ($SITE_URL)"
echo "-- current state"
r "wp plugin list --name=secure-custom-fields --fields=name,status,version --format=csv; wp plugin list --name=dealdirect-core --fields=name,status,version --format=csv; wp config has DD_HUBSPOT_TOKEN && echo DD_HUBSPOT_TOKEN: set || echo DD_HUBSPOT_TOKEN: NOT set"
[ "${RUN_YES:-}" = 1 ] || { echo "dry run OK (set RUN_YES=1 to deploy)"; exit 0; }

STAMP=$(date +%Y%m%d-%H%M%S)
r "mkdir -p ~/backups && if [ -d wp-content/plugins/dealdirect-core ]; then tar czf ~/backups/dealdirect-core-$STAMP.tgz -C wp-content/plugins dealdirect-core && echo backup: ~/backups/dealdirect-core-$STAMP.tgz; fi"
r "wp plugin is-installed secure-custom-fields || wp plugin install secure-custom-fields; wp plugin activate secure-custom-fields"
# tests/ stays in the repo; only runtime files go to the server
tar czf - -C "$ROOT/wp-content/plugins" --exclude='dealdirect-core/tests' dealdirect-core \
  | eval "$SSH_CMD" "'cd $WP_PATH/wp-content/plugins && rm -rf dealdirect-core.new && mkdir dealdirect-core.new && tar xzf - -C dealdirect-core.new --strip-components=1 && rm -rf dealdirect-core && mv dealdirect-core.new dealdirect-core'"
r "wp plugin activate dealdirect-core && wp dealdirect seed-stats && wp rewrite flush --hard"
r "$PURGE_CMD" >/dev/null 2>&1 || true
echo "-- read-back"
r "wp plugin list --name=dealdirect-core --fields=name,status,version --format=csv; wp post-type get offering --field=name; wp option get options_aum"
code=$(curl -s -o /dev/null -w '%{http_code}' "$SITE_URL/wp-json/dealdirect/v1/token" || true)
echo "GET /wp-json/dealdirect/v1/token -> $code (expect 200)"
echo "rollback: ssh in, then: cd $WP_PATH/wp-content/plugins && rm -rf dealdirect-core && tar xzf ~/backups/dealdirect-core-$STAMP.tgz (or wp plugin deactivate dealdirect-core if this was the first deploy)"
