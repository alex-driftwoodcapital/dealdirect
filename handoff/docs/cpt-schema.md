# `offering` CPT

The CPT already exists on the Bricks site. **Step 1 is to export it, not redesign it.** Run on staging:

```
wp post-type get offering --format=json
wp post list --post_type=offering --fields=ID,post_title,post_name,post_status --format=csv
wp post meta list <ID> --format=json     # for 2–3 offerings, to learn the field keys
```

Identify the field plugin (ACF / Meta Box / JetEngine / Bricks native) and keep the existing field keys. Map them to the fields below; add only what is missing.

## Required fields
| Field | Type | Used by | Notes |
|---|---|---|---|
| `offering_status` | select: `open` / `coming_soon` / `closed` | Home grids, chip | Drives which loop the post appears in |
| `offering_tag` | text | card eyebrow, rail, past tile | e.g. "Preferred Equity · Miami, FL" |
| `card_title` | text (optional) | card | falls back to post title |
| `card_summary` | textarea ≤ 140 chars | live card | compliance-approved line |
| `card_image` | image | cards, past tiles | falls back to featured image |
| `card_cta_label` | text, default "View Offering" | live card | |
| `notify_form` | form ID | coming-soon card | email capture |
| `home_order` | number | both loops | ascending |
| `metrics` | repeater: `value`, `qualifier` ("Target*"), `label`, `footnote` | single — metrics blocks | keep existing if present |
| `brochure` | file | single, EB-5 | "Download Brochure" (gated by form) |

## Home loops (Etch Loop Manager)
```php
// liveOfferings
$query_args = [
  'post_type' => 'offering',
  'posts_per_page' => -1,
  'meta_query' => [[ 'key' => 'offering_status', 'value' => ['open','coming_soon'], 'compare' => 'IN' ]],
  'meta_key' => 'home_order', 'orderby' => 'meta_value_num', 'order' => 'ASC',
];
// pastOfferings — same with 'value' => 'closed'
```
Markup pattern (verify syntax against `etch-expert/reference/templates-dynamic-loops.md`):
```
{#loop liveOfferings as item}
  <article class="deal-card">
    … {item.meta.offering_tag} … {item.title} …
    {#if item.meta.offering_status === "coming_soon"} notify form {/if}
    {#if item.meta.offering_status === "open"} <a href={item.permalink.relative}>…</a> {/if}
  </article>
{/loop}
```
Use `item.etch.*` / `item.meta.*` / `options.acf.*` per the field plugin found in step 1.

## Live offerings to populate
1. Riverside Wharf Miami — Preferred Equity (`/offering/riverside-wharf-preferred-equity/`) — open
2. Riverside Wharf Miami — QOZ — coming_soon (no single page yet)
3. Courtyard DST — open (confirm slug)
4. Advantaged Strategy 2026 — open (confirm slug)
All past offerings → `closed`.
