# WordPress read-only external security audit (reference)

Fetched 2026-10-02. Items tagged [SECONDARY] come from search summaries or non-primary pages; [UNVERIFIED] means not confirmed in a fetched page. Not legal advice.

## 0. Scope rules (hard limits)
- Audit only the owner's site or an approved client's site, with written approval on file (domain list + dates).
- Passive, read-only requests: GET/HEAD of public URLs, a browser, `curl -sI`, DNS lookups. One request per path, no loops.
- NOT allowed: exploitation, brute force or password guessing (including wp-login, xmlrpc.php system.multicall), credential stuffing, fuzzing or high-volume crawling, DoS, scanning anyone else's hosts or shared-host neighbours, submitting forms with payloads, downloading and keeping exposed secrets/dumps.
- If a secret or personal data is exposed: stop, record URL + HTTP status + file size only (no contents), notify the owner privately, recommend rotation.

## 1. HTTP security headers
Check with `curl -sI https://SITE/` and on an inner page. Prefer `always`-style delivery on all responses (incl. errors).
| Header | Good looks like | Source |
|---|---|---|
| Strict-Transport-Security | `max-age=63072000; includeSubDomains; preload` (OWASP). Preload requires max-age >= 31536000 and includeSubDomains. Only honored over HTTPS. Do not add `preload` until every subdomain is HTTPS. | https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html ; https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Strict-Transport-Security |
| Content-Security-Policy | Present. MDN strict baseline: `script-src 'nonce-{RANDOM}'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'`. Roll out first as `Content-Security-Policy-Report-Only`. Nonce must be unique per response. WordPress/Etch plus third-party scripts often need a tuned policy; flag absence as Medium, not Critical. | https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP |
| X-Frame-Options | `DENY` or `SAMEORIGIN` (OWASP lists `DENY`). `ALLOW-FROM` is obsolete. CSP `frame-ancestors` supersedes it; if the site must be embedded, use frame-ancestors with an allow-list. | https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Frame-Options |
| X-Content-Type-Options | `nosniff` (only valid value). | https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Content-Type-Options |
| Referrer-Policy | `strict-origin-when-cross-origin` (browser default since Nov 2020; OWASP value). `no-referrer` for max privacy. `unsafe-url` is a flag. For intake/help pages prefer `no-referrer` or `same-origin` so URLs do not leak to third parties. | https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Referrer-Policy |
| Permissions-Policy | e.g. `geolocation=(), camera=(), microphone=()` (OWASP). Syntax `feature=(self "https://x")`; `()` disables. | https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Permissions-Policy |
| COOP / COEP / CORP | OWASP lists `same-origin` / `require-corp` / `same-site`; COEP `require-corp` breaks third-party embeds, so Low priority here. | OWASP cheat sheet above |
| Information leaks | Remove or neutralize `Server` version, `X-Powered-By` (PHP version). | OWASP cheat sheet above |
Also note `Set-Cookie`, `Cache-Control` on logged-in/intake pages [UNVERIFIED value recommendation].

## 2. TLS, redirects, mixed content
- `http://SITE` returns 301 to `https://SITE` in one hop; `www` and apex both resolve to one canonical HTTPS URL; no redirect chains over 2 hops.
- Certificate valid, not near expiry, hostname matches (browser padlock or `curl -vI`). Prefer a TLS lab check of public hostnames you own.
- Mixed content: load pages with DevTools Console open; flag any `http://` subresource (images, scripts, forms action). Check WordPress Settings > General URLs are https.
- HSTS served only on HTTPS responses; confirm header present after the redirect.

