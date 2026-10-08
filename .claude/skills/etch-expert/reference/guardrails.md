# Etch guardrails (load first)

Every Etch run (`etch-expert`, `etch-builder`, `etch-page-editor`) reads this file before anything else. One line per rule: DO / DO NOT, then the source.
Pinned: Etch 1.6.8, ACSS 4.0.1, WP 7.1.3 (verified on a previous build's staging, TwoEleven; re-check DealDirect's versions with `etch-page-editor/scripts/ssh-setup.sh --check`). Docs re-read 2026-10-07; every docs path below was checked against the docs.etchwp.com sitemap that day.

Sources: **D** = official docs, `https://docs.etchwp.com` + the path shown. **S** = staging finding (`confirmed-on-staging.md`, `fixtures/PILOT.md`, `etch-build/parity-audit.md`). **P** = project rule (project memory, skills).
When docs and staging disagree, staging wins for this site and the mismatch goes in `confirmed-on-staging.md`. Lint column: **L** = `etch-page-editor/scripts/lint.py` checks it, **C** = `etch-builder/scripts/spec-check.py` checks it at the design-spec stage, blank = judgement or a staging test.

## 1. Process
| Rule | Source | Check |
|---|---|---|
| DO work on staging first; live, publish, delete or DNS only on Alex's own typed words. | P | |
| DO snapshot and re-read the current value before any edit; merge, never overwrite. | P (`etch-page-editor`) | |
| DO NOT write to a page while a builder tab is open on it: a builder Save overwrites direct edits. One writer per page. | S | |
| DO run the builder round-trip gate (open, Save with no edits, re-read, diff) once per new pattern signature; drift means fix the generator, not the page. | S `fixtures/PILOT.md` | |
| DO cite the docs page for every Etch construct you use; never hand-invent Etch markup or dynamic-data syntax. Copy forms from the docs or `fixtures/`. | P, D `/getting-started/core-principles` | |
| DO build in Etch only; the block editor is for client content edits (Etch authors custom blocks clients edit there). | D `/gutenberg/block-authoring` | |
| DO NOT build from a design without a design spec that passes `spec-check.py`; missing data stops the build, it is never filled by taste. | P (`etch-builder/formats/design-spec.md`) | C |
| Public API: DO use feature detection (`etch.environment.capabilities`, `blockTypes`), never version checks; the contract is 0.x experimental. | D `/public-api` | |
| Connector: DO keep exactly one connected builder tab per site; read `etch-connector --help` before scripting. | D `/etch-connector/usage`, `/etch-connector/cli-reference` | |
| Connector: DO treat safe mode as a guardrail, not a vault; run only our own scripts. | D `/etch-connector/security` | |
| DO check the installed version and feature flags before relying on a feature (`/wp-content/uploads/etch/flags.user.json`). | D `/feature-flags` | |
| DO rerun the round-trip gate and pattern regression after an Etch or ACSS update. | S | |

## 2. Structure and semantics
| Rule | Source | Check |
|---|---|---|
| DO use Section > Container for every top-level band; Etch adds the container width, centring and flex column. Several containers per section are fine (intro + grid). | D `/elements/section`, `/elements/container` | L (warn) |
| DO start every section with a heading: the first section on the page has the h1, all others start with an h2. No heading means it is a div, not a section. | D `/elements/section` ("Always include a heading") | C |
| DO keep one h1 per page and never skip heading levels (h1 → h2 → h3). | D `/elements/section` (Accessibility), `/elements/heading` | C, L (warn >1 h1) |
| DO use an anchor to navigate (another page or another part of the page) and a `<button>` for on-page actions (dialog, carousel, toggle). A link that looks like a button is a CSS job. Remove link attributes when turning an anchor into a button. | D `/elements/anchor` ("Buttons vs Links") | C |
| DO use the dynamic element (`tag={props.headingLevel}`) when a component's heading level must change, instead of conditions. | D `/elements/element` | |
| DO keep text inside `etch/text` within an element. | D `/elements/text` | L |
| DO loop the `li`, not the card inside it. | D `/loops/basic-loops` | |
| DO give every block a meaningful `metadata.name` (it is what Alex and the client see in the structure panel). | S | L (warn) |
| DO put rich text that comes from data in a div parent via the HTML element; never `unsafe="true"` (off on staging). | D `/elements/html`, S | L |
| DO NOT nest sections or containers without a layout reason. | D `/elements/section`, `/elements/container` | |
| DO use real landmarks: header, main (template), footer, nav with a label; dialogs as `<dialog>` with a labelled heading and a real close button. | D `/elements/element`, S parity audit (dialog close, header) | C (states) |
| Forms: DO use a plain semantic form (label per field, `name`, error text, `role="status" aria-live`) posting to the site's existing endpoint; no native WP form element is documented. | D `/studio/forms` (pattern only), P | |

