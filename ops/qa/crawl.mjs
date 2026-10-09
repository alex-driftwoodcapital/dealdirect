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
  '/offering/driftwood-hotel-income-i-dst/': [302, 'https://driftwoodcapital.com/1031-exchanges-and-dsts/'],
  '/offering/driftwood-tax-advantage-strategy-i/': [302, 'https://driftwoodcapital.com/bonus-depreciation/'],
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
    const ids = [...new Set([...body.matchAll(/\sid=["']([^"']+)["']/g)].map((m) => m[1]))];
    return { status: r.status, loc, title: decode(pick(/<title[^>]*>([^<]*)/i)), h1: decode(pick(/<h1[^>]*>([\s\S]*?)<\/h1>/i).replace(/<[^>]+>/g, '')), canonical, ids };
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

// ids the builders add on their own (not content anchors)
const NOISE = /^(wp-|etch-|bricks|brx|brxe-|gtm|__|query-|tns|ac-|rank-math|ez-toc)/;
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
  const lost = l.status === 200 && s.status === 200 ? l.ids.filter((id) => !NOISE.test(id) && !s.ids.includes(id)) : [];
  if (lost.length) problems.push(`anchor ids missing on staging: ${lost.join(' ')}`);
  const notes = [];
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
