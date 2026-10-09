"""Driftwood Hotel Income I, DST (/offering/driftwood-hotel-income-i-dst/): an `offering` post rendered by the
single-offering template. Built from the Weston DST brochure (handoff/design/Weston DST Brochure.dc.html, sections #p1-#p11;
the landing-page handoff that came with it is handoff/design/assets/dst/HANDOFF-README.md). Every string comes from the
brochure via q(); its footnote marks are Unicode superscripts (¹, ⁴), shown as the site's footnote marks (rich()).

Alex, 2026-10-09:
- the PUBLIC version of the brochure: the institutional line ("For institutional due diligence use only…"), the page
  labels and the Cap Rate row with its footnote are left out (DROPPED_COPY);
- contacts only: the brochure's contact cards (#contact) are how visitors get in touch; no site request form here,
  every button scrolls to them;
- no accredited-investor gate (as on the other offerings).
Sections follow the handoff: hero (#p1), offering summary (#p2), acquisition criteria and investment opportunity (#p3),
brand and property (#p4), gallery (#p5), location (#p6), market (#p7), sponsor (#p8), contact (#p11), disclosures and
risk factors (#p9, #p10)."""
import os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
from etch import El, Img, Svg, section
from design import Copy, norm
from offering import Offering, sup

DESIGN = os.path.join(os.path.dirname(__file__), '..', '..', 'handoff', 'design', 'Weston DST Brochure.dc.html')
q = Copy(DESIGN, '<doc-page', '</doc-page>')
o = Offering(q)
A = 'handoff/design/assets/dst/'

# ---------- footnote marks: the brochure writes them as superscript characters inside the sentence ----------
SUPS = '⁰¹²³⁴⁵⁶⁷⁸⁹'
TO_DIGIT = str.maketrans(SUPS, '0123456789')
SPLIT = set()    # brochure strings shown split around their marks (not on the page verbatim: DYNAMIC_COPY)
PIECES = set()   # the text either side of a mark: verbatim parts of a brochure string (COPY_EXTRA)


def rich(prefix):
    """A brochure string as text + footnote-mark elements ("Leverage ¹" -> "Leverage", sup 1)."""
    s = q(prefix)
    parts = [p for p in re.split(r'\s*([' + SUPS + r']+)', s) if p]
    if len(parts) == 1:
        return [s]
    SPLIT.add(s)
    out = []
    for p in parts:
        if all(c in SUPS for c in p):
            out.append(sup(p.translate(TO_DIGIT)))
        else:
            PIECES.add(norm(p))
            out.append(p)
    return out


class _Pieces:
    all = PIECES


def notes(*pairs, extra=()):
    """Footnotes as in the brochure: bold "1." then its text; extra: unnumbered lines after them."""
    return El('div', 'Footnotes', 'footnotes dst-notes', children=[
        El('p', 'Footnote', children=[El('strong', 'Number', 'dst-notes__n', children=[q(n)]), ' ', q(t)]) for n, t in pairs
    ] + [El('p', 'Note', children=[q(t)]) for t in extra])


def band(media, alt, cls=''):
    """A full-width photo band with the brochure's soft fade into the page."""
    return El('figure', 'Photo', ('dst-band ' + cls).strip(), children=[Img('Photo', media, alt)])


def eyebrow(text, dark=False):
    return El('p', 'Eyebrow', 'eyebrow eyebrow--dark' if dark else 'eyebrow', children=[text])


