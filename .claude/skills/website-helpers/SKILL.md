---
name: "website-helpers"
description: "Router for the Etch/ACSS website skills: which one to use to build, edit, style, audit or test a site. START HERE when a website task comes up and the right skill is unclear."
---

# Website helpers (router)

| Need | Use |
|---|---|
| How to do it properly in Etch (HTML, CSS nesting/chaining, JS, components, loops) | `etch-expert` |
| Style with ACSS 4 (variables, tokens, utilities) | `acss-expert` |
| Edit existing pages, copy, styles (staging first) | `etch-page-editor` |
| Build a NEW page or component natively in Etch | `etch-builder` |
| Run any of the above unsupervised, safely | `site-build-runner` |
| Passive security audit of a site you own or are authorized to audit | `security-auditor` |
| Tracking codes: what fires where, conversions, tags on sensitive pages | `tracking-auditor` |
| Technical SEO + AI-answer (GEO) audit | `seo-geo-auditor` |
| See the site through simulated visitors (hypotheses only) | `client-test-group` |

## Typical flow
Audit (read-only) > ranked fix list > owner approves > `site-build-runner` on staging > re-audit read-only > owner approves go-live.

## Standing rules
- Audits never edit. Builds go to staging first; go-live, deletes, DNS and sends need explicit owner approval.
- Use a real browser for audits; never claim an absence you did not see.
- Read the project's brand/copy rules before editing copy.
