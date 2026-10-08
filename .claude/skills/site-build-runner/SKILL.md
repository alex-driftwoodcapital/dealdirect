---
name: "site-build-runner"
description: "Run site changes unsupervised and safely: scope, staging first, backups, verify, stop conditions, one-message report. Wraps etch-page-editor, etch-builder, acss-expert."
---

# Site build runner
One job: the protocol for working without the owner watching. It does not edit by itself; it sequences the editor/builder/styler and enforces limits.

## Preconditions
A session that can reach the server (SSH + WP-CLI) with credentials the owner provided locally. The brief states one goal and a done condition.

## Loop (per piece)
1. Re-read live values; timestamped backup. If a value changed since you read it, STOP and re-read.
2. Check how (`etch-expert`) and choose styles (`acss-expert`), then edit (`etch-page-editor`) or build (`etch-builder`) on staging.
3. Purge cache; verify in own headless Chromium at 375 and 1440 (text, colors, widths, no overflow). Leave interactive pieces untouched unless in the brief.
4. Read-only audits after, as relevant: `seo-geo-auditor`, `security-auditor`, `tracking-auditor`, `client-test-group`.
5. Next piece, until the done condition is met.

## Stop and ask when
A conflict with a builder save, a failed verify you cannot fix in one round, anything outside the brief, or any irreversible step (go live, delete, DNS, send): needs the owner's explicit approval.

## Report
One message: what changed, where, widths checked, what is left. Never claim an absence or a fix you did not verify.
