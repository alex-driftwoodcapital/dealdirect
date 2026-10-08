# HubSpot setup — portal 2951523

## How we track which offering someone requested
No custom offering field. Every request, whether a long or short form, is a native HubSpot form submission sent from the offering's own page. HubSpot stores the form, page URL, page title and date on each submission, matched to the contact by email.

List for one offering: Lists → Contact-based → Filter "Form submission" → any of the three DealDirect forms → refine "Page URL contains `<offering-slug>`".

Rule: every request must be submitted from the offering's own URL. The home page QOZ "Get notified" box links to `/riverside-wharf-qoz/`, or the site sends that page's URL as `pageUri`.

## 1. Properties (Settings → Data Management → Properties, group "DealDirect")
Reuse existing properties if the current Bricks integration already writes them. Search before creating.

| Label | Internal name | Type | Options (label = value) |
|---|---|---|---|
| Accredited investor status | `dd_accreditation` | Dropdown | Annual income exceeds $200K (for the last 2 years) · Joint household income greater than $300k (for the last 2 years) · Net worth exceeding $1M (excluding primary home) · None of the above |
| Preferred contact method | `dd_contact_method` | Dropdown | Email · Phone · Video Call · WhatsApp |
| EB-5 $800,000 acknowledgement | `eb5_investment_ack` | Single checkbox | — |

Built-in properties used as is: first name, last name, email, phone, country.
The EB-5 page shows only 3 of the 4 accreditation options (no joint income). It uses the same property.

## 2. Forms (Marketing → Forms → Create → Embedded → Blank; never embedded on the site)
| Form | Fields (* required) |
|---|---|
| DealDirect – Registration | accreditation*, first name*, last name*, email*, phone*, consent* |
| DealDirect – Offering Request | email* |
| DealDirect – EB-5 Registration | accreditation*, first name*, last name*, email*, phone*, country*, contact method, $800,000 acknowledgement*, consent* |

Country: the site sends the country name as text. Leave HubSpot's Country as single-line text, or match the option list exactly.

## 3. Consent
Settings → Marketing → Email → Subscription types: create or confirm "DealDirect offerings" and note its ID.
On the Registration and EB-5 forms, go to Options → Data privacy & consent → "Consent checkbox for communications; form submit as consent to process" → choose that subscription → mark required.
Paste the site text exactly:
- Registration: "I consent to Driftwood Capital storing and processing my personal information and communicating with me via email, call, or text (SMS). I have read and agree to the Terms of Use and Privacy Policy"
- EB-5: same text without "(SMS)". Confirm with compliance which version is correct and use one.
- Portuguese and Spanish EB-5 pages send their translated text through the API. Compliance should approve those strings.

## 4. Workflow
Use the existing follow-up workflow. Add an enrollment trigger: "Form submission → any of the three DealDirect forms". No new properties are written.
Optional: create one Deal per submission, named `{contact} – {conversion page title}`, if IR wants a per-request pipeline view.

## 5. Send to developer
Received:
- Subscription type IDs: Marketing Information = `7195048` · EB-5 Onboarding = `105452959` · One to One = `3199624` · Investor Relations `8656352` not used for leads
- Opt-ins per form: Registration → Marketing Information + One to One · EB-5 Registration → EB-5 Onboarding + Marketing Information + One to One. Each goes in the `communications` array with `value: true`.
- One to One is a HubSpot internal type: sales 1:1 emails already reach contacts who haven't unsubscribed from it, and HubSpot may ignore an opt-in for it through the form. Test on staging. If it's rejected, drop it from the payload; nothing is lost.
- Registration form GUID: `f45b7940-7408-4669-acb0-c38ec1107137` (portal 2951523, region na1)
- EB-5 Registration form GUID: `93d3de43-8296-4dae-afc1-c9e12699389b`. Fields: `accredited_investor`*, `firstname`*, `lastname`*, `email`*, `phone`*, `country`* (HubSpot dropdown: site must send the exact option value, in English, from PT/ES pages too), `preferred_contact_method` (radio; internal values confirmed = labels: `Email` · `Phone` · `Video Call` · `WhatsApp`; send these from PT/ES pages too), `eb5_amount_acknowledgement`* (single checkbox, required on site and in HubSpot, send `true`), hidden UTMs. Used by the EN/PT/ES EB-5 pages.
- Offering Request form GUID: `3f7d6df4-c356-4d6c-bc04-f9502dd8864b`. Fields: `email`*, hidden `utm_campaign`, `utm_content`, `utm_medium`, `utm_source`, `utm_term`. No consent.
- Registration field names: `accredited_investor`* (dropdown), `firstname`*, `lastname`*, `email`*, `phone`*, hidden `utm_campaign`, `utm_content`, `utm_medium`, `utm_source`, `utm_term`
- `accredited_investor` values. The site's option value goes on the left; send HubSpot the exact string on the right (case and punctuation included):
  - `income` / EB-5 `inc` → `annual income exceeding $200,000`
  - `joint` → `joint household income greater than $300k (for the last 2 years)`
  - `networth` / EB-5 `nw` → `Net worth exceeding $1 million excluding primary home`
  - `none` → never sent (stops at the apology screen)
