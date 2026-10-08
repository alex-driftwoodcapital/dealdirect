# Design spec (the handoff contract)

The builder never guesses. `art-director` writes one design spec per page (YAML, or JSON) plus its reference images; `scripts/spec-check.py` must print 0 errors before any build step. Missing data means the builder stops and lists what it needs; it never fills a gap by taste.
Etch rules behind each check: `etch-expert/reference/guardrails.md`. Plan: `plugins/etch-builder/LAYOUT-PLAN.md` §4.

```
python3 -I scripts/spec-check.py page.yaml [--root DIR] [--site-styles etch_styles.json]
```
Exit 0 = build, 1 = do not build (each line names the field and the fix), 2 = unreadable. `--root`: folder the reference and shot paths are relative to (default: the spec's folder). `--site-styles`: an `etch_styles` export (fresh snapshot `option-etch_styles.json`, or `etch-expert/reference/fixtures/styles-used.json`) so existing site classes count as known. Tests: `python3 -I scripts/spec-check-tests/run.py`.

## Shape
Required unless marked optional. Full working example: `scripts/spec-check-tests/good/services.yaml`; real skeleton: `examples/home-v117/home.yaml`.

```yaml
spec_version: 1
page: {title: "Services", slug: services, status: draft, template: default}   # status is always draft
site_profile: dealdirect-staging         # host, IDs, brand rules
site_styles: path/to/etch_styles.json    # optional: existing site classes count as known
site_classes: [callout-band]             # optional: more known site classes
scope: [services-intro]                  # optional: edit flow, only these sections change
references:
  source: mockup-v117/services.html      # one source of truth (file, zip#member, or https URL)
  shots: {375: refs/services-375.png, 1440: refs/services-1440.png}   # full page, stored with the spec
tokens:                                  # brand name -> ACSS 4 variable or class; every value must exist in ACSS 4.0.1
  surfaces: {paper: bg--ultra-light, ink: bg--dark, butter: --secondary}   # "paper" is required
  type: {h1: --h1, body: --text-m}
notes: ["free text, ignored by the checker"]   # optional
sections:
  - id: services-intro                   # kebab-case, unique: becomes data-section and the heading id
    role: hero                           # hero intro features split proof quote faq list cta form nav footer logos story game dialog custom
    landmark: section                    # section header footer aside nav div figure dialog
    heading: {level: 1, text: "Websites that bring people in", highlight: "bring people in"}  # required for section/aside/dialog
    content:                             # verbatim copy, in order; the builder never edits words
      - {type: kicker, text: "Services"}
      - {type: p, text: "..."}
      - {type: h3, text: "..."}          # sub-headings in order
      - {type: list, items: ["...", "..."]}
      - {type: link, text: "Book a free review", href: /book/, style: btn--secondary}         # navigates
      - {type: button, text: "Watch", action: "open dialog tour-video", style: btn--secondary btn--outline}  # on-page action
      - {type: embed, source: "page 48 Home > Brief form"}   # keep an existing interactive block verbatim
    layout:
      pattern: split                     # library pattern name, or "new"
      wide: "2 cols, text 7 / media 5, media right"
      narrow: "stacked, media first"
    surface: paper                       # a key of tokens.surfaces
    media:                               # optional
      - {media_id: 812, alt: "...", ratio: "4/3", fit: cover, loading: eager}
      # alt: text | library (use the media library alt) | decorative: true with alt: ""
    component: {use: existing, ref: 143, props: {tone: butter}}   # optional; or {new: Card, props: [...], slots: [...]}
    data: {loop: {key: services, source: "WP Query post_type=service", item: service, inner: {...}}}   # optional
    responsive: ["cards switch to a row when the container is at least 40rem"]   # intent, not breakpoints
    states: ["dialog: centred, round icon close"]          # optional
    motion: {ref: art-director/reference/site-motion.md, reduced_motion: "final state"}   # optional
    shots: {1440: refs/services-intro-1440.png}           # optional per-section crops
    must_match: [order, copy, surface, columns, heading sizes, button roles]   # also: media spacing states motion
    may_differ: [exact line breaks]      # optional
```

`content` item types: `p kicker h2-h6 list link button quote cite label embed note`. A section built from an existing component may leave `content` out (copy lives in `component.props`), but keeps its `heading` so the page outline can be checked.

## What blocks a build (error codes)
| Code | Rule | Why (guardrails) |
|---|---|---|
| E_PLACEHOLDER | No TODO, TBD, FIXME, lorem ipsum, `[...]`, `{{` or a bare "..." anywhere | Never fill gaps by taste |
| E_MISSING, E_FORMAT, E_STATUS | page title/slug/status/template, site_profile, references.source, tokens.surfaces with `paper`, sections; status is draft | Process |
| E_SHOTS, E_FILE | Full-page shots at a phone width (320-430, 375 preferred) and a desktop width (1280-1920, 1440 preferred), stored as files that exist; source exists | Fidelity check needs them |
| E_TOKEN | Every token and every `--var` in layout/responsive/states exists in ACSS 4.0.1 (3.x names name their replacement) | §4 Styling |
| E_ID, E_SCOPE | Section ids unique kebab-case; `scope` names real ids | |
| E_ROLE, E_LANDMARK | Known role and landmark | §2 |
| E_HEADING | section/aside/dialog start with a heading (no heading: landmark `div` or `figure`); highlight is part of the heading | docs `/elements/section` |
| E_H1, E_HEADING_ORDER | Exactly one h1, in the first section with a heading; no skipped levels; dialog headings start at h2 | docs `/elements/section` |
| E_CONTENT | Each item has a known type and its verbatim text (list: items; embed: source) | |
| E_LINK, E_BUTTON | Links have href and no on-page action; buttons have an action and no href | docs `/elements/anchor` |
| E_STYLE | Links and buttons name their role: ACSS or known site classes, `text`, or `nested` | Parity audit: button roles |
| E_LAYOUT, E_RESPONSIVE | pattern, wide and narrow arrangement; responsive intent listed | docs `/responsive-development/philosophy` |
| E_SURFACE, E_SURFACE_NEIGHBOR | Surface is a token name; neighbours never share a non-paper surface (dialogs skipped) | art-director rule |
| E_MEDIA, E_ALT | Media by WordPress ID (no URLs), loading eager/lazy, ratio, fit; alt or decorative | docs `/elements/dynamic-image`, `/elements/image` |
| E_COMPONENT | Existing: integer `ref` + props mapping. New: props list + slots | docs `/components/*`, `/public-api/blocks` |
| E_LOOP | key, source, item; a nested loop never reuses an outer item name | docs `/loops/nested-loops` |
| E_DIALOG | A button somewhere opens each dialog by id; each dialog has a close button | Parity audit: dialogs |
| E_MOTION | Motion names its reference and the reduced-motion behaviour | §9 |
| E_MUST_MATCH | Fidelity checks named, from the known list | |

Warnings (do not block): more than one eager image, an eager image below the first section, responsive lines that talk about "breakpoints" without a width.

## Not checked here (checked later)
Whether media IDs and component refs exist on the site (builder lint and the write step), the CSS itself (`acss-expert verify.py`), the built page against the shots (fidelity check, plan §6).
