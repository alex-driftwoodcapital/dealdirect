# lint.py
`python3 scripts/lint.py [--styles <etch_styles.json>] [--loops <etch_loops.json>] [--acss-css automatic.css] [--component] FILE...`
Run it on any block markup before writing it to a site. Use a fresh `scripts/snapshot.sh` for the live `etch_styles`/`etch_loops` (`option-*.json` in the snapshot dir); without them it falls back to the fixtures' subset.

Errors (exit 1): invalid JSON, unknown block type (only the 9 catalogued Etch blocks plus `post-content`), mismatched/unclosed blocks, element without tag/attributes, plain `img` element, inline event handlers, `style` ids not in `etch_styles`, unsafe raw HTML (disabled in settings), dynamic-image without `mediaId`, condition missing `condition`/`conditionString`, loop with unknown `loopId`, component without numeric `ref`, slot without name, script without code/id.
Warnings: class with no style record (pass `--acss-css` to accept ACSS classes), class whose style id is missing from `styles` (builder adds it on save, see fixtures/PILOT.md), section child that is not the container div, inline `style`, raw-html, missing `metadata.name`, `{props.*}` outside a component, more than one h1.
Tests: `lint-tests/run.sh <etch_styles.json> <etch_loops.json>` (fixtures must be clean; `lint-tests/bad.html` must trip every rule).
Not checked: ACSS variable/recipe names (use `acss-expert`), whether a component `ref` post exists, media IDs.
