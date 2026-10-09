"""Section builders for offering pages (handoff/docs/etch-components.md "Offering single"), shared by every offering
(site/pages/offering_*.py). Each takes the page's Copy lookup `q`, so text always comes from that page's design file;
structure and classes are the same on every offering (styles: site/styles/offering.css + shared.css). CTAs that open
the request dialog (forms phase) keep href="#request" and carry data-modal-open="offering-request"."""
from etch import El, Img, section

ARROW = El('span', 'Arrow', attrs={'aria-hidden': 'true'}, children=['→'])
UP = 'https://driftwooddealdirect.com/wp-content/uploads/'

HERO_SCRIPT = """// offering-hero: muted background loop; never plays under prefers-reduced-motion (QA checklist). Scoped; no globals.
const video = document.querySelector('.offering-hero__video');
if (video && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  video.muted = true;
  video.preload = 'auto';
  video.play().catch(() => {});
}
"""
VIDEO_SCRIPT = """// offering-video: replace the poster with the Vimeo player on click (no third-party request before that). Scoped.
document.querySelectorAll('.offering-video__frame').forEach((frame) => {
  const play = frame.querySelector('.offering-video__play');
  if (!play) return;
  play.addEventListener('click', () => {
    const iframe = document.createElement('iframe');
    iframe.src = frame.dataset.videoSrc;
    iframe.title = frame.dataset.videoTitle;
    iframe.allow = 'autoplay; fullscreen; picture-in-picture';
    iframe.allowFullscreen = true;
    frame.replaceChildren(iframe);
    iframe.focus();
  });
});
"""
PROGRAM_SCRIPT = """// program-tabs: tabs (click, arrow keys, Home/End) switch panels; thumbnails switch the panel's image. Scoped.
document.querySelectorAll('.program-tabs').forEach((root) => {
  const tabs = [...root.querySelectorAll('[role="tab"]')];
  const select = (tab) => {
    tabs.forEach((t) => {
      const on = t === tab;
      t.setAttribute('aria-selected', String(on));
      t.tabIndex = on ? 0 : -1;
      root.querySelector('#' + t.getAttribute('aria-controls')).hidden = !on;
    });
  };
  tabs.forEach((tab, i) => {
    tab.addEventListener('click', () => select(tab));
    tab.addEventListener('keydown', (e) => {
      const to = { ArrowRight: i + 1, ArrowLeft: i - 1, Home: 0, End: tabs.length - 1 }[e.key];
      if (to === undefined) return;
      e.preventDefault();
      const next = tabs[(to + tabs.length) % tabs.length];
      select(next);
      next.focus();
    });
  });
  root.querySelectorAll('.program-tabs__panel').forEach((panel) => {
    const slides = [...panel.querySelectorAll('.program-tabs__slide')];
    const thumbs = [...panel.querySelectorAll('.program-tabs__thumb')];
    thumbs.forEach((thumb, i) => thumb.addEventListener('click', () => {
      slides.forEach((s, j) => { s.hidden = j !== i; });
      thumbs.forEach((t, j) => t.setAttribute('aria-pressed', String(j === i)));
    }));
  });
});
"""


def sup(n):
    return El('sup', 'Footnote ref', 'fn-ref', children=[n])


