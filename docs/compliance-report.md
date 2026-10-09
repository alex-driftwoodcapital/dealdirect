# Compliance report: evidence register

Generated from `handoff/design/evidence-register/claims.js` by `ops/compliance/report.mjs` (2026-10-09).
Every figure on the rebuilt pages was lifted verbatim from the live site, which is not a source document, so a
claim is only closed once compliance traces it to an offering document or accepts it in writing.

**46 open items block go-live** (CLAUDE.md rule 10): 27 `gap` and 19 `check`.
Also: 2 `internal` (live typos carried verbatim), 1 `traced`.

| Status | Meaning |
|---|---|
| `gap` | needs a source document (PPM, brochure, model, third-party report) and its locator |
| `check` | needs a compliance decision on the wording or figure shown |
| `internal` | a live typo carried verbatim (CLAUDE.md rule 1); compliance decides whether to fix |
| `traced` | traced to a source; nothing to do |

## Decisions already applied in the build
- "shovel-ready" removed everywhere, every language (Riverside Wharf is under construction; CLAUDE.md rule 2).
- Platform figures (30+ years, 78 hotels, 15,162 keys, ~$3.5B, ±6,000 employees, as of Sept 1, 2026) come from the platform-stats options page, not typed into pages (rule 8).
- Riverside Wharf has three vehicles: Preferred Equity, Common Equity QOZ, EB-5 (2026-10-09). The old /offering/riverside-wharf/ 301s to the QOZ page; /offering/riverside-wharf-eb-5/ 301s to /eb-5-investments/.
- Legal and footnote text is never below 12px or 4.5:1 contrast (rule 6).

## Home

| Status | Section | Claim | Shown on the page | Note / what closes it |
|---|---|---|---|---|
| `gap` | – | Riverside Wharf Pref — card summary | A transformative hospitality & entertainment development in the heart of Downtown Miami | Copy from live home. Close with offering brochure. |
| `gap` | – | Riverside Wharf QOZ — summary, tag, status | [from CPT] | Placeholder until offering CPT export. |
| `gap` | – | Courtyard DST — name, tag, summary | [from CPT] | Placeholder. Confirm whether this is Courtyard by Marriott Fort Lauderdale Weston. |
| `gap` | – | Advantaged Strategy 2026 — tag, summary | [from CPT] | Placeholder until CPT export. |
| `gap` | – | Past offerings — names and tags | 8 sample tiles | Sample names from the Driftwood portfolio, NOT confirmed DealDirect offerings. Replace from CPT (status = closed). |

## RW Pref

| Status | Section | Claim | Shown on the page | Note / what closes it |
|---|---|---|---|---|
| `gap` | Metrics | Net quarterly distributions (target) | 13.0% | Close with PPM / term sheet. |
| `check` | Metrics | Net equity multiple (target) | 1.65x | Live repeat block (hidden in source) showed 1.7x; design repeat block now matches top: 1.65x. Confirm 1.65x. |
| `gap` | Metrics | Minimum investment | $100,000 | PPM. |
| `gap` | Metrics | Assumed hold period | 5-Year (+ two 1-year extensions) | PPM. |
| `check` | Metrics repeat | Footnote 1 coupon | A14% annual coupon | Live hidden repeat block said 14%. Design repeat block now uses the top footnotes verbatim (13% / preferred return). Resolved by design; confirm. |
| `check` | Metrics repeat | Metric label | Net IRR | Design repeat block now uses Net Quarterly Distributions (as top). Live home card says Net IRR — not carried over. |
| `gap` | Overview | Hotel keys | 167-key | Development budget / brochure. |
| `gap` | Overview | Meeting & event space | ~18,000 SF | needs a source document (PPM, brochure, model, third-party report) and its locator |
| `check` | Overview | Entertainment venues | over 40,000 SF | Offering highlights say "nearly 100,000 square feet of entertainment space". Definitions differ — confirm both. |
| `gap` | Partners | TAO Group operating history | more than 25 years | needs a source document (PPM, brochure, model, third-party report) and its locator |
| `gap` | Offering | Total capitalization | ~$336M (as of Nov 25, 2025) | Stack sums: 145 + 60 + 35 + 96 = 336. Recomputes. |
| `check` | Offering | Cumulative LTC by layer | 43% / 61% / 71% / 100% | Recomputed: 145/336 = 43.2%, 205/336 = 61.0%, 240/336 = 71.4%. OK. |
| `gap` | Offering | Fees | 1.0% structuring / 1.0% annual AM | PPM Fees and Expenses. |
| `gap` | Market | Florida visitors Q3 2025 | 34.3 million | VISIT FLORIDA, Dec 31, 2025. |
| `gap` | Market | MIA passengers 2025 | nearly 56 million, +3.5 million YoY | Miami-Dade County / J.D. Power. |
| `gap` | Market | Miami MSA housing rank / millionaire growth | #2 / No. 5, +94% | Miami Realtors; Henley & Partners. |
| `gap` | Market | Hotel investment market rank | #2 | CBRE Investor Intentions 2025. |
| `gap` | Market | Downtown lux/UU RevPAR growth, occ, ADR | 5.9%, +4.6%, +1.2% | CoStar Nov 2025. Note 4.6% + 1.2% ≈ 5.9% compounding — plausible. |
| `gap` | Market | Miami lux/UU 12-mo ADR / RevPAR | $344.19 / $245.64 | CoStar Nov 2025. |
| `check` | Rationale | Blended land basis vs area average | ~$9M/acre vs $28M/acre, roughly 60% below | Recomputed: 1 − 9/28 = 67.9%, not ~60%. Compliance to confirm wording. |
| `gap` | Rationale | Ground lease | 80-year + two 10-year | City of Miami lease. |
| `gap` | Rationale | Parking savings | ~$9.5M | needs a source document (PPM, brochure, model, third-party report) and its locator |
| `gap` | Rationale | Wharf annual revenue | over $20M since 2017 | needs a source document (PPM, brochure, model, third-party report) and its locator |
| `check` | Rationale | Senior loan term sheet | $125M | Rationale 05 says $125M; rationale 07 and the cap stack say $145M. Rationale 07 also repeats 05 text verbatim. Resolve. |
| `gap` | Rationale | Year 1 NOI from entertainment | ~49% of targeted NOI | Model. |
| `check` | Rationale 05 + 07 | Project status | the Project is now shovel-ready | REMOVED everywhere (2026-10-02, Driftwood instruction): project is under construction. Pref: rationale section removed. QOZ: sentence removed from rationale cards 05 + 07. Live site still says shovel-ready. |

