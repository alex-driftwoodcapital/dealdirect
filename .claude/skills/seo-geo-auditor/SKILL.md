---
name: "seo-geo-auditor"
description: "Technical SEO and GEO (AI answer engine) audit of a website: schema, sitemap, titles, llms.txt, bot access, Search Console. Read-only."
---

# SEO + GEO auditor

Read-only. For keyword/content-gap work, use a dedicated SEO skill if available. If a previous audit exists for the site, re-verify it; don't assume fixed.

## Honesty rules
- No "100%" score exists. Aim for zero technical errors, complete structured data, answer-ready copy. Scores are judgment, label them so. Nobody controls whether ChatGPT or Google cites a site.
- Some hosts return a captcha/202 to datacenter IPs. Fetch from a real browser or a local machine; mark anything unfetched as unverified.

## Checklist
**Crawl/index:** status codes, canonicals, no stray noindex, robots.txt, sitemap lists all pages, no duplicate sitemap routes, www/non-www single-hop redirect, HSTS, custom 404, no dead internal links.
**On-page:** unique title (<=60) and meta (<=160) per page, exactly one H1, sane H2/H3 order, no empty headings, alt text, internal links between related pages, server-rendered content (not JS-only).
**Schema:** Organization (name, logo, url, sameAs), Service/Offer or Product, FAQPage, ItemList, Person, BreadcrumbList without duplicates, no leftover old-brand names.
**GEO:** llms.txt, quotable definition blocks, answer-first summaries, AI-bot access allowed (GPTBot, ClaudeBot, PerplexityBot, Google-Extended, OAI-SearchBot) in robots AND host security, brand entity presence, Google Business Profile for local businesses.
**Search Console:** sitemap submitted, home re-indexed under the current brand title.
**Speed:** Lighthouse/CWV only if actually run; otherwise "unverified".

## Output
Score table (judgment), then findings tagged P0/P1/P2 and SAFE (can be fixed in site/config) / OWNER (needs their account) / DISCUSS (copy or brand call). Save to a dated file (`seo-geo-<date>.md`); reply with the top 5 only.