class Offering:
    """Builders bound to one page's copy lookup."""

    def __init__(self, q):
        self.q = q

    # ---------- small parts ----------
    def request(self, label, cls='button button--primary', name='Request'):
        return El('a', name, cls, {'href': '#request', 'data-modal-open': 'offering-request'}, [self.q(label)])

    def chip(self, cls=''):
        return El('span', 'Rendering chip', ('chip chip--glass rendering-chip ' + cls).strip(), children=[self.q('Rendering')])

    @staticmethod
    def footnotes(name, paras, dark=False):
        return El('div', name, 'footnotes footnotes--dark' if dark else 'footnotes', children=paras)

    def fn(self, ref, text):
        return El('p', 'Footnote', children=([sup(ref)] if ref else []) + [self.q(text)])

    def legal_link(self):
        return El('a', 'Disclaimers link', 'link-arrow', {'href': '#legal'}, [self.q('Click here to see important disclaimers')])

    def texts(self, items):
        """[prefix | ref digits | (prefix,)]: copy strings with footnote refs between them."""
        return [sup(t) if t.isdigit() else self.q(t) for t in items]

    # ---------- sections ----------
    def hero(self, eyebrow, video, poster, video_label, badge=None):
        q = self.q
        eyebrow_kids = [q(eyebrow)] + ([El('span', 'Status', 'chip chip--glass offering-hero__badge', children=[q(badge)])] if badge else [])
        return section('Hero', 'offering-hero', 'offering-hero-h', [
            # No autoplay attribute: the script starts it, so reduced-motion visitors only get the poster (LCP image).
            El('video', 'Hero video', 'offering-hero__video', {
                'src': '{{mediaurl:%s}}' % video, 'poster': '{{mediaurl:%s}}' % poster,
                'muted': '', 'loop': '', 'playsinline': '', 'preload': 'none',
                'aria-label': video_label}, script=HERO_SCRIPT),
            self.chip('offering-hero__rendering'),
            El('div', 'Veil', 'offering-hero__veil', {'aria-hidden': 'true'}),
            El('div', 'Copy', 'offering-hero__copy', children=[
                El('div', 'Heading group', children=[
                    El('p', 'Eyebrow', 'eyebrow eyebrow--dark offering-hero__eyebrow', children=eyebrow_kids),
                    El('h1', 'Heading', 'offering-hero__title', {'id': 'offering-hero-h'}, [q('Riverside Wharf Miami')]),
                ]),
                self.request('Request Investor Details', 'button button--white', 'Request investor details'),
            ]),
        ])

    def stat(self, value, qualifier, label, ref, accent):
        q = self.q
        return El('div', 'Stat', 'stat-card stat-card--tall offering-stat', children=[
            El('p', 'Value', 'stat-card__value stat-card__value--accent' if accent else 'stat-card__value', children=[
                q(value)] + ([El('span', 'Qualifier', 'stat-card__qualifier', children=[q(qualifier)])] if qualifier else [])),
            El('p', 'Label', 'stat-card__label', children=[q(label)] + ([sup(ref)] if ref else [])),
        ])

    def metrics(self, title, title_ref, lede, stats, notes):
        q = self.q
        return section('Target metrics', 'offering-metrics', 'metrics-h', [
            El('h2', 'Heading', 'offering-metrics__title', {'id': 'metrics-h'}, [q(title), sup(q(title_ref))]),
            El('p', 'Lede', 'offering-metrics__lede', children=[q(lede)]),
            El('div', 'Stats', 'offering-metrics__grid', children=[self.stat(*m) for m in stats]),
            self.footnotes('Footnotes', [self.fn(r, t) for r, t in notes] + [self.legal_link()]),
        ], attrs={'id': 'metrics'})

    @staticmethod
    def subnav(items):
        return El('nav', 'On this page', 'offering-subnav', {'aria-label': 'On this page'}, [
            El('div', 'Rail', 'offering-subnav__rail', children=[
                El('a', label, 'offering-subnav__link', {'href': '#' + anchor}, [label]) for label, anchor in items
            ]),
        ])

    def overview(self, image, alt, title, paras, notes):
        q = self.q
        return section('Overview', 'offering-overview', 'overview-h', [
            El('div', 'Row', 'media-split', children=[
                El('figure', 'Image', 'media-card', children=[Img('Pool deck', image, alt), self.chip()]),
                El('div', 'Copy', 'media-split__copy', children=[
                    El('h2', 'Heading', 'offering-overview__title', {'id': 'overview-h'}, [q(title)]),
                    El('div', 'Body', 'offering-overview__body', children=[El('p', 'Text', children=self.texts(p)) for p in paras]),
                    self.request('Request Offering Details'),
                ]),
            ]),
            self.footnotes('Footnotes', [self.fn(None, t) for t in notes]),
        ], attrs={'id': 'overview'})

    @staticmethod
    def webinar(video_src, video_title, poster=None, poster_alt=''):
        frame = [Img('Poster', poster, poster_alt)] if poster else []
        return section('Webinar', 'offering-video', None, [
            Img('Background', 'cover-bg', ''),
            El('div', 'Frame', 'offering-video__frame', {'data-video-src': video_src, 'data-video-title': video_title},
               script=VIDEO_SCRIPT, children=frame + [
                El('button', 'Play', 'offering-video__play', {'type': 'button', 'aria-label': 'Play video'}, [
                    El('span', 'Icon', 'offering-video__icon', {'aria-hidden': 'true'}),
                ]),
            ]),
        ], attrs={'id': 'webinar', 'aria-label': 'Riverside Wharf Miami webinar'})

    def partners(self):
        q = self.q
        return section('Partners', 'offering-partners', None, [
            El('div', 'Cards', 'offering-partners__grid', children=[
                El('article', 'TAO Group', 'card-light partner-card', children=[
                    El('div', 'Media', 'partner-card__media', children=[Img('Photo', 'Night-club-Lobby', ''), self.chip()]),
                    El('div', 'Body', 'partner-card__body', children=[
                        El('h2', 'Title', 'partner-card__title', children=[q('Partnering with TAO Group Hospitality')]),
                        El('p', 'Text', 'partner-card__text', children=[q('To elevate the entertainment experience')]),
                        El('a', 'Link', 'link-arrow', {'href': 'https://taogroup.com/'}, [q('Learn more about TAO Group Hospitality.'), ARROW]),
                    ]),
                ]),
                El('article', 'Dream Hotels', 'card-light partner-card', children=[
                    El('div', 'Media', 'partner-card__media', children=[Img('Photo', 'Riverside-Wharf-Coastal-Bar', ''), self.chip()]),
                    El('div', 'Body', 'partner-card__body', children=[
                        El('h2', 'Title', 'partner-card__title', children=[q('Dream Hotels, part of the Hyatt family')]),
                        El('p', 'Text', 'partner-card__text', children=[q('Recognized as a premier lifestyle brand')]),
                    ]),
                ]),
            ]),
        ], attrs={'id': 'partners', 'aria-label': 'Partners'})

    def structure(self, stack, highlights, notes):
        """Capitalization stack (amount, label, cumulative %, modifier) + highlights ([copy/ref items]) + footnotes."""
        q = self.q
        return section('Offering', 'offering-structure', None, [
            El('div', 'Row', 'offering-structure__row', children=[
                El('div', 'Capitalization stack', 'cap-stack', children=[
                    El('h3', 'Title', 'cap-stack__title', children=[q('Anticipated Capitalization Stack'), sup('1')]),
                    El('p', 'Total', 'cap-stack__total', children=[q('~336M')]),
                    El('ol', 'Layers', 'cap-stack__layers', children=[
                        El('li', label, 'cap-stack__layer ' + mod, children=[
                            El('span', 'Amount and label', 'cap-stack__text', children=[
                                El('strong', 'Amount', 'cap-stack__amount', children=[q(amount)]),
                                El('span', 'Label', 'cap-stack__label', children=[q(label)]),
                            ]),
                            El('span', 'Cumulative', 'cap-stack__pct', children=[q(pct)]),
                        ]) for amount, label, pct, mod in stack
                    ]),
                ]),
                El('div', 'Highlights', 'highlights-list', children=[
                    El('h3', 'Title', 'highlights-list__title', children=[q('Offering highlights')]),
                    El('ul', 'Items', 'highlights-list__items', children=[
                        El('li', 'Highlight', 'highlights-list__item', children=self.texts(h)) for h in highlights
                    ]),
                    self.request('Request Offering Details'),
                ]),
            ]),
            self.footnotes('Footnotes', [self.fn(r, t) for r, t in notes]),
        ], attrs={'id': 'offering', 'aria-label': 'Offering'})

    def market(self, drivers, notes):
        q = self.q
        return section('Market', 'metrics-band metrics-band--dark', 'market-h', [
            El('div', 'Row', 'metrics-band__row', children=[
                El('div', 'Intro', 'metrics-band__intro', children=[
                    El('h2', 'Heading', 'metrics-band__title', {'id': 'market-h'}, [q('Strategic market fundamentals')]),
                    El('p', 'Text', 'metrics-band__text', children=[q('Characterized by global connectivity')]),
                    self.request('Request Information', 'button button--glass', 'Request information'),
                ]),
                El('ul', 'Drivers', 'metrics-band__list', children=[
                    El('li', 'Driver', 'metrics-band__item', children=self.texts(d)) for d in drivers
                ]),
            ]),
            self.footnotes('Footnotes', [self.fn(None, t) for t in notes], dark=True),
        ], attrs={'id': 'market'})

    def metrics_repeat(self, stats, notes):
        q = self.q
        return section('Target metrics (repeat)', 'offering-metrics offering-metrics--repeat', 'metrics2-h', [
            El('div', 'Head', 'offering-metrics__head', children=[
                El('h2', 'Heading', 'offering-metrics__title', {'id': 'metrics2-h'}, [q('Target Metrics*')]),
                self.request('Download Brochure', name='Download brochure'),
            ]),
            El('div', 'Stats', 'offering-metrics__grid', children=[self.stat(*m) for m in stats]),
            self.footnotes('Footnotes', [self.fn(r, t) for r, t in notes] + [self.legal_link()]),
        ])

    def oz(self, image, alt, title, title_ref, intro, benefits, notes):
        """Opportunity Zone benefits (#structure, QOZ offerings): benefit cards beside a portrait image."""
        q = self.q
        return section('OZ benefits', 'offering-oz', 'oz-h', [
            El('div', 'Row', 'offering-oz__row', children=[
                El('div', 'Copy', 'offering-oz__copy', children=[
                    El('h2', 'Heading', 'offering-oz__title', {'id': 'oz-h'}, [q(title), sup(title_ref)]),
                    El('p', 'Intro', 'offering-oz__intro', children=[q(intro)]),
                    El('div', 'Benefits', 'offering-oz__benefits', children=[
                        El('div', 'Benefit', 'offering-oz__benefit', children=[
                            El('strong', 'Title', 'offering-oz__benefit-title', children=[q(t)]),
                            El('p', 'Text', children=[q(b)]),
                        ]) for t, b in benefits
                    ]),
                    self.request('Request Investor Details'),
                ]),
                El('figure', 'Image', 'media-card offering-oz__media', children=[Img('Photo', image, alt), self.chip()]),
            ]),
            self.footnotes('Footnotes', notes),
        ], attrs={'id': 'structure'})

    def program(self, title, tabs, note):
        """Program tabs (#assets): tabs -> gallery + spec panel (etch-components.md program-tabs). tabs: [(label,
        [(media slug, alt)], spec nodes)]. All panels are in the markup; the scoped script switches them."""
        q = self.q
        tablist = El('div', 'Tabs', 'program-tabs__tabs', {'role': 'tablist', 'aria-label': 'Program'}, [
            El('button', label, 'program-tabs__tab', {
                'type': 'button', 'role': 'tab', 'id': f'program-tab-{i}', 'aria-controls': f'program-panel-{i}',
                'aria-selected': 'true' if i == 0 else 'false', 'tabindex': '0' if i == 0 else '-1'}, [label])
            for i, (label, _, _) in enumerate(tabs)
        ])
        panels = []
        for i, (label, images, spec) in enumerate(tabs):
            attrs = {'role': 'tabpanel', 'id': f'program-panel-{i}', 'aria-labelledby': f'program-tab-{i}', 'tabindex': '0'}
            if i:
                attrs['hidden'] = ''
            slides = [El('div', f'Slide {n}', 'program-tabs__slide', {'hidden': ''} if n else {}, [Img('Image', m, alt)])
                      for n, (m, alt) in enumerate(images)]
            thumbs = [El('button', f'Thumb {n}', 'program-tabs__thumb', {
                'type': 'button', 'aria-label': f'Show image {n + 1}', 'aria-pressed': 'true' if n == 0 else 'false'}, [Img('Thumb', m, '')])
                for n, (m, _) in enumerate(images)]
            panels.append(El('div', label, 'program-tabs__panel', attrs, [
                El('div', 'Gallery', 'program-tabs__gallery', children=[
                    El('figure', 'Stage', 'program-tabs__stage', children=slides + [self.chip()]),
                    El('div', 'Thumbs', 'program-tabs__thumbs', children=thumbs),
                ]),
                El('div', 'Spec', 'card-light program-tabs__spec', children=spec),
            ]))
        return section('Proposed program', 'program-tabs', 'program-h', [
            El('div', 'Head', 'program-tabs__head', script=PROGRAM_SCRIPT, children=[
                El('h2', 'Heading', 'program-tabs__title', {'id': 'program-h'}, [q(title)]),
                tablist,
            ]),
            *panels,
            El('p', 'Disclaimer', 'footnotes', children=[q(note)]),
        ], attrs={'id': 'assets'})

    def spec(self, title, groups):
        """Spec panel content: h3, then (lead paragraph or None, [list items]) groups."""
        q = self.q
        out = [El('h3', 'Title', 'program-tabs__spec-title', children=[q(title)])]
        for lead, items in groups:
            if lead:
                out.append(El('p', 'Lead', 'program-tabs__spec-lead', children=[q(lead)]))
            out.append(El('ul', 'List', 'program-tabs__spec-list', children=[El('li', 'Item', children=item) for item in items]))
        return out

    def rationale(self, title, cards, note):
        """Investment rationale (#rationale): rationale-card grid (title, body nodes)."""
        q = self.q
        return section('Investment rationale', 'offering-rationale', 'rationale-h', [
            El('h2', 'Heading', 'offering-rationale__title', {'id': 'rationale-h'}, [q(title)]),
            El('div', 'Cards', 'offering-rationale__grid', children=[
                El('article', t, 'rationale-card', children=[
                    El('h3', 'Title', 'rationale-card__title', children=[q(t)]),
                    El('p', 'Text', 'rationale-card__text', children=body),
                ]) for t, body in cards
            ]),
            El('p', 'Disclaimer', 'footnotes', children=[q(note)]),
        ], attrs={'id': 'rationale'})

    def legal(self):
        q = self.q
        return section('Legal', 'legal-block', 'legal-h', [
            El('h2', 'Heading', 'legal-block__title', {'id': 'legal-h'}, [q('Legal disclosure')]),
            El('p', 'Text', children=[q('This website is not an offer')]),
            El('h2', 'Heading', 'legal-block__title', children=[q('* Target Returns')]),
            El('p', 'Text', children=[q('The target returns shown')]),
            El('p', 'Text', children=[q('These types of investments')]),
            El('h2', 'Heading', 'legal-block__title', children=[q('Renderings')]),
            El('p', 'Text', children=[q('This document contains artist')]),
        ], attrs={'id': 'legal'})

    def cta(self):
        q = self.q
        return section('Get started', 'cta-band cta-band--cover', 'cta-h', [
            El('div', 'Card', 'cta-band__card', children=[
                Img('Background', 'cover-bg', ''),
                El('div', 'Copy', 'cta-band__copy', children=[
                    El('h2', 'Heading', 'cta-band__title', {'id': 'cta-h'}, [q('Ready to get started?')]),
                    El('p', 'Text', 'cta-band__text', children=[q('Join our network of accredited')]),
                ]),
                self.request('Start Investing', 'button button--white', 'Start investing'),
            ]),
        ])


# Same on every Riverside Wharf offering: market drivers (copy prefix / footnote ref items) and their footnotes.
MARKET = [['Florida’s tourism demand', '1'], ['Miami International Airport served', '2'],
          ['Miami MSA was ranked', '3', '; and ranked No. 5', '4'], ['Miami also ranked', '5'],
          ['Miami’s Downtown submarket', '6'], ['The luxury and upper-upscale segment', '6']]
MARKET_NOTES = ['1. VISIT FLORIDA', 'This webpage is a preliminary summary for discussion purposes only and does not contain all material information. Nothing herein constitutes an offering']
METRIC_NOTES = [('1', 'Targeted preferred return anticipated'), ('2', 'The minimum investment amount'),
                ('3', 'The anticipated hold period'), (None, '* Target internal rate of return')]
