// mapdata.js — Driftwood portfolio map dataset (parsed from STR-sourced CSV).
// Plain JS global: window.__MAPDATA. No build step.
(function () {
  var CITY_COORDINATES = {
  "Guanacaste, Costa Rica": { lat: 10.5000, lng: -85.5000 },
  "San Juan, PR": { lat: 18.4655, lng: -66.1057 },
  "Miami, FL": { lat: 25.7617, lng: -80.1918 },
  "Cocoa Beach, FL": { lat: 28.3200, lng: -80.6076 },
  "Ft. Lauderdale, FL": { lat: 26.1224, lng: -80.1373 },
  "West Palm Beach, FL": { lat: 26.7153, lng: -80.0534 },
  "Daytona Beach, FL": { lat: 29.2108, lng: -81.0228 },
  "Melbourne, FL": { lat: 28.0836, lng: -80.6081 },
  "Doral, FL": { lat: 25.8176, lng: -80.3595 },
  "Jacksonville, FL": { lat: 30.3322, lng: -81.6557 },
  "Pompano Beach, FL": { lat: 26.2379, lng: -80.1248 },
  "Orlando, FL": { lat: 28.5383, lng: -81.3792 },
  "Tallahassee, FL": { lat: 30.4383, lng: -84.2807 },
  "Clermont, FL": { lat: 28.5494, lng: -81.7729 },
  "Ft. Myers, FL": { lat: 26.6406, lng: -81.8723 },
  "Naples, FL": { lat: 26.1420, lng: -81.7948 },
  "Stuart, FL": { lat: 27.1975, lng: -80.2528 },
  "Dallas, TX": { lat: 32.7767, lng: -96.7970 },
  "Rockwall, TX": { lat: 32.8943, lng: -96.4795 },
  "Houston, TX": { lat: 29.7604, lng: -95.3698 },
  "Southlake, TX": { lat: 32.9412, lng: -97.1342 },
  "Plano, TX": { lat: 33.0198, lng: -96.6989 },
  "San Antonio, TX": { lat: 29.4241, lng: -98.4936 },
  "Tempe, AZ": { lat: 33.4255, lng: -111.9400 },
  "Scottsdale, AZ": { lat: 33.4942, lng: -111.9261 },
  "Williams, AZ": { lat: 35.2495, lng: -112.1904 },
  "San Diego, CA": { lat: 32.7157, lng: -117.1611 },
  "Pleasant Hill, CA": { lat: 37.9479, lng: -122.0647 },
  "Pleasanton, CA": { lat: 37.6604, lng: -121.8758 },
  "San Jose, CA": { lat: 37.3382, lng: -121.8863 },
  "Mountain View, CA": { lat: 37.3861, lng: -122.0839 },
  "Avila Beach, CA": { lat: 35.1797, lng: -120.7305 },
  "Pismo Beach, CA": { lat: 35.1428, lng: -120.6400 },
  "Paso Robles, CA": { lat: 35.6369, lng: -120.6545 },
  "Durham, NC": { lat: 35.9940, lng: -78.8986 },
  "Raleigh, NC": { lat: 35.7796, lng: -78.6382 },
  "Asheville, NC": { lat: 35.5951, lng: -82.5515 },
  "Highlands, NC": { lat: 35.0526, lng: -83.1968 },
  "Wrightsville Beach, NC": { lat: 34.2085, lng: -77.7961 },
  "Falls Church, VA": { lat: 38.8823, lng: -77.1711 },
  "Fairfax, VA": { lat: 38.8462, lng: -77.3064 },
  "Winchester, VA": { lat: 39.1857, lng: -78.1633 },
  "Atlanta, GA": { lat: 33.7490, lng: -84.3880 },
  "Alpharetta, GA": { lat: 34.0754, lng: -84.2941 },
  "Springfield, IL": { lat: 39.7817, lng: -89.6501 },
  "St. Charles, IL": { lat: 41.9142, lng: -88.3087 },
  "Matteson, IL": { lat: 41.5073, lng: -87.7356 },
  "Manchester, NH": { lat: 42.9956, lng: -71.4548 },
  "Portsmouth, NH": { lat: 43.0718, lng: -70.7626 },
  "Franklin, NH": { lat: 43.4431, lng: -71.6459 },
  "Norwood, MA": { lat: 42.1945, lng: -71.1995 },
  "Boston, MA": { lat: 42.3601, lng: -71.0589 },
  "Las Vegas, NV": { lat: 36.1699, lng: -115.1398 },
  "Park City, UT": { lat: 40.6461, lng: -111.4980 },
  "Salt Lake City, UT": { lat: 40.7608, lng: -111.8910 },
  "Osage Beach, MO": { lat: 38.1511, lng: -92.6343 },
  "Kansas City, MO": { lat: 39.0997, lng: -94.5786 },
  "Hilton Head Island, SC": { lat: 32.2163, lng: -80.7526 },
  "Richardson, TX": { lat: 32.9483, lng: -96.7299 },
  "Weston, FL": { lat: 26.1004, lng: -80.3998 },
  "Saratoga Springs, NY": { lat: 43.0844, lng: -73.7850 },
  "Novi, MI": { lat: 42.4806, lng: -83.4755 },
  "Wilmington, DE": { lat: 39.7447, lng: -75.5511 },
  "Pittsburgh, PA": { lat: 40.4406, lng: -79.9959 },
  "Rockville, MD": { lat: 39.0840, lng: -77.1528 },
  "East Elmhurst, NY": { lat: 40.7620, lng: -73.8760 },
  "Albany, NY": { lat: 42.6526, lng: -73.7562 },
  "Appleton, WI": { lat: 44.2619, lng: -88.4154 },
  "Alamogordo, NM": { lat: 32.8995, lng: -105.9603 },
  "Bozeman, MT": { lat: 45.6770, lng: -111.0429 },
  "Louisville, KY": { lat: 38.2527, lng: -85.7585 },
  "Bentonville, AR": { lat: 36.3729, lng: -94.2088 },
  "Mesa, AZ": { lat: 33.4152, lng: -111.8315 },
  "Colorado Springs, CO": { lat: 38.8339, lng: -104.8214 },
  "Roswell, NM": { lat: 33.3943, lng: -104.5230 },
  "Longmont, CO": { lat: 40.1672, lng: -105.1019 },
  "Portland, OR": { lat: 45.5152, lng: -122.6784 },
  "Florida City, FL": { lat: 25.4479, lng: -80.4792 },
  "Nashville, TN": { lat: 36.1627, lng: -86.7816 },
  "Bloomington, MN": { lat: 44.8408, lng: -93.2983 },
  "New Orleans, LA": { lat: 29.9511, lng: -90.0715 },
  "Milpitas, CA": { lat: 37.4323, lng: -121.8996 },
  "Rogers, AR": { lat: 36.3320, lng: -94.1185 },
  "Juno Beach, FL": { lat: 26.8784, lng: -80.0537 },
};

  var PROPERTY_COORDINATES = {
  // Fix: Removed duplicate entries for property coordinates to resolve build errors.
  "Margaritaville Beach Resort Playa Flamingo": { lat: 10.4319, lng: -85.7952 },
  "Courtyard Miami West/FL Turnpike": { lat: 25.7968, lng: -80.3804 },
  "Hilton Cocoa Beach Oceanfront": { lat: 28.3527, lng: -80.6086 },
  "Residence Inn by Marriott Miami West/FL Turnpike": { lat: 25.7969, lng: -80.3815 },
  "Tru/Home2 Suites by Hilton Fort Lauderdale Downtown": { lat: 26.1264, lng: -80.1378 },
  "Canopy by Hilton West Palm Beach Downtown": { lat: 26.7110, lng: -80.0540 },
  "Hampton Inn Daytona Beach/Beachfront": { lat: 29.2223, lng: -81.0068 },
  "Crowne Plaza Melbourne-Oceanfront by IHG": { lat: 28.1256, lng: -80.5962 },
  "Element Melbourne Oceanfront": { lat: 28.1437, lng: -80.5902 },
  "Holiday Inn Express Miami Airport Blue Lagoon Area, an IHG Hotel": { lat: 25.7760, lng: -80.2850 },
  "DoubleTree by Hilton Miami North I-95": { lat: 25.8643, lng: -80.2089 },
  "DoubleTree by Hilton Miami Doral": { lat: 25.7951, lng: -80.3664 },
  "Holiday Inn Express Doral Miami by IHG": { lat: 25.8115, lng: -80.3541 },
  "TownePlace Suites by Marriott Miami Kendall West": { lat: 25.6828092, lng: -80.456583 },
  "Tru by Hilton Jacksonville South Mandarin": { lat: 30.1557, lng: -81.6235 },
  "Home2 Suites by Hilton Pompano Beach Pier": { lat: 26.2366, lng: -80.0886 },
  "Miami International Airport Hotel": { lat: 25.7950, lng: -80.2790 },
  "Holiday Inn Express & Suites Orlando International Airport by IHG": { lat: 28.4623, lng: -81.3090 },
  "Holiday Inn Express & Suites Kendall East - Miami": { lat: 25.6833, lng: -80.3837 },
  "Four Points by Sheraton Tallahassee Downtown": { lat: 30.4389, lng: -84.2831 },
  "Hampton Inn Ft. Lauderdale Airport North Cruise Port": { lat: 26.0960, lng: -80.1472 },
  "Delta Hotels by Marriott West Palm Beach": { lat: 26.7022, lng: -80.0935 },
  "Candlewood Suites Miami Doral, an IHG Hotel": { lat: 25.8113, lng: -80.3478 },
  "Crowne Plaza Jacksonville Airport/I-95N by IHG": { lat: 30.4907, lng: -81.6496 },
  "Staybridge Suites Orlando Airport South by IHG": { lat: 28.4429, lng: -81.3116 },
  "Hampton Inn & Suites Clermont": { lat: 28.5448, lng: -81.7513 },
  "Hampton Inn & Suites Fort Myers-Estero/FGCU": { lat: 26.4912, lng: -81.7960 },
  "Fairfield by Marriott Inn & Suites Naples": { lat: 26.1956, lng: -81.6775 },
  "SpringHill Suites by Marriott Naples": { lat: 26.1983, lng: -81.6882 },
  "Fairfield by Marriott Inn & Suites Orlando Near Universal Orlando Resort": { lat: 28.4836, lng: -81.4568 },
  "Hampton Inn & Suites Stuart-North": { lat: 27.2346, lng: -80.2676 },
  "Courtyard by Marriott Miami Airport": { lat: 25.7795, lng: -80.2681 }, 
  "Marriott Miami Airport": { lat: 25.78493, lng: -80.2622 },
  "Residence Inn by Marriott Miami Airport": { lat: 25.78493, lng: -80.2622 },
  "Dalmar (Ft. Lauderdale Dual-Brand Hotel)": { lat: 26.12494, lng: -80.1379 },
  "Riverside Wharf Miami": { lat: 25.7689, lng: -80.1982 }, 
  "Westin Cocoa Beach Resort & Spa": { lat: 28.3685, lng: -80.6011 },
  "Crowne Plaza Springfield - Convention Ctr by IHG": { lat: 39.7960, lng: -89.6448 },
  "Holiday Inn Express Springfield Downtown": { lat: 39.8020, lng: -89.6479 },
  "Courtyard by Marriott Chicago St. Charles": { lat: 41.9161, lng: -88.3377 },
  "Fairfield by Marriott Inn & Suites Matteson Chicago": { lat: 41.5034, lng: -87.7336 },
  "Hampton Inn Tropicana": { lat: 36.1017, lng: -115.1738 },
  "Sheraton Dallas Hotel by the Galleria": { lat: 32.9263, lng: -96.8197 },
  "Hilton Dallas/Rockwall Lakefront": { lat: 32.8943, lng: -96.4795 },
  "Houston Marriott North": { lat: 29.9678, lng: -95.4137 },
  "Hilton Houston North": { lat: 29.9576, lng: -95.4278 },
  "Hilton Dallas/Southlake Town Square": { lat: 32.9495, lng: -97.1298 },
  "Hotel Vesper, Houston, a Tribute Portfolio Hotel": { lat: 29.7402, lng: -95.4608 },
  "Hilton Dallas/Plano Granite Park": { lat: 33.0886, lng: -96.8207 },
  "The Chifley Houston, Tapestry Collection by Hilton": { lat: 29.7369, lng: -95.4619 },
  "Sheraton Dallas Hotel": { lat: 32.78513, lng: -96.795 },
  "DoubleTree San Antonio Airport (Full Service Branded Hotel)": { lat: 29.5246, lng: -98.4962 },
  "DoubleTree by Hilton Hotel Phoenix Tempe": { lat: 33.4077, lng: -111.9673 },
  "Canopy by Hilton Tempe Downtown": { lat: 33.4239, lng: -111.9398 },
  "The Scottsdale Resort and Spa, Curio Collection by Hilton": { lat: 33.5516, lng: -111.9069 },
  "Hyatt House Scottsdale/Old Town": { lat: 33.4939, lng: -111.9252 },
  "Courtyard Phoenix-Mesa Gateway Airport": { lat: 33.3206, lng: -111.6353 },
  "SpringHill Suites Colorado Springs North/Air Force Academy": { lat: 38.9930, lng: -104.8010 },
  "TownePlace Suites Roswell": { lat: 33.3757, lng: -104.5236 },
  "Fairfield by Marriott Inn & Suites Roswell": { lat: 33.4092, lng: -104.5232 },
  "Home2 Suites by Hilton Longmont": { lat: 40.1573, lng: -105.1023 },
  "Courtyard Portland East": { lat: 45.5330, lng: -122.4790 },
  "Fairfield by Marriott Inn & Suites Homestead Florida City": { lat: 25.4479, lng: -80.4728 },
  "Hilton Garden Inn Louisville Mall of St. Matthews": { lat: 38.2418, lng: -85.6432 },
  "Hilton Durham near Duke University": { lat: 36.0122, lng: -78.9692 },
  "Marriott Raleigh Durham Research Triangle Park": { lat: 35.8824, lng: -78.8573 },
  "Hilton Raleigh North Hills": { lat: 35.8359, lng: -78.6437 },
  "The Radical Asheville, Tapestry Collection by Hilton": { lat: 35.5869, lng: -82.5661 },
  "Sheraton Park City": { lat: 40.6601, lng: -111.5061 },
  "Sheraton Salt Lake City Hotel": { lat: 40.7599, lng: -111.8959 },
  "Residence Inn by Marriott Salt Lake City Downtown": { lat: 40.76163, lng: -111.898 },
  "Margaritaville Lake Resort Lake of the Ozarks": { lat: 38.1408, lng: -92.7302 },
  "The Saratoga Hilton": { lat: 43.0833, lng: -73.7848 },
  "Aloft New York LaGuardia Airport": { lat: 40.7674, lng: -73.8735 },
  "Marriott Albany": { lat: 42.7169, lng: -73.8059 },
  "Sheraton Detroit Novi Hotel": { lat: 42.4431, lng: -83.4357 },
  "The Westin Tysons Corner": { lat: 38.9174, lng: -77.2223 },
  "Hilton Fairfax": { lat: 38.8604, lng: -77.3572 },
  "Hilton Washington DC/Rockville Hotel & Executive Meeting Ctr": { lat: 39.0601, lng: -77.1216 },
  "Fairfield by Marriott Inn & Suites Winchester": { lat: 39.1581, lng: -78.1458 },
  "SpringHill Suites by Marriott Fairfax Fair Oaks": { lat: 38.8617, lng: -77.3592 },
  "Fairfield by Marriott Inn & Suites Atlanta Buckhead": { lat: 33.8447, lng: -84.3725 },
  "Fairfield by Marriott Inn & Suites Atlanta Perimeter Center": { lat: 33.9189, lng: -84.3484 },
  "Wylie Hotel Atlanta, Tapestry Collection by Hilton": { lat: 33.7726, lng: -84.3639 },
  "Hilton Garden Inn Atlanta North/Alpharetta": { lat: 34.0583, lng: -84.2804 },
  "Hampton Inn Atlanta-Perimeter Center": { lat: 33.9163, lng: -84.3424 },
  "San Diego Marriott Mission Valley": { lat: 32.7758, lng: -117.1479 },
  "Hyatt House Pleasant Hill": { lat: 37.9482, lng: -122.0620 },
  "Hyatt House Pleasanton": { lat: 37.6975, lng: -121.9083 },
  "Sheraton San Jose Silicon Valley": { lat: 37.4172, lng: -121.9328 },
  "Avila Beach House (CA Independent Resort)": { lat: 35.1797, lng: -120.7342 },
  "Pacific Point Resort (CA Independent Resort)": { lat: 35.1436, lng: -120.6421 },
  "Paso Robles Inn (CA Independent Resort)": { lat: 35.6268, lng: -120.6912 },
  "Element by Westin Mission Valley": { lat: 32.7766, lng: -117.1525 },
  "Staybridge Suites Wilmington Downtown by IHG": { lat: 39.7389, lng: -75.5511 },
  "Hotel Rumbao, a Tribute Portfolio Hotel": { lat: 18.4639, lng: -66.1105 },
  "Sheraton Pittsburgh Hotel at Station Square": { lat: 40.4334, lng: -80.0055 },
  "Hilton Appleton Paper Valley": { lat: 44.2619, lng: -88.4069 },
  "Fairfield by Marriott Inn & Suites Alamogordo": { lat: 32.9231, lng: -105.9598 },
  "Best Western Plus GranTree Inn": { lat: 45.6943, lng: -111.0493 },
  "Hyatt Place Bentonville/Rogers": { lat: 36.3315, lng: -94.1809 },
  "Hotel Preston Nashville Airport": { lat: 36.1264, lng: -86.7061 },
  "The Westin New Orleans": { lat: 29.9514, lng: -90.0647 },
  "Courtyard by Marriott Manchester-Boston Regional Airport": { lat: 42.95016, lng: -71.4313 },
  "Homewood Suites by Hilton Manchester/Airport": { lat: 42.93622, lng: -71.4443 },
  "SpringHill Suites by Marriott Manchester-Boston Regional Airport": { lat: 42.93723, lng: -71.4458 },
  "Homewood Suites by Hilton Portsmouth": { lat: 43.09011, lng: -70.7813 },
  "Residence Inn by Marriott Boston Franklin": { lat: 42.09045, lng: -71.4338 },
  "Boston Raffles (Boston Ultra Luxury Hotel)": { lat: 42.34854, lng: -71.0748 },
  "Hampton Inn Suites Minneapolis St Paul Arpt-Mall of America": { lat: 44.8553, lng: -93.2422 },
  "SpringHill Suites by Marriott Minneapolis-St. Paul Airport/Mall of America": { lat: 44.8558, lng: -93.2386 },
  "Hotel Bourre Bonne Louisville, Curio Collection by Hilton": { lat: 38.2527, lng: -85.7585 },
  /* added with the 2026 roster — credit positions per DLP Property List (rec’d 8-11-26) */
  "DoubleTree by Hilton Hilton Head Island": { lat: 32.1855, lng: -80.7534 },
  "Courtyard by Marriott Dallas Richardson at Spring Valley": { lat: 32.9337, lng: -96.7203 },
  "Courtyard by Marriott Fort Lauderdale Weston": { lat: 26.1010, lng: -80.3838 },
  "InterContinental Kansas City at the Plaza": { lat: 39.0409, lng: -94.5906 },
  "Delta Hotels by Marriott Nashville Airport": { lat: 36.1264, lng: -86.7061 },
  "Tru/Home2 Suites by Hilton Pompano Beach Pier": { lat: 26.2340, lng: -80.0895 },
  "Hotel Rumbao Parking Structure": { lat: 18.4639, lng: -66.1105 },
  /* 15700 JFK Blvd, Houston, TX 77032 */
  "Sheraton North Houston at George Bush Intercontinental": { lat: 29.9865, lng: -95.3376 },
  /* 4901 W Plano Pkwy, Plano, TX 75093 */
  "Courtyard by Marriott Dallas Plano Parkway at Preston Road": { lat: 33.0207, lng: -96.8064 },
  /* 13950 US Highway 1, Juno Beach, FL 33408 */
  "Holiday Inn Express North Palm Beach-Oceanview by IHG": { lat: 26.8790, lng: -80.0553 },
  /* 150 S Lexington Ave, Asheville, NC 28801 */
  "Zelda Dearest, an SLH Hotel": { lat: 35.5896, lng: -82.5546 },
  /* 8300 Sunset Blvd, West Hollywood, CA 90069 */
  "PUBLIC West Hollywood": { lat: 34.0958, lng: -118.3730 },
};

  /* ── Dual-branded hotels ────────────────────────────────────────────────
     One building, two flags, two entries in CoStar. Driftwood counts these as
     two properties, matching CoStar, so the property count agrees with the
     number a reviewer pulling comps would see.

     KEYS ARE NOT SPLIT. The row's room count is the whole building and stays
     whole — the tape carries no per-flag split, and inventing one would move a
     total that is correct today. So a dual-brand property adds 2 to the
     property count and its full keys once. Add per-flag rows to the CSV if the
     split ever arrives; then drop the entry here.

     Only list a property CoStar actually splits. `flags` is what CoStar lists,
     and is what the map tooltip shows.

     CREDIT IS NOT SPLIT. Credit positions are counted exactly as the loan tape
     provides them — one row, one position — so the count always ties to the
     lender's own document. The Dalmar is dual-branded and is deliberately NOT
     listed here for that reason. Only equity properties appear below. */
  var DUAL_BRANDED = {
    'Tru/Home2 Suites by Hilton Fort Lauderdale Downtown': {
      flags: ['Tru by Hilton', 'Home2 Suites by Hilton']
    },
    'Tru/Home2 Suites by Hilton Pompano Beach Pier': {
      flags: ['Tru by Hilton', 'Home2 Suites by Hilton']
    }
  };

  // ---- Flag derivation (flag = specific brand product, brand = parent company) ----
  var FLAG_PATTERNS = [
    // Hilton portfolio — longest first
    ['Tru/Home2 Suites by Hilton', 'Tru/Home2 Suites by Hilton'],
    ['Home2 Suites by Hilton', 'Home2 Suites by Hilton'],
    ['Homewood Suites by Hilton', 'Homewood Suites by Hilton'],
    ['Hilton Garden Inn', 'Hilton Garden Inn'],
    ['Canopy by Hilton', 'Canopy by Hilton'],
    ['Curio Collection by Hilton', 'Curio Collection by Hilton'],
    ['DoubleTree by Hilton', 'DoubleTree by Hilton'],
    ['Tapestry Collection by Hilton', 'Tapestry Collection by Hilton'],
    ['Hampton Inn & Suites', 'Hampton Inn & Suites'],
    ['Hampton Inn', 'Hampton Inn'],
    ['Tru by Hilton', 'Tru by Hilton'],
    ['Hilton', 'Hilton'],
    // Marriott portfolio
    ['Residence Inn by Marriott', 'Residence Inn'],
    ['Residence Inn', 'Residence Inn'],
    ['Courtyard by Marriott', 'Courtyard by Marriott'],
    ['Courtyard', 'Courtyard by Marriott'],
    ['SpringHill Suites by Marriott', 'SpringHill Suites'],
    ['SpringHill Suites', 'SpringHill Suites'],
    ['TownePlace Suites by Marriott', 'TownePlace Suites'],
    ['TownePlace Suites', 'TownePlace Suites'],
    ['Fairfield by Marriott', 'Fairfield by Marriott'],
    ['Fairfield', 'Fairfield by Marriott'],
    ['Delta Hotels by Marriott', 'Delta Hotels'],
    ['Four Points by Sheraton', 'Four Points by Sheraton'],
    ['Element by Westin', 'Element'],
    ['Element', 'Element'],
    ['Westin', 'Westin'],
    ['Sheraton', 'Sheraton'],
    ['Aloft', 'Aloft'],
    ['Marriott', 'Marriott'],
    // IHG portfolio
    ['Crowne Plaza', 'Crowne Plaza'],
    ['Holiday Inn Express & Suites', 'Holiday Inn Express'],
    ['Holiday Inn Express', 'Holiday Inn Express'],
    ['Holiday Inn', 'Holiday Inn'],
    ['Staybridge Suites', 'Staybridge Suites'],
    ['Candlewood Suites', 'Candlewood Suites'],
    ['InterContinental', 'InterContinental'],
    // Hyatt portfolio
    ['Hyatt House', 'Hyatt House'],
    ['Hyatt Place', 'Hyatt Place'],
    ['Hyatt Regency', 'Hyatt Regency'],
    ['Park Hyatt', 'Park Hyatt'],
    ['Grand Hyatt', 'Grand Hyatt'],
    // Other chains
    ['Best Western Plus', 'Best Western Plus'],
    ['Best Western', 'Best Western'],
    ['Margaritaville', 'Margaritaville'],
    ['Trailborn', 'Trailborn'],
  ];
  function deriveFlag(name) {
    var n = name || '';
    for (var i = 0; i < FLAG_PATTERNS.length; i++) {
      if (n.toLowerCase().indexOf(FLAG_PATTERNS[i][0].toLowerCase()) >= 0) return FLAG_PATTERNS[i][1];
    }
    return 'Independent';
  }

  /* ⚠ ZERO-KEY PROPERTY — Hotel Rumbao Parking Structure is a garage carrying
     its own property number on compliance's roster. It counts as a property
     and adds nothing to any keys total. */

  /* ⚠ UNCONFIRMED ROOM COUNTS — the DLP Property List loan tape carries no
     "# of Rooms" column, so the seven properties below were added with ESTIMATED keys.
     They are NOT STR-sourced like every other row. Replace with management's figures
     before these totals reach an investor-facing deck. Each is also flagged at runtime
     as hotel.roomsUnconfirmed === true. Longmont (109) and TownePlace Roswell (49) are
     sourced and are deliberately NOT on this list. */
  var UNCONFIRMED_ROOMS = [
    'Courtyard Phoenix-Mesa Gateway Airport',
    'SpringHill Suites Colorado Springs North/Air Force Academy',
    'Fairfield by Marriott Inn & Suites Roswell',
    'Courtyard Portland East',
    'Fairfield by Marriott Inn & Suites Homestead Florida City',
    'Hilton Garden Inn Louisville Mall of St. Matthews',
    'PUBLIC West Hollywood'
  ];

  var RAW_CSV_DATA = `Hotel Name,Actual Name,City,State,# of Rooms,Own/Operate,Category,Brand,Chain Scale
Margaritaville Beach Resort Playa Flamingo,Margaritaville Beach Resort Playa Flamingo,Guanacaste,Costa Rica,120,Own,Acquisition,Margaritaville,Upscale
Courtyard Miami West/FL Turnpike,Courtyard Miami West/FL Turnpike,Miami,FL,127,Own,Acquisition,Marriott,Upscale
Hilton Cocoa Beach Oceanfront,Hilton Cocoa Beach Oceanfront,Cocoa Beach,FL,295,Own,Acquisition,Hilton,Upper Upscale
"Holiday Inn Express Miami Airport Blue Lagoon Area, an IHG Hotel","Holiday Inn Express Miami Airport Blue Lagoon Area, an IHG Hotel",Miami,FL,122,Operate,Management,IHG,Upper Midscale
DoubleTree by Hilton Miami North I-95,DoubleTree by Hilton Miami North I-95,Miami,FL,174,Operate,Management,Hilton,Upper Upscale
Residence Inn by Marriott Miami West/FL Turnpike,Residence Inn by Marriott Miami West/FL Turnpike,Miami,FL,123,Own,Development,Marriott,Upscale
Crowne Plaza Springfield - Convention Ctr by IHG,Crowne Plaza Springfield - Convention Ctr by IHG,Springfield,IL,288,Own,Acquisition,IHG,Upper Upscale
Holiday Inn Express Springfield Downtown,Holiday Inn Express Springfield Downtown,Springfield,IL,140,Own,Acquisition,IHG,Upper Midscale
DoubleTree by Hilton Miami Doral,DoubleTree by Hilton Miami Doral,Doral,FL,150,Operate,Management,Hilton,Upper Upscale
Tru/Home2 Suites by Hilton Fort Lauderdale Downtown,Tru/Home2 Suites by Hilton Fort Lauderdale Downtown,Ft. Lauderdale,FL,218,Own,Development,Hilton,Upscale
Canopy by Hilton West Palm Beach Downtown,Canopy by Hilton West Palm Beach Downtown,West Palm Beach,FL,150,Own,Development,Hilton,Upper Upscale
Hampton Inn Tropicana,Hampton Inn Tropicana,Las Vegas,NV,322,Own,Acquisition,Hilton,Upper Midscale
Sheraton Dallas Hotel by the Galleria,Sheraton Dallas Hotel by the Galleria,Dallas,TX,317,Own,Acquisition,Marriott,Upper Upscale
Hilton Durham near Duke University,Hilton Durham near Duke University,Durham,NC,196,Own,Acquisition,Hilton,Upper Upscale
Sheraton Park City,Sheraton Park City,Park City,UT,200,Own,Acquisition,Marriott,Upper Upscale
Hampton Inn Daytona Beach/Beachfront,Hampton Inn Daytona Beach/Beachfront,Daytona Beach,FL,91,Own,Acquisition,Hilton,Upper Midscale
Holiday Inn Express Doral Miami by IHG,Holiday Inn Express Doral Miami by IHG,Doral,FL,75,Operate,Management,IHG,Upper Midscale
Margaritaville Lake Resort Lake of the Ozarks,Margaritaville Lake Resort Lake of the Ozarks,Osage Beach,MO,520,Own,Acquisition,Margaritaville,Upscale
The Saratoga Hilton,The Saratoga Hilton,Saratoga Springs,NY,242,Own,Acquisition,Hilton,Upper Upscale
Hilton Dallas/Rockwall Lakefront,Hilton Dallas/Rockwall Lakefront,Rockwall,TX,233,Own,Acquisition,Hilton,Upper Upscale
Sheraton Detroit Novi Hotel,Sheraton Detroit Novi Hotel,Novi,MI,238,Own,Acquisition,Marriott,Upper Upscale
TownePlace Suites by Marriott Miami Kendall West,TownePlace Suites by Marriott Miami Kendall West,Miami,FL,116,Operate,Management,Marriott,Upscale
Canopy by Hilton Tempe Downtown,Canopy by Hilton Tempe Downtown,Tempe,AZ,198,Own,Development,Hilton,Upper Upscale
The Westin Tysons Corner,The Westin Tysons Corner,Falls Church,VA,407,Own,Acquisition,Marriott,Upper Upscale
Crowne Plaza Melbourne-Oceanfront by IHG,Crowne Plaza Melbourne-Oceanfront by IHG,Melbourne,FL,290,Own,Acquisition,IHG,Upper Upscale
Houston Marriott North,Houston Marriott North,Houston,TX,390,Own,Acquisition,Marriott,Upper Upscale
Hilton Houston North,Hilton Houston North,Houston,TX,480,Own,Acquisition,Hilton,Upper Upscale
Fairfield by Marriott Inn & Suites Atlanta Buckhead,Fairfield by Marriott Inn & Suites Atlanta Buckhead,Atlanta,GA,115,Own,Acquisition,Marriott,Upper Midscale
Fairfield by Marriott Inn & Suites Atlanta Perimeter Center,Fairfield by Marriott Inn & Suites Atlanta Perimeter Center,Atlanta,GA,115,Own,Acquisition,Marriott,Upper Midscale
San Diego Marriott Mission Valley,San Diego Marriott Mission Valley,San Diego,CA,353,Own,Acquisition,Marriott,Upper Upscale
Staybridge Suites Wilmington Downtown by IHG,Staybridge Suites Wilmington Downtown by IHG,Wilmington,DE,134,Own,Acquisition,IHG,Upscale
Fairfield by Marriott Inn & Suites Winchester,Fairfield by Marriott Inn & Suites Winchester,Winchester,VA,85,Operate,Management,Marriott,Upper Midscale
Tru by Hilton Jacksonville South Mandarin,Tru by Hilton Jacksonville South Mandarin,Jacksonville,FL,106,Operate,Management,Hilton,Upper Midscale
Tru/Home2 Suites by Hilton Pompano Beach Pier,Tru/Home2 Suites by Hilton Pompano Beach Pier,Pompano Beach,FL,150,Operate,Management,Hilton,Upscale
Miami International Airport Hotel,Miami International Airport Hotel,Miami,FL,262,Operate,Management,Independent,Midscale
Hilton Dallas/Southlake Town Square,Hilton Dallas/Southlake Town Square,Southlake,TX,248,Own,Acquisition,Hilton,Upper Upscale
"The Chifley Houston, Tapestry Collection by Hilton","The Chifley Houston, Tapestry Collection by Hilton",Houston,TX,284,Operate,Management,Hilton,Upper Upscale
Hilton Fairfax,Hilton Fairfax,Fairfax,VA,316,Own,Acquisition,Hilton,Upper Upscale
"Hotel Rumbao, a Tribute Portfolio Hotel","Hotel Rumbao, a Tribute Portfolio Hotel",San Juan,PR,240,Own,Acquisition,Marriott,Upper Upscale
"Hotel Vesper, Houston, a Tribute Portfolio Hotel","Hotel Vesper, Houston, a Tribute Portfolio Hotel",Houston,TX,131,Own,Acquisition,Marriott,Upper Upscale
Sheraton Pittsburgh Hotel at Station Square,Sheraton Pittsburgh Hotel at Station Square,Pittsburgh,PA,399,Own,Acquisition,Marriott,Upper Upscale
"The Scottsdale Resort and Spa, Curio Collection by Hilton","The Scottsdale Resort and Spa, Curio Collection by Hilton",Scottsdale,AZ,278,Own,Acquisition,Hilton,Upper Upscale
Holiday Inn Express & Suites Orlando International Airport by IHG,Holiday Inn Express & Suites Orlando International Airport by IHG,Orlando,FL,107,Operate,Management,IHG,Upper Midscale
Holiday Inn Express & Suites Kendall East - Miami,Holiday Inn Express & Suites Kendall East - Miami,Miami,FL,66,Operate,Management,IHG,Upper Midscale
Hilton Appleton Paper Valley,Hilton Appleton Paper Valley,Appleton,WI,388,Operate,Management,Hilton,Upper Upscale
"Wylie Hotel Atlanta, Tapestry Collection by Hilton","Wylie Hotel Atlanta, Tapestry Collection by Hilton",Atlanta,GA,111,Operate,Management,Hilton,Upper Upscale
Element Melbourne Oceanfront,Element Melbourne Oceanfront,Melbourne,FL,130,Own,Development,Marriott,Upscale
Four Points by Sheraton Tallahassee Downtown,Four Points by Sheraton Tallahassee Downtown,Tallahassee,FL,164,Operate,Management,Marriott,Upscale
Hilton Dallas/Plano Granite Park,Hilton Dallas/Plano Granite Park,Plano,TX,299,Own,Acquisition,Hilton,Upper Upscale
Fairfield by Marriott Inn & Suites Alamogordo,Fairfield by Marriott Inn & Suites Alamogordo,Alamogordo,NM,73,Operate,Management,Marriott,Upper Midscale
Hilton Raleigh North Hills,Hilton Raleigh North Hills,Raleigh,NC,333,Operate,Management,Hilton,Upper Upscale
Hampton Inn Ft. Lauderdale Airport North Cruise Port,Hampton Inn Ft. Lauderdale Airport North Cruise Port,Ft. Lauderdale,FL,109,Operate,Management,Hilton,Upper Midscale
"Candlewood Suites Miami Doral, an IHG Hotel","Candlewood Suites Miami Doral, an IHG Hotel",Miami,FL,94,Operate,Management,IHG,Midscale
Marriott Raleigh Durham Research Triangle Park,Marriott Raleigh Durham Research Triangle Park,Durham,NC,225,Own,Acquisition,Marriott,Upper Upscale
SpringHill Suites by Marriott Fairfax Fair Oaks,SpringHill Suites by Marriott Fairfax Fair Oaks,Fairfax,VA,140,Operate,Management,Marriott,Upscale
"The Radical Asheville, Tapestry Collection by Hilton","The Radical Asheville, Tapestry Collection by Hilton",Asheville,NC,71,Operate,Management,Hilton,Upper Upscale
Hyatt Place Bentonville/Rogers,Hyatt Place Bentonville/Rogers,Rogers,AR,103,Operate,Management,Hyatt,Upscale
Hilton Washington DC/Rockville Hotel & Executive Meeting Ctr,Hilton Washington DC/Rockville Hotel & Executive Meeting Ctr,Rockville,MD,315,Own,Acquisition,Hilton,Upper Upscale
Delta Hotels by Marriott Nashville Airport,Delta Hotels by Marriott Nashville Airport,Nashville,TN,200,Operate,Management,Marriott,Upscale
Hilton Garden Inn Atlanta North/Alpharetta,Hilton Garden Inn Atlanta North/Alpharetta,Alpharetta,GA,164,Operate,Management,Hilton,Upscale
Hampton Inn & Suites Clermont,Hampton Inn & Suites Clermont,Clermont,FL,87,Operate,Management,Hilton,Upper Midscale
Fairfield by Marriott Inn & Suites Orlando Near Universal Orlando Resort,Fairfield by Marriott Inn & Suites Orlando Near Universal Orlando Resort,Orlando,FL,116,Operate,Management,Marriott,Upper Midscale
Hampton Inn & Suites Stuart-North,Hampton Inn & Suites Stuart-North,Stuart,FL,102,Operate,Management,Hilton,Upper Midscale
Marriott Albany,Marriott Albany,Albany,NY,360,Operate,Management,Marriott,Upper Upscale
Sheraton San Jose Silicon Valley,Sheraton San Jose Silicon Valley,Milpitas,CA,229,Operate,Management,Marriott,Upper Upscale
DoubleTree by Hilton Hilton Head Island,DoubleTree by Hilton Hilton Head Island,Hilton Head Island,SC,77,Operate,Management,Hilton,Upper Upscale
Courtyard by Marriott Dallas Richardson at Spring Valley,Courtyard by Marriott Dallas Richardson at Spring Valley,Richardson,TX,149,Operate,Management,Marriott,Upscale
Courtyard by Marriott Chicago St. Charles,Courtyard by Marriott Chicago St. Charles,St. Charles,IL,121,Operate,Management,Marriott,Upscale
Courtyard by Marriott Fort Lauderdale Weston,Courtyard by Marriott Fort Lauderdale Weston,Weston,FL,176,Own,Acquisition,Marriott,Upscale
InterContinental Kansas City at the Plaza,InterContinental Kansas City at the Plaza,Kansas City,MO,371,Operate,Management,IHG,Luxury
Sheraton Dallas Hotel,Sheraton Dallas Hotel,Dallas,TX,1841,Lending,Lending,Marriott,Upper Upscale
Courtyard by Marriott Miami Airport,Courtyard by Marriott Miami Airport,Miami,FL,301,Lending,Lending,Marriott,Upscale
Marriott Miami Airport,Marriott Miami Airport,Miami,FL,371,Lending,Lending,Marriott,Upper Upscale
Residence Inn by Marriott Miami Airport,Residence Inn by Marriott Miami Airport,Miami,FL,164,Lending,Lending,Marriott,Upscale
The Westin New Orleans,The Westin New Orleans,New Orleans,LA,462,Lending,Lending,Marriott,Upper Upscale
Courtyard by Marriott Manchester-Boston Regional Airport,Courtyard by Marriott Manchester-Boston Regional Airport,Manchester,NH,139,Lending,Lending,Marriott,Upscale
Homewood Suites by Hilton Manchester/Airport,Homewood Suites by Hilton Manchester/Airport,Manchester,NH,131,Lending,Lending,Hilton,Upscale
SpringHill Suites by Marriott Manchester-Boston Regional Airport,SpringHill Suites by Marriott Manchester-Boston Regional Airport,Manchester,NH,100,Lending,Lending,Marriott,Upscale
Homewood Suites by Hilton Portsmouth,Homewood Suites by Hilton Portsmouth,Portsmouth,NH,116,Lending,Lending,Hilton,Upscale
Residence Inn by Marriott Boston Franklin,Residence Inn by Marriott Boston Franklin,Franklin,MA,108,Lending,Lending,Marriott,Upscale
Residence Inn by Marriott Salt Lake City Downtown,Residence Inn by Marriott Salt Lake City Downtown,Salt Lake City,UT,189,Lending,Lending,Marriott,Upscale
Boston Raffles (Boston Ultra Luxury Hotel),Boston Raffles,Boston,MA,147,Lending,Lending,Accor,Luxury
Dalmar (Ft. Lauderdale Dual-Brand Hotel),The Dalmar & Element Fort Lauderdale Downtown,Ft. Lauderdale,FL,323,Lending,Lending,Marriott,Upper Upscale
Element by Westin Mission Valley,Element by Westin Mission Valley,San Diego,CA,148,Own,Development,Marriott,Upscale
Riverside Wharf Miami,Riverside Wharf Miami,Miami,FL,167,Own,In Development,Independent,Luxury
Westin Cocoa Beach Resort & Spa,Westin Cocoa Beach Resort & Spa,Cocoa Beach,FL,502,Own,In Development,Marriott,Upper Upscale
Courtyard Phoenix-Mesa Gateway Airport,Courtyard Phoenix-Mesa Gateway Airport,Mesa,AZ,130,Lending,Lending,Marriott,Upscale
SpringHill Suites Colorado Springs North/Air Force Academy,SpringHill Suites Colorado Springs North/Air Force Academy,Colorado Springs,CO,106,Lending,Lending,Marriott,Upscale
TownePlace Suites Roswell,TownePlace Suites Roswell,Roswell,NM,49,Lending,Lending,Marriott,Upper Midscale
Hotel Rumbao Parking Structure,Hotel Rumbao Parking Structure,San Juan,PR,0,Own,Acquisition,Marriott,Upper Upscale
Sheraton North Houston at George Bush Intercontinental,Sheraton North Houston at George Bush Intercontinental,Houston,TX,419,Operate,Management,Marriott,Upper Upscale
Courtyard by Marriott Dallas Plano Parkway at Preston Road,Courtyard by Marriott Dallas Plano Parkway at Preston Road,Plano,TX,149,Operate,Management,Marriott,Upscale
Holiday Inn Express North Palm Beach-Oceanview by IHG,Holiday Inn Express North Palm Beach-Oceanview by IHG,Juno Beach,FL,108,Operate,Management,IHG,Upper Midscale
"Zelda Dearest, an SLH Hotel","Zelda Dearest, an SLH Hotel",Asheville,NC,20,Operate,Management,Independent,Luxury
Fairfield by Marriott Inn & Suites Roswell,Fairfield by Marriott Inn & Suites Roswell,Roswell,NM,62,Lending,Lending,Marriott,Upper Midscale
Home2 Suites by Hilton Longmont,Home2 Suites by Hilton Longmont,Longmont,CO,109,Lending,Lending,Hilton,Upper Midscale
Courtyard Portland East,Courtyard Portland East,Portland,OR,124,Lending,Lending,Marriott,Upscale
Fairfield by Marriott Inn & Suites Homestead Florida City,Fairfield by Marriott Inn & Suites Homestead Florida City,Florida City,FL,105,Lending,Lending,Marriott,Upper Midscale
Hilton Garden Inn Louisville Mall of St. Matthews,Hilton Garden Inn Louisville Mall of St. Matthews,Louisville,KY,116,Lending,Lending,Hilton,Upscale
PUBLIC West Hollywood,PUBLIC West Hollywood,West Hollywood,CA,137,Lending,Lending,Independent,Luxury`;

  var CATEGORY_COLORS = {
    'Acquisition':    '#2468A8',  /* --strat-acquisitions  ocean blue      */
    'Management':     '#5B6B7D',  /* --strat-dhm           slate (DHM)     */
    'Development':    '#C0664B',  /* --strat-development   terracotta      */
    'In Development': '#D69B84',  /* light terracotta — pre-open           */
    'Lending':        '#0E9E84',  /* --strat-credit        teal            */
    'Unknown':        '#A9B2BE'
  };
  var CATEGORY_LABELS = {
    'Management': 'Management', 'Acquisition': 'Acquisitions', 'Development': 'Dev',
    'In Development': 'Pre-opening', 'Lending': 'Credit', 'Unknown': 'Unknown'
  };
  var CATEGORY_ORDER = ['Acquisition', 'Management', 'Development', 'In Development', 'Lending'];

  function parseCSVLine(str) {
    var result = [], current = '', inQuote = false;
    for (var i = 0; i < str.length; i++) {
      var ch = str[i];
      if (ch === '"') inQuote = !inQuote;
      else if (ch === ',' && !inQuote) { result.push(current.trim()); current = ''; }
      else current += ch;
    }
    result.push(current.trim());
    return result;
  }

  function parseHotels(csv) {
    var lines = csv.split('\n');
    var headers = parseCSVLine(lines[0]).map(function (h) { return h.trim(); });
    var hotels = [];
    for (var i = 1; i < lines.length; i++) {
      var line = lines[i];
      if (!line.trim()) continue;
      var values = parseCSVLine(line);
      if (values.length < 5) continue;
      var raw = {};
      headers.forEach(function (h, idx) {
        if (values[idx] != null) raw[h] = values[idx].replace(/^"|"$/g, '');
      });
      var name = raw['Hotel Name'] || 'Unknown Hotel';
      var city = raw['City'] || '';
      var state = raw['State'] || '';
      var coords = PROPERTY_COORDINATES[name] || CITY_COORDINATES[city + ', ' + state] || { lat: 37.0902, lng: -95.7129 };
      var category = raw['Category'] || 'Unknown';
      if (!CATEGORY_COLORS[category]) category = 'Unknown';
      hotels.push({
        id: 'hotel-' + i,
        name: name,
        actualName: raw['Actual Name'] || name,
        city: city,
        state: state,
        rooms: parseInt(raw['# of Rooms'] || '0', 10) || 0,
        type: raw['Own/Operate'] || '',
        category: category,
        roomsUnconfirmed: UNCONFIRMED_ROOMS.indexOf(name) >= 0,
        // Property-count weight: 2 for a dual-brand CoStar lists twice, else 1.
        // Every property count sums `units`; keys always sum `rooms`.
        units: DUAL_BRANDED[name] ? 2 : 1,
        dualFlags: DUAL_BRANDED[name] ? DUAL_BRANDED[name].flags.slice() : null,
        brand: raw['Brand'] || 'Independent',
        flag: deriveFlag(raw['Actual Name'] || raw['Hotel Name'] || ''),
        chainScale: raw['Chain Scale'] || 'Unclassified',
        lat: coords.lat,
        lng: coords.lng
      });
    }
    return hotels;
  }

  // ── Market names ────────────────────────────────────────────────────────
  // Investors think in markets, not municipalities. Suburbs collapse into the
  // metro they belong to so one metro reads as one dot; genuinely distinct
  // resort and secondary markets stay separate. Values are the label drawn on
  // the map. Anything absent falls through to "City, ST".
  var MARKETS = {
    'Fairfax|VA': 'Northern Virginia', 'Falls Church|VA': 'Northern Virginia',
    'Rockville|MD': 'Washington, D.C.',
    'Durham|NC': 'Raleigh\u2013Durham', 'Raleigh|NC': 'Raleigh\u2013Durham',
    'Atlanta|GA': 'Atlanta', 'Alpharetta|GA': 'Atlanta',
    'Dallas|TX': 'Dallas\u2013Fort Worth', 'Plano|TX': 'Dallas\u2013Fort Worth',
    'Richardson|TX': 'Dallas\u2013Fort Worth', 'Rockwall|TX': 'Dallas\u2013Fort Worth',
    'Southlake|TX': 'Dallas\u2013Fort Worth',
    'Scottsdale|AZ': 'Phoenix\u2013Scottsdale', 'Tempe|AZ': 'Phoenix\u2013Scottsdale',
    'Mesa|AZ': 'Phoenix\u2013Scottsdale',
    'Miami|FL': 'Miami', 'Doral|FL': 'Miami',
    'Ft. Lauderdale|FL': 'Ft. Lauderdale', 'Pompano Beach|FL': 'Ft. Lauderdale',
    'Weston|FL': 'Ft. Lauderdale',
    'Orlando|FL': 'Orlando', 'Clermont|FL': 'Orlando',
    'Florida City|FL': 'Homestead',
    'Osage Beach|MO': 'Lake of the Ozarks',
    'East Elmhurst|NY': 'New York',
    'St. Charles|IL': 'Chicago',
    'San Jose|CA': 'San Jose', 'Milpitas|CA': 'San Jose',
    'Bentonville|AR': 'Bentonville', 'Rogers|AR': 'Bentonville',
    'West Palm Beach|FL': 'West Palm Beach', 'Juno Beach|FL': 'West Palm Beach',
    'Boston|MA': 'Boston', 'Franklin|MA': 'Boston',
    'Novi|MI': 'Detroit',
    'Longmont|CO': 'Boulder',
    // Disambiguated because the bare city name reads as an unknown small town
    'Springfield|IL': 'Springfield, IL',
    'Manchester|NH': 'Manchester, NH'
  };

  function marketFor(city, state) {
    var k = (city || '') + '|' + (state || '');
    if (MARKETS[k]) return MARKETS[k];
    // Bare city name is the house form on maps; the table above carries the
    // handful that need a state to be unambiguous.
    return city || state || '';
  }

  /* DATA_SERIAL — bump on every roster edit. _ds_bundle.js carries a compiled
     copy of this file, and the bundle is rebuilt at the end of a turn, so a
     page can load a stale embedded copy alongside this fresh one. The guard
     below means the NEWER serial always wins regardless of load order, and
     'dwdata:changed' tells <dw-stat> and <dw-map> to re-read. */
  var DATA_SERIAL = 20260918;
  if (window.__MAPDATA && (window.__MAPDATA.DATA_SERIAL || 0) >= DATA_SERIAL) return;

  window.__MAPDATA = {
    DATA_SERIAL: DATA_SERIAL,
    HOTELS: parseHotels(RAW_CSV_DATA),
    UNCONFIRMED_ROOMS: UNCONFIRMED_ROOMS,
    CATEGORY_COLORS: CATEGORY_COLORS,
    CATEGORY_LABELS: CATEGORY_LABELS,
    CATEGORY_ORDER: CATEGORY_ORDER,
    PROPERTY_COORDINATES: PROPERTY_COORDINATES,
    CITY_COORDINATES: CITY_COORDINATES,
    MARKETS: MARKETS,
    marketFor: marketFor,
    DUAL_BRANDED: DUAL_BRANDED,
    // Count properties the way CoStar does: dual-brands count twice.
    // Use this instead of hotels.length anywhere a property count is shown.
    countProperties: function (hotels) {
      return (hotels || []).reduce(function (n, h) { return n + (h.units || 1); }, 0);
    },
    EQUITY_CATEGORIES: ['Acquisition', 'Management', 'Development'],
    DATA_AS_OF: 'September 1, 2026'
  };
  try { window.dispatchEvent(new CustomEvent('dwdata:changed')); } catch (e) {}
})();
