# Etch Public API, Connector, Intelligence, Gutenberg authoring, Integrations
Sources: https://docs.etchwp.com/public-api (+ /blocks /components /loops /styles /stylesheets /navigation /fields /skills /ai /ui-and-history /types-reference), /etch-connector/*, /etch-intelligence/*, /gutenberg/{block-authoring,passthrough}, /integrations, /integrations/{controls,hooks,custom-fields,custom-fields/*}
Verified from docs 2026-10-02. (Condensed; see pages for omitted examples.)
Etch pinned: 1.6.8 (staging, 2026-10-07). Staging-tested facts: `confirmed-on-staging.md`. Block markup examples: `fixtures/`.

## Public API (`window.etch`; contract `0.x`, experimental, prefer feature detection)
`npm install @digital-gravy/etch-public-api` ; `import { getEtch, isEtchAvailable, isEtchApiError, EtchApiError, ETCH_API_VERSION } from "@digital-gravy/etch-public-api";` `getEtch(options?: ConnectOptions): Etch` throws `EtchApiError` `NOT_AVAILABLE` if builder not loaded; `isEtchAvailable(): boolean`. `ConnectOptions { apiVersion?: string; id?: string }`.
```
interface Etch { blocks; loops; styles; stylesheets; components; navigation; fields; ui; history; skills; ai;
  saveAsync(): Promise<void>; readonly apiVersion: string; readonly version: string; readonly environment?: EtchEnvironment; }
```
Persistence: `blocks`, `styles`, `loops` buffered -> `await etch.saveAsync()`; `stylesheets`, `components`, `fields` persist immediately (`*Async`).
Errors: `EtchApiError.code`: `BLOCK_NOT_FOUND` `WRONG_BLOCK_TYPE` `READONLY` `INVALID_ARGUMENT` `LOOP_NOT_FOUND` `STYLE_NOT_FOUND` `STYLESHEET_NOT_FOUND` `COMPONENT_NOT_FOUND` `POST_NOT_FOUND` `OPERATION_FAILED` `NOT_AVAILABLE`.
Feature detection (Since 1.6.7): `etch.environment?.capabilities.fields === true` (capabilities `loops` `fields` `templates` `wpMedia`); `etch.environment?.blockTypes.includes("etch/passthrough")`; missing `environment` = all available; branch on capability, not `product`.

### etch.blocks
```
select(blockId): void; deselect(): void; getSelectedId(): string | null;
getJson(blockId): PublicBlockJson; getTree(): PublicBlockJson[]; find(predicate: {type?,class?,attribute?}): string[];
create(json: EtchBlockJson, parentId?: string|null, index?: number): string; delete(id); duplicate(id): string;
move(id, newParentId: string|null, index?); replace(id, json): string; update(id, patch: {name?,hidden?,attributes?,text?});
copy(id): CopyObject; pasteAsync(payload, targetId?, index?): Promise<string>;
setText(id, text) /*text blocks only*/; rename(id, name);
getAttribute(id,key); setAttribute(id,key,value?) /*undefined clears*/; removeAttribute(id,key);
addClass(id, className) /*pass style id from styles.create*/; removeClass; hasClass;
enterComponentEditMode(id); exitComponentEditMode({revert?}); isInComponentEditMode(); saveComponentEditModeAsync();
```
`find`: `etch.blocks.find({ type: "etch/text" })`, `{ class: "btn" }`, `{ attribute: "href" }`. `styles` array on reads is read-only (rejected on authoring). Invalid parent throws `WRONG_BLOCK_TYPE`. Component instance props are block attributes; unknown key throws `INVALID_ARGUMENT`. `etch/dynamic-image` attrs: `mediaId`, `useSrcSet`, `maximumSize`; `etch/svg`: `src`, `stripColors`. Block `script: { code: string }` (deferred module in head; target by selector).
Block types: `etch/text {text}`, `etch/element {tag, attributes}`, `etch/dynamic-element`, `etch/dynamic-image`, `etch/svg`, `etch/loop {itemId, target?, indexId?, loopId?, loopParams?}`, `etch/condition {conditionString}`, `etch/component {componentId, attributes}`, `etch/slot-content {slotName}`, `etch/slot-placeholder {slotName}`, `etch/post-content`, `etch/raw-html`, `etch/passthrough {gutenbergBlock}`; all have `version`, `context`, `children`. `copy()` returns opaque `CopyObject`.

