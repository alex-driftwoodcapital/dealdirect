# ACSS 4 fundamentals
Sources: https://docs.automaticcss.com/setup/whats-new-in-4 , /spacing/spacing-variables , /typography/fluid-text ; values and class list verified against the staging 4.0.1 build (reference/staging-4.0.1-facts.md). The old /3.0/fundamentals pages are 3.x and were removed from this file.

## What ACSS 4 is
- Variable-first and BEM-first (custom classes built on ACSS variables). Most utility-class modules were removed; recipes (`?name;`) replace the useful ones. Breakpoint-free: sizes are fluid, layout switches are your own `@media`/container query.
- Variables are CSS custom properties on `:root`, used as `var(--name)`: `background-color: var(--base);` `padding: var(--space-l);` `color: var(--white);`. Fallbacks are built in.
- Local override pattern (re-assign a token in a scope, by class, id or attribute): `.my-card--dark { --text-color: var(--white); }` (tokens verified: `--text-color`, `--bg-*`, `--btn-*` are locally scoped by design).
- The dashboard's cheat sheet (filter type "variable") lists everything; offline, use `index/acss-index.json` (`scripts/lookup.py`).

## T-shirt sizes
- `xs, s, m, l, xl, xxl` (What's New says 2XL, but the 4.0.1 build outputs `xxl`; icons use `2xl`). Base is M; below divides by the scale, above multiplies.
- Patterns the build outputs: `--space-{size}`, `--section-space-{size}`, `--text-{size}`, `.text--{size}`, `.section--{size}`, `.header--{size}`, `.btn--{size}`, bridges `--space-{big}-to-{small}`.
- Widths are NOT t-shirt sizes: `.width--10..90`, `--width-10..90`.
- Utility classes the build really outputs: facts file, "Utility classes the build outputs".