# ---------- 1 · hero (#p1) ----------
CONTACT_CTA = 'Contact the offering team'   # handoff README, hero CTAs (the brochure is print, it has no buttons)
SUMMARY_CTA = 'View offering summary'
hero = section('Hero', 'dst-hero', 'dst-hero-h', [
    Img('Background', 'dst-cover-bg', '', loading='eager'),
    El('div', 'Content', 'dst-hero__content', children=[
        El('span', 'Rule', 'dst-hero__rule', {'aria-hidden': 'true'}),
        El('p', 'Eyebrow', 'dst-hero__eyebrow', children=[q('Courtyard by Marriott Fort Lauderdale Weston')]),
        El('h1', 'Heading', 'dst-hero__title', {'id': 'dst-hero-h'}, [q('Driftwood Hotel Income I, DST')]),
        El('p', 'Lede', 'dst-hero__lede', children=[q('A 176-key select-service hotel')]),
        El('div', 'Actions', 'dst-hero__actions', children=[
            El('a', 'Contact', 'button button--white', {'href': '#contact'}, [CONTACT_CTA]),
            El('a', 'Summary', 'button button--glass', {'href': '#offering'}, [SUMMARY_CTA]),
        ]),
    ]),
    El('p', 'Disclaimer', 'dst-hero__disclaimer', children=[q('DST Interests are speculative')]),
])

SUBNAV = [('Offering', 'offering'), ('Property', 'property'), ('Gallery', 'gallery'), ('Location', 'location'),
          ('Market', 'market'), ('Sponsor', 'sponsor'), ('Contact', 'contact'), ('Disclosures', 'disclosures')]

# ---------- 2 · offering summary (#p2) ----------
KPIS = [('~$23.98M', 'Max Offering'), ('~42.54%', 'Leverage'), ('6.8%', 'Year-1 Target'), ('7.0%', '5-Yr Avg.')]
TERMS = [('Property', '176-key Courtyard'), ('Market', 'South Florida'), ('Submarket', 'Miami–Fort Lauderdale'),
         ('Vehicle', 'Ownership in the 1031'), ('Strategic Exit', 'Sell the asset'), ('Sponsor Equity', 'Driftwood retains a 5%'),
         ('Year Built', '2002'), ('Last Renovated', '2024')]   # Cap Rate row left out (public version)
summary = section('Offering summary', 'dst-section dst-summary', 'offering-h', [
    band('Courtyard-Weston-1', 'Courtyard by Marriott Fort Lauderdale Weston', 'dst-band--tall'),
    El('div', 'Head', 'dst-head', children=[
        El('h2', 'Heading', 'dst-title', {'id': 'offering-h'}, [q('Driftwood Hotel Income I, DST')]),
        El('p', 'Subtitle', 'dst-subtitle', children=[q('Courtyard by Marriott Fort Lauderdale Weston')]),
    ]),
    El('ul', 'Figures', 'dst-kpis', children=[
        El('li', 'Figure', 'dst-kpi', children=[
            El('strong', 'Value', 'dst-kpi__value', children=[q(v)]),
            El('span', 'Label', 'dst-kpi__label', children=rich(l)),
        ]) for v, l in KPIS
    ]),
    El('dl', 'Terms', 'dst-terms', children=[
        El('div', 'Row', 'dst-terms__row', children=[
            El('dt', 'Label', 'dst-terms__label', children=[q(k)]),
            El('dd', 'Value', 'dst-terms__value', children=rich(v)),
        ]) for k, v in TERMS
    ]),
    notes(('1.', 'Senior mortgage of approximately'), ('2.', 'Targeted Distributions are for illustrative'), ('3.', 'The Trust is structured')),
], attrs={'id': 'offering'})

# ---------- 3 · acquisition criteria and investment opportunity (#p3) ----------
CRITERIA = ['Premium-branded select-service', 'Unencumbered by third-party', 'Multiple nonseasonal demand',
            'Opportunity for value-add ROI', 'Ability to re-license']
OPPORTUNITY = [('Sponsor Alignment', 'Driftwood Capital co-invested'), ('Diversified Demand Base', '100+ distinct accounts'),
               ('$6M Renovation', 'Required brand renovation'), ('Affluent Master-Planned Community', 'Weston, FL was recently'),
               ('Proximate to Cleveland Clinic', 'The hotel is located ~1.3 miles'), ('#1 RevPAR in Comp Set', 'The hotel has achieved 122%')]