## 3. Exposed files and endpoints (one GET/HEAD each; record status only)
Expected safe result: 403/404, not 200 with content.
- `/wp-config.php` should never display source (200 with PHP text is critical). Backups: `/wp-config.php.bak`, `.old`, `.save`, `.orig`, `.swp`, `~`, `/wp-config.php.zip` [common backup patterns; WSTG page for backups returned only a redirect notice, so list is [SECONDARY]]. WP hardening doc: restrict wp-config via `<Files "wp-config.php"> Require all denied </Files>`, permissions 400/440, may sit one directory above the install. https://developer.wordpress.org/advanced-administration/security/hardening/
- `/.git/HEAD`, `/.git/config`, `/.env`, `/.htaccess`, `/.DS_Store`, `/backup.zip`, `/db.sql`, `/*.sql` at web root: any 200 is a finding.
- `/wp-content/debug.log`: default location when `WP_DEBUG_LOG` is true; WordPress docs say debug tools are not recommended on live sites; set `WP_DEBUG_DISPLAY` false. https://developer.wordpress.org/advanced-administration/debug/debug-wordpress/ Also check error text printed on pages (display on).
- `/readme.html`, `/license.txt`, `/wp-includes/version.php` blocked: readme.html reveals the core version [SECONDARY]; low severity, remove after updates.
- `/xmlrpc.php`: a GET commonly returns "XML-RPC server accepts POST requests only" if enabled [SECONDARY]. Report enabled/disabled only; never POST. Disable if unused (SiteGround Security plugin can disable it; see 9).
- `/wp-json/` index lists namespaces/routes (public by design). `/wp-json/wp/v2/users`: listing users is a known enumeration vector, returning ID, name, slug for authors with public posts [SECONDARY: search summaries; WordPress's own docs page (https://developer.wordpress.org/rest-api/reference/users/) documents the endpoint but not its auth behavior]. Also `/?author=1` redirecting to `/author/username/` [UNVERIFIED]. Do not iterate IDs beyond a single sample request.
- Directory listing: GET `/wp-content/uploads/`, `/wp-content/plugins/`, `/wp-content/themes/`; an "Index of /" page is a finding (fix: `Options -Indexes` in .htaccess [SECONDARY]).
- `/wp-login.php` and `/wp-admin/`: expected to exist and redirect; check HTTPS only, presence of rate limiting/2FA via policy or plugin list, not by trying credentials. Hardening doc suggests BasicAuth on wp-admin and HTTPS-only admin.
- `DISALLOW_FILE_EDIT` true prevents dashboard file editing (hardening doc). Verify via owner's wp-admin, not externally.
- `robots.txt` and `sitemap.xml` may disclose hidden paths: read them, do not crawl what they list beyond the owner's scope.

## 4. Plugin, theme and version exposure
- Read the HTML source: `<meta name="generator" content="WordPress x.y">`, `?ver=` query strings on assets, `/wp-content/plugins/NAME/` and `/wp-content/themes/NAME/` paths. Passive list only.
- Compare found versions with the plugin's changelog and a vulnerability database (look up by slug/version; do not test). Flag outdated, abandoned (not updated in over 2 years), nulled/pirated, or duplicate-function plugins. Ask the owner for authoritative list via wp-admin or WP-CLI (`wp plugin list --status=active --format=table`, `wp core version`, `wp core verify-checksums`).
- Etch/ACSS-specific: confirm the site is on a supported WordPress and PHP version [UNVERIFIED target versions; check wordpress.org/about/requirements].

## 5. Forms, spam, CSRF, rate limits (observe only)
- Form `action` is HTTPS, same origin or a named processor (list third-party processors).
- Spam control present: honeypot field, CAPTCHA/Turnstile/hCaptcha, or server throttling; do not submit floods to test. One manual test submission with the owner's consent and a clearly marked test message.
- CSRF: forms in WordPress core/plugins carry a nonce (`_wpnonce` or plugin equivalent) hidden field [SECONDARY]; cookies with `SameSite` Lax/Strict add defense (see 6).
- Rate limiting: check policy docs or headers (`429`, `Retry-After`) in normal use; do not provoke.
- Intake forms: no PII in URL query strings, no PII in page titles, no email notifications carrying sensitive details unencrypted, form data stored where? (ask owner), retention limits.

## 6. Cookie flags
MDN guidance (https://developer.mozilla.org/en-US/docs/Web/Security/Practical_implementation_guides/Cookies): `Secure` always; `HttpOnly` for session/sensitive; `SameSite=Strict` or `Lax`; `__Host-` prefix (Path=/, no Domain) or `__Secure-`; short Max-Age; narrow Path/Domain. Example `Set-Cookie: __Host-ID=...; Max-Age=2592000; Path=/; Secure; HttpOnly; SameSite=Strict`.
Audit: list cookies set to an anonymous visitor (DevTools > Application). WordPress login cookies appear only after login; the owner's logged-in test account can check them. Flag any marketing cookie set before consent on sensitive pages.

## 7. Third-party scripts and SRI
- Inventory every third-party host in Network tab; justify each, remove the rest. Combine with tracking-auditor reference.
- SRI: `<script src=".." integrity="sha384-..." crossorigin="anonymous">`; sha256/384/512 allowed; `crossorigin="anonymous"` mandatory; SRI does not protect dynamically injected scripts (tag managers, vendor loaders). https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Subresource_Integrity
- Self-host static libraries (fonts, jQuery) where practical; pin versions; avoid `@latest` CDN URLs.
- A tag manager can change code without a deploy: restrict who can publish, and review versions.

## 8. Email authentication (DNS lookups only)
- SPF: TXT at the domain starting `v=spf1`, ends with `~all` or `-all`, one record only, under 10 DNS lookups [lookup limit: UNVERIFIED in fetched page]. Include only senders actually used (SiteGround mail, Mailchimp, HubSpot, etc.).
- DKIM: TXT at `selector._domainkey.DOMAIN` for each sender (selector from a sent message header).
- DMARC (https://knowledge.workspace.google.com/admin/security/set-up-dmarc): TXT host `_dmarc.DOMAIN`, e.g. `v=DMARC1; p=none; rua=mailto:postmaster@DOMAIN; pct=100; adkim=s; aspf=s`. Set up SPF and DKIM first. Rollout none, then quarantine, then reject, raising `pct` as passes. Do not point `rua` at a personal inbox (high volume).
- Check: `dig +short TXT DOMAIN`, `dig +short TXT _dmarc.DOMAIN`.

## 9. SiteGround-specific hardening (recommendations to the owner)
- HTTPS: Site Tools > Security > HTTPS Enforce, toggle On per domain/subdomain. For WordPress SiteGround says best done at application level via the Speed Optimizer plugin > Environment Options > HTTPS Enforce. The KB does not address HSTS, so add the header separately (hosting config or plugin) [UNVERIFIED how]. https://www.siteground.com/kb/how-do-i-enforce-https ; summary via search [SECONDARY]
- SiteGround Security (Security Optimizer) plugin, per SiteGround blog summaries [SECONDARY, official page fetch returned empty]: Login Security (2FA for admin/editor users, limit login attempts per IP, change login URL, block "admin" username), XML-RPC disabled by default with option to disable, other hardening toggles. Confirm exact toggle names in wp-admin before reporting.
- Other: keep PHP at a supported version in Site Tools; automatic WP updates; SiteGround backups (verify a restore point exists); least-privilege WP roles; unique admin usernames; remove unused plugins/themes.
- A past critical authentication bypass was patched in the SiteGround Security plugin (Wordfence, 2022): https://www.wordfence.com/blog/2022/04/critical-authentication-bypass-vulnerability-patched-in-siteground-security-plugin/ so require current plugin version.

## 10. Severity and report
Critical: secrets, DB dumps, `.git`, wp-config source exposed. High: no HTTPS redirect, outdated core/plugin with known CVE, debug.log public, directory listing of uploads with sensitive files. Medium: missing CSP/HSTS, xmlrpc enabled, users enumerable, no DMARC. Low: readme.html, version strings, missing Permissions-Policy.
Row: Check | URL tested | HTTP status/header seen | Expected | Severity | Owner action. Include date, tester, approval reference.
