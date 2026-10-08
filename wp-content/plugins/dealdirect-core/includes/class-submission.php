<?php
/**
 * Pure submission logic for the HubSpot proxy: validation, value mapping and payload building.
 * No WordPress calls, so it is unit-tested in tests/run.php. Spec: handoff/docs/hubspot-setup-steps.md.
 */
namespace DealDirect;

final class Submission {
	const PORTAL = '2951523';

	const FORMS = [
		'registration'     => 'f45b7940-7408-4669-acb0-c38ec1107137',
		'eb5'              => '93d3de43-8296-4dae-afc1-c9e12699389b',
		'offering-request' => '3f7d6df4-c356-4d6c-bc04-f9502dd8864b',
	];

	// Field name => required. Names are HubSpot internal names; the site's inputs use the same names.
	const FIELDS = [
		'registration'     => [ 'accredited_investor' => true, 'firstname' => true, 'lastname' => true, 'email' => true, 'phone' => true ],
		'eb5'              => [ 'accredited_investor' => true, 'firstname' => true, 'lastname' => true, 'email' => true, 'phone' => true,
		                        'country' => true, 'preferred_contact_method' => false, 'eb5_amount_acknowledgement' => true, 'page_language' => false ],
		'offering-request' => [ 'email' => true ],
	];

	const UTM = [ 'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content' ];

	// Site option value => exact HubSpot value. "none" is never sent: the visitor stops at "Our apologies".
	const ACCREDITATION = [
		'income'   => 'annual income exceeding $200,000',
		'inc'      => 'annual income exceeding $200,000',
		'joint'    => 'joint household income greater than $300k (for the last 2 years)',
		'networth' => 'Net worth exceeding $1 million excluding primary home',
		'nw'       => 'Net worth exceeding $1 million excluding primary home',
	];

	const CONTACT_METHODS = [ 'Email', 'Phone', 'Video Call', 'WhatsApp' ];

	// Subscription type IDs opted in per long form (Marketing Information 7195048, One to One 3199624, EB-5 Onboarding 105452959).
	const SUBSCRIPTIONS = [
		'registration' => [ 7195048, 3199624 ],
		'eb5'          => [ 105452959, 7195048, 3199624 ],
	];

	const MAX_LEN = 200;
	const MAX_CONSENT_LEN = 600;

	/**
	 * Validate and normalise a request body.
	 * @return array{ok:bool, error?:string, code?:string, form?:string, fields?:array, consent_text?:string, utm?:array, hutk?:string, page_uri?:string, page_name?:string}
	 */
	public static function validate( array $body, string $site_host ): array {
		$form = is_string( $body['form'] ?? null ) ? $body['form'] : '';
		if ( ! isset( self::FORMS[ $form ] ) ) {
			return self::fail( 'unknown_form', 'Something went wrong. Please reload the page and try again.' );
		}
		$in  = is_array( $body['fields'] ?? null ) ? $body['fields'] : [];
		$out = [];
		foreach ( self::FIELDS[ $form ] as $name => $required ) {
			$v = $in[ $name ] ?? '';
			$v = is_bool( $v ) ? ( $v ? 'true' : '' ) : trim( (string) ( is_scalar( $v ) ? $v : '' ) );
			if ( $v === '' ) {
				if ( $required ) {
					return self::fail( 'missing_field', 'Please complete all required fields.', $name );
				}
				continue;
			}
			if ( mb_strlen( $v ) > self::MAX_LEN ) {
				return self::fail( 'too_long', 'One of the fields is too long.', $name );
			}
			$out[ $name ] = $v;
		}
		if ( ! filter_var( $out['email'], FILTER_VALIDATE_EMAIL ) ) {
			return self::fail( 'bad_email', 'Please enter a valid email address.', 'email' );
		}
		$out['email'] = strtolower( $out['email'] );
		if ( isset( $out['accredited_investor'] ) ) {
			$key = $out['accredited_investor'];
			if ( $key === 'none' ) {
				return self::fail( 'not_accredited', 'Our offerings are available to accredited investors only.' );
			}
			if ( ! isset( self::ACCREDITATION[ $key ] ) ) {
				return self::fail( 'bad_value', 'Please choose an accreditation option.', 'accredited_investor' );
			}
			$out['accredited_investor'] = self::ACCREDITATION[ $key ];
		}
		if ( isset( $out['preferred_contact_method'] ) && ! in_array( $out['preferred_contact_method'], self::CONTACT_METHODS, true ) ) {
			return self::fail( 'bad_value', 'Please choose a contact method.', 'preferred_contact_method' );
		}
		if ( isset( $out['eb5_amount_acknowledgement'] ) && ! in_array( strtolower( $out['eb5_amount_acknowledgement'] ), [ 'true', '1', 'on', 'yes' ], true ) ) {
			return self::fail( 'missing_field', 'Please confirm the investment amount.', 'eb5_amount_acknowledgement' );
		}
		if ( isset( $out['eb5_amount_acknowledgement'] ) ) {
			$out['eb5_amount_acknowledgement'] = 'true';
		}

		$consent_text = '';
		if ( isset( self::SUBSCRIPTIONS[ $form ] ) ) {
			$c = is_array( $body['consent'] ?? null ) ? $body['consent'] : [];
			$consent_text = trim( (string) ( $c['text'] ?? '' ) );
			if ( empty( $c['agreed'] ) || $consent_text === '' ) {
				return self::fail( 'consent_required', 'Please agree to the consent statement to continue.', 'consent' );
			}
			if ( mb_strlen( $consent_text ) > self::MAX_CONSENT_LEN ) {
				return self::fail( 'too_long', 'Something went wrong. Please reload the page and try again.', 'consent' );
			}
		}

		$utm = [];
		$u   = is_array( $body['utm'] ?? null ) ? $body['utm'] : [];
		foreach ( self::UTM as $k ) {
			$v = trim( (string) ( is_scalar( $u[ $k ] ?? null ) ? $u[ $k ] : '' ) );
			if ( $v !== '' ) {
				$utm[ $k ] = mb_substr( $v, 0, self::MAX_LEN );
			}
		}

		// pageUri must be on this site: HubSpot attributes the request to it (it is how IR tells offerings apart).
		$page_uri = (string) ( $body['pageUri'] ?? '' );
		$host     = parse_url( $page_uri, PHP_URL_HOST );
		$scheme   = parse_url( $page_uri, PHP_URL_SCHEME );
		if ( ! $host || strcasecmp( $host, $site_host ) !== 0 || ! in_array( $scheme, [ 'http', 'https' ], true ) ) {
			return self::fail( 'bad_page', 'Something went wrong. Please reload the page and try again.' );
		}
		$hutk = (string) ( $body['hutk'] ?? '' );

		return [
			'ok'           => true,
			'form'         => $form,
			'fields'       => $out,
			'consent_text' => $consent_text,
			'utm'          => $utm,
			'hutk'         => preg_match( '/^[a-f0-9]{32}$/i', $hutk ) ? $hutk : '',
			'page_uri'     => $page_uri,
			'page_name'    => mb_substr( trim( (string) ( $body['pageName'] ?? '' ) ), 0, self::MAX_LEN ),
		];
	}

