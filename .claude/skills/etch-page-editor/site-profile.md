# Site profile: Driftwood DealDirect (the only site-specific file for this skill)
Machine-read copy: `profiles/dealdirect-staging.env` (SSH target, WP path, purge command, protected IDs, pinned versions). To use another site or host, add `profiles/<site>.env` and set `ETCH_PROFILE`.

| Item | Value |
|---|---|
| Host | Cloudways (SSH port 22, WP-CLI preinstalled) |
| Staging | https://wordpress-1077248-6717515.cloudwaysapps.com (Cloudways temporary URL; keep noindex) |
| SSH | Cloudways Master Credentials user on the server Public IP; key `~/.ssh/dealdirect_staging` (cloud sessions: written from the `ETCH_SSH_KEY` secret by `scripts/ssh-setup.sh`) |
| WP path | `applications/<app folder>/public_html` under the master user's home: TBD |
| Live | TBD (domain not mapped yet). Writes need Alex's own typed words |
| Pinned versions | TBD: record from `scripts/ssh-setup.sh --check` on first connect |
| Cache purge | `wp cache flush; wp breeze purge --cache=all` (Breeze; Varnish purged through Breeze when enabled) |
| Protected (no restore/overwrite without typed OK) | TBD: header, footer and templates once they exist |
| Page IDs (staging) | TBD: fill after the first snapshot |
| Stored in | `post_content` (blocks), `etch_styles`, `etch_global_stylesheets`, `etch_loops`; element scripts are base64 |

## DealDirect rules while editing
TBD from the brand handoff: CTA label(s), button sizes, typefaces, colors, languages, copy rules. Until then, ask before inventing any brand rule; do not carry over another site's rules.
