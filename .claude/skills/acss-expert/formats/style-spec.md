# Style spec: handoff from acss-expert to the Etch skills
acss-expert returns a style spec; it writes nothing to the site. etch-builder / etch-page-editor own structure, where the CSS is stored (`etch_styles`, element style) and writing it. The spec never introduces a stylesheet, global CSS or SCSS file: every `css` block belongs to one class or element.

```
STYLE SPEC v1
site: <profile file>  acss: 4.0.1  verified: <date>  verify: 0 errors (command + result)
items:
- role: <what it is: "Hero section", "Pricing card">
  target: <existing class (preferred) | new class name | element role | #id>
  apply_classes: [<ACSS/site classes to put on the element, each verified>]
  css: |
    <nested CSS for that one target; ACSS variables and ?recipes only where ACSS has one>
  uses: [<every ACSS name in css/apply_classes, with its docs page>]
  notes: <brand rule, ordering, anything Etch must do (e.g. recipe expands in builder)>
```
Rules
1. Preference order: ACSS variable, then utility class in the build, then existing site class, then a new class (see `reference/best-practices.md`).
2. Names come only from `index/acss-index.json`; `python3 -I scripts/verify.py <css or markup>` must print `0 error(s)` and the result goes in the header. Unknown names block the Etch save.
3. Brand values come from the site profile (`index/site-profile.md`), expressed as tokens.
4. `?recipe;` lines are listed under `notes` ("expands in the builder; not checkable offline").
5. One `@media`/container query at most per item, only for a layout switch; ACSS 4 has no breakpoint presets.
6. Etch specifics (nesting `&`, `etch_styles` keys, loops, components) are not defined here; see `etch-expert`.

Example
```
STYLE SPEC v1
site: index/site-profile.md (example from TwoEleven)  acss: 4.0.1  verified: 2026-10-07  verify: python3 -I scripts/verify.py spec.css -> 0 error(s)
items:
- role: Primary CTA button
  target: existing class .btn--secondary (no new class)
  apply_classes: [.btn--secondary]
  css: ""
  uses: [.btn--secondary (docs /buttons/button-classes)]
  notes: ACSS secondary = Butter fill, Ink text = brand primary CTA. No size class: default button is 16px, 52px tall.
- role: Card grid
  target: new class .card-grid
  apply_classes: []
  css: |
    display: grid;
    grid-template-columns: var(--grid-auto-3);
    gap: var(--grid-gap);
  uses: [--grid-auto-3 (/grids/auto-grids), --grid-gap (/grids/grid-variables)]
  notes: stacks by itself, no breakpoint
```
