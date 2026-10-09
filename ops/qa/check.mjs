// ROLE-TEMPLATE — staging QA in a real browser, run by .github/workflows/qa.yml (read-only: GETs only).
// Every page at 375 / 768 / 1440: status, horizontal overflow, console errors, failed requests, the self-hosted
// font and ACSS palette actually in use, <html lang>, title, robots, canonical, hreflang; full-page screenshots.
// Plus the URL decisions (301s, 410s, 404). Writes qa-out/report.md, results.json and screenshots; exits 1 on a failure.
import { chromium, request } from 'playwright';
import fs from 'fs';

const BASE = (process.env.QA_BASE_URL || '').replace(/\/$/, '');
const auth = { username: process.env.QA_HTTP_USER || '', password: process.env.QA_HTTP_PASSWORD || '' };
if (!BASE) { console.error('QA_BASE_URL is not set'); process.exit(2); }
const OUT = 'qa-out';
fs.mkdirSync(`${OUT}/shots`, { recursive: true });

const PAGES = [
  ['home', '/', 'en-US'],
  ['eb5', '/eb-5-investments/', 'en'],
  ['eb5-es', '/inversiones-eb-5/', 'es'],
  ['eb5-pt', '/investimentos-eb-5/', 'pt-BR'],
  ['eb5-new', '/new-eb-5-page/', 'en-US'],
  ['preferred-equity', '/offering/riverside-wharf-preferred-equity/', 'en-US'],
  ['qoz', '/offering/riverside-wharf-qoz/', 'en-US'],
  ['dst', '/offering/driftwood-hotel-income-i-dst/', 'en-US'],
  ['not-found', '/qa-no-such-page/', 'en-US', 404],  // name, path, lang, status (200 unless given)
];
const URLS = [  // path, expected status, expected Location (path) for redirects
  ['/offering/riverside-wharf/', 301, '/offering/riverside-wharf-qoz/'],
  ['/offering/riverside-wharf-eb-5/', 301, '/eb-5-investments/'],
  ['/admin-login/', 410], ['/forgot-password/', 410], ['/reset-password/', 410], ['/registration-success/', 410],
  ['/qa-no-such-page/', 404],
  // card-only offerings (site/lib/card_offering.py): 302 to their card link until they have a page (the DST has its
  // page since #38; DTAS goes to its own site for now, Alex 2026-10-09)
  ['/offering/driftwood-tax-advantage-strategy-i/', 302, 'https://dtas1.driftwoodcapital.com/'],
];
const WIDTHS = [375, 768, 1440];
const fails = [];
const rows = [];

const api = await request.newContext({ httpCredentials: auth, maxRedirects: 0 });
const urlRows = [];
for (const [path, want, to] of URLS) {
  const r = await api.get(BASE + path, { maxRedirects: 0 });
  const loc = (r.headers()['location'] || '').replace(BASE, '');
  // 404 and 410 must show the DealDirect not-found template (site/pages/template_404.py), not a bare theme page
  const body = want >= 400 ? await r.text() : '';
  const tpl = want < 400 || body.includes('not-found__title');
  const ok = r.status() === want && (!to || loc === to) && tpl;
  if (!ok) fails.push(`${path}: got ${r.status()}${loc ? ' -> ' + loc : ''}${tpl ? '' : ' without the not-found template'}, want ${want}${to ? ' -> ' + to : ''}`);
  urlRows.push(`| \`${path}\` | ${want}${to ? ' → `' + to + '`' : ''} | ${r.status()}${loc ? ' → `' + loc + '`' : ''}${tpl ? '' : ' (no not-found template)'} | ${ok ? 'ok' : '**FAIL**'} |`);
}

