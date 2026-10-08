# ACSS 4.x Functions, Mixins, Recipes, WP-CLI
Sources: https://docs.automaticcss.com/mixins/{what-are-mixins,breakpoint-mixins,center-mixin,heading-text-style-mixins,line-clamp-utilities,button-mixins,border-mixin,icon-mixin,focus-parent,clickable-parent,gradient-fades,texture-overlay-mixins,auto-grid-mixin,content-grid-mixin,card-container-mixin} , /recipes (+ /recipes/{grid,flex,column,button,border-radius,card-container,color,content-grid,custom-property,divider,gradient-fades,ipsum,javascript,list,media-query,overlap,query-loop,text,accessibility}-recipe(s)) , /cli (+ /cli/{settings,css,status,logs,doctor,flags,license}) ; functions: https://docs.automaticcss.com/3.0/functions/{calc,ctr,fluid-function,percent-function,pow-function,rem-function}
verified from docs 2026-10-02
> **4.0.1 check (2026-10-07):** `/functions/*` still 404 on docs.automaticcss.com (listed in sitemap) and `/3.0/functions/*` is the only source. 4.x pages (fluid-text, fluid-headings, section-padding-classes) still say custom sizes can be made "using the fluid() function" without syntax, so `fluid()` exists but its 4.x signature is unconfirmed; a compiled stylesheet cannot prove SCSS. Prefer native `clamp()` with ACSS tokens and the bridge variables (`--space-l-to-xs`), which are verified. Recipe names `?grid-N ?auto-grid ?variable-grid ?flex-* ?center-* ?columns ?content-grid ?clickable-parent ?focus-parent ?divider-* ?concentric-radius ?btn ?card-container ?breakpoint-*` are documented 4.x and unchanged; `?{color}-clr` is stale (expands to non-existent `--primary-h/-s/-l`). `?` recipes cannot be seen in the compiled CSS: expand them in the builder.

Caveat: the 4.x URLs /functions/{calc,ctr,fluid-function,pow-function,rem-function} are listed in the sitemap but return 404. Function syntax below is from the 3.0 docs (marked 3.x) and was not re-confirmed for 4.x.

## Functions (3.x docs; Custom SCSS area only; cannot be used directly in `:root`, interpolate `#{}`)
- `fluid(min, max)` generates clamp from px min/max: `:root { --h1-hero: #{fluid(28,60)}; }` ; `.gap--3xl { gap: fluid(60, 80); }`
- `ctr(24)` px to rem (convert-to-rem): `padding: ctr(24);` In `:root`: `$my-custom-value: ctr(24); :root { --my-custom-value: #{$my-custom-value}; }`
- `rem(value)` attaches rem unit: `$my-custom-width: rem($vp-max * .33);` (`$vp-max` = unitless site width)
- `percent(value)`: `$my-percent: percent(5 * 5);` => 25%
- `pow(base, exp)`: `$my-pow: pow($my-text-size, 3);` (2.4 => 13.824)
- `calc()` is standard CSS; examples: `gap: calc(var(--content-gap) / 2);` ; `--primary-trans-5: hsl(var(--primary-h) calc(var(--primary-s) / .2) var(--primary-l))`

## Mixins (Custom SCSS area of ACSS dashboard only; not builder inputs/CSS). Use `@include name(args)`. Args are positional in order; later args need earlier ones answered (or name them `$arg: value`).
- Button: `@include btn($style, $props);` `$style` default `primary`, `$props` default `yes` (`no` outputs only scoped vars, use on `.btn--` prefixed classes): `@include btn(secondary, no);` Styles: `primary|secondary|tertiary|accent|base|neutral` + `-light` / `-dark`; outline quoted: `@include btn("primary.btn--outline");` (see components.md)
- Breakpoint: `@include breakpoint(ext) { }` (max-width) ; `@include breakpoint-up(ext) { }` (min-width). ext examples: xl, l, m, s.
- Center: `@include center($alignment, $output);` `$alignment` (default `all`): `all|left|right|top|bottom`; `$output`: `full|core|tokens`. e.g. `@include center(left);` ; at breakpoint `@include breakpoint(l) { @include center(left, tokens); }`. Selector is output doubled by design (specificity).
- Heading/text style: `@include heading-style(h2);` ; `@include text-style(l);` (page prose also writes `@heading-style();`/`@text-style();`; code uses `@include`). Null properties not output.
- Line clamp: `@include line-clamp($line-count);`
- Border: `@include border($style, $position, $radius);` (see surfaces.md)
- Icon: `@include icon($style, $box-style);` (see components.md)
- Card: `@include card;` ; `@include card-container("inline-size > 767px") { }` (see components.md)
- Focus/clickable parent: `@include focus-parent(shadow|outline);` ; `@include clickable-parent;` (on the `a`/`button`; see accessibility.md)
- Fade: `@include fade($axis, $amount);` axis block|inline|top|right|bottom|left, amount default 25%
- Textures: `@include texture(1);` `@include texture-overlay(1);`
- Grids: `@include auto-grid($column-count, $min, $flow, $force-even-column-count);` ; `@include content-grid;` (see layout.md)

## Utility class: line clamp
`.line-clamp--1` .. `.line-clamp--5`, `.line-clamp--custom` (+ `--line-count` var, set at ID level). Recipe `?line-clamp` (text-recipes: choose count via `--line-count`).

