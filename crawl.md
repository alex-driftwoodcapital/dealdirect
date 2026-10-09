# Crawl diff, live vs staging — 2026-10-09 22:41 UTC

14 URLs (live sitemaps + REST listings + decided old URLs + new pages).

**No unexpected status changes or lost anchors**


| URL | Live | Staging | Problems | Differences (for review) |
|---|---|---|---|---|
| `/` | 200 | 200 | ok | – |
| `/admin-login/` | 200 | 410 | ok | – |
| `/eb-5-investments/` | 200 | 200 | ok | h1 “Get your Green Card by investing in hotels in the U.S.” → “Riverside Wharf Miami” |
| `/forgot-password/` | 200 | 410 | ok | – |
| `/inversiones-eb-5/` | 200 | 200 | ok | h1 “Obtenga su residencia americana invirtiendo en hoteles en U.” → “Riverside Wharf Miami” |
| `/investimentos-eb-5/` | 200 | 200 | ok | h1 “Obtenha sua residência americana investindo em hotéis nos EU” → “Riverside Wharf Miami” |
| `/new-eb-5-page/` | 200 | 200 | ok | h1 “Access the path to U.S. Citizenship by investing in a hotel ” → “Riverside Wharf Miami” |
| `/offering/riverside-wharf-eb-5/` | 200 | 301 → `/eb-5-investments/` | ok | – |
| `/offering/riverside-wharf-preferred-equity/` | 200 | 200 | ok | anchors dropped by the design (decision pending): #structure #assets #rationale; h1 “” → “Riverside Wharf Miami” |
| `/offering/riverside-wharf/` | 200 | 301 → `/offering/riverside-wharf-qoz/` | ok | – |
| `/registration-success/` | 200 | 410 | ok | – |
| `/reset-password/` | 200 | 410 | ok | – |
| `/offering/driftwood-tax-advantage-strategy-i/` | 404 | 302 → `https://dtas1.driftwoodcapital.com/` | ok | – |
| `/offering/riverside-wharf-qoz/` | 404 | 200 | ok | – |
