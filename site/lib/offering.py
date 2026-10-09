"""Section builders for offering pages (handoff/docs/etch-components.md "Offering single"), shared by every offering
(site/pages/offering_*.py). Each takes the page's Copy lookup `q`, so text always comes from that page's design file;
structure and classes are the same on every offering (styles: site/styles/offering.css + shared.css). CTAs that open
the request dialog (forms phase) keep href="#request" and carry data-modal-open="offering-request"."""
from etch import El, Img, section

ARROW = El('span', 'Arrow', attrs={'aria-hidden': 'true'}, children=['→'])
UP = 'https://driftwooddealdirect.com/wp-content/uploads/'

HERO_SCRIPT = """// offering-hero: muted background loop on wider screens; never under prefers-reduced-motion (QA checklist). Scoped; no globals.
const video = document.querySelector('.offering-hero__video');
if (video) {
  // Plays only where it is cheap: wider screens, no reduced motion, no data saver. Phones keep the poster (the video is
  // ~10 MB). While the hero is off screen the video pauses, so it is not decoded while the page scrolls.
  const ok = window.matchMedia('(min-width: 768px)').matches && !window.matchMedia('(prefers-reduced-motion: reduce)').matches
    && !(navigator.connection && navigator.connection.saveData);
  if (ok) {
    video.muted = true;
    video.preload = 'auto';
    new IntersectionObserver(([e]) => { if (e.isIntersecting) video.play().catch(() => {}); else video.pause(); }).observe(video);
  }
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
SUBNAV_SCRIPT = """// offering-subnav: marks the section being read (aria-current; the phone dropdown's label follows it) and closes the
// dropdown after a pick, on Escape and on a tap outside. Scoped; the links work without it.
document.querySelectorAll('.offering-subnav').forEach((nav) => {
  const menu = nav.querySelector('.offering-subnav__menu');
  const current = nav.querySelector('.offering-subnav__current');
  const links = [...nav.querySelectorAll('a[href^="#"]')];
  const close = () => { if (menu) menu.open = false; };
  links.forEach((a) => a.addEventListener('click', close));
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && menu && menu.open) { close(); menu.querySelector('summary').focus(); } });
  document.addEventListener('click', (e) => { if (menu && menu.open && !menu.contains(e.target)) close(); });
  const ids = [...new Set(links.map((a) => a.getAttribute('href').slice(1)))];
  const sections = ids.map((id) => document.getElementById(id)).filter(Boolean);
  if (!('IntersectionObserver' in window) || !sections.length) return;
  const mark = (id) => {
    links.forEach((a) => { if (a.getAttribute('href') === '#' + id) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current'); });
    const hit = links.find((a) => a.getAttribute('href') === '#' + id);
    if (hit && current) current.textContent = hit.textContent;
  };
  const seen = new IntersectionObserver((entries) => {
    const shown = entries.filter((e) => e.isIntersecting).sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
    if (shown.length) mark(shown[0].target.id);
  }, { rootMargin: '-130px 0px -60% 0px' });
  sections.forEach((s) => seen.observe(s));
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


CAROUSEL_SCRIPT = """// rendering-carousel: prev/next buttons, a "3 / 13" counter and arrow keys over a native scroll-snap track (swipe
// and trackpad scroll need no script). Smooth unless the visitor asks for reduced motion. Scoped; without the script the
// track still scrolls and the buttons stay hidden.
document.querySelectorAll('.rendering-carousel').forEach((c) => {
  const track = c.querySelector('.rendering-carousel__track');
  const slides = track ? [...track.children] : [];
  const ctl = c.querySelector('.rendering-carousel__controls');
  if (!slides.length || !ctl) return;
  const prev = ctl.querySelector('[data-dir="prev"]'), next = ctl.querySelector('[data-dir="next"]');
  const count = ctl.querySelector('.rendering-carousel__count');
  const behavior = matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth';
  let i = 0;
  const go = (n) => {
    n = Math.max(0, Math.min(slides.length - 1, n));
    track.scrollTo({ left: slides[n].offsetLeft - slides[0].offsetLeft, behavior });
  };
  const update = () => {
    count.textContent = (i + 1) + ' / ' + slides.length;
    prev.disabled = i === 0;
    next.disabled = i === slides.length - 1;
  };
  prev.addEventListener('click', () => go(i - 1));
  next.addEventListener('click', () => go(i + 1));
  track.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight') { e.preventDefault(); go(i + 1); }
    if (e.key === 'ArrowLeft') { e.preventDefault(); go(i - 1); }
  });
  if ('IntersectionObserver' in window) {
    const seen = new IntersectionObserver((entries) => {
      entries.forEach((e) => { if (e.isIntersecting) { i = slides.indexOf(e.target); update(); } });
    }, { root: track, threshold: 0.6 });
    slides.forEach((s) => seen.observe(s));
  }
  ctl.hidden = false;
  update();
});
"""


def sup(n):
    return El('sup', 'Footnote ref', 'fn-ref', children=[n])


class Offering:
    """Builders bound to one page's copy lookup."""

    def __init__(self, q, cta=None):
        """cta: one label for every request button on the page, in place of the design's (e.g. a teaser page's
        "Reserve Your Spot"); the page lists it as non-design copy with who asked for it."""
        self.q, self.cta_label = q, cta

    # ---------- small parts ----------
    def request(self, label, cls='button button--primary', name='Request'):
        return El('a', name, cls, {'href': '#request', 'data-modal-open': 'offering-request'}, [self.cta_label or self.q(label)])

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
        """Section bar (sticky under the header): the row of links on wide screens; below 1024px a dropdown whose
        summary shows the section being read and opens the same links. Labels and anchors come from the page."""
        link = lambda cls, label, anchor: El('a', label, cls, {'href': '#' + anchor}, [label])
        return El('nav', 'On this page', 'offering-subnav', {'aria-label': 'On this page'}, [
            El('div', 'Rail', 'offering-subnav__rail', children=[link('offering-subnav__link', l, a) for l, a in items]),
            El('details', 'Menu', 'offering-subnav__menu', children=[
                El('summary', 'Toggle', 'offering-subnav__toggle', children=[
                    El('span', 'Current section', 'offering-subnav__current', children=[items[0][0]]),
                    El('span', 'Chevron', 'offering-subnav__chevron', {'aria-hidden': 'true'}),
                ]),
                El('div', 'Sections', 'offering-subnav__list', children=[link('offering-subnav__item', l, a) for l, a in items]),
            ]),
        ], script=SUBNAV_SCRIPT)

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

    def carousel(self, eyebrow, title, slides, request_label):
        """Renderings carousel (#renderings): slides = [(media slug, alt, caption)], one per view on phones, the next one
        peeking from tablets up. A native scroll-snap track (swipe, trackpad, keyboard); CAROUSEL_SCRIPT adds the
        buttons and the counter."""
        q = self.q
        n = len(slides)
        return section('Renderings', 'rendering-carousel', 'renderings-h', [
            El('div', 'Head', 'rendering-carousel__head', children=[
                El('div', 'Titles', 'rendering-carousel__titles', children=[
                    El('p', 'Eyebrow', 'eyebrow', children=[q(eyebrow)]),
                    El('h2', 'Heading', 'rendering-carousel__title', {'id': 'renderings-h'}, [q(title)]),
                ]),
                El('div', 'Controls', 'rendering-carousel__controls', {'hidden': ''}, [
                    El('button', 'Previous', 'rendering-carousel__arrow', {'type': 'button', 'data-dir': 'prev', 'aria-label': 'Previous rendering',
                                                                          'aria-controls': 'renderings-track'}),
                    El('p', 'Counter', 'rendering-carousel__count', {'aria-live': 'polite'}),
                    El('button', 'Next', 'rendering-carousel__arrow rendering-carousel__arrow--next', {'type': 'button', 'data-dir': 'next',
                                                                                                  'aria-label': 'Next rendering', 'aria-controls': 'renderings-track'}),
                ]),
            ]),
            El('ul', 'Track', 'rendering-carousel__track', {'id': 'renderings-track', 'tabindex': '0', 'aria-label': title}, children=[
                El('li', 'Slide', 'rendering-carousel__slide', {'aria-roledescription': 'slide', 'aria-label': f'{k} of {n}'}, [
                    El('figure', 'Rendering', 'rendering-carousel__figure', children=[
                        Img('Photo', media, alt), self.chip(),
                        El('figcaption', 'Caption', 'chip chip--glass rendering-carousel__caption', children=[caption]),
                    ]),
                ]) for k, (media, alt, caption) in enumerate(slides, 1)
            ]),
            self.request(request_label),
        ], attrs={'id': 'renderings', 'aria-roledescription': 'carousel'}, script=CAROUSEL_SCRIPT)

    def rendering_band(self, media, alt):
        """One wide rendering between sections, with its Rendering tag."""
        return section('Rendering', 'rendering-band', None, [
            El('figure', 'Rendering', 'media-card rendering-band__figure', children=[Img('Photo', media, alt), self.chip()]),
        ], attrs={'aria-label': alt})

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
                                El('span', 'Label', 'cap-stack__label', children=[label if label == COMMON_EQUITY else q(label)]),
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
# The ~$96M layer is the common equity, not the total equity the designs label it (Alex, 2026-10-09); pages list it in
# NON_DESIGN and drop the design's 'Total equity'.
COMMON_EQUITY = 'Common equity'
MARKET_NOTES = ['1. VISIT FLORIDA', 'This webpage is a preliminary summary for discussion purposes only and does not contain all material information. Nothing herein constitutes an offering']
METRIC_NOTES = [('1', 'Targeted preferred return anticipated'), ('2', 'The minimum investment amount'),
                ('3', 'The anticipated hold period'), (None, '* Target internal rate of return')]
