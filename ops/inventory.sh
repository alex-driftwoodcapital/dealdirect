#!/usr/bin/env bash
# Phase 1 inventory. READ-ONLY on both sites. Run by .github/workflows/inventory.yml (Actions > Inventory), or from the
# repo root on the Mac (needs SSH to staging + internet). User accounts are never exported (the output is committed):
#   bash ops/inventory.sh            -> writes inventory/<YYYYMMDD>/
# Staging: WP-CLI reads over SSH. Live: public GETs only (pages, sitemap, WP REST), no login, no form posts.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
. "$ROOT/.claude/skills/etch-page-editor/profiles/dealdirect-staging.env"
LIVE="https://driftwooddealdirect.com"
OUT="$ROOT/inventory/$(date +%Y%m%d)"; mkdir -p "$OUT/staging" "$OUT/live/pages" "$OUT/live/rest"
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
r() { eval "$SSH_CMD" "'cd $WP_PATH && $*'" </dev/null; }
get() { curl -sSL -A "$UA" --max-time 30 "$@"; }
echo "== staging (read-only WP-CLI)"
s() { local f="$1"; shift; r "$@" > "$OUT/staging/$f" 2>&1 || echo "  (failed: $f)"; }
s core.txt              "wp core version --extra"
s plugins.csv           "wp plugin list --fields=name,status,version,update --format=csv"
s themes.csv            "wp theme list --fields=name,status,version --format=csv"
s post-types.json       "wp post-type list --fields=name,label,public,rewrite --format=json"
s pages.csv             "wp post list --post_type=any --post_status=any --fields=ID,post_type,post_name,post_title,post_status --format=csv"
s options-site.txt      "wp option get home; wp option get siteurl; wp option get blog_public; wp option get permalink_structure; wp option get show_on_front; wp option get page_on_front; wp option get timezone_string"
s options-etch-acss.txt "wp option list --search=\"*etch*\" --fields=option_name,autoload --format=csv; wp option list --search=\"*automatic*\" --fields=option_name,autoload --format=csv; wp option list --search=\"*acss*\" --fields=option_name,autoload --format=csv"
s acss-files.txt        "find wp-content/uploads -maxdepth 3 -iname \"*automatic*.css\" -o -maxdepth 3 -iname \"*acss*.css\" | head -20"
s media-count.txt       "wp post list --post_type=attachment --format=count"
# the compiled ACSS stylesheet, for acss-expert/scripts/build-index.py
css=$(r "find wp-content/uploads -maxdepth 3 -name automatic.css | head -1" || true)
[ -n "$css" ] && r "cat $css" > "$OUT/staging/automatic.css" && echo "  saved automatic.css ($css)"
echo "== live (public GETs)"
get -o "$OUT/live/robots.txt" "$LIVE/robots.txt" || true
for sm in sitemap_index.xml wp-sitemap.xml sitemap.xml; do
  code=$(curl -s -o "$OUT/live/$sm" -w '%{http_code}' -A "$UA" "$LIVE/$sm" || true); [ "$code" = 200 ] || rm -f "$OUT/live/$sm"
done
get -o "$OUT/live/rest/types.json" "$LIVE/wp-json/wp/v2/types" || true
get -o "$OUT/live/rest/pages.json" "$LIVE/wp-json/wp/v2/pages?per_page=100&_fields=id,slug,link,title,status,template,parent" || true
for t in offering offerings; do
  code=$(curl -s -o "$OUT/live/rest/$t.json" -w '%{http_code}' -A "$UA" "$LIVE/wp-json/wp/v2/$t?per_page=100" || true)
  [ "$code" = 200 ] || rm -f "$OUT/live/rest/$t.json"
done
for p in 1 2 3 4 5 6 7 8 9 10; do
  code=$(curl -s -o "$OUT/live/rest/media-$p.json" -w '%{http_code}' -A "$UA" \
    "$LIVE/wp-json/wp/v2/media?per_page=100&page=$p&_fields=id,slug,source_url,alt_text,mime_type,media_details.width,media_details.height" || true)
  [ "$code" = 200 ] || { rm -f "$OUT/live/rest/media-$p.json"; break; }
done
# rendered HTML of every page in the permalink map (source of verbatim copy, SEO meta, anchors, forms)
for path in / /eb-5-investments/ /inversiones-eb-5/ /investimentos-eb-5/ /new-eb-5-page/ /forgot-password/ /offering/riverside-wharf-preferred-equity/; do
  name=$(echo "$path" | sed 's#^/##; s#/$##; s#/#__#g'); [ -n "$name" ] || name=home
  code=$(curl -s -o "$OUT/live/pages/$name.html" -w '%{http_code}' -A "$UA" -L "$LIVE$path" || true)
  echo "  $code $path"
done
# offering singles listed by the REST API, if exposed
if [ -f "$OUT/live/rest/offering.json" ]; then
  python3 -c 'import json,sys;[print(o["link"]) for o in json.load(open(sys.argv[1]))]' "$OUT/live/rest/offering.json" | while read -r u; do
    name="offering__$(basename "$u")"; [ -f "$OUT/live/pages/$name.html" ] || get -o "$OUT/live/pages/$name.html" "$u" || true
  done
fi
# extra copy sources (ops/sources.txt): public GETs, rendered HTML + the WP REST post when exposed
mkdir -p "$OUT/sources"
[ -f "$ROOT/ops/sources.txt" ] && grep -v '^\s*#' "$ROOT/ops/sources.txt" | sed 's/#.*//' | while read -r u; do
  [ -n "$u" ] || continue
  host=$(echo "$u" | sed -E 's#https?://([^/]+).*#\1#'); slug=$(basename "${u%/}")
  code=$(curl -s -o "$OUT/sources/${host}__${slug}.html" -w '%{http_code}' -A "$UA" -L "$u" || true)
  echo "  $code $u"
  for t in posts pages; do
    get -o "$OUT/sources/${host}__${slug}.$t.json" "https://$host/wp-json/wp/v2/$t?slug=$slug" || true
    grep -q '"id"' "$OUT/sources/${host}__${slug}.$t.json" 2>/dev/null || rm -f "$OUT/sources/${host}__${slug}.$t.json"
  done
done
echo "== done: $OUT"
ls -R "$OUT" | head -60
