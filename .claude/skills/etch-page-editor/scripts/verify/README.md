# verify: 375/1440 check

Setup once: `cd scripts/verify && npm install && PLAYWRIGHT_BROWSERS_PATH=$HOME/.cache/etch-verify-browsers npx playwright-core install chromium-headless-shell`
Run: `node verify.mjs <outdir> <url>...` (exit 1 if any page is non-200, overflows horizontally, or logs a console error).
Per URL and width (375, 1440): status, horizontal overflow with offending elements, `h1` count, images without `alt`, console errors, failed requests, full-page screenshot. Writes `report.md`, `report.json`, PNGs to `<outdir>`.
Own headless Chromium only (never Alex's windows). Analytics/GTM/Facebook requests are blocked so staging checks never send hits. Reduced motion is on. Needs the staging page to be publicly reachable (the SiteGround captcha blocks cloud IPs; run from the Mac).
Sample report from staging Home, Work, Pricing: `sample/report-2026-10-07.md` (all 200, no overflow, 0 console errors).
