// Loads this design system into the template. In a consuming project, point
// base at the bound DS folder relative to this page (e.g. '_ds/<folder>' at
// the project root, '../_ds/<folder>' one level down) — one line to edit.
(() => {
  const here = document.currentScript && document.currentScript.src;
  // _ds_bundle.js compiles EVERY .js in this project — including this file — and
  // executes it, which would load the whole design system a second time from the
  // wrong root (that was 8 console 404s). Only run when we are executing as our
  // own <script src=".../ds-base.js">, never as bundled code.
  if (!here || !/ds-base\.js(\?|$)/.test(here)) return;
  const base = new URL('../_ds/driftwood-capital-design-system-9d3afadb-b605-4c8f-bf63-ba3657b86844/', here).href.replace(/\/$/, '');
  for (const p of ["colors_and_type.css","styles.css"]) {
    const l = document.createElement('link');
    l.rel = 'stylesheet'; l.href = base + '/' + p;
    document.head.appendChild(l);
  }
  const s = document.createElement('script');
  s.src = base + '/_ds_bundle.js';
  s.onerror = () => console.error('ds-base.js: failed to load ' + s.src + ' — if this is a consuming project, point the base line in ds-base.js at the bound _ds/<folder> tree relative to this page (e.g. _ds/<folder> at the project root, ../_ds/<folder> one level down); in a fresh design system this can just mean the bundle is not compiled yet');
  document.head.appendChild(s);
})();
