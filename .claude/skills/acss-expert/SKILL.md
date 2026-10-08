---
name: "acss-expert"
description: "Expert on Automatic.css (ACSS) 4.x for every site build: styles things with exact verified variables, utilities and recipes, looks up names and values, audits CSS for unknown or 3.x names. Layers on top of the Etch builder; never creates stylesheets."
---

# ACSS 4 expert
One job: decide how something is styled with ACSS using only names that exist in the installed build, and hand a **style spec** to the Etch skills (`etch-builder`, `etch-page-editor`; they own structure and writing). This skill writes nothing to the site and never creates a stylesheet, global CSS or SCSS file: CSS lives at element level (class, nested block, attribute).

## Always first
1. Load the site profile: `index/site-profile.md` (TwoEleven staging) or fill `index/site-profile.template.md` for a new site (checklist: `reference/new-site-setup.md`). Brand and measured values live there; project memory wins over it.
2. The live build is the truth: `index/automatic.css`, `index/acss-settings.json`, `index/acss-index.json` (ACSS 4.0.1, rebuild with `scripts/build-index.py`). Docs pages are partly 3.x; `reference/staging-4.0.1-facts.md` lists what is absent and what to use instead.
3. Never use a name from memory. ACSS 4 is breakpoint-free and variable-first: no `.grid--N`, `.gap--`, `.pad--`, `.link--`, `.text--{color}` etc.

## Modes
| Mode | When | How |
|---|---|---|
| **Style** | "style / build this with ACSS" | Pick by `reference/best-practices.md` order (variable, build utility, site class, new class). Start from `reference/page-recipes.md` when a section type matches. Return a style spec (`formats/style-spec.md`), then run verify. |
| **Lookup** | "what is X / its value / is there a class for Y" | `python3 -I scripts/lookup.py NAME` (`-s` for substring). Cite the docs page it prints. Absent names return the replacement. |
| **Audit** | "review this CSS/markup" | `python3 -I scripts/verify.py FILE [--site-styles etch_styles.json]`. Report errors (unknown/3.x names, new stylesheets), warnings (hard-coded values that equal a token), then give fixes as a style spec. |

## Verify (blocking)
Before handing over CSS or markup: `python3 -I scripts/verify.py FILE` must end `0 error(s)`. Unknown ACSS names block the Etch save. Details and reuse from the Etch lint: `scripts/verify.md`. If it cannot be checked offline (`?recipes`, SCSS functions), say so in the spec notes.

## Reference (load only what the task needs)
`best-practices.md`, `page-recipes.md`, `new-site-setup.md`, `staging-4.0.1-facts.md`, then by topic: `colors.md`, `spacing.md`, `typography.md`, `dimension.md`, `layout.md`, `components.md` (buttons, cards, icons), `surfaces.md` (borders, shadows, effects, overlays), `accessibility.md`, `functions-mixins-recipes.md`, `setup-and-breakpoints.md`, `fundamentals.md`. Each file carries a dated 4.0.1 check note; `functions-mixins-recipes.md` and parts of `components.md` stay unconfirmed where the docs 404.

## Boundaries
- ACSS owns: which variable/utility/recipe, its real value, brand-to-token mapping, CSS audit.
- Etch owns: block structure, components, loops, dynamic data, where CSS is stored and how it is written (`etch_styles`, nesting syntax).
- Layering: Etch proposes structure, ACSS returns the style spec, Etch writes both. ACSS never changes structure; Etch never invents ACSS names.

## Output
Style spec (or lookup answer / audit report) with every ACSS name and its docs page, the verify result, and a plain note for anything unconfirmed.
