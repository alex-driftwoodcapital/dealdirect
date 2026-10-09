<?php
/**
 * Content model: the `offering` CPT, its fields and the Platform stats options page.
 * Registered in code (not the SCF admin UI) so the model is versioned with the site and identical on staging and live.
 * Fields need Secure Custom Fields (or ACF); Etch reads them as item.acf.* / options.acf.*.
 * Spec: handoff/docs/cpt-schema.md, handoff/docs/platform-stats.md.
 */
namespace DealDirect;

defined( 'ABSPATH' ) || exit;

function register_offering(): void {
	register_post_type( 'offering', [
		'labels'        => [
			'name'          => 'Offerings',
			'singular_name' => 'Offering',
			'add_new_item'  => 'Add offering',
			'edit_item'     => 'Edit offering',
			'all_items'     => 'All offerings',
		],
		'public'        => true,
		'has_archive'   => false,
		'rewrite'       => [ 'slug' => 'offering', 'with_front' => false ], // frozen permalink: /offering/{slug}/
		'show_in_rest'  => true,
		'supports'      => [ 'title', 'editor', 'thumbnail', 'excerpt', 'custom-fields', 'revisions' ],
		'menu_icon'     => 'dashicons-building',
		'menu_position' => 20,
	] );
}
add_action( 'init', __NAMESPACE__ . '\\register_offering' );

// Seeded on activation; editors change values in WP Admin > Platform stats.
function platform_stat_fields(): array {
	return [
		[ 'name' => 'years_experience', 'label' => 'Years of experience', 'type' => 'text', 'instructions' => 'e.g. 30+' ],
		[ 'name' => 'properties', 'label' => 'Properties', 'type' => 'number', 'instructions' => 'Owned / sponsored / operated; credit excluded; dual-brands count as two.' ],
		[ 'name' => 'keys', 'label' => 'Keys', 'type' => 'number', 'instructions' => 'Credit never included. Not displayed on the site today.' ],
		[ 'name' => 'aum', 'label' => 'AUM', 'type' => 'text', 'instructions' => 'e.g. ~$3.5B' ],
		[ 'name' => 'employees', 'label' => 'Employees', 'type' => 'number', 'instructions' => 'Approximate; shown as ±6,000.' ],
		[ 'name' => 'as_of', 'label' => 'As of', 'type' => 'date_picker', 'instructions' => 'Date of the last data update (footnote 2).' ],
	];
}

