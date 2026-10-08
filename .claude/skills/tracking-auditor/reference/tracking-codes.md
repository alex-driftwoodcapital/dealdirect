# Tracking code detection and verification (reference)

Fetched 2026-10-02 from primary vendor docs (URLs inline). Items tagged [UNVERIFIED] were NOT confirmed in a fetched primary page; confirm with a live network capture before reporting them as fact. Not legal advice.

Method: passive only. Load the client's own page in a browser, open DevTools > Network (Preserve log, disable cache), view source, and note requests. A script tag alone does not prove a tag fired; an outbound request does.

## 1. Google tag / GA4 / Google Ads (gtag.js)
Source: https://developers.google.com/tag-platform/gtagjs/install
- Snippet: `<script async src="https://www.googletagmanager.com/gtag/js?id=TAG_ID"></script>` then `window.dataLayer = window.dataLayer || []; function gtag(){dataLayer.push(arguments);} gtag('js', new Date()); gtag('config','TAG_ID');`
- GA4 ID format `G-XXXXXXXX`; Ads tag IDs are `AW-`. (GA4 `G-` format: [UNVERIFIED] on fetched pages; Google Ads tag IDs are found at ads.google.com/aw/tagsettings per the same doc.)
- Proof the tag fired (Google's own wording): "If you see requests to googletagmanager.com, your tag is firing." Per product: Google Ads = `googleadservices.com` or `googlesyndication.com`; Analytics = `google-analytics.com` or `analytics.google.com`; Floodlight = `doubleclick.net`.
- Doc note: if a product shows no requests, events may not be sent via the `event` command even though `config` ran.
- GA4 hit path `/g/collect` on those hosts: from search summary of Google docs (https://developers.google.com/analytics/devguides/collection/ga4/troubleshoot); open the request Payload tab for params. Exact param names (tid, en, dl): [UNVERIFIED].
- Measurement Protocol (server-side): `POST https://www.google-analytics.com/mp/collect` (EU: `https://region1.google-analytics.com/mp/collect`), needs `api_secret` + `measurement_id` (web) or `firebase_app_id`. Designed for server/trusted use, so you will not see it in a browser. https://developers.google.com/analytics/devguides/collection/protocol/ga4/sending-events
- Google's GA PII rule: no data passed that Google could recognize as PII; includes emails, phones, SSNs, PII in URLs, page titles, form/search data, custom dimensions, campaign params, event data. https://support.google.com/analytics/answer/6366371
  Audit hint: check URLs/titles/query strings on intake pages for names, emails, case types.

## 2. Google Tag Manager
Source: https://developers.google.com/tag-platform/tag-manager/datalayer
- Loader: `https://www.googletagmanager.com/gtm.js?id=GTM-XXXXXX`; noscript fallback is an iframe to `ns.html`. dataLayer start events: `gtm.start`, `event:'gtm.js'`; also `gtm.load`.
- Container IDs `GTM-`. Container contents are public: fetch `gtm.js?id=GTM-...` (the owner's own container) and read which tags/IDs it carries. Treat as inspection of your own client's asset only.
- `dataLayer.push({'event':'name'})`; init `window.dataLayer = window.dataLayer || [];` before GTM.
- GTM can load every other vendor below (Meta, TikTok, LinkedIn, HubSpot, Hotjar, Clarity); a GTM container means the page source will not show them. Judge by network requests.
- Scoping a tag to specific pages (https://support.google.com/tagmanager/answer/7679319): under "This trigger fires on" choose "Some Events" and add a condition so it fires only where required (doc example uses Click URL contains /path). Page Path / Page URL variables as the condition variable is the usual form [UNVERIFIED in fetched text]. Trigger order: Consent Initialization, Initialization, Page View, DOM Ready, Window Loaded.
- Blocking/exception triggers: [UNVERIFIED in fetched text]; confirm in GTM UI. Preferred pattern for sensitive sites: allow-list (fire only on named pages), never exclude-list.
- Verify scoping: GTM Preview (Tag Assistant) on an intake page: tag must show "Not Fired"; confirm in Network.
- Server-side tagging: a first-party subdomain can collect and forward, hiding vendor hosts from the browser. https://developers.google.com/tag-platform/tag-manager/server-side/overview Look for unfamiliar first-party collect endpoints.

## 3. Consent Mode v2
Source: https://developers.google.com/tag-platform/security/guides/consent
- Parameters: `ad_storage`, `analytics_storage`, `ad_user_data`, `ad_personalization`; values `'granted'`/`'denied'`.
- `gtag('consent','default',{'ad_storage':'denied','ad_user_data':'denied','ad_personalization':'denied','analytics_storage':'denied'});` then `gtag('consent','update',{...})` on user choice.
- `wait_for_update` (ms) gives the CMP time to call update before measurement.
- `url_passthrough: true` may append `gclid`, `dclid`, `gclsrc`, `_gl`, `wbraid` to links.
- Audit: default must be set before the tag loads (Consent Initialization in GTM). Test with banner untouched: no ad requests should carry granted state. Consent Mode only signals; it does not by itself stop requests unless tags honor it (cookieless pings can still be sent: [UNVERIFIED]).

## 4. Google Ads conversion, remarketing, enhanced conversions
- Ad requests to `googleadservices.com` / `googlesyndication.com` (source in 1). Remarketing vs conversion distinction in the request path: [UNVERIFIED].
- Enhanced conversions: first-party data (email, name, home address, phone) normalized (trim, lowercase, E.164 phones) then hex SHA256 and sent to Google for matching to signed-in Google accounts. https://support.google.com/google-ads/answer/9888656
  Audit: if enabled on a help/intake form, hashed identity is leaving the site.

## 5. Meta Pixel and Conversions API
Sources: https://developers.facebook.com/docs/meta-pixel/implementation/conversion-tracking ; /advanced/advanced-matching ; /implementation/data-processing-options
- Base code: `fbq('init', PIXEL_ID); fbq('track','PageView');` script `connect.facebook.net/en_US/fbevents.js`; noscript fallback `<img src="https://www.facebook.com/tr?id=PIXEL_ID&ev=PageView&noscript=1">`.
- Proof of firing: request to `facebook.com/tr` (the documented noscript form shows `id=` and `ev=`; the JS-path request shape is [UNVERIFIED]). Meta's documented debug aid is the Meta Pixel Helper Chrome extension. https://developers.facebook.com/docs/meta-pixel/support
- Events: `fbq('track','Purchase',{currency:'USD',value:30.00})`; custom: `fbq('trackCustom','Name',{...})` (name max 50 chars).
- Advanced matching (manual in `fbq('init',ID,{em:..})` or automatic via Events Manager): fields `em, fn, ln, ph, external_id, ge, db, ct, st, zp, country`; pixel hashes SHA-256 automatically; appears as `ud[em]=` style params. Audit: look for `ud[` params on any page.
- Limited Data Use: `fbq('dataProcessingOptions', ['LDU'], 0, 0);` (0,0 = Meta geolocation); `['LDU'],1,1000` = California; `[]` disables. Doc says impact on performance possible. LDU is a US-state-privacy processing option, not a substitute for removing the pixel from sensitive pages.
- Conversions API: server-to-server sending to Meta, linked to a dataset ID, processed like pixel events. https://developers.facebook.com/docs/marketing-api/conversions-api/ Not visible in browser; ask the client/plugin list (CAPI plugins, server GTM). Endpoint path and event_id dedup: [UNVERIFIED].

## 6. TikTok, LinkedIn, HubSpot, Hotjar, Clarity
- TikTok: loader `analytics.tiktok.com/i18n/pixel/events.js`, `ttq.load('PIXEL_ID')`, `ttq.page()` (from secondary summaries, e.g. vendor help centre search results; official page returned 404): treat as [UNVERIFIED] until seen in a capture.
- LinkedIn Insight Tag: collects URL, referrer, IP, device characteristics, timestamp; LinkedIn says do not install on pages with sensitive data (financial accounts, medical info, health transactions). https://www.linkedin.com/help/lms/answer/a427660 Hosts `snap.licdn.com`, `px.ads.linkedin.com`: [UNVERIFIED].
- HubSpot: tracking script `js.hs-scripts.com/{hubId}.js`; cookies `hubspotutk`, `__hstc`, `__hssc`, `__hssrc` (from HubSpot community/search results; secondary). Opt-out: `var _hsq = window._hsq = window._hsq || []; _hsq.push(["doNotTrack"]);` sets a do-not-track cookie and stops page views, events, identification. https://developers.hubspot.com/docs/api-reference/latest/account/settings/tracking-code/do-not-track Forms embedded from HubSpot also identify visitors by cookie: [UNVERIFIED].
- Microsoft Clarity (session replay): code in `<head>`; verify by POSTs to `https://www.clarity.ms/collect`; masks sensitive content by default; cannot capture third-party iframes or canvas; cookies can be toggled, consent can be passed; not for sites targeting under-18s. https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-setup
- Hotjar: session replay; suppress via `data-hj-suppress` attribute/class (suppresses text and media inside element), password fields suppressed by default, content masking in Settings > Privacy (https://help.hotjar.com/... page returned 403; this is from search summaries, treat as secondary). `static.hotjar.com/c/hotjar-ID.js`, `hjid`: [UNVERIFIED].
- Audit rule: any session replay on intake/help forms is a high flag; confirm masking of all inputs, and that URLs hold no identifiers.

## 7. Cross-domain and donation platforms
- GA4 cross-domain: Admin > Data streams > Web stream > Configure tag settings > Configure your domains. Linker param `_gl` added to links/forms; verify by clicking the cross-domain link and checking `_gl` in the destination URL. https://support.google.com/analytics/answer/10071811
- Quirks to check on each donor flow (Donorbox, Givebutter, Classy, Stripe pages, etc.): is the form an iframe or redirect? Third-party iframes are not captured by Clarity; whether parent-page GA sees events inside a cross-origin iframe requires the platform to run its own tag or send postMessage: [UNVERIFIED]. Check which tags the platform's own domain loads (separate capture on its URL), whether `_gl` survives, and whether referrer/page title on the thank-you URL carries donor name or amount.
- Conversion events should fire on a confirmed thank-you state, not the button click, to avoid inflating counts.

## 8. What the platforms' own policies say (quoted, not legal advice)
- Meta Business Tools Terms s1.h: you represent you will not share Business Tool Data that "includes or is based on, directly or otherwise, health information, financial information, consumer report information, or other categories of sensitive information (including any information defined as sensitive under applicable laws, regulations and applicable industry guidelines)". Also: names of events, conversions and custom audiences "must not reflect, imply or be based on any category of information" in 1.h. https://www.facebook.com/legal/technology_terms
  Meta (via secondary summary) says advertisers are responsible for what they send and its filters are not a guarantee: [UNVERIFIED primary].
- Google Ads personalized advertising: sensitive interest categories bar advertiser-curated audiences (remarketing/customer lists/custom segments) ; predefined Google audiences remain allowed. https://support.google.com/adspolicy/answer/143465 "Marginalized groups" is a sensitive category defined as "using someone's membership in a marginalized or vulnerable social group, such as social castes, immigrants or refugees." https://support.google.com/adspolicy/answer/16701957 Health is also listed as sensitive.
- Practical read for orgs serving sensitive audiences (health, legal, immigration, etc.): remarketing or Meta event data from help/intake pages can indicate immigrant status; the platforms' own policies above point the same way. Recommend: no ad pixels, remarketing, enhanced conversions, advanced matching or session replay on help/intake/legal-aid pages; GTM allow-list triggers; consent defaults denied; cookieless aggregate analytics instead. Legal conclusions go to the client's counsel.

## 9. Report row
Page URL | tags in source | requests proving firing | consent state at load | identifiers in URL/title | verdict.
