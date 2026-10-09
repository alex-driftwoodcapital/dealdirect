<?php
/**
 * Page feel and loading: the site font is preloaded (it is ACSS's font-1-src; without a preload the text first paints in
 * a fallback face and jumps when Plus Jakarta Sans arrives), and in-page links (the section bar, footnotes) scroll
 * smoothly instead of jumping, unless the visitor asks for reduced motion. Linked sections land below the fixed header
 * (68px) and, on offering pages, the sticky section bar.
 */
namespace DealDirect;

const FONT_PATH = 'assets/fonts/plus-jakarta-sans-latin-wght-normal.woff2';

function font_preload( string $url ): string {
	return '<link rel="preload" href="' . $url . '" as="font" type="font/woff2" crossorigin>' . "\n";
}

function motion_css(): string {
	return '<style id="dd-motion">@media (prefers-reduced-motion:no-preference){html{scroll-behavior:smooth}}'
		. 'html{scroll-padding-top:84px}html:has(.offering-subnav){scroll-padding-top:136px}</style>' . "\n";
}

if ( function_exists( 'add_action' ) ) {
	add_action( 'wp_head', function () {
		echo font_preload( esc_url( plugins_url( FONT_PATH, __DIR__ . '/../dealdirect-core.php' ) ) );
		echo motion_css();
	}, 2 );
}
