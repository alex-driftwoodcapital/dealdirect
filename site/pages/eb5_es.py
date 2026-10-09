"""Inversiones EB-5 (/inversiones-eb-5/): the EB-5 page in Spanish, built by site/lib/eb5_page.py from handoff/design/Inversiones EB-5.dc.html, read by
position against the EN design (design.Aligned). The design's two legal paragraphs with no EN counterpart (all
information subject to change; the translation notice, English prevails) are placed as the design places them. Its
template (template_page_es) carries the Spanish footer; the Spanish EB-5 dialog (eb5_dialog_es) ends the page."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
from design import Aligned
from eb5_page import alt_texts, build, media, track_data
from etch import El
import eb5 as en

DESIGN = os.path.join(os.path.dirname(__file__), '..', '..', 'handoff', 'design', 'Inversiones EB-5.dc.html')
q = Aligned(en.q, DESIGN, extra=[136, 139])  # 136: subject to change; 139: translation notice
TRACK = track_data(DESIGN)
LEGAL = [El('p', 'Text', children=[q.extra(0)]), El('p', 'Text', children=[q.extra(1)])]
PAGE = build(q, TRACK, alt_texts(DESIGN), legal_extra=LEGAL, dialog='eb5-dialog-es')
STYLESHEETS = en.STYLESHEETS
NON_DESIGN = {'→', '+', '±', '1', '2', '1.', '2.', '3.', '4.', '5.'} | {v for t in TRACK for v in t[:6]}
MEDIA = media(DESIGN)
META = {'title': 'Inversiones EB-5', 'slug': 'inversiones-eb-5', 'status': 'publish'}  # live title; frozen permalink /inversiones-eb-5/
