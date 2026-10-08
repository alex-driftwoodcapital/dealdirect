# ACSS 4.x Layout: grids, flexbox, columns

> **4.0.1 check (2026-10-07, see staging-4.0.1-facts.md):** the build outputs NO grid, auto-grid, variable-grid, alternating-grid, span/order/alignment, flex or column utility classes (only `.content-grid`, `.content--*`, `.width--*`). Everything below that is a `.grid--*`/`.col-*`/`.order--*`/`.align-*`/`.justify-*`/`.masonry--*`/`.variable-grid`/`.stretch` class is 3.x docs text left on stale pages; use the variables and `?` recipes instead: `grid-template-columns: var(--grid-N)`, `var(--grid-auto-N)`, `var(--grid-gap)`, recipes `?grid-N`, `?auto-grid`, `?variable-grid`, `?flex-grid`, `?columns`, `?content-grid`. Breakpoint forms (`.grid--l-2`) cannot exist (breakpoints removed): use `@media` or container queries on the element.
Sources: https://docs.automaticcss.com/grids/{grid-classes-standard,auto-grids,variable-grid,content-grid,auto-alternating-grids,grid-variables,masonry-layouts,auto-grid-mixin} , /flexbox/{flex-grids,flex-recipes} , /columns/{css-columns,masonry-layouts} , /recipes/{grid-recipes,column-recipes,content-grid-recipe,flex-recipes} , /mixins/content-grid-mixin
verified from docs 2026-10-02
Notes: no 4.x page named grid-system or flexbox-classes exists (sitemap); grid-classes-standard is the grid-system page. Recipe prefix in 4.x is `?` (3.x was `@`). Pages vary in age: see CONFLICTS at bottom.

## Grid variables (for custom/BEM classes)
`var(--grid-1)` ... `var(--grid-12)`, `var(--grid-1-2) var(--grid-1-3) var(--grid-2-1) var(--grid-2-3) var(--grid-3-1) var(--grid-3-2)`, `var(--grid-gap)`.
```
.service-grid { display: grid; grid-template-columns: var(--grid-3); gap: var(--grid-gap); }
@media (max-width: 991px) { .service-grid { grid-template-columns: var(--grid-2); } }
```
Recipes: `?grid-1`..`?grid-12`, `?grid-1-2 ?grid-1-3 ?grid-2-1 ?grid-2-3 ?grid-3-1 ?grid-3-2` expose standard grid utility code (`?grid-{}`); combine with breakpoint recipes.

## Auto grids (auto responsive, no breakpoints)
- Variable (verified in the build): `display: grid; grid-template-columns: var(--grid-auto-4); gap: var(--grid-gap);` for 2..12 columns. Min item width follows the content width; site setting "aggressiveness" (staging .7; 0-1, higher stacks sooner) and flow `auto-fit`.
- Recipe: `?auto-grid;` with `--column-count` and `--min` (min item width) set on the element; no per-item spans (docs: spans impractical).
- Mixin (Custom SCSS only): `@include auto-grid($column-count, $min, $flow, $force-even-column-count);`
- Removed class forms (`.grid--auto-N`, `.grid--stack-*`, `.grid--auto-fill`) are not in the 4.0.1 build.

## Variable grid
- Recipe `?variable-grid;`: columns fill by minimum item width `--min` (set on the element or via inline style, e.g. `--min: 380px`); default 2 equal columns at content width. Change `--min` with your own `@media` to fix orphans. The `.variable-grid` class is not in the build.

## Content grid (zones)
- `.content-grid` on any box (nestable); mixin `@include content-grid;` (no args); recipe `?content-grid;` (outputs `%root%` automatically). In a `section` ACSS removes inline padding and zeroes column gaps.
- Auto sections: Layout > Content Grid > "Default Sections to Content Grid"; off per section with `.content-grid--off`.
- Zones: Content (`var(--content-width)`, default zone), Feature, Feature Max, Full.
- Classes: `.content--feature`, `.content--feature-max`, `.content--full`, `.content--full-safe` (full width, content respects gutter). Page also references `.feature--` utilities.
- Programmatic: `grid-column: feature | feature-max | full;` e.g. `.blog-post-body > blockquote { grid-column: feature; }`. Full-safe: `grid-column: full; padding-inline: var(--gutter);`
- Local vars: `--content-width: 70ch;` `--feature-width: 75px;` `--feature-max-width: 75px;` (value added to each side of content zone). Globals in dashboard Layout > Content Grid.
- 50/50: `grid-template-columns: calc((min(50vw - var(--gutter), var(--content-width) / 2)) - (var(--grid-gap) / 2)) minmax(0, 1fr);` (override `--grid-gap` on container, not the calc).

## Flexbox (no utility classes in 4.x)
- 3.x flex classes (`.flex--row`, `.flex--col`, `.flex-grid--1`..`.flex-grid--6` + breakpoint variants) removed; replaced by recipes.
- Recipes: `?flex-row` (display:flex; flex-direction:row) , `?flex-column` (display:flex; flex-direction:column), `?center-all` (flex column; align-items:center; justify-content:center; text-align:center), `?center-left` (align-items:flex-start; justify-content:center; text-align:left), `?center-right` (flex-end; center; right), `?center-top` (align-items:center; justify-content:flex-start; text-align:center), `?center-bottom` (center; flex-end; center). All center-* use flex-direction:column.
- `?flex-grid`: centered/stretched unbalanced items. Vars: `--gap` (default `var(--grid-gap, 1.5rem)`), `--columns` (3), `--stretch` (0; `1` stretches). Default responsive: `@media (max-width: 900px){--columns:2}` `@media (max-width: 600px){--columns:1}`; override with own media queries.
```
.my-grid { ?flex-grid; --columns: 4; --gap: var(--space-l); --stretch: 1; }
```

## Columns (`?columns` recipe; utility classes removed in 4.0)
Removed: `.col-count--`, `.col-width--`, `.col-rule--`, `.col-span--`(per columns page).
Vars: `--col-count`, `--col-min-width`, `--col-rule-style`, `--col-rule-width`, `--col-rule-color`, `--col-gap`, `--row-gap` (margin on children).
Width vars: `var(--col-width-s|m|l)`; rule widths `var(--col-rule-width-s|m|l)` (sizes set in dashboard).
Rule example: `--col-rule-style: solid; --col-rule-width: var(--col-rule-width-m); --col-rule-color: var(--border-color);`
Masonry (columns page): `?columns` + `--col-count: 3; --col-gap: var(--space-l); --row-gap: var(--space-l);` or `--col-min-width: 300px`. `.masonry--1`..`.masonry--5` removed per columns/masonry page.

## CONFLICTS (resolved 2026-10-07)
- Settled by the build and "Changes From 3.x": `.masonry--N`, `.col-*--`, `.flex-grid--N` are removed; `/grids/masonry-layouts` is stale. Same for `.grid--*` classes (not in the stylesheet).
- grids/masonry-layouts (4.x tree) still documents `.masonry--1`..`.masonry--5`, `.masonry--[breakpoint]-[columns]`, `.col-width--[size]`; columns/masonry-layouts says these are removed in 4.0. Prefer `?columns`; verify in the dashboard before using classes.
- auto-grids / variable-grid pages show `@auto-grid;`, `@variable-grid;` (3.x syntax); recipes pages use `?`.
