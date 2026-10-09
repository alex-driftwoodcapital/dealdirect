"""Site footer builder: the footer of the EB-5 designs (EN, ES, PT share its markup; only the strings change). q is a Copy
over the EN footer or an Aligned copy over another language's footer. One Etch component per language."""
from etch import El, Svg

LOGO = 'https://driftwooddealdirect.com/wp-content/uploads/dealdirect-logo.svg'


def build(q):
    return [
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
