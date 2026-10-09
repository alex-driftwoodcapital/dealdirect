"""/new-eb-5-page/ (the live EB-5 ads landing page, permalink kept): the same page as /eb-5-investments/
(handoff/docs/eb5-localization.md: "same content"), built from the same design and builder. Live serves it noindex;
the SEO step must carry that over (handoff/docs/permalinks.md: robots per page)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from eb5 import PAGE, q, NON_DESIGN, MEDIA, STYLESHEETS  # noqa: F401  (one page, two permalinks)

META = {'title': 'New EB-5 Page', 'slug': 'new-eb-5-page', 'status': 'publish'}  # live title; frozen permalink
