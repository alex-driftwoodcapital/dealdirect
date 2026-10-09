# Go-live plan: DealDirect on Etch + ACSS

Nothing here runs without Alex's typed OK (CLAUDE.md: AUTHORIZED_SITE is staging only until then). Each
**Blocker** must be closed or explicitly accepted before the switch. This plan lists steps; it writes nothing.

## 1. Blockers (all must be closed)

| # | Blocker | Owner | How it's verified |
|---|---|---|---|
| 1 | Evidence register: every open `gap` / `check` traced or accepted (see `docs/compliance-report.md`) | Compliance | Report shows 0 open items |
| 2 | Riverside Wharf QOZ metrics: the `[TBD]` placeholders and the Pref footnotes carried on the QOZ page replaced or approved | Compliance / Alex | Register item "RW QOZ · Metrics" closed |
| 3 | All live offerings on the new Home (incl. Tax Advantaged Strategies 2026 and the Income hotel fund DST) with their card fields and pages | Build | Home loop shows every live/coming-soon offering; crawl diff has no missing offering URL |
| 4 | Design fidelity pass against the handoff on every page (hero titles, link colors, section details) | Build, Alex reviews | Side-by-side screenshots at 375 / 768 / 1440 |
| 5 | 404 page copy approved (written 2026-10-09 at Alex's request) | Alex | Alex's OK on `site/pages/template_404.py` |
| 6 | HubSpot test submissions on staging: Registration, Offering Request, EB-5 Registration, each reaching its form and triggering its workflow (follow-up email / brochure) | Alex (test email) | Submission visible in HubSpot under each form |
| 7 | HubSpot tracking tag confirmed inside the GTM container (the site loads only GTM) | Alex / marketing | GTM preview on staging with `DD_GTM_ON_STAGING` shows the HubSpot tag firing |
| 8 | Cookie notice: the first-party cookies `dd_lead` and `dd_utm` (and GTM's) listed in the cookie notice and the Privacy Policy; consent tool and GTM consent mode chosen | Alex / legal | Privacy Policy page published with the list |
| 9 | Privacy Policy and Terms of Use pages exist at the footer's URLs | Alex / legal | Crawl diff: both 200 |
| 10 | QA job green on staging (browser checks + crawl diff, live vs staging) | Build | `qa/latest` report: no problems |
| 12 | Preferred Equity's live sub-nav anchors `#structure` `#assets` `#rationale`: the approved design has no such sections; decide where each lands (or accept the loss) | Alex | Crawl diff no longer lists "anchors dropped by the design" |
| 11 | Previous build's leftover components/templates on staging removed (etchnavcomponent, etchburgercomponent, header, footer, home template) | Build | Done 2026-10-09 (in WP Trash, JSON backup); `ops/cleanup/retire.sh` keeps it so |

## 2. Choose the switch method (Alex)

**A. Point the live domain at the staging app (recommended).** Cloudways: clone the staging app to a production
app (or promote it), add `driftwooddealdirect.com` as its primary domain, issue SSL, then move DNS.
- Nothing from the Bricks site comes along, so its GTM snippet, Rank Math and old pages can't double up.
- Rollback = point DNS back at the Bricks server (keep it running, untouched, for at least 2 weeks).

**B. Deploy into the live WordPress install.** Same scripts with a live profile.
- Needs: Etch, etch-theme, ACSS 4.0.1, Secure Custom Fields installed there; the live site's own GTM snippet
  (`wp_head` / `wp_footer` code) **turned off at the same moment**, or GTM loads twice and every pageview counts
  double; Rank Math deactivated (dealdirect-core prints titles, OG and canonical; two SEO plugins would duplicate them).
- Rollback = full Cloudways backup restore. Riskier; only if the live server must stay.

## 3. Switch day (method A)

1. **Freeze.** No Etch builder edits on staging (rule 9); last deploy from `main` green; QA green.
2. **Backups.** Cloudways backup of the Bricks site (files + DB) and of staging.
3. **Production settings** on the new app:
   - Settings > Reading: untick "Discourage search engines". This also turns GTM on (`includes/tracking.php`
     loads it only while the site is public) and lets `dealdirect-core` print the live robots default.
   - `wp-config.php`: `DD_HUBSPOT_TOKEN` (from the secret store, never pasted in chat); remove `DD_GTM_ON_STAGING` if set.
   - Turn off Cloudways password protection.
   - Site URL / Home URL to `https://driftwooddealdirect.com` (`wp search-replace` on the staging host name, `--dry-run` first).
4. **Sitemap.** Live serves Rank Math's `/sitemap_index.xml` (submitted in Search Console). The new site serves
   WordPress's `/wp-sitemap.xml`: add a 301 from `/sitemap_index.xml` and `/page-sitemap.xml` to it, and submit
   the new sitemap in Search Console.
5. **DNS** to the new app; wait for SSL.
6. **Verify on live** (same tools, live base URL):
   - Run the QA job with `QA_BASE_URL=https://driftwooddealdirect.com` (no basic auth): every page 200, the 301s and
     410s, Plus Jakarta Sans, ACSS, `<html lang>`, hreflang, the exit-link interstitial, the 404 page.
   - GTM Tag Assistant: one GTM container load per page, HubSpot tag firing.
   - One real submission per form with an internal test address; check HubSpot and the workflow email.
   - Juniper Square login link opens through the interstitial.
7. **Purge** caches (Cloudways Varnish / Breeze) and re-run step 6's QA once.

## 4. After go-live

- Search Console: submit the new sitemap; watch Coverage for 404s for two weeks (the crawl diff lists every old URL
  and its decided status, so any new 404 is a miss to fix with a 301 entry in `includes/retired.php`).
- HubSpot: compare form submissions per day with the previous two weeks.
- Keep the Bricks site/backup for 2 weeks, then archive.

## 5. Rollback

- Method A: DNS back to the Bricks server (TTL lowered to 300s the day before), re-enable its caches.
- Method B: restore the Cloudways backup from step 2.
- Either way: tell HubSpot owners that submissions between the switch and the rollback came from the new forms.