criteria = section('Acquisition criteria', 'dst-section dst-section--alt dst-criteria', 'criteria-h', [
    band('Courtyard-Weston-2', 'The bistro and market'),
    El('h2', 'Heading', 'dst-title dst-title--m', {'id': 'criteria-h'}, [q('Driftwood Capital Acquisition Criteria for DSTs')]),
    El('ul', 'Criteria', 'dst-bullets', children=[El('li', 'Criterion', children=rich(c)) for c in CRITERIA]),
    El('div', 'Investment opportunity', 'dst-panel', children=[
        El('h3', 'Heading', 'dst-panel__title', children=[q('Investment Opportunity')]),
        El('ul', 'Items', 'dst-panel__grid', children=[
            El('li', 'Item', 'dst-panel__item', children=[
                El('h4', 'Title', 'dst-panel__item-title', children=[q(t)]),
                El('p', 'Text', 'dst-panel__item-text', children=rich(b)),
            ]) for t, b in OPPORTUNITY
        ]),
    ]),
    notes(('1.', 'No ROI or efficiency gain'), ('2.', "See 'Compensation to the Sponsor"), ('3.', 'Prospective investors should be aware that under the Delaware Statutory Trust Act, the Trustee is prohibited from making significant new capital expenditures. If a franchisor requires a PIP that exceeds the Trust\'s limited reserves, the Trust'),
          ('4.', 'U.S. Census Bureau — Weston City'), extra=['All brands stated are for illustrative']),
], attrs={'id': 'criteria'})

# ---------- 4 · brand and property (#p4) ----------
BRANDS = [('brand-marriott', 'Marriott', 'dst-brands__marriott'), ('brand-courtyard', 'Courtyard by Marriott', 'dst-brands__courtyard'),
          ('brand-bonvoy', 'Marriott Bonvoy', 'dst-brands__bonvoy')]
BRAND_PARAS = ["Marriott International is the world's largest", 'Courtyard by Marriott, classified', 'The property may benefit from Marriott Bonvoy',
               'This loyalty engine']
FB = ['The bistro (breakfast/dinner/bar)', 'Market (24-hour sundry)', 'Select catering and banquet solutions']
RECREATION = ['Heated outdoor pool', 'Fitness center', 'Business center', 'Free high-speed Wi-Fi', 'On-site self-parking', 'Pet-friendly rooms',
              'Valet dry cleaning', 'Modernized AV Equipment', '3 Meeting and event spaces']


def stat(value, label, block):
    return El('div', 'Figure', block + '__item', children=[El('strong', 'Value', block + '__value', children=[q(value)]),
                                                         El('span', 'Label', block + '__label', children=rich(label))])


