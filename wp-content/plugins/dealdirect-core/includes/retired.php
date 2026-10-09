<?php
/**
 * Live URLs the rebuild does not keep (Alex, 2026-10-09). Only applied while nothing else lives at the path.
 * - Retired: the old Bricks login/registration pages, replaced by the Juniper Square investor login ("retire"). They
 *   answer 410 Gone (removed on purpose, so search engines drop them) instead of a plain 404.
 * - Redirected (301): the old Riverside Wharf offering URLs. Riverside Wharf now has three vehicles: Preferred Equity
 *   (same URL), Common Equity QOZ (/offering/riverside-wharf-qoz/, the successor of /offering/riverside-wharf/) and
 *   EB-5, which lives on the EB-5 pages (/eb-5-investments/ and its ES/PT versions keep their URLs).
 */
namespace DealDirect;

const RETIRED_PATHS = [ 'registration-success', 'forgot-password', 'reset-password', 'admin-login' ];
const REDIRECTS     = [
	'offering/riverside-wharf'     => '/offering/riverside-wharf-qoz/',
	'offering/riverside-wharf-eb-5' => '/eb-5-investments/',
];

function request_path( string $uri ): string {
	return trim( (string) parse_url( $uri, PHP_URL_PATH ), '/' );
}

/** Whether a request path ("/forgot-password/", "forgot-password?x=1") is a retired page. */
function is_retired_path( string $uri ): bool {
	return in_array( request_path( $uri ), RETIRED_PATHS, true );
}

/** Where an old URL now lives (site-relative path), or null. */
function redirect_target( string $uri ): ?string {
	return REDIRECTS[ request_path( $uri ) ] ?? null;
}

if ( function_exists( 'add_action' ) ) {
	// Priority 1: before WordPress's own 404 guessing (redirect_canonical) picks a look-alike slug.
	add_action( 'template_redirect', function () {
		if ( ! is_404() ) {
			return;
		}
		$uri = $_SERVER['REQUEST_URI'] ?? '';
		if ( $to = redirect_target( $uri ) ) {
			wp_safe_redirect( home_url( $to ), 301, 'DealDirect' );
			exit;
		}
		if ( is_retired_path( $uri ) ) {
			status_header( 410 );
			nocache_headers();
		}
	}, 1 );
}
