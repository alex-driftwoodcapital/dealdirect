// ROLE-TEMPLATE
// Crawl diff, live vs staging (handoff/docs/permalinks.md "Before go-live"): every URL in the live sitemaps and REST
// listings, fetched from both sites (GETs only; live is never written to). Compares status, <title>, canonical path,
// <h1> and anchor ids. A changed status counts only when it is not one of the agreed old-URL decisions (EXPECTED).
// Writes qa-out/crawl.md + crawl.json; exits 1 on an unexpected status or a lost anchor id.
// env: QA_BASE_URL (staging), QA_HTTP_USER / QA_HTTP_PASSWORD (staging basic auth), LIVE_URL (default the live site).
import fs from 'fs';

const LIVE = (process.env.LIVE_URL || 'https://driftwooddealdirect.com').replace(/\/$/, '');
const STAGING = (process.env.QA_BASE_URL || '').replace(/\/$/, '');
if (!STAGING) { console.error('QA_BASE_URL is required'); process.exit(2); }
const AUTH = process.env.QA_HTTP_USER ? 'Basic ' + Buffer.from(`${process.env.QA_HTTP_USER}:${process.env.QA_HTTP_PASSWORD}`).toString('base64') : '';
const OUT = 'qa-out';

// Decisions recorded in CLAUDE.md (dealdirect-core includes/retired.php): path -> [status, Location path]
const EXPECTED = {
  '/offering/riverside-wharf/': [301, '/offering/riverside-wharf-qoz/'],
  '/offering/riverside-wharf-eb-5/': [301, '/eb-5-investments/'],
  '/offering/driftwood-tax-advantage-strategy-i/': [302, 'https://dtas1.driftwoodcapital.com/'],
  '/registration-success/': [410], '/forgot-password/': [410], '/reset-password/': [410], '/admin-login/': [410],
};
// URLs the rebuild adds (not on live yet)
const EXTRA = ['/offering/riverside-wharf-qoz/'];

