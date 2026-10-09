"""Exit dialog (Etch component, wp_block "exit-dialog"): the live site's "You are now leaving our website" interstitial
(handoff/docs/permalinks.md: keep it). Any click on a link to another site (not this host, not driftwoodcapital.com or
its subdomains; http/https only, as on live) opens it; "Proceed to site" opens the link in a new tab, as on live.
Placed by the English templates (template_page.frame); the live ES/PT pages have no interstitial, so neither do ours.
Copy: verbatim from the live site's modal (inventory 2026-10-08, live/pages/home.html #external-link-modal); the design
files have none, so the strings are listed in NON_DESIGN."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
from etch import El

T = {
    'title': 'You are now leaving our website',
    'text': 'You are about to leave our website and access a third-party site. Please note that we are not responsible '
            'for the content, accuracy, or security of external websites. This link is provided for informational '
            'purposes only and does not constitute an endorsement or recommendation.',
    'go': 'Proceed to site',
    'close': '×',
}

SCRIPT = r"""// exit-dialog: warn before leaving for a third-party site (live behavior). Scoped; no globals.
(() => {
  const dlg = document.querySelector('[data-dialog="exit"]');
  if (!dlg) return;
  const go = dlg.querySelector('[data-exit-go]');
  let opener = null;
  const external = (a) => {
    try {
      const u = new URL(a.href, location.href);
      return /^https?:$/.test(u.protocol) && u.hostname !== location.hostname
        && u.hostname !== 'driftwoodcapital.com' && !u.hostname.endsWith('.driftwoodcapital.com');
    } catch (_) { return false; }
  };
  document.addEventListener('click', (e) => {
    const a = e.target.closest('a[href]');
    if (!a || a === go || !external(a)) return;
    e.preventDefault();
    opener = a;
    go.href = a.href;
    dlg.showModal();
    go.focus();
  }, true);
  const close = () => dlg.close();
  go.addEventListener('click', close);
  dlg.addEventListener('close', () => { if (opener) opener.focus(); });
  dlg.addEventListener('click', (e) => { if (e.target === dlg) close(); });  // backdrop
  dlg.querySelectorAll('[data-close]').forEach((b) => b.addEventListener('click', close));
})();
"""

PAGE = [
    El('dialog', 'Exit dialog', 'dd-dialog', {'data-dialog': 'exit', 'aria-labelledby': 'dd-exit-h'}, script=SCRIPT, children=[
        El('div', 'Panel', 'dd-dialog__panel', children=[
            El('button', 'Close', 'dd-dialog__close', {'type': 'button', 'aria-label': 'Close', 'data-close': ''}, [T['close']]),
            El('div', 'View', 'dd-dialog__view', children=[
                El('h2', 'Heading', 'dd-dialog__title', {'id': 'dd-exit-h', 'tabindex': '-1'}, [T['title']]),
                El('p', 'Text', 'dd-dialog__text', children=[T['text']]),
                El('div', 'Actions', 'dd-dialog__nav', children=[
                    El('a', 'Proceed', 'button button--primary', {'href': '#', 'target': '_blank', 'rel': 'noopener',
                                                                    'data-exit-go': ''}, [T['go']]),
                ]),
            ]),
        ]),
    ]),
]

STYLESHEETS = ['shared', 'dialog']
NON_DESIGN = set(T.values())
q = None
MEDIA = {}
META = {'kind': 'component', 'title': 'Exit dialog', 'slug': 'exit-dialog', 'order': 13}
