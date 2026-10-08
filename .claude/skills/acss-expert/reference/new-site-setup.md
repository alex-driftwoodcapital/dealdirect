# New site setup checklist (ACSS 4.x)
Order matters: settings first, export, then profile, then build. Official: /setup/how-to-install-acss, /dimension/content-width, /spacing/standard-spacing-setup, /typography/fluid-text, /colors/palette-intro, /setup/builder-configuration/etch (Etch needs no setup). Values below name the key in `acss-settings.json` (what to read after export).

1. **Install and license** (WordPress: upload plugin, Automatic.css > License, use the key labeled "Automatic.css"; with WP-CLI `wp acss license set` then `wp acss license activate`). Never put the key in files.
2. **Dimensions** (Layout > Website Dimensions): content width and minimum width. Keys `vp-max`, `vp-min`. Must equal the builder's container width. There are no breakpoints in 4.x.
3. **Palette** (Palette): enter brand hexes for primary, secondary, tertiary, accent, base, neutral; turn on only colors used (`option-*-clr`). Keys `color-*`. Enable semantic colors only if forms/alerts need them. Decide Unified Lightness (`option-palette-unify-*`).
4. **Color scheme**: `website-color-scheme` (`light only` unless the brand ships dark mode). Backgrounds & Text: set `bg-*`, `text-*` assignments and Automatic Color Relationships.
5. **Spacing** (Spacing): base (`base-space`, `base-space-min`) and scales (`space-scale`, `mob-space-scale`), section adjustments, gutter. Turn on Smart Spacing and contextual gaps as needed (`option-gaps` = utility classes `.grid-gap` etc.; variables always exist).
6. **Typography**: root font size (100%), `text-scale`, `text-m-min/max`, heading min/max (`h1-min..h6-max`), line heights, font family (`text-font-family`; custom fonts via Typography > Fonts, file path relative).
7. **Buttons**: enable the colors needed (`option-*-btn`, `option-*-btn-outline`), radius, padding, weight, min width.
8. **Modules**: turn on only what the build uses: cards (and list selectors), forms, effects (enter/exit/hover/visible), sticky, overlays, surfaces, border/shadow/radius sizes. Unused modules emit no CSS: a class missing in the stylesheet usually means its module is off.
9. **Focus and motion**: Additional Styling > Focus; leave Reduce Motion on.
10. **Regenerate and export**: `wp acss css regenerate`; copy `wp-content/uploads/automatic-css/automatic.css`; `wp acss settings export --file=acss-settings.json` into `skills/acss-expert/index/` (or `profiles/<site>/`).
11. **Index and profile**: `python3 -I scripts/build-index.py`; copy `index/site-profile.template.md` and fill from the export; commit.
12. **Smoke test**: build one section with the profile, run the verify pass (thread 4), view at 375 and 1440, no horizontal overflow.
Refresh on every ACSS update: repeat 10-11 and diff `acss-index.json`.
