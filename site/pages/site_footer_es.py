"""Site footer, Spanish (Etch component, wp_block "site-footer-es"): the footer of handoff/design/Inversiones EB-5.dc.html read by
position against the EN footer (site/lib/footer.py). Used by the Spanish EB-5 page's template."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
from design import Aligned
from footer import build
from site_footer import q as en

DESIGN = os.path.join(os.path.dirname(__file__), '..', '..', 'handoff', 'design', 'Inversiones EB-5.dc.html')
q = Aligned(en, DESIGN, '<footer', '</footer>')
PAGE = build(q)
STYLESHEETS = ['shared', 'footer']
META = {'kind': 'component', 'title': 'Site footer (Spanish)', 'slug': 'site-footer-es', 'order': 11}
MEDIA = {}
NON_DESIGN = set()
