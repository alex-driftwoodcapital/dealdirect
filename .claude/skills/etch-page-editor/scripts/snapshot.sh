#!/usr/bin/env bash
# usage: snapshot.sh <post_id>... ; also snapshots $SNAP_OPTIONS. Prints the snapshot dir.
. "$(dirname "$0")/lib.sh"
OUT="${SNAP_DIR:-$HOME/etch-snapshots}/$(date +%Y%m%d-%H%M%S)"; mkdir -p "$OUT"
echo "site: $SITE_NAME ($SITE_URL) host: $(remote hostname)" >&2
: > "$OUT/manifest.tsv"
for id in "$@"; do
  remote "wp post get $id --field=post_content" > "$OUT/post-$id.html"
  mod=$(remote "wp post get $id --field=post_modified_gmt")
  printf 'post\t%s\t%s\t%s\n' "$id" "$mod" "$(shasum -a 256 < "$OUT/post-$id.html" | cut -c1-16)" >> "$OUT/manifest.tsv"
done
for o in $SNAP_OPTIONS; do
  remote "wp option get $o --format=json" > "$OUT/option-$o.json"
  printf 'option\t%s\t-\t%s\n' "$o" "$(shasum -a 256 < "$OUT/option-$o.json" | cut -c1-16)" >> "$OUT/manifest.tsv"
done
echo "$PROFILE" > "$OUT/profile"; date -u +%FT%TZ > "$OUT/taken-at"
echo "$OUT"
