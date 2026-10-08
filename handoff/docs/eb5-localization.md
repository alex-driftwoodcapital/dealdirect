# EB-5 pages — one template, three languages

All EB-5 landing pages share one Etch template (`eb5-landing`) and one section order. Only strings change.

| Permalink | Lang | Design file |
|---|---|---|
| /eb-5-investments/ | en | EB-5 Investments.dc.html |
| /new-eb-5-page/ | en | EB-5 Investments.dc.html (same content; live landing page, keep permalink) |
| /investimentos-eb-5/ | pt-BR | Investimentos EB-5.dc.html |
| /inversiones-eb-5/ | es | Inversiones EB-5.dc.html |

## Build rules
- Set `<html lang>` per page and add hreflang alternates (en / pt-BR / es + x-default → /eb-5-investments/).
- Store page strings as ACF fields per page (or a WPML/Polylang string set). Offering KPIs, prior-project data and platform stats stay single-source; only labels translate.
- Number format per locale: pt-BR uses 800.000 / 9.000.000; es keeps 800,000 (matches live ES pages). The platform stats (dwstats) render en-US today — format them with `Intl.NumberFormat(locale)` in Etch; translate the as-of date the same way.
- HubSpot: one form; pass `page_language` as a hidden field.
- PT and ES legal: Target-returns, TEA footnote and "all information subject to change" text are the live page's own wording. The general "Legal disclosure" paragraph is the live PT text on PT; on ES it is a new translation of the English text. Both pages end with the "English prevails" translation notice.

## Needs compliance / translator review
1. New translations (not on the live PT/ES pages): Benefits list, Investment & Job Creation requirements, developer benefits list, new timeline wording, 5 extra FAQs, ES legal disclosure, renderings note, CTA, form placeholders.
2. "Money back guarantee…" item translated literally (Garantia / Garantía) — same wording question as English.
3. Live PT/ES pages differ from the new EN page; the new pages follow EN: offering KPIs (live PT/ES: 2–6% interest, 33.2 jobs/investor, 5+ years vs EN 2% debt / 6% equity / 3–5 years), timeline (live 6 steps vs EN 5), Home2 Suites jobs (live PT/ES 12 vs EN 17), Element & Staybridge status (live PT "Em construção" vs EN Operating), live PT "25+ years" vs 30+.
4. Fixed on EN: the contact-method question and submit button were in Spanish.
