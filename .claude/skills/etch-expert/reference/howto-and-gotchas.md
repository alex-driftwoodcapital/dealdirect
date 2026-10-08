# How-tos, known issues, feature flags

Sources: https://docs.etchwp.com/how-to/basics/{how-to-set-content-width,how-to-set-global-heading-styles,how-to-set-global-section-styles,how-to-install-custom-fonts}, /known-issues, /feature-flags
Verified from docs 2026-10-02. (Only these 4 how-to pages exist in the sitemap; none for JavaScript/HTML attributes. Automatic.css users skip the content-width/heading/section tutorials: ACSS manages them.)
Etch pinned: 1.6.8 (staging, 2026-10-07). Staging-tested facts: `confirmed-on-staging.md`. Block markup examples: `fixtures/`.

## Set content width
Container `max-width` = `var(--content-width)` with fallback `1366px` (undefined variable, so your own value wins). Style Manager (paint brush icon) > Variables Manager tab, add:
```
--content-width: 1280px;
```

## Global heading styles
Attributes Bar (Cmd/Ctrl + Enter) with any element selected, type:
```
{h1} {h2} {h3} {h4} {h5} {h6}
```
Then Style Manager (filter category "Tag"); style by adding the heading to canvas, click selector pill, use CSS Panel. Shared styles selector (wrap in braces to add in Etch):
```
:where(h1,h2,h3,h4,h5,h6)
```

## Global section styles
Sections have no default padding and no gutter (non-ACSS). Add selector in Attributes Bar:
```
{:where(section:not(section section))}
```
(`:where()` = 0,0,0 specificity; `section:not(section section)` = top-level sections only). Variable Manager:
```
--gutter: clamp(16px, 10dvw, 80px);
```
Styles:
```
:where(section:not(section section)) {
    padding-inline: var(--gutter); /* Left and right */
    padding-block: clamp(30px, 5dvw, 80px); /* Top and bottom */
}
```
Docs warn this clamp is not ideal; best uses a formula from content width + minimum device size (clamp calculator or ACSS).

## Custom fonts (Since 1.0.0-rc-5)
Local files (best): (1) enable the custom font upload toggle in Etch Settings (WordPress blocks font uploads by default), save, refresh builder, upload in media library, copy URL path; (2) add `@font-face` to a global stylesheet (e.g. new "Typography" stylesheet) or deploy the `?font-face` recipe:
```
@font-face {
  font-family: "Your Font Name";
  src: url("/wp-content/uploads/path-to-font.woff2") format("woff2");
  font-style: normal;
  font-weight: 400;
  font-display: swap;
}
```
One block per family/weight. Variable font (once per family): `font-weight: 100 900;` with src `.../path-to-font-variable.woff2`. (3) Tokens and defaults:
```
:root {
  --heading-font-family: "My Font Family";
  --text-font-family: "My Font Family";
}
```
```
h1,h2,h3,h4,h5,h6 {
  font-family: var(--heading-font-family);
}
body, p, li, a, button {
  font-family: var(--text-font-family);
}
```
CDN alternative (worse performance, GDPR considerations): put at top of stylesheet, then same tokens:
```
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
```
Selector-system defaults give tree shaking and in-editor identification; stylesheet approach is simpler.

## Known issues (known-issues)
- WIP: Content Hub / CPTs / Custom Fields = functional proof of concept; treat as playground unless needs are basic.
- Quirk: Partial selectors. HTML editor parses classes typed in plain HTML into selector pills, but is debounced and guesses when you're done typing; slow typing creates partial selectors in the style manager. Fix/avoid: add classes via the Attributes Bar instead of the HTML editor.
- WIP: Mini GUI (CSS Quick Actions Bar) is V1; replacing traditional styling panels over time.
- Empty elements: 35px min size in builder only (see elements-and-html.md).
- Firefox may have bugs; Safari interface color bugs (see principles.md).

## Feature flags (feature-flags)
Create valid JSON file `/wp-content/uploads/etch/flags.user.json` (missing or `{}` = all defaults; invalid or empty file = error). You own overrides across updates (your value beats a new default).
```
{
  "FLAG_NAME": "on",
  "FLAG_NAME_2": "off"
}
```
| Flag | Description | Default |
|---|---|---|
| `ENABLE_DEBUG_LOG` | Enables debug logging | `off` |
| `ENABLE_SERVER_TIMING` | Server timing headers for performance monitoring | `off` |
| `RETURN_ACF_DYNAMIC_DATA` | Returns data based on ACF field settings | `off` |
| `ENABLE_CLEAR_BUFFER_IN_STREAM_REQUEST` | Force-clears PHP output buffers on AI streaming requests; enable if AI assistant response comes back empty on your host | `off` |
| `ENABLE_METABOX_LEGACY_MOE` | Legacy Meta Box data retrieval; when disabled uses standard Meta Box format | `on` |
