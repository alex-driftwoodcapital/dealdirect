# Responsive in Etch (container-query first)

How every Etch layout adapts. Read `guardrails.md` first; tokens and fluid scales come from `acss-expert`. Docs: `https://docs.etchwp.com` + path, re-read 2026-10-07 (Etch 1.6.8).

## The order to reach for
1. **Intrinsic, no query** (D `/responsive-development/intrinsic-responsiveness`). Etch says use queries only for what cannot be handled intrinsically.
   - Fluid type and space: ACSS tokens (`--h1`, `--text-m`, `--space-*`, `--section-space-*`) are already `clamp()`-based. Never write a query that only changes a font size or a gap.
   - Variable grids: `grid-template-columns: repeat(auto-fit, minmax(min(100%, 22rem), 1fr))` (auto-fit collapses empty tracks; the `min(100%, …)` stops overflow on phones).
   - Flex-wrap for rows of buttons, chips, logos.
   - `min()`, `max()`, `clamp()` for widths (`inline-size: min(60ch, 100%)`), `ch` for measure, `em` for padding that scales with text.
   - `aspect-ratio` + `object-fit` for media; `dvh` (not `vh`) for full-height heroes.
2. **Container query** for anything a component does as its space changes (D `/responsive-development/container-queries`):
   ```css
   .split {
     display: grid;
     gap: var(--space-l);
     :has(> &) { container-type: inline-size; }   /* Has Me: the parent becomes the container */
     @container (width >= to-rem(720px)) {
       grid-template-columns: 7fr 5fr;
     }
   }
   ```
   Add the Has Me block before the first `@container`. It travels with the component, so the component works in any parent. A named container on a specific parent (`container: sec / inline-size`) is fine when a section must measure its own container, as `.home-leaks` does.
3. **Media query** only for viewport concerns (D `/responsive-development/using-media-queries`): top-level page layout, showing or hiding global UI (the phone menu button), `hover: hover`, `prefers-reduced-motion`, `prefers-color-scheme`, `print`, orientation.

Decision line from the docs: "Does this style depend on the viewport, or on the space available to the component?" Viewport → media query. Space → container query.

## Writing queries
- Mobile-first: base styles are the narrow layout; queries add complexity with `>=` (D `/responsive-development/workflow`).
- Range syntax: `(width >= 600px)`, `(400px <= width <= 800px)` (D `/responsive-development/using-media-queries`).
- `to-rem(800px)` → `50rem` on the front end, pixels in the editor; base 16px (D `/utilities/functions`). Use it for query values.
- Pick the value where the content breaks, not a device size. There are no global breakpoints in Etch (D `/responsive-development/philosophy`, `/interface/responsive-controls`). In the builder, drag the canvas to the break and let the responsive controls insert the query with the element's measurement.
- `@custom-media` tokens exist (since 1.2.0) but create a global "Custom Media Definitions" stylesheet behind an experimental toggle (D `/responsive-development/custom-media`). Off for this project unless Alex turns it on. Compound `and` conditions do not work with custom-media tokens.

## In the design spec
`responsive:` lines state intent in this shape: what changes + at what container (or viewport) width + why. Examples:
- "cards go from stacked to 2 columns when the grid container is at least 40rem"
- "logo max width grows to 220px from a 48em viewport (top-level band)"
- "intrinsic only (auto-fit grid)"
The builder turns each line into intrinsic CSS or one query. A line that names a device ("tablet") or a site-wide breakpoint gets a warning from `spec-check.py`.

## Checking
- Preview at 375 and 1440 (plus 768 when the layout changes between) with no horizontal overflow; drag the canvas through the range in the builder for anything new.
- Reduced motion: every animation has a `prefers-reduced-motion: reduce` branch (D `/responsive-development/using-media-queries`).
- Phone header and menu are site-wide (header part): test changes on a test page first (parity audit rows 16-19).

## Staging examples (real, saved)
- `.home-leaks`: named section container, then `@container sec (max-width: 836px)` → one column. Works; the newer form is mobile-first `>=`.
- `.home-reach`: `container-type: inline-size` on the section, `@container (min-width: 760px)` widens the intro measure.
- `.home-guide`: viewport `@media (width >= 56em)` for a top-level two-column split (acceptable: page-level layout).
- `.home-solutions`, `.home-contact`: intrinsic auto-fit grids with `minmax(min(100%, 22rem), 1fr)`, no queries.
(Source: `fixtures/styles-used.json`.)
