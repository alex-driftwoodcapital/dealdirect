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
from offering import Offering, MARKET, MARKET_NOTES, METRIC_NOTES, UP, COMMON_EQUITY, sup
import market_update

DESIGN = os.path.join(os.path.dirname(__file__), '..', '..', 'handoff', 'design', 'Riverside Wharf QOZ.dc.html')
q = Copy(DESIGN)
RESERVE = 'Reserve Your Spot'  # Alex, 2026-10-09 ("reserve their spot using the form"); compliance to confirm the wording
o = Offering(q, cta=RESERVE)
ARTICLE = os.path.join(os.path.dirname(__file__), '..', 'sources', 'driftwoodcapital-opportunity-zones-program-explained.html')
oz_src = Article(ARTICLE, "<div id='inner_content", '<footer id="main-footer"', 'oz-note-', 'oz-ref-')
COPY_EXTRA = [oz_src.copy, market_update.COPY]  # + Alex's market update (site/sources/riverside-wharf-market-update.html)

METRICS = [  # (value, qualifier, label, footnote ref, accent): values are the design's [TBD] placeholders
    ('[TBD]', 'Target*', 'Net Quarterly Distributions', '1', True),
    ('[TBD]', 'Target*', 'Net Equity Multiple', None, False),
    ('[TBD]', None, 'Minimum Investment', '2', False),
    ('[TBD]', None, 'Assumed Hold Period', '3', False),
]
STACK = [  # the common-equity layer is this offering's highlight; the others are muted
    ('~$96M', COMMON_EQUITY, '100%', 'cap-stack__layer--highlight cap-stack__layer--lead'),
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
SUBNAV = [('Overview', 'overview'), ('Video', 'webinar'), ('Renderings', 'renderings'), ('QOZ 2.0', 'qoz'),
          ('Partners', 'partners'), ('Offering', 'offering'), ('Market', 'market'), ('Market update', 'market-update'), ('Legal', 'legal')]

IRS = 'https://www.irs.gov/credits-deductions/businesses/opportunity-zones'
OZ_BENEFITS = [('Capital Gain Exclusion:', 'For qualifying investments held for 10 years'),
               ('Tax Deferral and Recognition:', 'The Opportunity Zone framework allows')]
# The design's OZ benefits section (o.oz), as one part of the QOZ section below: same classes and copy, its title in
# the part's summary, its own footnote (the IRS link) inside it so its "1" doesn't mix with the article's endnotes.
OZ_TITLE = [q('Potential Opportunity Zone tax incentives'), sup('1')]
oz_benefits = [
    El('div', 'Row', 'offering-oz__row', children=[
        El('div', 'Copy', 'offering-oz__copy', children=[
            El('p', 'Intro', 'offering-oz__intro', children=[q('Established under the 2017 Tax Cuts and Jobs Act')]),
            El('div', 'Benefits', 'offering-oz__benefits', children=[
                El('div', 'Benefit', 'offering-oz__benefit', children=[
                    El('strong', 'Title', 'offering-oz__benefit-title', children=[q(t)]), El('p', 'Text', children=[q(b)])])
                for t, b in OZ_BENEFITS]),
        ]),
        El('figure', 'Image', 'media-card offering-oz__media', children=[
            Img('Photo', 'Riverside-Wharf_Dream-Hotel-Prefunction', 'Riverside Wharf Dream Hotel Pre-function'), o.chip()]),
    ]),
    o.footnotes('Footnotes', [El('p', 'Footnote', children=[sup('1'), q('Information is for illustrative purposes only') + ' ',
                                                           El('a', 'IRS link', attrs={'href': IRS}, children=[q(IRS)]), q('.')]),
                              o.fn(None, 'This webpage is a preliminary summary for discussion purposes only and does not contain all material information. Nothing herein constitutes tax advice')]),
]


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

# Renderings, placed with the content instead of one big grid (Alex, 2026-10-09: "use the renderings strategically across
# the page not a massive grid, then below the video we can have a nice carousel to save space"): the hero (view from the
# river), the overview (pool deck), the carousel under the video (the program's spaces, each captioned with its design
# category), the OZ and hospitality parts (pre-function, complex), the partners (lobby, coastal bar), a wide aerial before
# the market section and the riverfront F&B scene in the market update. Nothing is shown twice.
P = '-2023-05-25_ICRAVE_THE-WHARF-FB_100-DD-PRESENTATION-'
CAROUSEL = [  # (suffix, alt, design gallery category)
    ('_Exterior-view-from-street', 'Exterior view from street', 'Hotel'), (P + '22', 'Hotel', 'Hotel'),
    ('-Coastal-dining', 'Coastal dining', 'Restaurants'), ('-AFT-show-kitchen', 'Show kitchen', 'Restaurants'),
    ('-AFT-Bar', 'Bar', 'Restaurants'), ('_Dream-Hotel-Wine-Bar', 'Dream Hotel wine bar', 'Restaurants'),
    ('-RIVERSIDE-WHARF_DAYCLUB_View02b-2023-01-20', 'Day club', 'Entertainment'), ('-Night-club-Main-Floor', 'Nightclub main floor', 'Entertainment'),
    ('-Night-club-Sunset-Lounge', 'Nightclub sunset lounge', 'Entertainment'), (P + '15', 'Entertainment', 'Entertainment'),
    (P + '10', 'Entertainment', 'Entertainment'), (P + '40', 'Entertainment', 'Entertainment'),
    ('_Ballroom', 'Ballroom', 'Conference'),
]
# a strip under the webinar video, same section (Alex, 2026-10-09: "I want these as a strip below the video")
renderings = o.strip([(W + s, 'Riverside Wharf ' + alt, cat) for s, alt, cat in CAROUSEL], 'Riverside Wharf renderings')
aerial = o.rendering_band(W + '_View-from-exterior', 'Riverside Wharf view from exterior')
market_scene = El('figure', 'Image', 'media-card market-update__media', children=[
    Img('Photo', W + P + '33', 'Riverside Wharf food and beverage venue'), o.chip()])


# All QOZ content in one section (#qoz; Alex, 2026-10-09: "All qoz should be in the same section", "Whatever can be on
# a drop down or accordion do it. We need to optimize space. Don't do a toc column"): the article's title and its
# executive summary stay open as the lead; every other part is a native <details> accordion (the EB-5 FAQ's classes),
# its heading an anchored h3 in the summary; the article's disclaimer stays visible under them. Parts: the design's OZ
# benefits and "Opportunity Zones Program Explained" (driftwoodcapital.com) block by block.
TITLE = 'Opportunity Zones Program Explained'
EXEC, ABOUT = 'Executive summary: How Opportunity Zone investing works after QOZ 2.0', 'About Opportunity Zones'
MECH, GAINS, NOTE = 'The Core Mechanics: How the Tax Benefits Work', 'Eligible Gains', 'What Investors May Want to Note'
CHANGED, HOSP = 'What Changed: QOZ 1.0 vs. QOZ 2.0', 'The Opportunity Zone Advantage for Hospitality Assets'
SUMMARY, SOURCES = 'Summary', 'Sources and endnotes'
ICON = '+'

ACC_SCRIPT = """// qoz accordions: a link to something inside a closed part (footnote marks, endnotes and their back-links, #structure)
// opens that part before the browser scrolls to it. Scoped to the QOZ section; without it the parts still open by hand.
const qoz = document.getElementById('qoz');
if (qoz) {
  const reveal = (id) => {
    const t = id && document.getElementById(id);
    if (!t || !qoz.contains(t)) return;
    for (let d = t.closest('details'); d; d = d.parentElement && d.parentElement.closest('details')) d.open = true;
  };
  const fromHash = (h) => { try { return decodeURIComponent(h.slice(1)); } catch (_) { return ''; } };
  document.addEventListener('click', (e) => {
    const a = e.target.closest('a[href^="#"]');
    if (a) reveal(fromHash(a.getAttribute('href')));
  });
  window.addEventListener('hashchange', () => reveal(fromHash(location.hash)));
  reveal(fromHash(location.hash));
}
"""


def blocks(heading, cls='qoz-prose'):
    return El('div', 'Text', cls, children=[oz_src.el(b) for b in oz_src.section(heading)])


def part(anchor, title, body, attrs=None):
    """One accordion part: the heading (h3, anchored) in the summary, the body below."""
    return El('details', 'Part', 'faq qoz-acc', {'id': anchor, **(attrs or {})}, [
        El('summary', 'Summary', 'faq__q qoz-acc__q', children=[
            El('h3', 'Heading', 'qoz-acc__title', children=title),
            El('span', 'Icon', 'faq__icon', {'aria-hidden': 'true'}, [ICON]),
        ]),
        El('div', 'Body', 'qoz-acc__body', children=body),
    ])


head = El('div', 'Head', 'qoz-head', children=[
    El('p', 'Eyebrow', 'eyebrow', children=[oz_src.copy(TITLE)]),
    El('h2', 'Heading', 'qoz-head__title', {'id': 'qoz-h'}, [oz_src.copy('A practical overview of Opportunity Zone investing')]),
    El('p', 'Byline', 'qoz-head__byline', children=[oz_src.copy('Driftwood Capital')]),
])
lead = El('div', 'Executive summary', 'qoz-intro', {'id': 'qoz-executive-summary'}, [
    El('h3', 'Heading', 'qoz-intro__subtitle', children=[oz_src.copy(EXEC)]),
    blocks(EXEC, 'qoz-prose qoz-prose--dark'),
])

mech = oz_src.section(MECH)  # two paragraphs, the "basic sequence" line, the five steps
gains_src = oz_src.section(GAINS)
changed_src = oz_src.section(CHANGED)  # two paragraphs, then the table's scroll wrapper
table = next(c for c in changed_src[2][2] if not isinstance(c, str) and c[0] == 'table')


def els(node):
    return [k for k in node[2] if not isinstance(k, str)]


# Quick comparison (Alex, 2026-10-09: "a quick easy comparison between oz 1.0 and 2.0, a quick summary besides the
# content"): the article's own QOZ 1.0 / QOZ 2.0 table, always visible under the executive summary. Each cell carries its
# column header as data-label, so on small screens a row stacks into a labelled card.
caption, thead, tbody = (next(c for c in els(table) if c[0] == t) for t in ('caption', 'thead', 'tbody'))
cols = [oz_src.copy(_t.strip()) for _t in (''.join(x for x in th[2] if isinstance(x, str)) for th in els(els(thead)[0]))]
quick = El('div', 'Quick comparison', 'qoz-quick', children=[
    El('table', 'Comparison', 'qoz-quick__table', children=[
        oz_src.el(caption, 'qoz-quick__caption', 'Caption'),
        oz_src.el(thead, 'qoz-quick__head', 'Head'),
        El('tbody', 'Rows', children=[
            El('tr', 'Row', 'qoz-quick__row', children=[
                oz_src.el(cell, 'qoz-quick__cell' + (' qoz-quick__cell--new' if i == 2 else ''), 'Cell',
                          {'scope': 'row'} if cell[0] == 'th' else {'data-label': cols[i]})
                for i, cell in enumerate(els(tr))])
            for tr in els(tbody)]),
    ]),
])
hosp = oz_src.section(HOSP)
# Its last paragraph ends "To learn more, visit our offering page here." (a link to this offering): left out here.
LAST = (hosp[3][0], hosp[3][1], [c for c in hosp[3][2] if isinstance(c, str) or c[0] != 'strong'])
notes = oz_src.endnotes()

parts = El('div', 'Parts', 'qoz-parts', children=[
    part('qoz-about', [oz_src.copy(ABOUT)], [blocks(ABOUT)]),
    part('structure', OZ_TITLE, oz_benefits),  # the design's #structure anchor (old sub-nav links) opens this part
    part('qoz-mechanics', [oz_src.copy(MECH)], [
        El('div', 'Text', 'qoz-prose qoz-steps__lede', children=[oz_src.el(b) for b in mech[:2]]),
        oz_src.el(mech[2], 'qoz-steps__lead', 'Sequence'),
        oz_src.el(mech[3], 'qoz-steps__list', 'Steps'),
    ]),
    part('qoz-eligible-gains', [oz_src.copy(GAINS)], [
        oz_src.el(gains_src[0], 'qoz-gains__text', 'Text'),
        oz_src.el(gains_src[1], 'qoz-gains__list', 'List'),
    ]),
    part('qoz-what-to-note', [oz_src.copy(NOTE)], [
        El('div', 'Notes', 'qoz-gains__notes', children=[oz_src.el(b, 'qoz-note', 'Note') for b in oz_src.section(NOTE)]),
    ]),
    part('qoz-what-changed', [oz_src.copy(CHANGED)], [
        # the table itself is the quick comparison above the parts
        El('div', 'Rules', 'qoz-compare__rules', children=[oz_src.el(changed_src[0], 'qoz-rule', 'Original rules'),
                                                           oz_src.el(changed_src[1], 'qoz-rule qoz-rule--new', 'New rules')]),
    ]),
    part('qoz-hospitality', [oz_src.copy(HOSP)], [
        El('div', 'Row', 'qoz-hospitality__row', children=[
            El('div', 'Text', 'qoz-prose', children=[oz_src.el(b) for b in hosp[:3]] + [oz_src.el(LAST)]),
            El('figure', 'Image', 'media-card qoz-hospitality__media', children=[Img('Photo', W + '_Complex', 'Riverside Wharf Complex'), o.chip()]),
        ]),
    ]),
    part('qoz-sources', [oz_src.copy(SOURCES)], [
        El('ol', 'Endnotes', 'qoz-endnotes__list', children=[oz_src.el(notes[n], None, 'Endnote', {'id': f'oz-note-{n}'}) for n in sorted(notes)]),
    ]),
])
qoz = section('Opportunity Zones', 'qoz-section', 'qoz-h', [
    head,
    lead,
    quick,
    parts,
    # the article's closing summary reads as the takeaway after the parts, always open (Alex, 2026-10-09: "all those
    # accordions need to make sense, we have one for 'summary'"); the accordions hold only the content parts and sources
    El('div', 'Summary', 'qoz-summary', {'id': 'qoz-summary'}, [
        El('h3', 'Heading', 'qoz-summary__title', children=[oz_src.copy(SUMMARY)]),
        blocks(SUMMARY),
    ]),
    o.request('Request Investor Details'),
    # the article's disclaimer, always visible (CLAUDE.md rule 6)
    El('div', 'Disclaimer', 'footnotes qoz-disclaimer', children=[oz_src.el(b) for b in oz_src.section(SOURCES) if b[0] == 'p']),
], attrs={'id': 'qoz'}, script=ACC_SCRIPT)

STYLESHEETS = ['shared', 'offering']  # + this page's site/styles/offering_rw_qoz.css
PAGE = [
    o.hero('QOZ Common Equity', 'Riverside-Wharf-hero', 'Riverside-Wharf_View-from-River', 'Riverside Wharf Miami rendering video', badge='Coming soon'),
    # the design's target metrics with their [TBD] placeholders (Alex, 2026-10-09: "remove these for now, keep the
    # placeholders we had" — the program figures band is off the page)
    o.metrics('QOZ Common Equity Target Metrics', '* 1', '[QOZ target summary', METRICS, METRIC_NOTES),
    o.subnav(SUBNAV),
    o.overview('Riverside-Wharf_Pooldeck', 'Riverside Wharf Pool deck', 'A hospitality & entertainment development', [
        ['This two tower project', '1', ', a rooftop day club', '2', '.'], ['Designed to foster'], ['Located in a market'],
        ['The project is structured with the objective of generating cash flows', '3', '.']],
        ['1 Profile Magazine', '2 These project descriptions', '3 Such benefits', 'All information is as of the date indicated',
         'Nothing herein constitutes an offering of securities. All information provided is for informational purposes only and should not be deemed as advice in relation to legal, taxation, financial or investment matters. The description of the project']),
    # No poster in the design (empty image slot): the frame shows the play button on the dark band until clicked.
    o.webinar('https://player.vimeo.com/video/1073671948?byline=0&title=0&autoplay=1', 'Riverside Wharf Miami video', extra=renderings),
    qoz,
    o.partners(),
    o.structure(STACK, HIGHLIGHTS, STRUCTURE_NOTES),
    aerial,
    o.market(MARKET, MARKET_NOTES),
    market_update.build(o.fn(None, MARKET_NOTES[1]), media=market_scene),
    o.legal(),
    o.cta(),
]

# Design copy this teaser leaves out (Alex, 2026-10-09: teaser + reservation form): the "[TBD]" target metrics (both
# metric bands, their footnotes and disclaimer link), the two placeholder highlights, and the design's request-button
# labels, all replaced by RESERVE ("Download Brochure" too: the site never hosts a brochure, CLAUDE.md rule 7).
# Bring a section back by putting it on the page and taking its strings off this list.
DROPPED_COPY = {q(t) for t in ('[QOZ highlight', 'Target Metrics*', 'Request Offering Details', 'Request Information',
                               'Request Investor Details', 'Download Brochure', 'Start Investing',
                               'Total equity')}  # 'Total equity': the ~$96M layer is common equity (Alex, 2026-10-09)
# Alex, 2026-10-09: "Remove program, and rationale for now. This page should enhance the oz information." Both sections
# stay defined above; their strings that appear nowhere else on the page are dropped.
DROPPED_COPY |= ({norm(t) for t in all_texts([program, rationale])} & set(q.all)) - {norm(t) for t in all_texts(PAGE)}

# Not design copy: the arrow, the reserve label (Alex), the accordion icon, the sub-nav labels (design script data) and the program tab labels (design script data).
NON_DESIGN = {'→', RESERVE, ICON} | {label for label, _ in SUBNAV} | {label for label, _ in GALLERIES}
# The ~$96M layer's label (Alex, 2026-10-09) and the market update's footnote marks and back-links.
NON_DESIGN |= {COMMON_EQUITY} | market_update.NON_DESIGN
# slug -> (source, Etch Asset Manager collection). Live-site uploads keep their filenames; images are compressed on
# import with the Etch Asset Manager preset.
MEDIA = {
    'Riverside-Wharf_View-from-River': (UP + 'Riverside-Wharf_View-from-River.jpg', 'Riverside Wharf'),
    # the live loop (Dream_Website_banner.mp4) re-encoded lighter for the web, 1080p 10.5 -> 6.4 MB (site/media/README.md)
    'Riverside-Wharf-hero': ('site/media/Riverside-Wharf-hero.mp4', 'Video'),
    'Riverside-Wharf_Pooldeck': (UP + 'Riverside-Wharf_Pooldeck.jpg', 'Riverside Wharf'),
    'Night-club-Lobby': (UP + 'Night-club-Lobby.jpg', 'Riverside Wharf'),
    'cover-bg': ('handoff/design/assets/cover-bg.png', 'Brand'),
    **{W + s: (UP + W + s + '.jpg', 'Riverside Wharf') for _, suffixes in GALLERIES for s in suffixes},
}

COPY_SOURCE = 'DealDirect Home.dc.html'  # card field values below are checked against it (copy gate)
META = {'kind': 'offering', 'title': 'Riverside Wharf Miami – QOZ Common Equity', 'slug': 'riverside-wharf-qoz', 'status': 'publish',
        'fields': {  # Home card (DealDirect Home.dc.html live data, key riverside-wharf-qoz); the summary is the design's placeholder
            'offering_status': 'coming_soon', 'offering_tag': 'QOZ', 'card_title': 'Riverside Wharf Miami',
            'card_summary': '[Summary from offering CPT]', 'card_image': '{{media:Riverside-Wharf_Pooldeck}}', 'card_cta_label': RESERVE,  # links to this teaser (Alex, 2026-10-09)
           
            'card_rendering': 1, 'home_order': 2,
        },
        # no live page of its own: title from the live pattern; og:image as live /offering/riverside-wharf/
        'seo': {'og_image': '{{media:Riverside-Wharf_View-from-River}}', 'og_image_alt': 'Riverside Wharf View from River'}}
