# Styles, CSS syntax, responsive, utilities

Sources: https://docs.etchwp.com/interface/{css-panel,attributes-bar,selector-pills,responsive-controls}, /responsive-development/{philosophy,workflow,container-queries,using-media-queries,custom-media,intrinsic-responsiveness}, /utilities/{functions,recipes/*}, /elements/{section,container}
Verified from docs 2026-10-02.
Etch pinned: 1.6.8 (staging, 2026-10-07). Staging-tested facts: `confirmed-on-staging.md`. Block markup examples: `fixtures/`.

## How styles work (css-panel)
- CSS editor only available when selected element has a valid CSS selector (add via Attributes Bar or by typing class/ID in HTML). Selector pill appears in CSS editor.
- "Attached CSS": styles belong to the selector/element, move with element/pattern/component on copy/import/export; CSS loads only when element present (no unused CSS); no global stylesheet hunting.
- Editor always shows the wrapper; you can't remove it or write outside it:
```
.your-selector {
    /* Code goes here */
}
```
- All styling is achieved with CSS nesting. No `%%root%%`-style dynamic root.
- Bi-directional sync: styling inputs (Mini GUI / CSS Quick Actions Bar) <-> CSS panel; single source of truth per selector. Mini GUI is V1.
- Global CSS: Style Manager > Stylesheets Manager (stylesheets, collections); variables: Variables Manager (e.g. `--content-width: 1280px;`).

