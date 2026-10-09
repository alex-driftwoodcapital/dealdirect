# Handoff: Driftwood Hotel Income I, DST — Offering Landing Page

## Overview
A single-page offering website for **Driftwood Hotel Income I, DST**, the Delaware Statutory Trust that owns the 176-key Courtyard by Marriott Fort Lauderdale Weston. Source of truth is the 11-page **institutional investor brochure** (`reference/Weston DST Brochure.dc.html`). The landing page re-flows that brochure into a responsive, scrolling web page for accredited investors and advisors, ending in a contact CTA.

The audience is accredited investors under a **Rule 506(c)** offering. Compliance copy (disclaimers, footnotes, risk factors) is part of the design and must ship verbatim.

## About the design files
The files in `reference/` are **design references built in HTML** — a fixed-size, US Letter print brochure, not production code. Do not ship the HTML or copy its absolute-positioned layout. Recreate the content and visual language as a responsive landing page in the target codebase's existing stack (React/Next, Vue, etc.) using its established patterns. If no stack exists, Next.js + CSS modules or Tailwind is a reasonable choice.

To view the reference: open `reference/Weston DST Brochure.dc.html` in a browser (it needs `support.js` and `doc-page.js` beside it; image paths point to `assets/opt/…` — repoint to `../assets/photos/` or serve from a folder where that path resolves). Each brochure page is a `<section id="p1">`…`<section id="p11">`; this README refers to them that way.

## Fidelity
**High-fidelity for visual language and content; layout to be adapted.** Colors, type, weights, tracking, card treatments, and all copy are final. Page geometry is print-specific (816px-wide Letter pages) — translate to a web grid per the section specs below.

## Copy rules (compliance — read first)
- **All copy is verbatim** from the brochure. Lift strings directly from the reference HTML. Do not rewrite, shorten, or "improve" any sentence, figure, or footnote.
- Every superscript footnote marker in body copy must keep its matching footnote text **in the same section**, directly below that section's content. Footnote numbers are **bold** (`font-weight:700`), formatted `1.`, `2.`.
- Numbering restarts per section exactly as in the brochure (each page has its own 1…n).
- The persistent line `For institutional due diligence use only. Not for review by, or distribution to, retail investors.` appears on every brochure page. On the web, show it in the sticky header bar (or a fixed top strip) and again in the footer.
- Required on page: `Securities offered through Metric Financial LLC. Member FINRA/SIPC.` (appears in hero disclaimer, disclosures, and footer).
- "As of" date: `All figures herein are as of May 21, 2026.` — keep in hero disclaimer.
- Confirm with Driftwood compliance whether a 506(c) accredited-investor acknowledgement gate is required before content is shown (see Interactions).

## Page structure
Max content width **1200px**, side padding 64px desktop / 24px mobile. Section vertical padding 96–128px desktop, 64px mobile. Alternate backgrounds `#F8FAFC` and `#EEF2F6`; dark sections use the navy field image.

### 0. Header (sticky)
- Height 72px. Transparent over hero with `logo-white.svg` (width 132px); after scrolling past the hero, background `rgba(248,250,252,0.85)` + `backdrop-filter: blur(12px)`, 1px bottom border `#D3D8E0`, swap to `logo-color.svg`.
- Right side: anchor links (Offering · Property · Location · Market · Sponsor · Disclosures) 13px/500, color `#0B2B48` (white over hero); primary button "Contact" scrolling to Contact.
- Above or inside the header: compliance strip, 8–10px, weight 700, `letter-spacing:0.07em`, uppercase, text = institutional line above.

### 1. Hero — source `#p1`
- Full-viewport (min 640px, max 900px) dark field: `background:#061A2E url(assets/photos/cover-bg.jpg) center/cover`, `background-position:34% center`.
- Content bottom-left aligned:
  - Rule: 72×1px, `#6FB0E0`.
  - Eyebrow: "Courtyard by Marriott Fort Lauderdale Weston" — 11px, 600, `letter-spacing:0.24em`, uppercase, `#6FB0E0`.
  - H1: "Driftwood Hotel Income I, DST" — 40px print → **56–72px web**, weight 300, `letter-spacing:-0.02em`, line-height 1.06, white.
  - Lede (verbatim from `#p1`): "A 176-key select-service hotel in Weston, Florida — offered as beneficial interests in a Delaware Statutory Trust for qualified 1031 exchange and direct equity investors." — 18px web, 400, line-height 1.42, `#E4EAF0`, max-width 640px.
  - CTAs: primary "Contact the offering team" (→ Contact), ghost "View offering summary" (→ section 2).
