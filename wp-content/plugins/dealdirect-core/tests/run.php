<?php
// Unit tests for DealDirect\Submission (no WordPress needed). Run: php tests/run.php
require __DIR__ . '/../includes/class-submission.php';
require __DIR__ . '/../includes/i18n.php';
require __DIR__ . '/../includes/seo.php';
require __DIR__ . '/../includes/retired.php';
require __DIR__ . '/../includes/tracking.php';
use DealDirect\Submission as S;

$fail = 0;
function check( string $name, bool $ok ) { global $fail; echo ( $ok ? 'ok   ' : 'FAIL ' ) . $name . "\n"; $fail |= ! $ok; }

$host = 'wordpress-1077248-6717515.cloudwaysapps.com';
$page = "https://$host/offering/riverside-wharf-preferred-equity/";
$reg  = [
	'form'     => 'registration',
	'fields'   => [ 'accredited_investor' => 'networth', 'firstname' => 'Ana', 'lastname' => 'Diaz', 'email' => 'Ana@Example.com', 'phone' => '+1 305 555 0100' ],
	'consent'  => [ 'agreed' => true, 'text' => 'I consent to Driftwood Capital storing and processing my personal information' ],
	'utm'      => [ 'utm_source' => 'google', 'utm_medium' => '', 'evil' => 'x' ],
	'hutk'     => str_repeat( 'a', 32 ),
	'pageUri'  => $page,
	'pageName' => 'Riverside Wharf Preferred Equity',
];

$v = S::validate( $reg, $host );
check( 'registration validates', $v['ok'] === true );
check( 'email lower-cased', $v['fields']['email'] === 'ana@example.com' );
check( 'accreditation mapped to exact HubSpot string', $v['fields']['accredited_investor'] === 'Net worth exceeding $1 million excluding primary home' );
check( 'only known, non-empty UTMs kept', $v['utm'] === [ 'utm_source' => 'google' ] );

$p = S::payload( $v );
$names = array_column( $p['fields'], 'name' );
check( 'payload has form fields + utm', $names === [ 'accredited_investor', 'firstname', 'lastname', 'email', 'phone', 'utm_source' ] );
check( 'context carries offering pageUri, pageName, hutk', $p['context'] === [ 'pageUri' => $page, 'pageName' => 'Riverside Wharf Preferred Equity', 'hutk' => str_repeat( 'a', 32 ) ] );
$subs = array_column( $p['legalConsentOptions']['consent']['communications'], 'subscriptionTypeId' );
check( 'registration opts in to Marketing Information + One to One', $subs === [ 7195048, 3199624 ] );
check( 'consent text is the text shown', $p['legalConsentOptions']['consent']['text'] === $reg['consent']['text'] && $p['legalConsentOptions']['consent']['consentToProcess'] === true );
check( 'subscription override drops One to One', array_column( S::payload( $v, [ 7195048 ] )['legalConsentOptions']['consent']['communications'], 'subscriptionTypeId' ) === [ 7195048 ] );
check( 'endpoint uses portal + form GUID', S::endpoint( 'registration' ) === 'https://api.hsforms.com/submissions/v3/integration/secure/submit/2951523/f45b7940-7408-4669-acb0-c38ec1107137' );

$none = $reg; $none['fields']['accredited_investor'] = 'none';
$r = S::validate( $none, $host );
check( '"none of the above" is refused (never sent)', ! $r['ok'] && $r['code'] === 'not_accredited' );

$bad = $reg; $bad['fields']['accredited_investor'] = 'millionaire';
check( 'unknown accreditation value refused', S::validate( $bad, $host )['code'] === 'bad_value' );

$noc = $reg; $noc['consent']['agreed'] = false;
check( 'registration without consent refused', S::validate( $noc, $host )['code'] === 'consent_required' );

$miss = $reg; unset( $miss['fields']['phone'] );
$r = S::validate( $miss, $host );
check( 'missing required field named', $r['code'] === 'missing_field' && $r['field'] === 'phone' );

$em = $reg; $em['fields']['email'] = 'not-an-email';
check( 'bad email refused', S::validate( $em, $host )['code'] === 'bad_email' );

$off = $reg; $off['pageUri'] = 'https://evil.example/offering/x/';
check( 'pageUri on another host refused', S::validate( $off, $host )['code'] === 'bad_page' );
$js = $reg; $js['pageUri'] = "javascript://$host/";
check( 'non-http pageUri refused', S::validate( $js, $host )['code'] === 'bad_page' );

$hk = $reg; $hk['hutk'] = '<script>';
check( 'malformed hutk dropped', S::validate( $hk, $host )['hutk'] === '' );

$unk = $reg; $unk['form'] = 'newsletter';
check( 'unknown form refused', S::validate( $unk, $host )['code'] === 'unknown_form' );

$long = $reg; $long['fields']['firstname'] = str_repeat( 'x', 201 );
check( 'over-long field refused', S::validate( $long, $host )['code'] === 'too_long' );

$extra = $reg; $extra['fields']['lifecyclestage'] = 'customer';
$r = S::validate( $extra, $host );
check( 'fields not in the form are dropped', $r['ok'] && ! isset( $r['fields']['lifecyclestage'] ) );

