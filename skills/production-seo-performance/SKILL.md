---
name: production-seo-performance
description: >-
  Architectural procedure and production runbook for engineering high-performance,
  zero-FOUC web applications with staging-guarded Schema.org Knowledge Graphs,
  100% self-hosted font pipelines, layout shift (CLS) prevention, and automated
  pre-release SEO & Core Web Vitals audit gates.
---

# Production SEO & Web Performance Architectural Runbook ⚡🔍

Follow this runbook when architecting, refactoring, or auditing technical SEO, Core Web Vitals (CWV), and asset delivery pipelines across web projects.

This procedure encodes hard-won production lessons into an executable standard: protecting domain authority from staging indexation leaks, eliminating render-blocking third-party font calls, constructing interconnected entity knowledge graphs, preventing layout shifts (CLS), and enforcing automated audit gates before release.

---

## 🛑 Non-Negotiable Hard-Gate Rules

When an AI agent or engineer operates under this skill, the following four production hard-gates must be strictly respected:

1. **Gate 1: Priority-0 Staging Environment Guard**  
   Non-production domains (staging, preview, dev, test) must inject a Priority-0 hard `noindex, nofollow, noarchive, nosnippet` meta tag and immediately bail out of all Schema.org structured data injection. Never allow staging environments to be indexed by search engines or pollute the live entity graph.

2. **Gate 2: 100% Self-Hosted Local Font Pipeline (Zero External Font Calls)**  
   External third-party font CDNs (e.g. `fonts.googleapis.com`, `fonts.gstatic.com`, Typekit) are strictly forbidden in production builds. All typography must be self-hosted locally in `.woff2` format, preloaded in critical CSS, and declared with `font-display: swap`. Any `@import url("http...")` in stylesheets is treated as a fatal build violation.

3. **Gate 3: Zero Cumulative Layout Shift (CLS < 0.1)**  
   Every image, video, SVG canvas, and embed must declare explicit intrinsic dimensions (`width` and `height`) or an explicit CSS `aspect-ratio`. Dynamic content or late-loading banners must never cause layout reflow. Native `loading="lazy"` and `decoding="async"` must be applied to all below-the-fold media.

4. **Gate 4: Pre-Release SEO & Core Web Vitals Audit Gate**  
   Before any code release, the automated verification script (`scripts/audit_production_readiness.py`) must execute and pass with zero errors. All pages must have canonical tags, descriptive titles, human meta descriptions, valid Schema.org `@graph` JSON-LD, zero font leaks, and zero missing image dimensions.

---

## 🏛️ Phase 1: Technical SEO & Entity Knowledge Graph Architecture

Modern search engines parse structured data as interconnected knowledge entities rather than disconnected microdata strings.

### 1. Priority-0 Staging Environment Guard
Place the staging guard at the very top of the `<head>` lifecycle (e.g. priority `0` in WordPress `wp_head` or top of HTML templates):

```php
// Check if current host is staging or non-production
define( 'APP_STAGING_HOST', 'staging.example.com' );

function is_staging_environment() {
    $host = isset( $_SERVER['HTTP_HOST'] ) ? strtolower( trim( $_SERVER['HTTP_HOST'] ) ) : '';
    return ( $host === APP_STAGING_HOST || str_contains( $host, 'localhost' ) || str_contains( $host, '.test' ) );
}

if ( is_staging_environment() ) {
    add_action( 'wp_head', function() {
        echo "\n  <!-- NON-PRODUCTION: Search indexing permanently disabled -->\n";
        echo "  <meta name=\"robots\" content=\"noindex, nofollow, noarchive, nosnippet\">\n";
        echo "  <meta name=\"googlebot\" content=\"noindex, nofollow\">\n";
    }, 0 );
    return; // Bail: Prevent structured data output on staging
}
```

