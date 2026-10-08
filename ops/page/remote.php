<?php
// Host-side helper for ops/page/deploy.py. Run: wp eval-file remote.php <action> <json-file> <dry|write>
// Never touches anything but the named media, etch_styles records and page meta. Prints one JSON object.
[ $action, $file, $mode ] = [ $args[0] ?? '', $args[1] ?? '', $args[2] ?? 'dry' ];
$in    = $file ? json_decode( (string) file_get_contents( $file ), true ) : [];
$write = $mode === 'write';
$out   = [];

if ( $action === 'media' ) {
	// $in: {slug: source}. source = host path of an uploaded local file, or a URL (the host downloads it).
	require_once ABSPATH . 'wp-admin/includes/file.php';
	require_once ABSPATH . 'wp-admin/includes/media.php';
	require_once ABSPATH . 'wp-admin/includes/image.php';
	global $wpdb;
	foreach ( $in as $slug => $src ) {
		$name = basename( parse_url( $src, PHP_URL_PATH ) );
		// Same filename already in the library (a previous run): reuse it, never re-upload.
		$id = (int) $wpdb->get_var( $wpdb->prepare(
			"SELECT post_id FROM {$wpdb->postmeta} WHERE meta_key = '_wp_attached_file' AND (meta_value = %s OR meta_value LIKE %s) ORDER BY post_id LIMIT 1",
			$name, '%/' . $wpdb->esc_like( $name ) ) );
		if ( $id ) { $out[ $slug ] = [ 'id' => $id, 'status' => 'exists' ]; continue; }
		if ( ! $write ) { $out[ $slug ] = [ 'id' => null, 'status' => 'would import ' . $name ]; continue; }
		$tmp = preg_match( '#^https?://#', $src ) ? download_url( $src, 60 ) : $src;
		if ( is_wp_error( $tmp ) ) { $out[ $slug ] = [ 'id' => null, 'status' => 'ERROR ' . $tmp->get_error_message() ]; continue; }
		$id = media_handle_sideload( [ 'name' => $name, 'tmp_name' => $tmp ], 0 );
		$out[ $slug ] = is_wp_error( $id ) ? [ 'id' => null, 'status' => 'ERROR ' . $id->get_error_message() ] : [ 'id' => $id, 'status' => 'imported' ];
	}
} elseif ( $action === 'styles' ) {
	// $in: {id: record}. Upsert by selector: an existing record keeps its id and gets our css; a new one gets our id.
	$styles = get_option( 'etch_styles', [] );
	$styles = is_array( $styles ) ? $styles : [];
	$by_sel = [];
	foreach ( $styles as $sid => $rec ) { $by_sel[ $rec['selector'] ?? '' ] = $sid; }
	$changed = 0;
	foreach ( $in as $id => $rec ) {
		$sel = $rec['selector'];
		if ( isset( $by_sel[ $sel ] ) ) {
			$sid = $by_sel[ $sel ];
			if ( ! empty( $styles[ $sid ]['readonly'] ) ) { $out[ $sel ] = [ 'id' => $sid, 'status' => 'readonly, kept' ]; continue; }
			$same = (string) ( $styles[ $sid ]['css'] ?? '' ) === (string) $rec['css'];
			$out[ $sel ] = [ 'id' => $sid, 'status' => $same ? 'same' : 'update css' ];
			if ( ! $same ) { $styles[ $sid ]['css'] = $rec['css']; $changed++; }
		} else {
			if ( isset( $styles[ $id ] ) ) { WP_CLI::error( "id $id is taken by {$styles[$id]['selector']}" ); }
			$styles[ $id ] = $rec;
			$out[ $sel ] = [ 'id' => $id, 'status' => 'add' ];
			$changed++;
		}
	}
	if ( $write && $changed ) { update_option( 'etch_styles', $styles ); }
	$out = [ 'records' => $out, 'changed' => $changed, 'written' => $write && $changed > 0 ];
} elseif ( $action === 'page' ) {
	// $in: {slug, post_type}. The post with that slug (any status; for wp_template only the active theme's), and the
	// sha we recorded at our last deploy. explicit statuses: 'any' skips drafts when WP-CLI runs logged out.
	$type = $in['post_type'] ?? 'page';
	$q    = [ 'post_type' => $type, 'name' => $in['slug'], 'post_status' => [ 'draft', 'pending', 'private', 'future', 'publish' ], 'numberposts' => 1, 'orderby' => 'ID', 'order' => 'ASC' ];
	if ( $type === 'wp_template' ) { $q['tax_query'] = [ [ 'taxonomy' => 'wp_theme', 'field' => 'name', 'terms' => get_stylesheet() ] ]; }
	$p = get_posts( $q );
	$out = $p ? [ 'id' => $p[0]->ID, 'status' => $p[0]->post_status, 'deployed_sha' => (string) get_post_meta( $p[0]->ID, '_dd_deployed_sha', true ) ] : [ 'id' => null ];
} elseif ( $action === 'create' ) {
	// $in: {post_type, slug, title}. Empty published wp_block / wp_template (with the active theme term) that the
	// normal update path (edit-run.sh) then fills. Pages are created by edit-run.sh --new instead.
	if ( ! in_array( $in['post_type'], [ 'wp_block', 'wp_template' ], true ) ) { WP_CLI::error( 'create: wp_block or wp_template only' ); }
	if ( ! $write ) { $out = [ 'id' => null ]; } else {
		$id = wp_insert_post( [ 'post_type' => $in['post_type'], 'post_name' => $in['slug'], 'post_title' => $in['title'], 'post_status' => 'publish', 'post_content' => '' ], true );
		if ( is_wp_error( $id ) ) { WP_CLI::error( $id->get_error_message() ); }
		if ( $in['post_type'] === 'wp_template' ) { wp_set_object_terms( $id, get_stylesheet(), 'wp_theme' ); }
		$out = [ 'id' => $id ];
	}
} elseif ( $action === 'refs' ) {
	// $in: {slugs: [...]}. Component (wp_block) ids by slug, for {{ref:<slug>}} placeholders.
	foreach ( $in['slugs'] as $slug ) {
		$p = get_posts( [ 'post_type' => 'wp_block', 'name' => $slug, 'post_status' => [ 'publish', 'draft', 'private' ], 'numberposts' => 1, 'orderby' => 'ID', 'order' => 'ASC' ] );
		$out[ $slug ] = $p ? $p[0]->ID : null;
	}
} elseif ( $action === 'inventory' ) {
	// Read-only: what templates, template parts and components exist now (printed in dry runs).
	foreach ( get_posts( [ 'post_type' => [ 'wp_template', 'wp_template_part', 'wp_block' ], 'post_status' => 'any', 'numberposts' => 200 ] ) as $p ) {
		$theme = wp_get_object_terms( $p->ID, 'wp_theme', [ 'fields' => 'names' ] );
		$out[] = sprintf( '%s #%d %s (%s)%s', $p->post_type, $p->ID, $p->post_name, $p->post_status, $theme && ! is_wp_error( $theme ) ? ' theme=' . implode( ',', $theme ) : '' );
	}
	// Etch Asset Manager storage is undocumented: report what could hold collections (attachment taxonomies and
	// their terms, Etch options/post types whose names mention assets or collections) so it can be read, not guessed.
	$tax = [];
	foreach ( get_object_taxonomies( 'attachment', 'objects' ) as $t ) {
		$terms = get_terms( [ 'taxonomy' => $t->name, 'hide_empty' => false, 'number' => 50 ] );
		$tax[ $t->name ] = is_wp_error( $terms ) ? [] : array_map( fn( $x ) => $x->name . ( $x->parent ? ' (child of #' . $x->parent . ')' : '' ) . ' [' . $x->count . ']', $terms );
	}
	global $wpdb;
	$opts  = $wpdb->get_col( "SELECT option_name FROM {$wpdb->options} WHERE option_name LIKE '%etch%' AND (option_name LIKE '%asset%' OR option_name LIKE '%collection%' OR option_name LIKE '%media%')" );
	$types = array_values( array_filter( get_post_types(), fn( $n ) => preg_match( '/etch|asset|collection/i', $n ) ) );
	$meta  = $wpdb->get_col( "SELECT DISTINCT meta_key FROM {$wpdb->postmeta} WHERE meta_key LIKE '%etch%' AND (meta_key LIKE '%asset%' OR meta_key LIKE '%collection%') LIMIT 20" );
	$out = [ 'active_theme' => get_stylesheet(), 'posts' => $out, 'asset_storage' => [ 'attachment_taxonomies' => $tax, 'options' => $opts, 'post_types' => $types, 'attachment_meta' => $meta ] ];
} elseif ( $action === 'status' ) {
	// $in: {id, status}. Staging pages are published on Alex's word (2026-10-08); live is never written from here.
	$cur = get_post_status( (int) $in['id'] );
	if ( $write && $cur !== $in['status'] ) { wp_update_post( [ 'ID' => (int) $in['id'], 'post_status' => $in['status'] ] ); }
	$out = [ 'from' => $cur, 'to' => $in['status'], 'changed' => $write && $cur !== $in['status'] ];
} elseif ( $action === 'mark' ) {
	// $in: {id, sha}. Record what we wrote, so the next deploy can tell a builder save from our own content.
	if ( $write ) { update_post_meta( (int) $in['id'], '_dd_deployed_sha', $in['sha'] ); }
	$out = [ 'marked' => $write ];
} else {
	WP_CLI::error( "unknown action $action" );
}
echo wp_json_encode( $out, JSON_UNESCAPED_SLASHES ) . "\n";
