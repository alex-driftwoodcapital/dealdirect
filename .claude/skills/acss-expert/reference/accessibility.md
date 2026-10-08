# ACSS 4.x Accessibility

> **4.0.1 check (2026-10-07, see staging-4.0.1-facts.md):** confirmed in the build: `.hidden-accessible`, `.skip-link`, `--focus-color`, `--focus-width`, `--focus-offset`, `:focus-visible` styling. `.clickable-parent`, `.focus-parent*` and `.focus--*` are absent (removed in 4.0, docs "Changes From 3.x"): use the `?` recipes. The two docs pages disagree on where `?clickable-parent` goes (heading with the link vs the parent); recipes cannot be checked in a compiled stylesheet, so verify in a staging render.
Sources: https://docs.automaticcss.com/accessibility/{clickable-parent,focus-parent,focus-styling,hidden-accessible-class,reduce-motion} , /recipes/accessibility-recipes , /mixins/{clickable-parent,focus-parent}
verified from docs 2026-10-02

## Clickable parent (make whole card clickable via heading link + absolutely positioned pseudo-element)
- Recipe (recommended): `?clickable-parent`. accessibility-recipes page: apply to the heading element containing the link; parent container must be `position: relative`; heading must contain an `<a>`. clickable-parent page: "apply the recipe to the parent element that contains your link". (Pages differ on target element; follow the recipes page and verify.)
- Mixin (Custom SCSS only, use on the actual `a` or `button`):
```
.clickable-card { position: relative; }
.clickable-card__heading a { @include clickable-parent; }
```
- Removed in 4.0: `.clickable-parent` utility class. Avoid with multiple child links.

## Focus parent (move focus indication from child link to parent)
- Recipe: `?focus-parent` (apply to the parent set to `position: relative`).
- Mixin: `@include focus-parent(shadow);` or `@include focus-parent(outline);` (`shadow` = box-shadow; `outline` = offset outline). Custom SCSS only.
```
.clickable-card { position: relative; @include focus-parent(shadow); }
.clickable-card__heading a { @include clickable-parent; }
```
- Removed in 4.0: `.focus-parent`, `.focus-parent--shadow`, `.focus-parent--outline`.

## Global focus styling
- Dashboard: Additional Styling > Focus (renamed from "Accessibility"). Options: Focus Style (Outline | Shadow), Focus Color (default primary), Focus Width (rem suggested), Focus Offset (outline only).
- Local color: `--focus-color`, e.g. `.dark-section { --focus-color: var(--white); }`
- Removed in 4.0: `.focus--{color}` classes (`.focus--primary`, etc.).

## Hidden accessible text
- Class `.hidden-accessible` hides text visually but keeps it for assistive tech/search engines:
```
<a href="#"><i class="fb-icon"></i><span class="hidden-accessible">Follow us on Facebook</span></a>
```
- In the builder, ACSS shows an accessibility icon next to hidden text.

## Reduce motion
- Options > Defaults & Misc > Reduce Motion (on by default; moved from Options > Accessibility in 4.0). Do not turn off.
- When `prefers-reduced-motion: reduce`: scroll animations (On Enter/On Exit) `animation: none`; On Visible `transition: none`; hover effects `transition: none` with `translate`/`scale` reset to `none`. It is an OS setting, so it hides your own animations if your OS has it on.

## Related (documented elsewhere in this set)
- External link indication: visual cue + screen reader text default "Link to external site." (see components.md).
- `.unrelate`, color relationships, effects respecting `prefers-reduced-motion` (see components.md, surfaces.md).
- Recipes `?clickable-parent`, `?focus-parent` replace the removed classes.
