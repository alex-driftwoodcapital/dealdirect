# Round-trip pilot result (2026-10-07, Etch 1.6.8, TwoEleven staging)

**Verdict: PASS with benign drift.** Fixture-derived markup written straight to `post_content` loaded in the builder as editable structure (tree showed the Page hero component and the section with its children, no raw-HTML blocks, no errors, canvas rendered correctly). Saving once with no edits kept every block, attribute, text and prop intact.

Test page: draft page 474 "ZZ Etch round-trip pilot (delete me)", built from the Page hero instance (`pages/work.html`) and the section from `components/newsletter-band.html` (props placeholder removed). Written by WP-CLI, opened via `/?etch=magic&post_id=474`, saved with the builder Save button, then `post_content` re-read.

## What the builder changed on save (drift)
1. **Adds `styles` IDs for classes.** Elements written with only `attributes.class` (no `styles`) came back with `"styles":["<id>"]`, one per class that has a record in `etch_styles` (e.g. `.newsletter-band__row` → `z7by2wo`). Fix in a generator: emit `styles` yourself by looking up class → style ID in `etch_styles`.
2. **Creates a style record for an element `id`.** `id="pilot-heading"` produced an `#pilot-heading` record (`dk67r38`) in `etch_styles` and linked it. Expect one stray record per authored `id` attribute; clean up when deleting a test page.
3. **Whitespace between blocks is normalized** (blank lines / newlines around block comments). A diff script must ignore whitespace between block comments.
4. Nothing else changed: tags, `metadata.name`, `data-etch-element`, aria attributes, component `ref` and props, text content all identical.

## Other findings
- `etch_db_version` moved to 1.6.8 after the first admin/builder load (the migration runs then, not on plugin update).
- Fixture component definitions contain `{props.x}` expressions (e.g. `data-surface="{props.surface}"`); these are only valid inside the component definition, so strip or fill them when using such markup on a page.
- Builder reached via the wp-admin "Edit with Etch" link (`/?etch=magic&post_id=<id>`), needs a logged-in browser. The connector bridge (`etch-connector tabs`) showed no connected builder tab, so this pilot saved with the builder's Save button and was verified over WP-CLI instead of through `etch.*`.
- Not tested: a page with loops, dynamic images, scripts or conditions; save after an edit; frontend render of a published page at 375/1440 (the draft was checked only in the builder canvas).

## Docs read (docs.etchwp.com)
`/public-api`: `window.etch`, namespaces blocks/styles/loops need `etch.saveAsync()`, components/stylesheets/fields persist immediately; contract is 0.x experimental. `/etch-connector/ai-agent-guide`: scripts run as async functions via `etch-connector eval`; safe mode, no `window`/`document`. The connector `--help` adds: classes are the read-only `styles` array (authored `attributes.class` is dropped by `blocks.create()`), images use `etch/dynamic-image` with a Media prop, sections wrap one `data-etch-element="container"`.