$eb5 = [
	'form'    => 'eb5',
	'fields'  => [ 'accredited_investor' => 'inc', 'firstname' => 'João', 'lastname' => 'Silva', 'email' => 'j@example.com', 'phone' => '+55 11 5555 0100',
	               'country' => 'Brazil', 'preferred_contact_method' => 'WhatsApp', 'eb5_amount_acknowledgement' => true, 'page_language' => 'pt-BR' ],
	'consent' => [ 'agreed' => true, 'text' => 'Eu concordo' ],
	'pageUri' => "https://$host/investimentos-eb-5/",
];
$v = S::validate( $eb5, $host );
check( 'eb5 validates (unicode names, bool acknowledgement)', $v['ok'] && $v['fields']['eb5_amount_acknowledgement'] === 'true' && $v['fields']['firstname'] === 'João' );
check( 'eb5 inc maps to income string', $v['fields']['accredited_investor'] === 'annual income exceeding $200,000' );
check( 'eb5 opts in to EB-5 Onboarding + Marketing + One to One', array_column( S::payload( $v )['legalConsentOptions']['consent']['communications'], 'subscriptionTypeId' ) === [ 105452959, 7195048, 3199624 ] );
check( 'no hutk -> no hutk in context', ! isset( S::payload( $v )['context']['hutk'] ) );

$ack = $eb5; $ack['fields']['eb5_amount_acknowledgement'] = false;
check( 'eb5 without $800k acknowledgement refused', S::validate( $ack, $host )['code'] === 'missing_field' );
$cm = $eb5; $cm['fields']['preferred_contact_method'] = 'Telegrama';
check( 'eb5 contact method must be an English HubSpot value', S::validate( $cm, $host )['code'] === 'bad_value' );
$cm2 = $eb5; unset( $cm2['fields']['preferred_contact_method'] );
check( 'eb5 contact method optional', S::validate( $cm2, $host )['ok'] );

$or = [ 'form' => 'offering-request', 'fields' => [ 'email' => 'ana@example.com', 'firstname' => 'ignored' ], 'pageUri' => $page, 'pageName' => 'RW' ];
$v = S::validate( $or, $host );
check( 'offering-request needs only email, no consent', $v['ok'] && array_keys( $v['fields'] ) === [ 'email' ] );
check( 'offering-request payload has no consent block', ! isset( S::payload( $v )['legalConsentOptions'] ) );

check( 'HubSpot invalid email -> plain message', S::hubspot_error( 400, '{"errors":[{"errorType":"INVALID_EMAIL"}]}' ) === 'Please enter a valid email address.' );
check( 'HubSpot unknown error -> generic message', str_starts_with( S::hubspot_error( 500, 'oops' ), 'We could not send' ) );
check( 'subscription error detected', S::is_subscription_error( '{"errors":[{"message":"Invalid subscription type id 3199624"}]}' ) );
check( 'other error is not a subscription error', ! S::is_subscription_error( '{"errors":[{"message":"Required field email missing"}]}' ) );

$h = \DealDirect\hreflang_links( 'https://example.com/' );
check( 'hreflang group: en, es, pt-BR + x-default', array_keys( $h ) === [ 'en', 'es', 'pt-BR', 'x-default' ] );
check( 'x-default is the EN page', $h['x-default'] === 'https://example.com/eb-5-investments/' && $h['es'] === 'https://example.com/inversiones-eb-5/' );
check( 'PT page lang is pt-BR', \DealDirect\page_lang( 'investimentos-eb-5' ) === 'pt-BR' );
check( 'other pages keep the site language', \DealDirect\page_lang( 'new-eb-5-page' ) === null && \DealDirect\page_lang( 'home' ) === null );

check( 'SEO title: live pattern by default', \DealDirect\seo_title( 'EB-5 Investments', [] ) === 'EB-5 Investments - Driftwood Capital | DealDirect' );
check( 'SEO title: page override wins', \DealDirect\seo_title( 'X – Y', [ 'title' => 'X - Y - Driftwood Capital | DealDirect' ] ) === 'X - Y - Driftwood Capital | DealDirect' );
check( 'robots string -> wp_robots directives', \DealDirect\robots_directives( 'follow, noindex, max-snippet:-1' ) === [ 'follow' => true, 'noindex' => true, 'max-snippet' => '-1' ] );

check( 'retired login pages answer 410', \DealDirect\is_retired_path( '/forgot-password/' ) && \DealDirect\is_retired_path( '/admin-login?redirect=x' ) );
check( 'other paths are not retired', ! \DealDirect\is_retired_path( '/eb-5-investments/' ) && ! \DealDirect\is_retired_path( '/forgot-password/extra/' ) );
check( 'old Riverside Wharf URL -> QOZ', \DealDirect\redirect_target( '/offering/riverside-wharf/' ) === '/offering/riverside-wharf-qoz/' );
check( 'old EB-5 offering URL -> EB-5 page', \DealDirect\redirect_target( '/offering/riverside-wharf-eb-5/?utm_source=x' ) === '/eb-5-investments/' );
check( 'kept URLs are not redirected', \DealDirect\redirect_target( '/offering/riverside-wharf-qoz/' ) === null && \DealDirect\redirect_target( '/eb-5-investments/' ) === null );

check( 'GTM loads on the public (live) site', \DealDirect\gtm_enabled( true, false ) );
check( 'GTM stays off on staging unless forced', ! \DealDirect\gtm_enabled( false, false ) && \DealDirect\gtm_enabled( false, true ) );
check( 'GTM snippet carries the live container', str_contains( \DealDirect\gtm_head( \DealDirect\GTM_ID ), "'GTM-NX8DQZGQ'" ) && str_contains( \DealDirect\gtm_body( 'GTM-NX8DQZGQ' ), 'ns.html?id=GTM-NX8DQZGQ' ) );

exit( $fail );
