# Etch templates, dynamic data, loops, conditions, facets
Sources: https://docs.etchwp.com/templates/* , /dynamic-data/dynamic-data-intro , /dynamic-data/dynamic-data-keys , /dynamic-data/dynamic-data-modifiers/{basic,arithmetic,comparison}-modifiers , /dynamic-data/dynamic-data-integration/* , /loops/{basic-loops,loop-arguments,main-query,nested-loops,looping-attachments} , /conditional-logic/{intro-to-conditional-logic,basic-conditions,advanced-conditions} , /facets/*
Verified from docs 2026-10-02. (Condensed; code verbatim.)
Etch pinned: 1.6.8 (staging, 2026-10-07). Staging-tested facts: `confirmed-on-staging.md`. Block markup examples: `fixtures/`.

## Templates
- Templates author to WordPress FSE templates. Required: Index (`index`). Recommended: `single`, `archive`, `author`, `404`. Template Manager: column layout; new CPT/taxonomy adds columns. Search Results created under "Miscellaneous"; 404 from Template Hub (Miscellaneous).
- Index template (already exists; edit in Template Manager) minimum: header component, Content Slot, footer component; Div with HTML tag `main` between them + Content Slot element.
- Post Content: use `{@post-content}` (not `{this.content}`); not subject to slot logic.
```
<main>
    {@post-content}
</main>
<article>
    {@post-content}
</article>
```
- Page templates: only override index for pages; docs call them "dinosaur architecture", prefer CPTs. Author template: "More to come...". Native "Post" type has no archive: make a page and use a standard post loop. Single templates: keys via `this.` (`this.title`). Archive templates: use Main Query loop.
- Search results: new template has `<main>` with `{@post-content}`; replace with:
```
<main>
  <section data-etch-element="section" class="search">
    <div data-etch-element="container" class="search__header">
      <h1 class="search__title">Search results for: {url.parameter.s}</h1>
    </div>
    <div data-etch-element="container" class="search__results">
      {#loop mainQuery as item}
        <article class="search-card">
          <h2 class="search-card__title"><a href={item.permalink.relative}>{item.title}</a></h2>
          <div class="search-card__description">{item.excerpt}</div>
        </article>
      {/loop}
    </div>
  </section>
</main>
```
`{#loop mainQuery($count: 10) as item}` limits. Docs recommend WS Form for the search form.

## Dynamic data syntax
- Expression `{key}`. Namespaces: `this` (templates), `taxonomy`/`term`, `item` (loops, name is yours), `user`, `site`, `url`, `options`, `component`, `environment`, `props`, `slots`.
- Dot notation: letters, digits, underscore only. Otherwise bracket notation: `{item["full name"]}`, `{item["post-meta"]}`, `{item[0]}`, `{this["page title"]}`, `{item["author-info"]["email"]}`, `{this.categories[0].name}`, `{item["users"][0]["display-name"]}` (single or double quotes). Old dash/space dot syntax unsupported.
- Arrays: `{#loop categories as category}<span>{category.name}</span>{/loop}`; `{this.categories.at(0).name}` = `{this.categories[0].name}`; zero-based, `-1` = last.
- Literal braces: `{"{This will be output as is}"}`. Output `{this}` (or Loop Manager) to see full JSON. Object keys need a sub-key (`{item.author.displayName}`).

