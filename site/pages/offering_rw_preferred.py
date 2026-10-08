"""Riverside Wharf Preferred Equity (/offering/riverside-wharf-preferred-equity/): an `offering` post rendered by the
single-offering template. Etch build of handoff/design/Riverside Wharf Preferred Equity.dc.html; section order and
anchors follow the design (#metrics #overview #webinar #partners #offering #market #legal), every string comes from
the design file via q(). CTAs that open the request dialog (forms phase) keep href="#request" and carry
data-modal-open="offering-request"."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
from etch import El, Img, section
from design import Copy

DESIGN = os.path.join(os.path.dirname(__file__), '..', '..', 'handoff', 'design', 'Riverside Wharf Preferred Equity.dc.html')
q = Copy(DESIGN)
ARROW = El('span', 'Arrow', attrs={'aria-hidden': 'true'}, children=['→'])


def sup(n):
    return El('sup', 'Footnote ref', children=[n])


def request(label, cls='button button--primary', name='Request'):
    return El('a', name, cls, {'href': '#request', 'data-modal-open': 'offering-request'}, [q(label)])


def chip(cls=''):
    return El('span', 'Rendering chip', ('chip chip--glass rendering-chip ' + cls).strip(), children=[q('Rendering')])


def footnotes(name, paras, dark=False):
    return El('div', name, 'footnotes footnotes--dark' if dark else 'footnotes', children=paras)


def fn(ref, text):
    return El('p', 'Footnote', children=([sup(ref)] if ref else []) + [q(text)])


# ---------- hero ----------
HERO_SCRIPT = """// offering-hero: muted background loop; never plays under prefers-reduced-motion (QA checklist). Scoped; no globals.
const video = document.querySelector('.offering-hero__video');
if (video && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  video.muted = true;
  video.preload = 'auto';
  video.play().catch(() => {});
}
"""
hero = section('Hero', 'offering-hero', 'offering-hero-h', [
    # No autoplay attribute: the script starts it, so reduced-motion visitors only get the poster (LCP image).
    El('video', 'Hero video', 'offering-hero__video', {
        'src': '{{mediaurl:Dream_Website_banner}}', 'poster': '{{mediaurl:Riverside-Wharf_View-from-River}}',
        'muted': '', 'loop': '', 'playsinline': '', 'preload': 'none',
        'aria-label': 'Riverside Wharf Miami rendering video'}, script=HERO_SCRIPT),
    chip('offering-hero__rendering'),
    El('div', 'Veil', 'offering-hero__veil', {'aria-hidden': 'true'}),
    El('div', 'Copy', 'offering-hero__copy', children=[
        El('div', 'Heading group', children=[
            El('p', 'Eyebrow', 'eyebrow eyebrow--dark offering-hero__eyebrow', children=[q('Preferred Equity')]),
            El('h1', 'Heading', 'offering-hero__title', {'id': 'offering-hero-h'}, [q('Riverside Wharf Miami')]),
        ]),
        request('Request Investor Details', 'button button--white', 'Request investor details'),
    ]),
])

# ---------- target metrics ----------
METRICS = [  # (value, qualifier, label, footnote ref, accent)
    ('13.0%', 'Target*', 'Net Quarterly Distributions', '1', True),
    ('1.65x', 'Target*', 'Net Equity Multiple', None, False),
    ('$100,000', None, 'Minimum Investment', '2', False),
    ('5-Year', None, 'Assumed Hold Period', '3', False),
]


def stat(value, qualifier, label, ref, accent):
    return El('div', 'Stat', 'stat-card stat-card--tall offering-stat', children=[
        El('p', 'Value', 'stat-card__value stat-card__value--accent' if accent else 'stat-card__value', children=[
            q(value)] + ([El('span', 'Qualifier', 'stat-card__qualifier', children=[q(qualifier)])] if qualifier else [])),
        El('p', 'Label', 'stat-card__label', children=[q(label)] + ([sup(ref)] if ref else [])),
    ])


METRIC_NOTES = [('1', 'Targeted preferred return anticipated'), ('2', 'The minimum investment amount'),
                ('3', 'The anticipated hold period'), (None, '* Target internal rate of return')]


def legal_link():
    return El('a', 'Disclaimers link', 'link-arrow', {'href': '#legal'}, [q('Click here to see important disclaimers')])


metrics = section('Target metrics', 'offering-metrics', 'metrics-h', [
    El('h2', 'Heading', 'offering-metrics__title', {'id': 'metrics-h'}, [q('Preferred Equity Target Metrics'), sup(q('* 1'))]),
    El('p', 'Lede', 'offering-metrics__lede', children=[q('Targeted net quarterly distributions')]),
    El('div', 'Stats', 'offering-metrics__grid', children=[stat(*m) for m in METRICS]),
    footnotes('Footnotes', [fn(r, t) for r, t in METRIC_NOTES] + [legal_link()]),
], attrs={'id': 'metrics'})

# ---------- sub-nav (labels and anchors from the design's subnav data) ----------
SUBNAV = [('Metrics', 'metrics'), ('Overview', 'overview'), ('Video', 'webinar'), ('Partners', 'partners'),
          ('Offering', 'offering'), ('Market', 'market'), ('Legal', 'legal')]
subnav = El('nav', 'On this page', 'offering-subnav', {'aria-label': 'On this page'}, [
    El('div', 'Rail', 'offering-subnav__rail', children=[
        El('a', label, 'offering-subnav__link', {'href': '#' + anchor}, [label]) for label, anchor in SUBNAV
    ]),
])

# ---------- overview ----------
overview = section('Overview', 'offering-overview', 'overview-h', [
    El('div', 'Row', 'media-split', children=[
        El('figure', 'Image', 'media-card', children=[Img('Pool deck', 'Riverside-Wharf_Pooldeck', 'Riverside Wharf Pool deck'), chip()]),
        El('div', 'Copy', 'media-split__copy', children=[
            El('h2', 'Heading', 'offering-overview__title', {'id': 'overview-h'}, [q('A hospitality & entertainment development')]),
            El('div', 'Body', 'offering-overview__body', children=[
                El('p', 'Text', children=[q('This two tower project'), sup('1'), q(', a rooftop day club'), sup('2'), q('.')]),
                El('p', 'Text', children=[q('Designed to foster')]),
                El('p', 'Text', children=[q('Located in a market')]),
                El('p', 'Text', children=[q('The project is structured with the objective of generating cash flows')]),
            ]),
            request('Request Offering Details'),
        ]),
    ]),
    footnotes('Footnotes', [fn(None, '1 Profile Magazine'), fn(None, '2 These project descriptions'),
                            fn(None, 'All information is as of the date indicated'), fn(None, 'Nothing herein constitutes')]),
], attrs={'id': 'overview'})

# ---------- webinar (click-to-play: the Vimeo iframe is only created on click) ----------
VIDEO_SCRIPT = """// offering-video: replace the poster with the Vimeo player on click (no third-party request before that). Scoped.
document.querySelectorAll('.offering-video__frame').forEach((frame) => {
  const play = frame.querySelector('.offering-video__play');
  if (!play) return;
  play.addEventListener('click', () => {
    const iframe = document.createElement('iframe');
    iframe.src = frame.dataset.videoSrc;
    iframe.title = frame.dataset.videoTitle;
    iframe.allow = 'autoplay; fullscreen; picture-in-picture';
    iframe.allowFullscreen = true;
    frame.replaceChildren(iframe);
    iframe.focus();
  });
});
"""
webinar = section('Webinar', 'offering-video', None, [
    Img('Background', 'cover-bg', ''),
    El('div', 'Frame', 'offering-video__frame', {
        'data-video-src': 'https://player.vimeo.com/video/1213615578?h=cd2e9fb726&byline=0&title=0&autoplay=1',
        'data-video-title': 'Riverside Wharf Miami webinar'}, script=VIDEO_SCRIPT, children=[
        Img('Poster', 'riverside-wharf-webinar-poster', 'Riverside Wharf Miami video'),
        El('button', 'Play', 'offering-video__play', {'type': 'button', 'aria-label': 'Play video'}, [
            El('span', 'Icon', 'offering-video__icon', {'aria-hidden': 'true'}),
        ]),
    ]),
], attrs={'id': 'webinar', 'aria-label': 'Riverside Wharf Miami webinar'})

# ---------- partners ----------
partners = section('Partners', 'offering-partners', None, [
    El('div', 'Cards', 'offering-partners__grid', children=[
        El('article', 'TAO Group', 'card-light partner-card', children=[
            El('div', 'Media', 'partner-card__media', children=[Img('Photo', 'Night-club-Lobby', ''), chip()]),
            El('div', 'Body', 'partner-card__body', children=[
                El('h2', 'Title', 'partner-card__title', children=[q('Partnering with TAO Group Hospitality')]),
                El('p', 'Text', 'partner-card__text', children=[q('To elevate the entertainment experience')]),
                El('a', 'Link', 'link-arrow', {'href': 'https://taogroup.com/'}, [q('Learn more about TAO Group Hospitality.'), ARROW]),
            ]),
        ]),
        El('article', 'Dream Hotels', 'card-light partner-card', children=[
            El('div', 'Media', 'partner-card__media', children=[Img('Photo', 'Riverside-Wharf-Coastal-Bar', ''), chip()]),
            El('div', 'Body', 'partner-card__body', children=[
                El('h2', 'Title', 'partner-card__title', children=[q('Dream Hotels, part of the Hyatt family')]),
                El('p', 'Text', 'partner-card__text', children=[q('Recognized as a premier lifestyle brand')]),
            ]),
        ]),
    ]),
], attrs={'id': 'partners', 'aria-label': 'Partners'})

# ---------- offering: capitalization stack + highlights ----------
STACK = [  # (amount, label, cumulative %, modifier)
    ('~$96M', 'Total equity', '100%', 'cap-stack__layer--top'),
    ('~$35M', 'Preferred equity', '71%', 'cap-stack__layer--highlight'),
    ('~$60M', 'EB-5 mezzanine loan', '61%', 'cap-stack__layer--mezz'),
    ('~$145M', 'Total senior debt', '43%', 'cap-stack__layer--senior'),
]
HIGHLIGHTS = [  # (text, footnote ref, trailing text)
    ('Represents approximately 71%', '2', '.'), ('The investment targets a 13%', '3', None),
    ('The project is structured with the objective of generating diversified', None, None),
    ('The planned development includes', '4', '.'), ('Special use designations', '5', '.'),
    ('The hospitality component may benefit', None, None), ('The investment structure provides', '6', '.'),
]
OFFERING_NOTES = ['As of November 25, 2025', 'The preferred equity position', '. Subject to available cash flow']
offering = section('Offering', 'offering-structure', None, [
    El('div', 'Row', 'offering-structure__row', children=[
        El('div', 'Capitalization stack', 'cap-stack', children=[
            El('h3', 'Title', 'cap-stack__title', children=[q('Anticipated Capitalization Stack'), sup('1')]),
            El('p', 'Total', 'cap-stack__total', children=[q('~336M')]),
            El('ol', 'Layers', 'cap-stack__layers', children=[
                El('li', label, 'cap-stack__layer ' + mod, children=[
                    El('span', 'Amount and label', 'cap-stack__text', children=[
                        El('strong', 'Amount', 'cap-stack__amount', children=[q(amount)]),
                        El('span', 'Label', 'cap-stack__label', children=[q(label)]),
                    ]),
                    El('span', 'Cumulative', 'cap-stack__pct', children=[q(pct)]),
                ]) for amount, label, pct, mod in STACK
            ]),
        ]),
        El('div', 'Highlights', 'highlights-list', children=[
            El('h3', 'Title', 'highlights-list__title', children=[q('Offering highlights')]),
            El('ul', 'Items', 'highlights-list__items', children=[
                El('li', 'Highlight', 'highlights-list__item', children=[q(t)] + ([sup(r)] if r else []) + ([q(tail)] if tail else []))
                for t, r, tail in HIGHLIGHTS
            ]),
            request('Request Offering Details'),
        ]),
    ]),
    footnotes('Footnotes', [fn(str(i), t) for i, t in enumerate(OFFERING_NOTES, 1)] + [
        fn(None, '4 These project descriptions'), fn(None, '5 These features are expected'), fn(None, '6 For a complete schedule'),
        fn(None, 'All information is as of the date indicated'), fn(None, 'All projections, financial or otherwise, are for illustrative purposes only and should not be construed as what actual results will be. Rather')]),
], attrs={'id': 'offering', 'aria-label': 'Offering'})

# ---------- market ----------
MARKET = [('Florida’s tourism demand', ['1']), ('Miami International Airport served', ['2']),
          ('Miami MSA was ranked', ['3', '; and ranked No. 5', '4']), ('Miami also ranked', ['5']),
          ('Miami’s Downtown submarket', ['6']), ('The luxury and upper-upscale segment', ['6'])]


def market_item(text, rest):
    kids = [q(text)]
    for r in rest:
        kids.append(sup(r) if r.isdigit() else q(r))
    return El('li', 'Driver', 'metrics-band__item', children=kids)


market = section('Market', 'metrics-band metrics-band--dark', 'market-h', [
    El('div', 'Row', 'metrics-band__row', children=[
        El('div', 'Intro', 'metrics-band__intro', children=[
            El('h2', 'Heading', 'metrics-band__title', {'id': 'market-h'}, [q('Strategic market fundamentals')]),
            El('p', 'Text', 'metrics-band__text', children=[q('Characterized by global connectivity')]),
            request('Request Information', 'button button--glass', 'Request information'),
        ]),
        El('ul', 'Drivers', 'metrics-band__list', children=[market_item(t, r) for t, r in MARKET]),
    ]),
    footnotes('Footnotes', [fn(None, '1. VISIT FLORIDA'), fn(None, 'This webpage is a preliminary summary')], dark=True),
], attrs={'id': 'market'})

# ---------- target metrics (repeat) ----------
metrics2 = section('Target metrics (repeat)', 'offering-metrics offering-metrics--repeat', 'metrics2-h', [
    El('div', 'Head', 'offering-metrics__head', children=[
        El('h2', 'Heading', 'offering-metrics__title', {'id': 'metrics2-h'}, [q('Target Metrics*')]),
        request('Download Brochure', name='Download brochure'),
    ]),
    El('div', 'Stats', 'offering-metrics__grid', children=[stat(*m) for m in METRICS]),
    footnotes('Footnotes', [fn(r, t) for r, t in METRIC_NOTES] + [legal_link()]),
])

# ---------- legal (one column, full content width: CLAUDE.md rule 6) ----------
legal = section('Legal', 'legal-block', 'legal-h', [
    El('h2', 'Heading', 'legal-block__title', {'id': 'legal-h'}, [q('Legal disclosure')]),
    El('p', 'Text', children=[q('This website is not an offer')]),
    El('h2', 'Heading', 'legal-block__title', children=[q('* Target Returns')]),
    El('p', 'Text', children=[q('The target returns shown')]),
    El('p', 'Text', children=[q('These types of investments')]),
    El('h2', 'Heading', 'legal-block__title', children=[q('Renderings')]),
    El('p', 'Text', children=[q('This document contains artist')]),
], attrs={'id': 'legal'})

# ---------- get started ----------
cta = section('Get started', 'cta-band cta-band--cover', 'cta-h', [
    El('div', 'Card', 'cta-band__card', children=[
        Img('Background', 'cover-bg', ''),
        El('div', 'Copy', 'cta-band__copy', children=[
            El('h2', 'Heading', 'cta-band__title', {'id': 'cta-h'}, [q('Ready to get started?')]),
            El('p', 'Text', 'cta-band__text', children=[q('Join our network of accredited')]),
        ]),
        request('Start Investing', 'button button--white', 'Start investing'),
    ]),
])

STYLESHEETS = ['shared', 'offering']
PAGE = [hero, metrics, subnav, overview, webinar, partners, offering, market, metrics2, legal, cta]

# Not design copy: the arrow and the sub-nav labels, which the design renders from its script data (subnav: [...]).
NON_DESIGN = {'→'} | {label for label, _ in SUBNAV}
# slug -> (source, Etch Asset Manager collection[, filename]). Live-site uploads keep their filenames.
UP = 'https://driftwooddealdirect.com/wp-content/uploads/'
MEDIA = {
    'Riverside-Wharf_View-from-River': (UP + 'Riverside-Wharf_View-from-River.jpg', 'Riverside Wharf'),
    'Dream_Website_banner': (UP + 'Dream_Website_banner.mp4', 'Video'),
    'Riverside-Wharf_Pooldeck': (UP + 'Riverside-Wharf_Pooldeck.jpg', 'Riverside Wharf'),
    'Night-club-Lobby': (UP + 'Night-club-Lobby.jpg', 'Riverside Wharf'),
    'Riverside-Wharf-Coastal-Bar': (UP + 'Riverside-Wharf-Coastal-Bar.jpg', 'Riverside Wharf'),
    # Vimeo's poster frame for the webinar (design src); its URL has no filename, so it is named here.
    'riverside-wharf-webinar-poster': ('https://i.vimeocdn.com/video/2192570125-97b8978ab21cef729947bb6150572d3d869d9d7201c95d3f32a26fc55c5db2da-d_1920x1080?f=webp&region=us',
                                       'Riverside Wharf', 'riverside-wharf-webinar-poster.webp'),
    'cover-bg': ('site/assets/cover-bg.webp', 'Brand'),  # handoff/design/assets/cover-bg.png at 1920px, WebP
}

META = {'kind': 'offering', 'title': 'Riverside Wharf Preferred Equity', 'slug': 'riverside-wharf-preferred-equity',
        'status': 'publish'}  # frozen permalink /offering/riverside-wharf-preferred-equity/ (handoff/docs/permalinks.md)
