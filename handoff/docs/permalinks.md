# Permalink map — nothing changes

| URL | Today (Bricks) | Rebuild (Etch) | Design reference |
|---|---|---|---|
| `/` | Page (front page) | Same page ID, rebuilt | `DealDirect Home.dc.html` |
| `/offering/riverside-wharf-preferred-equity/` | `offering` single | Etch template for `offering` single | `Riverside Wharf Preferred Equity.dc.html` |
| `/offering/[QOZ slug — confirm]/` | new `offering` post (coming soon) | same template; OZ section ON | `Riverside Wharf QOZ.dc.html` |
| `/offering/{other-slugs}/` | `offering` single | same template | — |
| `/eb-5-investments/` | Page | Same page, rebuilt | `EB-5 Investments.dc.html` |
| `/inversiones-eb-5/` | Page (ES) | EB-5 layout, ES copy from live | EB-5 |
| `/investimentos-eb-5/` | Page (PT) | EB-5 layout, PT copy from live | EB-5 |
| `/new-eb-5-page/` | Page (live landing page) | Refresh as-is, its own sections in EB-5 styling | EB-5 |
| `/forgot-password/` | Page | Keep; restyle form only | — |

## Rules
- Rebuild **in place** on the same post IDs. Do not delete-and-recreate (keeps slugs, SEO meta, internal links, analytics history).
- `offering` rewrite slug stays `offering`, `with_front` unchanged. After any CPT change: `wp rewrite flush --hard` on staging and re-check every URL above returns 200.
- Keep anchor IDs on offering singles: `#metrics #overview #webinar #partners #offering #structure #assets #market #rationale #legal`. EB-5: `#legal`.
- Carry over per page: SEO title, meta description, canonical, OG image (e.g. `Riverside-Wharf_View-from-River.jpg`, `EB-5-Background.jpeg`), robots.
- Keep GTM `GTM-NX8DQZGQ`, Juniper Square login URL, external-link "You are now leaving our website" interstitial.
- Before go-live: crawl live and staging (same URL list), diff status codes and canonicals. No 301s should be needed; if one appears, stop and ask.
