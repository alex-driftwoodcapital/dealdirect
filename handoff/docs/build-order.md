# Build order (staging only)

0. **Prep** — fill `CLAUDE.md` placeholders. Snapshot staging DB + files (Cloudways backup). Confirm Etch + ACSS 4 versions. Inventory plugins (forms, SEO, field plugin, GTM).
1. **Export** — offering CPT + field keys (`docs/cpt-schema.md`), page list with IDs, form definitions, media IDs for every image used in the design files.
2. **ACSS settings** — `docs/acss-mapping.md`. Self-host Plus Jakarta Sans. Read back the generated scales.
3. **Global components** — header, footer, legal-block, footnotes, cta-band, modal, section-head.
4. **Pilot** — EB-5 page (`/eb-5-investments/`): simplest, no loops. User review before continuing.
5. **Offering single template** — Riverside Wharf Preferred Equity; then check every other offering renders with the same template.
6. **Home** — CPT loops, video hero, deal cards, past tiles, registration + login modals (existing form plugin).
7. **ES / PT EB-5** — duplicate the EB-5 layout; replace copy with each live page's text verbatim; keep their own forms.
8. **/new-eb-5-page/** — keep its live section order; apply EB-5 components.
9. **Evidence register** — every `check` and `gap` in `design/evidence-register/claims.js` resolved or explicitly accepted by compliance.
10. **Go-live plan** — crawl diff (`docs/permalinks.md`), then migrate per the user's instruction.

# QA checklist (every page)
- [ ] Copy matches live verbatim (diff text content)
- [ ] All URLs + anchor IDs unchanged; status 200; canonical correct
- [ ] SEO title/description/OG carried over
- [ ] 375 / 768 / 1440: no horizontal overflow, no clipped text
- [ ] Tap targets ≥ 44px at 375
- [ ] Text contrast ≥ 4.5:1 (footnotes on dark included); footnotes ≥ 12px
- [ ] Heading order logical; one H1
- [ ] Images have alt (decorative = empty alt)
- [ ] Keyboard: header, modals (trap + Esc), tabs (arrow keys), accordion
- [ ] `prefers-reduced-motion`: no autoplay video, no transitions
- [ ] Forms submit to the same destinations as today; "None of the above" shows Our Apologies
- [ ] GTM fires; Juniper Square login link works; external-link interstitial still works
- [ ] No unresolved `var(--…)` in computed styles
- [ ] Lighthouse: LCP < 2.5s on hero (poster preloaded, video lazy)
