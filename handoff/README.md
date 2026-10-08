> **Received 2026-10-08. Build target overrides:** see the repo root `CLAUDE.md` (staging is `wordpress-1077248-6717515.cloudwaysapps.com`, a fresh install, not the `…6707404` copy named below). The handoff's `skills/` folder is not copied here; the installed skills live in `.claude/skills/`.

# Handoff: Driftwood DealDirect — Bricks → Etch + ACSS 4 rebuild

## Overview
driftwooddealdirect.com is the accredited-investor front door for Driftwood Capital offerings. It is currently WordPress + Bricks. This handoff rebuilds it in **WordPress + Etch + Automatic.css 4.x**, in the Driftwood Capital design system, on staging first:

- Staging: `https://wordpress-1077248-6707404.cloudwaysapps.com/` (Cloudways)
- Live: `https://driftwooddealdirect.com/`

Scope:
1. **Home (`/`)** — new layout: video hero, live-offering deal cards looped from the `offering` CPT, closed-offering grid, legal, CTA.
2. **Offering single (`/offering/{slug}/`)** — same sections and order as today, new look. Riverside Wharf Preferred Equity is the reference instance.
3. **EB-5 (`/eb-5-investments/`)** — same sections and order as today, new look.
4. **ES / PT EB-5 and `/new-eb-5-page/`** — no separate mock. Built from the EB-5 design with their own live copy (see `docs/build-order.md`).

Pages other than Home must read as a *refresh*: same content, same order, same CTAs, same forms. Do not restructure them.

## About the design files
Files in `design/` are **design references built in HTML** (Design Component prototypes). They show intended look and behaviour. They are **not** production code. Recreate them in Etch using Etch elements, components, loops and ACSS variables, following the skills in `skills/` — copy that folder to `.claude/skills/` in your repo first (start with `website-helpers`, then `etch-expert`, `acss-expert`). To view them rendered, open them in the design project (they load the Driftwood design-system bundle from `_ds/`, which is not included here).

## Fidelity
**High-fidelity.** Colours, type, radii, shadows and spacing are final. Copy is verbatim from the live site and must not be rewritten. Items marked `[from CPT]` are placeholders to be filled from the existing offering CPT.

