#!/usr/bin/env bash
# Read-only diagnosis of the site forms on STAGING (Actions > "Forms check"). Submits nothing to HubSpot.
#  1. HubSpot side (ops/forms/check.php on the host): token present, each form readable with its fields, contact search.
#  2. The endpoint from outside, as a browser would: GET /token twice (fresh nonce each time, not cached), then POST /submit
#     without a nonce (expect 403) and with a nonce but an empty body (expect 400, validation): reachable, nothing sent on.
#  3. What staging logged: today's /dealdirect/v1 requests from the access logs (time, method, path, status; no IPs) and
#     the plugin's own "dealdirect:" error lines.
# env: STAGING_HTTP_USER / STAGING_HTTP_PASSWORD (basic auth in front of staging)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
. "${ETCH_PROFILE:-$ROOT/.claude/skills/etch-page-editor/profiles/dealdirect-staging.env}"
case "$SITE_NAME" in *STAGING*) ;; *) echo "REFUSED: staging profile only ($SITE_NAME)" >&2; exit 3;; esac
r() { eval "$SSH_CMD" "'cd $WP_PATH && $*'" </dev/null; }
up() { eval "$SSH_CMD" "'cat > $1'" < "$2"; }
bash "$ROOT/.claude/skills/etch-page-editor/scripts/ssh-setup.sh" --check >/dev/null
echo "== HubSpot (from staging)"
TMP="/tmp/dd-forms-$$"; r "mkdir -p $TMP"; up "$TMP/check.php" "$ROOT/ops/forms/check.php"
r "wp eval-file $TMP/check.php; rm -rf $TMP"

echo; echo "== endpoint (from outside)"
A=(-s -u "${STAGING_HTTP_USER:-}:${STAGING_HTTP_PASSWORD:-}")
for i in 1 2; do
  out=$(curl "${A[@]}" -D /tmp/h$i -o /tmp/b$i -w '%{http_code}' "$SITE_URL/wp-json/dealdirect/v1/token?x=$RANDOM" || echo 000)
  echo "GET /token #$i: HTTP $out · $(grep -i -E '^(cache-control|x-cache|age|x-varnish|cf-cache-status):' /tmp/h$i | tr -d '\r' | tr '\n' ' ')"
done
n1=$(python3 -c "import json;print(json.load(open('/tmp/b1')).get('nonce',''))" 2>/dev/null || true)
n2=$(python3 -c "import json;print(json.load(open('/tmp/b2')).get('nonce',''))" 2>/dev/null || true)
echo "nonce returned: $([ -n "$n1" ] && echo yes || echo NO) · same both times: $([ "$n1" = "$n2" ] && echo yes || echo no) (same is normal within 12 h)"
plain=$(curl "${A[@]}" -o /tmp/b3 -w '%{http_code}' "$SITE_URL/wp-json/dealdirect/v1/token" || echo 000)
n3=$(python3 -c "import json;print(json.load(open('/tmp/b3')).get('nonce',''))" 2>/dev/null || true)
echo "GET /token without cache-buster: HTTP $plain · nonce matches a fresh one: $([ "$n3" = "$n1" ] && echo yes || echo 'NO (a cached nonce: submissions answer 403)')"
code=$(curl "${A[@]}" -o /tmp/b4 -w '%{http_code}' -X POST -H 'Content-Type: application/json' -d '{}' "$SITE_URL/wp-json/dealdirect/v1/submit" || echo 000)
echo "POST /submit, no nonce: HTTP $code (expect 403) $(head -c 160 /tmp/b4)"
code=$(curl "${A[@]}" -o /tmp/b5 -w '%{http_code}' -X POST -H 'Content-Type: application/json' -H "X-DD-Nonce: $n1" -d '{"form":"registration"}' "$SITE_URL/wp-json/dealdirect/v1/submit" || echo 000)
echo "POST /submit, nonce, empty form: HTTP $code (expect 400 validation; nothing reaches HubSpot) $(head -c 200 /tmp/b5)"

echo; echo "== staging logs (today, /dealdirect/v1)"
r 'L=../logs; ls $L 2>/dev/null | tr "\n" " "; echo; for f in $L/*access*.log; do [ -f "$f" ] || continue; grep -h "dealdirect/v1" "$f" | grep "$(date +%d/%b/%Y)" | awk "{print \$4, \$6, \$7, \$9}" | tail -n 40; done; echo "-- plugin errors:"; for f in $L/*error*.log ../logs/php*.log wp-content/debug.log; do [ -f "$f" ] && grep -h "dealdirect:" "$f" | tail -n 30; done; true'
