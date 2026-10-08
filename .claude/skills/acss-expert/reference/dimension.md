# ACSS 4.x dimension

> **4.0.1 check (2026-10-07, see staging-4.0.1-facts.md):** `.content-width`, `.content-width--safe`, `.width--10..90`, `.width--auto|full|fit-content|max-content|min-content`, `--gutter`, `--content-width` (69.5rem), `--content-width-safe` are all confirmed in the build. `.breakout--*` is absent (3.x only): use Content Grid zones. `.content-offset--off` is only a default exclusion selector, not an output class.
Sources (verified from docs 2026-10-02): https://docs.automaticcss.com/dimension/content-width , /dimension/content-width-safe , /dimension/width-utilities , /dimension/boxed-layout , /dimension/header-height , /dimension/scroll-offsets , /dimension/auto-object-fit ; breakout: https://docs.automaticcss.com/3.0/dimension/breakout-classes (3.x only)
NOTE: /dimension/breakout-classes does not exist in 4.x docs (404); breakout content below is from the 3.0 tree, unverified for 4.x (3.x text suggests Content Grid as the alternative for full-bleed).

## Content width
- Set in dashboard Layout > Website Dimensions (4.x; formerly Viewport tab): "Content Width" (desktop) and "Minimum Width" (narrowest viewport for fluid calcs).
- Class `.content-width`: sets `max-inline-size: var(--content-width)` (4.x; was max-width). Variable `var(--content-width)` (always available).
- Pattern for custom elements: `width: 100%; max-width: var(--content-width);`. Fractions: `max-width: calc(var(--content-width) * 0.75);`.
- Use `var(--content-width)` in builder instead of static value.

## Content width safe (gutter-aware)
- `var(--gutter)` = responsive inline gutter (sections use it for padding-inline).
- `var(--content-width-safe)` = `min(var(--content-width), calc(100% - var(--gutter) * 2))`.
- Class `.content-width--safe`: `inline-size: 100%; max-inline-size: var(--content-width-safe); margin-inline: auto;`. With the variable you must add `margin-inline: auto` yourself.
- Use only where parent has no gutter (section with 0 inline padding, or no section) - otherwise double gutter. Use plain `.content-width` when parent has a gutter.

## Width utilities
- Classes `.width--10` ... `.width--90` (steps 10,20,...,90): `inline-size: 100%; max-inline-size: calc(var(--content-width) * 0.N)` (e.g. `.width--20` = * 0.2). Only output when "Width" option is on (Options).
- Variables `--width-10` ... `--width-90` (= `calc(var(--content-width) * 0.N)`), only when "Width Variables" on (Options > Variable Manager). `--content-width` unaffected.
- Special classes: `.content-width`, `.content-width--safe`, `.width--full` (inline-size 100%; max 100%), `.width--auto` (inline-size auto; max 100%), `.width--max-content`, `.width--min-content`, `.width--fit-content` (each max-inline-size 100%).

## Boxed layout (Layout > Boxed Layout toggle)
- Settings: Device Background (background shorthand; default `--white`), Body Width, Top Margin (no bottom margin possible), Border Style / Border Width / Border Color (top right bottom left syntax), Border Radius, Body Shadow (box-shadow on body).
- Structure: `html` = edge-to-edge canvas; `body` = fixed width container.

## Header height (Layout > Header)
- Header Sizing: "Header Height (Desktop)" and "Header Height (Mobile)" (px) -> fluid `--header-height`.
- Toggles: "Offset Content Automatically" (adds `margin-block-start: var(--header-height)`), "Offset Scroll Margin Automatically".
- Header Exclusions (when offset on): Exclude Headers default `[data-sticky-header='0'], .content-offset--off`; Exclude Pages (body selectors e.g. `.page-id-2`, `.post-type-services`).
- Sticky: Additional Styling > Sticky > "Offset Sticky Automatically"; `.sticky` class; per-element override `--sticky-offset` or `inset-block-start`.

## Scroll offsets (Additional Styling > Scroll Offsets)
- "Scroll Offset (Desktop)" and "Scroll Offset (Mobile)" (px), added on top of header-height offset (if Offset Scroll Margin Automatically on).

## Auto Object Fit (Options > Workflow Enhancements)
- Sets every `img`: `object-fit: var(--object-fit, cover); object-position: var(--object-position, 50% 50%);`. Override by setting `--object-fit` / `--object-position` on a parent.
