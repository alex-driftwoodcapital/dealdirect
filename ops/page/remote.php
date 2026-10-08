<?php
// Host-side helper for ops/page/deploy.py. Run: wp eval-file remote.php <action> <json-file> <dry|write>
// Never touches anything but the named media, etch_styles records and page meta. Prints one JSON object.
[ $action, $file, $mode ] = [ $args[0] ?? '', $args[1] ?? '', $args[2] ?? 'dry' ];
$in    = $file ? json_decode( (string) file_get_contents( $file ), true ) : [];
$write = $mode === 'write';
$out   = [];

// Etch Asset Manager compression, done server-side the way the builder does it (staging, Etch 1.6.8): presets live in
// the etch_compression_presets option {name, compression 0-100, outputFormat webp|avif|jpeg|png, overwrite, resize};
// the builder encodes with quality = 100 - compression; resize is {type: axis (axis width|height) | side (side
// long|short), pixels, downscaleOnly} or {type: scale, ...}. The builder's own encoder (Squoosh) runs in the
// browser, so deploy imports apply the same preset here with WordPress's image editor.
function dd_preset( ?string $want ) {
	$all = array_values( array_filter( (array) get_option( 'etch_compression_presets', [] ), 'is_array' ) );
	if ( $want !== null && $want !== '' ) {
		foreach ( $all as $p ) { if ( ( $p['name'] ?? '' ) === $want ) { return $p; } }
		return new WP_Error( 'preset', "no Etch compression preset named \"$want\" (saved: " . ( implode( ', ', array_column( $all, 'name' ) ) ?: 'none' ) . ')' );
	}
	if ( count( $all ) === 1 ) { return $all[0]; }
	return new WP_Error( 'preset', $all
		? 'several Etch compression presets (' . implode( ', ', array_column( $all, 'name' ) ) . '): set COMPRESS_PRESET in the staging profile'
		: 'no Etch compression preset saved: create one in the Asset Manager (Etch builder) first' );
}

function dd_preset_label( array $p ): string {
	$r = $p['resize'] ?? null;
	$rs = ! is_array( $r ) ? 'no resize' : ( ( $r['type'] ?? '' ) === 'scale' ? 'scale ' . ( $r['scale'] ?? $r['factor'] ?? '?' )
		: ( ( $r[ $r['type'] ] ?? '?' ) . ' ' . ( $r['pixels'] ?? '?' ) . 'px' . ( ! empty( $r['downscaleOnly'] ) ? ' (downscale only)' : '' ) ) );
	return sprintf( '"%s": %s q%d, %s', $p['name'] ?? '?', $p['outputFormat'] ?? 'webp', 100 - (int) ( $p['compression'] ?? 25 ), $rs );
}

// Returns [path, filename] of the compressed file, or WP_Error. $name keeps its basename, new extension.
function dd_compress( string $file, string $name, array $p ) {
	$fmt  = $p['outputFormat'] ?? 'webp';
	$mime = [ 'webp' => 'image/webp', 'avif' => 'image/avif', 'jpeg' => 'image/jpeg', 'png' => 'image/png' ][ $fmt ] ?? null;
	if ( ! $mime || ! wp_image_editor_supports( [ 'mime_type' => $mime ] ) ) { return new WP_Error( 'fmt', "server cannot encode $fmt" ); }
	$ed = wp_get_image_editor( $file );
	if ( is_wp_error( $ed ) ) { return $ed; }
	[ 'width' => $w, 'height' => $h ] = $ed->get_size();
	$r = $p['resize'] ?? null;
	if ( is_array( $r ) && $w && $h ) {
		$type = $r['type'] ?? '';
		if ( $type === 'scale' ) {
			$f = (float) ( $r['scale'] ?? $r['factor'] ?? 0 );
			if ( $f <= 0 ) { return new WP_Error( 'resize', 'scale preset without a factor: ' . wp_json_encode( $r ) ); }
			[ $tw, $th ] = [ (int) round( $w * $f ), (int) round( $h * $f ) ];
		} else {
			$dim = $type === 'axis' ? ( ( $r['axis'] ?? '' ) === 'height' ? 'h' : 'w' )
				: ( ( ( $r['side'] ?? '' ) === 'short' ) === ( $w >= $h ) ? 'h' : 'w' );  // long side of a landscape = width
			$px  = (int) ( $r['pixels'] ?? 0 );
			$cur = $dim === 'w' ? $w : $h;
			$f   = $px > 0 ? $px / $cur : 1;
			[ $tw, $th ] = [ (int) round( $w * $f ), (int) round( $h * $f ) ];
		}
		$down_only = ! empty( $r['downscaleOnly'] );
		if ( $tw > 0 && $th > 0 && ( $tw < $w || ( ! $down_only && $tw !== $w ) ) ) {
			$res = $ed->resize( $tw, $th, false );
			if ( is_wp_error( $res ) ) { return $res; }
		}
	}
	$ed->set_quality( max( 1, min( 100, 100 - (int) ( $p['compression'] ?? 25 ) ) ) );
	$out_name = pathinfo( $name, PATHINFO_FILENAME ) . '.' . ( $fmt === 'jpeg' ? 'jpg' : $fmt );
	$saved    = $ed->save( get_temp_dir() . 'dd-' . wp_generate_password( 8, false ) . '-' . $out_name, $mime );
	return is_wp_error( $saved ) ? $saved : [ $saved['path'], $out_name ];
}

