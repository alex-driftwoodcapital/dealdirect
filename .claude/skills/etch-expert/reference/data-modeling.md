# Data modeling in Etch: assets, custom fields, CPT vs repeater, menu icons
Researched 2026-10-03. Sources at the bottom. "Unconfirmed" = not in official docs, test on staging.
Etch pinned: 1.6.8 (staging, 2026-10-07). Staging-tested facts: `confirmed-on-staging.md`. Block markup examples: `fixtures/`.

## 1. Asset Manager (organize media)
- Etch-native Asset Manager replaces the WP Media Library inside the builder (since Etch 1.6.0; Settings dialog has a toggle). Open from the left settings bar or Command Bar (Cmd/Ctrl+K).
- **Collections** = named groups, like folders, but one asset can sit in several collections. Unassigned assets show under "Uncategorized".
- Create: "+ New Collection" in the sidebar. Rename: double-click or right-click. Move: right-click > "Move into..." / "Move to top level"; drag to reorder. Deleting a collection never deletes assets.
- Assign: drag assets onto a collection or use the collection popover. Uploads go into the currently selected collection (1.6.1); bulk uploads keep their collection (1.6.4).
- Compression presets (1.6.2): save, reuse. Accepts JPG, PNG, WebP, AVIF, SVG, MP4, MOV, PDF, CSV, XLS.
- TwoEleven convention (our choice, not Etch's): collections `Brand` (logos, portraits), `Clients` (client logos by name), `Work` (project shots, one sub-collection per client), `Insights` (post images), `Video`, `Docs`. Name files `client-what-size` before upload. Compress with a preset before upload, not after.
- **Unconfirmed:** nesting depth. Docs page says one level; changelog 1.6.2 says two. Assume one, test on staging. Whether collections show in the WP admin Media Library: not documented.

## 2. Etch custom fields vs SCF
- Etch has its own custom fields (Content Hub; read with `this.etch.field_id`, `item.etch.field_id`). Docs call Content Hub / CPTs / Custom Fields a "functional proof of concept, treat as playground unless needs are basic" (howto-and-gotchas.md). Field types are fewer (image type only added in 1.6.4); repeater/group support in Content Hub: **unconfirmed**.
- SCF (Secure Custom Fields, WordPress.org fork of ACF, free) has 30+ field types incl. Repeater, Flexible Content, Relationship, Options Pages, and registers CPTs/taxonomies. Etch reads it through the ACF namespace: `this.acf.field`, `{#loop this.acf.faq as faq}`, `options.acf.field`.
- **Rule:** Default to SCF for anything we depend on (repeaters, relationships, options pages, anything client-edited long term, anything in schema/loops that must not break). Use Etch custom fields only for simple one-off scalar fields (text, image, toggle) on a single template, where you want zero extra plugin and can afford to rebuild. Never split one object's fields across both. Decision already made: CPTs are registered in SCF (Alex 2026-09-29, no CPT UI plugin).
- Do NOT build field groups by hand on production; test the read-back syntax on staging first.

## 3. New CPT vs repeater vs other
Ask in order; first yes wins.
1. Does each entry need its **own URL/single page**, or SEO of its own? -> **CPT**.
2. Will entries be **added by editors over time** (>~15 expected, or grows monthly), or **queried/filtered/sorted/related** from several places (archive, home highlights, schema, related-to)? -> **CPT**.
3. Is it an ordered list that **belongs to one page or one parent** and is only shown there (steps, features, logos row, 5-10 stats, a page's FAQ)? -> **Repeater** on that page/CPT (SCF Repeater, or an Etch component Group in Repeater mode for component-only data).
4. Is it a single reusable value shared site-wide (address, hours, social links, default CTA)? -> **Options page** field.
5. Is it just a label to group/filter entries? -> **Taxonomy**, not a CPT.
6. Is it a fixed visual block with no editor need? -> plain **Component props** (Etch components support Group and Repeater props).
- Tie-breaker: if two of "own page / grows / reused in 2+ places" are false, it is a repeater.
- Smell test: a CPT with no single pages (`publicly_queryable: false`), under ~15 fixed entries, shown on one page = should have been a repeater.
- Performance: each CPT adds an admin menu item, a query per loop and editing screens; a repeater is one meta read on a page already loaded.

## 4. Every CPT gets a real menu icon
- `register_post_type( ..., 'menu_icon' => ... )` (or the icon field in SCF's post type UI). Default is the Posts pin: never ship it.
- Accepted: a Dashicons class (`dashicons-portfolio`), a base64 SVG data URI (`data:image/svg+xml;base64,...`, SVG must use `fill="black"` so WP recolors it), an image URL, or `'none'` (CSS-styled). Also set `menu_position` (5 below Posts, 20 below Pages, 25 below Comments, 60 first separator).
- TwoEleven picks: service `dashicons-hammer`, project `dashicons-portfolio`, faq `dashicons-editor-help`, problem `dashicons-warning`, testimonial `dashicons-format-quote`, resource `dashicons-book`. Confirm each name exists in the Dashicons list before use. For a brand-specific icon, use a 20x20 `//` mark SVG in the base64 form.
- Etch 1.5.3: CPTs default to Featured Image + hierarchical parent support. Whether Etch's own CPT creator exposes an icon field: **unconfirmed**.

## Could not confirm
Content Hub docs page (404 at docs.etchwp.com/interface/content-hub); repeater in Etch-native fields; collection nesting depth (1 vs 2); collection visibility in the WP Media Library.

## Sources
- Asset Manager: https://docs.etchwp.com/interface/asset-manager
- Etch changelog (1.5.3, 1.6.0-1.6.4): https://etchwp.com/changelog/
- Etch docs index: https://docs.etchwp.com/
- register_post_type menu_icon/menu_position: https://developer.wordpress.org/reference/functions/register_post_type/
- Dashicons: https://developer.wordpress.org/resource/dashicons/
- SCF: https://wordpress.org/plugins/secure-custom-fields/
