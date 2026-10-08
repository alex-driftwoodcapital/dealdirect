# JavaScript in Etch

Sources: https://docs.etchwp.com/interface/js-panel, /interface/modular-interface, /elements/html, /public-api/blocks (section "Block scripts"), /integrations/hooks, /etch-intelligence/build-mode
Verified from docs 2026-10-02.
Etch pinned: 1.6.8 (staging, 2026-10-07). Staging-tested facts: `confirmed-on-staging.md`. Block markup examples: `fixtures/`.

NOTE: the dedicated page https://docs.etchwp.com/interface/js-panel is an empty stub (title "Javascript Panel" only). No how-to page for JavaScript exists in the sitemap. The facts below are everything the docs state; nothing else is documented there.

## What the docs state
- A "Javascript Panel" exists: "Write and edit JavaScript code directly in the interface" (modular-interface). Panels can be shown/hidden/moved to sidebars or bottom drawer. Code-First approach: maximize the code panel.
- Script delivery (public-api/blocks, "Block scripts"): any block can carry an optional `script` field. The code is enqueued in the document `<head>` as a deferred `type="module"` -- "the same way all JavaScript works in Etch". The script has NO runtime link to the block's element, so you must always target it by selector.
```
interface EtchBlockScript {
  code: string;
}
```
```
const id = etch.blocks.create({
  type: "etch/element",
  version: 1,
  context: { name: "My Block" },
  options: {},
  children: [...],
  tag: "div",
  attributes: { class: "my-block" },
  script: {
    code: `document.querySelectorAll(".my-block").forEach(function (el) {
  // initialise each instance
});`,
  },
});
```
- Rendering raw script via the HTML element requires `unsafe="true"` (`<etch:html content={...} unsafe="true" />`): with `unsafe="false"` (default) HTML is sanitized (`wp_kses_allowed_html('post')`); `unsafe="true"` lets `<script>` and `<iframe>` through, with XSS risk -- only for trusted sources.
- Canvas-only assets via PHP hook (integrations/hooks): action `etch/canvas/enqueue_assets` -- "enqueue additional styles and scripts" loaded inside the canvas:
```
add_action('etch/canvas/enqueue_assets', function() {
    wp_enqueue_style('custom-css', 'https://localhost/style.css');
    wp_enqueue_script('custom-js', 'https://localhost/script.js');
});
```
- Etch Build Mode (AI) writes "JavaScript when it's genuinely needed -- vanilla and minimal."
- Builder-only note: Quick Notes attribute `data-etch-note` is stripped on frontend.

## Not documented (do not assume)
- How the Javascript Panel scopes/attaches code to an element or page, any per-element `this`/root reference, where panel scripts load, or any JS API beyond the above. Verify in the builder or ask before relying on it.
