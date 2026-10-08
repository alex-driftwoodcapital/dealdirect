# Etch component inventory

Build these as Etch components (props in parentheses), BEM-named. Section shells use ACSS section padding + 1334px container.

## Global
| Component | Props | Notes |
|---|---|---|
| `site-header` | `theme` (over-media / solid) | Fixed. Scroll state via a small scoped script toggling `data-scrolled` on the header at 40px; CSS handles colours, blur, height. Logo, `site-header__links`, `site-header__actions` (Login ghost, Sign Up filled). Mobile: links hidden < 760px; actions stay. |
| `site-footer` | — | Logo, dashboard link, copyright, legal nav |
| `cta-band` | `heading`, `body`, `button_label`, `button_action` | `cover-bg.png` card, radius 24 |
| `legal-block` | slot | 12px / 1.7 two-column grid |
| `footnotes` | slot | `.footnotes` 12px, slate-600 (or white 72–78% on dark) |
| `modal` | `id`, slot | Overlay + panel; open via `data-modal-open="{id}"`; Esc/backdrop close; focus trap |
| `section-head` | `eyebrow`, `heading`, `intro`, `dark` | 48×2 rule, eyebrow, H2 |

## Home
| Component | Props |
|---|---|
| `hero-video` | `video_mp4`, `video_webm`, `poster`, `eyebrow`, `heading`, `lede`, slot: CTAs + rail. Reduced motion → no autoplay. |
| `hero-rail__item` | loop item: status, title, tag, href (`#{slug}`) |
| `deal-card` | loop item: `status`, `tag`, `title`, `summary`, `image`, `href`, `cta_label`. Children: `deal-card__photo`, `deal-card__veil`, `deal-card__chip`, `deal-card__body`, `deal-card__eyebrow`, `deal-card__title`, `deal-card__summary`, `deal-card__cta`, `deal-card__notify` |
| `past-tile` | loop item: `tag`, `title`, `image`. `past-tile__chip` reads "Closed" |

## Offering single
`offering-hero`, `stat-card` (value, qualifier, label, footnote_ref — DS `.dw-stat-card`), `offering-subnav` (sticky, anchors), `media-split` (image side, slot), `partner-card`, `cap-stack` (layers: amount, label, cumulative %, highlight), `highlights-list`, `metrics-band--dark`, `program-tabs` (tabs → gallery + spec panel; script scoped to component), `rationale-card` (index, title, body).

## EB-5
`process-timeline` (step label, body), `project-card` (image, chip, title, summary, 4 metrics, CTA), `faq-item` (native `<details>`), `track-card` (image, status, name, location, investors, capital, jobs), `lang-switch`.

## Scripts (keep tiny, scoped, no globals — see `etch-expert/reference/javascript.md`)
1. header scroll state, 2. modal open/close/focus trap, 3. program tabs + gallery, 4. coming-soon notify reveal (if the form plugin can't do it), 5. registration step logic — prefer the form plugin's native multi-step + conditional "Our Apologies" step.
