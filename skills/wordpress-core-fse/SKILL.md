---
name: wordpress-core-fse
description: >-
  Architectural procedure and production runbook for engineering high-performance,
  decoupled WordPress Full Site Editing (FSE) block themes. Enforces a strict 8pt grid,
  theme.json tokenization, bespoke dynamic blocks (block.json v3 + render.php),
  SMACSS modular styling without Gutenberg inline layout constraints, declarative
  data registries, and resilient hybrid template fallbacks.
---

# WordPress Core & FSE Architectural Runbook

Follow this runbook when building, refactoring, or auditing WordPress Full Site Editing (FSE) block themes and bespoke blocks. This procedure enforces production-grade decoupling, eliminates Gutenberg layout fragility, and ensures seamless long-term maintainability.

---

## 🛑 Non-Negotiable Hard-Gate Rules

When an AI agent executes tasks under this skill, the following four production hard-gates must be strictly respected:

1. **Zero Inline Layout Styling**: Never inject layout styles (`style="display: flex"`, `style="padding:..."`, `style="margin:..."`, `style="grid-template-columns:..."`) directly into block markup or template parts. All layout orchestration belongs in the theme's SMACSS layout or module layers.
2. **Strict 8pt Grid Quantization**: All spacing presets in `theme.json` (`spacingSizes`) and CSS layout rules must strictly follow an 8pt mathematical scale (`8px`, `16px`, `24px`, `32px`, `40px`, `48px`, `56px`, `64px`, `80px`, `96px`). Arbitrary one-off spacing values (`13px`, `27px`, `55px`) are forbidden.
3. **Declarative SSOT Data Registries**: For multi-entity datasets (e.g. branch campuses, clinic locations, academic departments, recurring program suites), never hardcode data into page post content. Store data declaratively in PHP registries and inject it dynamically via context resolvers.
4. **Bespoke Dynamic Block Standard**: All custom blocks must use the native Block API v3 (`block.json`), declare server-side rendering (`"render": "file:./render.php"`), and output clean, semantic BEM markup (`.m-<block>__<element>--<modifier>`).

---

## 🏛️ Phase 1: `theme.json` Token Codification

The `theme.json` file is the central design contract of an FSE theme. It must codify the 8pt spacing system, fluid typography, and a semantic color palette.

### 1. 8pt Spacing Token Grid
Ensure `defaultSpacingSizes` is disabled so Gutenberg does not inject unquantized default increments:

```json
{
  "$schema": "https://schemas.wp.org/trunk/theme.json",
  "version": 3,
  "settings": {
    "spacing": {
      "defaultSpacingSizes": false,
      "customSpacingSize": true,
      "spacingScale": { "steps": 0 },
      "spacingSizes": [
        { "name": "8px (1 unit)",   "size": "8px",  "slug": "10" },
        { "name": "16px (2 units)", "size": "16px", "slug": "20" },
        { "name": "24px (3 units)", "size": "24px", "slug": "30" },
        { "name": "32px (4 units)", "size": "32px", "slug": "40" },
        { "name": "40px (5 units)", "size": "40px", "slug": "50" },
        { "name": "48px (6 units)", "size": "48px", "slug": "60" },
        { "name": "56px (7 units)", "size": "56px", "slug": "70" },
        { "name": "64px (8 units)", "size": "64px", "slug": "80" },
        { "name": "80px (10 units)", "size": "80px", "slug": "100" },
        { "name": "96px (12 units)", "size": "96px", "slug": "120" }
      ],
      "units": ["px", "rem", "%", "vw", "vh"]
    }
  }
}
```

### 2. Fluid Typographic Hierarchy
Pair an editorial display family with a functional UI body font. Use harmonic size steps (`xs` to `5xl`) mapped to CSS custom properties `--wp--preset--font-size--*`.

---

## 🧱 Phase 2: Bespoke Dynamic Blocks (`block.json` + `render.php`)

Avoid client-side React block builds for high-content or dynamic entities. Use native server-rendered blocks:

### 1. `block.json` Schema (API v3)
Create each block inside `blocks/<block-slug>/block.json`:

```json
{
  "$schema": "https://schemas.wp.org/trunk/block.json",
  "apiVersion": 3,
  "name": "namespace/block-slug",
  "version": "1.0.0",
  "title": "Block Human Title",
  "category": "theme-category",
  "description": "Clear functional description of the block.",
  "supports": {
    "html": false,
    "align": ["wide", "full"]
  },
  "render": "file:./render.php"
}
```

