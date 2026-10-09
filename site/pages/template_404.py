"""Not-found template (wp_template "404" for etch-theme): the page frame (header, <main>, footer, request dialog) with
a dark not-found band in place of the post content (dark like every page's hero, so the transparent header reads). Also what the retired login URLs show, with status 410
(dealdirect-core includes/retired.php). Neither the live site nor the design has 404 copy: the strings below are
placeholders listed in NON_DESIGN until Alex approves them (CLAUDE.md rule 1)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
sys.path.insert(0, os.path.dirname(__file__))
from etch import El, section
from template_page import frame

T = {
    'eyebrow': '404',
    'title': 'Page not found',
    'text': 'The page you are looking for has moved or no longer exists.',
    'home': 'Back to Home',
    'cta': 'Start Investing',  # PRIMARY_CTA (CLAUDE.md), the Home hero's button
}

not_found = section('Not found', 'not-found', 'not-found-h', [
    El('p', 'Eyebrow', 'eyebrow eyebrow--dark', children=[T['eyebrow']]),
    El('h1', 'Heading', 'not-found__title', {'id': 'not-found-h'}, [T['title']]),
    El('p', 'Text', 'not-found__text', children=[T['text']]),
    El('div', 'Actions', 'not-found__actions', children=[
        El('a', 'Home', 'button button--white', {'href': '/'}, [T['home']]),
        El('button', 'Start investing', 'button button--glass', {'type': 'button', 'data-modal-open': 'registration'},
           [T['cta']]),
    ]),
])

PAGE = frame(main=[not_found])
META = {'kind': 'template', 'title': '404', 'slug': '404', 'order': 25}
MEDIA = {}
q = None
NON_DESIGN = set(T.values())
