"""Home (/; staging page #48, the front page): Etch build of handoff/design/DealDirect Home.dc.html. Hero with the
rendering video, Live offerings and Past offerings as Etch loops over `offering` posts (handoff/docs/cpt-schema.md
"Home loops"; card fields set on each offering, site/pages/offering_*.py META['fields']), the tax-advantaged routes and
the legal block. Every static string comes from the design file via q(); card text comes from the offerings' fields.
CTAs that open the registration dialog (forms phase) carry data-modal-open="registration"."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
from etch import El, Img, Loop, section
from design import Copy
from offering import ARROW, UP, sup

DESIGN = os.path.join(os.path.dirname(__file__), '..', '..', 'handoff', 'design', 'DealDirect Home.dc.html')
q = Copy(DESIGN)
COPY_SOURCE = 'DealDirect Home.dc.html'  # literals inside the card expressions are checked against it

HERO_SCRIPT = """// home-hero: muted background loop; never plays under prefers-reduced-motion (QA checklist). Scoped; no globals.
const video = document.querySelector('.home-hero__video');
if (video && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  video.muted = true;
  video.preload = 'auto';
  video.play().catch(() => {});
}
"""
hero = section('Hero', 'home-hero', 'home-hero-h', [
    # No autoplay attribute: the script starts it, so reduced-motion visitors only get the poster (LCP image).
    El('video', 'Hero video', 'home-hero__video', {
        'src': '{{mediaurl:Dream_Website_banner}}', 'poster': '{{mediaurl:Riverside-Wharf_View-from-River}}',
        'muted': '', 'loop': '', 'playsinline': '', 'preload': 'none', 'aria-hidden': 'true'}, script=HERO_SCRIPT),
    El('div', 'Veil', 'home-hero__veil', {'aria-hidden': 'true'}),
    El('div', 'Copy', 'home-hero__copy', children=[
        El('h1', 'Heading', 'home-hero__title', {'id': 'home-hero-h'}, [q('Invest today with DealDirect')]),
        El('p', 'Lede', 'home-hero__lede', children=[q('We find the deals')]),
        El('div', 'Actions', 'home-hero__actions', children=[
            El('button', 'Start investing', 'button button--white', {'type': 'button', 'data-modal-open': 'registration'}, [q('Start Investing')]),
        ]),
    ]),
])

# ---------- live offerings: a loop over open + coming-soon offerings ----------
STATUS = '{item.meta.offering_status.equal("coming_soon", "Coming soon", "Open")}'
card = El('article', 'Offering card', 'deal-card', {
    'id': '{item.slug}', 'data-status': '{item.meta.offering_status}', 'data-rendering': '{item.meta.card_rendering}'}, [
    El('div', 'Photo', 'deal-card__photo', children=[Img('Photo', '{item.meta.card_image}', '')]),
    El('span', 'Rendering chip', 'chip chip--glass rendering-chip deal-card__rendering', children=[q('Rendering')]),
    El('div', 'Veil', 'deal-card__veil', {'aria-hidden': 'true'}),
    El('span', 'Status', 'chip chip--glass deal-card__chip', children=[STATUS]),
    El('div', 'Body', 'deal-card__body', children=[
        El('p', 'Eyebrow', 'deal-card__eyebrow', children=['{item.meta.offering_tag}']),
        El('h2', 'Title', 'deal-card__title', children=['{item.meta.card_title}']),
        El('p', 'Summary', 'deal-card__summary', children=['{item.meta.card_summary}']),
        El('a', 'View offering', 'deal-card__cta', {'href': '{item.permalink.relative}'}, ['{item.meta.card_cta_label}', ARROW]),
        # Coming soon: the registration dialog (forms phase) submits with this offering's URL as pageUri
        # (handoff/docs/hubspot-setup-steps.md "Home page QOZ Get notified").
        El('button', 'Get notified', 'deal-card__notify', {'type': 'button', 'data-modal-open': 'registration',
                                                         'data-page-uri': '{item.permalink.relative}',
                                                         'data-page-name': '{item.title}'}, [q('Get notified'), ARROW]),
        El('p', 'Notified', 'deal-card__notified', {'role': 'status', 'tabindex': '-1', 'hidden': ''}, [q("Thank you. We'll email you")]),
    ]),
])
live = section('Live offerings', 'home-live', None, [
    El('div', 'Grid', 'home-live__grid', children=[Loop('Live offerings', 'ddlive1', 'item', [card])]),
], attrs={'id': 'offerings', 'aria-label': 'Live offerings'})

# ---------- tax-advantaged routes ----------
ROUTES = [  # (number, position label, position, heading, body, footnote ref, invest-via label, href, learn-more href)
    ('01', 'You have', 'Realized capital gains', 'Qualified Opportunity Zone Funds', 'Directs capital gains', '1',
     'Riverside Wharf Miami QOF', '/offering/riverside-wharf-qoz/', 'https://driftwoodcapital.com/opportunity-zones/'),
    ('02', 'You are', 'A 1031 exchange buyer', 'Delaware Statutory Trusts', 'Offers fractional interests', '2',
     'Driftwood Hotel Income I, DST', '#courtyard-dst', 'https://driftwoodcapital.com/1031-exchanges-and-dsts/'),
    ('03', 'You are seeking', 'To offset passive income', 'Bonus Depreciation Funds', 'Applies cost segregation', None,
     'Driftwood Tax Advantage Strategy I', '#advantaged-strategy-2026', 'https://driftwoodcapital.com/bonus-depreciation/'),
]


def route(num, pos_label, pos, heading, body, ref, via, via_href, more):
    # The design's thin gradient rule above the heading is left out: no accent rules above headings (CLAUDE.md, Brand).
    return El('article', heading, 'tax-route', children=[
        El('p', 'Number', 'tax-route__num', children=[q(num)]),
        El('p', 'Position label', 'tax-route__label', children=[q(pos_label)]),
        El('p', 'Position', 'tax-route__position', children=[q(pos)]),
        El('h3', 'Heading', 'tax-route__title', children=[q(heading)]),
        El('p', 'Body', 'tax-route__body', children=[q(body)] + ([sup(ref)] if ref else [])),
        El('div', 'Invest via', 'tax-route__via', children=[
            El('span', 'Label', 'tax-route__via-label', children=[q('Invest via')]),
            El('a', 'Vehicle', 'tax-route__vehicle', {'href': via_href}, [q(via)]),
        ]),
        El('a', 'Learn more', 'tax-route__more', {'href': more}, [q('Learn how it works'), ARROW]),
    ])


tax = section('Tax-advantaged', 'home-tax', 'tax-h', [
    El('div', 'Intro', 'home-tax__intro', children=[
        El('p', 'Eyebrow', 'eyebrow home-tax__eyebrow', children=[q('Driftwood Strategies · Tax-Advantaged')]),
        El('h2', 'Heading', 'home-tax__title', {'id': 'tax-h'}, [q('Tax-advantaged access to the Driftwood platform')]),
        El('p', 'Lede', 'home-tax__lede', children=[q('Three vehicles that pair')]),
    ]),
    El('div', 'Routes', 'home-tax__grid', children=[route(*r) for r in ROUTES]),
    El('div', 'Footnotes', 'footnotes', children=[El('p', 'Footnote', children=[q('1. Qualified Opportunity Zone benefits')]),
                                                  El('p', 'Footnote', children=[q('2. Qualification of a Delaware Statutory Trust')])]),
], attrs={'id': 'tax-advantaged'})

# ---------- past offerings: a loop over closed offerings; the one-item guard loop drops the whole band when none ----------
tile = El('article', 'Past offering', 'past-tile', children=[
    El('div', 'Photo', 'past-tile__photo', children=[Img('Photo', '{past.meta.card_image}', '')]),
    El('div', 'Veil', 'past-tile__veil', {'aria-hidden': 'true'}),
    El('span', 'Status', 'chip chip--light past-tile__chip', children=[q('Closed')]),
    El('div', 'Body', 'past-tile__body', children=[
        El('p', 'Tag', 'past-tile__tag', children=['{past.meta.offering_tag}']),
        El('h3', 'Name', 'past-tile__title', children=['{past.meta.card_title}']),
    ]),
])
past = Loop('Past offerings (shown when any exist)', 'ddpastg', 'guard', [
    section('Past offerings', 'home-past', None, [
        El('div', 'Grid', 'home-past__grid', children=[Loop('Past offerings', 'ddpast1', 'past', [tile])]),
    ], attrs={'id': 'past', 'aria-label': 'Past offerings'}),
])

legal = section('Legal', 'legal-block', 'legal-h', [
    El('h2', 'Heading', 'legal-block__title', {'id': 'legal-h'}, [q('Legal disclosure')]),
    El('p', 'Text', children=[q('This website is not an offer')]),
    El('h2', 'Heading', 'legal-block__title', children=[q('* Target Returns')]),
    El('p', 'Text', children=[q('The target returns shown')]),
], attrs={'id': 'legal'})

STYLESHEETS = ['shared']
PAGE = [hero, live, tax, past, legal]


def offerings_query(statuses, count=-1):
    # handoff/docs/cpt-schema.md "Home loops" (liveOfferings / pastOfferings), ordered by home_order
    return {'type': 'wp-query', 'args': {
        'post_type': 'offering', 'post_status': 'publish', 'posts_per_page': count,
        'meta_query': [{'key': 'offering_status', 'value': statuses, 'compare': 'IN'}],
        'meta_key': 'home_order', 'orderby': 'meta_value_num', 'order': 'ASC'}}


# Etch loop records (etch_loops option; fixtures/loops-used.json shape), upserted by the deploy before the page.
LOOPS = {
    'ddlive1': {'key': 'liveOfferings', 'name': 'Live offerings', 'global': True, 'config': offerings_query(['open', 'coming_soon'])},
    'ddpast1': {'key': 'pastOfferings', 'name': 'Past offerings', 'global': True, 'config': offerings_query(['closed'])},
    'ddpastg': {'key': 'pastOfferingsAny', 'name': 'Past offerings (any)', 'global': True, 'config': offerings_query(['closed'], 1)},
}

# Not design copy: the arrow. Card text is offering data (fields), checked on the offering modules.
NON_DESIGN = {'→'}
MEDIA = {
    'Dream_Website_banner': (UP + 'Dream_Website_banner.mp4', 'Video'),
    'Riverside-Wharf_View-from-River': (UP + 'Riverside-Wharf_View-from-River.jpg', 'Riverside Wharf'),
}
META = {'title': 'Home', 'slug': 'home', 'status': 'publish', 'seo': {}}  # front page (page_on_front = 48); live head: pattern title, no og:image
