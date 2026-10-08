<?php
/**
 * REST proxy to HubSpot: GET /dealdirect/v1/token, POST /dealdirect/v1/submit.
 * The private app token lives in wp-config.php as DD_HUBSPOT_TOKEN and never reaches the browser.
 */
namespace DealDirect;

defined( 'ABSPATH' ) || exit;

const NONCE_ACTION   = 'dd_submit';
const LEAD_COOKIE    = 'dd_lead';
const ONE_TO_ONE     = 3199624;
const RATE_IP_MAX    = 8;   // submissions per IP per window
const RATE_EMAIL_MAX = 4;   // submissions per email per window
const RATE_WINDOW    = 600; // seconds

add_action( 'rest_api_init', function () {
	// Pages are cached by Breeze/Varnish, so a nonce printed into the page goes stale: the form fetches one at submit time.
	register_rest_route( 'dealdirect/v1', '/token', [
		'methods'             => 'GET',
		'permission_callback' => '__return_true',
		'callback'            => function () {
			$r = new \WP_REST_Response( [ 'nonce' => wp_create_nonce( NONCE_ACTION ) ] );
			$r->header( 'Cache-Control', 'no-store, max-age=0' );
			return $r;
		},
	] );
	register_rest_route( 'dealdirect/v1', '/submit', [
		'methods'             => 'POST',
		'permission_callback' => '__return_true',
		'callback'            => __NAMESPACE__ . '\\handle_submit',
	] );
} );

function respond( array $data, int $status = 200 ): \WP_REST_Response {
	$r = new \WP_REST_Response( $data, $status );
	$r->header( 'Cache-Control', 'no-store, max-age=0' );
	return $r;
}

function handle_submit( \WP_REST_Request $req ): \WP_REST_Response {
	if ( ! wp_verify_nonce( (string) $req->get_header( 'x_dd_nonce' ), NONCE_ACTION ) ) {
		return respond( [ 'status' => 'error', 'message' => 'Your session expired. Please try again.' ], 403 );
	}
	$body = $req->get_json_params();
	if ( ! is_array( $body ) ) {
		return respond( [ 'status' => 'error', 'message' => 'Something went wrong. Please reload the page and try again.' ], 400 );
	}
	// Honeypot: a hidden "website" input that people never fill.
	if ( ! empty( $body['website'] ) ) {
		return respond( [ 'status' => 'sent' ] );
	}
	$v = Submission::validate( $body, (string) wp_parse_url( home_url(), PHP_URL_HOST ) );
	if ( ! $v['ok'] ) {
		$status = $v['code'] === 'not_accredited' ? 422 : 400;
		return respond( [ 'status' => $v['code'] === 'not_accredited' ? 'not_accredited' : 'error', 'message' => $v['error'], 'field' => $v['field'] ], $status );
	}
	if ( ! rate_ok( 'ip_' . client_ip(), RATE_IP_MAX ) || ! rate_ok( 'em_' . $v['fields']['email'], RATE_EMAIL_MAX ) ) {
		return respond( [ 'status' => 'error', 'message' => 'Too many requests. Please try again in a few minutes.' ], 429 );
	}
	if ( ! defined( 'DD_HUBSPOT_TOKEN' ) || ! DD_HUBSPOT_TOKEN ) {
		error_log( 'dealdirect: DD_HUBSPOT_TOKEN is not defined' );
		return respond( [ 'status' => 'error', 'message' => 'We could not send your details. Please try again later.' ], 503 );
	}

	if ( $v['form'] === 'offering-request' ) {
		$known = contact_exists( $v['fields']['email'] );
		if ( $known === null ) {
			return respond( [ 'status' => 'error', 'message' => 'We could not send your details. Please try again later.' ], 502 );
		}
		if ( ! $known ) {
			return respond( [ 'status' => 'needs_registration', 'email' => $v['fields']['email'] ] );
		}
	}

	$res = post_hubspot( $v['form'], Submission::payload( $v ) );
	// One to One is a HubSpot internal type and may be refused through forms; nothing is lost without it.
	if ( $res['status'] === 400 && Submission::is_subscription_error( $res['body'] ) ) {
		$subs = array_values( array_diff( Submission::SUBSCRIPTIONS[ $v['form'] ] ?? [], [ ONE_TO_ONE ] ) );
		$res  = post_hubspot( $v['form'], Submission::payload( $v, $subs ) );
	}
	if ( $res['status'] < 200 || $res['status'] >= 300 ) {
		error_log( sprintf( 'dealdirect: HubSpot %s returned %d', $v['form'], $res['status'] ) );
		return respond( [ 'status' => 'error', 'message' => Submission::hubspot_error( $res['status'], $res['body'] ) ], 502 );
	}
	if ( $v['form'] !== 'offering-request' ) {
		set_lead_cookie( $v['fields']['email'] );
	}
	return respond( [ 'status' => 'sent' ] );
}

