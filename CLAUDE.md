# DealDirect: Etch + ACSS 4 rebuild (standing instructions)

The design handoff is in `handoff/` (README, `design/`, `docs/`). Read `handoff/README.md` once before page work. Where the handoff and this file disagree, this file wins.

## Project values
- STAGING_URL: https://wordpress-1077248-6717515.cloudwaysapps.com/ (Cloudways; the handoff's `…6707404` is NOT the build target)
- LIVE_URL: https://driftwooddealdirect.com/ (WordPress + Bricks today). Read-only source of copy, media and SEO meta. Never write to it.
- SSH: `master_peedmrgrfq@66.42.75.99`, key `~/.ssh/dealdirect_staging`, WP path `applications/kyvvrceayg/public_html` (profile: `.claude/skills/etch-page-editor/profiles/dealdirect-staging.env`)
- Versions (2026-10-08): WordPress 7.1.3, Etch 1.6.8, ACSS 4.0.1, etch-theme 0.0.3
- PAGE_IDS (staging): Home 48, Privacy Policy 3 (draft). Fresh install: everything else is created by this build.
- TARGET_AUDIENCE: US accredited investors; EB-5 pages: foreign investors (EN/ES/PT)
- PRIMARY_CTA: "Start Investing" (registration) · offering pages "Request Investor Details" · EB-5 "Connect with an EB-5 Specialist"
- AUTHORIZED_SITE: staging only until Alex signs off in his own typed words.
- Staging pages are **published** on deploy (Alex, 2026-10-08: "publish the pages, not drafts"; staging sits behind Cloudways password protection). Each page's `META['status']` drives it. The live site still needs Alex's typed OK.
- HUBSPOT_PORTAL_ID: 2951523. Private app token: `DD_HUBSPOT_TOKEN` in staging `wp-config.php` only, never in the repo, Etch, JS or chat.
- GTM: `GTM-NX8DQZGQ`

