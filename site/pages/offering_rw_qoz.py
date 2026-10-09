"""Riverside Wharf QOZ (/offering/riverside-wharf-qoz/; slug to confirm, handoff/docs/permalinks.md): an `offering` post
rendered by the single-offering template. A teaser for now (Alex, 2026-10-09: "tease the project and allow people to
reserve their spot using the form ... the info we already have + lots of nice renderings + qoz information"):
  - the design's sections (handoff/design/Riverside Wharf QOZ.dc.html, copy via q()), minus its placeholder target
    metrics and placeholder highlights, and (for now) its program and investment rationale sections (DROPPED_COPY);
    key figures from the design's program instead;
  - a renderings mosaic (the design's own Riverside Wharf renderings);
  - "Opportunity Zones Program Explained" from driftwoodcapital.com (site/sources/, ops/sources.txt), lifted block by
    block through site/lib/article.py with its endnotes and disclaimer;
  - every request button reads "Reserve Your Spot" and opens the offering request dialog (Registration / Offering
    Request forms in HubSpot, pageName = this offering).
Sections: site/lib/offering.py; this page's own: site/styles/offering_rw_qoz.css."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
from etch import El, Img, section, all_texts
from article import Article
from design import Copy, norm
from offering import Offering, MARKET, MARKET_NOTES, METRIC_NOTES, UP, sup

DESIGN = os.path.join(os.path.dirname(__file__), '..', '..', 'handoff', 'design', 'Riverside Wharf QOZ.dc.html')
q = Copy(DESIGN)
RESERVE = 'Reserve Your Spot'  # Alex, 2026-10-09 ("reserve their spot using the form"); compliance to confirm the wording
o = Offering(q, cta=RESERVE)
ARTICLE = os.path.join(os.path.dirname(__file__), '..', 'sources', 'driftwoodcapital-opportunity-zones-program-explained.html')
oz_src = Article(ARTICLE, "<div id='inner_content", '<footer id="main-footer"', 'oz-note-')
COPY_EXTRA = [oz_src.copy]

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
HIGHLIGHTS = [  # the design's two "[QOZ highlight — from offering documents]" placeholders are left out (teaser)
    ['The project is located within a Qualified Opportunity Zone'],
    ['The project is structured with the objective of generating diversified'],
    ['The planned development includes', '4', '.'], ['Special use designations', '5', '.'],
    ['The hospitality component may benefit'], ['The investment structure provides', '6', '.'],
]
STRUCTURE_NOTES = [('1', 'As of November 25, 2025'), ('2', 'The preferred equity position'), ('3', '. Subject to available cash flow'),
                   (None, '3 QOZ investments'), (None, '4 These project descriptions'), (None, '5 These features are expected'),
                   (None, '6 For a complete schedule'), (None, 'All information is as of the date indicated'),
                   (None, 'All projections, financial or otherwise, are for illustrative purposes only and should not be construed as what actual results will be. Rather')]
# Sub-nav: the design's labels (its subnav data), in this page's section order, plus Renderings and QOZ 2.0 for the
# teaser's own sections (#metrics now holds the key figures).
SUBNAV = [('Overview', 'overview'), ('Renderings', 'renderings'), ('Video', 'webinar'), ('OZ Benefits', 'structure'),
          ('QOZ 2.0', 'qoz'), ('Partners', 'partners'), ('Offering', 'offering'), ('Market', 'market'), ('Legal', 'legal')]

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

# ---------- teaser sections (this page only; site/styles/offering_rw_qoz.css) ----------
# Key figures (#metrics): the design's own program figures, in place of its "[TBD]" target metrics.
FACTS = [('167-Keys', 'Dream by Hyatt (upper-upscale lifestyle brand)'), ('~23,000 SF', 'Nightclub'), ('~14,000 SF', 'Day Club'),
         ('~33,000 SF', 'Wharf Food & Beverage Venue'), ('~18,000 SF', 'State-of-the-art meeting & event space')]
facts = section('Key figures', 'qoz-facts', None, [
    El('ul', 'Figures', 'qoz-facts__grid', children=[
        El('li', 'Figure', 'qoz-facts__item', children=[
            El('strong', 'Value', 'qoz-facts__value', children=[q(v)]),
            El('span', 'Label', 'qoz-facts__label', children=[q(l)]),
        ]) for v, l in FACTS
    ]),
], attrs={'id': 'metrics', 'aria-label': 'Key figures'})

# Renderings mosaic (#renderings): the design's renderings; the first is the large tile.
MOSAIC = [('_View-from-River', 'View from River'), ('_Pooldeck', 'Pool deck'), ('-Night-club-Main-Floor', 'Nightclub main floor'),
          ('-RIVERSIDE-WHARF_DAYCLUB_View02b-2023-01-20', 'Day club'), ('_Exterior-view-from-street', 'Exterior view from street'),
          ('-Coastal-dining', 'Coastal dining'), ('-Night-club-Sunset-Lounge', 'Nightclub sunset lounge'), ('_Ballroom', 'Ballroom'),
          ('-AFT-Bar', 'Bar')]
renderings = section('Renderings', 'qoz-gallery', 'qoz-gallery-h', [
    El('div', 'Head', 'qoz-gallery__head', children=[
        El('p', 'Eyebrow', 'eyebrow', children=[q('QOZ Common Equity')]),
        El('h2', 'Heading', 'qoz-gallery__title', {'id': 'qoz-gallery-h'}, [q('Renderings')]),
    ]),
    El('div', 'Mosaic', 'qoz-gallery__grid', children=[
        El('figure', 'Rendering', 'qoz-gallery__tile', children=[Img('Photo', W + s, 'Riverside Wharf ' + alt), o.chip()])
        for s, alt in MOSAIC
    ]),
    o.request('Request Investor Details'),
], attrs={'id': 'renderings'})


# Opportunity Zones Program Explained (driftwoodcapital.com), block by block.
def blocks(heading, cls='qoz-prose'):
    return El('div', 'Text', cls, children=[oz_src.el(b) for b in oz_src.section(heading)])


def h3(text, cls):
    return El('h3', 'Heading', cls, children=[oz_src.copy(text)])


TITLE = 'Opportunity Zones Program Explained'
intro = section('QOZ 2.0', 'qoz-intro', 'qoz-intro-h', [
    El('div', 'Head', 'qoz-intro__head', children=[
        El('p', 'Eyebrow', 'eyebrow eyebrow--dark', children=[oz_src.copy(TITLE)]),
        El('h2', 'Heading', 'qoz-intro__title', {'id': 'qoz-intro-h'}, [oz_src.copy('A practical overview of Opportunity Zone investing')]),
        El('p', 'Byline', 'qoz-intro__byline', children=[oz_src.copy('Driftwood Capital')]),
    ]),
    El('div', 'Columns', 'qoz-intro__grid', children=[
        El('div', 'Column', 'qoz-intro__col', children=[h3(t, 'qoz-intro__subtitle'), blocks(t, 'qoz-prose qoz-prose--dark')])
        for t in ('Executive summary: How Opportunity Zone investing works after QOZ 2.0', 'About Opportunity Zones')
    ]),
], attrs={'id': 'qoz'})

MECH = 'The Core Mechanics: How the Tax Benefits Work'
mech = oz_src.section(MECH)  # two paragraphs, the "basic sequence" line, the five steps
steps = section('How it works', 'qoz-steps', 'qoz-steps-h', [
    El('h2', 'Heading', 'qoz-steps__title', {'id': 'qoz-steps-h'}, [oz_src.copy(MECH)]),
    El('div', 'Text', 'qoz-prose qoz-steps__lede', children=[oz_src.el(b) for b in mech[:2]]),
    oz_src.el(mech[2], 'qoz-steps__lead', 'Sequence'),
    oz_src.el(mech[3], 'qoz-steps__list', 'Steps'),
])

GAINS, NOTE = 'Eligible Gains', 'What Investors May Want to Note'
gains_src = oz_src.section(GAINS)
gains = section('Eligible gains', 'qoz-gains', 'qoz-gains-h', [
    El('div', 'Columns', 'qoz-gains__grid', children=[
        El('div', 'Eligible gains', 'qoz-gains__card', children=[
            El('h2', 'Heading', 'qoz-gains__title', {'id': 'qoz-gains-h'}, [oz_src.copy(GAINS)]),
            oz_src.el(gains_src[0], 'qoz-gains__text', 'Text'),
            oz_src.el(gains_src[1], 'qoz-gains__list', 'List'),
        ]),
        El('div', 'Notes', 'qoz-gains__notes', children=[
            h3(NOTE, 'qoz-gains__title'),
            *[oz_src.el(b, 'qoz-note', 'Note') for b in oz_src.section(NOTE)],
        ]),
    ]),
])

CHANGED = 'What Changed: QOZ 1.0 vs. QOZ 2.0'
changed_src = oz_src.section(CHANGED)  # two paragraphs, then the table's scroll wrapper
table = next(c for c in changed_src[2][2] if not isinstance(c, str) and c[0] == 'table')
compare = section('QOZ 1.0 vs. QOZ 2.0', 'qoz-compare', 'qoz-compare-h', [
    El('h2', 'Heading', 'qoz-compare__title', {'id': 'qoz-compare-h'}, [oz_src.copy(CHANGED)]),
    El('div', 'Rules', 'qoz-compare__rules', children=[oz_src.el(changed_src[0], 'qoz-rule', 'Original rules'),
                                                       oz_src.el(changed_src[1], 'qoz-rule qoz-rule--new', 'New rules')]),
    El('div', 'Table scroll', 'qoz-compare__scroll', {'tabindex': '0', 'role': 'region', 'aria-label': oz_src.copy('QOZ 1.0 and QOZ 2.0 comparison')},
       [oz_src.el(table, 'qoz-table', 'Comparison')]),
])

HOSP = 'The Opportunity Zone Advantage for Hospitality Assets'
hosp = oz_src.section(HOSP)
# Its last paragraph ends "To learn more, visit our offering page here." (a link to this offering): left out here.
LAST = (hosp[3][0], hosp[3][1], [c for c in hosp[3][2] if isinstance(c, str) or c[0] != 'strong'])
hospitality = section('Hospitality', 'qoz-hospitality', 'qoz-hospitality-h', [
    El('div', 'Row', 'media-split', children=[
        El('figure', 'Image', 'media-card qoz-hospitality__media', children=[Img('Photo', W + '_Complex', 'Riverside Wharf Complex'), o.chip()]),
        El('div', 'Copy', 'media-split__copy', children=[
            El('h2', 'Heading', 'qoz-hospitality__title', {'id': 'qoz-hospitality-h'}, [oz_src.copy(HOSP)]),
            El('div', 'Text', 'qoz-prose', children=[oz_src.el(b) for b in hosp[:3]] + [oz_src.el(LAST)]),
            o.request('Request Investor Details'),
        ]),
    ]),
])

notes = oz_src.endnotes()
summary = section('Summary', 'qoz-summary', 'qoz-summary-h', [
    El('div', 'Card', 'qoz-summary__card', children=[
        El('h2', 'Heading', 'qoz-summary__title', {'id': 'qoz-summary-h'}, [oz_src.copy('Summary')]),
        blocks('Summary'),
    ]),
    El('div', 'Endnotes', 'footnotes qoz-endnotes', children=[
        h3('Sources and endnotes', 'qoz-endnotes__title'),
        El('ol', 'Endnotes', 'qoz-endnotes__list', children=[oz_src.el(notes[n], None, 'Endnote', {'id': f'oz-note-{n}'}) for n in sorted(notes)]),
        *[oz_src.el(b) for b in oz_src.section('Sources and endnotes') if b[0] == 'p'],  # the article's disclaimer
    ]),
])


STYLESHEETS = ['shared', 'offering']  # + this page's site/styles/offering_rw_qoz.css
PAGE = [
    o.hero('QOZ Common Equity', 'Dream_Website_banner', 'Riverside-Wharf_View-from-River', 'Riverside Wharf Miami rendering video', badge='Coming soon'),
    facts,
    o.subnav(SUBNAV),
    o.overview('Riverside-Wharf_Pooldeck', 'Riverside Wharf Pool deck', 'A hospitality & entertainment development', [
        ['This two tower project', '1', ', a rooftop day club', '2', '.'], ['Designed to foster'], ['Located in a market'],
        ['The project is structured with the objective of generating cash flows', '3', '.']],
        ['1 Profile Magazine', '2 These project descriptions', '3 Such benefits', 'All information is as of the date indicated',
         'Nothing herein constitutes an offering of securities. All information provided is for informational purposes only and should not be deemed as advice in relation to legal, taxation, financial or investment matters. The description of the project']),
    renderings,
    # No poster in the design (empty image slot): the frame shows the play button on the dark band until clicked.
    o.webinar('https://player.vimeo.com/video/1073671948?byline=0&title=0&autoplay=1', 'Riverside Wharf Miami video'),
    oz,
    intro, steps, gains, compare, hospitality, summary,
    o.partners(),
    o.structure(STACK, HIGHLIGHTS, STRUCTURE_NOTES),
    o.market(MARKET, MARKET_NOTES),
    o.legal(),
    o.cta(),
]

# Design copy this teaser leaves out (Alex, 2026-10-09: teaser + reservation form): the "[TBD]" target metrics (both
# metric bands, their footnotes and disclaimer link), the two placeholder highlights, and the design's request-button
# labels, all replaced by RESERVE ("Download Brochure" too: the site never hosts a brochure, CLAUDE.md rule 7).
# Bring a section back by putting it on the page and taking its strings off this list.
DROPPED_COPY = {q(t) for t in ('[TBD]', 'Target*', 'Net Quarterly Distributions', 'Net Equity Multiple', 'Minimum Investment',
                               'Assumed Hold Period', 'Targeted preferred return anticipated', 'The minimum investment amount',
                               'The anticipated hold period', '* Target internal rate of return', 'Click here to see important disclaimers',
                               '[QOZ highlight', 'Target Metrics*', 'Request Offering Details', 'Request Information',
                               'Request Investor Details', 'Download Brochure', 'Start Investing',
                               'QOZ Common Equity Target Metrics', '* 1', '[QOZ target summary')}
# Alex, 2026-10-09: "Remove program, and rationale for now. This page should enhance the oz information." Both sections
# stay defined above; their strings that appear nowhere else on the page are dropped.
DROPPED_COPY |= ({norm(t) for t in all_texts([program, rationale])} & set(q.all)) - {norm(t) for t in all_texts(PAGE)}

# Not design copy: the arrow, the reserve label (Alex), the sub-nav labels (design script data) and the program tab labels (design script data).
NON_DESIGN = {'→', RESERVE} | {label for label, _ in SUBNAV} | {label for label, _ in GALLERIES}
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
