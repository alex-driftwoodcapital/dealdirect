<?php
// Run on the host via `wp eval-file apply.php <settings.json> <dry|write>`. Finds the ACSS settings option (the array
// option holding "color-primary"), prints what would change, and with "write" merges the input keys and saves.
[ $json, $mode ] = [ $args[0] ?? '', $args[1] ?? 'dry' ];
$new = json_decode( (string) file_get_contents( $json ), true );
if ( ! is_array( $new ) ) { WP_CLI::error( "cannot read $json" ); }
global $wpdb;
$names = $wpdb->get_col( "SELECT option_name FROM {$wpdb->options} WHERE option_name LIKE '%automatic%css%' OR option_name LIKE '%acss%'" );
$opt = null;
foreach ( $names as $n ) { $v = get_option( $n ); if ( is_array( $v ) && array_key_exists( 'color-primary', $v ) ) { $opt = $n; break; } }
if ( ! $opt ) { WP_CLI::error( 'ACSS settings option not found (looked at: ' . implode( ', ', $names ) . ')' ); }
$cur = get_option( $opt );
$changes = [];
foreach ( $new as $k => $v ) {
	if ( ! array_key_exists( $k, $cur ) ) { WP_CLI::warning( "unknown key on this ACSS build, skipped: $k" ); unset( $new[ $k ] ); continue; }
	if ( (string) $cur[ $k ] !== (string) $v ) { $changes[] = sprintf( '%-34s %s -> %s', $k, json_encode( $cur[ $k ] ), json_encode( $v ) ); }
}
WP_CLI::log( "option: $opt (" . count( $cur ) . ' keys); changes: ' . count( $changes ) );
foreach ( $changes as $c ) { WP_CLI::log( '  ' . $c ); }
if ( $mode !== 'write' ) { WP_CLI::success( 'dry run, nothing written' ); return; }
update_option( $opt, array_merge( $cur, $new ) );
WP_CLI::success( 'settings saved; ACSS must now regenerate its stylesheet' );
