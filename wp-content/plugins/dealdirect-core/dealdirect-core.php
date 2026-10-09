<?php
/**
 * Plugin Name: DealDirect Core
 * Description: Content model (offering CPT, fields, Platform stats) and the HubSpot form proxy for driftwooddealdirect.com.
 * Version: 0.1.0
 * Requires PHP: 8.1
 * Requires Plugins: secure-custom-fields
 * Author: Driftwood Capital
 */

defined( 'ABSPATH' ) || exit;

require_once __DIR__ . '/includes/class-submission.php';
require_once __DIR__ . '/includes/content-model.php';
require_once __DIR__ . '/includes/rest.php';
require_once __DIR__ . '/includes/i18n.php';

// Register the CPT before flushing so /offering/{slug}/ resolves right after activation.
register_activation_hook( __FILE__, function () {
	\DealDirect\register_offering();
	flush_rewrite_rules();
} );

if ( defined( 'WP_CLI' ) && WP_CLI ) {
	/** wp dealdirect seed-stats : fill empty Platform stats fields from data/platform-stats.json */
	WP_CLI::add_command( 'dealdirect seed-stats', function () {
		WP_CLI::log( wp_json_encode( \DealDirect\seed_platform_stats() ) );
	} );
}

register_deactivation_hook( __FILE__, 'flush_rewrite_rules' );
