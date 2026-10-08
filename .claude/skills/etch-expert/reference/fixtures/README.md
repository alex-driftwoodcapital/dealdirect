# Etch fixtures (known-good markup)

Real `post_content` exported read-only from TwoEleven **staging** (`alexg281.sg-host.com`) on 2026-10-07. Everything here already renders and round-trips in the builder on that site, so copy from it instead of hand-writing block markup.

## Versions (pin these in the site profile)

| Item | Version |
|---|---|
| Etch plugin | **1.6.8** (latest as of 2026-10-07; staging updated from 1.6.7 that day after a DB export to `~/backups/pre-etch-1.6.8-*.sql`). `etch_svg_version` 2. `etch_db_version` still read 1.6.7 right after the update (likely migrates on first admin load) |
| Automatic.css | 4.0.1 |
| Theme | etch-theme 0.0.3 |
| WordPress | 7.1.3 |
| PHP | 8.2.34 |
| SCF (secure-custom-fields) | 6.9.5 |

Re-exported after the 1.6.8 update: all 9 posts, the style records, and the global stylesheet are byte-identical to the 1.6.7 export, so the fixtures are valid on 1.6.8. Raw-HTML `unsafe` is off in staging Etch settings (`allow_raw_html_unsafe_usage:false`).

## Contents

| File | Source (staging post ID) | Why it is here |
|---|---|---|
| `pages/home.html` | page 48 Home | sections, interactive scripts, dynamic images, loops, component instances |
| `pages/work.html` | page 184 Work | loops over a CPT, conditions, `dynamic-image` bound to fields, raw-html |
| `pages/pricing.html` | page 181 Pricing | forms, fieldsets, radios, toggles (`aria-pressed`), dialogs |
| `parts/header.html` | wp_block 22 Header | menu components with `slot-content`, nested object props |
| `parts/footer.html` | wp_block 28 Footer | SVG (`svg`/`path`), nav lists, component instances |
| `parts/template-home.html` | wp_template 12 Home | the minimal template shape (`etch/element` main + `post-content`) |
| `components/page-hero.html` | wp_block 176 | component definition with props + `condition` blocks |
| `components/callout-band.html` | wp_block 143 | component with a `slot-placeholder` |
| `components/newsletter-band.html` | wp_block 457 | select prop (`{props.surface}`), button with two style IDs |
| `styles-used.json` | option `etch_styles` | the 61 style records referenced by `"styles":[...]` in the files above (IDs are the join key) |
| `loops-used.json` | option `etch_loops` | loops referenced (`prjfeat`, `prjmore`) |
| `global-stylesheets.json` | option `etch_global_stylesheets` | the site's global stylesheet(s) as stored |
| `catalogue.md` | derived | block types, attribute keys, patterns, and what is NOT covered |

Not exported: component prop schemas (`etch_component_properties` meta; a read of it was blocked this run), the license key/options, and anything from the live site.

## Using them

1. Pick the closest fixture, copy the block comments verbatim, change `content` strings and attribute values only.
2. Keep every `"styles":[...]` ID that points at a record in `styles-used.json`; a new class needs a new `etch_styles` record first (see `../styles-and-css.md`).
3. Never invent block types; use only those in `catalogue.md`.
4. Before writing any of this to a site, re-read the target and back it up (`etch-page-editor`). Fixtures are TwoEleven content: replace copy, IDs (`mediaId`, component `ref`) and class names for another site.

## Cross-check against official docs (docs.etchwp.com, 2026-10-07)

- The public docs do **not** document the block JSON storage format (the Gutenberg block-authoring page is conceptual only). These fixtures plus `catalogue.md` are therefore the source of truth for markup shape; re-verify on each Etch update.
- Conditions: docs list `&&`, `||`, `==`, `!=`, `===`, `!==` and `{#if}`; no else/elseif documented. Fixtures also use the builder operator `isTruthy`. `{#else}` stays unconfirmed.
- Loops: docs use `{#loop name as item}` (optional `, index`), matching the `loopId`/`itemId` block keys.
- Consistent with docs: component props as `{props.x}`, dynamic data as `{item.field}`.
- Still unread: Public API and Connector sub-pages (`/public-api`, `/etch-connector/usage`, `/etch-connector/ai-agent-guide`) hold the technical detail; read them in Thread 2.
