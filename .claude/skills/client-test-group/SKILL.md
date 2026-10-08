---
name: "client-test-group"
description: "Simulate 3-5 prospective customers browsing a live or staging site and report friction, booking/bounce reasons, objections and a ranked fix list. Read-only; hypotheses, not data."
---

# Client test group (simulated)

Purpose: find friction by walking the site as realistic buyers. **It finds friction. It does not validate demand.** Everything is a simulated hypothesis.

## Setup (fill in per project)
Site: `[LIVE_URL]` or staging `[STAGING_URL]`. Audience: `[TARGET_AUDIENCE]`. Primary conversion: `[PRIMARY_CTA]` (e.g. booking, contact form, purchase). Price/offer facts to verify against the page: `[OFFER_FACTS]`.

## Rules
- Read-only. Never edit the site, submit forms, book, or send anything. Stop at the form/pop-up; describe it, don't submit.
- Label every output "Simulated hypothesis". Never invent metrics, conversion rates, quotes, testimonials or budgets beyond the persona card. Quote only text actually seen on the page (verbatim, with page).
- Real browser required. If none is available, say so and stop; don't guess from memory.
- Test against the project's own copy/design rules and flag violations as findings.
- Test phone width for at least 2 personas, desktop for the rest.
- Lean: skim each page once per persona, no screenshots unless a defect needs proof.

## Personas (pick 3-5, tailor to `[TARGET_AUDIENCE]`)
Each card: role, goal, fear, budget reality, device, language, how they arrived. Typical spread: the day-to-day user, the budget decision-maker, the cost-conscious evaluator, a non-native-language or mobile-first visitor, a skeptic who wants proof and risk.

## Journey per persona
Enter via Home, then scan hero, proof/portfolio, services, pricing, blog/resources, about, FAQ, then the primary CTA and any fallback. Record per step: what they looked for, found/missed, confusion, trust gained or lost, objection raised. End with one outcome: **Converts / Sends inquiry / Bounces / Comes back later**, plus the single reason.

## Output (short)
Header: date, URL, device(s), "Simulated hypotheses, not data".
Per persona (max ~120 words): persona line, path taken, stalled at (page + element), objections, what they'd say (marked simulated), outcome + reason.
Ranked fix list (max 10 rows): rank, issue, personas hit, page/element, suggested fix, effort (S/M/L).
One-line caveat: simulated; validate the top 3 with real prospects.