- Open on Registration: consent setting

Still needed:
- Subscription type IDs. HubSpot's settings screens don't show them; look them up with the private app token: `GET https://api.hubapi.com/communication-preferences/v3/definitions` (scope `communication_preferences.read`). Mapping: Registration → "Marketing Information"; EB-5 Registration → "EB-5 Onboarding" (+ "Marketing Information" if confirmed). "Investor Relations" is not used for leads.
- Three form GUIDs (from the form URL or Embed → copy `formId`)
- Subscription type ID
- Private app token: Settings → Integrations → Private Apps, scopes `forms`, `crm.objects.contacts.read`, `communication_preferences.read`. It goes in `wp-config.php` only, never in chat or Etch.
- Internal names of any existing properties reused instead of the table above

## Consent capture (required on Registration + EB-5)
The site's consent checkbox is required; the form cannot be submitted unchecked.
Every long-form submission must include `legalConsentOptions` with the exact text shown on the page, which records:
- consent to process, with the submission timestamp, the text agreed to and the page URL (stored on the form submission)
- opt-in to the subscription type (ID needed), with a dated entry in the contact's communication subscription history
- the legal basis on the contact
Test: submit on staging, then check the contact → Communication subscriptions → history shows the opt-in with date/time, and the form submission shows the consent text.
The Offering Request form (repeat visitors) sends no consent; the original dated consent stays on the contact.

## UTM capture (site script, all forms)
1. On any page load, read `utm_source`, `utm_medium`, `utm_campaign`, `utm_term`, `utm_content` from the URL.
2. If any are present, save all five to a first-party cookie `dd_utm` (30 days), replacing earlier values (most recent wins). Pages without UTMs leave the cookie alone.
3. On submit, send the cookie's values as the five hidden fields. If no cookie exists, send nothing for them.
Add `dd_utm` to the cookie notice.

## Site behavior (built into the designs)
- **Offering pages** (Riverside Wharf Pref, Riverside Wharf QOZ, and every future offering): every CTA opens an on-page request modal (`#request`). Never link to the home page, or the submission logs the home URL.
  - New visitor → 2-step Registration form (`data-hs-form="registration"`).
  - Returning visitor (`dd_lead` cookie) → "Confirm your email" → Offering Request form (`data-hs-form="offering-request"`). "Not registered yet?" clears the cookie and opens Registration.
  - Both submit with `pageUri` = the offering page URL.
- **Home page QOZ "Get notified"**: button opens the Registration dialog (new visitor) or the Confirm-email dialog (`dd_lead` present → Offering Request). Both submit with `pageUri` = `/riverside-wharf-qoz/`, `pageName` = "Riverside Wharf QOZ". No inline email field on the card.
- **Home page "Start Investing" / Sign Up** (no offering) → Registration with `pageUri` = home URL.
- **EB-5 pages** → EB-5 Registration form, `pageUri` = that language's page URL.
- Input `name` attributes match HubSpot internal names; map `accredited_investor` values per the table above.
- `dd_lead` cookie: 365 days, set after a successful Registration or EB-5 submission; holds a hashed contact ID, never form answers.

## Non-accredited visitors
If accreditation = "None of the above", the form stops at step 1 and shows the "Our apologies" screen (accredited investors only). Nothing is submitted to HubSpot, and the remaining steps can't be reached. Confirmed: non-accredited visitors are never sent to HubSpot. No form, no partial submission, no email capture. This applies to the Registration form and all three EB-5 forms. The existing designs already do this.

## WP REST endpoint (server side; token never in Etch or JS)
`POST /wp-json/dealdirect/v1/submit` with `{ form: registration|offering-request|eb5, fields, consent, utm, hutk, pageUri, pageName }`
- Token: `DD_HUBSPOT_TOKEN` in `wp-config.php`.
- Offering Request: look up the email (CRM v3 contacts search). Registered → submit, return `sent`. Unknown → return `needs_registration`; the dialog switches to Registration with the email pre-filled.
- Map `accredited_investor` site values → HubSpot values server-side; reject `none`.
- Nonce + rate limit by IP and email. Return HubSpot validation errors to the dialog in plain language.
- On Registration/EB-5 success set `dd_lead` (365 days, hashed contact ID only). Add it and `dd_utm` to the cookie notice and privacy policy before go-live.

## Developer notes (Forms API payload)
Every submission, including zero-field repeat requests, must send:
`fields: [{name:"email", value}]` plus the form's fields, and
`context: { hutk, pageUri: <offering URL>, pageName: <offering title> }`
to `/submissions/v3/integration/secure/submit/2951523/{formGuid}` with the consent payload on the long forms.
