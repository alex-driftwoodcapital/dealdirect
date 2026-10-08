// usage: node verify.mjs <outdir> <url> [<url>...]   env: BROWSERS_PATH (default ~/.cache/etch-verify-browsers)
// Per URL at 375 and 1440: HTTP status, horizontal overflow (+ offending elements), console errors, failed requests, screenshot.
import { mkdirSync, writeFileSync } from 'node:fs';
import { homedir } from 'node:os';
process.env.PLAYWRIGHT_BROWSERS_PATH ||= `${homedir()}/.cache/etch-verify-browsers`;
const { chromium } = await import('playwright-core');
const BLOCK = /google-analytics|googletagmanager|doubleclick|facebook\.net/;
const [out, ...urls] = process.argv.slice(2);
if (!out || !urls.length) { console.error('usage: node verify.mjs <outdir> <url>...'); process.exit(2); }
mkdirSync(out, { recursive: true });
const browser = await chromium.launch();
const results = [];
for (const url of urls) for (const width of [375, 1440]) {
  const ctx = await browser.newContext({ viewport: { width, height: 900 }, reducedMotion: 'reduce' });
  await ctx.route(BLOCK, r => r.abort()); // never send staging hits to analytics
  const page = await ctx.newPage();
  const errors = [], failed = [];
  page.on('console', m => { if (m.type() === 'error' && !BLOCK.test(m.location().url || '')) errors.push(m.text()); });
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  page.on('requestfailed', r => !BLOCK.test(r.url()) && failed.push(`${r.url()} ${r.failure()?.errorText}`));
  const resp = await page.goto(url, { waitUntil: 'networkidle', timeout: 45000 }).catch(e => ({ status: () => 0, err: e.message }));
  const status = resp.status();
  const title = await page.title();
  const m = await page.evaluate(() => {
    const de = document.documentElement, vw = de.clientWidth;
    const bad = [...document.body.querySelectorAll('*')].filter(e => { const r = e.getBoundingClientRect(); return r.width && r.right > vw + 1 && getComputedStyle(e).position !== 'fixed'; })
      .slice(0, 5).map(e => e.tagName.toLowerCase() + (e.className && typeof e.className === 'string' ? '.' + e.className.split(' ')[0] : '') + ' right=' + Math.round(e.getBoundingClientRect().right));
    return { scrollWidth: de.scrollWidth, vw, overflow: de.scrollWidth > vw + 1, bad, h1: document.querySelectorAll('h1').length, imgsNoAlt: [...document.images].filter(i => !i.hasAttribute('alt')).length };
  });
  const slug = new URL(url).pathname.replace(/\W+/g, '_').replace(/^_|_$/g, '') || 'home';
  const shot = `${out}/${slug}-${width}.png`;
  await page.screenshot({ path: shot, fullPage: true });
  results.push({ url, width, status, title, ...m, consoleErrors: errors, failedRequests: failed, screenshot: shot });
  await ctx.close();
}
await browser.close();
writeFileSync(`${out}/report.json`, JSON.stringify(results, null, 1));
let md = '# Verify report\n\n| URL | px | status | overflow | h1 | img no alt | console errors | failed req |\n|---|---|---|---|---|---|---|---|\n';
for (const r of results) md += `| ${new URL(r.url).pathname} | ${r.width} | ${r.status} | ${r.overflow ? 'YES ' + r.bad.join('; ') : 'no'} | ${r.h1} | ${r.imgsNoAlt} | ${r.consoleErrors.length} | ${r.failedRequests.length} |\n`;
writeFileSync(`${out}/report.md`, md);
console.log(md);
process.exit(results.some(r => r.status !== 200 || r.overflow || r.consoleErrors.length) ? 1 : 0);
