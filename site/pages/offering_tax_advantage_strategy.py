"""Driftwood Tax Advantage Strategy I: card-only offering on Home (site/lib/card_offering.py). Name and tag from the
Home design's tax-advantaged section ("Invest via" row 03, the design's #advantaged-strategy-2026). Interim link: the
fund's current site (Alex, 2026-10-09: "link to https://dtas1.driftwoodcapital.com/ for now, we will recreate it here
at some point soon"); clear card_url when the page is built here."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
from card_offering import MEDIA, COPY_SOURCE, PAGE, q, NON_DESIGN, STYLESHEETS, meta  # noqa: F401

META = meta('Driftwood Tax Advantage Strategy I', 'driftwood-tax-advantage-strategy-i', 'Bonus Depreciation Funds', 4,
            'https://dtas1.driftwoodcapital.com/')
