# ACSS 4.x Components: buttons, cards, links, forms, icons

> **4.0.1 check (2026-10-07, see staging-4.0.1-facts.md):** staging outputs only `.btn--primary|secondary` (+`-light|-dark`), `.btn--base`, `.btn--base-light`, `.btn--outline` combined with a color, sizes `.btn--xs..xxl`, `.btn--none`; tertiary/accent/neutral/semantic button colors are off (`option-*-btn` off). Buttons: `--btn-radius` 999px, weight 800, min-width 8.75rem, padding 14px 24px, border 2px. Cards (`option-cards` off) and forms (`option-forms` off) emit no CSS, so `--card-*`, `.form--*` and card selectors are unavailable until enabled. `.link--*` removed in 4.0. Icons: build outputs `.icon--plain` / `data-icon-style="plain"` (docs say `naked`), has no `.icon--light|dark` or `data-icon-theme`, and sizes `.icon--xs|s|m|l|xl|2xl`. Use what the build outputs.
Sources: https://docs.automaticcss.com/buttons/{button-styling,button-classes,button-variables,outline-buttons,auto-button-styling-exclusions,gradient-outline-buttons} , /cards/{card-framework-philosophy,card-styling,card-color-scheme,card-targeting,card-workflow} , /links/{link-styling,external-link-indication} , /forms/form-styling-basics , /icons/{icon-framework,icon-mixin} , /mixins/{button-mixins,card-container-mixin} , /recipes/{button-recipes,card-container-recipe}
verified from docs 2026-10-02

## Buttons
- Naming: `.btn--` (abbreviated). Works on `<a>` or `<button>`. Any class starting `.btn--` auto-receives global button styles/framework.
- Solid: `.btn--primary`, `.btn--secondary`, `.btn--tertiary`, `.btn--accent`, `.btn--base`, `.btn--neutral` (only if color active in Palette).
- Light/dark variants: `.btn--{color}-{variant}` e.g. `.btn--primary-light`, `.btn--primary-dark`. Use alone; do not combine with the main class.
- Outline: `.btn--outline` combined with `.btn--{color}` (and `.btn--{size}`); works with light/dark variants. Requires Buttons & Links > Options > "Outline Variants" on.
- Sizes (t-shirt xs, s, m, l, xl, xxl): `.btn--l`, `.btn--s`, etc. Example: `.btn--primary .btn--outline .btn--s` (class order irrelevant).
- `.unrelate` on a button prevents auto color-relationship changes on backgrounds (new in 4.0).
- Removed in 4.0: styles action, white, black, shade. Outline border width unified with solid.
- Dashboard: Buttons & Links tab. Default options: padding (Y/X, em preferred), min width, line-height, letter-spacing, font weight/family/style, text-transform, text-decoration (+hover), custom text size (min/max; default "M"), border width/style/radius (default = global radius), transition (global default). Per-color: background, bg hover, text, text hover, border, border hover, focus color. Options panel toggles solid/outline/light-dark loading per color. Do not use `.rounded`/radius variables on buttons (set radius in dashboard).
- Override locally (tokens are locally scoped):
```
#btn123 { --btn-padding-block: 2em; --btn-padding-inline: 4em; --btn-font-weight: 900; --btn-background: var(--primary-dark); --btn-background-hover: var(--primary-ultra-dark); }
body.custom .btn--primary { --btn-padding-block: 2em; ... }
```
- Variables (button-variables page): `--btn-background --btn-background-hover --btn-text-color --btn-text-color-hover --btn-text-transform --btn-text-decoration --btn-text-decoration-hover --btn-letter-spacing --btn-line-height --btn-font-size --btn-font-weight --btn-font-family --btn-font-style --btn-padding-block --btn-padding-inline --btn-min-width --btn-align-items --btn-transition-duration --btn-border-color --btn-border-color-hover --btn-border-style --btn-radius --btn-border-width --btn-outline-background-color --btn-outline-border-hover --btn-outline-text-color --btn-outline-text-color-hover --focus-color`
  - 4.0: added `--btn-font-family`, `--btn-align-items`; removed `--btn-outline-border-width` (use `--btn-border-width`).
- Exclusions: Buttons & Links > Options > Additional Options; comma-separated selectors e.g. `.btn--third-party-example, .btn--another`.
- Custom buttons: make `.btn--custom` class (gets defaults), use recipe `?btn` (outputs main button vars; type in custom CSS or Custom SCSS) or mixin.
- Mixin (Custom SCSS only): `@include btn(primary);` Styles: `{primary|secondary|tertiary|accent|base|neutral}` plus `-light`, `-dark`, and outline forms quoted: `@include btn("primary.btn--outline");` (also `primary-light.btn--outline`, `primary-dark.btn--outline`). Specificity fix: double selector `.x.x { @include btn(...) }`.
- Gradient outline button page (custom CSS recipe, 5 steps): uses `@property --gradient-color-1/-2 { initial-value: transparent }` (vanilla adds `syntax: " <color>"; inherits: false;`), `.btn--primary.btn--primary`, `::before` with mask (`mask-composite: exclude`), vars `--gradient-angle --gradient-transition`. NOTE: page uses `--btn-outline-border-width` which 4.0 button-variables page says is removed; and `--transition-duration`, `--transition-timing`. Read page for full code.
- Button variables page example also shows `var(--btn-border-radius)` (differs from listed `--btn-radius`).

