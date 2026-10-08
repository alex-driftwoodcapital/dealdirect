# Platform stats — one source, never typed by hand

Every firm-level figure on the site (years, hotels, keys, AUM, employees, as-of date) comes from the Driftwood design system's **dwstats.js**: the compliance-vetted single source of truth. It computes hotels and keys from the vetted roster in mapdata.js, and holds management-reported figures (AUM, employees, years) in its MANUAL block.

## Current approved values (dwstats.js, as of September 1, 2026)
| Stat key | Value | Used on |
|---|---|---|
| `yearsExperience` | 30+ | EB-5 · Driftwood Capital section |
| `properties` | 78 (owned / sponsored / operated; credit excluded; dual-brands count as two) | EB-5 |
| `keys` | 15,162 (credit never included) | not displayed (removed from EB-5 by design) |
| `aum` | ~$3.5B | EB-5 |
| `employees` | ±6,000 | EB-5 |
| `asOf` | September 1, 2026 | EB-5 footnote 2 |

These replace the live /new-eb-5-page/ figures (30+ / 82 / 15,964 / $4B+ / ±6,000, as of April 7, 2025).

## Build in WordPress
1. Create an ACF (or field-plugin) **Options page** "Platform stats", with one field per key above. Never hard-code a figure in a page.
2. In Etch, output them with dynamic data: `{options.acf.platform_keys.numberFormat()}` etc. (check the namespace syntax in `etch-expert/reference/templates-dynamic-loops.md`). Build one `platform-stats` component and reuse it everywhere.
3. On every data refresh, the DS owner updates `dwstats.js` / `mapdata.js` first, then copies the values into the Options page. Optional: a small WP-CLI script that reads the values from `design/dwstats.js` + `design/mapdata.js` (run them in Node with a `window` shim) and writes the options.
4. Footnote 2 reads its date from `asOf`.

Rules carried from dwstats.js: credit positions are never counted as ours; dual-branded hotels count as two properties but their keys once.
