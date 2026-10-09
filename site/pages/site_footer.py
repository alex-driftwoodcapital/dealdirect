"""Site footer, English (Etch component, wp_block "site-footer"): the footer of handoff/design/EB-5 Investments.dc.html,
built by site/lib/footer.py. The ES/PT EB-5 pages use site_footer_es / site_footer_pt from the same builder."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
from design import Copy
from footer import build

DESIGN = os.path.join(os.path.dirname(__file__), '..', '..', 'handoff', 'design', 'EB-5 Investments.dc.html')
q = Copy(DESIGN, '<footer', '</footer>')
PAGE = build(q)
STYLESHEETS = ['shared', 'footer']
META = {'kind': 'component', 'title': 'Site footer', 'slug': 'site-footer', 'order': 11}
MEDIA = {}
NON_DESIGN = set()
