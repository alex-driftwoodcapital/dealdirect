// Read-only semantic audit: node audit-semantic.js <url...>. Run where the site is reachable.
// Needs playwright (npm i -g playwright).
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch({args:['--no-sandbox']});
for(const u of process.argv.slice(2)){const pg=await b.newPage();
try{const r=await pg.goto(u,{waitUntil:'networkidle',timeout:60000});
await pg.waitForTimeout(3000);
const d=await pg.evaluate(()=>{const q=s=>[...document.querySelectorAll(s)];
return {url:location.href,title:document.title,h:q('h1,h2,h3,h4,h5,h6').map(e=>e.tagName+':'+e.textContent.trim().slice(0,38)),
lm:{header:q('header').length,nav:q('nav').map(n=>n.getAttribute('aria-label')),main:q('main').length,footer:q('footer').length},lang:document.documentElement.lang,
imgs:q('img').length,noalt:q('img:not([alt])').length,emptyalt:q('img[alt=""]').length,
emptyLinks:q('a').filter(a=>!a.textContent.trim()&&!a.getAttribute('aria-label')&&!a.querySelector('img[alt]:not([alt=""]),svg title')).length,
emptyBtn:q('button').filter(a=>!a.textContent.trim()&&!a.getAttribute('aria-label')).length,
roleBtn:q('[role=button]:not(button)').length,
dupIds:(()=>{const c={};q('[id]').forEach(e=>c[e.id]=(c[e.id]||0)+1);return Object.keys(c).filter(k=>c[k]>1).slice(0,5)})(),
btnNoType:q('form button:not([type])').length,ul:q('ul').length,sections:q('section').length,sectNoLabel:q("section:not([aria-labelledby]):not([aria-label])").length}});
console.log(JSON.stringify(d));}catch(e){console.log(u,'ERR',e.message.slice(0,100))}
await pg.close()}
await b.close()})();