// Stale page cache: a cache-busted fetch (?ddqa=<time>) carries markers of the current build that the plain URL lacks.
// Markers: the layout rails (site/lib/etch.py section()), the exit-link dialog, the response header the cache adds.
const MARKERS = ['dd-rail', 'data-dialog="exit"'];
const cacheRows = [];
for (const [, path, lang, want = 200] of PAGES) {
  if (want !== 200) continue;
  const plain = await api.get(BASE + path), busted = await api.get(BASE + path + '?ddqa=' + Date.now());
  const [pb, bb] = [await plain.text(), await busted.text()];
  const missing = MARKERS.filter((m) => bb.includes(m) && !pb.includes(m) && (m !== 'data-dialog="exit"' || lang.startsWith('en')));
  const via = ['x-cache', 'x-varnish', 'age', 'x-proxy-cache', 'cf-cache-status'].map((h) => plain.headers()[h] ? `${h}: ${plain.headers()[h]}` : '').filter(Boolean).join(', ');
  if (missing.length) fails.push(`${path}: served from a stale cache (plain URL lacks ${missing.join(', ')}; a cache-busted fetch has them)${via ? ' [' + via + ']' : ''}`);
  cacheRows.push(`| \`${path}\` | ${missing.length ? '**stale**: lacks ' + missing.join(', ') : 'fresh'} | ${via || '–'} |`);
}