## Dynamic data keys
Post/item: `id` `title` `slug` `content` `excerpt` `permalink.relative` `permalink.full` `image` (`image.url`, `image.alt`) `date` `modified` `status` `type` `thumbnail` `author` (`author.id`, `author.displayName`) `template` (`.slug` `.id` `.title`) `readingTime` (minutes, 200 wpm); raw: `post_author` `post_date` `post_date_gmt` `post_content` `post_title` `post_excerpt` `post_status` `comment_status` `ping_status` `post_password` `post_name` `to_ping` `pinged` `post_modified` `post_modified_gmt` `guid` `menu_order` `post_type` `post_mime_type` `post_parent` `comment_count`. Other docs examples also use `item.featuredImage.url`/`.alt`/`.id`, `this.featuredImage`, `item.image.id`, `this.categories` (objects with `name`,`slug`,`id`).
User: `user.id` `.login` `.email` `.displayName` `.firstName` `.lastName` `.nickname` `.fullName` `.description` `.userUrl` `.avatar` `.registered` `.userRoles` (array) `.userRole` (first) `.capabilities` `.loggedIn` (boolean).
Site: `site.name` `.description` `.home_url` `.url` `.admin_url` `.version` `.language` `.isMultisite` `.currentDate` (unix timestamp).
URL: `url.full` `url.relative` `url.parameter` (`{url.parameter.firstName}`; case sensitive; sanitized with `sanitize_text_field()`).
Environment: `environment.current` is `"etch"`, `"gutenberg"` or `"frontend"`; `environment.context` is `"componentEditor"` in component editor. `{#if environment.current === "etch" || environment.current === "gutenberg"}...{/if}`.
Custom fields: `item.etch.field_id` / `this.etch.field_id`; WP meta `item.meta.field_id` / `this.meta.field_id`; options `options.<namespace>` (namespaces `acf`, `metabox`, `jetengine`; Meta Box: `options.metabox.option_page_name.field_name`). Third-party: see Integrations.
Filters (must return array): `etch/dynamic_data/post` ($data, $post_id; `{this.custom_data.field_name_1}`), `etch/dynamic_data/term` ($data, $term_id, $taxonomy; `{term.term_custom_data.field_name_1}`), `etch/dynamic_data/user` ($data, $user_id; `{user.user_custom_data.field_name_1}`), `etch/dynamic_data/option` ($data; `{options.my_custom_data.field_name_1}`).
```
add_filter('etch/dynamic_data/post', function( $data, $post_id ) {
    $data['custom_data'] = array('field_name_1' => "Field 1 value");
    return $data;
});
```

## Modifiers (chainable: `{item.price.multiply(1.2).round(2).numberFormat(2, ".", ",")}`)
Basic: `.dateFormat("F j, Y")` (PHP format; `.format()` deprecated) `.numberFormat(decimals=0, decimalPoint=".", thousandsSeparator=",")` `.toUpperCase()` `.toLowerCase()` `.toString()` `.toInt()` `.toSlug()` `.toBool()` `.trim()` `.ltrim()` `.rtrim()` `.stripTags()` `.urlEncode()` `.urlDecode()` `.htmlEncode()` `.htmlDecode()` (Since 1.5.2) `.truncateChars(count, ellipsis="...")` `.truncateWords(count, ellipsis="...")` `.round(precision=0)` `.ceil()` `.floor()` `.concat()` `.length()` `.reverse()` `.at(index)` `.slice(start, end)` `.indexOf()` `.pluck("author.displayName")` `.keys()` `.values()` `.split(separator=",")` `.join(", ")` `.replace(search, replace)` `.replaceAll(search, replace)` (Since 1.4.9) `.applyData()` (`{this.etch.header.applyData()}`) `.unserializePhp()`.
Examples: `<article class="post-{post.title.toSlug()}">`; `{#loop this.title.split(" ") as word}<span>{word} </span>{/loop}`; `{item.meta.keys().includes("name", "name custom field is set", "name custom field is not set")}`.
Arithmetic (Since 1.4.20; non-numeric or missing arg returns original; divide/mod by 0 returns original): `.add()` `.subtract()` `.multiply()` `.divide()` `.mod()`.
Comparison (return boolean, or custom `trueValue`,`falseValue`; this is the inline if/else, since `{#if}` cannot be inline): `.startsWith(search,t,f)` `.endsWith` `.includes(search,t,f)` (string or array) `.intersects(array,t,f)` (Since 1.1.0) `.less(compareTo,t,f)` `.lessOrEqual` `.greater` `.greaterOrEqual` `.equal` `.isTruthy(t,f)` `.isFalsy(t,f)` (Since 1.6.8).
```
<div class="{product.price.greater(10, 'product--expensive', 'product--affordable')}">
{#loop items as item, index}
  <div class="{index.mod(2).equal(0, 'row--even', 'row--odd')}">
{featured.isTruthy("Featured", "")}   {gap.isFalsy("Not set", "Set")}
```

