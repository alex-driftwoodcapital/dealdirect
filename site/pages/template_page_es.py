"""Template for the Spanish EB-5 page (wp_template "page-inversiones-eb-5": WordPress's page-{slug} template, which wins over "page"
for that one page): the page frame with the Spanish footer (site_footer_es)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from template_page import frame, MEDIA, q, NON_DESIGN  # noqa: F401

PAGE = frame(footer='site-footer-es', exit_dialog=False)
META = {'kind': 'template', 'title': 'Page: inversiones-eb-5', 'slug': 'page-inversiones-eb-5', 'order': 22}