const browser = await chromium.launch();
for (const [name, path, lang, want = 200] of PAGES) {
  for (const w of WIDTHS) {
    // phones as phones (touch, overlay scrollbars): the screenshot is the full 375px, no scrollbar strip
    const ctx = await browser.newContext({ httpCredentials: auth, viewport: { width: w, height: 900 }, ...(w < 768 ? { isMobile: true, hasTouch: true } : {}) });
    const page = await ctx.newPage();
    const errors = [], failed = [];
    // a page that should answer 404 logs its own 404 as a console error: that one is expected
    page.on('console', (m) => { if (m.type() === 'error' && !(want !== 200 && /status of 404/.test(m.text()))) errors.push(m.text().slice(0, 160)); });
    page.on('pageerror', (e) => errors.push(e.message.slice(0, 160)));
    page.on('response', (r) => { if (r.status() >= 400 && r.url().startsWith(BASE) && r.url() !== BASE + path) failed.push(`${r.status()} ${r.url().replace(BASE, '')}`); });
    const resp = await page.goto(BASE + path, { waitUntil: 'networkidle', timeout: 60000 });
    await page.evaluate(() => document.fonts.ready);
    const info = await page.evaluate(() => {
      const meta = (n) => document.querySelector(`meta[name="${n}"]`)?.content || '';
      const fonts = [...document.fonts].filter((f) => f.status === 'loaded').map((f) => f.family.replace(/"/g, ''));
      return {
        overflow: document.documentElement.scrollWidth - window.innerWidth,
        lang: document.documentElement.lang,
        title: document.title,
        robots: meta('robots'),
        canonical: document.querySelector('link[rel=canonical]')?.href || '',
        hreflang: document.querySelectorAll('link[rel=alternate][hreflang]').length,
        exitDialog: !!document.querySelector('dialog[data-dialog="exit"]'),
        // brand palette as ACSS outputs it (ops/acss/build-settings.py COLORS), resolved to rgb by the browser
        palette: Object.fromEntries(['primary', 'secondary', 'accent'].map((c) => {
          const el = document.createElement('i'); el.style.color = `var(--${c})`; document.body.append(el);
          const v = getComputedStyle(el).color; el.remove();
          const g = Object.assign(document.createElement('canvas'), { width: 1, height: 1 }).getContext('2d');
          g.fillStyle = v; g.fillRect(0, 0, 1, 1);  // oklch() -> sRGB pixel
          return [c, { css: v, rgb: [...g.getImageData(0, 0, 1, 1).data.slice(0, 3)] }];
        })),
        jakarta: fonts.includes('Plus Jakarta Sans'),
        bodyFont: getComputedStyle(document.body).fontFamily.split(',')[0].replace(/"/g, '').trim(),
        primary: getComputedStyle(document.documentElement).getPropertyValue('--primary').trim(),
        h2: getComputedStyle(document.documentElement).getPropertyValue('--h2').trim().slice(0, 60),
      };
    });
    // Lazy images (loading="lazy") only load near the viewport: scroll the page through once so the full-page
    // screenshot shows every image, then back to the top (the fixed header and hero are captured as on arrival).
    await page.evaluate(async () => {
      for (let y = 0; y < document.documentElement.scrollHeight; y += window.innerHeight * 0.8) {
        window.scrollTo(0, y);
        await new Promise((r) => setTimeout(r, 120));
      }
      window.scrollTo(0, 0);
    });
    await page.waitForLoadState('networkidle').catch(() => {});
    await page.screenshot({ path: `${OUT}/shots/${name}-${w}.jpg`, fullPage: true, type: 'jpeg', quality: 70 });
    const status = resp ? resp.status() : 0;
    const problems = [];
    if (status !== want) problems.push(`status ${status}, want ${want}`);
    if (info.overflow > 0) problems.push(`horizontal overflow ${info.overflow}px`);
    if (errors.length) problems.push(`console: ${errors[0]}`);
    if (failed.length) problems.push(`failed: ${failed.slice(0, 3).join(', ')}`);
    if (!info.jakarta || info.bodyFont !== 'Plus Jakarta Sans') problems.push(`font: ${info.bodyFont}${info.jakarta ? '' : ' (Jakarta not loaded)'}`);
    if (w === 1440 && info.lang !== lang) problems.push(`lang ${info.lang}, want ${lang}`);
    const BRAND = { primary: [11, 43, 72], secondary: [36, 104, 168], accent: [111, 176, 224] };  // #0B2B48 #2468A8 #6FB0E0
    if (w === 1440) for (const [c, want] of Object.entries(BRAND)) {
      const { css, rgb } = info.palette[c];
      if (rgb.some((v, i) => Math.abs(v - want[i]) > 3)) problems.push(`ACSS --${c} is ${css} (rgb ${rgb.join(', ')}), want rgb(${want.join(', ')})`);
    }
    // the "leaving our website" interstitial is on every English page (site/pages/exit_dialog.py), as on live
    if (w === 1440 && lang.startsWith('en') && !info.exitDialog) problems.push('no exit-link interstitial');
    problems.forEach((p) => fails.push(`${path} @${w}: ${p}`));
    rows.push({ name, path, w, status, ...info, errors, failed, problems });
    await ctx.close();
  }
}
await browser.close();

const first = rows.find((r) => r.w === 1440) || {};
const md = [
  `# Staging QA — ${new Date().toISOString().slice(0, 16).replace('T', ' ')} UTC`, '',
  fails.length ? `**${fails.length} problem(s)**` : '**All checks passed**', '',
  ...fails.map((f) => `- ${f}`), '',
  `ACSS on staging: \`--primary: ${first.primary}\` · \`--h2: ${first.h2}\``, '',
  '## Pages', '', '| Page | Width | Status | Overflow | Font | lang | Robots | hreflang | Problems |', '|---|---|---|---|---|---|---|---|---|',
  ...rows.map((r) => `| [${r.name}](shots/${r.name}-${r.w}.jpg) | ${r.w} | ${r.status} | ${r.overflow > 0 ? r.overflow + 'px' : '–'} | ${r.jakarta ? 'Jakarta' : r.bodyFont} | ${r.lang} | ${r.robots.slice(0, 30)} | ${r.hreflang} | ${r.problems.join('; ') || 'ok'} |`),
  '', '## Titles', '', ...rows.filter((r) => r.w === 1440).map((r) => `- \`${r.path}\`: ${r.title}`),
  '', '## Old URLs', '', '| Path | Want | Got | |', '|---|---|---|---|', ...urlRows, '',
  '## Page cache', '', '| Page | Plain URL vs cache-busted | Cache headers |', '|---|---|---|', ...cacheRows, '',
].join('\n');
fs.writeFileSync(`${OUT}/report.md`, md);
fs.writeFileSync(`${OUT}/results.json`, JSON.stringify({ fails, rows, urls: urlRows }, null, 1));
console.log(md);
process.exit(fails.length ? 1 : 0);