## Nesting syntax
```
.header {
    display: flex;
    flex-direction: row;

    nav {
        display: flex;
    }
}
```
SCSS-like stemming (Etch isn't SCSS-powered but supports it): `&__`, `&_`, `&--`, `&-` all parse; `&` = parent selector.
```
.card {
    display: flex;
    flex-direction: row;

    &__heading {
        font-size: var(--h2);
    }
    &__description {
        font-size: var(--text-s);
    }
    &__link {
        color: var(--neutral);
    }
}
```
Parent-context styling (reverse `&`):
```
.card {
    .hero & {
        /* styles for the card when the card is in .hero */
    }
}
```
"Has Me" (style/define parent from child):
```
.card {
	:has(> &) {
		container-type: inline-size;
	}
}
```
## Auto-wrapping
- Auto variable wrapping: typing `--primary` expands to `var(--primary)` (accept with tab, enter or semicolon; also Enter in CSS styling inputs). Multiple at once:
```
.card {
    padding-inline: --space-m --space-l;
}
```
-> `padding-inline: var(--space-m) var(--space-l);`
- Auto calc wrapping: `100px + 2rem` -> `calc(100px + 2rem)`; works with auto variable wrapping.

## Functions
- `to-rem()`: converts px to rem on front-end, keeps px reference in editor. `to-rem(800px)` -> `50rem`. Base 16px (100%). Works anywhere incl. media/container queries. Renamed from `rem()` before version 1.0.0-alpha-4 (auto-migrated; avoids clash with native CSS `rem()`).

## Responsive philosophy
- Container-query-first; no device breakpoints; each component sets its own thresholds. Container queries use same syntax as media queries.
- Workflow: (1) build structure + selectors (Cmd/Ctrl+Enter), (2) style mobile-first (recommended, not required), (3) drag canvas, find breakpoints, click auto-insert query button (media = canvas width; container = element width), add styles inside block, (4) use `@custom-media` for recurring queries. Add "Has Me" before first container query.

## Container queries
```
.card {
	display: grid;
	gap: 1rem;

	:has(> &) {
		container-type: inline-size;
	}

	@container (width >= 500px) {
		grid-template-columns: 200px 1fr;
	}
}
```
Manual container on a specific parent: `.card-grid { container-type: inline-size; }` (couples to that parent). Multiple thresholds: several `@container (width >= 400px) {}` / `(width >= 700px)` blocks inside the selector. Custom token form: `@container (--component-wide) { grid-template-columns: 200px 1fr; }`.

## Media queries (use for viewport/global layout, print, orientation, hover, preference)
```
.site-header {
	display: flex;
	flex-direction: column;

	@media (width >= 900px) {
		flex-direction: row;
		justify-content: space-between;
	}
}
```
Range syntax (recommended) and traditional both work:
```
@media (width >= 600px) { }
@media (width <= 900px) { }
@media (400px <= width <= 800px) { }
@media (min-width: 600px) { }
@media (max-width: 900px) { }
@media (min-width: 400px) and (max-width: 800px) { }
```
Multiple conditions: `@media (width >= 900px) and (orientation: landscape) { }`. Note: multiple conditions with `and` are NOT compatible with `@custom-media` tokens; define the full compound condition as one `@custom-media` rule. Non-size examples: `@media (hover: hover)`, `@media (prefers-reduced-motion: reduce)`, `@media (prefers-color-scheme: dark)`.

## @custom-media (Since 1.2.0; gated behind Etch experimental settings toggle)
When enabled Etch creates Global Stylesheet "Custom Media Definitions".
```
/* Global (site-wide) queries */
@custom-media --small-screen (width <= 600px);
@custom-media --large-screen (width >= 1200px);
@custom-media --landscape-wide screen and (width >= 900px) and (orientation: landscape);

/* Component-specific queries */
@custom-media --news-card-wide (width >= 421px);
```
Use: `@media (--small-screen) { }`, `@container (--news-card-wide) { grid-template-columns: 160px 1fr; }`. Names must start with `--`. Definitions travel with copied elements. Global aliases work in container queries and vice versa.

## Intrinsic responsiveness (use instead of queries where possible)
Docs cover (examples use plain CSS): `clamp()` fluid type/spacing e.g. `font-size: clamp(1.75rem, 1.2rem + 2vw, 3rem);`, `grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));` (auto-fit collapses empty tracks; auto-fill keeps them), viewport units (`dvh` recommended over `vh` on mobile), `em`/`%`/`ch` (`max-width: 65ch;`), `min()`/`max()`/`clamp()` (`width: min(1200px, 100% - 2rem);`, `width: clamp(200px, 25%, 350px);`), flex-wrap (`flex: 1 1 600px;` / `flex: 1 1 250px;`), `aspect-ratio: 16 / 9;`, `object-fit: cover;`.

## Recipes (utilities) - expand by typing `?name;` in CSS
```
.foo {
    ?flex-column;
}
```
-> `display: flex; flex-direction: column;`. `?grid-3;` -> `display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); grid-template-rows: 1fr;`. `?auto-grid;` expands to a long block (uses `--column-count: 4;`, `--auto-grid-aggressiveness: .7;`, `--grid-gap`, `--content-width`).
Names by category (custom recipes: not yet user-creatable):
- Accessibility: clickable-parent, focus-parent, skip-link
- Color: color-mix
- Fade: fade-block, fade-inline, fade-top, fade-right, fade-bottom, fade-left
- Flex: flex-row, flex-column, center-all, center-left, center-right, center-top, center-bottom, flex-grid (`--columns` default 3, `--gap`, `--stretch`; reduces columns at 900px and 600px)
- Gradients (vars): gradient-linear/radial/conic (`--color-1`, `--color-2`), gradient-sharp (`--color-1`, `--color-2`, `--stop` 50%), gradient-fade (`--color-1`), gradient-vignette (`--color-1`, `--stop` 50%), gradient-text (`--color-1`, `--color-2`), gradient-border (`--color-1` bg, `--color-2`, `--color-3`; 2px)
- Grid: auto-grid, variable-grid, grid-1 to grid-12, grid-1-2, grid-1-3, grid-2-1, grid-2-3, grid-3-1, grid-3-2, content-grid
- Misc: columns, line-clamp, concentric-radius, concentric-radius-reverse (`--radius`, `--minimum-inner-radius`), font-face, is-bg, brace-contain `{""}`, brace-left `{"{"}`, brace-right `{"}"}`, footer-reveal (template, footer adjacent to main)
- Pseudo: ::before, ::after, ::before, ::after, :hover, :focus-visible, :hover, :focus-visible, hover-exclude-touch
- Ribbons: corner-ribbon on element inside container with `data-ribbon-position="top-left"|"top-right"`; vars `--ribbon-width` 300px, `--ribbon-offset` to-rem(20px), `--ribbon-background-color` var(--black, #000), `--ribbon-text-color` var(--white, #fff), `--ribbon-text-size` 1em, `--ribbon-shadow` 0 5px 10px #ccc, `--ribbon-padding` .5em 1em
