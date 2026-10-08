# ACSS 4.x spacing

> **4.0.1 check (2026-10-07, see staging-4.0.1-facts.md):** all `--space-*`, `--section-space-*` (+ 15 bridges each), `--gutter`, `--container-gap`, `--content-gap`, `--grid-gap` confirmed (values in the facts file; M = 24px fixed on staging). `.section--{xs..xxl}` and bridge classes (`.section--xl-to-l`), `.header--{xs..xxl}`, `.smart-spacing`, `.smart-spacing--off` confirmed. NOT output: `.container-gap`, `.content-gap`, `.grid-gap` (`option-gaps` off; use the variables) and `.gap--`/`.pad--`/`.margin--`. Size name is `xxl`.
Sources (verified from docs 2026-10-02): https://docs.automaticcss.com/spacing/standard-spacing-setup , /spacing/spacing-variables , /spacing/section-spacing , /spacing/section-padding-classes , /spacing/header-padding-classes , /spacing/contextual-spacing , /spacing/automatic-spacing , /spacing/smart-spacing
NOTE: no /spacing/spacing-system page exists in 4.x docs (404). Exact pixel/rem values and scale numbers are not given in docs (dashboard-set).

## Standard spacing setup (dashboard > Spacing)
- Inputs: Base Spacing (Desktop value = exact at content width and beyond; Mobile value = exact at min website width), Base Scale (Desktop Ratio, Mobile Ratio).
- Base spacing maps to all "M" values and affects section spacing. Sizes above M = multiplied by scale; below M = divided by scale.
- Scale: t-shirt sizes xs, s, m, l, xl, xxl. Fluid between mobile and desktop (no breakpoints).
- Affects: Spacing Variables, Section Padding Classes, Contextual Spacing Utilities, Header Classes. Adjustable any time.

## Variables
| Pattern | Meaning |
|---|---|
| `var(--space-{size})` | standard spacing, size = xs s m l xl xxl. No `--pad-m` etc.: "spacing is just spacing" |
| `var(--section-space-{size})` | section block padding values |
| `var(--gutter)` | website gutter (section inline padding) |
| `var(--space-{large}-to-{small})` | bridge: desktop max of large, mobile min of small |
| `var(--section-space-{large}-to-{small})` | section bridge |
- Bridge list (both `--space-` and `--section-space-` prefixes): xxl-to-xl, xxl-to-l, xxl-to-m, xxl-to-s, xxl-to-xs, xl-to-l, xl-to-m, xl-to-s, xl-to-xs, l-to-m, l-to-s, l-to-xs, m-to-s, m-to-xs, s-to-xs. (15 each.)
- Examples from docs: `padding-block: var(--section-space-xl);` `padding-block: calc(var(--section-space-l) * 1.1);` `padding-inline: var(--gutter);` `padding: calc(var(--space-l) / 1.1);` `padding-block: var(--space-xl-to-m);` `margin-block-start: calc((var(--section-space-m) + var(--space-l)) * -1);`
- Fine-tune with calc(); keep adjustments small (if scale 1.5, stay within ~1.25 of chosen size).

## Section spacing
- "M" section spacing applied to top-level `section` elements by default.
- Dashboard: "Base Spacing Multiplier" (first number = mobile, second = desktop; fluid), "Gutter" inputs (inline padding via responsive clamp), "Block Padding" (via section spacing variable; 1 value = both, 2 values = top, bottom). Inputs map to M; other sizes from the spacing scale.
- Classes: `.section--{size}` (xs to xxl): changes block padding only, keeps gutter. Header: `.header--{size}` (follows standard spacing, not section spacing).
- Best-practice structure: `section` (gutter via inline padding) + inner `div` (content width, auto-centered).

## Contextual spacing (set in Spacing tab)
| Context | Class | Variable |
|---|---|---|
| Container gap (between containers in a section) | `.container-gap` | `var(--container-gap)` |
| Content gap (between content elements) | `.content-gap` | `var(--content-gap)` |
| Grid gap | `.grid-gap` | `var(--grid-gap)` |
- Tweak with calc: `gap: calc(var(--grid-gap) * 2);` Doc example also uses `grid-template-columns: var(--grid-3);`.

## Automatic Spacing
- Applies contextual spacing automatically at zero specificity: Auto Container Gap (gap between direct-child divs of `section`), Auto Content Gap (divs directly in `section`), Auto Grid Gap (grids using grid utility classes). Each toggleable.

## Smart Spacing (Spacing > Smart Spacing)
- Removes default margins from headings, paragraphs, lists, list items so `gap` is even; re-applies spacing only between adjacent siblings in: rich text, blog post content, `.smart-spacing` containers, "Target Additional Selectors" input, WooCommerce content. Only direct children of target. Parent must be Flex/Grid for gap use.
- Classes: `.smart-spacing` (put on direct parent), `.smart-spacing--off` (disable at box/section/page level; removes ALL spacing).
- "Target Additional Selectors" format: `".extra-wrapper" ".brxe-text > div"` (quoted, comma separated). "Avoid Duplicate Margins" selectors editable.
- Tabs: Text and Lists; Other (Flow Spacing, Figures, Figcaptions, Blockquotes). "(block)" inputs take 2 values (top, bottom).
- Variables: `--paragraph-spacing`, `--heading-spacing`, `--h2-spacing`, `--h3-spacing`, `--h4-spacing`, `--h5-spacing`, `--h6-spacing`, `--list-spacing`, `--list-indent-spacing`, `--list-item-spacing`, `--nested-list-spacing`, `--nested-list-indent-spacing`, `--nested-list-item-spacing`, `--flow-spacing`, `--figure-spacing`, `--figcaption-spacing`, `--blockquote-spacing`.
