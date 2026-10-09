<?php
/**
 * Google Tag Manager, as on the live site (GTM-NX8DQZGQ; live loads GTM only: other tags, HubSpot's tracking
 * included, live inside the container). The standard snippet: the script in <head>, the noscript iframe right after
 * <body>. Loaded only while the site is public ("Discourage search engines" off), so staging traffic never reaches
 * the live analytics; define DD_GTM_ON_STAGING (wp-config) to test it on staging.
 */
namespace DealDirect;

const GTM_ID = 'GTM-NX8DQZGQ';

/** Whether GTM loads on this site. */
function gtm_enabled( bool $site_public, bool $staging_override ): bool {
	return $site_public || $staging_override;
}

function gtm_head( string $id ): string {
	return "<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});"
		. "var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;"
		. "j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);"
		. "})(window,document,'script','dataLayer','" . $id . "');</script>\n";
}

function gtm_body( string $id ): string {
	return '<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=' . $id
		. '" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>' . "\n";
}

if ( function_exists( 'add_action' ) ) {
	$on = fn() => gtm_enabled( (bool) get_option( 'blog_public' ), defined( 'DD_GTM_ON_STAGING' ) && DD_GTM_ON_STAGING );
	add_action( 'wp_head', function () use ( $on ) { if ( $on() ) { echo gtm_head( GTM_ID ); } }, 1 );
	add_action( 'wp_body_open', function () use ( $on ) { if ( $on() ) { echo gtm_body( GTM_ID ); } }, 1 );
}