if ( $action === 'media' ) {
	// $in: {preset: name|null, items: {slug: {src, collection[, name]}}}. src = host path of an uploaded local file, or a
	// URL (the host downloads it). Images are compressed with the Etch preset before import (videos, SVG and PDFs as
	// they are); the source filename is kept in _dd_source so the next run finds the image again. Every file goes into
	// its Etch Asset Manager collection (taxonomy etch_collection); missing collections are created, existing kept.
	require_once ABSPATH . 'wp-admin/includes/file.php';
	require_once ABSPATH . 'wp-admin/includes/media.php';
	require_once ABSPATH . 'wp-admin/includes/image.php';
	global $wpdb;
	$tax = 'etch_collection';
	if ( ! taxonomy_exists( $tax ) ) { WP_CLI::error( "taxonomy $tax not registered: is Etch active?" ); }
	$preset = null;
	foreach ( $in['items'] as $slug => $m ) {
		[ $src, $coll ] = [ $m['src'], $m['collection'] ];
		$name = $m['name'] ?? basename( parse_url( $src, PHP_URL_PATH ) );  // name: for sources whose URL has no filename
		// A previous run: our import of this source (_dd_source), else the same filename in the library. Never re-upload.
		$id = (int) $wpdb->get_var( $wpdb->prepare( "SELECT post_id FROM {$wpdb->postmeta} WHERE meta_key = '_dd_source' AND meta_value = %s ORDER BY post_id LIMIT 1", $name ) );
		$id = $id ?: (int) $wpdb->get_var( $wpdb->prepare(
			"SELECT post_id FROM {$wpdb->postmeta} WHERE meta_key = '_wp_attached_file' AND (meta_value = %s OR meta_value LIKE %s) ORDER BY post_id LIMIT 1",
			$name, '%/' . $wpdb->esc_like( $name ) ) );
		$status = $id ? 'exists' : 'imported';
		if ( ! $id ) {
			$is_image = (bool) preg_match( '/\.(jpe?g|png|webp|avif)$/i', $name );
			if ( $is_image && $preset === null ) { $preset = dd_preset( $in['preset'] ?? null ); }
			if ( $is_image && is_wp_error( $preset ) ) { $out[ $slug ] = [ 'id' => null, 'status' => 'BLOCKED ' . $preset->get_error_message() ]; continue; }
			$how = $is_image ? 'compress with ' . dd_preset_label( $preset ) : 'as is';
			if ( ! $write ) { $out[ $slug ] = [ 'id' => null, 'status' => "would import $name ($how)", 'collection' => "would add to $coll" ]; continue; }
			$tmp = preg_match( '#^https?://#', $src ) ? download_url( $src, 120 ) : $src;
			if ( is_wp_error( $tmp ) ) { $out[ $slug ] = [ 'id' => null, 'status' => 'ERROR ' . $tmp->get_error_message() ]; continue; }
			[ $file, $file_name ] = [ $tmp, $name ];
			if ( $is_image ) {
				$c = dd_compress( $tmp, $name, $preset );
				if ( is_wp_error( $c ) ) { $out[ $slug ] = [ 'id' => null, 'status' => 'ERROR compress ' . $c->get_error_message() ]; continue; }
				[ $file, $file_name ] = $c;
				$status = sprintf( 'imported %s (%s, %d KB -> %d KB)', $file_name, dd_preset_label( $preset ), filesize( $tmp ) / 1024, filesize( $file ) / 1024 );
			}
			$id = media_handle_sideload( [ 'name' => $file_name, 'tmp_name' => $file ], 0 );
			if ( is_wp_error( $id ) ) { $out[ $slug ] = [ 'id' => null, 'status' => 'ERROR ' . $id->get_error_message() ]; continue; }
			update_post_meta( $id, '_dd_source', $name );
			if ( $is_image ) { update_post_meta( $id, '_dd_preset', $preset ); }
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
	// Etch compression presets the deploy applies to imported images (see dd_preset), and what the host can encode.
	$encode = [];
	foreach ( [ 'image/webp', 'image/avif', 'image/jpeg' ] as $mime ) { $encode[ $mime ] = wp_image_editor_supports( [ 'mime_type' => $mime ] ); }
	$compressor = [ 'presets' => array_map( 'dd_preset_label', array_values( array_filter( (array) get_option( 'etch_compression_presets', [] ), 'is_array' ) ) ), 'server_can_encode' => $encode ];
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