### 2. Centralized Interlinked Schema.org `@graph`
All entity nodes (`LocalBusiness` / `Organization`, `Person` (founder/director), `Place` (facility), `Service`, `FAQPage`, `BreadcrumbList`) must link together inside a single `@graph` array using `@id` node identifiers:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": ["LocalBusiness", "ProfessionalService"],
      "@id": "https://example.com/#business",
      "name": "Brand Name",
      "url": "https://example.com/",
      "founder": {
        "@type": "Person",
        "@id": "https://example.com/#founder",
        "name": "CharNithi"
      },
      "location": {
        "@type": "Place",
        "@id": "https://example.com/#facility",
        "name": "Studio Facility"
      }
    },
    {
      "@type": "WebPage",
      "@id": "https://example.com/commercial/#webpage",
      "url": "https://example.com/commercial/",
      "name": "Commercial Services — Brand Name",
      "isPartOf": { "@id": "https://example.com/#business" }
    },
    {
      "@type": "FAQPage",
      "@id": "https://example.com/commercial/#faq",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "What commercial photography do you specialize in?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Products, spaces, food, and fashion campaigns."
          }
        }
      ]
    }
  ]
}
```

### 3. OpenGraph & Twitter Card Fallback Hierarchy
Each page must output standard social meta tags with guaranteed fallbacks:
- `og:title` & `twitter:title`: Concise, brand-aligned page title.
- `og:description` & `twitter:description`: Active, human description (< 155 characters).
- `og:image` & `twitter:image`: Absolute URL to high-resolution asset (1200×630px recommended).
- `og:url` & `canonical`: Exact self-referential canonical URL.

---

## ⚡ Phase 2: Zero-FOUC & Render-Blocking Optimization (FCP & LCP)

Render-blocking assets create Flash of Unstyled Content (FOUC), degrade First Contentful Paint (FCP), and damage Largest Contentful Paint (LCP).

### 1. 100% Self-Hosted Local Font Enforcer
1. Download `.woff2` formats for all font weights. Store them locally in `assets/fonts/`.
2. Define `@font-face` rules directly in critical CSS with `font-display: swap`:
   ```css
   @font-face {
     font-family: 'BrandFont';
     font-style: normal;
     font-weight: 400;
     font-display: swap;
     src: url('../fonts/brand-font-400.woff2') format('woff2');
   }
   ```
3. Preload primary heading and body font files in `<head>`:
   ```html
   <link rel="preload" href="/assets/fonts/brand-font-400.woff2" as="font" type="font/woff2" crossorigin>
   ```
4. Block external font imports during CSS compilation:
   ```python
   # In build_css.py
   imports = re.findall(r'@import\s+url\([\'"]?([^\'"\)]+)[\'"]?\);', content)
   for imp in imports:
       if imp.startswith('http'):
           raise ValueError(f"Performance violation: External font '{imp}' forbidden. Self-host local .woff2.")
   ```

### 2. Critical CSS Inlining & Synchronous Page Compilation
- Inline critical above-the-fold layout styles directly into `<style id="critical-css">` in the HTML document.
- Compile modular SMACSS page stylesheets synchronously (e.g. `template-[slug].compiled.css`) to prevent FOUC when navigating between views.

---

## 🖼️ Phase 3: Media Stability & Core Web Vitals (CLS & INP)

Cumulative Layout Shift occurs when media loads without reserved dimensions, pushing surrounding DOM nodes downward.

### 1. Strict Dimension Reservation
Never output an `<img>` or `<video>` without intrinsic dimensions:
```html
<!-- Correct: Explicit dimensions and aspect ratio reserved -->
<img 
  src="/assets/images/hero.webp" 
  alt="Studio Production Lighting" 
  width="1200" 
  height="630" 
  loading="eager" 
  fetchpriority="high"
  decoding="async"
  style="aspect-ratio: 1200 / 630; width: 100%; height: auto;"
>

<!-- Below-the-fold image: lazy loaded -->
<img 
  src="/assets/images/portfolio-01.webp" 
  alt="Commercial product campaign" 
  width="800" 
  height="600" 
  loading="lazy" 
  decoding="async"
  style="aspect-ratio: 800 / 600; width: 100%; height: auto;"
>
```

### 2. Modern Media Delivery
- Serve modern WebP or AVIF formats with compressed raster fallbacks.
- Use responsive `<picture>` tags with `srcset` for varied device densities.

---

## 👥 Phase 4: Multi-Persona Audit & Sign-Off Matrix

When auditing SEO and performance, deploy specialized personas to review each angle:

| Persona | Role | Verification Responsibility |
|---|---|---|
| **🌿 Eleanor** | Brand & Human Experience | Audits all meta titles, descriptions, and FAQs to guarantee authentic, human prose without keyword stuffing, robotic corporate jargon, or false urgency. |
| **⚡ Chloe** | CRO & Digital Marketing | Optimizes SERP CTR (click-through rates), OpenGraph social sharing preview cards, and high-impact FAQ rich snippet coverage. |
| **🛠️ Sally** | UX & Performance Systems | Verifies zero-FOUC rendering, preloads critical `.woff2` fonts, inspects CSS compilation, and eliminates layout shifts (CLS < 0.1). |
| **⚙️ Forge** | Core Systems Engineer | Validates the staging environment guard, Schema.org `@graph` syntax, CSS compilation freshness, and pre-release audit pass. |

---

## 🧪 Phase 5: Automated Pre-Release Verification

Run the automated auditor before merging or deploying:

```bash
# From project root
python3 scripts/audit_production_readiness.py --path .
```

The script verifies:
1. `✔` Non-production / staging `noindex` guard is present and correctly prioritized.
2. `✔` Zero external font CDN calls or unapproved `@import` statements.
3. `✔` All declared `@font-face` fonts exist as local `.woff2` assets.
4. `✔` Schema.org `@graph` JSON-LD is syntactically valid with required entity nodes.
5. `✔` All `<img>` tags have explicit `width`, `height`, and `alt` attributes.