/** @return array{status:int, body:string} status 0 on transport error */
function post_hubspot( string $form, array $payload ): array {
	$r = wp_remote_post( Submission::endpoint( $form ), [
		'timeout' => 15,
		'headers' => [ 'Authorization' => 'Bearer ' . DD_HUBSPOT_TOKEN, 'Content-Type' => 'application/json' ],
		'body'    => wp_json_encode( $payload ),
	] );
	if ( is_wp_error( $r ) ) {
		error_log( 'dealdirect: HubSpot transport error: ' . $r->get_error_message() );
		return [ 'status' => 0, 'body' => '' ];
	}
	return [ 'status' => (int) wp_remote_retrieve_response_code( $r ), 'body' => (string) wp_remote_retrieve_body( $r ) ];
}

/** true / false, or null when HubSpot could not be asked. */
function contact_exists( string $email ): ?bool {
	$r = wp_remote_post( 'https://api.hubapi.com/crm/v3/objects/contacts/search', [
		'timeout' => 15,
		'headers' => [ 'Authorization' => 'Bearer ' . DD_HUBSPOT_TOKEN, 'Content-Type' => 'application/json' ],
		'body'    => wp_json_encode( [
			'filterGroups' => [ [ 'filters' => [ [ 'propertyName' => 'email', 'operator' => 'EQ', 'value' => $email ] ] ] ],
			'properties'   => [ 'email' ],
			'limit'        => 1,
		] ),
	] );
	if ( is_wp_error( $r ) || (int) wp_remote_retrieve_response_code( $r ) !== 200 ) {
		error_log( 'dealdirect: contact search failed' );
		return null;
	}
	$j = json_decode( (string) wp_remote_retrieve_body( $r ), true );
	return ( (int) ( $j['total'] ?? 0 ) ) > 0;
}

/** Marks a returning visitor. Holds a keyed hash, never form answers. Readable by JS to pick the dialog. */
function set_lead_cookie( string $email ): void {
	$value = substr( hash_hmac( 'sha256', $email, wp_salt( 'auth' ) ), 0, 32 );
	setcookie( LEAD_COOKIE, $value, [
		'expires'  => time() + YEAR_IN_SECONDS,
		'path'     => '/',
		'secure'   => is_ssl(),
		'httponly' => false,
		'samesite' => 'Lax',
	] );
}

function client_ip(): string {
	// Cloudways sits behind its own proxy/Varnish; REMOTE_ADDR is the visitor unless Cloudflare is added later.
	$ip = $_SERVER['HTTP_CF_CONNECTING_IP'] ?? $_SERVER['REMOTE_ADDR'] ?? '';
	return filter_var( $ip, FILTER_VALIDATE_IP ) ? $ip : 'unknown';
}

function rate_ok( string $key, int $max ): bool {
	$k = 'dd_rl_' . md5( $key );
	$n = (int) get_transient( $k );
	if ( $n >= $max ) {
		return false;
	}
	set_transient( $k, $n + 1, RATE_WINDOW );
	return true;
}