## Recipes (type `?name;` in builder custom CSS or Custom SCSS; semicolon triggers expansion; 4.0 changed prefix from `@` to `?`; needs Options > Workflow Enhancements variable expansion)
- Layout: `?grid-1`..`?grid-12`, `?grid-1-2 ?grid-1-3 ?grid-2-1 ?grid-2-3 ?grid-3-1 ?grid-3-2`; `?auto-grid` (`--column-count`, `--min`); `?variable-grid` (`--min`); `?content-grid;`; `?columns` (vars in layout.md); `?flex-row ?flex-column ?center-all ?center-left ?center-right ?center-top ?center-bottom ?flex-grid`
- Buttons: `?btn` (custom button vars; attach to `.btn--custom`)
- Cards: `?card-container` (e.g. `%root% { @container card ( inline-size >= 767px ) { ... } }`)
- Accessibility: `?clickable-parent`, `?focus-parent`
- Colors: `?{color-name}-clr` => `hsl(var(--primary-h) var(--primary-s) var(--primary-l) / 1)` (e.g. `?primary-clr`); shades `?{color-name}-{shade}-clr`
- Borders/dividers: `?concentric-radius` (sets parent padding via `var(--padding)`; inner radius default `var(--radius)`); `?divider-top`, `?divider-bottom`, `?divider-all`
- Custom property: `?property;` (Houdini `@property` declaration)
- Media queries: max-width `?breakpoint-xs ?breakpoint-s ?breakpoint-m ?breakpoint-l ?breakpoint-xl ?breakpoint-xxl`; min-width `?breakpoint-up-xs ?breakpoint-up-s ?breakpoint-up-m ?breakpoint-up-l ?breakpoint-up-xl ?breakpoint-up-xxl`
- Lists/text: `?list-none;` (apply on the list; class equivalent `.list--none`), `?line-clamp`
- Fades: `?fade-block; ?fade-inline; ?fade-top; ?fade-right; ?fade-bottom; ?fade-left;`
- Misc: `?ipsum-short` (lede dummy paragraph), `?script` (`<script type="module"> </script>` wrapper), `?query-children` (nested query loops in compatible builders)
- Overlap: `?overlap;` (background-style extending from top of box to a stop point), `?overlap-alt;` (background on adjacent sibling box, overlap extends up into target). Vars: `--background` (any background shorthand), `--foreground`, `--overlap-amount`, `--overlay` (must remain `linear-gradient(...)`, e.g. `linear-gradient(var(--black-trans-10), var(--black-trans-10))`). Pseudo tweaks: `%root% + *::before { border-radius: 0 150px 0 0; }` / `{ clip-path: polygon(0 10%, 100% 0, 100% 100%, 0% 100%); }` (page writes the vars with en dashes; real syntax is `--`).
- `%root%` = placeholder for the current element's selector in builder CSS (used in docs examples).

## WP-CLI (`wp acss`, ACSS 4.x; needs WP-CLI, shell access; use `wp help acss <cmd>`)
| Command | Purpose |
|---|---|
| `wp acss settings` | get, set, list, export, import, reset |
| `wp acss css` | regenerate stylesheets |
| `wp acss status` | version, builders, CSS files, flags |
| `wp acss logs` | tail, clear, path |
| `wp acss doctor` | health checks |
| `wp acss flags` | list, get, set, unset, path |
| `wp acss license` | get, set, activate, deactivate |

- `wp acss settings get [<key>] [--format=json|yaml|var_export]` (e.g. `get color-primary`)
- `wp acss settings set <key> <value> [--force] [--skip-css]` (`--force` skips schema validation)
- `wp acss settings list [--search=<pattern>] [--format=table|json|csv|yaml|count]`
- `wp acss settings export [--file=<path>]` (stdout if omitted)
- `wp acss settings import <file> [--force] [--skip-css] [--yes]` (replaces ALL settings; no auto backup)
- `wp acss settings reset [--skip-css] [--yes]` (wipes all config)
- `wp acss css regenerate` (writes `/wp-content/uploads/automatic-css/automatic.css` and `automatic-variables.css`; errors if no settings saved)
- `wp acss status [--format=text|json|yaml] [--section=plugin|integrations|css|settings|flags]`
- `wp acss logs tail [--events=<n>] [--lines=<n>] [--type=activity|debug] [--follow]` (defaults: type activity, events 20, lines 100)
- `wp acss logs clear [--type=activity|debug|all] [--yes]`
- `wp acss logs path [--format=table|json|yaml]` (logs: `activity.log`, `debug.log` in `wp-content/uploads/automatic-css/`)
- `wp acss doctor [--format=text|json] [--fix]` (checks PHP 8.1+, WP 5.9+, perms, config, CSS file age >7 days warn, builders; `--fix` creates uploads dir)
- `wp acss flags list [--format=table|json|yaml]`, `flags get <flag>`, `flags set <flag> <on|off>`, `flags unset <flag>`, `flags path [--format=table|json]` (sources by priority: `flags.user.json` in uploads/automatic-css, `flags.dev.json`, `flags.json`; run `css regenerate` after set)
- `wp acss license get [--format=table|json] [--show-key]`, `license set` (key via hidden prompt or stdin only: `printf '%s' "$ACSS_LICENSE_KEY" | wp acss license set`), `license activate`, `license deactivate`
- CI patterns: `wp acss status --format=json | jq '.css'` ; `wp acss settings import ./config/acss-settings.json --yes --skip-css` then `wp acss css regenerate` ; `wp acss doctor --format=json > /tmp/acss-health.json`
