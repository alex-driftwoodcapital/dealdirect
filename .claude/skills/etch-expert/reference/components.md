# Etch components (custom + native)
Sources: https://docs.etchwp.com/components-native/overview (+ /components-native/{basic-nav,off-canvas,...}), https://docs.etchwp.com/components/{intro-components,creating-a-component,creating-component-props,mapping-component-props,using-a-component-static,using-a-component-dynamic,creating-component-variations,component-namespace,slots}, https://docs.etchwp.com/components/props/{prop-boolean,prop-class,prop-condition,prop-group,prop-loop,prop-media,prop-object,prop-select,prop-text}
Verified from docs 2026-10-02. (Condensed; code verbatim.)
Etch pinned: 1.6.8 (staging, 2026-10-07). Staging-tested facts: `confirmed-on-staging.md`. Block markup examples: `fixtures/`.

## Custom components: concepts
- Components != templates. Components = reusable pieces (header, footer, card, CTA, button). Props control data and behaviour; variations are done with props only, not snapshot copies.
- Create: build static version -> right-click parent in structure panel -> "Create Component" (editor is purple, has "Component Editor" panel) -> name (parent element's name is reused) -> add props -> purple "Save" (does not close editor) -> "Exit" (before saving = abandon).
- Insert instance: Cmd + I insert menu.
- Props: add with "+" in component editor. Types: Text, Boolean, Select, Media, Loop, Object, Class, Group (plus Condition, Repeater mode of Group). Every prop has Label + Key.
- Prop kinds: data props (content) and behavior props (booleans/options).

## Mapping props
- Visual: click target icon next to prop, then click canvas element (replaces text with `{props.serviceName}`).
- Copy icon copies key (e.g. `props.serviceName`) for href/src/alt/custom attributes (HTML editor or attribute inputs).
- Braces rule: outside braces wrap `{props.heading}`; inside an expression do not:
```
{props.heading}
{#loop props.items as item}
{#if props.isFeatured}
href="{props.linkUrl}"
```

## Scope (critical)
- Never use loop/template keys (`{post.title}`, `{item.name}`) inside a component; components only see global data (`this`, `site`, `url`) plus props. Pass data in via props.
- Static use: fill prop inputs manually. Dynamic use: put component in loop, enter keys as prop values: Post Title -> `{item.title}`, Post Image -> `{item.image.id}`, Post Link -> `{item.permalink.relative}`; in templates e.g. Heading -> `{this.title}`, Featured Image -> `{this.featuredImage}`.
- Instance panel inputs: Text, Boolean toggle, Select dropdown, Image media selector, Array, Slot.

## Slots
- Add in component editor: Slot icon in Elements Bar, or write `{@slot yourSlotName}` in HTML editor. Instance-side syntax: `{#slot yourSlotName}{/slot}`.
- `slots` object: `slots.yourSlotName.empty  // true if the slot has no content, false otherwise`
- Default content:
```
{#if slots.default.empty}
  <p>This is the default content — it will only show if the slot is empty.</p>
{/if}
{@slot default}
```
- Conditional wrapper:
```
{#if !slots.footer.empty}
  <div class="card-footer">
    {@slot footer}
  </div>
{/if}
```
- Unlimited slots; empty slots render nothing on frontend; content is per-instance; removing a slot definition removes empty instances (slots with content are kept). Slot content cannot see data from a loop running inside the component (authored once, in outer scope). Put the component (not a slot) inside the loop and pass item via Object Prop. Cannot restrict slot content types.

## Component namespace (Since 1.4.15; only inside the component's own HTML)
Keys: `component.id` (Number, may be empty if unsaved), `component.name` (e.g. "Blog Card"), `component.key` (e.g. "BlogCard"), `component.defaults.<propKey>` (resolved default; class props -> class names, group props nested via dot notation).
```
<div data-component-id="{component.id}" data-component-key="{component.key}">
{#if props.title !== component.defaults.title}
  <span class="custom-badge">Custom</span>
{/if}
<div style="max-width: {component.defaults.layout.width};">
```

## Prop types
- Text: string/textarea. Boolean: true/false toggle (conditions, on/off styling via attributes or container style queries).
- Media: modes ID-based (internal media ID; use for dynamic image elements) and URL-based (direct URL).
- Select: one `key : value` per line; single key = key and value. Space around ":" required (`key : value` correct, `key:value` incorrect). Referencing outputs the value (key output not possible yet).
- Class (Since 1.3.0): map via class attribute: `<div class="card {props.cardStyle}">`. Default classes set with "+" (e.g. `.rounded`); instance classes replace defaults entirely. Typing a class creates the style if missing.
- Condition (Since 1.4.8): no key; visibility wrapper for nested props, condition string like an if element (see Basic Conditions); also hides Gutenberg block attributes. Example conditions: showButton is true; current_user.role is administrator. Nested props sit at the same data level. Can nest in Group and vice versa.
- Group (Since 1.4.0): label + key; nested access `{props.hero.title}`; preview data built from nested defaults.
- Repeater mode (Since 1.4.6; toggle on Group; type becomes `repeater`, data = array):
```
{#loop props.features as item}
  <div>
    <h3>{item.title}</h3>
    <p>{item.description}</p>
  </div>
{/loop}
```
 Key must be camelCased or bracket notation: Correct `{#loop props.myFeatures as item}{/loop}`, `{#loop props['my-features'] as item}{/loop}`; Incorrect `{#loop {props.myFeatures} as item}{/loop}`. Instance panel: collapsible Item 1.., Add and Delete buttons. Nested group in repeater: `{member.social.twitter}`.
- Loop prop: `{#loop props.yourLoopProp as item}{/loop}` (typical: `{#loop someLoop as item}{/loop}`). Not dash-cased (use `props['your-loop-prop']`).
  - With args: `{#loop props.myLoop($count: props.myCount) as item}`; modifiers: `{#loop props.myLoop.slice(0, 3) as item}`, `{#loop props.myLoop($count: props.myCount.toInt()) as item}`, `{#loop props['my-loop'].slice(0, 5) as item}`; combined:
```
{#loop props['featured-loop'].slice(0, props.maxItems.toInt())($offset: props.startFrom.toInt()) as item}
  <article><h2>{item.title}</h2><p>{item.excerpt.truncateWords(20)}</p></article>
{/loop}
```
- Object prop: passes loop/object/array/json into component. Key is base: `{props.post.title}`, `{props.post.featuredImage}`, `{props.post.permalink.relative}`. Its code editor holds fallback/preview JSON only. Instance has an `object` combobox (auto-fills from ancestor loops; in nested loops pick the nearest loop; custom JSON can be typed). Use Object prop for standardized item cards; individual props for per-instance-configured UI.
```
<article class="post-card">
    <etch:img mediaId="{props.post.featuredImage.id}" alt="{props.post.title}" class="post-card__image" />
    <div class="post-card__content">
        <h3 class="post-card__title">{props.post.title}</h3>
        <a href="{props.post.permalink.relative}" class="post-card__link">Read more</a>
    </div>
</article>
```
Fallback JSON: `{ "title": "Title of the Post", "featuredImage": { "id": 0 }, "permalink": { "relative": "#" } }`
Instance usage: `{#loop posts as post}<PostCard post="{post}" />{/loop}` ; nested: `{#loop department.members as member}<TeamMemberCard member="{member}" />{/loop}` ; alt: `<ProductCard object="{item}" />`.
  - A loop and everything it renders must be on the same side of the component boundary; move nested loop inside and use `{#loop props.product.terms as term}`.
  - Tip in docs: output `{item}` in the loop to see real JSON for fallback data. Unsynced Pattern avoids scope limits but loses edit-once.

## Variations (props, not snapshots)
```
{#if props.showLede}
  <p>{props.lede}</p>
{/if}
{#if props.showCta}
  <a href="{props.ctaUrl}">{props.ctaText}</a>
{/if}
style="--card-bg: {props.cardBg}; --card-color: {props.cardColor};"
data-theme="{props.theme}"
```
Select options (one per line): `dark` `light` `primary`; CSS: `.card[data-theme="dark"] { background: var(--dark-bg); ... }`.

## Native components (/components-native/*)
- Overview list: Accordion, Advanced Nav, Alert, Banner, Basic Nav, Before After, Carousel, Copy To Clipboard, Countdown, Dev Note, Dialog, Drawer, Gallery, Greeter, Hotspot, Icon Menu Bar, Lightbox, Logo Carousel, Map, Off Canvas, Read More, Reading Progress, Scroll Snap, Search, Skip Link, Slide Menu, Star Rating, Switch, Table Of Contents, Table, Tabs, Tooltip.
- "Not currently available, but planned": Alert, Before/After, Copy to Clipboard, Countdown, Hotspot, Lightbox, Map, Slide Menu, Switch, Table of Contents, Table, Tabs, Tooltip.
- "Waiting on our Components API" -> paste-in versions at https://patterns.etchwp.com/layouts/<name>/ : accordion, navigation (Advanced Nav, JSON loop driven), banner-alpha, carousel-alpha, dev-note, dialog, drawer, gallery-alpha, greeter-alpha, menu-bar-alpha, logo-carousel-alpha, revealer-alpha (Read More), reading-progress-alpha, scroll-snap-alpha, search-alpha, skip-link-alpha, star-rating-alpha.
- Only Basic Nav and Off Canvas have full pages (below). Paste prebuilt JSON with cmd+v / ctrl+v anywhere in builder.

### Basic Nav
Setup: Header component with `{#slot right}` for Navigation + Burger components. Loop `basicNav` is preinstalled (edit JSON in Loop Manager). Style CSS vars on `.etch-nav`, `.etch-burger`; breakpoint 768px (search `/* Set the desired breakpoint */`).
JSON shape: `[{"label":"Home","url":"/"},{"label":"Item 2","children":[{"label":"Item 2.1","url":"/dropdown1"}, ...]}]` — `children` become dropdown, grandchildren become flyout. Use relative URLs.
Nav JS option `ariaCurrentPage` boolean|object default false (`homePage` boolean default true). Example: `instantiateNavClass({ ariaCurrentPage: { homePage: false, }, });`
Nav props: `jsonNav` (loop, preset), `navAriaLabel` string "Menu", `mouseSubmenu` select "hover" (`hover`,`click`,`click-sub-hover`).
Burger JS options: `button` (required HTMLElement), `target`, `selfAriaExpanded` false, `targetOptions` {`class`,`ariaExpanded`}, `onToggle(isOpen)`, `onClose()`. Burger prop `ariaLabel` "Menu". Example: `new EtchBurgerScript({ button: burgerBtn, target: etchNav, selfAriaExpanded: true, targetOptions: { ariaExpanded: true, }, onClose, });` and `instantiateBurgerClass(etchNav, closeEtchNav);` with `window.etchElements?.etchNav?.closeAllNavs()`.

### Off Canvas (Drawer)
CSS vars on `.etch-drawer`. Slot: `drawerContent` (add via slot icon in bottom bar if missing). Trigger: set prop `triggerSelector` to a .class or #id.
Props (default): `showEditor` boolean false (internal editor show/hide); `triggerSelector` string `.open-drawer`; `drawerPlacement` select `left` (`left`,`right`,`top`,`bottom`); `drawerDisplayMethod` select `overlap` (`overlap`,`pushBody`); `closeButtonVariant` select `icon` (Icon, Label, Label and Icon); `closeButtonLabel` `Close`; `drawerId` `etch-drawer` (unique alphanumeric, needed for multiple drawers); `maxWidth` `400px`; `maxHeight` `100px`; `drawerBackgroundColor` `white`; `drawerBackdropColor` `rgba(0, 0, 0, 0.5)`; `drawerPadding` `1em`; `cloneSelector` string optional (element cloned into drawer, restored on close); `isInLoop` boolean false.
