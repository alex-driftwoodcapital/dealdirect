/* dwstats.js — Driftwood platform stats: SINGLE SOURCE OF TRUTH.
   ─────────────────────────────────────────────────────────────────
   HOW TO UPDATE: edit the MANUAL block below (management-reported
   figures the map can't derive). Hotels / keys / states are COMPUTED
   live from mapdata.js — update the portfolio list (see the Data
   Console card) and those refresh everywhere automatically.

   USE IN DECKS:  load mapdata.js + dwstats.js (ds-base.js does this),
   then write  <dw-stat stat="properties"></dw-stat>
               <dw-stat stat="keys" approx round="hundred"></dw-stat>
               <dw-stat stat="managedProperties"></dw-stat>
   Available keys — computed: properties, keys, states,
                               portfolioProperties, portfolioKeys,
                               creditProperties, managedProperties,
                               acquisitionProperties, developmentProperties,
                               preOpeningProperties, mapProperties, mapPins
                  — manual:   everything in MANUAL below.

   ⚠ CREDIT IS NEVER COUNTED AS OURS. Credit ('Lending') positions are loans,
   not hotels we own or operate — they appear on the map only to show the
   platform's reach. No stat exposed here folds credit rooms into a keys
   total. If you need the credit book, cite it separately and by name:
   "<dw-stat stat=\"creditProperties\"></dw-stat> credit positions".

   DUAL-BRANDED HOTELS COUNT AS TWO PROPERTIES, matching CoStar, which lists
   each flag separately. Their keys are the one building and count once. So
   `properties` (80) exceeds the number of equity rows in mapdata (78) and the
   number of map pins — by design. The table lives in mapdata.js as
   DUAL_BRANDED, and holds equity properties only.

   Three property counts, three different things — do not substitute one for
   another:
     properties (78)         DHM-managed footprint: acquisition + management +
                             development. The headline count — every hotel
                             actually under management today.
     portfolioProperties (80) the 78 above plus the two pre-opening assets
                             (Riverside Wharf Miami, Westin Cocoa Beach).
     managedProperties (38)  the third-party slice of that 79 — hotels DHM
                             operates for owners other than Driftwood
     creditProperties (22)   loan positions, as the tape provides them
     mapProperties (102)     every property on the map, credit included
                             = acquisition 33 + development 7 + pre-opening 2
                             + credit 22 + third-party managed 38. Any
                             footprint breakdown must show all five rows or it
                             will not sum to its own total.

   managedProperties used to be a hand-entered figure. It is now computed from the
   'Management' category, so it can no longer drift from the roster.        */