## RW QOZ

| Status | Section | Claim | Shown on the page | Note / what closes it |
|---|---|---|---|---|
| `gap` | Metrics | QOZ common equity target metrics (both blocks) | [TBD] | Page cloned from Pref. All four metrics, the target summary line and highlights 1–2 are placeholders. Footnotes 1–3, *, the "A14% annual coupon" note and highlights 3–8 (incl. 1.0% fees) are still the Pref text — compliance must confirm or replace for QOZ. |
| `check` | Offering | Cap stack highlight | Total equity ~$96M | Highlighted as the QOZ offering layer; confirm the QOZ common equity amount and whether it should be shown separately from pref. |

## EB-5

| Status | Section | Claim | Shown on the page | Note / what closes it |
|---|---|---|---|---|
| `check` | Why Driftwood | EB-5 raised to date | ~$87M | Source: /new-eb-5-page/. Recomputed from the six prior projects: 9.0+18.0+23.0+26.0+4.5+7.2 = $87.7M (~$88M). Confirm rounding. |
| `check` | Why Driftwood | EB-5 investors / projects / approval rate | 165+ / 6+ / 100% | Recomputed investors from project cards: 18+36+46+52+9+9 = 170 (165+ holds). 100% footnoted to USCIS approvals. |
| `check` | Offerings | Riverside Wharf EB-5 — status wording | shovel-ready (title + description) | REMOVED (Driftwood instruction): word deleted from offering title and description. Compliance to confirm the edited wording. |
| `gap` | Offerings | EB-5 Debt / Equity rate, duration | 2%* / 6%* / 3-5 Years | Supersedes the old page (0.5%-6%, 5 Years / 3 Years). Close with EB-5 PPM. |
| `check` | Prior projects | Home2 Fort Lauderdale jobs per investor | 17 Jobs | New page says 17; old /eb-5-investments/ says 12. Residence Inn status: new page Operating, old page Active. Design uses new page. |
| `internal` | Direct with developer | Typo | fund administrstors | Live typo, carried verbatim. |
| `check` | Timeline | Headline wording change | Illustrative EB-5 Immigration Timeline (was: EB-5 Immigration Process) | Changed at Driftwood request to signal the timeline is not a guarantee. Compliance to approve wording. |
| `check` | Projects | Riverside Wharf EB-5 annual rate | 0.5%-6% | Feature block lower on the page says 2%* target annual rate. Align. |
| `check` | Projects | Hold / debt term | 5 Years vs 3 Years | Projects card: Anticipated Hold Period 5 Years. Feature block: Anticipated Debt Term 3 Years. Align. |
| `gap` | Projects | Required investment | $800,000 USD | TEA threshold; USCIS. |
| `gap` | Projects | Target jobs per investor | 33.2 | Economist report. |
| `check` | Advantage | Accredited investor network | more than 1,200 as of December 2023 | Stale date (2023). Driftwood DS guide cites >850 LPs. Update or keep dated. |
| `internal` | Advantage | Hospitality management track record | 25- year | Typo on live ("25- year"). |
| `check` | Track record | Six projects: investors / capital / jobs / status | 18·$9.0M · 36·$18.0M · 46·$23.0M · 52·$26.0M · 9·$4.5M · 9·$7.2M | Recomputed $ per investor: $500K for five rows (pre-RIA minimum) but Staybridge = $800K. Plausible (post-2022), confirm. |
| `check` | Form | Form labels | "Nombre", "¿Cómo prefiere que le contactemos?", "Enviar Información" | Spanish strings on the English form. Design uses English; confirm. |

## How to close an item
- Drop the source document into `handoff/design/evidence-register/evidence/` (or link it), fill the claim's `file` and `locator`, and set its status to `traced`.
- For a `check`, record compliance's decision in the claim's `note` and set the status to `traced` (accepted as is) or change the figure in the design file first (the copy gate then requires the page to match).
- Re-run `node ops/compliance/report.mjs > docs/compliance-report.md`.