add_action( 'acf/init', function () {
	if ( function_exists( 'acf_add_options_page' ) ) {
		acf_add_options_page( [
			'page_title' => 'Platform stats',
			'menu_slug'  => 'platform-stats',
			'capability' => 'manage_options',
			'icon_url'   => 'dashicons-chart-bar',
			'position'   => 21,
			'redirect'   => false,
		] );
	}
	if ( ! function_exists( 'acf_add_local_field_group' ) ) {
		return;
	}

	$f = fn( array $a ) => $a + [ 'key' => 'field_dd_' . $a['name'] ];

	acf_add_local_field_group( [
		'key'      => 'group_dd_offering',
		'title'    => 'Offering',
		'location' => [ [ [ 'param' => 'post_type', 'operator' => '==', 'value' => 'offering' ] ] ],
		'position' => 'normal',
		'fields'   => [
			$f( [ 'name' => 'offering_status', 'label' => 'Status', 'type' => 'select', 'required' => 1,
				'choices' => [ 'open' => 'Open', 'coming_soon' => 'Coming soon', 'closed' => 'Closed' ], 'default_value' => 'open',
				'instructions' => 'Open and Coming soon show in Live offerings on Home; Closed shows in Past offerings.' ] ),
			$f( [ 'name' => 'offering_tag', 'label' => 'Tag', 'type' => 'text', 'instructions' => 'e.g. Preferred Equity · Miami, FL' ] ),
			$f( [ 'name' => 'home_order', 'label' => 'Home order', 'type' => 'number', 'default_value' => 10, 'instructions' => 'Ascending.' ] ),
			$f( [ 'name' => 'card_title', 'label' => 'Card title', 'type' => 'text', 'instructions' => 'Optional; falls back to the post title.' ] ),
			$f( [ 'name' => 'card_summary', 'label' => 'Card summary', 'type' => 'textarea', 'rows' => 2, 'maxlength' => 140, 'instructions' => 'Compliance-approved line, 140 characters max.' ] ),
			$f( [ 'name' => 'card_image', 'label' => 'Card image', 'type' => 'image', 'return_format' => 'array', 'instructions' => 'Optional; falls back to the featured image.' ] ),
			$f( [ 'name' => 'card_cta_label', 'label' => 'Card button label', 'type' => 'text', 'default_value' => 'View Offering' ] ),
			$f( [ 'name' => 'card_url', 'label' => 'Card link (no page yet)', 'type' => 'url',
				'instructions' => 'Only for an offering without a page here: its URL redirects (302) to this link. Clear it once the offering has its page.' ] ),
			$f( [ 'name' => 'card_rendering', 'label' => 'Card image is a rendering', 'type' => 'true_false', 'ui' => 1, 'default_value' => 0,
				'instructions' => 'Shows the "Rendering" chip on the Home card.' ] ),
			$f( [ 'name' => 'show_oz_section', 'label' => 'Show OZ incentives section', 'type' => 'true_false', 'ui' => 1, 'default_value' => 0,
				'instructions' => 'Shows #structure and its sub-nav item (QOZ offerings).' ] ),
			$f( [ 'name' => 'offering_layer', 'label' => 'Highlighted cap-stack layer', 'type' => 'text', 'instructions' => 'Label of the layer to highlight in the capital stack.' ] ),
			$f( [ 'name' => 'metrics', 'label' => 'Target metrics', 'type' => 'repeater', 'layout' => 'table', 'button_label' => 'Add metric',
				'sub_fields' => [
					[ 'key' => 'field_dd_metric_value', 'name' => 'value', 'label' => 'Value', 'type' => 'text' ],
					[ 'key' => 'field_dd_metric_qualifier', 'name' => 'qualifier', 'label' => 'Qualifier', 'type' => 'text', 'instructions' => 'e.g. Target*' ],
					[ 'key' => 'field_dd_metric_label', 'name' => 'label', 'label' => 'Label', 'type' => 'text' ],
					[ 'key' => 'field_dd_metric_footnote', 'name' => 'footnote', 'label' => 'Footnote', 'type' => 'text' ],
				] ] ),
			$f( [ 'name' => 'brochure', 'label' => 'Brochure', 'type' => 'file', 'return_format' => 'array', 'mime_types' => 'pdf' ] ),
		],
	] );

	acf_add_local_field_group( [
		'key'      => 'group_dd_platform_stats',
		'title'    => 'Platform stats',
		'location' => [ [ [ 'param' => 'options_page', 'operator' => '==', 'value' => 'platform-stats' ] ] ],
		'fields'   => array_map( fn( $a ) => $f( $a + ( $a['type'] === 'date_picker' ? [ 'display_format' => 'F j, Y', 'return_format' => 'F j, Y' ] : [] ) ), platform_stat_fields() ),
	] );
} );

/** Seed Platform stats from data/platform-stats.json (copied from the design system's dwstats.js). Only fills empty fields. */
function seed_platform_stats(): array {
	if ( ! function_exists( 'update_field' ) ) {
		return [ 'skipped' => 'Secure Custom Fields is not active' ];
	}
	$data = json_decode( (string) file_get_contents( __DIR__ . '/../data/platform-stats.json' ), true );
	$done = [];
	foreach ( platform_stat_fields() as $field ) {
		$name = $field['name'];
		if ( isset( $data[ $name ] ) && ( get_field( $name, 'option' ) === null || get_field( $name, 'option' ) === '' || get_field( $name, 'option' ) === false ) ) {
			update_field( 'field_dd_' . $name, $data[ $name ], 'option' );
			$done[] = $name;
		}
	}
	return [ 'seeded' => $done ];
}
