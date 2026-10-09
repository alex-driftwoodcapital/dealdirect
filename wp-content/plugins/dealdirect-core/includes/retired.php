<?php
/**
 * Live URLs retired by the rebuild (Alex, 2026-10-09: "retire"): the old Bricks login/registration pages, replaced by
 * the Juniper Square investor login. They answer 410 Gone (removed on purpose, so search engines drop them) instead of
 * a plain 404. Not redirects. Only applies while nothing else lives at the path.
 */
namespace DealDirect;

const RETIRED_PATHS = [ 'registration-success', 'forgot-password', 'reset-password', 'admin-login' ];

/** Whether a request path ("/forgot-password/", "forgot-password?x=1") is a retired page. */
function is_retired_path( string $path ): bool {
	$path = trim( (string) parse_url( $path, PHP_URL_PATH ), '/' );
	return in_array( $path, RETIRED_PATHS, true );
}

if ( function_exists( 'add_action' ) ) {
	add_action( 'template_redirect', function () {
		if ( is_404() && is_retired_path( $_SERVER['REQUEST_URI'] ?? '' ) ) {
			status_header( 410 );
			nocache_headers();
		}
	} );
}
