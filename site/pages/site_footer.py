"""Site footer (Etch component, wp_block "site-footer"): the footer of handoff/design/EB-5 Investments.dc.html
(identical in every design file). Copy is looked up from that footer, never retyped."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
from etch import El, Svg
from design import Copy

DESIGN = os.path.join(os.path.dirname(__file__), '..', '..', 'handoff', 'design', 'EB-5 Investments.dc.html')
q = Copy(DESIGN, '<footer', '</footer>')
LOGO = 'https://driftwooddealdirect.com/wp-content/uploads/dealdirect-logo.svg'

PAGE = [
    El('footer', 'Site footer', 'site-footer', children=[
        El('div', 'Inner', 'site-footer__inner', children=[
            El('div', 'Top', 'site-footer__top', children=[
                Svg('Logo', LOGO, 'Driftwood Capital | DealDirect', cls='site-footer__logo'),
                El('a', 'Investor login', 'site-footer__login', {'href': 'https://app.junipersquare.com/login?path=%2Fi%2Fdriftwoodcapital'},
                   [q('Existing investor? Log into your dashboard.')]),
            ]),
            El('div', 'Rule', 'site-footer__rule', {'aria-hidden': 'true'}),
            El('div', 'Bottom', 'site-footer__bottom', children=[
                El('p', 'Copyright', 'site-footer__copy', children=[q('Copyright ©')]),
                El('nav', 'Legal nav', 'site-footer__legal', {'aria-label': 'Legal'}, [
                    El('a', 'Privacy', 'site-footer__link', {'href': 'https://driftwoodcapital.com/privacy-policy/'}, [q('Privacy Policy')]),
                    El('a', 'Terms', 'site-footer__link', {'href': 'https://driftwoodcapital.com/terms-of-use/'}, [q('Terms of Use')]),
                ]),
            ]),
        ]),
    ]),
]
META = {'kind': 'component', 'title': 'Site footer', 'slug': 'site-footer', 'order': 11}
MEDIA = {}
NON_DESIGN = set()
