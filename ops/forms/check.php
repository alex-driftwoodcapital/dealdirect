<?php
// ROLE-TEMPLATE
// Read-only HubSpot check, run on STAGING by ops/forms/check.sh (wp eval-file): is the token there, and can it read each
// form the site submits to (Forms API GET) and search contacts (the offering-request step)? Never submits anything and
// never prints the token.
use DealDirect\Submission;

if ( ! class_exists( Submission::class ) ) {
	echo "dealdirect-core not active\n";
	return;
}
if ( ! defined( 'DD_HUBSPOT_TOKEN' ) || ! DD_HUBSPOT_TOKEN ) {
	echo "DD_HUBSPOT_TOKEN: NOT set (every submission answers 503)\n";
	return;
}
echo 'DD_HUBSPOT_TOKEN: set (' . strlen( DD_HUBSPOT_TOKEN ) . " chars, starts with \"" . substr( DD_HUBSPOT_TOKEN, 0, 4 ) . "\")\n";
$h = [ 'Authorization' => 'Bearer ' . DD_HUBSPOT_TOKEN ];
foreach ( Submission::FORMS as $form => $guid ) {
	$r = wp_remote_get( "https://api.hubapi.com/marketing/v3/forms/$guid", [ 'timeout' => 15, 'headers' => $h ] );
	if ( is_wp_error( $r ) ) {
		echo "form $form ($guid): transport error: " . $r->get_error_message() . "\n";
		continue;
	}
	$code = wp_remote_retrieve_response_code( $r );
	$j    = json_decode( wp_remote_retrieve_body( $r ), true ) ?: [];
	$name = $j['name'] ?? '';
	$names = [];
	foreach ( $j['fieldGroups'] ?? [] as $g ) {
		foreach ( $g['fields'] ?? [] as $f ) {
			$names[] = ( $f['name'] ?? '?' ) . ( ! empty( $f['required'] ) ? '*' : '' );
		}
	}
	$sent = array_keys( Submission::FIELDS[ $form ] );
	$missing_on_form = array_values( array_diff( $sent, array_map( fn( $n ) => rtrim( $n, '*' ), $names ) ) );
	$required_not_sent = array_values( array_filter( $names, fn( $n ) => str_ends_with( $n, '*' ) && ! in_array( rtrim( $n, '*' ), $sent, true ) ) );
	echo "form $form ($guid): HTTP $code" . ( $name ? " \"$name\"" : '' ) . ( isset( $j['archived'] ) ? ' archived=' . var_export( $j['archived'], true ) : '' )
		. ( $code !== 200 ? ' ' . substr( (string) ( $j['message'] ?? wp_remote_retrieve_body( $r ) ), 0, 200 ) : '' ) . "\n";
	if ( $code === 200 ) {
		echo '  fields on the form: ' . implode( ', ', $names ) . "\n";
		echo '  sent by the site but not on the form: ' . ( $missing_on_form ? implode( ', ', $missing_on_form ) : 'none' ) . "\n";
		echo '  required on the form but not sent: ' . ( $required_not_sent ? implode( ', ', $required_not_sent ) : 'none' ) . "\n";
	}
}
$r = wp_remote_post( 'https://api.hubapi.com/crm/v3/objects/contacts/search', [
	'timeout' => 15,
	'headers' => $h + [ 'Content-Type' => 'application/json' ],
	'body'    => wp_json_encode( [ 'filterGroups' => [ [ 'filters' => [ [ 'propertyName' => 'email', 'operator' => 'EQ', 'value' => 'nobody@example.invalid' ] ] ] ], 'limit' => 1 ] ),
] );
echo 'contact search (offering-request step): ' . ( is_wp_error( $r ) ? 'transport error: ' . $r->get_error_message() : 'HTTP ' . wp_remote_retrieve_response_code( $r )
	. ( wp_remote_retrieve_response_code( $r ) !== 200 ? ' ' . substr( wp_remote_retrieve_body( $r ), 0, 200 ) : '' ) ) . "\n";