## Loops
- Sources: WP Query, JSON, WP Terms, WP Users. Create via Loop element/Loop Manager; UI: select element, Cmd/Ctrl + click Loop button (sibling, then drag item in). Loop the repeating item (`<li>`), not its child.
- Syntax `{#loop loopName as item}...{/loop}`; index `{#loop recentPosts as post, index}` (0-based; `data-post-idx={index}`); inline `{#loop [1,2,3,4,5] as item}`; JSON source e.g. `[{ "name": "Jane Austen" }, ...]` + `{item.name}`.
- No-results workaround (empty loops render nothing): `{#loop posts.length().equal(0, [1], []) as item}<p>No results</p>{/loop}`
- Query args (Loop Manager):
```
$query_args = [
  'post_type' => 'post',
  'posts_per_page' => $count ?? -1,
  'orderby' => 'date',
  'order' => 'DESC',
  'post_status' => 'publish',
  'ignore_sticky_posts' => 1
];
```
- Arguments: `$token` placeholders; defaults via `??` (first declared default wins if arg reused). `{#loop blogPosts($count: 3) as item}`; multiple `{#loop relatedPosts($count: 3, $post_id: this.id) as post}`; in component `{#loop recent_posts($count: props.numberOfPosts) as item}`; string values quoted `$taxonomy: "category"`, `$term_id: this.categories.at(0).id`. `'post__not_in' => [$post_id]` and tax_query `'terms' => [$term_id]` must be arrays (`'field' => 'term_id'` or `'slug'`).
- Main Query: preset name `Main Query`, key `mainQuery`, type `main-query`; defaults `posts_per_page` `$count ?? 10`, `orderby` `$orderby ?? 'date'`, `order` `$order ?? 'DESC'`, `offset` `$offset ?? 0`. For archives/taxonomy archives/search. `{#loop mainQuery($count: 3) as item}`, `{#loop mainQuery($orderby: "title", $order: "ASC") as item}`, `{#loop mainQuery($count: -1) as item}`. `{item.main.some_special_field_from_third_party_plugin}` = raw passthrough (advanced).
- Nested: `{#loop categories as category}` + `{#loop posts($cat: category.id) as post}` (arg `'cat' => $cat`); CPT: `{#loop projectStatus as status}` + `{#loop projects($status: status.id) as project}` (`'terms' => $status`). JSON nested: inner source `{item.books}`; use distinct names (`{#loop authors as author}` / `{#loop author.books as book}`): same name hides outer (before 1.6.8 it fell back).
- Attachments: `'post_type' => 'attachment'`, `'post_parent' => $id`, `'posts_per_page' => -1`, `'post_status' => 'inherit'`, `'orderby' => 'menu_order'`, optional `'post_mime_type' => 'image'`; taxonomized via `tax_query` (e.g. `happyfiles_category`).

## Conditional logic
- Condition element = `{#if}{/if}`; block-level (use comparison modifiers for inline/attributes).
- `{#if user.loggedIn}` ; `{#if !user.loggedIn}` ; `{#if this.categories.pluck("name").includes("ABCs")}` ; `{#if props.productCategory === "featured"}` ; `{#if props.rating >= 4}`.
- Quotes only around text, never numbers/booleans. Operators: `===` `!==` `==` `!=` `>` `<` `>=` `<=` `&&` `||` `!` and parentheses. Strict preferred (loose does type conversion).
- Examples: `props.isActive && props.rating >= 4.5` ; `user.userRoles.includes("administrator") || user.userRoles.includes("editor")` ; `(props.isActive || props.isHighlighted) && (props.rating >= 4.5)` ; `this.author.id === user.id` ; `this.meta.price <= url.parameter.budget`.

## Facets
- Native Etch facet pages (load, filter, apply, reset, sort, search, pagination, map): "Coming soon..." (only third-party documented).
- FacetWP: query arg `'facetwp' => 'true'`; class `facetwp-template` on direct parent of loop; facet shortcodes OUTSIDE that wrapper (else console error "Facets should not be inside the 'facetwp-template' container"); `[facetwp facet="pagination"]` (Pager facet); one FacetWP-enabled query per page; finite `posts_per_page` needed.
- WP Grid Builder: arg `'wp_grid_builder' => 'wpgb-content-1'`; same class on loop parent (`<div class="results wpgb-content-1">`); `[wpgb_facet id="your-facet-id" grid="wpgb-content-1"]`; selector must start `wpgb-content-` and match in query arg, class, shortcode `grid`. Pagination = Facet Action Load Content, Load Type Pagination. Multiple loops supported (unique selector each).
