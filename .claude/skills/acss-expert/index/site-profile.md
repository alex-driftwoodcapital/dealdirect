# Site profile: TwoEleven (staging alexg281.sg-host.com)
Measured values come from `index/automatic.css` and `index/acss-settings.json`; brand rules come from Alex. Blank template: `site-profile.template.md`. Live site wins: re-measure after any export refresh.

## Source
- ACSS 4.0.1; stylesheet generated 2026-10-03 03:58; WP 7.1.3, Etch 1.6.8 (staging); builder = Etch (ACSS needs no setup in Etch).
- Files: `index/automatic.css`, `index/acss-settings.json`, `index/acss-index.json`. Real values and the list of classes the build outputs: `reference/staging-4.0.1-facts.md`.

## Measured
- Content width `--content-width: 69.5rem` (1112px); fluid range 360 to 1112px; `body-max-width` 1920px; gutter 16 to 44px. Breakpoint-free (use `@media`/container queries on the element if needed).
- Spacing: base 24px both ends (M fixed 24px); scale 1.5 desktop, 1.333 mobile. `--space-xs..xxl` = 10.7-13.5 / 16-18 / 24 / 32-36 / 42.6-54 / 56.8-81px. Section spacing M = 72 to 128px.
- Text: scale 1.333; `--text-xs` 13, `-s` 15, `-m` 16-17, `-l` 18-20, `-xl` 20-23, `-xxl` 27.6-40.3px. Headings `--h1` 43-99, `--h2` 34-58, `--h3` 22-30, `--h4` 19-22, `--h5` 14-15, `--h6` 13-14px. Line heights: text 1.55, h1 0.96, h2 0.99.
- Radius: `--radius` 16px; buttons `--btn-radius` 999px (pills). Button: padding 14px 24px, weight 800, 16px, min-width 8.75rem, border 2px, line-height 1.25 (= 52px tall).
- Fonts: `--text-font-family: "Host Grotesk", system-ui, sans-serif`; no separate heading family. Color scheme `light only` (no `light-dark()`). Page background `--body-bg-color` = `--bg-ultra-light` (#FBFAF6).
- Palette enabled: primary, secondary, tertiary, accent, base, neutral (+ `--white`, `--black`). Semantic colors (success, warning, info, danger) OFF.
- Modules OFF (their classes/variables do not exist until enabled): gap classes, cards, forms, tertiary/accent/neutral/semantic buttons, enter/exit/hover effects.

## Brand mapping
| Brand | Value | ACSS token | Notes |
|---|---|---|---|
| Ink | #161B26 | `--base` (shades `--base-dark`...) | body text via `--text-dark`; dark surface `--bg-dark` |
| Blue | #2446D8 | `--primary` | links (`--link-color`), `.btn--primary` |
| Butter | #FFF3C4 | `--secondary` | `.btn--secondary` (butter fill, Ink text) |
| Periwinkle | #A9B8FF | `--tertiary` | accents; no button class yet (tertiary buttons OFF) |
| Rust (not in brand list) | #B5472A | `--accent` | present in settings; confirm with Alex before use |
| Neutral | #4A5163 | `--neutral` | muted text `--text-dark-muted` |
| Host Grotesk | font | `--text-font-family` | only typeface |

## Component rules
- Buttons: one size (16px, 52px tall; do not add `.btn--s/.btn--l`), one label "Book a free review". Primary CTA = solid butter with dark text = `.btn--secondary`. Secondary CTA = outline: `.btn--primary.btn--outline` on light surfaces, `.btn--secondary.btn--outline` on dark (`.bg--dark`/`.bg--ultra-dark`). (Note: ACSS's "primary" is Blue, the brand's primary button is ACSS secondary.)
- Eyebrows: 13px = `var(--text-xs)`.
- Shapes: no one-sided border on rounded shapes (use full `var(--border)` or none).
- Layout: no pinned or scroll-jacked layers, no fixed elements near the bottom; modals full screen on phones; check 375 and 1440 widths, no horizontal overflow.

## Open items
- Accent (#B5472A) and Periwinkle usage rules, heading weight/family, and whether tertiary/card/form modules should be turned on: Alex decision, then re-export staging and rebuild the index.
