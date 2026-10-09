// ROLE-TEMPLATE
// Staging performance probe, read-only (GETs only). Each page, as a phone on a throttled connection (4x CPU, ~1.6 Mbps,
// 150 ms RTT): load, then scroll through once (lazy images), and record transfer by type, every image actually shown
// (format, bytes, natural vs displayed pixels), the video, LCP, CLS, long tasks, TTFB and request count. Writes
// qa-out/perf.md + perf.json. Lighthouse (mobile) scores are added by the Perf workflow when it runs.
// env: QA_BASE_URL, QA_HTTP_USER / QA_HTTP_PASSWORD
import fs from 'fs';
import { chromium } from 'playwright';

const BASE = (process.env.QA_BASE_URL || '').replace(/\/$/, '');
const auth = { username: process.env.QA_HTTP_USER || '', password: process.env.QA_HTTP_PASSWORD || '' };
const OUT = 'qa-out';
const PAGES = [['home', '/'], ['eb5', '/eb-5-investments/'], ['eb5-es', '/inversiones-eb-5/'], ['preferred-equity', '/offering/riverside-wharf-preferred-equity/'],
  ['qoz', '/offering/riverside-wharf-qoz/']];
const kb = (n) => `${Math.round(n / 1024)} KB`;

fs.mkdirSync(OUT, { recursive: true });
const browser = await chromium.launch();
const results = [];
for (const [name, path] of PAGES) {
  const ctx = await browser.newContext({ httpCredentials: auth, viewport: { width: 375, height: 812 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
  const page = await ctx.newPage();
  const cdp = await ctx.newCDPSession(page);
  await cdp.send('Network.enable');
  await cdp.send('Network.emulateNetworkConditions', { offline: false, latency: 150, downloadThroughput: 1.6 * 1024 * 1024 / 8, uploadThroughput: 750 * 1024 / 8 });
  await cdp.send('Emulation.setCPUThrottlingRate', { rate: 4 });
  const reqs = [];
  page.on('requestfinished', async (r) => {
    try {
      const s = await r.sizes();
      const res = await r.response();
      reqs.push({ url: r.url(), type: r.resourceType(), bytes: s.responseBodySize + s.responseHeadersSize, mime: res ? (res.headers()['content-type'] || '') : '',
        cache: res ? (res.headers()['cache-control'] || '') : '', enc: res ? (res.headers()['content-encoding'] || '') : '' });
    } catch {}
  });
  await page.addInitScript(() => {
    window.__perf = { cls: 0, lcp: 0, lcpEl: '', long: 0, longN: 0 };
    new PerformanceObserver((l) => l.getEntries().forEach((e) => { if (!e.hadRecentInput) window.__perf.cls += e.value; })).observe({ type: 'layout-shift', buffered: true });
    new PerformanceObserver((l) => { const e = l.getEntries().at(-1); window.__perf.lcp = e.startTime; window.__perf.lcpEl = e.element ? (e.element.tagName + '.' + (e.element.className || '').toString().split(' ')[0]) + (e.url ? ' ' + e.url.split('/').pop() : '') : (e.url || ''); }).observe({ type: 'largest-contentful-paint', buffered: true });
    new PerformanceObserver((l) => l.getEntries().forEach((e) => { window.__perf.long += e.duration - 50; window.__perf.longN += 1; })).observe({ type: 'longtask', buffered: true });
  });
  const t0 = Date.now();
  await page.goto(BASE + path, { waitUntil: 'load', timeout: 120000 });
  const loadMs = Date.now() - t0;
  const atLoad = await page.evaluate(() => ({ ...window.__perf, nav: performance.getEntriesByType('navigation')[0]?.toJSON() }));
  // scroll through like a reader; collect long tasks / shifts while scrolling separately
  await page.evaluate(() => { window.__perf.longScroll = 0; const o = new PerformanceObserver((l) => l.getEntries().forEach((e) => { window.__perf.longScroll += e.duration - 50; })); o.observe({ type: 'longtask' }); });
  await page.evaluate(async () => {
    for (let y = 0; y < document.documentElement.scrollHeight; y += 300) { window.scrollTo(0, y); await new Promise((r) => setTimeout(r, 150)); }
  });
  await page.waitForLoadState('networkidle', { timeout: 60000 }).catch(() => {});
  const after = await page.evaluate(() => {
    const imgs = [...document.querySelectorAll('img')].filter((i) => i.currentSrc).map((i) => {
      const r = i.getBoundingClientRect();
      return { src: i.currentSrc, natural: `${i.naturalWidth}x${i.naturalHeight}`, nw: i.naturalWidth, shown: `${Math.round(r.width)}x${Math.round(r.height)}`, sw: Math.round(r.width), loading: i.loading, srcset: !!i.getAttribute('srcset'), sizes: i.getAttribute('sizes') || '', decoding: i.decoding, fetchpriority: i.getAttribute('fetchpriority') || '' };
    });
    const vids = [...document.querySelectorAll('video')].map((v) => ({ src: v.currentSrc || v.src, preload: v.preload, poster: v.poster }));
    const blur = [...document.querySelectorAll('body *')].filter((e) => { const cs = getComputedStyle(e); return (cs.backdropFilter && cs.backdropFilter !== 'none') && e.getBoundingClientRect().height > 0; }).length;
    const fixedOrSticky = [...document.querySelectorAll('body *')].filter((e) => /fixed|sticky/.test(getComputedStyle(e).position)).length;
    return { ...window.__perf, imgs, vids, blur, fixedOrSticky, height: document.documentElement.scrollHeight };
  });
  const byType = {};
  reqs.forEach((r) => { const t = r.type === 'media' || /video/.test(r.mime) ? 'media' : r.type; byType[t] = (byType[t] || 0) + r.bytes; });
  const imgBytes = new Map(reqs.filter((r) => r.type === 'image').map((r) => [r.url, r]));
  const imgs = after.imgs.map((i) => ({ ...i, bytes: imgBytes.get(i.src)?.bytes || 0, mime: imgBytes.get(i.src)?.mime || '', cache: imgBytes.get(i.src)?.cache || '' }));
  const nav = atLoad.nav || {};
  results.push({ name, path, loadMs, ttfb: Math.round((nav.responseStart || 0) - (nav.requestStart || 0)), dcl: Math.round(nav.domContentLoadedEventEnd || 0),
    lcp: Math.round(atLoad.lcp), lcpEl: atLoad.lcpEl, cls: +after.cls.toFixed(3), longLoad: Math.round(atLoad.long), longScroll: Math.round(after.longScroll || 0),
    requests: reqs.length, total: reqs.reduce((a, r) => a + r.bytes, 0), byType, imgs, vids: after.vids, blur: after.blur, fixedOrSticky: after.fixedOrSticky,
    htmlEnc: reqs.find((r) => r.type === 'document')?.enc || '', htmlCache: reqs.find((r) => r.type === 'document')?.cache || '',
    big: reqs.filter((r) => r.bytes > 300 * 1024).map((r) => `${r.url.split('/').pop().slice(0, 60)} ${kb(r.bytes)} ${r.mime.split(';')[0]}`) });
  await ctx.close();
}
await browser.close();

fs.writeFileSync(`${OUT}/perf.json`, JSON.stringify(results, null, 1));
const md = [`# Staging performance (phone, 4x CPU, ~1.6 Mbps / 150 ms) — ${new Date().toISOString().slice(0, 16).replace('T', ' ')} UTC`, '',
  '| Page | TTFB | LCP | load | CLS | long tasks load / scroll | requests | total | images | media | js | css | font | backdrop blurs |', '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|',
  ...results.map((r) => `| ${r.name} | ${r.ttfb} ms | ${r.lcp} ms | ${r.loadMs} ms | ${r.cls} | ${r.longLoad} / ${r.longScroll} ms | ${r.requests} | ${kb(r.total)} | ${kb(r.byType.image || 0)} | ${kb(r.byType.media || 0)} | ${kb(r.byType.script || 0)} | ${kb(r.byType.stylesheet || 0)} | ${kb(r.byType.font || 0)} | ${r.blur} |`), ''];
for (const r of results) {
  md.push(`## ${r.name} (${r.path})`, `LCP element: ${r.lcpEl} · HTML encoding: ${r.htmlEnc || 'none'} · HTML cache-control: ${r.htmlCache || '–'} · fixed/sticky elements: ${r.fixedOrSticky}`, '');
  if (r.big.length) md.push('Responses over 300 KB: ' + r.big.join(' · '), '');
  md.push('| image | type | bytes | natural | shown (CSS px) | srcset | loading | fetchpriority |', '|---|---|---|---|---|---|---|---|');
  for (const i of r.imgs) md.push(`| ${i.src.split('/').pop().slice(0, 70)} | ${i.mime.split(';')[0]} | ${kb(i.bytes)} | ${i.natural} | ${i.shown} | ${i.srcset ? 'yes' : 'no'} | ${i.loading} | ${i.fetchpriority || '–'} |`);
  if (r.vids.length) md.push('', 'Video: ' + r.vids.map((v) => `${(v.src || '').split('/').pop()} preload=${v.preload} poster=${(v.poster || '').split('/').pop()}`).join(' · '));
  md.push('');
}
fs.writeFileSync(`${OUT}/perf.md`, md.join('\n') + '\n');
console.log(md.slice(0, results.length + 4).join('\n'));
