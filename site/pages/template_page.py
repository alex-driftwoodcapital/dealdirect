"""Page template (wp_template "page" for etch-theme): header component, <main> with the page content, footer
component (docs.etchwp.com/templates: header component + Content Slot + footer component; post-content block form
from fixtures/parts/template-home.html). Applies to every WordPress page on staging."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
from etch import El, Component, Node


class PostContent(Node):
    def render(self):
        return '<!-- wp:post-content {"align":"full","layout":{"type":"default"}} /-->'


PAGE = [
    Component('Site header', 'site-header'),
    El('main', 'Main', children=[PostContent()]),
    Component('Site footer', 'site-footer'),
]
META = {'kind': 'template', 'title': 'Page', 'slug': 'page', 'order': 20}
MEDIA = {}
q = None
NON_DESIGN = set()
