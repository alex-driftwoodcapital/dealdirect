"""EB-5 Investments (/eb-5-investments/): Etch build of handoff/design/EB-5 Investments.dc.html.
Section order, anchors and copy follow the design; every string comes from the design file via q().
Header, footer and the registration dialog are site-wide pieces built separately: CTAs that open the
dialog carry data-modal-open="eb5-register"."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
from etch import El, Img, section
from design import Copy

DESIGN = os.path.join(os.path.dirname(__file__), '..', '..', 'handoff', 'design', 'EB-5 Investments.dc.html')
q = Copy(DESIGN)
ARROW = El('span', 'Arrow', attrs={'aria-hidden': 'true'}, children=['→'])


def link(text, href, name='Link'):
    return El('a', name, 'link-arrow', {'href': href}, [text, ARROW])


def stat(value_children, label, name='Stat'):
    # dt first for valid <dl> grouping; CSS shows the value on top (column-reverse).
    return El('div', name, 'stat-card', children=[
        El('dt', 'Label', 'stat-card__label', children=[label]),
        El('dd', 'Value', 'stat-card__value', children=value_children),
    ])


def sup(n):
    return El('sup', 'Footnote ref', children=[n])


hero = section('Hero', 'eb-hero', 'eb-hero-h', [
    Img('Hero image', 'eb5-family-flag-front', '', loading='eager'),
    El('div', 'Veil', 'eb-hero__veil', {'aria-hidden': 'true'}),
    El('div', 'Copy', 'eb-hero__copy', children=[
        El('p', 'Eyebrow', 'eyebrow eyebrow--dark', children=[q('EB-5 Investment')]),
        El('h1', 'Heading', 'eb-hero__title', {'id': 'eb-hero-h'}, [q('Riverside Wharf Miami')]),
    ]),
])

BENEFITS = [
    ('Clear path to U.S. citizenship', 'EB-5 investors, spouses'),
    ('No sponsorship required', 'Unlike other visa categories'),
    ('Live, work & study anywhere', 'No restrictions on where'),
    ('Access to top U.S. education', 'Investors’ children can attend'),
]
benefits = section('Benefits', 'eb-benefits', 'eb-benefits-h', [
    El('h2', 'Heading', 'eb-benefits__title', {'id': 'eb-benefits-h'}, [q('Access the path to U.S. Citizenship')]),
    El('div', 'Row', 'eb-benefits__row', children=[
        El('figure', 'Image', 'media-card', children=[Img('Passports', 'eb5-passports', 'U.S. passports')]),
        El('div', 'List column', 'eb-benefits__col', children=[
            El('ul', 'Benefits', 'eb-benefits__list', children=[
                El('li', 'Benefit', 'eb-benefits__item', children=[
                    El('h3', 'Title', 'eb-benefits__item-title', children=[q(t)]),
                    El('p', 'Text', children=[q(b)]),
                ]) for t, b in BENEFITS
            ]),
            link(q('Learn more about the EB-5 Program'), '#program'),
        ]),
    ]),
])


def req_card(title, intro, items, closing):
    return El('article', title, 'card-light eb-reqs__card', children=[
        El('h3', 'Title', 'eb-reqs__title', children=[q(title)]),
        El('p', 'Intro', children=[q(intro)]),
        El('ul', 'List', 'eb-reqs__list', children=[
            El('li', 'Item', children=[El('strong', 'Term', children=[q(term)]), ' ' + q(rest)]) for term, rest in items
        ]),
        El('p', 'Closing', children=[q(closing)]),
    ])


reqs = section('Requirements', 'eb-reqs', None, [
    El('div', 'Cards', 'eb-reqs__grid', children=[
        req_card('Investment Requirement', 'To participate in the EB-5 program',
                 [('$800,000', '– If the investment is in a Targeted'), ('$1,050,000', '– If the investment is in a non-TEA')],
                 'Investment funds must remain'),
        req_card('Job Creation Requirement', 'Each EB-5 investment must create',
                 [('Direct Jobs', '– Created by the business'), ('Indirect & Induced Jobs', '– Applicable only for investments')],
                 'Job creation must be documented'),
    ]),
    link(q('Learn more about the EB-5 Visa Classification'),
         'https://www.uscis.gov/working-in-the-united-states/permanent-workers/employment-based-immigration-fifth-preference-eb-5/about-the-eb-5-visa-classification'),
], tag='div')

offerings = section('Available offerings', 'eb-offerings', 'offerings-h', [
    El('h2', 'Heading', 'eb-offerings__title', {'id': 'offerings-h'}, [q('Available Offerings')]),
    El('article', 'Riverside Wharf EB-5', 'eb-project', children=[
        El('div', 'Media', 'eb-project__media', children=[
            # Poster only: the Vimeo background video (1079927883) needs an iframe, not yet confirmed in Etch (guardrails gaps).
            Img('Rendering', 'Riverside-Wharf_View-from-River', 'Riverside Wharf View from River'),
            El('div', 'Chips', 'eb-project__chips', children=[
                El('span', 'Chip', 'chip chip--glass', children=[q('EB-5 Project')]),
                El('span', 'Chip', 'chip chip--glass', children=[q('Directly from Sponsor')]),
            ]),
            El('span', 'Rendering chip', 'chip chip--glass eb-project__rendering', children=[q('Rendering')]),
        ]),
        El('div', 'Body', 'eb-project__body', children=[
            El('h3', 'Title', 'eb-project__title', children=[q('Riverside Wharf Miami — A transformative')]),
            El('p', 'Summary', 'eb-project__summary', children=[q('A mixed-use development poised')]),
            El('dl', 'Metrics', 'eb-project__stats', children=[
                stat([q('2%* Target')], q('Annual Rate EB-5 Debt')),
                stat([q('6% Target*')], q('Annual Rate EB-5 Equity')),
                stat([q('$800,000 USD'), sup('1')], q('Investment Amount')),
                stat([q('3-5 Years')], q('Expected Investment Duration')),
            ]),
            El('button', 'Download brochure', 'button button--primary', {'type': 'button', 'data-modal-open': 'eb5-register'}, [q('Download Brochure')]),
        ]),
    ]),
    El('div', 'Footnotes', 'footnotes', children=[El('p', 'Footnote', children=[q('1. Applies to EB-5 projects in a TEA')])]),
], attrs={'id': 'offerings'})

program = section('EB-5 program', 'eb-program', 'program-h', [
    El('div', 'Row', 'eb-program__row', children=[
        El('div', 'Copy', 'eb-program__copy', children=[
            El('h2', 'Heading', 'eb-program__title', {'id': 'program-h'}, [q('What is the EB-5 program?')]),
            El('h3', 'Subheading', 'eb-program__sub', children=[q('What is the EB-5 Program?')]),
            El('p', 'Text', children=[q('The United States Congress created')]),
            El('p', 'Text', children=[q('Through the EB-5 investment')]),
            link(q('Learn more about the EB-5 immigrant investor program'), 'https://www.uscis.gov/working-in-the-united-states/permanent-workers/eb-5-immigrant-investor-program'),
        ]),
        El('figure', 'Image', 'media-card', children=[Img('Green card', 'eb5-green-card', 'U.S. Permanent Resident Card on an American flag')]),
    ]),
], attrs={'id': 'program'})

STEPS = [('Start', 'Investor retains'), ('Month 1', 'Investor subscribes'), ('Months 2-24', 'USCIS reviews the I-526'),
         ('Year 2+', 'Approved investors'), ('Year 3+', 'If the I-829 Petition')]
process = section('Immigration timeline', 'eb-process', 'process-h', [
    El('h2', 'Heading', 'eb-process__title', {'id': 'process-h'}, [q('Illustrative EB-5 Immigration Timeline')]),
    El('ol', 'Steps', 'eb-process__steps', children=[
        El('li', 'Step', 'eb-process__step', children=[
            El('span', 'Dot', 'eb-process__dot', {'aria-hidden': 'true'}),
            El('p', 'When', 'eb-process__when', children=[q(when)]),
            El('p', 'Text', children=[q(text)]),
        ]) for when, text in STEPS
    ]),
    El('p', 'Footnote', 'footnotes footnotes--dark', children=[q('Actual timeline will vary')]),
])

POINTS = ['Money back guarantee', 'Most projects qualify', 'Job creation verified', 'Driftwood has historically', 'Dedicated Investor Relations']


def platform(value_children, label, ref):
    return El('div', 'Stat', 'stat-card stat-card--tall', children=[
        El('p', 'Value', 'stat-card__value', children=value_children),
        El('p', 'Label', 'stat-card__label', children=[label, sup(ref)]),
    ])


driftwood = section('Driftwood Capital', 'eb-direct', 'driftwood-h', [
    El('div', 'Intro', 'eb-direct__intro', children=[
        El('h2', 'Heading', 'eb-direct__title', {'id': 'driftwood-h'}, [q('Benefits of investing directly')]),
        El('p', 'Lede', 'eb-direct__lede', children=[q('EB-5 Projects directly from the developer')]),
    ]),
    El('div', 'Row', 'eb-direct__row', children=[
        El('ol', 'Benefits', 'eb-direct__list', children=[
            El('li', 'Point', 'eb-direct__item', children=[
                El('span', 'Number', 'eb-direct__num', {'aria-hidden': 'true'}, [f'{i}.']),
                El('span', 'Text', children=[q(p)]),
            ]) for i, p in enumerate(POINTS, 1)
        ]),
        # Platform figures come from WP Admin > Platform stats (CLAUDE.md rule 8), never typed here.
        El('div', 'Platform stats', 'eb-direct__stats', children=[
            platform(['{options.acf.years_experience}', ' ' + q('Years')], q('Years of History'), '1'),
            platform(['{options.acf.properties}'], q('Hotels Owned/ Managed'), '2'),
            platform(['{options.acf.aum}'], q('Hospitality Assets Under Management'), '2'),
            platform(['±', '{options.acf.employees.numberFormat()}'], q('Employees'), '2'),
        ]),
    ]),
    El('div', 'Footnotes', 'footnotes', children=[
        El('p', 'Footnote 1', children=[q('1. The founders and principals')]),
        El('p', 'Footnote 2', children=[q('2. Includes hotels and employees') + ' ', '{options.acf.as_of}', q('.')]),
    ]),
], attrs={'id': 'driftwood'})

TRACK = [  # handoff design data (name, location, investors, raised, jobs, status, alt, image file)
    ('Residence Inn Miami West/ FL Turnpike', 'Miami, FL', '18', '$9,000,000', '10 Jobs', 'Operating', 'Marriott Residence Inn Miami', 'Marriott-Residence-Inn-Miami-'),
    ('Home2 Suites by Hilton Fort Lauderdale Downtown', 'Ft. Lauderdale, FL', '36', '$18,000,000', '17 Jobs', 'Operating', 'Tru & Home2 Suites by Hilton', 'tru-home2'),
    ('Canopy by Hilton West Palm Beach Downtown', 'West Palm Beach, FL', '46', '$23,000,000', '14 Jobs', 'Operating', 'Canopy by Hilton', 'canopy-wpb'),
    ('Canopy by Hilton Tempe Downtown', 'Tempe, AZ', '52', '$26,000,000', '20 Jobs', 'Operating', 'Canopy by Hilton', 'canopy-tempe'),
    ('Element Melbourne Oceanfront', 'Melbourne, FL', '9', '$4,500,000', '17 Jobs', 'Operating', 'Element Melbourne Oceanfront', 'element-melbourne'),
    ('Staybridge Suites Wilmington Downtown, an IHG Hotel', 'Wilmington, DE', '9', '$7,200,000', '26 Jobs', 'Operating', 'Staybridge Suites Wilmington', 'StaybridgeSuites_Wilmington_EXT'),
]


def tile(name, loc, investors, raised, jobs, status, alt, media):
    m = lambda v, label: El('div', label, 'tile__metric', children=[
        El('dt', 'Label', 'tile__metric-label', children=[label]), El('dd', 'Value', 'tile__metric-value', children=[v])])
    return El('li', name, 'tile', children=[
        Img('Photo', media, alt),
        El('div', 'Veil', 'tile__veil', {'aria-hidden': 'true'}),
        El('span', 'Status', 'chip chip--light tile__chip', children=[status]),
        El('div', 'Body', 'tile__body', children=[
            El('h3', 'Name', 'tile__title', children=[name]),
            El('dl', 'Metrics', 'tile__metrics', children=[
                m(investors, q('Number of Investors')), m(raised, q('EB-5 Capital Raised')),
                m(jobs, q('Created per Investor')), m(loc, q('Location')),
            ]),
        ]),
    ])


track = section('Prior EB-5 projects', 'eb-track', 'track-h', [
    El('h2', 'Heading', 'eb-track__title', {'id': 'track-h'}, [q('Prior EB-5 Projects')]),
    El('ul', 'Projects', 'eb-track__grid', children=[tile(*t) for t in TRACK]),
    El('p', 'Footnote', 'footnotes', children=[q('To date, all six (6)')]),
])

FAQ = ['What is the investment process', 'How long does it take', 'Is it possible to include my family', 'Can I live and work anywhere',
       'What happens if my business venture', 'What is a Regional Center', 'Can I invest directly', 'What is the difference between direct',
       'What is conditional permanent residency', 'Can I work in the U.S. while']
ANSWERS = [None, 'The time it takes', 'Yes, the spouse', 'Yes, once you obtain', 'If the business project', 'A Regional Center is',
           'Yes, direct investment is possible', 'Direct investments require', 'It’s a two-year residency', 'You may need to obtain']
FIRST_STEPS = ['Identify and select', 'Make the capital investment', 'If the application is approved', 'Obtain a conditional', 'File Form I-829']


def faq_item(i):
    if ANSWERS[i] is None:
        answer = [El('p', 'Text', children=[q('The investment process in the EB-5 program generally')]),
                  El('ul', 'Steps', children=[El('li', 'Step', children=[q(s)]) for s in FIRST_STEPS])]
    else:
        answer = [El('p', 'Text', children=[q(ANSWERS[i])])]
    attrs = {'open': ''} if i == 0 else {}
    return El('details', 'Question', 'faq', attrs, [
        El('summary', 'Summary', 'faq__q', children=[q(FAQ[i]), El('span', 'Icon', 'faq__icon', {'aria-hidden': 'true'}, ['+'])]),
        El('div', 'Answer', 'faq__a', children=answer),
    ])


faq = section('FAQ', 'eb-faq', 'faq-h', [
    El('div', 'Grid', 'eb-faq__grid', children=[
        El('h2', 'Heading', 'eb-faq__title', {'id': 'faq-h'}, [q('Frequently Asked Questions')]),
        El('div', 'Questions', 'eb-faq__list', children=[faq_item(i) for i in range(len(FAQ))]),
    ]),
    El('p', 'Disclaimer', 'footnotes', children=[q('Nothing stated herein')]),
])

legal = section('Legal', 'legal-block', 'legal-h', [
    El('h2', 'Heading', 'legal-block__title', {'id': 'legal-h'}, [q('Legal disclosure')]),
    El('p', 'Text', children=[q('This website is not an offer')]),
    El('h2', 'Heading', 'legal-block__title', children=[q('* Target Returns')]),
    El('p', 'Text', children=[q('The target returns shown')]),
    El('p', 'Text', children=[q('Note the targeted returns')]),
    El('h2', 'Heading', 'legal-block__title', children=[q('Renderings')]),
    El('p', 'Text', children=[q('This document contains artist')]),
], attrs={'id': 'legal'})

cta = section('Get started', 'cta-band', 'cta-h', [
    El('div', 'Card', 'cta-band__card', children=[
        Img('Background', 'eb5-flag-wood-wide', ''),
        El('div', 'Scrim', 'cta-band__scrim', {'aria-hidden': 'true'}),
        El('div', 'Copy', 'cta-band__copy', children=[
            El('h2', 'Heading', 'cta-band__title', {'id': 'cta-h'}, [q('Ready to get started?')]),
            El('p', 'Text', 'cta-band__text', children=[q('Join our network of accredited')]),
        ]),
        El('a', 'Start investing', 'button button--white', {'href': '/#signup'}, [q('Start Investing')]),
    ]),
])

PAGE = [hero, benefits, reqs, offerings, program, process, driftwood, track, faq, legal, cta]

# Strings on the page that are not design copy: arrows, numbering, the approx sign the design's <dw-stat approx> renders,
# and the prior-project data from the design script.
NON_DESIGN = {'→', '+', '±', '1', '2', '1.', '2.', '3.', '4.', '5.'} | {v for t in TRACK for v in t[:6]}
# slug -> (source, Etch Asset Manager collection). Source: a file in handoff/design/assets/ or a live-site upload URL.
MEDIA = {
    'eb5-family-flag-front': ('handoff/design/assets/eb5/eb5-family-flag-front.webp', 'EB-5'),
    'eb5-passports': ('handoff/design/assets/eb5/eb5-passports.webp', 'EB-5'),
    'eb5-green-card': ('handoff/design/assets/eb5/eb5-green-card.webp', 'EB-5'),
    'eb5-flag-wood-wide': ('handoff/design/assets/eb5/eb5-flag-wood-wide.webp', 'EB-5'),
    'Riverside-Wharf_View-from-River': ('https://driftwooddealdirect.com/wp-content/uploads/Riverside-Wharf_View-from-River.jpg', 'Riverside Wharf'),
    'Marriott-Residence-Inn-Miami-': ('https://driftwooddealdirect.com/wp-content/uploads/Marriott-Residence-Inn-Miami-.jpeg', 'Prior Projects'),
    'tru-home2': ('https://driftwooddealdirect.com/wp-content/uploads/tru-home2.jpg', 'Prior Projects'),
    'canopy-wpb': ('https://driftwooddealdirect.com/wp-content/uploads/canopy-wpb.jpg', 'Prior Projects'),
    'canopy-tempe': ('https://driftwooddealdirect.com/wp-content/uploads/canopy-tempe.jpg', 'Prior Projects'),
    'element-melbourne': ('https://driftwooddealdirect.com/wp-content/uploads/element-melbourne.jpg', 'Prior Projects'),
    'StaybridgeSuites_Wilmington_EXT': ('https://driftwooddealdirect.com/wp-content/uploads/StaybridgeSuites_Wilmington_EXT.jpg', 'Prior Projects'),
}

META = {'title': 'EB-5 Investments', 'slug': 'eb-5-investments', 'status': 'publish'}  # frozen permalink /eb-5-investments/ (handoff/docs/permalinks.md)
