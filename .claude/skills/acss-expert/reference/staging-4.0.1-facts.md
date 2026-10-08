# Staging build facts: ACSS 4.0.1
Source: `index/automatic.css` (header: "Version: 4.0.1 - Generated: 2026-10-03") and `index/acss-settings.json` (2565 keys), exported from staging alexg281.sg-host.com. Checked against docs.automaticcss.com 4.x on 2026-10-07. **Live build wins over docs.** Files in `index/` are read-only reference, never deployed.
Latest 4.x at check time: 4.0.1 (docs pages dated Aug 7, 2026). Refresh = re-export both files and re-run this check.

## The big rule: ACSS 4 is breakpoint-free and variable-first
Official: "What's New in ACSS 4.x" (/setup/whats-new-in-4): removed most utility class modules, removed breakpoints, recipes use `?`, OKLCH colors, `light-dark()` scheme, transparency tokens removed, width classes 10..90. The build confirms it: no `@media` width queries, no breakpoint tokens; settings hold only `vp-min` 360 and `vp-max` 1112 (px) plus the content width. Docs pages not yet cleaned up still show 3.x classes; the build does not output them (see "Documented but absent").

## Settings that drive values (staging)
| Item | Value |
|---|---|
| Content width | `--content-width: 69.5rem` (= vp-max 1112px); `body-max-width` 1920px |
| Fluid range | 360px to 1112px viewport |
| Root font size | 100% (`--root-font-size`) |
| Gutter | clamp 16px to 44px |
| Spacing | base 24px both ends; scale 1.5 desktop, 1.333 mobile; section adjust 5.333 (desktop) / 3 (mobile) |
| Text | scale 1.333; M 16 to 17px |
| Radius | `--radius` 16px; `--btn-radius` 999px; `--radius-m`, `-50`, `-circle`, `-none` |
| Color scheme | `light only` (no `light-dark()` output) |
| Fonts | `--text-font-family: "Host Grotesk", system-ui, sans-serif`; button weight 800 |
| Content gap / container gap / grid gap | `--space-m` / `--space-xl` / `--space-m` |

## Resolved sizes (px, min at 360 to max at 1112)
- `--space-xs` 10.7 to 13.5 | `-s` 16 to 18 | `-m` 24 | `-l` 32 to 36 | `-xl` 42.6 to 54 | `-xxl` 56.8 to 81
- `--section-space-xs` 40.5 to 56.9 | `-s` 54 to 85.3 | `-m` 72 to 128 | `-l` 96 to 192 | `-xl` 127.9 to 288 | `-xxl` 170.5 to 432
- `--text-xs` 13 | `-s` 15 | `-m` 16 to 17 | `-l` 18 to 20 | `-xl` 20 to 23 | `-xxl` 27.6 to 40.3
- `--h1` 43 to 99 | `--h2` 34 to 58 | `--h3` 22 to 30 | `--h4` 19 to 22 | `--h5` 14 to 15 | `--h6` 13 to 14
- Bridge tokens exist for all pairs: `--space-{big}-to-{small}`, `--section-space-...`, `--text-...`, `--h{n}-to-h{m}` (e.g. `--space-l-to-xs`, `--h1-to-h3`).

## Palette (OKLCH)
Enabled colors: primary `#2446D8`, secondary `#FFF3C4`, tertiary `#A9B8FF`, accent `#B5472A`, base `#161B26`, neutral `#4A5163`, plus `--white`, `--black`. Semantic colors (success, warning, info, danger) are OFF: no `--warning` etc. Shades per color: `-ultra-light -light -semi-light -semi-dark -dark -ultra-dark -hover`. Surfaces: `--bg-ultra-light` #FBFAF6, `--bg-light` white, `--bg-dark` = base, `--bg-ultra-dark` #0F131B; `--text-dark` = base, `--text-dark-muted` = neutral, `--text-light` = white, `--text-light-muted` #C9D0DE.
Brand mapping check (SKILL.md): Ink = `--base`, Blue = `--primary`, Butter = `--secondary`, Periwinkle = `--tertiary`. Matches.

