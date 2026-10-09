"""EB-5 dialog, English (Etch component, wp_block "eb5-dialog"), placed on the EN EB-5 pages: the EB-5 Registration form
built by site/lib/eb5_form.py from the dialog in handoff/design/EB-5 Investments.dc.html. The ES/PT pages get their own
components from the same builder with their design's strings."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
from design import Copy
from eb5_form import build, countries, placeholders

DESIGN = os.path.join(os.path.dirname(__file__), '..', '..', 'handoff', 'design', 'EB-5 Investments.dc.html')
q = Copy(DESIGN, start='role="dialog"', end='</x-dc>')
COUNTRIES = countries(DESIGN)
T = {
    'h_accred': 'Accreditation Status', 'p_accred': 'Investments in qualified projects', 'q_accred': 'Are you an accredited investor?',
    'opt_select': '— Select an option', 'opt_nw': 'Net worth exceeding', 'opt_inc': 'Annual income exceeds', 'opt_none': 'None of the above',
    'h_contact': 'Contact Information',
    'fields': [('First name (required)', 'First name *'), ('Last name (required)', 'Last name *'), ('Email (required)', 'Email *'),
               ('Phone number (required)', 'Phone number *'), ('Country (required)', 'Country *')],
    'h_method': 'Contact Method', 'legend': 'How would you prefer we contact you?',
    'radios': ['Email', 'Phone', 'Video Call', 'WhatsApp'],
    'ack': 'I understand that there is a required investment',
    'consent': ['I consent to Driftwood Capital storing', ('Terms of Use', 'https://driftwoodcapital.com/terms-of-use/'), 'and',
                ('Privacy Policy', 'https://driftwoodcapital.com/privacy-policy/')],
    'h_sorry': 'Our Apologies', 'p_sorry': 'Currently, our investment opportunities',
    'prev': 'Previous',
    # Not in the dialog markup: the design script's nextLabel values and the close button's aria-label.
    'next': 'Next', 'submit': 'Submit', 'close': 'Close',
}
placeholders(DESIGN, [ph for _, ph in T['fields'][:4]])
PAGE = build(q, T, COUNTRIES)
STYLESHEETS = ['shared', 'dialog']
NON_DESIGN = {'Next', 'Submit'}
MEDIA = {}
META = {'kind': 'component', 'title': 'EB-5 dialog', 'slug': 'eb5-dialog', 'order': 13}
