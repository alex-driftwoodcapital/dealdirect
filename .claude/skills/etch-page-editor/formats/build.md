# Etch page builder (superseded: see `skills/etch-builder`)
The pipeline, templates, fill script and proven-types list now live in `etch-builder`. Kept for history.
Load `etch-expert` first (native syntax, structure) and `acss-expert` for styling.
One job: create new pages/components so they stay editable in the Etch builder. Status: from-scratch builds over SSH are NOT yet proven; the first one is a pilot on a single page. Editing existing pages is `etch-page-editor`; styling is `acss-expert`; run discipline is the run protocol in `etch-page-editor`.

## Method
1. Copy markup from an existing valid Etch page or component; never hand-invent block structure.
2. Prefer native Etch components, loops and CPT queries (service, project, problem, faq in SCF) over raw HTML blobs. Raw HTML/JS only when Etch has no way (WPCodeBox last).
3. Style via `acss-expert` rules (ACSS variables/utilities and existing classes first).
4. Write to staging (https://wordpress-1077248-6717515.cloudwaysapps.com), same backup/re-read/purge/verify method as `etch-page-editor`.

## Validation gate (once per new page)
Open it in the Etch builder on staging: it must render as editable structure (no raw-HTML blocks, no errors). Save with no changes, re-diff `post_content` against the pre-save copy, re-check at 375 and 1440. Any drift = fix the generator, not the page. After the first pass, record "proven" here; build more only after the pilot.

## Rules
If the page needs animation or effects, follow `art-director` (`reference/site-motion.md`) first.
Copy and design rules from `site-profile.md` apply. Go-live needs Alex's own typed words.

## Pilot result (2026-10-07)
Fixture-derived markup written to `post_content` PASSED the builder gate with benign drift (builder adds `styles` IDs for classes, creates a style record per `id`, normalizes whitespace). See `etch-expert/reference/fixtures/PILOT.md`. Generators should emit `styles` IDs and diffs should ignore whitespace between blocks. Loops, dynamic images, scripts and conditions are not yet proven.