- Hero disclaimer paragraph (verbatim, starts "DST Interests are speculative…") pinned at the bottom of the hero: 11px, line-height 1.28, `rgba(228,234,240,0.66)`, max-width 960px.

### 2. Offering Summary — source `#p2`
- Full-width photo band `Courtyard-Weston-1.jpg`, height ~480px desktop / 280px mobile, `object-position:center 60%`, with bottom fade to `#F8FAFC` (`linear-gradient(to bottom, rgba(248,250,252,0) 0%, rgba(248,250,252,.72) 58%, #F8FAFC 100%)` over the lower 52%) and top tone `rgba(6,26,46,0.34)→0` over top 34%.
- H2 "Driftwood Hotel Income I, DST" (27px print → 36px web, 300, `#0B2B48`), sub "Courtyard by Marriott Fort Lauderdale Weston" (18→22px, 400, `#4A5564`).
- **KPI cards** — 4 across desktop, 2×2 mobile:
  - `~$23.98M` Max Offering · `~42.54%` Leverage ¹ · `6.8%` Year-1 Target Distribution ² · `7.0%` 5-Yr Avg. Target Distribution ²
  - Card: radius 6px (web: 12px OK), border `1px solid rgba(36,104,168,0.09)`, background `linear-gradient(135deg,#FEFEFF 0%,#F1F5FA 100%)`, padding 24px.
  - Value: 32px web, 300, `-0.02em`, `#0B2B48`, `font-feature-settings:'tnum' 1`. Label: 10–11px, 600, `0.1em`, uppercase, `#2468A8`.
- **Terms table** (two columns: label 160px / value 1fr; stack on mobile). Rows: Property · Market · Submarket · Vehicle ³ · Strategic Exit · Sponsor Equity · Cap Rate (2025 NOI) ⁴ · Year Built · Last Renovated. Label 10px, 600, `0.09em`, uppercase, `#2468A8`. Value 15px, `#2E3744`, line-height 1.4. Row padding 12px 0, divider `1px solid #D3D8E0`.
- Footnotes 1–4 verbatim from `#p2`.

### 3. Acquisition Criteria & Investment Opportunity — source `#p3`
- Photo band `Courtyard-Weston-2.jpg` (same fade treatment, ~340px).
- H2 "Driftwood Capital Acquisition Criteria for DSTs" (21→30px, 400). Five bullets in a 2-col grid (1 col mobile), 28px column gap; bullet = 6px circle `#2468A8`; text 15px, line-height 1.5, `#2E3744`.
- **Investment Opportunity panel**: radius 12px, border `1px solid rgba(36,104,168,0.08)`, background `linear-gradient(135deg,#FDFEFF 0%,#EDF3FA 100%)`, padding 32px. H3 "Investment Opportunity" (20→26px, 400). 6 items, 3×2 grid desktop / 1 col mobile: Sponsor Alignment · Diversified Demand Base · $6M Renovation · Affluent Master-Planned Community · Proximate to Cleveland Clinic · #1 RevPAR in Comp Set. Item title 16px, 700, `#0B2B48`; body 15px, `#2E3744`.
- Footnotes 1–4 + trademark line verbatim from `#p3`.

### 4. Brand & Property — source `#p4`
- Photo band `Courtyard-Weston-4.jpg` (~400px). Brand logo row: `brand-marriott.svg` (48px h), `brand-courtyard.svg` (19px h), `brand-bonvoy.svg` (24px h), gap 21px, scale ~1.25× on web.
- Two columns (5/12 + 7/12; stack on mobile):
  - Left: H3 "Brand Overview ¹", four paragraphs verbatim; stat pair `~271M` Marriott Bonvoy Members³, `~43M` New Members in 2025³ (value 32px, 300, `#2468A8`; label 13px, `#2E3744`).
  - Right: H3 "Courtyard by Marriott Fort Lauderdale Weston", description paragraph; "Food & Beverage" list (3); "Recreation & Services" list (9); stat row `176` Rooms · `2002` Year Built · `2024` Last Renovation.
  - Right column sits on a soft wash `linear-gradient(to right, rgba(207,225,242,0.28), rgba(207,225,242,0))`.
- Footnotes 1–5 + trademark line verbatim.

### 5. Gallery — source `#p5`
- Masonry/bento grid of 7 photos (`gal-1` … `gal-7`), 13px gutters, square corners. Desktop: 12-col grid; reproduce the brochure's large-left + stacked-right rhythm. Mobile: 1-col, or horizontal snap carousel.
- Click opens a lightbox (arrow keys, Esc, swipe). Alt text from the reference `alt` attributes.

