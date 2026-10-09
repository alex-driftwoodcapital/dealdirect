"""Page template (wp_template "page" for etch-theme): header component, <main> with the page content, footer
component (docs.etchwp.com/templates: header component + Content Slot + footer component; post-content block form
from fixtures/parts/template-home.html), then the request dialog component (site/pages/request_dialog.py). Applies to
every WordPress page on staging."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
from etch import El, Component, Node


class PostContent(Node):
    def render(self):
        return '<!-- wp:post-content {"align":"full","layout":{"type":"default"}} /-->'


def frame(main_attrs=None, footer='site-footer', exit_dialog=True, main=None):
    # exit_dialog: the "leaving our website" interstitial (site/pages/exit_dialog.py), English pages only (as on live)
    return [
        Component('Site header', 'site-header'),
        El('main', 'Main', attrs=main_attrs, children=main or [PostContent()]),
        Component('Site footer', footer),
        Component('Request dialog', 'request-dialog'),
    ] + ([Component('Exit dialog', 'exit-dialog')] if exit_dialog else [])


PAGE = frame()
META = {'kind': 'template', 'title': 'Page', 'slug': 'page', 'order': 20}
MEDIA = {}
q = None
NON_DESIGN = set()