property_ = section('Brand and property', 'dst-section dst-property', 'property-h', [
    band('Courtyard-Weston-4', 'Lobby bar and lounge', 'dst-band--tall'),
    El('div', 'Brands', 'dst-brands', children=[Svg(name, A + slug + '.svg', name, cls='dst-brands__logo ' + cls) for slug, name, cls in BRANDS]),
    El('div', 'Columns', 'dst-property__cols', children=[
        El('div', 'Brand overview', 'dst-property__brand', children=[
            El('h2', 'Heading', 'dst-title dst-title--s', {'id': 'property-h'}, rich('Brand Overview')),
            *[El('p', 'Text', 'dst-text', children=rich(p)) for p in BRAND_PARAS],
            El('div', 'Figures', 'dst-pair', children=[stat('~271M', 'Marriott Bonvoy Members', 'dst-pair'),
                                                      stat('~43M', 'New Members in 2025', 'dst-pair')]),
        ]),
        El('div', 'Property', 'dst-property__hotel', children=[
            El('h3', 'Heading', 'dst-title dst-title--s', children=[q('Courtyard by Marriott'), El('br', 'Break'), q('Fort Lauderdale Weston')]),
            El('p', 'Text', 'dst-text', children=rich('Six-story concrete block')),
            El('h4', 'Food and beverage', 'dst-list-title', children=[q('Food & Beverage')]),
            El('ul', 'Food and beverage list', 'dst-list', children=[El('li', 'Item', children=[q(t)]) for t in FB]),
            El('h4', 'Recreation and services', 'dst-list-title', children=[q('Recreation & Services')]),
            El('ul', 'Recreation list', 'dst-list dst-list--two', children=[El('li', 'Item', children=[q(t)]) for t in RECREATION]),
            El('div', 'Figures', 'dst-trio', children=[stat('176', 'Rooms', 'dst-trio'), stat('2002', 'Year Built', 'dst-trio'),
                                                      stat('2024', 'Last Renovation', 'dst-trio')]),
        ]),
    ]),
    notes(('1.', 'There can be no assurance that brand'), ('2.', 'Participation does not assure'), ('3.', 'Marriott International 2025 Annual Report.'),
          ('4.', 'Past renovations are not indicative'), ('5.', 'Franchisors may accelerate'), extra=['All brands shown are for illustrative']),
], attrs={'id': 'property'})

# ---------- 5 · gallery (#p5): the brochure's seven photos, in its order, as a carousel ----------
GALLERY = [('gal-1', 'King guest room with balcony'), ('gal-5', 'The bistro bar'), ('gal-6', 'Courtyard and outdoor seating'),
           ('gal-2', 'Suite living area'), ('gal-3', 'Market and bistro service area'), ('gal-7', 'Pool and hotel exterior'),
           ('gal-4', 'In-room work desk')]
gallery = o.carousel([('dst-' + m, alt, None) for m, alt in GALLERY], label='Gallery', chip=False, sid='gallery')

# ---------- 6 · location (#p6) ----------
ADDRESS = '2000 N Commerce Pkwy, Weston, FL 33326'   # handoff README (Location); the brochure shows it on the map only
MAPS = 'https://www.google.com/maps/@26.0922635,-80.365178,17z'
MAPS_LABEL = 'Open in Google Maps'
DISTANCES = [('Cleveland Clinic Weston', '~1.3 miles'), ('Amerant Bank Arena', '~7.1 miles'), ('Sawgrass Mills Mall', '~7.5 miles'),
             ('Ft. Lauderdale Airport', '~19 miles'), ('Hard Rock Stadium', '~22 miles'), ('Miami International Airport', '~32 miles'),
             ('Downtown Miami', '~33 miles'), ('Kaseya Center (Miami Heat)', '~33 miles'), ('PortMiami', '~35 miles'), ('Miami Beach', '~37 miles')]
location = section('Location', 'dst-section dst-section--alt dst-location', None, [
    El('div', 'Map', 'dst-map', children=[
        Img('Map', 'dst-Weston-Market-Map', 'Weston, Florida location map'),
        El('figure', 'Inset', 'dst-map__inset', children=[
            Img('Aerial', 'dst-map-inset-3', 'Aerial view of the hotel and Cleveland Clinic Florida'),
            El('span', 'Callout', 'dst-map__pill dst-map__pill--clinic', children=[q('Cleveland Clinic')]),
            El('span', 'Callout', 'dst-map__pill dst-map__pill--hotel', children=[q('Hotel')]),
        ]),
    ]),
    El('div', 'Details', 'dst-location__details', children=[
        El('div', 'Address', 'dst-location__address', children=[
            El('p', 'Address', 'dst-location__line', children=[ADDRESS]),
            El('a', 'Map link', 'link-arrow', {'href': MAPS, 'target': '_blank', 'rel': 'noopener'}, [MAPS_LABEL, El('span', 'Arrow', attrs={'aria-hidden': 'true'}, children=['→'])]),
        ]),
        El('div', 'Distances', 'dst-distances', children=[
            eyebrow(q('Drive-time proximity')),
            El('dl', 'List', 'dst-distances__list', children=[
                El('div', 'Row', 'dst-distances__row', children=[El('dt', 'Place', children=[q(p)]), El('dd', 'Distance', children=[q(d)])])
                for p, d in DISTANCES
            ]),
        ]),
    ]),
], attrs={'id': 'location', 'aria-label': 'Location'})

