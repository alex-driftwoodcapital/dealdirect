"""Riverside Wharf QOZ (/offering/riverside-wharf-qoz/; slug to confirm, handoff/docs/permalinks.md): an `offering` post
rendered by the single-offering template. Etch build of handoff/design/Riverside Wharf QOZ.dc.html; section order and
anchors follow the design (#metrics #overview #webinar #partners #offering #market #structure #assets #rationale
#legal), every string comes from the design file via q(). The design's placeholders ("[TBD]", "[QOZ ... from offering
documents]") are shipped as they are: open `gap`s in handoff/design/evidence-register/claims.js, never filled in here.
Sections: site/lib/offering.py."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
from etch import El
from design import Copy
from offering import Offering, MARKET, MARKET_NOTES, METRIC_NOTES, UP, sup

DESIGN = os.path.join(os.path.dirname(__file__), '..', '..', 'handoff', 'design', 'Riverside Wharf QOZ.dc.html')
q = Copy(DESIGN)
o = Offering(q)

METRICS = [  # (value, qualifier, label, footnote ref, accent): values are the design's [TBD] placeholders
    ('[TBD]', 'Target*', 'Net Quarterly Distributions', '1', True),
    ('[TBD]', 'Target*', 'Net Equity Multiple', None, False),
    ('[TBD]', None, 'Minimum Investment', '2', False),
    ('[TBD]', None, 'Assumed Hold Period', '3', False),
]
STACK = [  # the total-equity layer is this offering's highlight (claims.js: confirm the QOZ common equity amount)
    ('~$96M', 'Total equity', '100%', 'cap-stack__layer--highlight cap-stack__layer--lead'),
    ('~$35M', 'Preferred equity', '71%', 'cap-stack__layer--light'),
    ('~$60M', 'EB-5 mezzanine loan', '61%', 'cap-stack__layer--mezz'),
    ('~$145M', 'Total senior debt', '43%', 'cap-stack__layer--senior'),
]
HIGHLIGHTS = [
    ['[QOZ highlight — from offering documents]'], ['[QOZ highlight — from offering documents]'],
    ['The project is located within a Qualified Opportunity Zone'],
    ['The project is structured with the objective of generating diversified'],
    ['The planned development includes', '4', '.'], ['Special use designations', '5', '.'],
    ['The hospitality component may benefit'], ['The investment structure provides', '6', '.'],
]
STRUCTURE_NOTES = [('1', 'As of November 25, 2025'), ('2', 'The preferred equity position'), ('3', '. Subject to available cash flow'),
                   (None, '3 QOZ investments'), (None, '4 These project descriptions'), (None, '5 These features are expected'),
                   (None, '6 For a complete schedule'), (None, 'All information is as of the date indicated'),
                   (None, 'All projections, financial or otherwise, are for illustrative purposes only and should not be construed as what actual results will be. Rather')]
# Sub-nav labels and order from the design's subnav data (its order, not the section order).
SUBNAV = [('Metrics', 'metrics'), ('Overview', 'overview'), ('Video', 'webinar'), ('Partners', 'partners'), ('Offering', 'offering'),
          ('OZ Benefits', 'structure'), ('Program', 'assets'), ('Market', 'market'), ('Rationale', 'rationale'), ('Legal', 'legal')]

IRS = 'https://www.irs.gov/credits-deductions/businesses/opportunity-zones'
oz = o.oz('Riverside-Wharf_Dream-Hotel-Prefunction', 'Riverside Wharf Dream Hotel Pre-function',
          'Potential Opportunity Zone tax incentives', '1', 'Established under the 2017 Tax Cuts and Jobs Act',
          [('Capital Gain Exclusion:', 'For qualifying investments held for 10 years'), ('Tax Deferral and Recognition:', 'The Opportunity Zone framework allows')],
          [El('p', 'Footnote', children=[sup('1'), q('Information is for illustrative purposes only') + ' ',
                                         El('a', 'IRS link', attrs={'href': IRS}, children=[q(IRS)]), q('.')]),
           o.fn(None, 'This webpage is a preliminary summary for discussion purposes only and does not contain all material information. Nothing herein constitutes tax advice')])


# A text node before an inline link keeps its trailing space (the design lookup trims edges; the copy gate ignores them).
def li(*texts):
    return [q(t) for t in texts]


# Program gallery: the design's galleries (Riverside-Wharf + suffix on the live uploads); alt = "Riverside Wharf <tab>".
W = 'Riverside-Wharf'
GALLERIES = [
    ('Hotel', ['_View-from-River', '_Pooldeck', '_Exterior-view-from-street', '-2023-05-25_ICRAVE_THE-WHARF-FB_100-DD-PRESENTATION-22', '_View-from-exterior', '_Complex']),
    ('Restaurants', ['-AFT-show-kitchen', '-AFT-Bar', '-Coastal-Bar', '_Dream-Hotel-Wine-Bar', '-Coastal-dining']),
    ('Entertainment', ['-Night-club-Lobby', '-2023-05-25_ICRAVE_THE-WHARF-FB_100-DD-PRESENTATION-15', '-Night-club-Main-Floor', '-2023-05-25_ICRAVE_THE-WHARF-FB_100-DD-PRESENTATION-10',
                       '-Night-club-Sunset-Lounge', '-2023-05-25_ICRAVE_THE-WHARF-FB_100-DD-PRESENTATION-40', '-RIVERSIDE-WHARF_DAYCLUB_View02b-2023-01-20', '-2023-05-25_ICRAVE_THE-WHARF-FB_100-DD-PRESENTATION-33']),
    ('Conference', ['_Ballroom', '_Dream-Hotel-Prefunction']),
]
SPECS = [
    o.spec('Dream Hotel', [(None, [[q('Dream by Hyatt (upper-upscale lifestyle brand)'), El('br', 'Break'), q('167-Keys')]]),
                           ('Amenities:', [li('Rooftop Pool and Bar'), li('Fitness Facility'), li('Lobby Lounge & Bar')])]),
    o.spec('Unique high-end restaurant experiences', [
        ('High-end: Asian Concept', [li('~10,300 SF'), li('~196-person'), li('Two-story restaurant'), li('Balcony terrace')]),
        ('High-end: Coastal Italian Concept', [li('~8,200 SF'), li('~180-person'), li('Dessert room'), li('Outdoor terrace overlooking Miami River')]),
        ('Three-meal: French Bistro Concept', [li('~2,025 SF'), li('~80-person'), li('Marra Forina')])]),
    o.spec('Signature Entertainment Venues', [
        ('Nightclub', [li('~23,000 SF'), li('Top-tier service'), li('Performances by')]),
        ('Day Club', [li('~14,000 SF'), li('13 luxurious'), li('State-of-the-art sound'), li('Live DJ booth for')]),
        ('Wharf Food & Beverage Venue', [li('Nautical-themed'), li('~33,000 SF'), li('Two outdoor bars'), li('Elevated VIP')])]),
    o.spec('State-of-the-art meeting & event space', [(None, [li('~18,000 SF'), li('Full-service kitchen'), li('Outdoor pre-function terrace overlooking'), li('Miami River')])]),
]
program = o.program('Proposed program', [
    (label, [(W + s, 'Riverside Wharf ' + label) for s in suffixes], spec) for (label, suffixes), spec in zip(GALLERIES, SPECS)
], 'Nothing herein constitutes an offering of securities. All information provided is for informational purposes only and should not be deemed as advice in relation to legal, taxation, financial or investment matters. The descriptions of the project listed herein is')

# The design's "here" link goes through an e-mail link scanner (linklock.titanhq.com); this is its decoded destination.
WHARF = 'https://breakwaterhg.com/portfolio/the-wharf-miami/'
RIVERWALK = 'https://www.aplaceunderthepalms.com/miami-river-and-bay-walks/'
rationale = o.rationale('Investment rationale', [
    ('Efficient land structure', [q('The Project’s mix of fee simple')]),
    ('Favorable long-term ground lease', [q('The Project was awarded an 80-year')]),
    ('Parking cost efficiency', [q('By utilizing off-site parking')]),
    ('Entertainment experience and proof of concept', [q('The Wharf concept has demonstrated') + ' ',
                                                       El('a', 'Wharf link', attrs={'href': WHARF}, children=[El('strong', 'Strong', children=[q('here')])]), q('.')]),
    ('Fully entitled project in a high barrier to entry market', [q('Positioned along the Miami River with approved density and zoning, the site is viewed by the Sponsors as difficult to replicate. A $125M')]),
    ('Entertainment-driven income with structured cash flow potential', [q('Key elements such as the nightclub')]),
    ('Unique zoning advantage with extended operating hours', [q('Positioned along the Miami River with approved density and zoning, the site is viewed by the Sponsors as difficult to replicate. A $145M')]),
    ('Irreplaceable riverfront location', [q('Strategically located on the Miami River') + ' ',
                                          El('a', 'Riverwalk link', attrs={'href': RIVERWALK}, children=[q('Riverwalk')]), q(', the Sponsors believe')]),
], 'Nothing herein constitutes an offering of securities. All information provided is for informational purposes only and should not be deemed as advice in relation to legal, taxation, financial or investment matters. The descriptions of the project listed herein is')

STYLESHEETS = ['shared', 'offering']
PAGE = [
    o.hero('QOZ Common Equity', 'Dream_Website_banner', 'Riverside-Wharf_View-from-River', 'Riverside Wharf Miami rendering video', badge='Coming soon'),
    o.metrics('QOZ Common Equity Target Metrics', '* 1', '[QOZ target summary', METRICS, METRIC_NOTES),
    o.subnav(SUBNAV),
    o.overview('Riverside-Wharf_Pooldeck', 'Riverside Wharf Pool deck', 'A hospitality & entertainment development', [
        ['This two tower project', '1', ', a rooftop day club', '2', '.'], ['Designed to foster'], ['Located in a market'],
        ['The project is structured with the objective of generating cash flows', '3', '.']],
        ['1 Profile Magazine', '2 These project descriptions', '3 Such benefits', 'All information is as of the date indicated',
         'Nothing herein constitutes an offering of securities. All information provided is for informational purposes only and should not be deemed as advice in relation to legal, taxation, financial or investment matters. The description of the project']),
    # No poster in the design (empty image slot): the frame shows the play button on the dark band until clicked.
    o.webinar('https://player.vimeo.com/video/1073671948?byline=0&title=0&autoplay=1', 'Riverside Wharf Miami video'),
    o.partners(),
    o.structure(STACK, HIGHLIGHTS, STRUCTURE_NOTES),
    o.market(MARKET, MARKET_NOTES),
    oz,
    o.metrics_repeat(METRICS, METRIC_NOTES),
    program,
    rationale,
    o.legal(),
    o.cta(),
]

# Not design copy: the arrow, the sub-nav labels (design script data) and the program tab labels (design script data).
NON_DESIGN = {'→'} | {label for label, _ in SUBNAV} | {label for label, _ in GALLERIES}
# slug -> (source, Etch Asset Manager collection). Live-site uploads keep their filenames; images are compressed on
# import with the Etch Asset Manager preset.
MEDIA = {
    'Riverside-Wharf_View-from-River': (UP + 'Riverside-Wharf_View-from-River.jpg', 'Riverside Wharf'),
    'Dream_Website_banner': (UP + 'Dream_Website_banner.mp4', 'Video'),
    'Riverside-Wharf_Pooldeck': (UP + 'Riverside-Wharf_Pooldeck.jpg', 'Riverside Wharf'),
    'Night-club-Lobby': (UP + 'Night-club-Lobby.jpg', 'Riverside Wharf'),
    'cover-bg': ('handoff/design/assets/cover-bg.png', 'Brand'),
    **{W + s: (UP + W + s + '.jpg', 'Riverside Wharf') for _, suffixes in GALLERIES for s in suffixes},
}

COPY_SOURCE = 'DealDirect Home.dc.html'  # card field values below are checked against it (copy gate)
META = {'kind': 'offering', 'title': 'Riverside Wharf Miami – QOZ Common Equity', 'slug': 'riverside-wharf-qoz', 'status': 'publish',
        'fields': {  # Home card (DealDirect Home.dc.html live data, key riverside-wharf-qoz); the summary is the design's placeholder
            'offering_status': 'coming_soon', 'offering_tag': 'QOZ', 'card_title': 'Riverside Wharf Miami',
            'card_summary': '[Summary from offering CPT]', 'card_image': '{{media:Riverside-Wharf_Pooldeck}}', 'card_cta_label': '',
            'card_rendering': 1, 'home_order': 2,
        },
        # no live page of its own: title from the live pattern; og:image as live /offering/riverside-wharf/
        'seo': {'og_image': '{{media:Riverside-Wharf_View-from-River}}', 'og_image_alt': 'Riverside Wharf View from River'}}
