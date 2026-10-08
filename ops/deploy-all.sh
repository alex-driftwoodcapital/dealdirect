#!/usr/bin/env bash
# Everything the site needs on STAGING, in order: plugin -> ACSS settings -> every page in site/pages/.
#   bash ops/deploy-all.sh             dry run (what each step would change)
#   RUN_YES=1 bash ops/deploy-all.sh   deploy
# Used by .github/workflows/staging.yml (dry run on PRs, deploy on merge to main); also runs fine on the Mac.
# Each step keeps its own backups and stop rules; the first failing step stops the rest.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
. "${ETCH_PROFILE:-.claude/skills/etch-page-editor/profiles/dealdirect-staging.env}"
mode=$([ "${RUN_YES:-}" = 1 ] && echo DEPLOY || echo "DRY RUN")
echo "### $SITE_NAME · $mode · $(git rev-parse --short HEAD 2>/dev/null || echo local)"
bash .claude/skills/etch-page-editor/scripts/ssh-setup.sh --check
if [ "${RUN_YES:-}" = 1 ] && [ -n "${DD_HUBSPOT_TOKEN:-}" ]; then
  # sent on stdin so it never appears in a command line or log; wp-config.php is the only place it is stored
  printf '%s' "$DD_HUBSPOT_TOKEN" | eval "$SSH_CMD" "'cd $WP_PATH && wp config set DD_HUBSPOT_TOKEN \"\$(cat)\" --type=constant --quiet'"
  echo "DD_HUBSPOT_TOKEN written to wp-config.php"
fi
echo; echo "### plugin"; bash ops/deploy-core.sh
echo; echo "### ACSS settings"; bash ops/acss/apply.sh
for f in site/pages/*.py; do
  page=$(basename "$f" .py)
  echo; echo "### page: $page"; python3 ops/page/deploy.py "$page"
done
echo; echo "### done ($mode)"