# ---------- 7 · market overview (#p7) ----------
MARKET = [('Affluent, Master-planned Community', '~27-square-mile'), ('South Florida Tourism Momentum', 'Broward County Convention Center'),
          ('Broward County Economic Fundamentals', 'Broward County population'), ('Cleveland Clinic', '258-bed Magnet-designated acute'),
          ('Sports & Entertainment', 'Amerant Bank Arena (~7.1 mi)'), ('Supply Dynamics', 'The 501-key Bonaventure')]
market = section('Market overview', 'dst-section dst-market', 'market-h', [
    band('dst-Weston-Aerial-2', 'Weston, Florida', 'dst-band--tall'),
    El('h2', 'Heading', 'dst-title', {'id': 'market-h'}, [q('Market Overview')]),
    El('div', 'Blocks', 'dst-blocks', children=[
        El('article', 'Block', 'dst-block', children=[El('h3', 'Title', 'dst-block__title', children=[q(t)]),
                                                     El('p', 'Text', 'dst-block__text', children=rich(b))]) for t, b in MARKET
    ]),
    notes(('1.', 'Rankings are historical'), ('2.', 'Zillow'), ('3.', 'U.S. Census Bureau — Weston city'), ('4.', 'World Population Review'),
          ('5.', 'City of Weston'), ('6.', 'Broward County — Convention'), ('7.', 'Broward County Aviation'), ('8.', 'Cleveland Clinic Weston –'),
          ('9.', 'Sun Sentinel')),
], attrs={'id': 'market'})

# ---------- 8 · the sponsor (#p8) ----------
STRATEGIES = [
    ('Acquisitions', 'Driftwood targets value-add', [('~$1.2B', 'Hotel Acquisitions'), ('~$264.9M', 'Built Hotel Spend')]),
    ('Development', 'Driftwood selectively pursues', [('~$950.3M', 'In Development'), ('$684.3M+', 'Renovations')]),
    ('Lending', 'Through its credit platform', [('~$2.4B', 'Transaction Experience'), ('~$391.3M', 'Credit Investments')]),
    ('Management', 'Driftwood Hospitality Management (DHM) delivers', [('85', 'Hotels Managed'), ('~6,000', 'Employees')]),
]
sponsor = section('The sponsor', 'dst-section dst-section--alt dst-sponsor', 'sponsor-h', [
    band('Courtyard-Weston-3', 'Guest room'),
    El('h2', 'Heading', 'dst-statement', {'id': 'sponsor-h'}, [
        q('Driftwood Capital operates a vertically integrated'), ' ',
        El('span', 'Accent', 'dst-statement__accent', children=[q('in acquisitions, development, lending')]),
    ]),
    El('p', 'Intro', 'dst-text dst-text--lead', children=[q('The principals of Driftwood have 30+')]),
    El('ul', 'Figures', 'dst-stats', children=[
        El('li', 'Figure', 'dst-stat', children=[El('strong', 'Value', 'dst-stat__value', children=[q(v)]),
                                                El('span', 'Label', 'dst-stat__label', children=rich(l))])
        for v, l in [('~$3.5B', 'Hospitality AUM'), ('85', 'Assets Owned'), ('~16,400', 'Keys')]
    ]),
    El('div', 'Strategies', 'dst-strategies', children=[
        El('h3', 'Heading', 'dst-strategies__title', children=[q('Driftwood Investment Strategies')]),
        El('div', 'Columns', 'dst-strategies__grid', children=[
            El('article', 'Strategy', 'dst-strategy', children=[
                El('h4', 'Title', 'dst-strategy__title', children=[q(t)]),
                El('p', 'Text', 'dst-strategy__text', children=[q(b)]),
                El('dl', 'Metrics', 'dst-strategy__metrics', children=[
                    El('div', 'Metric', 'dst-strategy__metric', children=[El('dd', 'Value', 'dst-strategy__value', children=[q(v)]),
                                                                       El('dt', 'Label', 'dst-strategy__label', children=rich(l))])
                    for v, l in metrics
                ]),
            ]) for t, b, metrics in STRATEGIES
        ]),
    ]),
    notes(('1.', 'Figures represent internal data'), ('2.', 'As of September 30, 2025'), ('3.', 'The figures presented are as of February 18'),
          ('4.', 'Cumulative gross transaction'), extra=['This document does not constitute an offering of securities. Any offering']),
], attrs={'id': 'sponsor'})

