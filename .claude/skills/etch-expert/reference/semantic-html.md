# Semantic HTML in Etch (short rules)

Extends `guardrails.md` section 2 and 3 (one h1, no skipped levels, anchor vs button, landmarks, alt). Not repeated here. Checked by the audit recipe at the bottom.

## Page shape
- Template = `header` (component) + one `main` + `footer` (component). One `main`, one page-level `header`, one `footer`. Etch sections are `section`, not landmarks, until named.
- Every `section` has a heading and `aria-labelledby` pointing to it (Etch adds it; keep the heading id). No heading = `div`.
- `nav`: one per purpose (primary, footer, breadcrumb, pagination), each with a distinct `aria-label`. Social icons or a button row are not a nav; a list of links to sections of the site is.
- `article` only for self-contained, repeatable pieces (an Insight post, a project card on its own page). A card inside a loop is an `li`; add `article` inside it only if it could stand alone.
- `aside` only for tangential content (sidebar, pull note). `figure` + `figcaption` for an image that has a caption.

## Elements
- Lists: any group of like items (cards, links, steps, logos, FAQ) is `ul` (or `ol` for sequence), loop the `li`. Never a stack of divs with bullets drawn in CSS.
- Heading level follows outline, not size. A decorative big number or kicker is a `p`, not a heading. Footer column titles: `h2`/`h3` per outline, or a `p` if they add no outline; never an `h4` jump.
- Links need text that works alone ("Read the donation page fixes", not "Click here"). Icon-only link or button: `aria-label` or visually hidden text. External `target="_blank"` links get `rel="noopener"` and say so in the label.
- Button/anchor rule stays in guardrails; also: a `<button>` inside a form needs `type`; never nest a button in an anchor.
- Tables only for tabular data (pricing comparison with headers `th scope`); never for layout.
- FAQ: `details` / `summary` or button + `aria-expanded` + panel id; heading outside the toggle.

## Images (adds to guardrails section 3)
- Informative: alt says what it shows or its purpose. Linked image: alt describes the destination. Decorative (texture, divider, background): `alt=""`, no `title`.
- Logos: alt is the org name, no "logo of". Client logo wall: one `ul`, alt = client name.
- Text inside images is repeated in alt or, better, set as real text.

## Language and focus
- `lang` on the document; set `lang="es"` on Spanish blocks inside English pages.
- Visible focus never removed; skip-to-content link is the first focusable element and targets `main`.
- Dialogs: `<dialog>` with labelled heading and real close button (guardrails section 2).

## Audit recipe (read-only)
Run `scripts/audit-semantic.js <urls>` (needs network access to the site from where it runs). It lists: h1 count, heading sequence, landmarks (`header/nav/main/footer`, labels), `img` without alt, empty links/buttons, `div role=button`, duplicate ids, unlabelled sections (lists made of divs: check by eye). Mark unreadable pages `[VERIFY via Mac browser]`. Each finding gets an owner (builder / copy / Alex).
