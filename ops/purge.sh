#!/usr/bin/env bash
# Purge every cache layer on STAGING after a deploy, and say what it found. The per-write PURGE_CMD (profile) relies on
# Breeze, which is installed but inactive on staging, so its purge was a silent no-op while a page-cache drop-in
# (wp-content/advanced-cache.php) and Cloudways Varnish kept serving old pages (QA 2026-10-09: new templates showed only
# on the never-cached 404 page). Layers: object cache, transients, page-cache folders, Varnish (the request Breeze
# itself sends: PURGE http://127.0.0.1:8080/.* with X-Purge-Method: regex and the site's Host).
#   bash ops/purge.sh          purge (only deletes caches)
#   bash ops/purge.sh --check  read-only: report the page-cache setup (dry runs)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
. "${ETCH_PROFILE:-$ROOT/.claude/skills/etch-page-editor/profiles/dealdirect-staging.env}"
case "$SITE_NAME" in *STAGING*) ;; *) echo "REFUSED: staging profile only ($SITE_NAME)" >&2; exit 3;; esac
r() { eval "$SSH_CMD" "'cd $WP_PATH && $*'" </dev/null; }
echo "== $SITE_NAME ($SITE_URL)"
r 'echo "WP_CACHE: $(wp config get WP_CACHE 2>/dev/null || echo unset)"; [ -f wp-content/advanced-cache.php ] && echo "page-cache drop-in: wp-content/advanced-cache.php ($(head -c 300 wp-content/advanced-cache.php | grep -o -i -m1 "breeze\|sg\|wp rocket\|litespeed\|w3 total" || echo unknown))" || echo "page-cache drop-in: none"'
[ "${1:-}" = --check ] && exit 0
r 'wp cache flush 2>&1 | tail -1; wp transient delete --all 2>&1 | tail -1'
r 'for d in breeze breeze-minification sgo-cache page_enhanced wp-rocket litespeed; do [ -d wp-content/cache/$d ] && { echo "page cache: wp-content/cache/$d ($(find wp-content/cache/$d -type f | wc -l) files) cleared"; rm -rf wp-content/cache/$d; }; done; true'
r 'host=$(wp option get home | sed -E "s#^https?://##; s#/.*##"); code=$(curl -s -o /dev/null -w "%{http_code}" -X PURGE -H "Host: $host" -H "X-Purge-Method: regex" "http://127.0.0.1:8080/.*" || echo none); echo "Varnish purge ($host): HTTP $code"'
