"""Driftwood Tax Advantage Strategy I: card-only offering on Home (site/lib/card_offering.py). Name and tag from the
Home design's tax-advantaged section ("Invest via" row 03); interim link: that row's "Learn how it works"."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
from card_offering import MEDIA, COPY_SOURCE, PAGE, q, NON_DESIGN, STYLESHEETS, meta  # noqa: F401

META = meta('Driftwood Tax Advantage Strategy I', 'driftwood-tax-advantage-strategy-i', 'Bonus Depreciation Funds', 4,
            'https://driftwoodcapital.com/bonus-depreciation/')