### 6. Location — source `#p6`
- Large map: `Weston-Market-Map.jpg` full-bleed, ~640px desktop. Optional upgrade: an interactive map (Google Maps / Mapbox) centered on **26.0922635, -80.365178**, zoom 13, with the hotel pin; keep the static image as fallback.
- Inset card top-left over the map: `map-inset-3.jpg` 232×134 (scale to ~320px web), 1.5px white frame, radius 7px, shadow `0 14px 30px -8px rgba(6,26,46,0.55), 0 3px 8px rgba(6,26,46,0.22)`, with "Cleveland Clinic" and "Hotel" pill callouts (white pill, 10px, 700, `#0B2B48`).
- Address line + "Open in Google Maps" link button (`https://www.google.com/maps/@26.0922635,-80.365178,17z`). Address: 2000 N Commerce Pkwy, Weston, FL 33326.
- Eyebrow "Drive-time proximity"; two-column distance list (10 rows) — name left `#2E3744`, distance right 600 `#0B2B48`, row divider `#D3D8E0`. Values verbatim from `#p6`.
- Background `#EEF2F6`.

### 7. Market Overview — source `#p7`
- Photo band `Weston-Aerial-2.jpg` (~460px). H2 "Market Overview". Six blocks in a 2-col grid (3-col at ≥1280px optional): Affluent, Master-planned Community · South Florida Tourism Momentum · Broward County Economic Fundamentals · Cleveland Clinic · Sports & Entertainment · Supply Dynamics. Title 17px 700; body 15px, line-height 1.5.
- Footnotes 1–9 verbatim.

### 8. The Sponsor — source `#p8`
- Photo band `Courtyard-Weston-3.jpg` (~280px).
- Statement H2 (18→28px, 400, line-height 1.28): first clause `#0B2B48`, second clause "in acquisitions, development, lending, and hotel property management." in `#2468A8`.
- Intro paragraph verbatim.
- 3 stat cards: `~$3.5B` Hospitality AUM¹ · `85` Assets Owned / Managed¹ · `~16,400` Keys¹ (value 28px, 600, `#2468A8`).
- **Investment Strategies panel** (radius 14px, border `1px solid rgba(36,104,168,0.16)`, background `linear-gradient(180deg,#FBFDFF 0%,#F2F7FC 100%)`): 4 columns separated by 1px `rgba(36,104,168,0.16)` rules — Acquisitions · Development · Lending · Management. Each: title 18px 400 `#2468A8`, paragraph, then two metrics pinned to bottom (value 22px 400 `#0B2B48`; label 10px 700 uppercase `#2468A8`). Collapse to 2×2 tablet, 1 col mobile.
- Footnotes 1–4 and the closing offering paragraph verbatim from `#p8`.

### 9. Contact — source `#p11`
- Dark navy field (same as hero). Centered `logo-white.svg` (220px).
- Two contact cards side by side (stack on mobile): **Wholesaler** — Andy Marshall, 404.247.3455, dstweston@driftwoodcapital.com · **National Accounts** — Joanna Venetch, 773.580.4308, jo@hana-solutions.com. Role eyebrow 10px 700 `0.16em` uppercase `#6FB0E0`; name 20px 500 white; details 15px `rgba(244,247,250,0.82)`. Phone = `tel:` link, email = `mailto:` link.
- Optional inquiry form (name, email, phone, accredited investor checkbox, message) — **confirm with Driftwood before adding**; not in the brochure.

### 10. Important Disclosures & Risk Factors — source `#p9`, `#p10`
- Full text verbatim, including the five bold sub-heads on `#p9` and three on `#p10`. Two-column CSS columns on desktop (`column-gap:40px`), single column mobile. Body 14px, line-height 1.55, `#2E3744`; lead paragraph 18px `#0B2B48`. Do not justify text on web (left-align).
- Do not collapse behind an accordion unless compliance approves; if collapsed, the first paragraph and a visible "Read full disclosures" control must remain.

### 11. Footer
- Navy `#061A2E`. Logo, both compliance lines from `#p11` (10px, 700, `0.1em`, uppercase, `rgba(244,247,250,0.55)`), © Driftwood Capital, link to driftwoodcapital.com.

## Interactions & behavior
- **Accredited-investor gate (to confirm):** first visit shows a modal over a `rgba(6,26,46,0.72)` scrim — paper card, short acknowledgement ("I confirm I am an accredited investor…" — copy to come from compliance), Accept / Leave. Persist acceptance in `localStorage`. Do not invent the acknowledgement wording.
- Header: transparent → solid on scroll past hero (160ms ease). Anchor links smooth-scroll with 72px offset; active link underlined `#2468A8` 2px.
- Scroll reveal: fade + 12px translateY, 360ms `cubic-bezier(0.2,0.7,0.2,1)`, once per element. Respect `prefers-reduced-motion`.
- Photo bands: optional parallax ≤0.3×.
- Buttons: primary fill `#0B2B48` → hover `#14385B` → active `#061A2E`, 160ms, no scale. Ghost: 1px border current color, hover fills `#0B2B48` with white text. On dark: ghost white.
- Links: color `#2468A8`, underline 1px offset 4px, 2px on hover.
- Cards: hover `--shadow-sm` → `--shadow-md`, translateY(-1px).
- Gallery lightbox as described above.
- Footnote markers can be links that scroll to their footnote (optional); keep the footnotes visible regardless.

