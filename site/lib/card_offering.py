"""Card-only offerings (Alex, 2026-10-09: "create card for now, we will create page for one and link the other"):
an `offering` post that shows on Home's Live offerings and has no page of its own yet. Its card_url field makes
/offering/<slug>/ redirect (302, temporary) to that link (dealdirect-core includes/content-model.php), so the card's
"View Offering" works today and needs no change when a page is built: clear card_url and add the page's sections.
Card values come from the Home design (COPY_SOURCE): the names and tags of the tax-advantaged section's "Invest via"
rows, its "Learn how it works" links as the interim targets, and the design's own summary placeholder."""
UP = 'handoff/design/assets/'
MEDIA = {'cover-bg': (UP + 'cover-bg.png', 'Brand')}  # no image for these offerings in the design or on live yet
COPY_SOURCE = 'DealDirect Home.dc.html'
PAGE = []  # no page yet: the single URL redirects to card_url
q = None
NON_DESIGN = set()
STYLESHEETS = ['shared']


def meta(title, slug, tag, order, url):
    return {'kind': 'offering', 'title': title, 'slug': slug, 'status': 'publish',
            'fields': {'offering_status': 'open', 'offering_tag': tag, 'card_title': title,
                       'card_summary': '[Summary from offering CPT]', 'card_image': '{{media:cover-bg}}',
                       'card_cta_label': 'View Offering', 'card_rendering': 0, 'home_order': order, 'card_url': url},
            'seo': {'robots': 'noindex, follow'}}  # a redirecting placeholder: keep it out of search until it has a page
