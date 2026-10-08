# Page recipes: common sections as ACSS style specs
Each recipe is a **style spec** (see thread 5 `formats/style-spec.md`): role, ACSS classes to apply, and element-level CSS using only verified names (checked against `index/acss-index.json`, 4.0.1; every `var()`/class below exists). Etch owns the structure; these never add stylesheets, only class/nested CSS on the elements. Class names in `.kebab` are examples: reuse the site's existing class if one exists (TwoEleven already has `.eyebrow`, `.section-head`). Brand colors follow `index/site-profile.md`. Official basis: /spacing/section-spacing, /grids/content-grid, /grids/grid-variables, /buttons/button-classes, /backgrounds/contextual-background-colors, /accessibility/clickable-parent.

## Section shell (every recipe sits in one)
- Section: `.section--l` (block padding + gutter) and a surface class when not default: `.bg--ultra-light|light|dark|ultra-dark`.
- Inner container: `.content-width` (parent has a gutter). Gap between children: `gap: var(--container-gap)`.
```
.section__inner { display: grid; gap: var(--container-gap); }
```

## Section head (eyebrow + h2 + lede)
- Classes: wrapper `.section-head`; eyebrow `.eyebrow`; lede `p`. Existing TwoEleven rules apply (eyebrow 13px, uppercase, `--primary`, `--tertiary` on dark).
```
.section-head { display: grid; gap: var(--space-s); max-inline-size: 47.5rem; }
.section-head > p:not(.eyebrow) { color: var(--text-dark-muted); max-inline-size: 62ch; font-size: var(--text-l); }
:where(.bg--dark, .bg--ultra-dark) .section-head > p:not(.eyebrow) { color: var(--text-light-muted); }
```

## Hero
- Section `.section--xl` (+ `.bg--ultra-light`). Content: eyebrow, `h1`, lede, button row. h1 uses the fluid `--h1`; do not set a px size.
```
.hero__inner { display: grid; grid-template-columns: var(--grid-2-1); gap: var(--grid-gap); align-items: center; }
.hero__copy { display: grid; gap: var(--space-m); justify-items: start; }
.hero__copy > p { font-size: var(--text-xl); max-inline-size: 52ch; text-wrap: pretty; }
.hero__actions { display: flex; flex-wrap: wrap; gap: var(--space-s); }
@media (max-width: 48rem) { .hero__inner { grid-template-columns: 1fr; } }
```
- Buttons: `.btn--secondary` (primary CTA) + `.btn--primary.btn--outline` on light.
- Single `@media` only because the layout must collapse; width is one number, not an ACSS breakpoint.

## Card grid (no ACSS cards module; custom class on tokens)
- Wrapper `.card-grid`; card `.card`; use `var(--grid-auto-3)` so it stacks by itself.
```
.card-grid { display: grid; grid-template-columns: var(--grid-auto-3); gap: var(--grid-gap); }
.card { display: flex; flex-direction: column; gap: var(--space-s); padding: var(--space-l); border: var(--border); border-radius: var(--radius); background: var(--white); box-shadow: var(--box-shadow-1); position: relative; }
.card h3 { font-size: var(--h4); }
.card .btn--secondary { margin-block-start: auto; align-self: start; }   /* button sits at the bottom of equal-height cards */
.card__link { ?clickable-parent; }   /* recipe on the heading link; card is position: relative */
```
- Cards in a row are equal height (grid stretch); `margin-block-start: auto` on the button pushes it to the bottom whatever the copy length (card is a flex column, so the auto margin works).
- `?clickable-parent` expands in the builder; apply to the heading that holds the single link.

## Split feature (text + media)
- Section `.section--l`; two children. Ratio via variable.
```
.feature { display: grid; grid-template-columns: var(--grid-1-2); gap: var(--space-xl); align-items: center; }
.feature__media img { inline-size: 100%; aspect-ratio: 4 / 3; object-fit: cover; border-radius: var(--radius); }
@media (max-width: 48rem) { .feature { grid-template-columns: 1fr; } }
```

## Full-bleed band inside a contained page
- Parent `.content-grid`; band child `.content--full-safe` (full width, content respects gutter). No 100vw.
```
.band { background: var(--primary); color: var(--white); padding-block: var(--section-space-s); }
```

## CTA band (dark)
- Section `.section--m .bg--dark` (relationships flip text/headings/links). Keep outline button white via the existing site override.
```
.cta { display: grid; justify-items: center; gap: var(--space-m); text-align: center; }
.cta h2 { max-inline-size: 22ch; font-size: var(--h2); text-wrap: balance; }
```
- Buttons: `.btn--secondary` (butter fill, Ink text) + `.btn--outline` (white on dark per site rule).

## Form (forms module is OFF on staging: fields use tokens, not `.form--*`)
```
.form { display: grid; gap: var(--space-s); max-inline-size: 36rem; }
.form label { font-weight: 600; font-size: var(--text-s); }
.form :is(input, select, textarea) { inline-size: 100%; padding: var(--space-xs) var(--space-s); border: var(--border); border-radius: var(--radius); background: var(--white); color: var(--text-dark); }
.form :is(input, select, textarea):focus-visible { outline: var(--focus-width) solid var(--focus-color); outline-offset: 2px; }
.form .btn--secondary { justify-self: start; }
```
- If the forms module is enabled later, drop the field rules and let ACSS style them (Options > Forms).

## Header / nav
- Header gets the sticky class; height from `--header-height` (set by the site script). Links default to ACSS link styles but nav links are excluded from the default link rule (`header a`).
```
.nav { display: flex; align-items: center; justify-content: space-between; gap: var(--space-m); padding-block: var(--space-s); padding-inline: var(--gutter); }
.nav__list { display: flex; gap: var(--space-m); list-style: none; padding: 0; }
.nav__list a { color: var(--text-dark); font-weight: 600; text-decoration: none; }
.nav__list a:hover { color: var(--primary); }
```
- Mobile menu = structure (Etch); full-screen on phones per brand rule.

## Footer
- Section `.bg--ultra-dark`, `.section--m`; columns via auto grid.
```
.site-footer__cols { display: grid; grid-template-columns: var(--grid-auto-4); gap: var(--grid-gap); }
.site-footer a { color: var(--text-light-muted); }
.site-footer a:hover { color: var(--white); }
.site-footer small { font-size: var(--text-xs); color: var(--text-light-muted); }
```

## Quote band
```
.quote-band { background-color: var(--primary); color: var(--white); }
.quote-band blockquote { font-size: var(--h2); font-weight: 700; max-inline-size: 22ch; }
.quote-band figcaption { color: var(--primary-ultra-light); }
```
(TwoEleven's live `.quote-band` also resets `--blockquote-*` vars to remove the default blockquote styling.)
