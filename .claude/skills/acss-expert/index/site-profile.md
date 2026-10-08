# Site profile: Driftwood DealDirect (staging wordpress-1077248-6717515.cloudwaysapps.com)
Measured values come from `index/automatic.css` and `index/acss-settings.json`; brand rules come from Alex. Blank template: `site-profile.template.md`; filled-in example from a previous build: `site-profile.twoeleven-example.md`.

> **Not measured yet.** `index/automatic.css`, `index/acss-settings.json` and `index/acss-index.json` are still the TwoEleven staging export (ACSS 4.0.1). The class/variable NAMES are valid ACSS 4.0.1 vocabulary; the VALUES and brand colors are not DealDirect's. On first SSH connect: save DealDirect's compiled `automatic.css` and settings export into `index/`, run `python3 -I scripts/build-index.py`, then fill the sections below (checklist: `reference/new-site-setup.md`).

## Source
- ACSS 4.0.1 (same version as the bundled index); stylesheet generated: TBD; WP 7.1.3, Etch 1.6.8; host: Cloudways.

## Measured (from files)
- TBD

## Brand mapping (TARGET from `handoff/docs/acss-mapping.md`; not applied to staging yet, Phase 2)
| Brand role | Value | ACSS token | Notes |
|---|---|---|---|
| Navy ink-800 | #0B2B48 | `--primary` | ultra-dark/dark #061A2E, semi-dark/hover #14385B, semi-light #22527F, light #3A6E9E |
| Ocean | #2468A8 | `--secondary` | dark #1B5388, hover #2060A0, light #5C97C9, ultra-light #B6D5EC; eyebrows on light |
| Teal-soft | #6FB0E0 | `--accent` | on dark only (eyebrows, chips) |
| Brand teal | #00AFA0 | `--tertiary` | logo only; avoid in UI |
| Slate-50 | #F5F6F8 | `--base` | ultra-light #FFFFFF, light #E9ECF0, semi-light #D3D8E0, semi-dark #4A5564, dark #2E3744, ultra-dark #1C2430 |
| Slate-300 | #A9B2BE | `--neutral` | |
| Body text | #48535F | `--text-color` | headings `--primary-ultra-dark` |
| Plus Jakarta Sans variable (200 to 800) | font | text + heading family | self-hosted; headings 300, -0.034em, line-height 1.06 |

## Component rules (target)
- Type scale (max/min px): h1 88/42, h2 56/30, h3 32/24, h4 18/17; text-l 20/16, text-m 16/15, text-s 14, text-xs 12 (footnote floor). Eyebrow `.eyebrow` 11px/700/.22em uppercase `--secondary` (`.eyebrow--dark` `--accent`).
- Content width 1334px, gutter 32px; section padding ~120 desktop / 72 mobile.
- Radii: 10 inputs, 12 buttons (`--radius`), 14 to 16 small cards, 20 stat/past tiles, 24 cards/modals/CTA, 999 chips. Custom props `--radius-card/-tile/-input`, `--shadow-card`, `--shadow-card-light` (values in `handoff/README.md`).
- Buttons: `.btn--primary` 52px tall, 12px/700/.13em uppercase; `.btn--glass` on dark; `:active` scale(.972). 4.0 has no `.btn--white`.
- Focus `--secondary`; dark sections `--focus-color: var(--white)`. 4.x has no transparency tokens: `color-mix(in oklch, var(--primary) 20%, transparent)`.

## Open items
- Export DealDirect's ACSS build and settings; rebuild the index.
- Apply the brand mapping above in the ACSS dashboard (Phase 2), then re-measure.