### etch.components (persist immediately)
```
list(): PublicComponentSummary[]; getJson(componentId: number): PublicComponentJson; createAsync(name): Promise<number>;
updateAsync(componentId, patch: {name?,key?,description?,properties?,blocks?}): Promise<void>; deleteAsync(componentId): Promise<void>;
```
Summary `{id:number,name,key (PascalCase),description?,properties}`. Property base `{name,key,description?}` + `type {primitive, specialized?}`: primitives `string` (specialized `color|url|image|select|array|wpMediaId`; `selectOptionsString` newline "Label : Value", first line default), `number` (reserved), `boolean`, `object`, `array`; specialized `array/class`, `object/group` and `array/repeater` (both with nested `properties`), `string/condition` (`properties`, `default` = expression).

### etch.loops (buffered)
```
getAll(): Record<string,EtchLoop>; add(loop): string; update(loopId, loop); delete(loopId); findLoop(query): (EtchLoop&{id})[];
setForBlock(blockId, { loopId?, target?, itemId?, indexId?, loopParams? })
EtchLoop { key, name, global: boolean, config }  config: {type:"wp-query"|"main-query", args: WpQueryArgs} | {type:"wp-terms", args} | {type:"wp-users", args} | {type:"json", data: unknown[]}
```
Args accept `"$count"` or `"$count ?? 10"` (NumericParam/BooleanParam). Example: `etch.loops.add({ key: "recent-posts", name: "Recent posts", global: true, config: { type: "wp-query", args: { post_type: "post", posts_per_page: 6, orderby: "date", order: "DESC" } } });` `setForBlock(blockId, { loopId, itemId: "post", indexId: "i", loopParams: { count: 3 } })`. Terms args: `taxonomy, orderby, order`; users args: `role, include, exclude, search, search_columns, orderby, order, number, offset, paged`.

### etch.styles (buffered) / etch.stylesheets (immediate)
```
styles: list(filter?: {type?}): StyleSummary[] /*{id,selector,type,collection,css}; type "class"|"id"|"tag"|"element"|"attribute"|"custom"*/;
  create(selector, css?): string; update(styleId, {selector?,css?}); delete(styleId);
  listVariables(collection?): Record<string,string>; getVariable(name, collection?); setVariable(name, value, collection?); removeVariable(name, collection?)
stylesheets: list(); get(id); createAsync({name, css, type?}): Promise<string>; updateAsync(id, patch); appendAsync(id, css); deleteAsync(id);
  listCustomMedia(): Record<string,string>; addCustomMediaAsync(name, query)   // type "default" | "@custom-media"
```


### etch.navigation, fields, ui, history, skills, ai
```
navigation: goTo(place) /*"builder"|"templates"|"content-hub"|"style-manager"|"loop-manager"|"asset-manager"*/; getCurrentPlace(); getPlaces();
  openPostAsync(postId); openTemplateAsync(templateId); getActivePostId(): number|null; isEditingTemplate(); listPostsAsync(postType?); listTemplatesAsync()
fields (all Async): listGroupsAsync(); getGroupAsync(id); createGroupAsync(def): Promise<string>; updateGroupAsync(id, def); deleteGroupAsync(id);
  addFieldAsync(groupId, field); updateFieldAsync(groupId, fieldKey, field); removeFieldAsync(groupId, fieldKey);
  getValuesAsync(postId); getValueAsync(postId, key); setValueAsync(postId, key, value); setValuesAsync(postId, values); deleteValueAsync(postId, key)
  group: { label, fields: [{label,key,type,required?}], assigned_to: {post_types|post_ids|taxonomies, op: "isIn"|"isNotIn"} }
ui: get/set/toggleColorScheme("light"|"dark"); isInterfaceHidden()/setInterfaceHidden(b)/toggleInterface(); exitToWordPress()
history: undo(); redo(); canUndo(); canRedo()
skills (sync, read-only): list(): SkillSummary[]; get(name): SkillDetail|undefined; getReference(name, file): string|undefined   // flow list() -> get() -> getReference()
ai: getState(); setState("idle"|"working"|"waiting"|"thinking"); hide()   // always clear in try/finally
```

