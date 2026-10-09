<?php
// Host-side helper for ops/cleanup/retire.sh. Run: wp eval-file retire.php <json-file> <dry|write>
// $in: {posts: [[post_type, slug], ...], ours: [template slugs this repo deploys]}. Trashes each listed post unless
// this repo wrote it (_dd_deployed_sha) or a live post still references it ("ref":<id> in its content). References
// from the other listed posts and from templates this repo deploys don't count (the same deploy replaces those).
[ $file, $mode ] = [ $args[0] ?? '', $args[1] ?? 'dry' ];
$in    = json_decode( (string) file_get_contents( $file ), true );
$write = $mode === 'write';
$ours  = (array) ( $in['ours'] ?? [] );
$listed = fn( $type, $slug ) => in_array( [ $type, $slug ], $in['posts'], true );
global $wpdb;
foreach ( $in['posts'] as [ $type, $slug ] ) {
	$q = [ 'post_type' => $type, 'name' => $slug, 'post_status' => [ 'publish', 'draft', 'private' ], 'numberposts' => 5 ];
	if ( $type === 'wp_template' ) { $q['tax_query'] = [ [ 'taxonomy' => 'wp_theme', 'field' => 'name', 'terms' => get_stylesheet() ] ]; }
	$found = get_posts( $q );
	if ( ! $found ) { printf( "  %-12s %-20s gone\n", $type, $slug ); continue; }
	foreach ( $found as $p ) {
		if ( get_post_meta( $p->ID, '_dd_deployed_sha', true ) ) { printf( "  %-12s %-20s #%d kept (deployed by this repo)\n", $type, $slug, $p->ID ); continue; }
		$users = $wpdb->get_results( $wpdb->prepare(
			"SELECT ID, post_type, post_name, post_content FROM {$wpdb->posts} WHERE post_status IN ('publish','draft','private','future') AND ID <> %d AND post_content LIKE %s",
			$p->ID, '%' . $wpdb->esc_like( '"ref":' . $p->ID ) . '%' ) );
		$users = array_filter( $users, fn( $u ) => preg_match( '/"ref":' . $p->ID . '(?!\d)/', $u->post_content )
			&& ! $listed( $u->post_type, $u->post_name ) && ! ( $u->post_type === 'wp_template' && in_array( $u->post_name, $ours, true ) ) );
		if ( $users ) {
			printf( "  %-12s %-20s #%d kept: used by %s\n", $type, $slug, $p->ID, implode( ', ', array_map( fn( $u ) => "{$u->post_type} #{$u->ID} {$u->post_name}", $users ) ) );
			continue;
		}
		if ( $write && ! wp_trash_post( $p->ID ) ) { WP_CLI::error( "could not trash #{$p->ID}" ); }
		printf( "  %-12s %-20s #%d %s\n", $type, $slug, $p->ID, $write ? 'trashed' : 'would trash' );
	}
}
