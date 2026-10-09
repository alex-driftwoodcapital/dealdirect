"""Template for the Portuguese EB-5 page (wp_template "page-investimentos-eb-5": WordPress's page-{slug} template, which wins over "page"
for that one page): the page frame with the Portuguese footer (site_footer_pt)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from template_page import frame, MEDIA, q, NON_DESIGN  # noqa: F401

PAGE = frame(footer='site-footer-pt', exit_dialog=False)
META = {'kind': 'template', 'title': 'Page: investimentos-eb-5', 'slug': 'page-investimentos-eb-5', 'order': 23}