## 3. Images, icons, media
| Rule | Source | Check |
|---|---|---|
| DO use the Dynamic Image element by WordPress media ID (it renders srcset/sizes); never a plain `img`, never a hard-coded upload URL. | D `/elements/dynamic-image`, S | L, C |
| DO give every image alt text (from the library or set explicitly); empty alt only when the spec marks it decorative. | D `/elements/image` | C |
| DO set `loading="eager"` only on the above-the-fold image; everything else lazy. | D `/elements/image` | C (warn) |
| DO set `aspect-ratio` + `object-fit` for media whose box must hold its shape. | D `/responsive-development/intrinsic-responsiveness` | |
| DO use the SVG element (`src`, `stripColors="true"` → `currentColor`) for icons that take theme colour. | D `/elements/svg` | |
| DO keep media in Asset Manager collections (Brand, Clients, Work, Insights, Video, Docs), not Uncategorized. | D `/interface/asset-manager`, P | |

## 4. Styling
| Rule | Source | Check |
|---|---|---|
| DO style at element level (attached CSS on the element's selector); no new stylesheets, no global CSS, no `<style>`, no `@import`. | D `/interface/css-panel`, P | L + `acss-expert verify.py` |
| DO pick in this order: ACSS variables and utilities, existing site classes, nesting on an existing class, a new class last. | P (`etch-expert` SKILL) | |
| DO verify every ACSS name with `acss-expert/scripts/verify.py` (or `lookup.py`); unknown or 3.x names block the save. | P | C (tokens), `verify.py` |
| DO write `styles` IDs explicitly next to each class (Path A, WP-CLI), or attach via `etch.styles.create` + `blocks.addClass` (Path B, API). | S `confirmed-on-staging.md` | L (warn) |
| DO add classes via the Attributes Bar or the API, not by typing in the HTML panel (debounced parser creates partial selectors). | D `/known-issues` ("Partial selectors"), `/interface/attributes-bar` | |
| DO use nesting and BEM stemming (`&__el`, `&--mod`) and parent context (`.parent & {}`); complex selectors go in braces `{.hero h1}`. | D `/interface/css-panel`, `/interface/selector-pills` | |
| DO change container width with `--content-width`, not `max-width` on the container. | D `/elements/container`, `/how-to/basics/how-to-set-content-width` | |
| DO NOT add an `id` only for styling: the builder can create a style record per `id`. Use ids for anchors and `aria-labelledby` only. | S `confirmed-on-staging.md` | |
| DO NOT use inline `style` except prop-driven tokens (`style="--card-bg: {props.bg}"`). | D `/components/creating-component-variations` | L (warn) |
| DO use recipes (`?auto-grid`, `?grid-1-2`, `?flex-column`, `?center-all`) only when the expansion passes `verify.py`; prefer ACSS tokens inside. | D `/utilities/recipes/grid-recipes`, `/utilities/recipes/flex-recipes` | |
| DO NOT turn on `@custom-media` (it creates a global "Custom Media Definitions" stylesheet, against the no-stylesheet rule) unless Alex says so; use literal `to-rem()` values. | D `/responsive-development/custom-media`, P (plan §10) | |
| Surfaces: neighbours never share a non-Paper surface; at most one Butter and one Blue band per page; separate sections by a surface change, not lines. | P (`art-director`) | C |

## 5. Responsive
Detail and examples: `responsive.md`. Building blocks: `primitives.md`.

| Rule | Source | Check |
|---|---|---|
| DO go intrinsic first: ACSS fluid type and space, auto-fit grids, `aspect-ratio`, `object-fit`, flex-wrap, `min()`/`clamp()`. | D `/responsive-development/intrinsic-responsiveness` | |
| DO use container queries for components, with the Has Me selector `:has(> &) { container-type: inline-size; }` added before the first `@container`. | D `/responsive-development/container-queries` | |
| DO use media queries only for viewport concerns: top-level page layout, `hover`, `prefers-reduced-motion`, print. | D `/responsive-development/using-media-queries` | |
| DO write mobile-first base styles, range syntax `(width >= 640px)`, and `to-rem()` for query values. | D `/responsive-development/workflow`, `/utilities/functions` | |
| DO NOT invent site-wide breakpoints: each component changes where its content needs it. The spec states responsive intent, not breakpoints. | D `/responsive-development/philosophy` | C |
| DO check 375 and 1440 (plus 768 when the layout changes between) with no horizontal overflow before calling a page done. | P (plan §6), S parity audit | |

## 6. Components, props, slots
| Rule | Source | Check |
|---|---|---|
| DO reuse an existing component (by `ref`) before making one; make one only when the design repeats a block 2+ times or the spec says so. | P (plan §6), D `/components/intro-components` | C |
| DO make variations with props on one component (boolean + condition, select + data attribute, inline tokens); never duplicate a component per variant. | D `/components/creating-component-variations` | |
| DO pass outside data in through props (`{item.title}` as a prop value); a component cannot read loop or template keys from outside. | D `/components/using-a-component-dynamic` | |
| DO NOT use `{props.*}` outside a component definition. | S | L (warn) |
| DO write select prop options as `label : value` with the spaces. | D `/components/props/prop-select` | |
| DO NOT put extra braces inside `{#loop}` / `{#if}` (`{#loop props.items as item}`); loop and repeater prop keys camelCase or bracket notation. | D `/components/mapping-component-props`, `/components/props/prop-loop` | |
| DO use slots for free-form content (`{@slot name}` in the definition, `{#slot name}` on the instance) and `slots.name.empty` for fallbacks and to drop empty wrappers. Slot content cannot see a loop inside the component: put the component inside the loop with an object prop instead. | D `/components/slots` | |
| The component prop schema is closed: setting an undeclared prop through the API throws `INVALID_ARGUMENT`. | D `/public-api/blocks` | |
| Native components: only Basic Nav (+ Burger) and Off Canvas have real docs (paste JSON from the docs page); the other listed native components are stubs, do not rely on them. | D `/components-native/overview` | |

## 7. Loops, conditions, dynamic data
| Rule | Source | Check |
|---|---|---|
| DO give nested loops different item names: an inner loop with the parent's name hides the outer one completely. | D `/loops/nested-loops` (note) | C |
| DO pass the parent's id into a nested loop (`{#loop posts($cat: category.id) as post}`). | D `/loops/nested-loops` | |
| DO reuse one saved loop with arguments (`$count ?? 10`; the first default wins) instead of cloning loops. | D `/loops/loop-arguments` | |
| DO quote string args at call time (`$taxonomy: "category"`) and pass arrays where WP expects arrays (`post__not_in`, `terms`). | D `/loops/loop-arguments` | |
| DO use the Main Query loop only on archive and search templates. | D `/loops/main-query` | |
| DO name the data source and item of every loop in the spec. | P | C |
| DO use strict comparisons by default, quotes only around strings, `!`, `&&`, `\|\|`, parentheses; inside attributes use comparison modifiers, not `{#if}`. | D `/conditional-logic/basic-conditions`, `/conditional-logic/advanced-conditions`, `/dynamic-data/dynamic-data-modifiers/comparison-modifiers` | |
| DO NOT rely on `{#else}` until it is confirmed on staging (not in the docs pages, not seen in saved markup). | S | |
| DO "no results" with the documented workaround (a second loop on `.length().equal(0,[1],[])`). | D `/loops/basic-loops` | |
| DO keep data we depend on in SCF; Etch CPTs and custom fields are a proof of concept. | D `/known-issues`, P | |

## 8. Templates
| Rule | Source | Check |
|---|---|---|
| DO shape templates as header component + `main` + `{@post-content}` + footer component; pull Gutenberg content with `{@post-content}`, not `{this.content}` (inside `main` on the index template, `article` on single posts). | D `/templates/index-template-catch-all`, `/templates/post-content-slot`, S `fixtures/parts/template-home.html` | |
| DO test header, nav, footer and template changes on a test page or test template first: they are site-wide. | P (plan §8 L7) | |

## 9. Scripts and motion
| Rule | Source | Check |
|---|---|---|
| DO keep JS small and scoped: a block script is enqueued in `<head>` as a deferred module with no link to its element, so target by selector, scope to the component, no globals, no scroll-jacking. | D `/public-api/blocks` (Block scripts), S | |
| DO NOT use inline event handlers (`onclick=`). | S | L |
| DO follow `art-director/reference/site-motion.md` for motion and honour `prefers-reduced-motion`. | P, D `/responsive-development/using-media-queries` | C (motion field) |

## 10. Safety
| Rule | Source | Check |
|---|---|---|
| DO NOT put secrets in pages: endpoints and keys in markup are public. | D `/studio/forms`, P | |
| DO escape or avoid echoing visitor input (`{url.parameter.*}`) into attributes until Etch's escaping is confirmed on staging. | P (security audit open question) | |
| DO NOT delete, publish or change DNS without Alex's typed words; restore from the snapshot if a write goes wrong. | P | |

## Known doc gaps (as of 2026-10-07)
Block JSON storage format, JS panel page (stub), `{#else}`, most native components, iframe, author template, recipe expansions beyond a few. Fixtures in `fixtures/` are the reference for storage; anything else is tested on staging and logged in `confirmed-on-staging.md`.
