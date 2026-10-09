"""EB-5 dialog, Spanish (Etch component, wp_block "eb5-dialog-es"): the dialog of handoff/design/Inversiones EB-5.dc.html, read by
position against the EN dialog (site/pages/eb5_dialog.py) and built by site/lib/eb5_form.py. HubSpot still gets the
English values (accreditation keys, contact methods, the country list, which this design also shows in English)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
from design import Aligned
from eb5_form import build, design_labels
import eb5_dialog as en

DESIGN = os.path.join(os.path.dirname(__file__), '..', '..', 'handoff', 'design', 'Inversiones EB-5.dc.html')
q = Aligned(en.q, DESIGN, start='role="dialog"', end='</x-dc>', extra=[276])  # 276: "(... in English)." after the consent links
LABELS = design_labels(DESIGN)
T = dict(en.T, next=LABELS['next'], submit=LABELS['submit'], close=LABELS['close'],
         fields=[(label, ph) for (label, _), ph in zip(en.T['fields'], LABELS['placeholders'])] + en.T['fields'][4:])
PAGE = build(q, T, en.COUNTRIES, consent_tail=q.extra(0))
STYLESHEETS = ['shared', 'dialog']
NON_DESIGN = {T['next'], T['submit']}
MEDIA = {}
META = {'kind': 'component', 'title': 'EB-5 dialog (Spanish)', 'slug': 'eb5-dialog-es', 'order': 13}