# ---------- 9 · contact (#p11) ----------
CONTACTS = [('Wholesaler', 'Andy Marshall', '404.247.3455', 'dstweston@driftwoodcapital.com'),
            ('National Accounts', 'Joanna Venetch', '773.580.4308', 'jo@hana-solutions.com')]
contact = section('Contact', 'dst-contact', None, [
    Img('Background', 'dst-cover-bg', ''),
    Svg('Logo', A + 'logo-white.svg', 'Driftwood Capital', cls='dst-contact__logo'),
    El('div', 'Cards', 'dst-contact__cards', children=[
        El('article', 'Contact', 'dst-card', children=[
            El('p', 'Role', 'dst-card__role', children=[q(role)]),
            El('h3', 'Name', 'dst-card__name', children=[q(name)]),
            El('a', 'Phone', 'dst-card__link', {'href': 'tel:+1' + re.sub(r'\D', '', phone)}, [q(phone)]),
            El('a', 'Email', 'dst-card__link', {'href': 'mailto:' + email}, [q(email)]),
        ]) for role, name, phone, email in CONTACTS
    ]),
    El('p', 'Compliance', 'dst-contact__line', children=[q('For accredited investor use only')]),
], attrs={'id': 'contact', 'aria-label': 'Contact'})

# ---------- 10 · important disclosures and risk factors (#p9, #p10) ----------
P9 = ['This presentation (this', 'This Presentation is for informational', 'Any offer or solicitation shall be made', 'By accepting this document',
      'None of the information contained herein has been filed', 'Securities are offered through Metric', 'This Presentation contains forward-looking',
      'The target returns discussed', 'Due to various risks', 'An investment in the Trust is speculative', 'Prospective investors should carefully consider']
RISKS = [('Illiquidity and Loss of Principal', ['The interests in the Trust are illiquid']),
         ('Real Estate and Hospitality Industry Risks', ['Property performance may be adversely']),
         ('Distribution Risk', ["The Trust's ability to make distributions"]),
         ('Sponsor and Counterparty Risk', ['The success of the Trust is materially']),
         ('Financing and Refinancing Risk', ["The Trust's performance is subject"]),
         ('Environmental and Regulatory Risk.', ['The Trust may be subject to environmental']),
         ('Delaware Statutory Trust Structural Constraints.', ['Under IRS Revenue Ruling', 'These structural constraints'])]
P10 = ['Tax benefits associated with a Section 1031', 'Past, targeted, or projected performance', 'Certain information contained herein has been obtained',
       'All information contained herein is the sole', 'The unauthorized distribution', 'Securities offered through Metric Financial LLC, Member FINRA/SIPC.']
