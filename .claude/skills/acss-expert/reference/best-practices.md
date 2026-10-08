# ACSS 4 best practices (builder-agnostic; names verified against the 4.0.1 build)
Official basis: What's New in 4.x (variable-first, BEM-first, breakpoint-free, recipes, OKLCH, color-scheme), /grids/grid-classes-standard ("custom BEM classes with ACSS variables are the best practice"), /spacing/smart-spacing, /colors/automatic-color-relationships. Names below are checked against `index/acss-index.json`. CSS lives at element level (class, attribute or nested block); never a new stylesheet.

## 1. Choose the tool in this order
1. **Variable in a declaration** (`padding-block: var(--section-space-m)`). Default for everything ACSS has a token for.
2. **Utility class the build outputs** (see facts file list) when it is exactly the job: `.section--l`, `.width--60`, `.bg--dark`, `.text--l`, `.content-grid`, `.btn--secondary`. 4.x removed most utilities, so a class that "should" exist often does not: look it up first.
3. **Existing site class** (`etch_styles`) or nesting/chaining on it.
4. **New class** only when 1-3 cannot do it; every value inside it still uses tokens.
Never hard-code a value that has a token (`24px` -> `var(--space-m)`, `#2446D8` -> `var(--primary)`, `16px` radius -> `var(--radius)`).

## 2. Fluid by default, no breakpoints
- Sizes (`--text-*`, `--h1..6`, `--space-*`, `--section-space-*`, `--gutter`) are fluid clamps between the min and max viewport. Do not re-create them with `@media`.
- Use a **bridge** (`--space-l-to-xs`, `--h1-to-h3`, `--text-xl-to-m`) when an element must shrink faster than the scale on small screens.
- Layout change needs a structural switch (columns -> 1): use an auto grid (`var(--grid-auto-3)`, aggressiveness is a site setting) or one `@media`/container query on the element. Do not invent `.grid--l-2` style classes.

## 3. Spacing rhythm
- Section block padding: `.section--{xs..xxl}` or `padding-block: var(--section-space-*)`; inline padding is the gutter (`var(--gutter)`). Do not stack both a section class and your own padding.
- Inside a section: `gap: var(--content-gap)` between content blocks, `var(--container-gap)` between containers, `var(--grid-gap)` in grids. Prefer `gap` over margins; the 4.0.1 build has Smart Spacing so headings/paragraphs have no default margins in rich text and `.smart-spacing` containers.
- Scale steps: one step apart is a visible change (x1.5 on staging). Use M (24px) for related items, L-XL for groups, section tokens for bands.
- Contextual gap classes (`.grid-gap`...) are OFF in staging: use the variables.

## 4. Color roles
- **Surface** = `.bg--ultra-light|light|dark|ultra-dark` (class, not just `background:`): only the class triggers Automatic Color Relationships (text, headings, links and buttons flip). `background: var(--bg-dark)` does not.
- **Text** = `.text--dark|dark-muted|light|light-muted` or `color: var(--text-dark-muted)`.
- **Brand** colors (`--primary`, `--secondary`, `--tertiary`, `--base`, `--neutral`) for accents; shades by name (`--primary-ultra-light`). Transparency: `color-mix(in oklch, var(--black) 20%, transparent)`, never `--*-trans-*` (removed).
- Contrast: pair text with its surface via the relationship classes; check small text on `--secondary` and `--tertiary` (light fills) with Ink, not white.
- Color relationships override local button colors on `.bg--dark`: to keep a brand button look, add `.unrelate` or raise specificity (the site's global sheet already does this for outline and base buttons).

## 5. Type
- Elements take the scale automatically (`h1..h6`, `p`). Use `.h3` etc. to restyle a different tag; `font-size: var(--h4)` in a class for custom elements.
- Body sizes: `.text--s|m|l|xl` or `var(--text-*)`. Small caps/eyebrow = `var(--text-xs)`.
- Line length via `max-inline-size: 62ch` or `.width--*`; do not set px widths.
- Never change weight/letter-spacing per size ad hoc: if repeated, make one class.

## 6. Width and layout
- `.content-grid` zones (`.content--feature|feature-max|full|full-safe`) for full-bleed bands inside a contained page; no 100vw hacks.
- `.width--10..90` / `--width-*` for fractions of content width. Inside a gutter-padded section use `.content-width`, not `--safe`.
- Grids: `display: grid; grid-template-columns: var(--grid-3); gap: var(--grid-gap)`; ratio: `var(--grid-1-2)`; auto: `var(--grid-auto-3)`.

## 7. Buttons, links, focus, motion
- Buttons: `.btn--{color}` (+ `.btn--outline`); sizes only if the brand needs them. Tokens are local: override `--btn-*` on the element, not the properties.
- Whole-card links: `?clickable-parent` recipe (not the removed class), single link per card.
- Focus: keep the global `:focus-visible`; recolor with `--focus-color`.
- Motion: ACSS effects (`.on-visible--fade`) respect `prefers-reduced-motion`; custom transitions use `var(--transition)`/`--ease-*`.

## 8. Anti-patterns (verify flags these)
| Anti-pattern | Do instead |
|---|---|
| `.grid--3`, `.gap--m`, `.pad--l`, `.link--primary`, `.text--primary` (3.x names) | variables and properties |
| `hsl(var(--primary-h) ...)`, `--primary-trans-10` | `var(--primary)`, `color-mix()` |
| `margin`/`padding` px with a token equal | the token |
| `@media (max-width: 767px)` copying removed ACSS breakpoints | one query only where layout must switch |
| New global stylesheet or `<style>` block for a component | nested CSS on the element/class |
| `.bg--dark` without checking button/heading colors | check the relationship, use `.unrelate` where needed |
| `font-size` in px | `var(--text-*)` / `var(--h*)` |
