"""Offering single template (wp_template "single-offering" for etch-theme): the same frame as the page template
(header component, <main> with the post content, footer component), so every offering post renders with it.
Each offering's sections are its post content (site/pages/offering_*.py). <main> carries the offering's title as
data-page-name: the request dialog shows it and sends it to HubSpot as pageName."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from template_page import frame, MEDIA, q, NON_DESIGN  # noqa: F401  (one frame for pages and offerings)

PAGE = frame({'data-page-name': '{this.title}'})

META = {'kind': 'template', 'title': 'Single: Offering', 'slug': 'single-offering', 'order': 21}
