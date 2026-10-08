# Block catalogue (Etch 1.6.8, re-verified identical to 1.6.7 export; observed on TwoEleven staging, 2026-10-07)

Counts are across the 9 fixtures. "Observed" means seen in real saved markup; anything not listed here has not been confirmed. Format of every block: `<!-- wp:NAME {json} -->…<!-- /wp:NAME -->`, or self-closing `<!-- wp:NAME {json} /-->` when it has no children.

| Block | n | JSON keys | Notes |
|---|---|---|---|
| `etch/element` | 669 | `metadata.name`, `tag`, `attributes`, optional `styles`, optional `script` | The workhorse. `attributes` is an object (or `[]` when empty). `tag` seen: main, section, div, p, h1-h3, span, a, nav, ul/ol/li, article, aside, header, footer, figure/figcaption, blockquote/cite, button, form, fieldset/legend, label, input, textarea, dialog, dl/dt/dd, strong/b/i/small/br, svg/g/path/circle/rect |
| `etch/text` | 371 | `metadata.name`, `content` | Self-closing. Text lives only here, inside an element. `content` may contain `{props.x}` / `{item.field}` expressions |
| `etch/component` | 14 | `ref` (wp_block post ID), `attributes` (props), optional `metadata.name` | Instance of a component. `ref` is a site-specific post ID. Prop values can be strings, `"{true}"`/`"{false}"` strings for booleans, or strings holding `{{…}}` JSON for object props (see header fixture) |
| `etch/slot-content` | 3 | `name` | Child of a component instance; content for the named slot (e.g. `menuContent`) |
| `etch/slot-placeholder` | 1 | `name` | Inside a component definition; where slot content renders (`callout-band`, slot `extra`) |
| `etch/condition` | 6 | `condition{leftHand,operator,rightHand}`, `conditionString` | Wraps children. Operators seen: `isTruthy` (14, with `rightHand:null`) and `\|\|`. Docs also list `&&` `==` `!=` `===` `!==`. Both `condition` and `conditionString` are present. `{#else}` still unconfirmed |
| `etch/loop` | 2 | `loopId`, `itemId` | `loopId` is a key in `etch_loops` (`prjfeat`, `prjmore`); `itemId` is the variable name for children (`project`) |
| `etch/dynamic-image` | 10 | `tag:"img"`, `attributes{mediaId,useSrcSet,loading,alt}` | `mediaId` is a WP media ID string or an expression (`{project.etch.screenshot.id}`). `useSrcSet` and `loading` are strings. Never a plain `img` element |
| `etch/raw-html` | 3 | `content`, `unsafe` | `unsafe:"false"` seen (sanitized, e.g. `<p>{project.etch.testimonial}</p>`). Needs the Etch security setting for `unsafe:"true"` |
| `post-content` | 1 | `align`, `layout` | WordPress core block. Only in `template-home.html` |

## Patterns

- **Class vs styles:** `attributes.class` holds the readable class name(s); `styles` is an array of style IDs (keys of `etch_styles`). Both are present on styled elements. Built-in IDs: `etch-section-style`, `etch-container-style`, `etch-flex-div-style`, keyed to `data-etch-element` = `section` / `container` / `flex-div`.
- **Section skeleton:** `section[data-etch-element=section]` → one `div[data-etch-element=container]` → content. Both carry their built-in style IDs. Sections also use `aria-labelledby` pointing at the heading's `id`, and `data-nav-label` for the in-page nav.
- **Class escape:** a double hyphen is stored as `--` inside JSON strings (e.g. `btn--base`). Keep it as written.
- **Scripts:** an element's `script` is `{"code":"<base64 of JS>","id":"<7 chars>"}` (15 elements). Decode to read, re-encode to write. `id` is unique per script.
- **Props in components:** definition markup uses `{props.key}`; instances pass `attributes:{key:value}`. Empty instance is `"attributes":[]`.
- **Data hooks:** JS hooks are `data-*` attributes (`data-newsletter-open`, `data-header-actions`, `data-plan`).
- **Metadata names:** every block has `metadata.name`, shown in the builder tree; set a meaningful one.
- **Entities:** `<`, `>`, `&`, `"` inside JSON strings are `<` `>` `&` `"`.

## Gaps (not covered by any fixture)

- Etch's own `etch/` blocks beyond the nine above (e.g. any query/pagination/icon/SVG block) were not seen; SVGs here are plain `svg`/`path` elements.
- `{#else}`, other condition operators, loop pagination, `unsafe:"true"` raw HTML.
- Component prop schema JSON (re-export in a later thread).
- Single-post template and Index template markup (only the Home template was exported).