## Etch Connector (npm `@digital-gravy/etch-connector`; free, open source)
- Lets an AI agent (Claude Code, Codex, Opencode) drive a live Etch builder tab via the Public API. Enable once: builder Settings -> AI -> "AI Connector" (experimental). Keep builder tab (editing a page/template) open. Click AI sparkles button ("Connect external AI agent"), then in agent chat run: `npx @digital-gravy/etch-connector serve`. One connected tab per site; connection ends if original chat or builder tab closes. No built-in guidance (put conventions in AGENTS.md/CLAUDE.md).
```
etch-connector serve [--ws-port 7331] [--control-port 7332] [--ws-host 127.0.0.1]
etch-connector tabs  [--json] [--control-port 7332] [--cdp]
etch-connector eval  [code] [-t|--tab name] [-f|--file path] [--timeout ms] [--cdp]
etch-connector shot      [-t name] [-s|--selector css] [--full] [--jpeg] [-o|--out file] [--freeze=false]   (CDP)
etch-connector html      <selector> [-t name]    (CDP)
etch-connector computed  <selector> [-t name] [--props a,b,c]   (CDP)
```
- `eval -t <tab> "<js>"`: body runs as async function (use `await`/`return`; result JSON on stdout). Safe mode: only `etch` global + standard JS (no `window`/`document`/network/storage). Exit codes: `0` success, `2` script error, `1` operational (tab not found, timeout, unreachable). CDP mode needs Chrome `--remote-debugging-port=9222` + `--cdp`. Listens on 127.0.0.1 only. `etch-connector --help` holds agent instructions.

## Etch Intelligence (experimental)
- Needs an OpenAI API key (only provider). Enable: builder Settings (gear) -> Experimental tab -> toggle AI Assistant -> paste OpenAI API Key -> Save. Panel appears automatically.
- Build Mode (default; wand icon, placeholder "Ask the AI to build something..."): generates insertable code (Etch HTML with `{this.title}`, `{#loop posts as post}`, `{#if ...}`; flat BEM CSS; minimal vanilla JS), creates loop definitions, CPTs, custom field groups/values, posts/pages, reads media library/current page. Code block actions: Insert, Replace, Copy. Context: attach files/images (10 MB each), "Add to AI context" (sparkles on element badge or right-click). Ask Mode (chat bubble icon): Q&A with copyable snippets.

## Gutenberg block authoring
- Etch authors to custom Gutenberg blocks (not core blocks), bi-directional sync on save; Etch = development environment, block editor = client content editing only (do not build in block editor). Patterns -> WP pattern library, components -> synced patterns, templates -> WP templates area.
- Passthrough blocks: non-core blocks detected are passed through to front end unparsed; shown as placeholder in Etch (`etch/passthrough`).

## Integrations
- Custom fields via `this.meta` (generic), `this.acf`, `this.metabox`, `this.jetengine`, `this.etch`; in loops `item.acf.field_id`. ACF return format: since alpha-3 full object; feature flag `RETURN_ACF_DYNAMIC_DATA` returns per ACF return setting.
- Text: `{this.acf.headline}`; WYSIWYG HTML renders. Docs tip: `{#if this.acf.headline}{this.acf.headline}{#else}Default Headline{/if}`.
- Image: `<img src="{this.acf.image_field.url}" alt="{this.acf.image_field.alt}" />` (also `.width` `.height` `.caption` `.id` `.sizes.<size>.url`).
- Gallery: `{#loop this.acf.gallery_field as image}<img src="{image.url}" alt="{image.alt}" />{/loop}`; `{this.acf.gallery_name.at(0).url}`.
- Repeater (also `metabox`, `jetengine`): `{#loop this.acf.faq as faq}<h3 class="faq__question">{faq.question}</h3>{/loop}`; nestable.
- Flexible content (ACF): `{#loop this.acf.page_sections as section}{#if section.acf_fc_layout == 'hero_banner'}...{/if}{/loop}`.
- Relationship: ACF `{#loop author.acf.author_books as book}...{/loop}`; Meta Box MB Relationships `{#loop mbFrom($related_cpt: 'my_cpt', $rel_field: 'relationship_field', $from_id: this.id) as related}` / `mbTo(... $to_id: this.id)`.
- Options pages: `{options.acf.field_name}`, `{options.metabox.option_page_slug.field_name}`, `{options.jetengine.option_page_slug.field_name}`; group `{options.provider.address.street}`; repeater `{#loop options.provider.hours as hour}`. If empty: field must be on an Options Page, name/key exact, value saved.
- Hooks: action `etch/canvas/enqueue_assets` (`add_action('etch/canvas/enqueue_assets', function() { wp_enqueue_style('custom-css', 'https://localhost/style.css'); wp_enqueue_script('custom-js', 'https://localhost/script.js'); });`); filters `etch/dynamic_data/post` (accepted args 2), `/user` (2), `/term` (3), `/option`.
- Controls: `window.etchControls.builder.settingsBar.{top|center|bottom}.{addBefore(control)|addAfter(control)|remove(id)}`; control `{ icon (Iconify e.g. 'ph:rocket-duotone'), tooltip, callback, id? }` (icon/tooltip/callback required); wrap in `window.addEventListener('load', () => { ... })`.
