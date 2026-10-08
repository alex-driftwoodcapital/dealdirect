# Etch principles, setup, interface

Sources: https://docs.etchwp.com/getting-started/{installation,requirements,etch-theme,things-to-know,core-principles,development-strategy}, /interface/{modular-interface,responsive-controls,style-manager}
Verified from docs 2026-10-02 (docs pages "Last updated Sep 29, 2026").
Etch pinned: 1.6.8 (staging, 2026-10-07). Staging-tested facts: `confirmed-on-staging.md`. Block markup examples: `fixtures/`.

## Core principles (core-principles)
1. Honor web dev fundamentals: HTML, CSS, PHP, JS as designed; no proprietary "magic".
2. Never generate an element the user can't access: no hidden wrappers/black-box elements.
3. Don't rescue users from themselves: no bogus code to prevent mistakes; tools/validation instead.
4. Do what's right, not what's easy.
5. Do what's effective, not what's popular.
6. Default styles must have 0,0,0 specificity (all Etch defaults; easy to override).
7. Make things easier, but don't compromise (no poor code / limitations / scalability tradeoffs).

## Things to know (things-to-know)
- Etch = "Unified Visual Development Environment (UVDE)": visual interface + direct access to real code; speaks real HTML/CSS (not a proprietary language). Built for people who know web dev or want to learn. Founder: Kevin Geary.

## Installation / Quick Start (installation)
1. Install the Etch plugin (upload + activate).
2. Install the Etch theme (upload + activate).
3. Claim license (free Etch Theme license; etchwp.com/account/customer-dashboard/ -> "Reclaim Etch Theme Now"; key in SureCart dashboard; download theme from dashboard). License needed for auto-updates.
4. Navigate to any page/post, click "Edit with Etch".
5. Build; publish.

## Etch theme (etch-theme)
- Etch requires a companion minimal blank WordPress block theme; provides hooks/structure for Auto Block Authoring and Gutenberg compatibility.
- Do NOT switch themes during development or after going live (risks: loss of page layouts/content, broken functionality, incompatibility, data corruption). Docs advise: install Etch Theme, don't use other block themes.

## Requirements (requirements)
- WordPress 5.9; PHP 8.1; WP memory limit 64MB (128MB recommended).
- Builder UI uses color-mix, relative color syntax, OKLCH; use latest browser. Chromium/WebKit best; Firefox may have bugs; Safari has known OKLCH/relative-color rendering bugs (interface colors only, not built sites).

## Development strategy (development-strategy)
- Weekly releases (sometimes more); bug fixes released as soon as available; partial feature releases are common; functionality first, UI second.

## Modular interface (modular-interface)
- Panels (show/hide/resize/rearrange): Canvas, Structure Panel, Properties Panel, HTML Panel, CSS Panel, Javascript Panel, Styling Panel.
- Drop zones: left/right sidebars, bottom drawer (accept multiple panels; sidebars stack, drawer lines up in a row). Drag via panel header drag area.
- Resize: panel resize handles; sidebar edge; bottom drawer top edge; double-click handle resets size.
- Panel visibility via Panel Manager; eye icon in Settings Bar toggles whole interface.
- Skill levels: Beginner = code editors off, styling panel only; Intermediate = CSS editor on; Advanced = all panels.

## Responsive controls (responsive-controls)
- No device breakpoints; canvas is fluid (drag handles each side), no preset sizes.
- CSS editor persistent across preview sizes; add styles for any "breakpoint" from any preview state.
- Canvas measurement shown at top while dragging; selected element measurements shown.
- Auto query insertion: media queries use exact canvas measurement; container queries use exact element measurement. After insertion the CSS Mini GUI (CSS Quick Actions Bar) resets.
- "Has Me" selector auto-insert icon; add it before using a container query.

## Style Manager (style-manager)
- Opened by the Style Manager icon in the left Etch bar (paint brush icon in sidebar per how-to).
- Tabs: Selector Manager (view/edit CSS, rename, delete selectors; sort/search; "Tag" category filter per how-to), Variable Manager (global CSS custom properties; collections), Stylesheets Manager (global CSS; collections).
