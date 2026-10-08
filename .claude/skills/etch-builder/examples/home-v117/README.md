# Homepage design spec skeleton (capstone L9)

`home.yaml` is the first real design spec: the current staging homepage (page 48) in the design-spec format, with the v117 mockup as the visual reference. Filled only from repo data on 2026-10-07.

Check it from the repo root:
```
python3 -I skills/etch-builder/scripts/spec-check.py skills/etch-builder/examples/home-v117/home.yaml --root .
```
Today it fails on purpose with 2 errors: the full-page reference shots at 375 and 1440 do not exist yet (the parity audit only kept per-section crops, at 1440 and 390). Capture them from `mockup-v117/index.html` in the Mac session with reduced motion on, save them next to the spec, and point `references.shots` at them; the spec then passes.

What the checker already caught while writing it, and how the spec fixes it:
- The trust bar and the client quote are `<section>`s with no heading on staging. Docs say a section starts with a heading (`/elements/section`), so the spec makes them a `div` and a `figure`.
- Parity-audit rows that are design facts (highlight as butter text, dialog title line and round close, blue "Send your brief", card preview graphic) are now `states` and `must_match` fields, not notes.

Interactive pieces (front-door demo, leaks game, brief form, solution dialogs' content) are `embed` items: kept verbatim from page 48, per the site rule to leave them alone beyond approved copy fixes.
