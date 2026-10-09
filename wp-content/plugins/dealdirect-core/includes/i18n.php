<?php
/**
 * Page languages for the EB-5 pages (handoff/docs/eb5-localization.md): <html lang> per page and hreflang alternates
 * (en / es / pt-BR + x-default -> the EN page). Pages not listed keep the site language. /new-eb-5-page/ is left out:
 * it is a noindex ads landing page, not an alternate of /eb-5-investments/.
 */
namespace DealDirect;

const PAGE_LANGS = [
	'eb-5-investments'   => 'en',
	'inversiones-eb-5'   => 'es',
	'investimentos-eb-5' => 'pt-BR',
];
const X_DEFAULT = 'eb-5-investments';

/** hreflang => URL for every page in the group (pure; $home ends with "/"). */
function hreflang_links( string $home ): array {
	$links = [];
	foreach ( PAGE_LANGS as $slug => $lang ) {
		$links[ $lang ] = $home . $slug . '/';
	}
	$links['x-default'] = $home . X_DEFAULT . '/';
	return $links;
}

/** The lang attribute value for a page slug, or null to keep the site language. */
function page_lang( string $slug ): ?string {
	return PAGE_LANGS[ $slug ] ?? null;
}

if ( function_exists( 'add_filter' ) ) {
	$current_slug = function (): string {
		$post = is_page() ? get_queried_object() : null;
		return $post instanceof \WP_Post ? $post->post_name : '';
	};
	add_filter( 'language_attributes', function ( $output ) use ( $current_slug ) {
		$lang = page_lang( $current_slug() );
		return $lang ? preg_replace( '/lang="[^"]*"/', 'lang="' . esc_attr( $lang ) . '"', $output ) : $output;
	} );
	add_action( 'wp_head', function () use ( $current_slug ) {
		if ( ! page_lang( $current_slug() ) ) {
			return;
		}
		foreach ( hreflang_links( trailingslashit( home_url() ) ) as $lang => $url ) {
			printf( '<link rel="alternate" hreflang="%s" href="%s" />' . "\n", esc_attr( $lang ), esc_url( $url ) );
		}
	} );
}
