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
// Writing the option does not rebuild ACSS's stylesheets (its dashboard Save does). dd_acss_css_for remembers which
// settings the stylesheets were last regenerated from, so a run with no setting changes still catches stale CSS.
$want  = md5( serialize( array_merge( $cur, $new ) ) );
$stale = get_option( 'dd_acss_css_for' ) !== $want;
WP_CLI::log( 'stylesheets: ' . ( $stale ? ( $mode === 'write' ? 'regenerating' : 'would regenerate (not built from these settings)' ) : 'built from these settings' ) );
if ( $mode !== 'write' ) {
	// The write run regenerates through ACSS's own WP-CLI command: fail the dry run (the PR check) if it is missing.
	if ( $stale || $changes ) {
		$h = WP_CLI::runcommand( 'help acss css', [ 'return' => 'all', 'exit_error' => false, 'launch' => true ] );
		if ( $h->return_code !== 0 || ! str_contains( $h->stdout, 'regenerate' ) ) { WP_CLI::error( 'wp acss css regenerate is not available on this ACSS build' ); }
		WP_CLI::log( 'wp acss css regenerate: available' );
	}
	WP_CLI::success( 'dry run, nothing written' );
	return;
}
if ( $changes ) { update_option( $opt, array_merge( $cur, $new ) ); }
if ( $stale || $changes ) {
	$r = WP_CLI::runcommand( 'acss css regenerate', [ 'return' => 'all', 'exit_error' => false, 'launch' => true ] );
	WP_CLI::log( trim( $r->stdout . "\n" . $r->stderr ) );
	if ( $r->return_code !== 0 ) { WP_CLI::error( 'wp acss css regenerate failed (exit ' . $r->return_code . ')' ); }
	update_option( 'dd_acss_css_for', $want, false );
}
WP_CLI::success( $changes ? 'settings saved, stylesheets regenerated' : ( $stale ? 'stylesheets regenerated' : 'nothing to do' ) );