## State
- `accreditedAccepted` (boolean, localStorage) — gate.
- `headerSolid` (scroll position > hero height).
- `activeSection` (IntersectionObserver) — nav highlight.
- `lightboxIndex` (number | null).
- Content is static; recommended to store copy in a single `content.ts` / CMS entry mirroring the section list above so compliance can review one file.

## Design tokens
Full set in `tokens/colors_and_type.css`. Values used:

Colors
- Navy ink-900 `#061A2E` (dark field, footer) · ink-800 `#0B2B48` (headings, primary) · ink-700 `#14385B` (hover)
- Accent ocean blue `#2468A8` (eyebrows, labels, bullets, stat values)
- Soft blue on dark `#6FB0E0`
- Slate-200 `#D3D8E0` (hairlines) · slate-400 `#6E7886` · slate-500 `#4A5564` (subheads, footnotes) · slate-600 `#2E3744` (body)
- Page `#F8FAFC`, alt band `#EEF2F6`, light text on dark `#E4EAF0`
- Card gradients: `#FEFEFF→#F1F5FA` (KPI), `#FDFEFF→#EDF3FA` (panel), `#FBFDFF→#F2F7FC` (strategies)
- Card borders: `rgba(36,104,168,0.08–0.16)`

Type — **Plus Jakarta Sans** only (variable 200–800; Google Fonts or self-host).
- Display/H1 300, `-0.02em` · H2/H3 300–400, `-0.02em` · body 400 · labels 600–700 uppercase.
- Eyebrows `0.22–0.24em` tracking; table labels `0.09em`; KPI labels `0.1em`.
- Numerals in stats use `font-feature-settings:'tnum' 1`.
- Web scale suggestion: 72 / 48 / 36 / 28 / 22 / 18 / 15 (body) / 13 / 11 / 10.
- Footnotes on web: 12px, line-height 1.4, `#4A5564`. Minimum body 15px.

Radii 6 / 12 / 14px; pills 999px. Shadows: sm `0 2px 6px rgba(11,43,72,.08)`, md `0 8px 24px -8px rgba(11,43,72,.18)`, lg `0 24px 60px -20px rgba(11,43,72,.28)`. Spacing 4pt base.

Do not use: gold, emoji, colored left-border accent cards, saturated red/green.

## Assets
- `assets/photos/` — compressed JPEGs (~2× brochure print size). For full-width web hero/bands, request the original high-res files from Driftwood (originals were uploaded to the design project); several are ~1600px wide and may soften on 2560px screens.
  - `cover-bg.jpg` — signature navy field (hero, contact)
  - `Courtyard-Weston-1…4.jpg` — section photo bands
  - `gal-1…7.jpg` — gallery
  - `Weston-Market-Map.jpg`, `map-inset-3.jpg` — location
  - `Weston-Aerial-2.jpg` — market overview
  - `Glenn-Wasserman.jpg` — not used in the brochure; ignore unless requested
- `assets/logo-color.svg`, `assets/logo-white.svg` — Driftwood Capital lockups
- `assets/brand-*.svg` — Marriott, Courtyard, Bonvoy marks (third-party trademarks; keep the trademark disclaimer line wherever they appear)
- Icons: none required. If needed, Lucide at 1.5px stroke.

## Files
- `reference/Weston DST Brochure.dc.html` — source brochure (all copy, footnotes, disclosures; sections `#p1`–`#p11`)
- `reference/support.js`, `reference/doc-page.js` — runtime needed only to view the reference
- `tokens/colors_and_type.css` — Driftwood design tokens
- `assets/` — images and logos

## Open questions for Driftwood
1. Is an accredited-investor acknowledgement gate required, and what is the approved wording?
2. Is an inquiry form wanted, and where do submissions go?
3. Should the page be indexed by search engines? (Default recommendation for a 506(c) offering page: `noindex` until compliance confirms.)
4. Should the site follow the institutional brochure (this handoff) or the public version, which drops the cap-rate row and the institutional header line?
5. Room count: brochure says 176 keys; the one-sheet copy supplied said 174. Confirm.
