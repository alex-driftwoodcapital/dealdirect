<?php
// Host-side helper for ops/page/deploy.py. Run: wp eval-file remote.php <action> <json-file> <dry|write>
// Never touches anything but the named media, etch_styles records and page meta. Prints one JSON object.
[ $action, $file, $mode ] = [ $args[0] ?? '', $args[1] ?? '', $args[2] ?? 'dry' ];
$in    = $file ? json_decode( (string) file_get_contents( $file ), true ) : [];
$write = $mode === 'write';
$out   = [];

if ( $action === 'media' ) {
	// $in: {slug: {src, collection}}. src = host path of an uploaded local file, or a URL (the host downloads it).
	// Every image goes into its Etch Asset Manager collection: taxonomy etch_collection on attachments (read from
	// staging 2026-10-08); a missing collection is created; existing collections on the image are kept.
	require_once ABSPATH . 'wp-admin/includes/file.php';
	require_once ABSPATH . 'wp-admin/includes/media.php';
	require_once ABSPATH . 'wp-admin/includes/image.php';
	global $wpdb;
	$tax = 'etch_collection';
	if ( ! taxonomy_exists( $tax ) ) { WP_CLI::error( "taxonomy $tax not registered: is Etch active?" ); }
	foreach ( $in as $slug => $m ) {
		[ $src, $coll ] = [ $m['src'], $m['collection'] ];
		$name = $m['name'] ?? basename( parse_url( $src, PHP_URL_PATH ) );  // name: for sources whose URL has no filename
		// Same filename already in the library (a previous run): reuse it, never re-upload.
		$id = (int) $wpdb->get_var( $wpdb->prepare(
			"SELECT post_id FROM {$wpdb->postmeta} WHERE meta_key = '_wp_attached_file' AND (meta_value = %s OR meta_value LIKE %s) ORDER BY post_id LIMIT 1",
			$name, '%/' . $wpdb->esc_like( $name ) ) );
		$status = $id ? 'exists' : 'imported';
		if ( ! $id ) {
			if ( ! $write ) { $out[ $slug ] = [ 'id' => null, 'status' => 'would import ' . $name, 'collection' => "would add to $coll" ]; continue; }
			$tmp = preg_match( '#^https?://#', $src ) ? download_url( $src, 60 ) : $src;
			if ( is_wp_error( $tmp ) ) { $out[ $slug ] = [ 'id' => null, 'status' => 'ERROR ' . $tmp->get_error_message() ]; continue; }
			$id = media_handle_sideload( [ 'name' => $name, 'tmp_name' => $tmp ], 0 );
			if ( is_wp_error( $id ) ) { $out[ $slug ] = [ 'id' => null, 'status' => 'ERROR ' . $id->get_error_message() ]; continue; }
		}
		$has = has_term( $coll, $tax, $id );
		if ( ! $has && $write ) {
			if ( ! term_exists( $coll, $tax ) ) {
				$t = wp_insert_term( $coll, $tax );
				if ( is_wp_error( $t ) ) { $out[ $slug ] = [ 'id' => $id, 'status' => 'ERROR collection ' . $t->get_error_message() ]; continue; }
			}
			wp_set_object_terms( $id, $coll, $tax, true );
		}
		$out[ $slug ] = [ 'id' => $id, 'url' => wp_get_attachment_url( $id ), 'status' => $status, 'collection' => $has ? "in $coll" : ( $write ? "added to $coll" : "would add to $coll" ) ];
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
	// $in: {post_type, slug, title}. Empty wp_block / wp_template (published, with the active theme term) or offering
	// (draft until the status step) that the normal update path (edit-run.sh) then fills. Pages: edit-run.sh --new.
	if ( ! in_array( $in['post_type'], [ 'wp_block', 'wp_template', 'offering' ], true ) ) { WP_CLI::error( 'create: wp_block, wp_template or offering only' ); }
	if ( ! $write ) { $out = [ 'id' => null ]; } else {
		$status = $in['post_type'] === 'offering' ? 'draft' : 'publish';
		$id = wp_insert_post( [ 'post_type' => $in['post_type'], 'post_name' => $in['slug'], 'post_title' => $in['title'], 'post_status' => $status, 'post_content' => '' ], true );
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
	// Etch's Asset Manager compressor (presets since 1.6.2) is undocumented: is it a server endpoint a deploy can call, or
	// browser-only? Report its REST routes, preset options, the Etch files that mention compression, and what the
	// server's image editor can encode, so imports can go through it instead of a hand-rolled conversion.
	$routes = array_values( array_filter( array_keys( rest_get_server()->get_routes() ), fn( $r ) => preg_match( '#^/etch#i', $r ) && preg_match( '/asset|compress|preset|media|image|upload/i', $r ) ) );
	$popts  = $wpdb->get_col( "SELECT option_name FROM {$wpdb->options} WHERE option_name LIKE '%etch%' AND (option_name LIKE '%preset%' OR option_name LIKE '%compress%' OR option_name LIKE '%optimi%')" );
	$files  = [];
	$dir    = WP_PLUGIN_DIR . '/etch';
	if ( is_dir( $dir ) ) {
		foreach ( new RecursiveIteratorIterator( new RecursiveDirectoryIterator( $dir, FilesystemIterator::SKIP_DOTS ) ) as $f ) {
			if ( count( $files ) >= 25 || ! preg_match( '/\.(php|js)$/', $f->getFilename() ) || $f->getSize() > 8000000 || str_contains( $f->getPathname(), '/vendor/' ) ) { continue; }
			if ( stripos( (string) file_get_contents( $f->getPathname() ), 'compress' ) !== false ) { $files[] = substr( $f->getPathname(), strlen( $dir ) + 1 ); }
		}
	}
	$encode = [];
	foreach ( [ 'image/webp', 'image/avif', 'image/jpeg' ] as $mime ) { $encode[ $mime ] = wp_image_editor_supports( [ 'mime_type' => $mime ] ); }
	// Read-only: the saved presets through Etch's own route (as an admin), and how its service stores them.
	$admins = get_users( [ 'role' => 'administrator', 'number' => 1, 'fields' => 'ID' ] );
	if ( $admins ) { wp_set_current_user( (int) $admins[0] ); }
	$res     = rest_do_request( new WP_REST_Request( 'GET', '/etch-api/compression-presets' ) );
	$presets = [ 'status' => $res->get_status(), 'data' => $res->get_data() ];
	wp_set_current_user( 0 );
	$svc     = $dir . '/classes/Services/CompressionPresetService.php';
	$storage = is_file( $svc ) ? array_values( array_filter( array_map( 'trim', file( $svc ) ), fn( $l ) => preg_match( '/get_option|update_option|post_type|\$wpdb|table|const |register_post_type|get_posts|meta/i', $l ) ) ) : [];
	// How the browser worker turns a preset into an encode (quality from 'compression', the 'resize' shape): short
	// excerpts around those words in Etch's own compress worker and preset service, read-only.
	$excerpts = [];
	foreach ( glob( $dir . '/apps/dist/builder/compress.worker-*.js' ) ?: [] as $wf ) {
		$js = (string) file_get_contents( $wf );
		foreach ( [ 'quality', 'resize', 'compression', 'maxWidth', 'width' ] as $word ) {
			$at = 0;
			for ( $n = 0; $n < 3 && ( $at = stripos( $js, $word, $at ) ) !== false; $n++, $at += strlen( $word ) ) {
				$excerpts[ $word ][] = substr( $js, max( 0, $at - 90 ), 180 );
			}
		}
	}
	$svc_resize = is_file( $svc ) ? array_values( array_filter( array_map( 'trim', file( $svc ) ), fn( $l ) => stripos( $l, 'resize' ) !== false || stripos( $l, 'compression' ) !== false ) ) : [];
	$compressor = [ 'presets' => $presets, 'worker_excerpts' => $excerpts, 'service_lines' => array_slice( $svc_resize, 0, 30 ), 'preset_storage' => array_slice( $storage, 0, 25 ), 'rest_routes' => $routes, 'options' => $popts, 'files_mentioning_compress' => $files, 'server_can_encode' => $encode, 'imagick' => extension_loaded( 'imagick' ), 'gd' => extension_loaded( 'gd' ) ];
	$out = [ 'active_theme' => get_stylesheet(), 'posts' => $out, 'asset_storage' => [ 'attachment_taxonomies' => $tax, 'options' => $opts, 'post_types' => $types, 'attachment_meta' => $meta ], 'etch_compressor' => $compressor ];
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