async function get(base, path, auth) {
  try {
    const r = await fetch(base + path, { redirect: 'manual', headers: { ...(auth ? { Authorization: auth } : {}), 'User-Agent': 'DealDirect crawl diff (read-only)' } });
    const body = r.status === 200 ? await r.text() : '';
    const loc = (r.headers.get('location') || '').replace(base, '');
    const pick = (re) => (body.match(re) || [, ''])[1].replace(/\s+/g, ' ').trim();
    const canonical = pick(/<link[^>]+rel=["']canonical["'][^>]*href=["']([^"']+)/i).replace(/^https?:\/\/[^/]+/, '');
    // content anchors only: ids on <link>/<script>/<style>/<meta> are the theme's assets, not anchors
    const ids = [...new Set([...body.matchAll(/<(\w+)\b[^>]*\sid=["']([^"']+)["']/g)]
      .filter((m) => !/^(link|script|style|meta|noscript|iframe)$/i.test(m[1])).map((m) => m[2]))];
    const linked = [...new Set([...body.matchAll(/href=["'][^"'#]*#([A-Za-z0-9_-]+)["']/g)].map((m) => m[1]))];
    return { status: r.status, loc, title: decode(pick(/<title[^>]*>([^<]*)/i)), h1: decode(pick(/<h1[^>]*>([\s\S]*?)<\/h1>/i).replace(/<[^>]+>/g, '')), canonical, ids, linked };
  } catch (e) {
    return { status: 0, error: String(e).slice(0, 120), ids: [] };
  }
}
const decode = (s) => s.replace(/&#8211;/g, '–').replace(/&#8217;/g, '’').replace(/&amp;/g, '&').replace(/&#039;|&#39;/g, "'").replace(/&quot;/g, '"');

async function liveUrls() {
  const paths = new Set(['/']);
  const add = (u) => { try { const p = new URL(u).pathname; paths.add(p.endsWith('/') ? p : p + '/'); } catch {} };
  const index = await (await fetch(LIVE + '/sitemap_index.xml')).text().catch(() => '');
  for (const sm of [...index.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1])) {
    const xml = await (await fetch(sm)).text().catch(() => '');
    [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].forEach((m) => add(m[1]));
  }
  for (const type of ['pages', 'offering']) {
    const list = await (await fetch(`${LIVE}/wp-json/wp/v2/${type}?per_page=100&_fields=link,status`)).json().catch(() => []);
    if (Array.isArray(list)) list.forEach((p) => add(p.link));
  }
  return [...paths].sort();
}

// Anchors that must survive (CLAUDE.md rule 3): the frozen list in handoff/docs/permalinks.md, plus every id the live page
// links to (href="#id": its sub-nav, "skip to"), plus the EB-5 pages' live section ids. Other live ids are the old
// builder's and form plugin's (field ids, wrappers) and are not compared.
const FROZEN = { offering: ['metrics', 'overview', 'webinar', 'partners', 'offering', 'structure', 'assets', 'market', 'rationale', 'legal'],
  eb5: ['legal', 'hero', 'intro', 'investment-process', 'driftwood-advantage', 'track-record', 'faq'] };
const kindOf = (path) => path.startsWith('/offering/') ? 'offering' : /eb-5|inversiones|investimentos/.test(path) ? 'eb5' : '';
const NOISE = /^(brx-|bricks|wp-|gtm)/;
// Live anchors the approved design removed with their sections (reported for a decision, not failed)
const DROPPED = {
  '/offering/riverside-wharf-preferred-equity/': ['structure', 'assets', 'rationale'],  // PE design: no structure/assets/rationale sections
};
const rows = [], fails = [];
const urls = [...new Set([...(await liveUrls()), ...Object.keys(EXPECTED), ...EXTRA])];
for (const path of urls) {
  const [l, s] = [await get(LIVE, path, ''), await get(STAGING, path, AUTH)];
  const want = EXPECTED[path];
  const problems = [];
  if (want) {
    if (s.status !== want[0] || (want[1] && s.loc !== want[1])) problems.push(`staging ${s.status}${s.loc ? ' → ' + s.loc : ''}, decided ${want[0]}${want[1] ? ' → ' + want[1] : ''}`);
  } else if (EXTRA.includes(path)) {
    if (s.status !== 200) problems.push(`new page answers ${s.status}`);
  } else if (l.status !== s.status) {
    problems.push(`status live ${l.status} / staging ${s.status}`);
  }
  const must = new Set([...(FROZEN[kindOf(path)] || []).filter((id) => l.ids.includes(id)), ...(l.linked || []).filter((id) => !NOISE.test(id))]);
  const missing = l.status === 200 && s.status === 200 ? [...must].filter((id) => !s.ids.includes(id)) : [];
  const dropped = missing.filter((id) => (DROPPED[path] || []).includes(id));
  const lost = missing.filter((id) => !dropped.includes(id));
  if (lost.length) problems.push(`anchor ids missing on staging: ${lost.join(' ')}`);
  const notes = [];
  if (dropped.length) notes.push(`anchors dropped by the design (decision pending): #${dropped.join(' #')}`);
  if (l.status === 200 && s.status === 200) {
    if (l.title !== s.title) notes.push(`title “${l.title}” → “${s.title}”`);
    if (l.canonical !== s.canonical) notes.push(`canonical ${l.canonical || '–'} → ${s.canonical || '–'}`);
    if (l.h1 !== s.h1) notes.push(`h1 “${l.h1.slice(0, 60)}” → “${s.h1.slice(0, 60)}”`);
  }
  problems.forEach((p) => fails.push(`${path}: ${p}`));
  rows.push({ path, live: l.status, staging: s.status, loc: s.loc, problems, notes });
}

fs.mkdirSync(OUT, { recursive: true });
fs.writeFileSync(`${OUT}/crawl.json`, JSON.stringify(rows, null, 1));
const md = [
  `# Crawl diff, live vs staging — ${new Date().toISOString().slice(0, 16).replace('T', ' ')} UTC`, '',
  `${urls.length} URLs (live sitemaps + REST listings + decided old URLs + new pages).`, '',
  fails.length ? `**${fails.length} problem(s)**` : '**No unexpected status changes or lost anchors**', '',
  ...fails.map((f) => `- ${f}`), '',
  '| URL | Live | Staging | Problems | Differences (for review) |', '|---|---|---|---|---|',
  ...rows.map((r) => `| \`${r.path}\` | ${r.live} | ${r.staging}${r.loc ? ' → `' + r.loc + '`' : ''} | ${r.problems.join('; ') || 'ok'} | ${r.notes.join('; ').replace(/\|/g, '\\|') || '–'} |`),
];
fs.writeFileSync(`${OUT}/crawl.md`, md.join('\n') + '\n');
console.log(md.slice(0, 6 + fails.length).join('\n'));
process.exit(fails.length ? 1 : 0);