## Where work runs
- **Staging deploys run in GitHub Actions** (`.github/workflows/staging.yml` → `ops/deploy-all.sh`): every PR gets a dry run against staging (the plan shows in the PR's checks), every merge to `main` deploys, and "Run workflow" (Actions tab, also from the GitHub app) deploys on demand. Secrets: `STAGING_SSH_KEY`, `STAGING_KNOWN_HOSTS`, optional `DD_HUBSPOT_TOKEN`.
- Cloud sessions cannot reach SSH, staging or the live site: they write specs, markup, CSS and code into this repo and open PRs. Alex merges (or says "merge"); the workflow deploys. The Mac Remote Control session is only needed for things Actions can't do (e.g. a builder check).
- Every write: snapshot first, re-read before editing, purge (`ops/deploy-all.sh` and the scripts it calls do this). Verify at 375 / 768 / 1440.

## Fresh install (differs from the handoff)
The handoff assumes staging is a copy of the Bricks site. It is not. So:
- The `offering` CPT (rewrite slug `offering`), its fields (`handoff/docs/cpt-schema.md`) and the platform-stats options page are **created**, not exported. Field plugin: Secure Custom Fields (installed on staging). The CPT, field groups and options page are registered in code by `dealdirect-core`, not in the SCF admin UI.
- Pages are created with the **same slugs** as live (`handoff/docs/permalinks.md`); "same post ID" does not apply.
- Media is imported from the live site's uploads (same filenames), not reused by attachment ID, and every image goes into an **Etch Asset Manager collection** (taxonomy `etch_collection`; never Uncategorized). Collections: Brand, EB-5, one per offering (e.g. Riverside Wharf), Prior Projects, Video, Docs. Each page's `MEDIA` gives `(source, collection)`; the build refuses an image without one. Images are compressed with the **Etch Asset Manager compression preset** (option `etch_compression_presets`; quality = 100 − compression, its format and resize), applied on the host by the deploy because Etch's own encoder runs in the browser. Sources stay originals (never pre-converted in the repo). If staging has no preset at all, the deploy creates the starting one from `ops/page/compression-preset.json` ("DealDirect site images": WebP, compression 25, long side 2560px, downscale only) through Etch's own route, so it shows and stays editable in the Asset Manager (Alex, 2026-10-08: no builder access, "keep building"); edits there win from then on. `COMPRESS_PRESET` in the staging profile picks one when several exist.
- Copy, SEO title/description/OG and anchor IDs are lifted from the live pages verbatim.

## Repo layout
- `handoff/`: the design handoff as received (do not edit except the override note in its README).
- `ops/`: deploy scripts, run by the Staging workflow or by hand (`ops/deploy-all.sh`: everything in order; `ops/inventory.sh`: Phase 1, read-only; `ops/deploy-core.sh`: deploys the plugin to staging; `ops/acss/apply.sh`: applies the DealDirect ACSS settings built by `ops/acss/build-settings.py`; all dry run by default).
- `wp-content/plugins/dealdirect-core/`: the site plugin (offering CPT + SCF fields, Platform stats options page, HubSpot proxy `dealdirect/v1`). Tests: `php tests/run.php` (+ `tests/README.md`).
- `site/`: page sources. `site/pages/<page>.py` (pages, plus the `site_header`/`site_footer`/`request_dialog` components and the `template_page` template; the request dialog sits in both templates and opens from `data-modal-open="registration"`/`"offering-request"`, `href="#request"` or `/#signup`; EB-5 pages (`eb5`, `eb5_new` = /new-eb-5-page/, later ES/PT) are built by `site/lib/eb5_page.py`; another language's design is read through `Aligned` (`site/lib/design.py`: the EN prefix picks the string at the same position in the ES/PT design); the EB-5 dialog (`eb5_dialog`, one component per language from `site/lib/eb5_form.py`) ends each EB-5 page and opens from `data-modal-open="eb5-register"`; both dialogs' classes live in the library sheet `site/styles/dialog.css`; `META` gives kind (page, offering, component, template), slug, status and deploy order; offerings are `offering` posts rendered by the `single-offering` template; their sections come from `site/lib/offering.py`, called with each page's own design copy; an offering's `META['fields']` sets its SCF card fields (Home cards; `{{media:slug}}` → attachment id; written with `update_field`, compared with stored meta, unknown fields refused); a page's `LOOPS` are Etch loop records (`etch_loops`) upserted before the page, used by `etch/loop` blocks (`Loop` in `site/lib/etch.py`); `COPY_SOURCE` names the design file that quoted literals in dynamic expressions and card field values must appear in verbatim) — structure; copy looked up from the design file, never retyped, `site/styles/<page>.css` (one rule per class = one Etch style record; classes used by more than one page live in the library sheets `site/styles/shared.css`, `offering.css` and `dialog.css`, picked by the page's `STYLESHEETS`, and a selector may live in one sheet only, so pages never overwrite each other's records; sections own their block padding, which overrides ACSS's default section padding, and containers only set width), `site/lib/` (block generator, copy lookup). `python3 -I site/build.py <page>` runs the copy gate and writes `build/<page>/` (gitignored); `python3 -I site/preview.py <page>` renders a local approximation for 375/768/1440 checks.
- `ops/page/deploy.py <page>`: writes a built page to staging (media import, style records, draft page via `edit-run.sh`); dry run by default, stops if the page was edited since the last deploy.
- `inventory/<date>/`: read-only exports of staging and the live site (copy, SEO meta, media list). Produced by Actions > **Inventory** (`.github/workflows/inventory.yml`, runs `ops/inventory.sh`) on the branch `inventory/<date>`, so cloud sessions can read it with `git fetch origin inventory/<date>`.
- `.claude/skills/`: the Etch/ACSS skills.

## Skills
Router: `website-helpers`. Load `etch-expert` and `acss-expert` before any page work. Edits: `etch-page-editor`. New pages: `etch-builder` (pilot gate first). Unsupervised runs: `site-build-runner`. Audits (read-only): `seo-geo-auditor`, `security-auditor`, `tracking-auditor`, `client-test-group`.
The fixtures, examples and ACSS index inside the skills come from a previous build (TwoEleven); never reuse their IDs, copy or brand values.

## Rules
1. **Copy is verbatim.** Lift text from the live page or the design file. Never rewrite, shorten or "fix" it. Known typos and conflicts are tracked in `handoff/design/evidence-register/claims.js`; compliance decides.
2. **Riverside Wharf is under construction.** Never carry over "shovel-ready", on any page or language.
3. **Permalinks and anchor IDs are frozen** (`handoff/docs/permalinks.md`).
4. **ACSS first.** Variables and utilities before custom CSS; verify every name exists on staging (`acss-expert` verify/lookup).
5. **BEM classes** as named in `handoff/docs/etch-components.md`.
6. Legal and footnote text: never below 12px or 4.5:1 contrast; one column at full content width. No section ships without its disclaimer block.
7. Forms: custom Etch UI → `POST /wp-json/dealdirect/v1/submit` → HubSpot Forms API v3 (`handoff/docs/hubspot-setup-steps.md`). Non-accredited visitors are never sent to HubSpot.
8. Platform figures come from the platform-stats options page (`handoff/docs/platform-stats.md`), never typed into a page.
9. Saving a page in the Etch builder overwrites SSH/WP-CLI edits: never mix on the same page without re-reading.
10. Compliance register: build with live figures as-is; every open `gap`/`check` must clear before go-live.

## Brand
Driftwood Capital design system (tokens in `handoff/README.md`, ACSS mapping in `handoff/docs/acss-mapping.md`). Plus Jakarta Sans only. Navy `#0B2B48` primary, ocean `#2468A8` accent, `#6FB0E0` accent on dark. No gold, no emoji, no coloured left-border cards, no accent rules above headings.

## Build phases (one PR each)
0 repo setup · 1 staging inventory + live content/media/SEO extraction · 2 ACSS settings + font · 3 global components · 4 EB-5 pilot (Alex reviews) · 5 offering template · 6 Home · 7 forms endpoint · 8 ES/PT EB-5 + /new-eb-5-page/ · 9 QA, crawl diff, compliance, go-live plan (Alex's typed OK).