## Screens
### Home — `design/DealDirect Home.dc.html`
| # | Section | Notes |
|---|---|---|
| 1 | Header (fixed) | Transparent over hero (white logo via `filter: brightness(0) invert(1)`, white nav), turns `rgba(255,255,255,.86)` + `backdrop-filter: blur(16px) saturate(1.5)` + 1px `rgba(219,229,240,.9)` bottom rule after 40px scroll. Height 88 → 68px, 360ms `cubic-bezier(.2,.7,.2,1)`. Links: Live offerings (#offerings), Past offerings (#past), EB-5. Buttons: Login (ghost), Sign Up (filled). Nav links hide < 760px. |
| 2 | Hero | Full-bleed **Dream video** (muted, loop, autoplay, playsinline; poster `Riverside-Wharf_View-from-River.jpg`). Two overlays: 100° navy gradient (.88 → .30) and vertical vignette. 48×2px teal-soft rule, 11px eyebrow, H1 "Invest today with DealDirect" (300 weight, clamp 42–88px, −0.036em), lede verbatim. CTAs: Start Investing (opens registration), View offerings (glass ghost). Bottom rail: one cell per live offering (status / title / tag / arrow), loops the same CPT query as the cards. |
| 3 | Live offerings | Eyebrow + H2 "Open for investment" + short note. Grid `repeat(auto-fit, minmax(min(100%,280px),1fr))`, gap 20px → 4-up at 1334px, 2-up tablet, 1-up mobile. **Deal card** = DS property card, dark: min-height 540px, radius 24, specular gradient border, full-bleed photo, progressive blur + navy fade veil (bottom 46% solid `rgba(6,26,46,.94)`, 28% ramp above), status chip top-left (dot: teal-soft = Open, `#E9C46A` = Coming soon), 38×1 teal rule, tag eyebrow, title 21/500, summary 14/1.6, CTA "View Offering →". Coming soon: CTA replaced by "Get notified" → inline email field + "Notify me" → success line. Hover: translateY(−4px). |
| 4 | Past offerings | Grid `auto-fill minmax(280px,1fr)`, gap 16. Tile 4:5, radius 20, photo, bottom gradient, white "CLOSED" pill top-left, tag eyebrow + name bottom. Not linked. |
| 5 | Legal | Two columns: "Legal disclosure" and "* Target Returns" — verbatim, 12px / 1.7, slate-600. |
| 6 | ~~CTA~~ | Removed from Home. |
| 7 | Footer | Navy. Logo, "Existing investor? Log into your dashboard." (Juniper Square URL), copyright line verbatim, Privacy / Terms. |
| — | Modals | Login (email, password, Log In, Forgot password). Registration: 2 steps (About Your Accreditation → About You) with "Our Apologies" branch when "None of the above" (nothing sent to HubSpot). Returning visitors get "Confirm your email". Same dialog is reused on every offering page and the home QOZ card. Copy verbatim. Custom Etch UI → WP REST endpoint → native HubSpot forms; see `docs/hubspot-setup-steps.md`. |

**Home, tax-advantaged section** (`#tax-advantaged`, between Live offerings and Past offerings): verbatim from the main site's Tax-Aware Investing page. Three cards (QOZ funds, DSTs, Bonus depreciation), 3 columns, 1 column ≤900px (never 2+1). Footnotes 1–2 sit under the cards. Open items: confirm DST/Tax Advantage Strategy offering names vs the live cards (Courtyard DST, Advantaged Strategy 2026), and the real driftwoodcapital.com URLs for "Learn how it works".

### Offering single — `design/Riverside Wharf Preferred Equity.dc.html`
Hero (photo, eyebrow, H1, Request Investor Details) → Target metrics (4 light stat cards + footnotes) → **sticky sub-nav** (Metrics · Overview · Video · Partners · Offering · OZ Benefits · Program · Market · Rationale · Legal; sticks at `top: 68px`, horizontally scrollable on mobile) → Overview (image + copy + CTA + footnotes) → Video (#webinar, embed the existing video) → Partners (TAO, Dream cards) → Offering (cap-stack bar, highlights list, footnotes) → Market (navy) → OZ incentives → Target metrics repeat (dark) → Proposed program (4 tabs, each a gallery with thumbs + spec panel) → Investment rationale (8 numbered cards) → Legal → CTA → Footer. Anchor IDs are unchanged from the live page (`#metrics #overview #webinar #partners #offering #structure #assets #market #rationale #legal`) — keep them, external links use them.

### Offering single — QOZ variant — `design/Riverside Wharf QOZ.dc.html`
Same template as Pref with the OZ incentives section (#structure) shown and a "Coming soon" chip in the hero. The Pref single hides #structure and its sub-nav item. Make the OZ section a per-offering toggle field (`show_oz_section`) and the highlighted cap-stack layer a field (`offering_layer`).

### EB-5 — `design/EB-5 Investments.dc.html`
Built from **/new-eb-5-page/** (layout + copy), with the immigration timeline kept from the old /eb-5-investments/, and duplicates removed. Order: Hero (eyebrow "EB-5 Investment", H1 = offering name, source sentence as lede) → Benefits (4 cards) → Investment / Job Creation requirements → Available Offerings (Riverside Wharf EB-5, Download Brochure; media = muted looping Vimeo background video 1079927883 "Dream Website banner", `background=1`, cover-fit, with the View-from-River JPG as poster/fallback) → What is the EB-5 Program (`#program`) → Immigration process timeline → **Driftwood Capital** (`#driftwood`: Benefits of investing directly with the developer — 5 points + 5 platform stats; the developer-led headline / Why Driftwood / 4 EB-5 stats block from /new-eb-5-page/ is intentionally omitted) → Prior EB-5 Projects (6) → FAQ (10; the 3 that repeat the Program / Requirements sections are dropped) → Legal (Target Returns appears once, here) → CTA → Footer. Serves `/eb-5-investments/`; `/new-eb-5-page/` (noindex draft) can be retired after launch — confirm. ES/PT pages get this layout with their own copy.

## Interactions
- All motion: 160–480ms, `cubic-bezier(.2,.7,.2,1)`. Buttons compress `scale(.972)` on press. Respect `prefers-reduced-motion` (no transitions, no smooth scroll, no autoplaying video → show poster).
- Modals: overlay `rgba(6,26,46,.72)` + 6px blur, white panel radius 24, max-width 520, Escape and backdrop click close, focus trapped, focus returns to trigger.
- Program tabs: `role="tablist"`, arrow-key navigation, first thumb selected on tab change.
- `scroll-padding-top` 136px on offering pages (header + sub-nav).

## Design tokens
See `docs/acss-mapping.md` for how each maps onto ACSS 4 settings.
- Navy: ink-900 `#061A2E`, ink-800 `#0B2B48` (primary), ink-700 `#14385B` (hover), ink-600 `#22527F`
- Ocean accent ("gold-*" names in DS): 700 `#1B5388`, 600 `#2060A0`, 500 `#2468A8`, 400 `#5C97C9`, 300 `#B6D5EC`
- On-dark accent: teal-soft `#6FB0E0`
- Slate: 50 `#F5F6F8`, 100 `#E9ECF0`, 200 `#D3D8E0`, 300 `#A9B2BE`, 400 `#6E7886`, 500 `#4A5564`, 600 `#2E3744`, 700 `#1C2430`; body copy `#48535F`
- Paper `#FFFFFF`; card wash `linear-gradient(160deg,#FFF 0%,#FDFEFE 54%,#F5F9FD 100%)`, border `rgba(219,229,240,.7)`
- **No accent rules/lines above headings or in cards** (design decision — the DS 48×2 rule is not used on this site).
- **KPI cards — one design everywhere** (component `stat-card`): light = DS `.dw-stat-card` (specular gradient border, white→#EDF2F7 fill, radius 20, padding 26/24); dark = glass (rgba(255,255,255,.06) fill, 1px rgba(255,255,255,.16) border, inset top highlight, radius 18). Value 28–38px / 300 / −0.03em with qualifier ("Target*") at the same size; label 15px / 500 below.
- Type: Plus Jakarta Sans variable (200–800) only. H1 300; H2 300; H3 300–500; eyebrows 11px/700, 0.22em, uppercase. Footnotes and legal text 14px / 1.7 (body copy is 15–16px), always one column at full content width (1334px), never in multi-column grids or narrowed with max-width.
- Radii: 10 (inputs), 12 (buttons), 14–16 (small cards), 20 (stat/past tiles), 24 (cards, modals, CTA), 999 (chips)
- Shadows: card `0 2px 6px rgba(11,43,72,.05), 0 20px 44px -20px rgba(11,43,72,.26), 0 52px 96px -44px rgba(11,43,72,.32)`; light card `0 1px 2px rgba(11,43,72,.025), 0 10px 28px -16px rgba(11,43,72,.09), 0 34px 60px -34px rgba(11,43,72,.13)`
- Content width 1334px, gutter 32px desktop.

## Assets
- `assets/cover-bg.png` — DS baked dark field (CTA, video band, metrics repeat)
- `assets/logo-driftwood-capital*.svg` — DS logos (only if the DealDirect logo is replaced)
- DealDirect logo and all photography: already in the WP media library (`/wp-content/uploads/…`). Reuse attachment IDs; do not re-upload.
- **Dream video:** `https://driftwooddealdirect.com/wp-content/uploads/Dream_Website_banner.mp4` (already in the media library). Create a WebM alongside it and serve both (`<source type="video/webm">` first, MP4 fallback), plus a poster JPG:
  ```
  ffmpeg -i Dream_Website_banner.mp4 -c:v libvpx-vp9 -b:v 0 -crf 34 -row-mt 1 -an -vf "scale=1920:-2" Dream_Website_banner.webm
  ffmpeg -i Dream_Website_banner.mp4 -ss 1 -frames:v 1 -q:v 3 Dream_Website_banner-poster.jpg
  ```
  `-an` strips audio (hero is muted). Upload both to the media library next to the MP4.
- Past-offering and Courtyard / Advantaged Strategy images come from the CPT export.

## Files
- `design/DealDirect Home.dc.html`, `design/Riverside Wharf Preferred Equity.dc.html`, `design/EB-5 Investments.dc.html`
- `design/evidence-register/` — compliance register (internal; open items must clear before launch)
- `docs/etch-components.md` — component inventory, BEM names, props
- `docs/acss-mapping.md` — ACSS 4 dashboard settings
- `docs/cpt-schema.md` — `offering` CPT + fields + home loops
- `docs/permalinks.md` — URL map, redirects, SEO carry-over
- `docs/eb5-localization.md` — EN/PT/ES EB-5 pages share one template; permalink map, hreflang, number formats, items for compliance review
- `docs/platform-stats.md` — firm figures pulled from the DS `dwstats.js` (single source), implemented as a WP Options page
- `docs/hubspot-setup-steps.md` — HubSpot: 3 form GUIDs, field names, accreditation value map, consent + subscription IDs, UTM capture, site behavior, WP endpoint. Offering = form + page URL (no hidden offering field).
- `docs/build-order.md` — build sequence + QA checklist
- `CLAUDE.md` — standing instructions for Claude Code (fill the placeholders)
- `skills/` — the 10 Etch/ACSS skills (copy to `.claude/skills/`)


## Background rule
The dark `cover-bg.png` navy field is reserved for the footer and special moments (hero, Get started band). Regular content sections use the light field (white → #EDF4FA). Never stack a regular dark section directly after another dark one.


## Riverside Wharf hero media
Pref + QOZ heroes: self-hosted `Dream_Website_banner.mp4` (WP uploads) as a muted, looping, inline background `<video>` (autoplay muted loop playsinline, object-fit:cover), poster = Riverside-Wharf_View-from-River.jpg. Keep the "Rendering" chip. Honour prefers-reduced-motion by pausing the video.
