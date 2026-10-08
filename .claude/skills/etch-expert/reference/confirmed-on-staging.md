# Confirmed on staging (previous build: TwoEleven, not DealDirect)
Etch behaviour findings carry over; IDs, refs and brand values below do not. Re-confirm on DealDirect staging before relying on a version-sensitive finding.
Things tested for real, not copied from docs. Newest first. Etch 1.6.8 / ACSS 4.0.1 unless noted. Add a line whenever a test settles a doc gap; remove a gap from `SKILL.md` when it lands here.

| Date | Confirmed | Evidence |
|---|---|---|
| 2026-10-07 | Hand/fixture-written block markup in `post_content` opens in the builder as editable structure and survives a no-edit Save. | `fixtures/PILOT.md` |
| 2026-10-07 | On save the builder adds `styles` IDs for classes that have a record, creates a style record for each element `id` attribute, and normalizes whitespace between blocks. | `fixtures/PILOT.md` |
| 2026-10-07 | `etch_db_version` migrates on the first builder/admin load after a plugin update, not on the update itself. | 1.6.7 to 1.6.8 update |
| 2026-10-07 | Etch 1.6.7 and 1.6.8 store the 9 fixture posts, the style records and the global stylesheet identically (no markup change between them). | byte comparison, fixtures README |
| 2026-10-07 | Block types in use: `etch/element, text, component, slot-content, slot-placeholder, condition, loop, dynamic-image, raw-html` plus core `post-content`. `unsafe` raw HTML is off in settings. | `fixtures/catalogue.md` |
| 2026-10-07 | Condition operators in saved markup: builder `isTruthy` and `\|\|`; docs list `&&`, `\|\|`, `==`, `!=`, `===`, `!==`. | catalogue, docs advanced-conditions |
| 2026-10-07 | Section skeleton (section > one container div, built-in style IDs) and `class` + `styles` pairing are how real pages are stored; `attributes.class` alone is accepted in `post_content` and gets its style IDs on save. | fixtures, pilot |
| 2026-10-07 | Generator test (hero + band + callout-band from `etch-builder` templates, written by `edit-run.sh`, saved in the builder with no edits): the only change was an empty `etch/slot-content` named `extra` added to the callout instance; no style-ID drift. The builder created one style record (`#<headingId>` of the component instance); the band's heading `id` produced none this time, so "one record per id" in PILOT.md is not universal. | generator test page 488 |
| 2026-10-07 | End to end (style spec, ACSS verify, add-styles, lint, `edit-run.sh --new`, builder Save, preview): a 3-section pricing page (hero, plan grid, callout) round-tripped with only one change, a style record for the h2 `id`. ACSS utility classes (`.btn--secondary`, `.bg--ultra-light`) already have empty placeholder records in `etch_styles`; the builder adds their IDs to `styles` on save. Preview at 375: 1 column, no horizontal overflow, 1 h1; wide: 3 columns. Staging `etch_styles` restored byte-identical afterward. | `etch-builder/examples/pricing-e2e` |
| 2026-10-07 | A class written with style IDs from the live `etch_styles` round-trips with no drift (templates in `etch-builder/templates`). | `etch-builder` end-to-end run (builder gate for it not re-run) |

## Docs facts re-read 2026-10-07 (docs.etchwp.com)
- Public API: `window.etch`; `blocks`/`styles`/`loops` buffers persist via `etch.saveAsync()`; `components`/`stylesheets`/`fields` persist immediately; contract 0.x experimental.
- Connector: scripts run as async functions in safe mode (no `window`/`document`); read `etch-connector --help` first.
- Loops: `{#loop name as item}` or `{#loop name as item, index}`; inline arrays allowed. Matches `loopId`/`itemId`.
- The block JSON storage format is NOT in the public docs; the fixtures are the reference.

## Still unconfirmed
- `{#else}` / else-if in conditions (not in docs, not seen in saved markup).
- Builder round-trip of loops, dynamic images, scripts and conditions from newly generated markup (existing fixtures contain them and already saved by the builder).
- Component prop schema JSON export; second-level Asset Manager nesting; script behaviour in the JS panel (docs page is a stub).
