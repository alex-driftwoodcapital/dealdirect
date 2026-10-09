"""EB-5 dialog (Etch component per language): the EB-5 Registration form of handoff/docs/hubspot-setup-steps.md, built from
one EB-5 design's dialog (EB-5 Investments / Inversiones EB-5 / Investimentos EB-5). Three steps (accreditation, contact
information, contact method + $800,000 acknowledgement + consent); "None of the above" stops at "Our Apologies" and
nothing is sent (CLAUDE.md rule 7). Submits to POST /wp-json/dealdirect/v1/submit as form "eb5" with this page's URL as
pageUri. Values sent to HubSpot stay English whatever the page language: accreditation keys (nw/inc), contact methods
(Email/Phone/Video Call/WhatsApp) and the country (the EN design's option text). The design closes the dialog on submit
(no confirmation screen in any EB-5 design), so the script does the same.
Opened by any element with data-modal-open="eb5-register"."""
import re
from etch import El

SCRIPT = r"""// eb5-dialog: EB-5 Registration (handoff/docs/hubspot-setup-steps.md). Scoped; no globals.
(() => {
  const dlg = document.querySelector('[data-dialog="eb5"]');
  if (!dlg) return;
  const API = '/wp-json/dealdirect/v1/';
  const $ = (s, el = dlg) => el.querySelector(s);
  const $$ = (s, el = dlg) => [...el.querySelectorAll(s)];
  const cookie = (n) => (document.cookie.match('(?:^|; )' + n + '=([^;]*)') || [])[1];
  const utm = () => { try { return JSON.parse(decodeURIComponent(cookie('dd_utm') || '')) || {}; } catch (_) { return {}; } };
  const form = $('form');
  let opener = null, step = 0;

  const setStep = (n) => {
    step = n;
    $$('[data-step]').forEach((f) => { f.hidden = f.dataset.step !== String(n); if (f.tagName === 'FIELDSET') f.disabled = f.hidden; });
    $('[data-prev]').disabled = n === 0;
    $('[data-next]').hidden = n === 'sorry';
    $$('[data-next] span').forEach((s) => { s.hidden = s.dataset.label !== (n === 2 ? 'submit' : 'next'); });
    $('.dd-dialog__error').textContent = '';
    const h = $('[data-step="' + n + '"] h2');
    if (h) { dlg.setAttribute('aria-labelledby', h.id); if (dlg.open) h.focus(); }
  };
  const open = (trigger) => {
    opener = trigger;
    form.reset();
    setStep(0);
    dlg.showModal();
  };
  const close = () => { dlg.close(); };
  dlg.addEventListener('close', () => { if (opener) opener.focus(); });
  dlg.addEventListener('click', (e) => { if (e.target === dlg) close(); });  // backdrop
  $$('[data-close]').forEach((b) => b.addEventListener('click', close));
  document.addEventListener('click', (e) => {
    const t = e.target.closest('[data-modal-open="eb5-register"]');
    if (!t || dlg.contains(t)) return;
    e.preventDefault();
    open(t);
  });
  $('[data-prev]').addEventListener('click', () => setStep(step === 'sorry' ? 0 : Math.max(0, step - 1)));

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const f = form.elements;
    if (step === 0) { setStep(f.accredited_investor.value === 'none' ? 'sorry' : 1); return; }  // "none" is never sent
    if (step === 1) { setStep(2); return; }
    const btn = $('[data-next]');
    btn.disabled = true;
    let data;
    try {
      const tok = await (await fetch(API + 'token', { credentials: 'same-origin', cache: 'no-store' })).json();
      const res = await fetch(API + 'submit', {
        method: 'POST', credentials: 'same-origin',
        headers: { 'Content-Type': 'application/json', 'X-DD-Nonce': tok.nonce },
        body: JSON.stringify({ form: 'eb5',
          fields: { accredited_investor: f.accredited_investor.value, firstname: f.firstname.value, lastname: f.lastname.value,
                    email: f.email.value, phone: f.phone.value, country: f.country.value,
                    preferred_contact_method: f.preferred_contact_method.value, eb5_amount_acknowledgement: f.eb5_amount_acknowledgement.checked,
                    page_language: document.documentElement.lang || '' },
          consent: { agreed: f.consent.checked, text: $('.dd-dialog__consent-text').textContent.replace(/\s+/g, ' ').trim() },
          utm: utm(), hutk: cookie('hubspotutk') || '', pageUri: location.origin + location.pathname, pageName: document.title,
          website: f.website.value }),
      });
      data = await res.json();
    } catch (_) {
      data = { status: 'error', message: 'We could not send your details. Please try again later.' };
    } finally { btn.disabled = false; }
    if (data.status === 'sent') { close(); return; }
    if (data.status === 'not_accredited') { setStep('sorry'); return; }
    const el = data.field && f[data.field];
    const box = el && el.closest && el.closest('[data-step]');
    if (box) setStep(Number(box.dataset.step));
    $('.dd-dialog__error').textContent = data.message || 'Something went wrong. Please try again.';
    if (el && el.focus) el.focus();
  });
})();
"""