## Cards (Card Framework; off by default)
- Enable: dashboard Cards > toggle. Must list selectors: Cards > Card Options > Card Selectors, comma-separated, e.g. `.service-card, .article-card, .media-card, .team-card`. Auto-targeting removed in 4.0. Target wrapper only.
- BEM children recognized: `__media`, `__avatar`, `[data-icon]` (attribute required for icons), headings h1-h6.
- Default layout: `display:flex; flex-direction:column`; option "Default Cards to Display Grid" (Card Options).
- Mixin: `.custom-element { @include card; }` (applies all framework styles without selector list).
- Tokens: `--card-padding --card-gap --card-radius --card-min-radius --card-border-width --card-border-style --card-border-color --card-background --card-heading-size --card-heading-color --card-text-size --card-text-color --card-link-color --card-link-color-hover --card-button-font-size --card-icon-size --card-icon-color --card-avatar-size --card-avatar-radius --card-media-radius --card-media-aspect-ratio --card-shadow`
- Per-card override: `.pricing-card { --card-padding: var(--space-l); --card-heading-size: var(--h2); --card-radius: var(--radius-l); }`. Manual alt: `.article-card { padding:0; gap:0 }` + `.article-card__content-wrapper { padding: var(--card-padding); gap: var(--card-gap); }`
- Styling options (Cards > Card Styling > Styling Options): background, heading/text color, padding, content gap, heading/text size, Concentric Radius (Off | Standard = `--radius + --card-padding` | Reverse = inner `--radius - --card-padding` clamped), Minimum Radius (Reverse only; default `4px`), border width/style/color, border radius (Off only), link color/hover, button style/text size, icon size/color/boxed (padding, border, radius, background), avatar (size, border, radius `50vw` circle, aspect ratio `1`), media (radius, aspect ratio, object fit), Card Shadow (e.g. `var(--box-shadow-1)`).
- Color scheme (needs Colors > Color Scheme support on): Default Card Scheme = Inherit | Light | Dark. Per-card modifier in class name: `--dark` / `--light`, e.g. `service-card--dark`, `testimonial-card--light` (framework detects `--light`/`--dark`).
- Container queries: mixin `@include card-container("inline-size > 767px") { ... }` (needs Card Framework on + Auto Container Query support for Cards on; range syntax in quotes; double selector for specificity). Recipe `?card-container` (3.x was `@card-container`):
```
%root% { @container card ( inline-size >= 767px ) { display: grid; grid-template-columns: var(--grid-2-3); --card-media-aspect-ratio: 4/3; --card-heading-size: var(--h2); } }
```
- Workflow: enable early; target each new card immediately; override with tokens not hard values; manual CSS only for unique properties.

## Links
- Dashboard: Buttons & Links > Links. Options: color, weight (`inherit`), decoration, decoration color/thickness, underline offset, global transition.
- Exclusions: enable "Add Link Default Exclusions"; textarea with quoted comma-separated selectors: `"header a", "footer a", ".nav a"` (feeds `:not()`).
- Removed in 4.0: `.link--primary`, `.link--secondary`, etc. (use custom properties/classes).
- External link indication: Buttons and Links > Links tab > "External Links" accordion > "Indicate External Links". Controls: indicator (any HTML entity), position (before/after), gap, size, alignment, color/hover, weight, offset (Y/X). Default exclusion: `:has(> img, > figure, > picture, > svg)`; add selectors after it, comma separated e.g. `:has(> img, > figure, > picture, > svg), .exclude-this-link, #exclude-this-link`. Default screen-reader text: "Link to external site." (customizable).

## Forms
- Only WS Form supported. Forms screen > "Load Forms" on. WS Form Styler must be enabled; click Save on WS Form settings page to regenerate files.
- Auto light/dark via CSS `light-dark()` following site `color-scheme`. Optional classes: `.form--light`, `.form--dark` (on form or parent).

## Icons
- Icon Framework on by default (Dashboard > Icons). Enable styling per icon with attribute `data-icon` (on the `<svg>` itself for code elements): `<svg data-icon xmlns="..." />`.
- Size: `.icon--{size}` (default 3 sizes, M default; "Expand Icon Sizes" under Icons > Options for more) or `data-icon-size="{size}"`.
- Style: `.icon--boxed` / `.icon--naked` or `data-icon-style="boxed|naked"`. Theme: `.icon--light` / `.icon--dark` or `data-icon-theme="light|dark"`. Work on parent for groups. Theme name matches icon color, not box.
- Lists: `.icon-list` on `<ul>/<ol>` or `[data-icon-list]`. Options: boxed list icons, icon size, list gap, inline offset, block offset. No pseudo-element icons.
- Global settings: icon padding/border width/style/radius (boxed only); per theme: color, background, border color, box shadow (boxed only); hover variants except box-shadow.
- Bricks specificity: use `%root%%root% {}` in custom CSS.
- Mixin (Custom SCSS only): `icon($style, $box-style)` both optional; `@include icon;` `@include icon(dark);` `@include icon(dark, off);` `$style`: light|dark; `$box-style`: `box` or anything else = no box. `@include icon(box);` is invalid. Not usable if boxed feature is off by default.
