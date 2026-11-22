<?php
/**
 * Canonical Bespoke Dynamic Block Render Template
 *
 * @package WordPress
 * @subpackage Theme_Namespace
 *
 * @var array    $attributes Block attributes.
 * @var string   $content    Block inner content.
 * @var WP_Block $block      Block instance.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

// 1. Resolve entity context dynamically or via attribute override
$entity_id = ! empty( $attributes['entityId'] ) ? sanitize_text_field( $attributes['entityId'] ) : 'default';

// 2. Fetch record from declarative registry
$record = function_exists( 'theme_get_entity_record' ) ? theme_get_entity_record( $entity_id ) : array();

if ( empty( $record ) ) {
	return;
}

$theme_class = ! empty( $record['theme_class'] ) ? esc_attr( $record['theme_class'] ) : '';
?>
<section class="m-feature-block <?php echo $theme_class; ?>" aria-label="<?php echo esc_attr( $record['title'] ); ?>">
	<div class="l-container">
		<header class="m-feature-block__header">
			<?php if ( ! empty( $record['badge'] ) ) : ?>
				<span class="m-feature-block__badge"><?php echo esc_html( $record['badge'] ); ?></span>
			<?php endif; ?>
			<h2 class="m-feature-block__title"><?php echo esc_html( $record['title'] ); ?></h2>
			<?php if ( ! empty( $record['subtitle'] ) ) : ?>
				<p class="m-feature-block__subtitle"><?php echo esc_html( $record['subtitle'] ); ?></p>
			<?php endif; ?>
		</header>

		<div class="m-feature-block__grid">
			<?php if ( ! empty( $record['items'] ) && is_array( $record['items'] ) ) : ?>
				<?php foreach ( $record['items'] as $item ) : ?>
					<article class="m-feature-block__card">
						<?php if ( ! empty( $item['image'] ) ) : ?>
							<div class="m-feature-block__photo-wrap">
								<img 
									src="<?php echo esc_url( $item['image'] ); ?>" 
									alt="<?php echo esc_attr( $item['title'] ); ?>" 
									class="m-feature-block__photo" 
									loading="lazy"
								/>
							</div>
						<?php endif; ?>
						<div class="m-feature-block__body">
							<h3 class="m-feature-block__item-title"><?php echo esc_html( $item['title'] ); ?></h3>
							<p class="m-feature-block__item-desc"><?php echo esc_html( $item['desc'] ); ?></p>
						</div>
					</article>
				<?php endforeach; ?>
			<?php endif; ?>
		</div>
	</div>
</section>
