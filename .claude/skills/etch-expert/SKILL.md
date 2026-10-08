---
name: "etch-expert"
description: "Expert on Etch (WordPress builder): native elements, components, loops, dynamic data, conditions, and best-in-class HTML, CSS (nesting, chaining) and JavaScript inside Etch. Rules and syntax only; edits go through etch-page-editor; new pages through etch-builder."
---

# Etch expert
One job: the right way to do it in Etch. Load before any `etch-page-editor` or `etch-builder` work. Writes nothing. ACSS names and tokens: `acss-expert`.

## How to work
0. **Load `reference/guardrails.md` first, every run**: the complete DO / DO NOT list with the official docs page (or staging finding) behind each rule. Cite those pages in your output. For layout work also load `reference/primitives.md` (every building block: stored form, API form, rules, staging status) and `reference/responsive.md` (container-query first).
1. Load only the reference files you need from `reference/` (copied from docs.etchwp.com, dated): `principles.md`, `elements-and-html.md`, `styles-and-css.md` (classes, nesting, chaining, responsive, functions), `javascript.md`, `components.md`, `templates-dynamic-loops.md` (templates, dynamic data, loops, conditions, facets), `api-connector-integrations.md`, `howto-and-gotchas.md`, `troubleshooting.md`.
2. Native first: elements, components, loops, CPT queries and conditions before raw HTML; raw HTML/JS only when Etch has no way (WPCodeBox last resort). Semantic HTML: rules in `reference/semantic-html.md` (landmarks, headings in order, lists, real buttons and links, alt, labels).
3. CSS: ACSS variables/utilities first (`acss-expert`), then existing classes, then nesting/chaining on an existing class, new class last; follow the exact syntax in `styles-and-css.md`.
4. JavaScript: small, scoped to the element/component, no globals, no scroll-jacking; follow `javascript.md` for how Etch stores and loads scripts.
5. Syntax rule: copy forms from the reference or from an existing valid Etch page; never hand-invent Etch markup or dynamic-data syntax. If unsure, test on staging and read back how Etch stored it.
6. Check the installed Etch version and feature flags against `howto-and-gotchas.md` before relying on a feature.

## Data modeling (assets, fields, CPTs)
Load `reference/data-modeling.md` before creating a CPT, field or asset collection.
- Organize media in Asset Manager collections (Brand, Clients, Work, Insights, Video, Docs); never dump into Uncategorized.
- SCF for anything we depend on (repeaters, relationships, options); Etch custom fields only for simple one-off scalars.
- New CPT only if entries need their own page, grow over time, or are reused/filtered in 2+ places; otherwise repeater (or options/taxonomy/props).
- Every CPT gets a real `menu_icon` (dashicon or base64 SVG) and `menu_position`, never the default.

## Official docs first
Always check and cite docs.etchwp.com for the installed version (Etch pinned 1.6.8, 2026-10-07; the reference copies below were verified 2026-10-02, re-read parts 2026-10-07). When docs and staging disagree, record it in `reference/confirmed-on-staging.md`. Known-good markup to copy: `reference/fixtures/` (README, `catalogue.md`, pilot result `PILOT.md`).

## Known gaps in the docs (as of 2026-10-07)
- The block JSON storage format and the JS panel page are not documented (JS panel is an empty stub: block scripts enqueue in `<head>` as deferred modules, no runtime link to the element, target by selector). Fixtures cover the format; test any script on staging.
- `{#else}` appears only as a docs tip, never in the conditional-logic pages: still unconfirmed. Condition operators ARE documented (`&&`, `||`, `==`, `!=`, `===`, `!==`). Native facets, most native components, iframe and author-template are "coming soon".
- Utility recipe expansions are mostly undocumented beyond `?flex-column`, `?grid-3`, `?auto-grid`.
- Settled by staging tests: see `reference/confirmed-on-staging.md`.

## Standing site rules
Saving the same page in the builder overwrites direct edits. Staging first (wordpress-1077248-6717515.cloudwaysapps.com). Interactive pieces untouched beyond approved copy fixes.

## Output
The exact structure or snippet, the reference file that confirms it, and anything that needs a staging test.
