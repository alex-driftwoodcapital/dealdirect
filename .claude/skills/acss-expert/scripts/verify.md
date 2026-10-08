# verify.py: blocking ACSS name check
Run before any CSS or Etch markup is saved. Exit 1 = BLOCKED (any ERROR). Stdlib only, reads `index/acss-index.json` (rebuild with `build-index.py`). Lookup rule: **present first, then absent**. Basis: official ACSS 4 docs (What's New; each page's "Changes From 3.x"), mapped in `reference/staging-4.0.1-facts.md`.

```
python3 -I scripts/verify.py FILE...                       # .css = CSS; anything else = Etch block markup / HTML / JSON (class lists + "css" strings)
python3 -I scripts/verify.py --site-styles etch_styles.json --site-css global.css FILE...
python3 -I scripts/verify.py --classes btn--primary grid--3 # quick class check
  --json  machine output   --strict-site  unknown non-ACSS classes become errors   --stylesheet automatic.css  other site's build
```
| Severity | Rule |
|---|---|
| ERROR | name in the absent list (3.x/removed) with its replacement; ACSS-shaped class (`prefix--x`) or `var(--x)` not in the build and not defined in the input/site CSS; unknown `?recipe`; 3.x `@btn;`/`@include`; `hsl(var(--x-h ...))`; `@import`, `@font-face`, `<style>`, `<link rel=stylesheet>` (no new stylesheets) |
| WARN | literal that equals a token for that property (palette hex, fixed spacing, radius, font size); 3.x `fluid()`/`ctr()`; site class not in `--site-styles` |
Never flagged: `--wp-*`, custom props the input or site styles define, site-local classes that are not ACSS-shaped.

## Reuse from the Etch lint (do not duplicate)
`etch-page-editor/scripts/lint.py --acss-css` currently takes class names from a regex over the stylesheet. Replace that with this module so removed/3.x names are caught too:
```python
import importlib.util
s = importlib.util.spec_from_file_location('acss_verify', '<repo>/skills/acss-expert/scripts/verify.py')
m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
v = m.Verifier.load(site_styles='etch_styles.json')
v.known_class('btn--secondary')            # bool: ACSS build or site styles
v.classify_class('grid--3')                # None | ('ERROR'|'WARN', message with replacement)
v.check_classes(['a', 'b'])                # list of {severity, where, message}
v.check_css(css_text); v.check_text(markup_or_json)
```
or shell out: `python3 -I verify.py --json --site-styles ... FILE` and read `errors`. Thread 6 wires it into the build step.

## Tests
`bash scripts/verify-tests/run.sh`: seeded-bad CSS/HTML must block with the expected findings; 6 real fixtures (pages, components) and 59 real `etch_styles` entries must pass; the 2 known live-site bugs below must be caught.
Known live-site bugs found (Etch styles, not fixed here): `.header-wrapper` uses `var(--text-color-dark)` and `.site-footer__newsletter` uses `var(--space-3xs)`; neither variable exists in ACSS 4.0.1, so those declarations are invalid.
