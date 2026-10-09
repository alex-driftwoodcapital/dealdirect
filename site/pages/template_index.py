"""Fallback template (wp_template "index" for etch-theme): the page frame, so any view without a more specific template
(an archive, a post type without its own template) still gets the DealDirect header, footer and request dialog. It
replaces the previous build's index template on staging."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from template_page import frame, MEDIA, q, NON_DESIGN  # noqa: F401

PAGE = frame()
META = {'kind': 'template', 'title': 'Index', 'slug': 'index', 'order': 24}
