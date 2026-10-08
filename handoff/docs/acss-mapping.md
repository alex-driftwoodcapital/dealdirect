# ACSS 4 settings ← Driftwood design system

Verify every name against the installed ACSS version (staging stylesheet) before use — see `acss-expert`. 4.x has no transparency tokens; use `color-mix(in oklch, var(--primary) 20%, transparent)`.

## Palette (Dashboard › Color)
| ACSS color | Base hex | DS token | Shade overrides to set |
|---|---|---|---|
| `--primary` | `#0B2B48` | ink-800 | ultra-dark `#061A2E` (ink-900), dark `#061A2E`, semi-dark `#14385B` (ink-700), hover `#14385B`, semi-light `#22527F`, light `#3A6E9E` |
| `--secondary` | `#2468A8` | ocean (gold-500) | dark `#1B5388`, hover `#2060A0`, light `#5C97C9`, ultra-light `#B6D5EC` |
| `--accent` | `#6FB0E0` | teal-soft (on dark only) | — |
| `--tertiary` | `#00AFA0` | brand teal (logo only; avoid in UI) | — |
| `--base` | `#F5F6F8` | slate-50 | ultra-light `#FFFFFF`, light `#E9ECF0`, semi-light `#D3D8E0`, semi-dark `#4A5564`, dark `#2E3744`, ultra-dark `#1C2430` |
| `--neutral` | `#A9B2BE` | slate-300 | — |
| `--white` / `--black` | `#FFFFFF` / `#061A2E` | | |

Text colour on light: `#48535F` for body (set `--text-color`), `--primary-ultra-dark` for headings (`--heading-color`).

## Typography (Dashboard › Typography)
- Font 1: Plus Jakarta Sans variable, self-hosted (`fonts/PlusJakartaSans-VariableFont_wght.ttf` from the DS). Heading + text family.
- `--heading-font-weight: 300`; `--heading-letter-spacing: -0.034em`; `--heading-line-height: 1.06`.
- Sizes (desktop max / mobile min, set in the dashboard scale, then read back the generated values):
  - h1 88 / 42 · h2 56 / 30 · h3 32 / 24 · h4 18 / 17
  - text-l 20 / 16 · text-m 16 / 15 · text-s 14 · text-xs 12 (footnote floor)
- Eyebrow: custom class `.eyebrow` → 11px, 700, `letter-spacing: .22em`, uppercase, `color: var(--secondary)`; `.eyebrow--dark` uses `var(--accent)`.

## Spacing & layout
- Content width **1334px**; gutter 32px (`--gutter`).
- Section padding: `--section-space-xl` ≈ 120px desktop / 72px mobile (use `--section-space-xl-to-l` if the scale lands short).
- Card padding 26–28px ≈ `--space-m`/`--space-l`; grid gaps 16 / 20px ≈ `--space-s`/`--space-m`. Read the actual scale on staging and pick nearest; don't hard-code.

## Radius, borders, shadows
- `--radius` 12px (buttons). Add custom props in ACSS custom CSS: `--radius-card: 24px; --radius-tile: 20px; --radius-input: 10px;`
- `--border-color-light: rgba(219,229,240,.7)`.
- Shadows (custom props, since ACSS shadow presets differ): `--shadow-card`, `--shadow-card-light` — values in README.

## Buttons (Buttons & Links)
- `.btn--primary` → bg `--primary`, hover `--primary-semi-dark`, text white, radius 12, height 52 (`--btn-padding-block` tuned), 12px / 700 / .13em uppercase.
- `.btn--primary.btn--outline` on dark → white 42% border, 10% white fill, 18px blur (custom chain `.btn--glass`).
- `.btn--white` is removed in 4.0 → use `.btn--base` with ultra-light, or `.btn--custom` with `?btn` recipe for the white-on-dark CTA.
- Press state: `transform: scale(.972)` on `:active` (custom CSS on `.btn--*`).

## Focus
Focus color `--secondary`; dark sections set `--focus-color: var(--white)`.
