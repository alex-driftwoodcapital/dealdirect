"""Riverside Wharf Preferred Equity (/offering/riverside-wharf-preferred-equity/): an `offering` post rendered by the
single-offering template. Etch build of handoff/design/Riverside Wharf Preferred Equity.dc.html; section order and
anchors follow the design (#metrics #overview #webinar #partners #offering #market #legal), every string comes from
the design file via q(). Sections: site/lib/offering.py."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
from design import Copy
from offering import Offering, MARKET, MARKET_NOTES, METRIC_NOTES, UP

DESIGN = os.path.join(os.path.dirname(__file__), '..', '..', 'handoff', 'design', 'Riverside Wharf Preferred Equity.dc.html')
q = Copy(DESIGN)
o = Offering(q)

METRICS = [  # (value, qualifier, label, footnote ref, accent)
    ('13.0%', 'Target*', 'Net Quarterly Distributions', '1', True),
    ('1.65x', 'Target*', 'Net Equity Multiple', None, False),
    ('$100,000', None, 'Minimum Investment', '2', False),
    ('5-Year', None, 'Assumed Hold Period', '3', False),
]
STACK = [  # (amount, label, cumulative %, modifier): the preferred-equity layer is this offering's highlight
    ('~$96M', 'Total equity', '100%', 'cap-stack__layer--top'),
    ('~$35M', 'Preferred equity', '71%', 'cap-stack__layer--highlight'),
    ('~$60M', 'EB-5 mezzanine loan', '61%', 'cap-stack__layer--mezz'),
    ('~$145M', 'Total senior debt', '43%', 'cap-stack__layer--senior'),
]
HIGHLIGHTS = [
    ['Represents approximately 71%', '2', '.'], ['The investment targets a 13%', '3'],
    ['The project is structured with the objective of generating diversified'],
    ['The planned development includes', '4', '.'], ['Special use designations', '5', '.'],
    ['The hospitality component may benefit'], ['The investment structure provides', '6', '.'],
]
STRUCTURE_NOTES = [('1', 'As of November 25, 2025'), ('2', 'The preferred equity position'), ('3', '. Subject to available cash flow'),
                   (None, '4 These project descriptions'), (None, '5 These features are expected'), (None, '6 For a complete schedule'),
                   (None, 'All information is as of the date indicated'),
                   (None, 'All projections, financial or otherwise, are for illustrative purposes only and should not be construed as what actual results will be. Rather')]
SUBNAV = [('Metrics', 'metrics'), ('Overview', 'overview'), ('Video', 'webinar'), ('Partners', 'partners'),
          ('Offering', 'offering'), ('Market', 'market'), ('Legal', 'legal')]

STYLESHEETS = ['shared', 'offering']
PAGE = [
    o.hero('Preferred Equity', 'Dream_Website_banner', 'Riverside-Wharf_View-from-River', 'Riverside Wharf Miami rendering video'),
    o.metrics('Preferred Equity Target Metrics', '* 1', 'Targeted net quarterly distributions', METRICS, METRIC_NOTES),
    o.subnav(SUBNAV),
    o.overview('Riverside-Wharf_Pooldeck', 'Riverside Wharf Pool deck', 'A hospitality & entertainment development', [
        ['This two tower project', '1', ', a rooftop day club', '2', '.'], ['Designed to foster'], ['Located in a market'],
        ['The project is structured with the objective of generating cash flows']],
        ['1 Profile Magazine', '2 These project descriptions', 'All information is as of the date indicated', 'Nothing herein constitutes']),
    o.webinar('https://player.vimeo.com/video/1213615578?h=cd2e9fb726&byline=0&title=0&autoplay=1', 'Riverside Wharf Miami webinar',
              'riverside-wharf-webinar-poster', 'Riverside Wharf Miami video'),
    o.partners(),
    o.structure(STACK, HIGHLIGHTS, STRUCTURE_NOTES),
    o.market(MARKET, MARKET_NOTES),
    o.metrics_repeat(METRICS, METRIC_NOTES),
    o.legal(),
    o.cta(),
]

# Not design copy: the arrow and the sub-nav labels, which the design renders from its script data (subnav: [...]).
NON_DESIGN = {'→'} | {label for label, _ in SUBNAV}
# slug -> (source, Etch Asset Manager collection[, filename]). Live-site uploads keep their filenames; images are
# compressed on import with the Etch Asset Manager preset.
MEDIA = {
    'Riverside-Wharf_View-from-River': (UP + 'Riverside-Wharf_View-from-River.jpg', 'Riverside Wharf'),
    'Dream_Website_banner': (UP + 'Dream_Website_banner.mp4', 'Video'),
    'Riverside-Wharf_Pooldeck': (UP + 'Riverside-Wharf_Pooldeck.jpg', 'Riverside Wharf'),
    'Night-club-Lobby': (UP + 'Night-club-Lobby.jpg', 'Riverside Wharf'),
    'Riverside-Wharf-Coastal-Bar': (UP + 'Riverside-Wharf-Coastal-Bar.jpg', 'Riverside Wharf'),
    # Vimeo's poster frame for the webinar (design src); its URL has no filename, so it is named here.
    'riverside-wharf-webinar-poster': ('https://i.vimeocdn.com/video/2192570125-97b8978ab21cef729947bb6150572d3d869d9d7201c95d3f32a26fc55c5db2da-d_1920x1080?f=webp&region=us',
                                       'Riverside Wharf', 'riverside-wharf-webinar-poster.webp'),
    'cover-bg': ('handoff/design/assets/cover-bg.png', 'Brand'),  # 4K original; the deploy compresses it with the Etch preset
}

META = {'kind': 'offering', 'title': 'Riverside Wharf Preferred Equity', 'slug': 'riverside-wharf-preferred-equity',
        'status': 'publish'}  # frozen permalink /offering/riverside-wharf-preferred-equity/ (handoff/docs/permalinks.md)