	/** Forms API v3 payload for a validated submission. $subscriptions lets the caller drop a rejected type (One to One). */
	public static function payload( array $v, ?array $subscriptions = null ): array {
		$fields = [];
		foreach ( $v['fields'] + $v['utm'] as $name => $value ) {
			$fields[] = [ 'objectTypeId' => '0-1', 'name' => $name, 'value' => $value ];
		}
		$context = [ 'pageUri' => $v['page_uri'], 'pageName' => $v['page_name'] ];
		if ( $v['hutk'] !== '' ) {
			$context['hutk'] = $v['hutk'];
		}
		$p    = [ 'submittedAt' => (string) ( time() * 1000 ), 'fields' => $fields, 'context' => $context ];
		$subs = $subscriptions ?? ( self::SUBSCRIPTIONS[ $v['form'] ] ?? [] );
		if ( isset( self::SUBSCRIPTIONS[ $v['form'] ] ) ) {
			$p['legalConsentOptions'] = [ 'consent' => [
				'consentToProcess' => true,
				'text'             => $v['consent_text'],
				'communications'   => array_map( fn( $id ) => [ 'value' => true, 'subscriptionTypeId' => $id, 'text' => $v['consent_text'] ], array_values( $subs ) ),
			] ];
		}
		return $p;
	}

	public static function endpoint( string $form ): string {
		return 'https://api.hsforms.com/submissions/v3/integration/secure/submit/' . self::PORTAL . '/' . self::FORMS[ $form ];
	}

	/** Plain-language message for a HubSpot Forms API error response body. */
	public static function hubspot_error( int $status, string $body ): string {
		$j = json_decode( $body, true );
		foreach ( (array) ( $j['errors'] ?? [] ) as $e ) {
			$type = $e['errorType'] ?? '';
			if ( $type === 'INVALID_EMAIL' || $type === 'BLOCKED_EMAIL' ) {
				return 'Please enter a valid email address.';
			}
			if ( $type === 'NUMBER_OUT_OF_RANGE' || $type === 'INVALID_NUMBER' ) {
				return 'Please check the phone number.';
			}
			if ( $type === 'REQUIRED_FIELD' ) {
				return 'Please complete all required fields.';
			}
		}
		return $status === 429 ? 'Too many requests. Please try again in a minute.' : 'We could not send your details. Please try again, or contact us directly.';
	}

	/** True when HubSpot rejected the request only because of a subscription type (One to One may be refused through forms). */
	public static function is_subscription_error( string $body ): bool {
		$j = json_decode( $body, true );
		foreach ( (array) ( $j['errors'] ?? [] ) as $e ) {
			if ( stripos( (string) ( $e['message'] ?? '' ), 'subscription' ) !== false ) {
				return true;
			}
		}
		return false;
	}

	private static function fail( string $code, string $message, string $field = '' ): array {
		return [ 'ok' => false, 'code' => $code, 'error' => $message, 'field' => $field ];
	}
}
