STYLE SPEC v1
site: index/site-profile.md (TwoEleven)  acss: 4.0.1  verified: 2026-10-07  verify: python3 -I scripts/verify.py /tmp/e2e/plan-grid.css -> 0 error(s)
items:
- role: Plan grid (pricing cards)
  target: new classes .plan-grid .plan-card .plan-card__name .plan-card__price .plan-card__desc
  apply_classes: [.bg--ultra-light on the section, .btn--secondary on the card links]
  css: see plan-grid.css (grid-auto-3, space/h/text tokens only)
  uses: [--grid-auto-3, --grid-gap, --space-s, --space-l, --border, --radius, --white, --box-shadow-1, --h3, --h4, --primary, --text-dark-muted, --text-m, .bg--ultra-light, .btn--secondary]
  notes: no media query; the grid stacks by itself. Button label is the single brand label.
