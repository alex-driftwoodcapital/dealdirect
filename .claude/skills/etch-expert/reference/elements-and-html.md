# Elements, HTML, attributes, selectors

Sources: https://docs.etchwp.com/elements/{overview,section,container,div,text,heading,anchor,image,dynamic-image,svg,html,element,empty-elements,loop,condition,iframe}, /interface/{attributes-bar,selector-pills,html-panel}, /utilities/quick-notes
Verified from docs 2026-10-02.
Etch pinned: 1.6.8 (staging, 2026-10-07). Staging-tested facts: `confirmed-on-staging.md`. Block markup examples: `fixtures/`.

## Element list (overview)
Anchor, Condition, Container, Div, Dynamic Image, Element, Empty Elements, Heading, Html, Iframe, Image, Loop, Section, Svg, Text. (Interactive widgets are "Components (Native)", separate.)

## Section + Container
Structure produced:
```
<section data-etch-element="section">
  <div data-etch-element="container">
    <!-- Your content here -->
  </div>
</section>
```
Section defaults: `display: flex; flex-direction: column; align-items: center;`
Container defaults: `display: flex; flex-direction: column; width: 100%; max-width: var(--content-width); align-self: center;`
- Defaults have 0,0,0 specificity; removing the `data-etch-element` attribute removes the defaults entirely.
- Target all containers: `:where([data-etch-element="container"]) { /* Default Styles */ }`
- Section can hold multiple containers or none. Containers have no gutter: use inside Section (header/footer are more precise sections); if inside a div, set a gutter on the parent div.
- Change container width via the variable: `.my-container { --content-width: 460px; }` (good) vs `max-width: 460px;` (not as good).
- Section rules: always include a heading (first section on page `H1`, others start `H2`); no heading -> probably should be a `div` not `section`; meaningful section names ("Product Features" not "Gray Box"); keep sections focused; proper heading hierarchy h1 -> h2 -> h3, don't skip levels; don't use as generic container (use `<div>`); don't nest unnecessarily.
- Top-level sections need block padding + inline padding (gutter) defaults unless using Automatic.css. Group related content in separate containers (heading+intro in one, grid in another).

## Div / Text / Heading / Anchor
- Div: `<div></div>`, no default styling; `display: block` so set `display: flex` before using flex alignment/gap.
- Text: `<p>` by default; tag can change to `span`, `li`, any valid element. Do NOT use a single Text element for rich text (multiple paragraphs) or as wrapper for rich dynamic data.
- Heading: `<h2>` by default; change tag only for semantics, never to change font-size/visual style (use CSS).
- Anchor: `<a href="#">Hyperlink</a>`; `href=""` mandatory (auto-added); `target="_blank"` via Attributes bar or HTML editor. Anchors = navigation; on-page events (modal, carousel) need `<button>`. Buttons that look like links: style with CSS, don't change tag for looks. Make a button by changing tag to `<button>` (remove anchor attributes) or by Text/Div with tag `<button>`. No literal Button element in Etch.

## Image / Dynamic Image / SVG
- Image: `<img src="path/to/image.jpg" alt="Description of the image" />`; `src` mandatory, `alt` for accessibility; `size` attribute picks WP size; `srcset`/`sizes` automatic. Optional `loading="lazy"|"eager"`, `decoding="async"|"sync"`. Dynamic data as src: `<img src="{item.featuredImage}">`. All attributes support dynamic data.
- Figure: right-click image -> "wrap with div", change `div` to `figure`; add Text inside, change `p` to `figcaption`.
- Custom WP sizes (functions.php) need regenerate-thumbnails; docs example uses add_image_size( 'image-480', 480, 9999 ) ... 'image-1920' + filter `image_size_names_choose`.
- Dynamic Image: `<etch:img />` renders WP image by media ID with `alt`, `src`, `srcset`, `sizes`. Attributes: `maximumSize`, `useSrcSet` (`false` disables srcset/sizes); custom `alt` overrides media library. Other attributes pass through to `<img>` except `src`, `maximumSize`, `useSrcSet`. Works with media/text props; loop over media IDs for galleries.
- SVG: `<etch:svg />`; `src` accepts any valid SVG URL (incl. external). Component use: Image prop "Icon", `{props.icon}` in `src`. `stripColors="true"` converts hardcoded colors to currentColor (color via CSS/inherit). Raw `<svg>` HTML is also natively supported.

## Special/ghost elements
- HTML element: `<etch:html content={item.your-rich-text} unsafe="false" />` (self-closing; `<etch:html />` not `<etch:html>foo</etch:html>`). Attributes: `content` (dynamic data/prop key), `unsafe` (default `false`; false = sanitized to `wp_kses_allowed_html('post')`; true = no sanitization incl. `<script>`, `<iframe>`, XSS risk). Parent of rich text must be `div`, not `p`/`span`. Add via right-click -> "Convert to Raw HTML" (recommended), component/template editor icon, or code editor.
- Dynamic Element: `<etch:element tag="div">`; tag accepts dynamic data, e.g. `<etch:element tag={props.headingLevel}`; Tag input is a combobox accepting any value; avoids conditional logic for tag swaps (e.g. h1 vs h2 in a Section Intro component).
- Loop element: ghost, no DOM output; provides loop context/controls (see /loops/basic-loops).
- Condition element: ghost, no DOM output; inline conditional logic.
- Iframe: page says "More to come...".
- Empty elements: builder-only 35px min size; override with `--empty-element-size` (element/section level, e.g. `.my-element { --empty-element-size: 20px; }`); `:root { --empty-element-size: 0; }` not recommended.

## Attributes Bar (Cmd/Ctrl + Return, or "+" in HTML/CSS panel header)
Accepts multiple attributes and selectors mixed. Examples verbatim:
- `.my-class` ; `#my-id` ; `.my-class #my-id`
- Random: `.rand` (also `#rand`)
- Pseudo: `.my-class:hover .my-class::before .my-class::after`
- Plain attributes (no selector generated): `data-attribute="my-data" aria-label="This is accessible"`
- Attribute selector (bracketed): `[data-attribute="my-data"]`
- Complex/compound selectors need braces: `{.hero h1}` (any valid CSS selector). Tag selectors: `{h1} {h2} {h3} {h4} {h5} {h6}`; grouped `:where(h1,h2,h3,h4,h5,h6)`.
- Docs suggest CSS nesting on the parent selector is often better than separate pseudo/complex selectors.

## Selector pills
- Valid selector -> pill in CSS editor; styles apply to selected pill. Rename: double-click pill or Style Manager. Remove via X on hover (manual selectors only); delete via right-click -> Delete or Style Manager (removes from DB).
- Complex selectors like `{.my-section h1}` are not removable from elements; edit to exclude: `{.my-section h1:not(.special-heading)}`. Pill appears on the element actually selected (the `h1`, not the section).
- No pill after adding a class: forgot the "." or the complex selector doesn't match the selected element.

## HTML panel (CodeMirror)
- Live HTML of page; edits reflect on canvas. Auto-complete tags/attributes; error highlighting; folding. Quick Notes: attribute `data-etch-note="This section needs review before launch"` (builder-only; stripped on frontend; toggle in Structure Panel settings).