(function () {
  var MANUAL = {
    asOf: 'September 1, 2026',        // last data update — keep in sync with mapdata
    employees: 6000,                  // platform-wide professionals (approx)
    aum: '~$3.5B',                    // assets owned / managed
    yearsExperience: '30+',           // principals' combined CRE experience
    investmentProfessionals: 23,
    excludedDevProperties: 2,         // Equity—Development not yet operational
    /* Distinct ownership groups across the vetted roster. Counted from the
       "Ownership Group" column of compliance's Property Listing: 41 distinct
       values, less the "TO BE DETERMINED" placeholder. */
    ownershipGroups: 40
  };

  /* KPI SCOPE — the categories that count toward headline platform KPIs
     (hotels Driftwood manages, acquires, or develops). Credit-only positions
     ('Lending') and not-yet-operational ('In Development') are EXCLUDED.
     As of September 1, 2026: 78 managed properties / 15,162 keys. The keys
     figure ties to compliance's file exactly.

     Her roster lists 77 rows, which is 79 properties with the two dual-brands
     counted twice — but Westin Cocoa Beach appears there with a blank room
     count because it is still pre-opening. It is NOT under management, so it
     sits in the pre-opening row with Riverside Wharf Miami, and the managed
     headline is 78. Pre-opening: 2 properties / 669 planned keys.

     THE ROSTER IS COMPLIANCE'S, NOT OURS. The non-credit rows in mapdata.js
     are the vetted list in "Property Listing - 2026-09-03-155015.xlsx", tab
     "Property List with Owners&A (2)", rows 2-81, less the three rows
     highlighted red there (DHM HQ, Saratoga Hilton - The Bistro, Fox Cities
     Exhibition Center). Hotels carry their Google-facing names, not the
     internal shorthand that file uses. Seven hotels moved to her "Previous
     Properties" tab and were dropped; four were added; Westin Cocoa Beach
     and the Rumbao parking structure is carried at zero keys because
     it holds its own property number on her list. Riverside Wharf Miami and
     Westin Cocoa Beach are the two pre-opening assets, both outside the 78.
     Do not add, drop, or re-key a property here without a
     corresponding row in her file.

     Property counts follow CoStar: a dual-branded hotel is two properties, so
     the count agrees with what a reviewer pulling comps sees. Keys are the
     building and are counted once — which is why properties (managed slice)
     rise by one per dual-brand flag with no matching change to keys. */
  var KPI_SCOPE = ['Acquisition', 'Management', 'Development'];

  /* CREDIT_SCOPE — loans, not hotels we run. Excluded from every keys total on
     principle, not just from the headline. Counted only as a property count,
     and counted EXACTLY as the loan tape provides it — one row, one position,
     no dual-brand splitting — so the figure always ties to the lender's own
     document. 22 positions: 21 on the 8-11-26 tape, plus PUBLIC West Hollywood
     (8300 Sunset Blvd, West Hollywood, CA) added Sept 2026. */
  var CREDIT_SCOPE = ['Lending'];

  /* THIRD_PARTY_SCOPE — hotels DHM operates for owners other than Driftwood.
     A subset of the KPI scope, not a separate book. */
  var THIRD_PARTY_SCOPE = ['Management'];

  /* PORTFOLIO_SCOPE — everything Driftwood has an equity interest in: the KPI
     scope plus assets under construction. Still no credit. 80 props / 15,329 keys. */
  var PORTFOLIO_SCOPE = ['Acquisition', 'Management', 'Development', 'In Development'];

  var US_STATES = 'AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY DC'.split(' ');

  /* REPORTED overrides — use ONLY when a compliance-approved figure must win
     over the live computed value (add e.g. keys: 16400). Empty = fully live. */
  var REPORTED = {};

  function computed() {
    var md = window.__MAPDATA;
    if (!md || !md.HOTELS) return {};
    var keys = 0, props = 0, states = {};
    var pfKeys = 0, pfProps = 0, creditProps = 0, tpProps = 0, acqProps = 0, devProps = 0, preProps = 0;
    md.HOTELS.forEach(function (h) {
      var r = +h.rooms || 0;
      // Dual-branded hotels count as two properties (CoStar lists them twice)
      // but their keys are the one building and are added once. See
      // DUAL_BRANDED in mapdata.js.
      var u = +h.units || 1;
      if (CREDIT_SCOPE.indexOf(h.category) >= 0) { creditProps += u; return; }
      if (PORTFOLIO_SCOPE.indexOf(h.category) >= 0) { pfProps += u; pfKeys += r; }
      if (THIRD_PARTY_SCOPE.indexOf(h.category) >= 0) tpProps += u;
      if (h.category === 'Acquisition') acqProps += u;
      if (h.category === 'Development') devProps += u;
      if (h.category === 'In Development') preProps += u;
      if (KPI_SCOPE.indexOf(h.category) >= 0) {
        props += u;
        keys += r;
        if (h.state && US_STATES.indexOf(h.state) >= 0) states[h.state] = 1;
      }
    });
    return {
      properties: props,            // KPI scope: manage / acquire / develop
      keys: keys,                   // KPI scope keys — NEVER includes credit
      states: Object.keys(states).length,  // U.S. states in KPI scope
      portfolioProperties: pfProps, // equity portfolio incl. under construction
      portfolioKeys: pfKeys,        // equity keys — NEVER includes credit
      creditProperties: creditProps,// credit positions, counted but not "ours"
      managedProperties: tpProps,   // DHM-operated for third-party owners
      acquisitionProperties: acqProps,
      developmentProperties: devProps,
      // Pre-opening ('In Development'): under construction, not yet operating.
      // Outside the headline `properties`, inside portfolioProperties. A
      // footprint breakdown needs this row or its parts cannot sum to the total.
      preOpeningProperties: preProps,
      // Every property on the map: equity + pre-opening + credit. A PROPERTY
      // count only — there is deliberately no matching keys total, because
      // that would fold credit rooms into something that reads as ours.
      mapProperties: pfProps + creditProps,
      mapPins: md.HOTELS.length     // pins on the map = one per building, so a
                                    // dual-brand is ONE pin though two properties
    };
  }

  /* Same stale-copy guard as mapdata.js — see DATA_SERIAL there. */
  /* Keep this in lockstep with DATA_SERIAL in mapdata.js — bump BOTH on any
     roster or MANUAL edit, or a stale bundled copy wins on the tie. */
  var STATS_SERIAL = 20260918;
  if (window.DWSTATS && (window.DWSTATS.STATS_SERIAL || 0) >= STATS_SERIAL) return;

  window.DWSTATS = {
    STATS_SERIAL: STATS_SERIAL,
    manual: MANUAL,
    reported: REPORTED,
    computed: computed,
    get: function (k) {
      if (k === 'keysAll' || k === 'propertiesAll') {
        console.warn('[dwstats] "' + k + '" is retired — it folded credit rooms into a total. ' +
          'Use portfolioKeys / portfolioProperties (equity, no credit), or creditProperties.');
        return undefined;
      }
      if (k in REPORTED) return REPORTED[k];
      var c = computed();
      if (k in c) return c[k];
      return MANUAL[k];
    },
    getComputed: function (k) {
      var c = computed();
      return (k in c) ? c[k] : undefined;
    }
  };

  function fmt(el, v) {
    if (v == null) return '—';
    if (typeof v === 'number') {
      var r = el.getAttribute('round');
      if (r === 'hundred') v = Math.round(v / 100) * 100;
      if (r === 'thousand') v = Math.round(v / 1000) * 1000;
      v = v.toLocaleString('en-US');
      if (el.hasAttribute('approx')) v = '\u00B1' + v;
    }
    return v;
  }

  var DwStat = function () { return Reflect.construct(HTMLElement, [], DwStat); };
  DwStat.prototype = Object.create(HTMLElement.prototype);
  DwStat.prototype.connectedCallback = function () {
    var self = this;
    var render = function () { self.textContent = fmt(self, window.DWSTATS.get(self.getAttribute('stat'))); };
    render();
    // Re-read whenever a later copy of mapdata/dwstats lands, so a figure can
    // never be pinned to the snapshot that happened to load first.
    if (!self._dwBound) {
      self._dwBound = true;
      window.addEventListener('dwdata:changed', render);
    }
    if (!window.__MAPDATA) {
      var n = 0;
      var iv = setInterval(function () {
        if (window.__MAPDATA || ++n > 50) { clearInterval(iv); render(); }
      }, 150);
    }
  };
  if (!customElements.get('dw-stat')) customElements.define('dw-stat', DwStat);
  try { window.dispatchEvent(new CustomEvent('dwdata:changed')); } catch (e) {}
})();
