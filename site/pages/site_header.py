"""Site header (Etch component, wp_block "site-header"): handoff/README.md Home §1 and the header in every design
file. The final design keeps only the logo. Fixed; transparent with a white logo over the dark hero, frosted white
with a hairline after 40px of scroll (a small scoped script sets data-scrolled; CSS does the rest)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
from etch import El, Svg

LOGO = 'https://driftwooddealdirect.com/wp-content/uploads/dealdirect-logo.svg'
SCRIPT = """// site-header: frosted state after 40px (handoff README Home §1). Scoped; no globals.
const header = document.querySelector('.site-header');
if (header) {
  const update = () => header.toggleAttribute('data-scrolled', window.scrollY > 40);
  update();
  window.addEventListener('scroll', update, { passive: true });
}
"""
PAGE = [
    El('header', 'Site header', 'site-header', script=SCRIPT, children=[
        El('div', 'Rail', 'site-header__rail', children=[
            El('a', 'Logo link', 'site-header__logo', {'href': '/', 'aria-label': 'Driftwood Capital | DealDirect home'}, [
                Svg('Logo', LOGO, 'Driftwood Capital | DealDirect logo', cls='site-header__logo-svg'),
            ]),
        ]),
    ]),
]
META = {'kind': 'component', 'title': 'Site header', 'slug': 'site-header', 'order': 10}
MEDIA = {}
q = None  # no visible text: the logo's accessible name is an attribute
NON_DESIGN = set()
