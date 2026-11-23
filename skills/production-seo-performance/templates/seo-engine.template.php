<?php
/**
 * Template: Centralized SEO & Schema.org Knowledge Graph Engine
 *
 * Features:
 * 1. Priority-0 Staging Environment Guard (noindex/nofollow on non-production).
 * 2. Dynamic Open Graph & Twitter Cards with contextual fallbacks.
 * 3. Unified Schema.org @graph (LocalBusiness / Organization, Founder, Facility, Service, FAQPage).
 * 4. High-CTR rich snippet optimization for Google SERPs.
 *
 * @package ProductionSEO
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

/**
 * -------------------------------------------------------------------------
 * 1. STAGING ENVIRONMENT GUARD (PRIORITY 0)
 * -------------------------------------------------------------------------
 * Prevents non-production hosts from being indexed or polluting the live
 * Schema.org entity graph.
 * -------------------------------------------------------------------------
 */
define( 'PROD_SEO_STAGING_HOST', 'staging.example.com' );

function prod_seo_is_staging() {
    $host = isset( $_SERVER['HTTP_HOST'] ) ? strtolower( trim( $_SERVER['HTTP_HOST'] ) ) : '';
    return ( $host === PROD_SEO_STAGING_HOST || strpos( $host, 'localhost' ) !== false || strpos( $host, '.test' ) !== false );
}

if ( prod_seo_is_staging() ) {
    add_action( 'wp_head', function() {
        echo "\n  <!-- NON-PRODUCTION ENVIRONMENT: Search indexing disabled -->\n";
        echo "  <meta name=\"robots\" content=\"noindex, nofollow, noarchive, nosnippet\">\n";
        echo "  <meta name=\"googlebot\" content=\"noindex, nofollow\">\n";
    }, 0 );

    // Bail out — do not output production SEO or Schema hooks below
    return;
}

/**
 * -------------------------------------------------------------------------
 * 2. CONTEXTUAL METADATA RESOLVER
 * -------------------------------------------------------------------------
 */
function prod_seo_get_context() {
    $site_url  = home_url( '/' );
    $theme_uri = get_stylesheet_directory_uri();

    $context = array(
        'title'       => 'Brand Name — Visual Direction & Production Studio',
        'description' => 'Commercial photography, visual identity, and studio production.',
        'canonical'   => home_url( '/' ),
        'image'       => $theme_uri . '/assets/images/og-default.jpg',
        'image_alt'   => 'Brand Name Studio Production',
        'faqs'        => array(),
    );

    if ( is_front_page() ) {
        $context['title']       = 'Brand Name — Production Studio & Visual Direction';
        $context['description'] = 'Commercial campaigns, executive portraits, and broadcast audio-video production led by CharNithi.';
        $context['canonical']   = home_url( '/' );
    }

    return apply_filters( 'prod_seo_page_context', $context );
}

/**
 * -------------------------------------------------------------------------
 * 3. OPEN GRAPH & TWITTER CARD OUTPUT
 * -------------------------------------------------------------------------
 */
add_action( 'wp_head', function() {
    $ctx = prod_seo_get_context();
    ?>
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="<?php echo esc_url( $ctx['canonical'] ); ?>">
    <meta property="og:title" content="<?php echo esc_attr( $ctx['title'] ); ?>">
    <meta property="og:description" content="<?php echo esc_attr( $ctx['description'] ); ?>">
    <meta property="og:image" content="<?php echo esc_url( $ctx['image'] ); ?>">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:url" content="<?php echo esc_url( $ctx['canonical'] ); ?>">
    <meta name="twitter:title" content="<?php echo esc_attr( $ctx['title'] ); ?>">
    <meta name="twitter:description" content="<?php echo esc_attr( $ctx['description'] ); ?>">
    <meta name="twitter:image" content="<?php echo esc_url( $ctx['image'] ); ?>">
    <?php
}, 1 );

/**
 * -------------------------------------------------------------------------
 * 4. SCHEMA.ORG INTERLINKED KNOWLEDGE GRAPH (@graph)
 * -------------------------------------------------------------------------
 */
add_action( 'wp_head', function() {
    $ctx       = prod_seo_get_context();
    $site_url  = home_url( '/' );
    $theme_uri = get_stylesheet_directory_uri();

    $graph = array(
        // Business Entity
        array(
            '@type'            => array( 'LocalBusiness', 'ProfessionalService' ),
            '@id'              => $site_url . '#business',
            'name'             => 'Brand Name',
            'url'              => $site_url,
            'logo'             => $theme_uri . '/assets/images/logo.png',
            'founder'          => array(
                '@type' => 'Person',
                '@id'   => $site_url . '#founder',
                'name'  => 'CharNithi',
                'jobTitle' => 'Visual Director'
            ),
            'address'          => array(
                '@type'           => 'PostalAddress',
                'addressLocality' => 'City',
                'addressRegion'   => 'Region',
                'addressCountry'  => 'IN'
            )
        ),
        // WebPage Entity
        array(
            '@type'      => 'WebPage',
            '@id'        => $ctx['canonical'] . '#webpage',
            'url'        => $ctx['canonical'],
            'name'       => $ctx['title'],
            'description'=> $ctx['description'],
            'isPartOf'   => array( '@id' => $site_url . '#business' )
        )
    );

    // Optional: FAQPage Entity for Rich SERP Snippets
    if ( ! empty( $ctx['faqs'] ) ) {
        $faq_entities = array();
        foreach ( $ctx['faqs'] as $faq ) {
            $faq_entities[] = array(
                '@type'          => 'Question',
                'name'           => $faq['q'],
                'acceptedAnswer' => array(
                    '@type' => 'Answer',
                    'text'  => $faq['a']
                )
            );
        }
        $graph[] = array(
            '@type'      => 'FAQPage',
            '@id'        => $ctx['canonical'] . '#faq',
            'mainEntity' => $faq_entities
        );
    }

    $schema_payload = array(
        '@context' => 'https://schema.org',
        '@graph'   => $graph
    );

    echo "\n  <!-- Schema.org Knowledge Graph -->\n";
    echo "  <script type=\"application/ld+json\">\n";
    echo wp_json_encode( $schema_payload, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT );
    echo "\n  </script>\n";
}, 2 );
