// ROLE-TEMPLATE
// Compliance report from the evidence register (handoff/design/evidence-register/claims.js): every claim that still
// blocks go-live (CLAUDE.md rule 10: each open `gap` / `check` must clear first), grouped by page, with what closes it.
// Read-only. usage: node ops/compliance/report.mjs > docs/compliance-report.md
import fs from 'fs';
import path from 'path';
import vm from 'vm';

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..', '..');
const src = fs.readFileSync(path.join(root, 'handoff/design/evidence-register/claims.js'), 'utf8');
const ctx = { window: {} };
vm.runInNewContext(src, ctx);
const claims = ctx.window.EVIDENCE_REGISTER.claims;

const WHAT = {
  gap: 'needs a source document (PPM, brochure, model, third-party report) and its locator',
  check: 'needs a compliance decision on the wording or figure shown',
  internal: 'a live typo carried verbatim (CLAUDE.md rule 1); compliance decides whether to fix',
  traced: 'traced to a source; nothing to do',
};
const count = (s) => claims.filter((c) => c.status === s).length;
const open = claims.filter((c) => c.status === 'gap' || c.status === 'check');
const esc = (s) => String(s ?? '').replace(/\|/g, '\\|').replace(/\n/g, ' ');
const pages = [...new Set(claims.map((c) => c.slide.split(' · ')[0]))];

const out = [
  '# Compliance report: evidence register',
  '',
  `Generated from \`handoff/design/evidence-register/claims.js\` by \`ops/compliance/report.mjs\` (${new Date().toISOString().slice(0, 10)}).`,
  'Every figure on the rebuilt pages was lifted verbatim from the live site, which is not a source document, so a',
  'claim is only closed once compliance traces it to an offering document or accepts it in writing.',
  '',
  `**${open.length} open items block go-live** (CLAUDE.md rule 10): ${count('gap')} \`gap\` and ${count('check')} \`check\`.`,
  `Also: ${count('internal')} \`internal\` (live typos carried verbatim), ${count('traced')} \`traced\`.`,
  '',
  '| Status | Meaning |', '|---|---|',
  ...Object.entries(WHAT).map(([k, v]) => `| \`${k}\` | ${v} |`),
  '',
  '## Decisions already applied in the build',
  '- "shovel-ready" removed everywhere, every language (Riverside Wharf is under construction; CLAUDE.md rule 2).',
  '- Platform figures (30+ years, 78 hotels, 15,162 keys, ~$3.5B, ±6,000 employees, as of Sept 1, 2026) come from the platform-stats options page, not typed into pages (rule 8).',
  '- Riverside Wharf has three vehicles: Preferred Equity, Common Equity QOZ, EB-5 (2026-10-09). The old /offering/riverside-wharf/ 301s to the QOZ page; /offering/riverside-wharf-eb-5/ 301s to /eb-5-investments/.',
  '- Legal and footnote text is never below 12px or 4.5:1 contrast (rule 6).',
  '',
];
for (const page of pages) {
  const rows = claims.filter((c) => c.slide.split(' · ')[0] === page && c.status !== 'traced');
  if (!rows.length) continue;
  out.push(`## ${page}`, '', '| Status | Section | Claim | Shown on the page | Note / what closes it |', '|---|---|---|---|---|');
  for (const c of rows) {
    out.push(`| \`${c.status}\` | ${esc(c.slide.split(' · ').slice(1).join(' · ') || '–')} | ${esc(c.claim)} | ${esc(c.value)} | ${esc(c.note) || esc(WHAT[c.status])} |`);
  }
  out.push('');
}
out.push('## How to close an item',
  '- Drop the source document into `handoff/design/evidence-register/evidence/` (or link it), fill the claim\'s `file` and `locator`, and set its status to `traced`.',
  '- For a `check`, record compliance\'s decision in the claim\'s `note` and set the status to `traced` (accepted as is) or change the figure in the design file first (the copy gate then requires the page to match).',
  '- Re-run `node ops/compliance/report.mjs > docs/compliance-report.md`.', '');
process.stdout.write(out.join('\n'));
