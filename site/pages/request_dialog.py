"""Request dialog (Etch component, wp_block "request-dialog"), placed in both templates so every page has it. One native
<dialog> for the three flows in handoff/docs/hubspot-setup-steps.md "Site behavior":
  - offering pages: CTAs (href="#request" / data-modal-open="offering-request") -> mode "request"
  - Home coming-soon card "Get notified" (data-modal-open="registration" + data-page-uri)  -> mode "notify"
  - Home "Start Investing" (data-modal-open="registration", no offering)                  -> mode "signup"
New visitors get the 2-step Registration form; returning visitors (dd_lead cookie) get "Confirm your email" (Offering
Request form); "None of the above" stops at "Our Apologies" and nothing is sent (CLAUDE.md rule 7). Submits go to
POST /wp-json/dealdirect/v1/submit (dealdirect-core) with a nonce fetched at submit time, the page's URL as pageUri,
UTMs from the dd_utm cookie and HubSpot's hutk. Copy: the offering dialog in the Preferred Equity design; the notify
wording from the Home design's dialog."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
from etch import El
from design import Copy

D = os.path.join(os.path.dirname(__file__), '..', '..', 'handoff', 'design')
q = Copy(os.path.join(D, 'Riverside Wharf Preferred Equity.dc.html'), start='role="dialog"', end='</x-dc>')
home = Copy(os.path.join(D, 'DealDirect Home.dc.html'), start='role="dialog"', end='</x-dc>')
COPY_EXTRA = [home]  # Home's notify wording; its Login screen is not built (the final header has no login: Juniper Square)
DONE_TEXT = 'Thank you. Our investor relations team will send you the details for'
# Rendered with the current offering's name in place of the design's sample offering:
DYNAMIC_COPY = {q('Riverside Wharf Preferred Equity'), q(DONE_TEXT)}

SCRIPT = r"""// request-dialog: registration / offering request (handoff/docs/hubspot-setup-steps.md). Scoped; no globals.
(() => {
  const dlg = document.querySelector('.dd-dialog');
  if (!dlg) return;
  const API = '/wp-json/dealdirect/v1/';
  const $ = (s, el = dlg) => el.querySelector(s);
  const $$ = (s, el = dlg) => [...el.querySelectorAll(s)];
  const cookie = (n) => (document.cookie.match('(?:^|; )' + n + '=([^;]*)') || [])[1];

  // UTMs: most recent visit with any utm_* wins, kept 30 days in dd_utm (first-party).
  const KEYS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'];
  const qs = new URLSearchParams(location.search);
  if (KEYS.some((k) => qs.get(k))) {
    const utm = Object.fromEntries(KEYS.filter((k) => qs.get(k)).map((k) => [k, qs.get(k)]));
    document.cookie = 'dd_utm=' + encodeURIComponent(JSON.stringify(utm)) + ';path=/;max-age=' + 30 * 86400 + ';samesite=lax' + (location.protocol === 'https:' ? ';secure' : '');
  }
  const utm = () => { try { return JSON.parse(decodeURIComponent(cookie('dd_utm') || '')) || {}; } catch (_) { return {}; } };

  let ctx = {}, opener = null, step = 0;
  const views = $$('[data-view]');
  const show = (name) => {
    views.forEach((v) => { v.hidden = v.dataset.view !== name; });
    const h = $('[data-view="' + name + '"] h2');
    if (h) { dlg.setAttribute('aria-labelledby', h.id); if (dlg.open) h.focus(); }
    $$('.dd-dialog__error').forEach((e) => { e.textContent = ''; });
  };
  const setStep = (n) => {
    step = n;
    $$('[data-step]').forEach((f) => { f.hidden = f.dataset.step !== String(n); f.disabled = f.hidden; });
    $$('.dd-dialog__steps li').forEach((li, i) => li.toggleAttribute('data-done', i <= Math.min(n, 1)));
    $('.dd-dialog__steps').hidden = n === 'sorry';
    $('[data-prev]').disabled = n === 0;
    $('[data-next]').hidden = n === 'sorry';
    $$('[data-next] span').forEach((s) => { s.hidden = s.dataset.label !== (n === 1 ? 'submit' : 'next'); });
    const h = $('[data-step="' + n + '"] h2');
    if (h) { dlg.setAttribute('aria-labelledby', h.id); if (dlg.open) h.focus(); }
  };

  const open = (trigger) => {
    opener = trigger;
    const main = document.querySelector('main[data-page-name]');
    const kind = trigger.dataset.modalOpen === 'offering-request' || trigger.getAttribute('href') === '#request' ? 'request'
      : trigger.dataset.pageUri ? 'notify' : 'signup';
    const name = trigger.dataset.pageName || (kind === 'request' && main ? main.dataset.pageName : '');
    ctx = { mode: kind, name, pageUri: new URL(trigger.dataset.pageUri || location.pathname, location.origin).href,
            pageName: name || document.title, card: trigger.closest('.deal-card') };
    dlg.dataset.mode = kind;
    $$('[data-dd-name]').forEach((e) => { e.textContent = name; });
    $('.dd-dialog__eyebrow').hidden = !name;
    $$('form', dlg).forEach((f) => f.reset());
    if (kind !== 'signup' && cookie('dd_lead')) { show('confirm'); } else { show('register'); setStep(0); }
    dlg.showModal();
  };
  const close = () => { dlg.close(); };
  dlg.addEventListener('close', () => { if (opener) opener.focus(); });
  dlg.addEventListener('click', (e) => { if (e.target === dlg) close(); });  // backdrop
  $$('[data-close]').forEach((b) => b.addEventListener('click', close));

  document.addEventListener('click', (e) => {
    const t = e.target.closest('[data-modal-open="registration"], [data-modal-open="offering-request"], a[href="#request"]');
    if (!t || dlg.contains(t)) return;
    e.preventDefault();
    open(t);
  });
  if (location.hash === '#request' && document.querySelector('main[data-page-name]')) {
    open(document.querySelector('a[href="#request"]') || document.body);
  }

  const done = () => {
    if (ctx.mode === 'request') { show('done'); return; }
    if (ctx.mode === 'notify' && ctx.card) {  // the card says thank you (Home design)
      const b = $('.deal-card__notify', ctx.card), m = $('.deal-card__notified', ctx.card);
      if (m) m.hidden = false;
      if (b) b.hidden = true;
      opener = m || opener;
    }
    close();
  };
  const fail = (form, data) => {
    $('.dd-dialog__error', form).textContent = data.message || 'Something went wrong. Please try again.';
    const f = data.field && form.elements[data.field];
    if (f && f.focus) f.focus();
  };
  const send = async (form, body) => {
    const btn = $('[type="submit"]', form);
    btn.disabled = true;
    try {
      const tok = await (await fetch(API + 'token', { credentials: 'same-origin', cache: 'no-store' })).json();
      const res = await fetch(API + 'submit', {
        method: 'POST', credentials: 'same-origin',
        headers: { 'Content-Type': 'application/json', 'X-DD-Nonce': tok.nonce },
        body: JSON.stringify({ ...body, utm: utm(), hutk: cookie('hubspotutk') || '', pageUri: ctx.pageUri, pageName: ctx.pageName,
                               website: form.elements.website ? form.elements.website.value : '' }),
      });
      return await res.json();
    } catch (_) {
      return { status: 'error', message: 'We could not send your details. Please try again later.' };
    } finally { btn.disabled = false; }
  };

  const reg = $('[data-view="register"]');
  $('[data-prev]').addEventListener('click', () => setStep(0));
  reg.addEventListener('submit', async (e) => {
    e.preventDefault();
    const f = reg.elements;
    if (step === 0) { setStep(f.accredited_investor.value === 'none' ? 'sorry' : 1); return; }  // "none" is never sent
    const consent = $('.dd-dialog__consent-text', reg).textContent.replace(/\s+/g, ' ').trim();
    const data = await send(reg, { form: 'registration',
      fields: { accredited_investor: f.accredited_investor.value, firstname: f.firstname.value, lastname: f.lastname.value,
                email: f.email.value, phone: f.phone.value },
      consent: { agreed: f.consent.checked, text: consent } });
    if (data.status === 'sent') done();
    else if (data.status === 'not_accredited') setStep('sorry');
    else fail(reg, data);
  });

  const conf = $('[data-view="confirm"]');
  conf.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = conf.elements.email.value;
    const data = await send(conf, { form: 'offering-request', fields: { email } });
    if (data.status === 'sent') done();
    else if (data.status === 'needs_registration') { show('register'); setStep(0); reg.elements.email.value = data.email || email; }
    else fail(conf, data);
  });
  $('[data-not-you]').addEventListener('click', () => {
    document.cookie = 'dd_lead=;path=/;max-age=0';
    show('register'); setStep(0);
  });
})();
"""


def field(label, name, kind, auto):
    return El('label', label, 'dd-dialog__field', children=[
        El('span', 'Label', 'dd-dialog__label', children=[q(label)]),
        El('input', 'Input', 'dd-dialog__input', {'type': kind, 'name': name, 'required': '', 'autocomplete': auto}),
    ])


def error():
    return El('p', 'Error', 'dd-dialog__error', {'role': 'alert', 'aria-live': 'assertive'})


OPTIONS = [('', '-- Select an option'), ('income', 'Annual income exceeds $200K'), ('joint', 'Joint household income'),
           ('networth', 'Net worth exceeding $1M'), ('none', 'None of the above')]
STEPS = ['About Your Accreditation', 'About You']  # step labels: design script data (rqSteps)

confirm = El('form', 'Confirm email', 'dd-dialog__view', {'data-view': 'confirm', 'data-hs-form': 'offering-request'}, [
    El('h2', 'Heading', 'dd-dialog__title', {'id': 'dd-confirm-h', 'tabindex': '-1'}, [q('Confirm your email')]),
    El('p', 'Text (request)', 'dd-dialog__text dd-dialog__text--request', children=[q("You're already registered. Confirm your email and we'll send")]),
    El('p', 'Text (notify)', 'dd-dialog__text dd-dialog__text--notify', children=[home("You're already registered. Confirm your email and we'll let you know")]),
    field('Email', 'email', 'email', 'email'),
    error(),
    El('button', 'Submit', 'button button--primary dd-dialog__submit', {'type': 'submit'}, [
        El('span', 'Label (request)', 'dd-dialog__text--request', children=[q('Request Details')]),
        El('span', 'Label (notify)', 'dd-dialog__text--notify', children=[home('Get Notified')]),
    ]),
    El('button', 'Not registered', 'dd-dialog__link', {'type': 'button', 'data-not-you': ''}, [q('Not registered yet? Register here')]),
])

register = El('form', 'Registration', 'dd-dialog__view', {'data-view': 'register', 'data-hs-form': 'registration', 'hidden': ''}, [
    El('ol', 'Steps', 'dd-dialog__steps', {'aria-label': 'Registration (Steps)'}, [
        El('li', s, 'dd-dialog__step', children=[El('span', 'Bar', 'dd-dialog__bar', {'aria-hidden': 'true'}), El('span', 'Label', children=[s])])
        for s in STEPS
    ]),
    El('fieldset', 'Accreditation', 'dd-dialog__stepbox', {'data-step': '0'}, [
        El('h2', 'Heading', 'dd-dialog__title', {'id': 'dd-step0-h', 'tabindex': '-1'}, [q('Accreditation Status')]),
        El('p', 'Text', 'dd-dialog__text', children=[q('Driftwood DealDirect opportunities are available')]),
        El('label', 'Accreditation', 'dd-dialog__field', children=[
            El('span', 'Label', 'dd-dialog__label', children=[q('Are you an accredited investor?')]),
            El('select', 'Select', 'dd-dialog__input', {'name': 'accredited_investor', 'required': ''}, [
                El('option', label, attrs={'value': v}, children=[q(label)]) for v, label in OPTIONS
            ]),
        ]),
    ]),
    El('fieldset', 'Personal information', 'dd-dialog__stepbox', {'data-step': '1', 'hidden': '', 'disabled': ''}, [
        El('h2', 'Heading', 'dd-dialog__title', {'id': 'dd-step1-h', 'tabindex': '-1'}, [q('Personal Information')]),
        El('p', 'Text', 'dd-dialog__text', children=[q('Now that we know you are an accredited investor')]),
        El('div', 'Fields', 'dd-dialog__grid', children=[
            field('First name', 'firstname', 'text', 'given-name'), field('Last name', 'lastname', 'text', 'family-name'),
            field('Email', 'email', 'email', 'email'), field('Phone number', 'phone', 'tel', 'tel'),
        ]),
        El('label', 'Consent', 'dd-dialog__consent', children=[
            El('input', 'Checkbox', 'dd-dialog__check', {'type': 'checkbox', 'name': 'consent', 'required': ''}),
            # The text sent to HubSpot as consent is this span's text, exactly as shown (hubspot-setup-steps.md, Consent).
            El('span', 'Consent text', 'dd-dialog__consent-text', children=[
                q('I consent to Driftwood Capital storing') + ' ',
                El('a', 'Terms', attrs={'href': 'https://driftwoodcapital.com/terms-of-use/'}, children=[q('Terms of Use')]),
                ' ' + q('and') + ' ',
                El('a', 'Privacy', attrs={'href': 'https://driftwoodcapital.com/privacy-policy/'}, children=[q('Privacy Policy')]),
            ]),
        ]),
        # honeypot: people never see or fill it (dealdirect-core drops submissions that do)
        El('input', 'Website (leave empty)', 'dd-dialog__hp', {'type': 'text', 'name': 'website', 'tabindex': '-1', 'autocomplete': 'off', 'aria-hidden': 'true'}),
    ]),
    El('div', 'Apologies', 'dd-dialog__stepbox', {'data-step': 'sorry', 'hidden': ''}, [
        El('h2', 'Heading', 'dd-dialog__title', {'id': 'dd-sorry-h', 'tabindex': '-1'}, [q('Our Apologies')]),
        El('p', 'Text', 'dd-dialog__text', children=[q('Currently, our investment opportunities')]),
    ]),
    error(),
    El('div', 'Nav', 'dd-dialog__nav', children=[
        El('button', 'Previous', 'dd-dialog__prev', {'type': 'button', 'data-prev': '', 'disabled': ''}, [q('Previous')]),
        El('button', 'Next', 'button button--primary dd-dialog__submit', {'type': 'submit', 'data-next': ''}, [
            El('span', 'Next', attrs={'data-label': 'next'}, children=['Next']),
            El('span', 'Submit', attrs={'data-label': 'submit', 'hidden': ''}, children=['Submit']),
        ]),
    ]),
])

finished = El('div', 'Done', 'dd-dialog__view', {'data-view': 'done', 'hidden': ''}, [
    El('h2', 'Heading', 'dd-dialog__title', {'id': 'dd-done-h', 'tabindex': '-1'}, [q('Request received')]),
    El('p', 'Text', 'dd-dialog__text', children=[DONE_TEXT + ' ', El('span', 'Offering', attrs={'data-dd-name': ''}), '.']),
    El('button', 'Close', 'button button--primary', {'type': 'button', 'data-close': ''}, [q('Close')]),
])

PAGE = [
    El('dialog', 'Request dialog', 'dd-dialog', {'aria-labelledby': 'dd-step0-h'}, script=SCRIPT, children=[
        El('div', 'Panel', 'dd-dialog__panel', children=[
            El('button', 'Close', 'dd-dialog__close', {'type': 'button', 'aria-label': 'Close', 'data-close': ''}, [q('×')]),
            El('p', 'Offering', 'dd-dialog__eyebrow', {'data-dd-name': '', 'hidden': ''}),
            confirm, register, finished,
        ]),
    ]),
]

STYLESHEETS = ['shared']
# Not design copy: the step labels and Next/Submit (design script data: rqSteps, rqNextLabel), the period after the
# offering name, and the start of the done sentence (design: "...details for <offering name>.", name filled at runtime).
NON_DESIGN = set(STEPS) | {'Next', 'Submit', '.', DONE_TEXT}
MEDIA = {}
META = {'kind': 'component', 'title': 'Request dialog', 'slug': 'request-dialog', 'order': 12}
