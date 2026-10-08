# ACSS 4.x typography

> **4.0.1 check (2026-10-07, see staging-4.0.1-facts.md):** `--h1..--h6`, `--text-{xs..xxl}`, all bridge tokens, `--text-color`, `--heading-*` confirmed (resolved px in the facts file). Text classes in the build are only `.text--{xs|s|m|l|xl|xxl}` and `.text--{dark|dark-muted|light|light-muted}`, plus `.h1..h6`; the weight/style/decoration/transform/alignment/color `.text--*` classes and `.marker--*` listed below are NOT output: use properties and variables. Per-size property variables (`--h1-color`, `--text-font-weight` ...) only exist when set in the dashboard; unset ones are absent. `fluid()` is 3.x SCSS: unconfirmed, see functions-mixins-recipes.md.
Sources (verified from docs 2026-10-02): https://docs.automaticcss.com/typography/fluid-text , /typography/fluid-headings , /typography/default-typography-styling , /typography/typography-variables , /typography/text-heading-line-length , /typography/text-classes , /typography/marker-classes , /typography/custom-fonts
NOTE: no /typography/fluid-responsive-typography page in 4.x (404); fluid-text + fluid-headings cover it. Docs give no numeric default sizes/scales except where stated below.

## Sizes
- Text sizes (t-shirt): xs, s, m, l, xl, xxl. Base = "M" (default paragraph size on desktop); XS and S scale down from M, others scale up.
- Heading sizes: h1-h6. Base heading size = H4 on desktop (typically slightly larger than base text, e.g. 18px text -> 20px heading).
- Dashboard: Typography tab (Root Font Size, Text/Headings tabs, Fonts tab). Root Font Size default 100% (62.5% optional). Sizes entered in px, output rem.
- Scale: separate desktop and mobile scales; values must be > 1. Base = adjusts all sizes evenly; scale = variance between sizes.
- Overrides: text min/max fields (plugged into clamp()/calc()); overriding removes size from scale (neighbours unaffected). Heading overrides: mobile/desktop fields per level; H5/H6 (and S/XS text) have min fields as accessibility floor.
- Custom sizes: use `fluid()` function.

## Font-size variables
- Headings: `--h1` `--h2` `--h3` `--h4` `--h5` `--h6`
- Text: `--text-xxl` `--text-xl` `--text-l` `--text-m` `--text-s` `--text-xs`
- Bridge text: `var(--text-{large}-to-{small})` - desktop max of large, mobile min of small. All 15: xxl-to-xl, xxl-to-l, xxl-to-m, xxl-to-s, xxl-to-xs, xl-to-l, xl-to-m, xl-to-s, xl-to-xs, l-to-m, l-to-s, l-to-xs, m-to-s, m-to-xs, s-to-xs (e.g. `--text-xl-to-s`).
- Bridge headings: `var(--h{large}-to-h{small})`: `--h1-to-h2` `--h1-to-h3` `--h1-to-h4` `--h1-to-h5` `--h1-to-h6` `--h2-to-h3` `--h2-to-h4` `--h2-to-h5` `--h2-to-h6` `--h3-to-h4` `--h3-to-h5` `--h3-to-h6` `--h4-to-h5` `--h4-to-h6` `--h5-to-h6`.

## Property variables
- Global headings: `--heading-font-family`, `--heading-color`, `--heading-line-height` (default), `--heading-font-weight` (default), `--heading-font-style`, `--heading-letter-spacing`, `--heading-text-transform`, `--heading-text-wrap` (default). Others exist only "if declared in the dashboard settings".
- Per heading level (h1 shown; same for h2-h6; exist if overridden in dashboard): `--h1-font-family`, `--h1-color`, `--h1-line-height`, `--h1-font-weight`, `--h1-font-style`, `--h1-letter-spacing`, `--h1-text-transform`, `--h1-max-width` (available by default; no global heading max-width var).
- Global text: `--text-font-family`, `--text-color`, `--text-line-height` (default), `--text-font-weight` (default), `--text-font-style`, `--text-letter-spacing`, `--text-text-transform`, `--text-max-width`, `--text-text-wrap` (default).
- Per text size (xl shown): `--text-xl-line-height`, `--text-xl-font-weight`, `--text-xl-font-style`, `--text-xl-letter-spacing`, `--text-xl-text-transform`, `--text-xl-max-width` (default).
- Docs examples: `font-size: var(--h4);` on an h2; `font-family: var(--heading-font-family);`; re-assign `--heading-font-family`, `--heading-color: var(--accent)`, `--heading-letter-spacing`, `--heading-line-height: calc(6px + 2ex)` in a class + `font-size: var(--h1)`.

## Defaults panel
- Heading/text defaults: Root Font Size, Base size (min/max), Type Scale (mobile/desktop), Font Family, Color, Line Height, Font Weight, Letter Spacing, Max-Width, Font Style, Text Transform, Text Wrap; also per size/level.
- Smart Line Height: leading added to double the x-height (`ex` unit in calc()); adjust `ex` value in decimal steps.
- Default text-wrap `pretty`; alternatives `balance` (not for >4 lines), `wrap` (off).
- Default max-width not applied in Bricks.

## Line length
- Typography panel: per text size and heading size; blank by default. Enter unit explicitly, e.g. `48ch`. Affects paragraphs, lists, `.text--l` etc.

## Text classes (all start `.text--`)
- Size `.text--{size}`: xs, s, m, l, xl, xxl
- Color `.text--{color}`: any ACSS color except transparency colors
- Weight `.text--{weight}`: 100 - 900
- Style: italic, oblique
- Decoration: none, underline, underline-wavy, underline-dotted, underline-double, underline-dashed, overline, line-through
- Transform: none, uppercase, lowercase, capitalize
- Alignment: left, center, right, justify
- Work on element or on container of multiple text elements.
- Marker classes `.marker--[color]-[shade]`: documented, but absent in 4.0.1; use `::marker { color: var(--primary); }`.

## Custom fonts (Typography > Fonts tab; Font 1-5, up to five)
- Outputs `@font-face`. Fields: Font Type (Static | Variable), Font Family (label), Font File Path (relative, e.g. `/wp-content/uploads/2025/your-font.woff2`, not full URL), Font Format (`woff2`, `woff`, `truetype`, `opentype`), Font Style (`normal`, `italic`, `oblique`), Font Weight (static only), Font Display (`auto`, `block`, `swap`, `fallback`, `optional`), Font Stretch (variable only), Font Variation Settings (variable only, e.g. `'wght' 700, 'slnt' 0`).
- Optional Fallbacks: second path + format. Static weights: same Font Family name, separate entry per weight. `.woff2` recommended.
- Apply: set "Default Font Family" in Headings/Text tab (family name must match exactly), per H1-H6 or text size, or `font-family: "Inter", sans-serif;`.