### 2. `render.php` Implementation Pattern
Always resolve context, sanitize inputs, and produce semantic BEM markup:

```php
<?php
/**
 * Dynamic Block Server Render
 *
 * @var array    $attributes Block attributes.
 * @var string   $content    Block default content.
 * @var WP_Block $block      Block instance.
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

// 1. Resolve entity context dynamically
$entity_id = Context_Resolver::get_current_id();
$data      = Data_Registry::get_record( $entity_id );

if ( empty( $data ) ) {
    return;
}

// 2. Output BEM markup without inline layout styles
?>
<section class="m-feature-block <?php echo esc_attr( $data['theme_class'] ?? '' ); ?>">
    <div class="l-container">
        <header class="m-feature-block__header">
            <span class="m-feature-block__badge"><?php echo esc_html( $data['badge'] ); ?></span>
            <h2 class="m-feature-block__title"><?php echo esc_html( $data['title'] ); ?></h2>
        </header>
        <div class="m-feature-block__grid">
            <!-- Dynamic Content Loop -->
        </div>
    </div>
</section>
```

---

## 🎨 Phase 3: Decoupled SMACSS Layout Architecture

Organize theme styles using the 5-layer SMACSS methodology in `style.css`:

```text
assets/css/
├── base/        # CSS variables, typography, resets, element defaults
├── layout/      # Containers (.l-container), grids (.l-grid-*), header, footer
├── modules/     # Reusable components (.m-card, .m-hero, .m-carousel) with strict BEM
├── state/       # Dynamic states (.is-active, .is-open, .is-scrolled)
└── theme/       # Entity or branch color overrides (.theme-branch-a, .theme-branch-b)
```

### Complex Layouts vs. Gutenberg Constraints
When dealing with complex requirements (multi-stop directional gradients, asymmetric focal centering, or scroll-snap rails):
- **Never nest multiple core/group blocks** with ad-hoc padding to simulate layout.
- Create a dedicated module (`.m-<component>`) and leverage modern CSS (`display: grid`, `scroll-snap-type: x mandatory`, `@media (max-width: 1024px)`).
- Provide hardware-accelerated animations on GPU transforms (`transform: translateY(-4px)`).

---

## 🗄️ Phase 4: Declarative Data Registries & Meta Boxes

For websites managing multiple branches, locations, or service lines:

1. **Single Source of Truth (SSOT)**: Store baseline entity metadata in a centralized PHP associative registry (`inc/entity-registry.php`). Adding an entity requires only appending a structured configuration array.
2. **Campus Identity Meta Box**: Expose non-technical editing panels via `add_meta_box` on the target post type. Sanitized field updates allow staff to modify subtitles, contact numbers, and badges without touching block markup.
3. **Context Provider**: Implement a lightweight singleton class (e.g. `Theme_Context`) that inspects the current query, URL slug, or taxonomy term to deliver the appropriate record to `render.php`.

---

## 🔄 Phase 5: Resilient Hybrid Template Rendering

To prevent breaking existing pages when new bespoke blocks are deployed across an established fleet:

Implement a hybrid rendering filter or wrapper in `template.php` / `page.html`:
```php
$current_post = get_post();
if ( $current_post && ! empty( trim( $current_post->post_content ) ) ) {
    $content = trim( $current_post->post_content );
    
    // Auto-inject missing bespoke blocks before terminal blocks
    if ( ! str_contains( $content, 'namespace/new-milestones-block' ) ) {
        $injection = "<!-- wp:namespace/new-milestones-block /-->\n";
        if ( str_contains( $content, '<!-- wp:namespace/contact-card' ) ) {
            $content = str_replace( '<!-- wp:namespace/contact-card', $injection . '<!-- wp:namespace/contact-card', $content );
        } else {
            $content .= "\n" . $injection;
        }
    }
    
    echo do_blocks( $content );
} else {
    // Fallback block sequence
    echo do_blocks( '<!-- wp:namespace/hero /-->' );
    echo do_blocks( '<!-- wp:namespace/new-milestones-block /-->' );
}
```

---

## 🧪 Phase 6: Automated Verification

Always execute the included theme validator before concluding any FSE task:

```bash
python3 scripts/validate_fse_theme.py --theme-path /path/to/theme
```

The script verifies:
- `theme.json` JSON validity and schema version.
- Exact compliance of `spacingSizes` with the 8pt quantized grid.
- All `blocks/*/block.json` use API v3 and valid render paths.
- Zero forbidden inline layout styles present in `render.php` and template files.
