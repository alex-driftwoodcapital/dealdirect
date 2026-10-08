# ACSS 4.x colors, color assignments, color scheme

> **4.0.1 check (2026-10-07, see staging-4.0.1-facts.md):** staging enables primary, secondary, tertiary, accent, base, neutral (OKLCH) with 7 shades each; semantic colors are off, so `--warning` etc. and `.text--warning-light` do not exist. `.text--{color}`, `.bg--{color}`, `.link--*` are not output (only the four `.bg--` and four `.text--` surface/text relationship classes). `--body-color` does not exist: use `--text-color` and `--body-bg-color`. HSL partials (`--primary-h/-s/-l`, `?primary-clr` expansion) do not exist in 4.x OKLCH output. Color scheme is `light only` on staging: no `light-dark()` is emitted; `-alt` colors in the settings export are legacy and unused.
Sources (verified from docs 2026-10-02): https://docs.automaticcss.com/colors/palette-intro , /colors/main-colors , /colors/semantic-colors , /colors/transparencies , /colors/unified-lightness , /color-assignments/background-text-assignments , /color-assignments/automatic-color-relationships , /color-scheme/color-scheme-setup , /color-scheme/implementing-color-scheme , /color-scheme/modern-color-scheme-workflow

## Palette
- Dashboard > Palette: Main Colors, Semantic Colors, Palette Options (Unified Lightness). Colors entered as hex etc., stored in OKLCH.
- Main colors (6 named slots; enable only needed): Primary, Secondary, Tertiary, Accent, Base, Neutral.
  - Primary: brand/CTAs/links. Secondary: 2nd brand. Tertiary: 3rd, sparing. Accent: rarest. Base: backgrounds + body text. Neutral: greys (borders, dividers, disabled).
- Shade scale per enabled main color (names verbatim): ultra-light, light, semi-light, semi-dark, dark, ultra-dark, plus hover shade. Every shade is overridable in dashboard.
- Variable patterns: `var(--{name})`, `var(--{name}-{shade})`. Examples in docs: `--primary`, `--primary-dark`, `--base-dark`, `--secondary-ultra-dark`, `--neutral`, `--base`, `--white`.
- Example classes in docs: `.btn--primary`, `.bg--ultra-dark`. (`.text--warning-light` example: absent in 4.0.1.)

## Semantic colors
- Names: Warning, Info, Success, Danger (configured under Palette > Semantic Colors). Formerly "contextual colors" pre-3.0.
- Classes: docs list `.text--`, `.bg--`, `.link--` + `{color}`; none are output in 4.0.1 (use `color: var(--...)`).
- Variables: `var(--{name})`, `var(--{name}-{shade})`.
- Partials per status color: `{color}-hex`, `{color}-hsl`, `{color}-h`, `{color}-s`, `{color}-l`, `{color}-rgb`, `{color}-r`, `{color}-g`, `{color}-b`.

## Unified Lightness (Palette > Palette Options)
- Toggles: "Unify Brand Lightness" (Primary, Secondary, Tertiary, Accent, Base base swatch), "Unify Semantic Lightness" (Success, Warning, Info, Danger).
- "Unified Lightness" value 0-1, default 0.65. Only base swatch L changes; shades/hover keep own L.

## Transparencies (4.x)
- No pre-built transparency tokens in 4.x. Removed (older names e.g. `--primary-trans-10`, `--base-ultra-dark-trans-60`).
- Use: `color-mix(in oklch, var(--primary) 20%, transparent)` or relative color `oklch(from var(--primary) l c h / 0.5)`.

## Background & text assignments (dashboard: Backgrounds & Text)
- Backgrounds (class and variable): `.bg--light` / `--bg-light`; `.bg--dark` / `--bg-dark`; `.bg--ultra-light` / `--bg-ultra-light`; `.bg--ultra-dark` / `--bg-ultra-dark`. Default website bg is `var(--body-bg-color)` (staging: `--bg-ultra-light`).
- Text (class and variable, both work with auto relationships): `.text--light` / `--text-light`; `.text--dark` / `--text-dark`; `.text--light-muted` / `--text-light-muted`; `.text--dark-muted` / `--text-dark-muted`.
- Default text color: `var(--text-dark)`, output as `var(--text-color)` (`--body-color` not in build).
- Use classes (not variables) for backgrounds: only classes trigger Automatic Color Relationships.

## Automatic Color Relationships
- Enable: Backgrounds & Text > Options > "Automatic Color Relationships" -> panels "Light Relationships", "Dark Relationships".
- Per relationship inputs: Text Color, Heading Color, Link Color, Button Style (name e.g. `primary`; outline: `primary.btn--outline`). Blank = default.
- `.bg--ultra-dark` etc. auto-flip foreground. `background: var(--bg-ultra-dark)` does NOT trigger it.
- Override one button: custom class + `@include btn(secondary);` or `.bg--ultra-dark :nth-child(2 of [class*="btn--"]) { @include btn(secondary); }`.

## Color scheme (light/dark) - dashboard: Color Scheme (Light/Dark)
- "Enable Color Scheme Support": palette vars output as `light-dark(light, dark)`; shades auto-invert (ultra-light <-> ultra-dark etc.); enables scheme utilities.
- Main and hover colors are NOT auto-inverted; per-color "Color Settings": "Main Color Override" and "Hover Override" (Lightness and Chroma for dark side).
- "Website Scheme" sets `color-scheme` on `:root`: `light only` -> `light`; `dark only` -> `dark`; `light dark` -> `light dark`; `normal`.
- "Force Scheme": "Force Dark Scheme" / "Force Light Scheme" = lists of CSS selectors.
- Classes: `.scheme--light`, `.scheme--dark` (force scheme on subtree).
- Patterns: follow user (`light dark`); manual toggle (set `color-scheme` on root, store e.g. localStorage); default fixed + `.scheme--*` areas. Flipped sections need explicit bg and fg colors to invert properly.
- Custom values: `light-dark(light-value, dark-value)` directly in CSS or dashboard inputs.
