# ACSS setup, breakpoints, Pro Mode
Source (verified from docs 2026-10-02): https://docs.automaticcss.com/setup/website-width-breakpoints , https://docs.automaticcss.com/setup/how-to-install-acss (both 4.x); Pro Mode: https://docs.automaticcss.com/3.0/setup/pro-mode (3.x only)
NOTE: /setup/pro-mode does not exist in the 4.x docs (404); Pro Mode content is from the 3.0 tree and unverified for 4.x.


> **4.0.1 check (2026-10-07, see staging-4.0.1-facts.md):** ACSS 4 is breakpoint-free (official What's New: "Removed Breakpoints"). The staging build has no breakpoint settings or `@media` presets; only `vp-min` 360 and `vp-max` 1112 (content width 69.5rem). The "Breakpoints", "Bricks mapping" and "Pro Mode" sections below describe 3.x-era behavior still left on the docs page; do not apply them to Etch builds. Etch needs no ACSS setup (docs /setup/builder-configuration/etch: "zero configuration"). Width lives under Layout > Website Dimensions (/dimension/content-width), not a Viewport tab.

## Install (4.x)
- WordPress: Plugins > Add New > Upload plugin zip > Activate. New "Automatic.css" admin sidebar area appears.
- Dashboard > License: enter key. Account may show two keys: use the one named "–Automatic.css" (usually second); not the bundle key or plan-named key.
- Framework "requires practically no setup to function".

## Website width (4.x)
- Docs page says Dashboard > Viewport tab > "Website Width" input (stale: 4.x puts content width and minimum width under Layout > Website Dimensions). Must equal the page builder's website/container width (needed for responsive typography, responsive spacing, auto grids).

