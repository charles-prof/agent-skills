<?php
/**
 * Declarative Single Source of Truth (SSOT) Entity Registry
 *
 * @package WordPress
 * @subpackage Theme_Namespace
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Returns all registered entity configurations.
 *
 * @return array<string, array>
 */
function theme_get_entity_registry() {
	return array(
		'headquarters' => array(
			'id'          => 'headquarters',
			'title'       => 'Central Campus & Innovation Center',
			'subtitle'    => 'Pioneering experiential learning and creative growth',
			'badge'       => 'Admissions Open 2026–27',
			'theme_class' => 'theme-primary',
			'phone'       => '+91 99440 00000',
			'email'       => 'admissions@example.com',
			'items'       => array(
				array(
					'title' => 'STEM & Robotics Lab',
					'desc'  => 'Hands-on experiential discovery pods for young learners.',
					'image' => get_theme_file_uri( 'assets/photos/stem.webp' ),
				),
				array(
					'title' => 'Visual Arts Studio',
					'desc'  => 'Creative sketch, painting, and tactile expression.',
					'image' => get_theme_file_uri( 'assets/photos/art.webp' ),
				),
			),
		),
	);
}

/**
 * Resolves a single entity by its identifier.
 *
 * @param string $id Entity identifier.
 * @return array|null
 */
function theme_get_entity_record( $id ) {
	$registry = theme_get_entity_registry();
	return $registry[ $id ] ?? null;
}
