---
name: "etch-builder"
description: "Build NEW Etch pages from proven fixture templates: fill from a small page spec, lint, write to staging as a draft, verify. Use for new pages or sections; edits to existing pages use etch-page-editor."
---

# Etch builder
Load `etch-expert/reference/guardrails.md` first, then `etch-expert` (syntax; official docs at docs.etchwp.com, cite them) and `acss-expert` (styling). Edits to EXISTING pages: `etch-page-editor`. Staging only; live needs Alex's own typed words.

## Pipeline
**Design-driven work starts with a design spec** (`formats/design-spec.md`, written by `art-director:etch-design-spec`): `python3 -I scripts/spec-check.py page.yaml` must print 0 errors before step 0; on errors, stop and list the missing data, never fill it by taste. Example: `examples/home-v117/`. Tests: `scripts/spec-check-tests/run.py`.
0. **Styles first** (new classes only): acss-expert style spec (`examples/pricing-e2e/style-spec.md`), `python3 -I acss-expert/scripts/verify.py file.css` must print 0 errors, then `add-styles.py records.json --yes`. Reuse existing class records and their IDs (e.g. `.btn--secondary` = `lbdxk83`, `.bg--ultra-light` = `yjhyf3h`): the builder adds those IDs on save, so templates must already carry them.
1. **Page spec**: a small JSON (`scripts/fill.py` header shows the shape): a list of sections, each a proven type.
2. **Fill**: `python3 scripts/fill.py spec.json > content.html`. Only types with a template in `templates/` are supported. Anything else: copy markup from `etch-expert/reference/fixtures/`, never hand-invent blocks.
3. **Lint**: `scripts/lint-acss.sh <snapshot_dir> content.html` (runs `acss-expert/scripts/verify.py` when present, so wrong/removed ACSS names block, then `lint.py`; see `etch-page-editor/scripts/lint.md`).
4. **Write + verify**: `RUN_YES=1 etch-page-editor/scripts/edit-run.sh --new "<title>" <slug> content.html` (snapshot, lint, create DRAFT, purge, diff). Later edits: `edit-run.sh <post_id> content.html --expect-sha <sha from a fresh snapshot> --verify <url>`. Drafts are not publicly viewable: publish only on Alex's word, then run `etch-page-editor/scripts/verify/verify.mjs` at 375/1440.
5. **Builder gate** (once per new section type): open `/?etch=magic&post_id=<id>`, Save with no changes, re-read `post_content`; expected drift is only what `etch-expert/reference/fixtures/PILOT.md` lists. Then mark the type proven below.

## Proven section types (round-trip checked)
- `page-hero`: component instance (ref 176), pilot 2026-10-07.
- `band`: section > container > row > copy (kicker, h2, sub), classes `newsletter-band*` with style IDs written explicitly, pilot 2026-10-07 (the generated template includes style IDs, so it should not drift; re-run the gate if it does).
- `callout-band`: component instance (ref 143, tones ink|butter|blue). Round-trip 2026-10-07 (generator test page): builder only added the empty `slot-content` `extra`, now written by the template.
- `plan-grid`: section > container > h2 + `ul.plan-grid` of three `li.plan-card` (name, price, description, `.btn--secondary` link). Needs 5 new class records first (`examples/pricing-e2e/new-styles.json`, added with `etch-page-editor/scripts/add-styles.py`). Round-trip 2026-10-07: only drift is a style record for the h2 `id` (`#<id>-heading`), a benign placeholder; delete it with the page.
Not proven: loops, dynamic images, conditions, scripts, forms.

## Rules
Copy and brand rules: `etch-page-editor/site-profile.md`. Motion: `art-director` (`reference/site-motion.md`). Section structure (section > one container div), images (`etch/dynamic-image` by media ID) and class handling per the Etch connector guide are enforced by lint.
