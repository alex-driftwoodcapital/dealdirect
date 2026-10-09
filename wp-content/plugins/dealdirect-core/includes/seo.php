<?php
/**
 * SEO head tags, carried over from the live site (Rank Math there; CLAUDE.md: SEO title/OG lifted verbatim): document
 * title, robots, Open Graph and Twitter tags. Per-post data is the post meta `_dd_seo` (JSON) the deploy writes from a
 * page's META['seo']: title (when it differs from "<post title> - <site>"), robots (when it differs from the live
 * default), og_image (attachment id) and og_image_alt. Live pages have no meta description, so none is printed.
 * Robots are left to WordPress while "Discourage search engines" is on (staging stays noindex).
 */
namespace DealDirect;

const SEO_SITE       = 'Driftwood Capital | DealDirect';  // live title suffix
const SEO_SITE_NAME  = 'Driftwood DealDirect';            // live og:site_name
const DEFAULT_ROBOTS = 'follow, index, max-snippet:-1, max-video-preview:-1, max-image-preview:large';
const OG_LOCALES     = [ 'en' => 'en_US', 'es' => 'es_ES', 'pt-BR' => 'pt_BR' ];

/** The document title: the page's own SEO title, else "<post title> - <site>" (live pattern). */
function seo_title( string $post_title, array $seo ): string {
	return ! empty( $seo['title'] ) ? $seo['title'] : $post_title . ' - ' . SEO_SITE;
}

/** A robots string ("follow, noindex, max-snippet:-1") as wp_robots directives: [name => true|value]. */
function robots_directives( string $robots ): array {
	$out = [];
	foreach ( array_filter( array_map( 'trim', explode( ',', $robots ) ) ) as $d ) {
		[ $k, $v ] = array_pad( explode( ':', $d, 2 ), 2, true );
		$out[ $k ] = $v;
	}
	return $out;
}

if ( function_exists( 'add_filter' ) ) {
	$seo_of = function (): ?array {
		if ( ! is_singular() ) {
			return null;
		}
		$raw = get_post_meta( get_queried_object_id(), '_dd_seo', true );
		$seo = $raw ? json_decode( $raw, true ) : [];
		return is_array( $seo ) ? $seo : [];
	};
	add_filter( 'pre_get_document_title', function ( $title ) use ( $seo_of ) {
		$seo = $seo_of();
		return $seo === null ? $title : seo_title( html_entity_decode( get_the_title( get_queried_object_id() ), ENT_QUOTES, 'UTF-8' ), $seo );
	} );
	add_filter( 'wp_robots', function ( $robots ) use ( $seo_of ) {
		$seo = $seo_of();
		if ( $seo === null || ! get_option( 'blog_public' ) ) {
			return $robots;  // staging: WordPress's noindex stays
		}
		return robots_directives( $seo['robots'] ?? DEFAULT_ROBOTS );
	} );
	add_action( 'wp_head', function () use ( $seo_of ) {
		$seo = $seo_of();
		if ( $seo === null ) {
			return;
		}
		$id    = get_queried_object_id();
		$title = wp_get_document_title();
		$lang  = function_exists( __NAMESPACE__ . '\\page_lang' ) ? page_lang( get_post_field( 'post_name', $id ) ) : null;
		$tags  = [
			'og:locale'       => OG_LOCALES[ $lang ?? 'en' ],
			'og:type'         => is_front_page() ? 'website' : 'article',
			'og:title'        => $title,
			'og:url'          => get_permalink( $id ),
			'og:site_name'    => SEO_SITE_NAME,
			'og:updated_time' => get_post_modified_time( 'c', false, $id ),
		];
		$img = ! empty( $seo['og_image'] ) ? wp_get_attachment_image_src( (int) $seo['og_image'], 'full' ) : false;
		if ( $img ) {
			$tags += [ 'og:image' => $img[0], 'og:image:secure_url' => $img[0], 'og:image:width' => $img[1], 'og:image:height' => $img[2],
				'og:image:alt' => $seo['og_image_alt'] ?? '', 'og:image:type' => get_post_mime_type( (int) $seo['og_image'] ) ];
		}
		foreach ( $tags as $p => $v ) {
			printf( '<meta property="%s" content="%s" />' . "\n", esc_attr( $p ), esc_attr( (string) $v ) );
		}
		printf( '<meta name="twitter:card" content="summary_large_image" />' . "\n" . '<meta name="twitter:title" content="%s" />' . "\n", esc_attr( $title ) );
		if ( $img ) {
			printf( '<meta name="twitter:image" content="%s" />' . "\n", esc_attr( $img[0] ) );
		}
	}, 5 );
	// Live prints no canonical on noindex pages.
	add_action( 'wp', function () use ( $seo_of ) {
		$seo = $seo_of();
		if ( $seo && isset( robots_directives( $seo['robots'] ?? '' )['noindex'] ) ) {
			remove_action( 'wp_head', 'rel_canonical' );
		}
	} );
}
