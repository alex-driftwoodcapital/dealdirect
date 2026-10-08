# Site profile: Driftwood DealDirect (the only site-specific file for this skill)
Machine-read copy: `profiles/dealdirect-staging.env` (SSH target, WP path, purge command, protected IDs, pinned versions). To use another site or host, add `profiles/<site>.env` and set `ETCH_PROFILE`.

| Item | Value |
|---|---|
| Host | Cloudways (SSH port 22, WP-CLI preinstalled) |
| Staging | https://wordpress-1077248-6717515.cloudwaysapps.com (Cloudways temporary URL; `blog_public` was 1 on 2026-10-08, i.e. search engines allowed: set to 0 on Alex's OK) |
| SSH | `master_peedmrgrfq@66.42.75.99` port 22 (Cloudways Master Credentials); key `~/.ssh/dealdirect_staging` (cloud sessions: written from the `ETCH_SSH_KEY` secret by `scripts/ssh-setup.sh`) |
| WP path | `applications/kyvvrceayg/public_html` (under the master user's home) |
| Live | TBD (domain not mapped yet). Writes need Alex's own typed words |
| Pinned versions (2026-10-08) | WordPress 7.1.3, Etch 1.6.8, ACSS 4.0.1, etch-theme 0.0.3 (same as the versions the reference docs were verified on) |
| Cache purge | `wp cache flush; wp breeze purge --cache=all` (Breeze; Varnish purged through Breeze when enabled) |
| Protected (no restore/overwrite without typed OK) | TBD: header, footer and templates once they exist |
| Page IDs (staging, 2026-10-08) | Home 48 (published), Privacy Policy 3 (draft) |
| Stored in | `post_content` (blocks), `etch_styles`, `etch_global_stylesheets`, `etch_loops`; element scripts are base64 |

## DealDirect rules while editing
Full list: repo root `CLAUDE.md` (wins) and `handoff/README.md`. The short version:
- Copy verbatim from the live page or design file; never rewrite. Never "shovel-ready" (Riverside Wharf is under construction).
- Permalinks and anchor IDs frozen (`handoff/docs/permalinks.md`). Offering anchors: `#metrics #overview #webinar #partners #offering #structure #assets #market #rationale #legal`.
- Plus Jakarta Sans only. Navy `#0B2B48`, ocean `#2468A8`, `#6FB0E0` on dark. No gold, no emoji, no coloured left-border cards, no accent rules above headings.
- CTAs: "Start Investing" (registration), "Request Investor Details" (offering pages, opens `#request` on the same page), "Connect with an EB-5 Specialist" (EB-5).
- Legal/footnotes >= 12px, >= 4.5:1, one column at full content width. Every section keeps its disclaimer.
- Dark `cover-bg` field only for hero, Get started band, footer; never two dark sections in a row.
- Motion 160 to 480ms `cubic-bezier(.2,.7,.2,1)`; honour `prefers-reduced-motion` (no autoplay video, no transitions).
