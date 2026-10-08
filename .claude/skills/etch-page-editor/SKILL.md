---
name: "etch-page-editor"
description: "Edit EXISTING pages, copy, classes, stylesheet and scripts on Driftwood DealDirect's Etch site (Cloudways) over SSH + WP-CLI (no Etch tab), build NEW pages natively (with pilot gate), and run site changes unsupervised. Staging first."
---

# Etch page editor
Load `etch-expert` first for syntax and `acss-expert` for styling.
One job: safe changes to the Etch site. Existing pages: this file. NEW pages or components: `formats/build.md` (native Etch build with a one-page pilot gate). Unsupervised runs: section below. Styling choices: `acss-expert`.

Use for page, copy, style or script changes on the Etch site. Alex never opens or foregrounds the Etch builder.

## Where it runs
Any session that has the SSH key reaches the server: a cloud session with the `ETCH_SSH_KEY` and `ETCH_SSH_KNOWN_HOSTS` secrets (run `scripts/ssh-setup.sh --check` first; the scripts also call it on first use), or a local machine with `~/.ssh/dealdirect_staging`. If the check fails (no secret, host not allowed by the environment's network policy), stop and report; draft only. Site facts (hosts, URLs, IDs, pinned versions, brand rules): `site-profile.md`. 
## How Etch stores things
Pages: block markup in `post_content`. Classes: `etch_styles`. Main stylesheet: `etch_global_stylesheets`. Loops: `etch_loops`. Element scripts: base64. Known-good markup to copy: `etch-expert/reference/fixtures/`.

## Edit method
1. Re-read the current value over SSH/WP-CLI. Never edit from memory or an old copy.
2. Timestamped backup first: `scripts/snapshot.sh <post_id>...` (also snapshots the Etch options).
3. Edit with a small script; merge, don't overwrite. If it changed since you read it, STOP and re-read.
4. Write back, then purge (`PURGE_CMD` in the profile). `scripts/diff.sh <snapshot>` shows what changed (whitespace ignored; flags a builder re-save); `RESTORE_YES=1 scripts/restore.sh <snapshot> post|option <id|name>` rolls back (dry run by default; refuses protected IDs).
5. Verify in your own headless Chromium (separate profile, never Alex's windows) at 375px and 1440px: text, colors, widths, no horizontal overflow.

## Catch
Saving the same page in the builder overwrites direct edits. Close or reload it before any save (the gate above is the one deliberate exception, and you do it on staging).

## Go-live
Staging first. Live needs Alex's own typed words (a coordinator relay with his message attached counts). Publish piece by piece, check live, report.

## Why not the connector
The Etch Connector needs a visible builder tab; Chrome throttles background tabs and it stalls.

## Rules while editing
DealDirect brand and copy rules live in `site-profile.md`.

## Motion
Page needs animation or effects: follow `art-director` (`reference/site-motion.md`: tool choice, limits) before editing.

## Report
One short message: what changed, where, widths checked, what's left for Alex.

## Unsupervised runs (protocol)
Used when Alex is not watching. Any session where `scripts/ssh-setup.sh --check` passes. The brief states one goal and a done condition.
- Run it with `scripts/run-brief.py brief.json` (dry run first; `--yes` to write; staging profile only). Brief shape and stop rules are in the script header; examples in `run-examples/`. It reads a baseline of every page named in the brief BEFORE writing, then per piece calls `edit-run.sh` (snapshot, lint with ACSS names, write, purge, diff, verify) and writes `report.md` with a rollback command per piece.
- It stops, skips the remaining pieces and reports on: lint errors, a page changed since the baseline read (builder save or another edit), protected or out-of-brief page, failed verify. Piece types for delete / publish / go-live / DNS / send do not exist: those need Alex's own typed words in the thread (a coordinator relay with his message attached counts).
- Around it: check how (`etch-expert`, cite docs.etchwp.com), choose styles (`acss-expert`), read-only audits after as relevant (`site-auditor`, `security-auditor`, `tracking-auditor`, `seo-geo-auditor`). Interactive pieces (leaks game, quiz, demos) stay untouched beyond approved copy fixes. After publishing (Alex's word), run `scripts/verify/verify.mjs` at 375/1440.
- Report in one message: what changed, where, widths checked, what is left for Alex. Never claim an absence or a fix you did not verify.
