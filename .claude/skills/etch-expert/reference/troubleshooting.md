# Etch troubleshooting, migration, and documented gotchas
Sources: https://docs.etchwp.com/troubleshooting/activity-log , /troubleshooting/performance-issues , /migration-guides/v1-migration ; gotchas collected from /components/props/prop-object , /components/slots , /components/props/prop-loop , /loops/nested-loops , /dynamic-data/dynamic-data-keys , /facets/third-party-facets/* , /etch-connector/usage , /integrations/custom-fields/options-pages
Verified from docs 2026-10-02.
Etch pinned: 1.6.8 (staging, 2026-10-07). Staging-tested facts: `confirmed-on-staging.md`. Block markup examples: `fixtures/`.

## Activity log
- Records one event per request (operation, success/failure, context): errors always logged, successes sampled; auto-rotates. Records request URLs, plugin version, timing, status; no passwords, personal info, or tokens.
- File: `wp-content/uploads/etch/activity.log` (plus `.log.1`, `.log.2`). Safe to delete. For support: download via FTP/file manager and share.
- Apache/LiteSpeed: Etch auto-creates `.htaccess` blocking access. Nginx (manual):
```
location ~* /wp-content/uploads/etch/.*\.log$ {
    deny all;
}
```
- IIS (manual, `web.config`):
```
<location path="wp-content/uploads/etch">
    <system.webServer>
        <security>
            <requestFiltering>
                <fileExtensions>
                    <add fileExtension=".log" allowed="false" />
                </fileExtensions>
            </requestFiltering>
        </security>
    </system.webServer>
</location>
```

## Performance issues
- Symptoms: server errors (PHP workers/memory), host rate limits (Kinsta, WP Engine, Cloudways) causing failed saves/missing data, slow admin, DB connection errors.
- Since 1.4.20: cap concurrent builder API requests in `wp-config.php` (default: no limit; docs suggest starting at 5, lower = less load but slower builder):
```
define( 'ETCH_API_CONCURRENCY_LIMIT', 5 );
```
- Raise worker limits gradually (each worker uses memory): Apache `mpm_event`/`mpm_worker` -> `MaxRequestWorkers`; PHP-FPM -> `pm.max_children`; XCloud -> PM Max Children.

## Migration to 1.0.0 (/migration-guides/v1-migration)
- 1.0.0 is first stable release; support ended for pre-alpha, alpha, beta. Step through stages in order (skipping risks incomplete migration or data loss). Back up first.
- Path: (1) full backup; (2) pre-alpha/alpha -> `1.0.0-alpha-15` (required; migration modal on open, follow it); (3) alpha/beta -> latest beta `1.0.0-beta-15`; (4) beta/RC -> `1.0.0`.
- Known caveats: move to custom Gutenberg blocks (data migration in alpha-15), changes to dynamic data handling, internal API/block definition refinements.

## Documented gotchas (symptom -> docs-stated cause/fix)
- Loop keys (`{post.title}`, `{item.name}`) empty inside a component -> components have own scope (only `this`, `site`, `url`, props). Pass via Object Prop: `{props.post.title}`; instance `<PostCard post="{post}" />` / `object="{item}"`. Loop and its markup must be on the same side of the component boundary.
- Nested loop stops working after extraction to component -> move the nested loop inside, loop over `props.product.terms`.
- Slot content can't see per-iteration loop data -> put component (not slot) inside the loop.
- Loop prop errors -> key must be camelCase or bracket notation; no extra braces: Incorrect `{#loop {props.myFeatures} as item}{/loop}`, Incorrect `props.your-loop-prop`.
- Select prop not working -> need spaces: `key : value`.
- Nested loops with same variable name (`item`/`item`) -> inner hides outer; rename (`author`/`book`). Pre-1.6.8 inner fell back to outer.
- Property names with dashes/spaces -> bracket notation `{item["post-meta"]}`.
- URL parameters case sensitive: `{url.parameter.Name}` not `{url.parameter.name}`.
- Empty loop renders nothing; workaround `{#loop posts.length().equal(0, [1], []) as item}`.
- Loop arg default `$count ?? 1` repeated with different defaults -> first declared default wins.
- `{#if}` can't be used inline in attributes -> use comparison modifiers (`.equal()`, `.greater()` ... with true/false values).
- String vs number in conditions: `props.rating === "2"` compares text; `props.rating >= 2` compares number (no quotes).
- Native "Post" type has no archive; Main Query loops only meaningful on archive-like contexts (results may be empty otherwise).
- FacetWP: facets must sit outside `facetwp-template` container (console error "Facets should not be inside the 'facetwp-template' container"); no effect -> check `'facetwp' => 'true'`; no pagination -> need finite `posts_per_page` + Pager facet; only one FacetWP-enabled query per page.
- WP Grid Builder: facet inert -> `wp_grid_builder` value must exactly match parent class and shortcode `grid`; wrong content updating -> unique `wpgb-content-*` per loop; class goes on the loop's direct parent.
- Options key outputs nothing (`{options.acf.field_name}`) -> field must exist on an Options Page, exact name/key, saved value.
- Connector: no connect button -> Settings -> AI -> turn on AI Connector; chat can't reach Etch -> re-run `npx @digital-gravy/etch-connector serve` in a chat (original chat closed ends connection); don't navigate away from builder tab; one tab per site.
- Public API: method throws `NOT_AVAILABLE` -> capability not backed on this runtime; use `etch.environment?.capabilities.<name> === true`. Unknown component prop key -> `INVALID_ARGUMENT`. Invalid parent for block -> `WRONG_BLOCK_TYPE`.
- Etch Intelligence not showing -> Settings -> Experimental -> AI Assistant on + OpenAI key + Save.
