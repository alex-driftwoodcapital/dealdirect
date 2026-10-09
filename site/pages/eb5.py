"""EB-5 Investments (/eb-5-investments/): Etch build of handoff/design/EB-5 Investments.dc.html, with the sections from
site/lib/eb5_page.py (shared with the ES/PT pages and /new-eb-5-page/). Every string comes from the design file via q.
Header, footer and the request dialog come from the page template; the EB-5 dialog component (site/pages/eb5_dialog.py)
ends the page and opens from data-modal-open="eb5-register"."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
from design import Copy
from eb5_page import SEO, alt_texts, build, media, track_data

DESIGN = os.path.join(os.path.dirname(__file__), '..', '..', 'handoff', 'design', 'EB-5 Investments.dc.html')
q = Copy(DESIGN)
TRACK = track_data(DESIGN)
PAGE = build(q, TRACK, alt_texts(DESIGN))

# Strings on the page that are not design copy: arrows, numbering, the approx sign the design's <dw-stat approx> renders,
# and the prior-project data from the design script.
NON_DESIGN = {'→', '+', '±', '1', '2', '1.', '2.', '3.', '4.', '5.'} | {v for t in TRACK for v in t[:6]}
STYLESHEETS = ['shared', 'eb5_layout']  # the EB-5 pages share eb5_layout.css
MEDIA = media(DESIGN)  # slug -> (source, Etch Asset Manager collection)

META = {'title': 'EB-5 Investments', 'slug': 'eb-5-investments', 'status': 'publish', 'seo': SEO}  # frozen permalink /eb-5-investments/ (handoff/docs/permalinks.md)