CONTACT = ['Email', 'Phone', 'Video Call', 'WhatsApp']  # HubSpot values (internal value = EN label)


def countries(design_path):
    """The country options, in the design's order, from the EN design's select (HubSpot needs these exact values)."""
    import html
    src = open(design_path, encoding='utf-8').read()
    sel = re.search(r'<select[^>]*autocomplete="country-name"[^>]*>(.*?)</select>', src, re.S).group(1)
    return [html.unescape(o) for o in re.findall(r'<option>([^<]*)</option>', sel)]


def placeholders(design_path, values):
    """Placeholders are attributes, which the copy gate doesn't read: each must be in the design verbatim."""
    src = open(design_path, encoding='utf-8').read()
    missing = [v for v in values if f'placeholder="{v}"' not in src]
    if missing:
        raise KeyError(f'placeholders not in the design: {missing}')


def build(q, t, en_countries, local_countries=None):
    """q: Copy over one EB-5 design's dialog. t: that design's strings as q() prefixes, plus 'next'/'submit' (design script
    data) and 'close' (aria label); see site/pages/eb5_dialog.py. en_countries: HubSpot values; local_countries: the same
    list as the language's design shows it (defaults to EN)."""
    shown = local_countries or en_countries
    assert len(shown) == len(en_countries), 'country lists differ in length'

    def text_input(label_ph, name, kind, auto):
        label, ph = label_ph
        return El('label', label, 'dd-dialog__field', children=[
            El('span', 'Label', 'hidden-accessible', children=[q(label)]),
            El('input', 'Input', 'dd-dialog__input', {'type': kind, 'name': name, 'required': '', 'autocomplete': auto,
                                                      'placeholder': ph}),
        ])

    def heading(key, hid):
        return El('h2', 'Heading', 'dd-dialog__title', {'id': hid, 'tabindex': '-1'}, [q(t[key])])

    consent = []
    for part in t['consent']:  # strings, and (link text, href) for the links
        if isinstance(part, tuple):
            consent.append(El('a', part[0], attrs={'href': part[1]}, children=[q(part[0])]))
        else:
            consent.append((' ' if consent else '') + q(part) + ' ')
    consent[-1] = consent[-1].rstrip() if isinstance(consent[-1], str) else consent[-1]

    step0 = El('fieldset', 'Accreditation', 'dd-dialog__stepbox', {'data-step': '0'}, [
        heading('h_accred', 'eb-step0-h'),
        El('p', 'Text', 'dd-dialog__text', children=[q(t['p_accred'])]),
        El('label', 'Accreditation', 'dd-dialog__field', children=[
            El('span', 'Label', 'dd-dialog__label', children=[q(t['q_accred'])]),
            El('select', 'Select', 'dd-dialog__input', {'name': 'accredited_investor', 'required': ''}, [
                El('option', 'Option', attrs={'value': v}, children=[q(t[k])])
                for v, k in [('', 'opt_select'), ('nw', 'opt_nw'), ('inc', 'opt_inc'), ('none', 'opt_none')]
            ]),
        ]),
    ])
    f = t['fields']
    step1 = El('fieldset', 'Contact information', 'dd-dialog__stepbox', {'data-step': '1', 'hidden': '', 'disabled': ''}, [
        heading('h_contact', 'eb-step1-h'),
        El('div', 'Fields', 'dd-dialog__grid', children=[
            text_input(f[0], 'firstname', 'text', 'given-name'), text_input(f[1], 'lastname', 'text', 'family-name'),
            text_input(f[2], 'email', 'email', 'email'), text_input(f[3], 'phone', 'tel', 'tel'),
            El('label', 'Country', 'dd-dialog__field', children=[
                El('span', 'Label', 'hidden-accessible', children=[q(f[4][0])]),
                El('select', 'Select', 'dd-dialog__input', {'name': 'country', 'required': '', 'autocomplete': 'country-name'}, [
                    El('option', 'Placeholder', attrs={'value': '', 'disabled': '', 'selected': ''}, children=[q(f[4][1])]),
                ] + [El('option', c, attrs={'value': v}, children=[c]) for v, c in zip(en_countries, shown)]),
            ]),
        ]),
    ])
    step2 = El('fieldset', 'Contact method', 'dd-dialog__stepbox', {'data-step': '2', 'hidden': '', 'disabled': ''}, [
        heading('h_method', 'eb-step2-h'),
        El('fieldset', 'Contact method', 'dd-dialog__choices', children=[
            El('legend', 'Question', 'dd-dialog__legend', children=[q(t['legend'])]),
        ] + [El('label', v, 'dd-dialog__choice', children=[
            El('input', 'Radio', attrs={'type': 'radio', 'name': 'preferred_contact_method', 'value': v}), q(label)])
            for v, label in zip(CONTACT, t['radios'])]),
        El('label', 'Acknowledgement', 'dd-dialog__consent', children=[
            El('input', 'Checkbox', 'dd-dialog__check', {'type': 'checkbox', 'name': 'eb5_amount_acknowledgement', 'required': ''}),
            El('span', 'Text', children=[q(t['ack'])]),
        ]),
        El('label', 'Consent', 'dd-dialog__consent', children=[
            El('input', 'Checkbox', 'dd-dialog__check', {'type': 'checkbox', 'name': 'consent', 'required': ''}),
            # The text sent to HubSpot as consent is this span's text, exactly as shown (hubspot-setup-steps.md, Consent).
            El('span', 'Consent text', 'dd-dialog__consent-text', children=consent),
        ]),
        # honeypot: people never see or fill it (dealdirect-core drops submissions that do)
        El('input', 'Website (leave empty)', 'dd-dialog__hp', {'type': 'text', 'name': 'website', 'tabindex': '-1', 'autocomplete': 'off', 'aria-hidden': 'true'}),
    ])
    sorry = El('div', 'Apologies', 'dd-dialog__stepbox', {'data-step': 'sorry', 'hidden': ''}, [
        heading('h_sorry', 'eb-sorry-h'),
        El('p', 'Text', 'dd-dialog__text', children=[q(t['p_sorry'])]),
    ])
    nav = El('div', 'Nav', 'dd-dialog__nav', children=[
        El('button', 'Previous', 'dd-dialog__prev', {'type': 'button', 'data-prev': '', 'disabled': ''}, [q(t['prev'])]),
        El('button', 'Next', 'button button--primary dd-dialog__submit', {'type': 'submit', 'data-next': ''}, [
            El('span', 'Next', attrs={'data-label': 'next'}, children=[t['next']]),
            El('span', 'Submit', attrs={'data-label': 'submit', 'hidden': ''}, children=[t['submit']]),
        ]),
    ])
    return [
        El('dialog', 'EB-5 dialog', 'dd-dialog', {'data-dialog': 'eb5', 'aria-labelledby': 'eb-step0-h'}, script=SCRIPT, children=[
            El('div', 'Panel', 'dd-dialog__panel', children=[
                El('button', 'Close', 'dd-dialog__close', {'type': 'button', 'aria-label': t['close'], 'data-close': ''}, [q('×')]),
                El('form', 'EB-5 Registration', 'dd-dialog__view', {'data-hs-form': 'eb5'}, [
                    step0, step1, step2, sorry, El('p', 'Error', 'dd-dialog__error', {'role': 'alert', 'aria-live': 'assertive'}), nav,
                ]),
            ]),
        ]),
    ]