## Utility classes the build outputs (complete list)
`.bg--{ultra-light|light|dark|ultra-dark}`, `.text--{dark|dark-muted|light|light-muted}`, `.text--{xs|s|m|l|xl|xxl}`, `.h1`-`.h6`, `.section--{xs..xxl}` and bridges (`.section--xl-to-l` ...), `.header--{xs..xxl}`, `.width--{10..90}`, `.width--{auto|full|fit-content|max-content|min-content}`, `.content-width`, `.content-width--safe`, `.content-grid`, `.content-grid--off`, `.content--{feature|feature-max|full|full-safe}`, `.btn--{primary|secondary}[-light|-dark]`, `.btn--base`, `.btn--base-light`, `.btn--outline` (combined), `.btn--{xs..xxl}`, `.btn--none`, `.icon--{xs|s|m|l|xl|2xl|boxed|plain}`, `.icon-list`, `.is-bg`, `.overlay`, `.scheme--{light|dark}`, `.smart-spacing`, `.smart-spacing--off`, `.smart-spacing-normalize`, `.sticky`, `.unrelate`, `.on-visible--{fade|float|stagger}`, `.on-visible-all--{fade|float}`, `.on-enter--stagger`, `.on-exit--stagger`, `.hidden-accessible`, `.skip-link`, `.blockquote`.
Off in staging (module toggled off, so names in the docs are absent): other button colors (tertiary, accent, neutral, semantic; `option-*-btn` off), cards (`option-cards` off), forms (`option-forms` off), enter/exit/hover effects, gap classes (`option-gaps` off), text/color transparency. Ribbons (`.ribbon`) are not in the build and the export has no toggle for them: unconfirmed, test before use. Turn on in the dashboard before using; then re-export.

## Documented but absent in 4.0.1 (do not use; replacement)
| Documented name | Why absent | Use instead |
|---|---|---|
| `.grid--*` (`.grid--N`, `.grid--l-2`, `.grid--1-2` etc.), `.col-span--`, `.order--`, `.align-*--`, `.justify-*--`, `.stretch` | breakpoints and most utility modules removed (whats-new); grid page /grids/grid-classes-standard is stale | `grid-template-columns: var(--grid-N)` or recipe `?grid-N`; `var(--grid-gap)` |
| `.grid--auto-N`, `.variable-grid`, `.grid-alternate--`, `.grid--stack-*` | not in build | `var(--grid-auto-N)`, recipes `?auto-grid`, `?variable-grid` |
| `.masonry--N`, `.col-count--`, `.col-width--`, `.col-rule--` | removed in 4.0 (/columns/masonry-layouts, /columns/css-columns) | `?columns` recipe |
| `.flex--row`, `.flex-grid--N` | removed (/flexbox/flex-grids) | `?flex-row`, `?flex-column`, `?flex-grid`, `?center-*` |
| `.gap--`, `.margin--`, `.pad--`, `.pad-section--`, `.pad-header--` | not in build | `var(--space-*)`, `.section--*`, `.header--*` |
| `.grid-gap`, `.container-gap`, `.content-gap` | `option-gaps` off | `var(--grid-gap)`, `var(--container-gap)`, `var(--content-gap)` |
| `.breakout--*` | 3.x only | `.content-grid` zones (`.content--feature`, `.content--full`) |
| `.link--*` | removed (/links/link-styling) | `--link-color`, custom class |
| `.text--{color}`, `.text--{weight}`, `.text--underline`, `.text--center` etc. | not in build (docs text-classes page lists them) | `color: var(--primary)`, own properties |
| `.marker--*` | not in build | `::marker { color: var(--primary) }` on the element |
| `.border`, `.border-dark`, `.box-shadow--m`, `.divider-*`, `.z--10`, `.relative`, `.transition`, `.focus--*`, `.focus-parent*`, `.clickable-parent` | removed in 4.0 (each page's "Changes From 3.x") | `var(--border)`, `var(--box-shadow-1)`, `?divider-*`, `?focus-parent`, `?clickable-parent` |
| `?primary-clr` expanding to `hsl(var(--primary-h) ...)` | `--primary-h/-s/-l` do not exist (OKLCH); recipes/color page stale | `var(--primary)`, `color-mix(in oklch, var(--primary) 20%, transparent)`, `oklch(from var(--primary) l c h / .5)` |
| `--body-color` | not in build | `--text-color`; page bg is `--body-bg-color` |
| `--*-trans-*` tokens | removed in 4.0 (/colors/transparencies); settings export still carries legacy `*-trans`, `*-alt`, `*-btn` keys: ignore | `color-mix()` |

## 3.x vs 4.x name conflicts that the build settles
- **t-shirt size `xxl`**: What's New says XXL became 2XL, but 4.0.1 outputs `xxl` everywhere (`--space-xxl`, `--text-xxl`, `.section--xxl`, `.btn--xxl`, `.header--xxl`). Only icons use `2xl` (`.icon--2xl`, `--icon-size-2xl`). Use `xxl` except icons.
- **Widths**: `.width--10`..`.width--90` and `--width-10`..`--width-90` (not t-shirt sizes).
- **Clickable parent**: recipes page says apply `?clickable-parent` to the heading that holds the link; the accessibility page says the parent. Not decidable from the build (recipes expand in the builder). Use the recipes page (heading) and verify in a staging render.
- **Breakpoint pages**: /setup/website-width-breakpoints still describes XS..XXL breakpoints and a Viewport tab; the build has none, and /dimension/content-width puts width under Layout > Website Dimensions.