disclosures = section('Disclosures', 'dst-section dst-disclosures', 'disclosures-h', [
    El('p', 'Lead', 'dst-disclosures__lead', {'id': 'disclosures-h'}, [q('An Investment in Driftwood Hotel Income I, DST is')]),
    El('div', 'Text', 'dst-disclosures__body', children=
        [El('p', 'Paragraph', children=[q(p)]) for p in P9]
        + [x for head, paras in RISKS for x in [El('h3', 'Risk', 'dst-disclosures__head', children=[q(head)])]
           + [El('p', 'Paragraph', children=[q(p)]) for p in paras]]
        + [El('p', 'Paragraph', children=[q(p)]) for p in P10]),
], attrs={'id': 'disclosures'})

STYLESHEETS = ['shared', 'offering']  # + this page's site/styles/offering_hotel_income_dst.css
PAGE = [hero, o.subnav(SUBNAV), summary, criteria, property_, gallery, location, market, sponsor, contact, disclosures]

COPY_EXTRA = [_Pieces]
DYNAMIC_COPY = SPLIT  # brochure strings shown with their superscript marks as footnote marks (the text either side is in PIECES)
# The public version (Alex, 2026-10-09): the institutional line and the page labels of the print brochure, the Cap Rate
# row and its footnote 4.
DROPPED_COPY = {q('For institutional due diligence use only'), q('Cap Rate (2025 NOI) ⁴'), q('8.16%'), q('Cap rate calculated as')} \
    | {t for t in q.all if t.startswith('Driftwood Capital • ')}
# p2 footnote "4." is dropped with the cap-rate row; the other "4." strings are on the page, so "4." stays required.
# Not brochure copy: the hero buttons and the address line, map link label (handoff README), the section-bar labels
# (handoff README's header links, plus Gallery and Contact), and the footnote mark digits.
NON_DESIGN = {CONTACT_CTA, SUMMARY_CTA, ADDRESS, MAPS_LABEL, '→'} | {label for label, _ in SUBNAV} | set('0123456789')
COPY_SOURCE = 'Weston DST Brochure.dc.html'

MEDIA = {
    'dst-cover-bg': (A + 'cover-bg.jpg', 'Weston DST', 'Weston-DST-cover-bg.jpg'),
    'Courtyard-Weston-1': (A + 'Courtyard-Weston-1.jpg', 'Weston DST'),
    'Courtyard-Weston-2': (A + 'Courtyard-Weston-2.jpg', 'Weston DST'),
    'Courtyard-Weston-3': (A + 'Courtyard-Weston-3.jpg', 'Weston DST'),
    'Courtyard-Weston-4': (A + 'Courtyard-Weston-4.jpg', 'Weston DST'),
    'dst-Weston-Aerial-2': (A + 'Weston-Aerial-2.jpg', 'Weston DST', 'Weston-Aerial-2.jpg'),
    'dst-Weston-Market-Map': (A + 'Weston-Market-Map.jpg', 'Weston DST', 'Weston-Market-Map.jpg'),
    'dst-map-inset-3': (A + 'map-inset-3.jpg', 'Weston DST', 'Weston-map-inset-3.jpg'),
    **{'dst-' + m: (A + m + '.jpg', 'Weston DST', 'Weston-DST-' + m + '.jpg') for m, _ in GALLERY},
}

META = {'kind': 'offering', 'title': 'Driftwood Hotel Income I, DST', 'slug': 'driftwood-hotel-income-i-dst', 'status': 'publish',
        'fields': {  # Home card; card_url cleared: the offering has its page now (the 302 to driftwoodcapital.com ends)
            'offering_status': 'open', 'offering_tag': 'Delaware Statutory Trusts', 'card_title': 'Driftwood Hotel Income I, DST',
            'card_summary': q('A 176-key select-service hotel'), 'card_image': '{{media:Courtyard-Weston-1}}',
            'card_cta_label': 'View Offering', 'card_rendering': 0, 'home_order': 3, 'card_url': ''},
        # a 506(c) offering page: kept out of search until compliance confirms (handoff open question 3)
        'seo': {'robots': 'noindex, follow'}}
NON_DESIGN |= {'Delaware Statutory Trusts', 'View Offering'}  # Home card tag and label (Home design's values)
