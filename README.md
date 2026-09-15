# Meaicon Website

This repository contains the static marketing website for Meaicon. The source remains plain HTML, CSS, and JavaScript, with Eleventy providing an optional static build layer for shared layouts and future content collections.

## Overview

- Static site with multi-page HTML structure
- Eleventy generates static output without a server-side runtime
- Designed for fast hosting on GitHub Pages, Netlify, Vercel, or any static host
- Assets are stored in the `assets/` folder, including branding, CSS, and JavaScript

## Branch and release status

- Active branch: `website-redesign`
- Tracking remote: `origin/website-redesign`
- Latest verified commit: pending — light enterprise redesign and contrast audit
- This is a long-lived redesign branch. Continue landing visual, content, accessibility, and SEO improvements here before merging into `main`.
- Keep `main` unchanged while the redesign is reviewed and iterated. Merge only after the branch has passed the final content, accessibility, performance, and deployment review.

## Project structure

```text
/workspaces/meaicon-website
├── index.html
├── about.html
├── solutions.html
├── industries.html
├── global-connectivity.html
├── partners.html
├── case-studies.html
├── contact.html
├── products.html
├── robots.txt
├── sitemap.xml
├── favicon.ico
├── favicon.svg
├── apple-touch-icon.png
├── README.md
├── assets/
│   ├── css/
│   ├── js/
│   ├── images/
│   └── brand/
│       └── meaicon/
└── .gitignore
```

## Quick start

Install dependencies and build the static output:

```bash
cd /workspaces/meaicon-website
npm install
npm run build
```

The generated site is written to `_site/`. To preview it with live reload:

```text
npm start
```

The existing root HTML pages remain the content source during the incremental migration. The homepage and the 10 primary interior pages are generated through Nunjucks entry templates in `index.njk` and `migrated/`, using shared files in `_includes/`. Their legacy files provide the current `<main>` content until structured content collections are introduced. `products.html` remains a standalone noindex redirect page.

The current shared visual system is the **Elite Enterprise Trust** theme: Plus Jakarta Sans headings, Inter body copy, an ice-white surface, Executive Midnight Blue text and sections, Electric Indigo accents, thin slate borders, restrained shadows, glassmorphic light navigation, telemetry widgets, and responsive bento-grid solution cards. Legacy midnight-blue sections include shared high-contrast text rules so headings and supporting copy remain readable across the interior pages.

## Update the repo from a zip

If you have a new site zip and want to replace the repo content in one fast step, run:

```bash
cd /workspaces/meaicon-website && \
rm -rf /tmp/meaicon-update && \
mkdir -p /tmp/meaicon-update && \
unzip -o "/path/to/your-site.zip" -d /tmp/meaicon-update && \
rsync -a --delete /tmp/meaicon-update/ ./
```

This updates the whole repository and removes old files that are no longer in the new package.

## Deployment

This site is intended for static hosting. Any of the following are suitable:

- GitHub Pages
- Netlify
- Vercel
- Any web host that supports static HTML files

Before deployment, verify that:

- all HTML pages load correctly
- all links resolve without 404s
- favicon and branding assets are present
- the site root renders correctly on desktop and mobile
- the hosting platform applies the `_headers` security policy

### IndexNow

The public verification key is available at `/7cc8503712a0c79742073c805efa675e.txt`. After deploying a metadata or content update, submit changed URLs to `https://api.indexnow.org/indexnow` with this key and the matching host. IndexNow requests discovery; search engines still decide whether and when to crawl or index a URL.

### SEO crawler MCP

VS Code is configured to start `@houtini/seo-crawler-mcp@2.1.5` on demand through `.vscode/mcp.json`. Use its `run_seo_audit` tool against the deployed site after content or design changes, then use `analyze_seo` to inspect missing metadata, broken links, canonical issues, sitemap coverage, and other crawl findings. Reports are written to `.seo-audits/`, which is intentionally excluded from version control.

### Content and design toolkit

The workspace recommends extensions for live previews, HTML and CSS validation, JavaScript linting, consistent formatting, spelling and content QA, color inspection, image preview, and image compression. These recommendations are stored in `.vscode/extensions.json` so contributors can reproduce the same editing environment.

For a recurring maintenance pass:

1. Preview changed pages with Live Preview at desktop and mobile widths.
2. Run the SEO crawler against the deployed site and review its report.
3. Fix broken links, missing metadata, canonical or sitemap issues, and accessibility warnings.
4. Check copy with Code Spell Checker and format changed files with Prettier.
5. Compress newly added image assets and rerun the crawl after deployment.

## Branding and UI consistency

The public site follows a fixed brand language built around the Meaicon identity:

- ice-white background: `#FAFBFC`
- Executive Midnight Blue text and dark sections: `#0A192F`
- Electric Indigo accent: `#4F46E5`
- slate border tone: `#E2E8F0`
- Plus Jakarta Sans headings with Inter body copy
- buttons use sharp or lightly rounded corporate corners, never pill styling
- hover transitions use restrained `0.2s ease-in-out` motion without neon glow effects

The cookie consent banner and modal were aligned to this system so they match the rest of the site instead of using a generic dark-template look. Recent refinements increased the luxury feel with more generous spacing, an enterprise-style legal tone, and a subtle gold brand accent line across the consent surfaces.

## Social Media Integration

All pages include professional social media profiles optimized for SEO and brand visibility:

### Social Profiles
- **LinkedIn**: https://www.linkedin.com/company/meaicon/
- **X (Twitter)**: https://x.com/meaicon
- **Instagram**: https://www.instagram.com/meaicon.official/
- **Facebook**: https://www.facebook.com/Meaicon.Official
- **YouTube**: https://www.youtube.com/channel/UCVbuZOFqHeFGAMmzu3jE3oA

### Implementation Details

#### Footer Social Icons
- Professional SVG icons for all 5 social media platforms
- Responsive grid layout with hover effects (accent color transition)
- Proper accessibility with `aria-label` attributes and semantic `rel="me"` links
- Consistent styling across all 11 indexable website pages

#### JSON-LD Schema Markup
- Added `sameAs` property to Organization schema on every page
- Improves search engine entity recognition and knowledge graph linking
- Enhances presence in social media search results
- Optimizes for improved SEO visibility across platforms

#### Coverage
- **Pages updated**: 10 (index.html, about.html, solutions.html, case-studies.html, contact.html, global-connectivity.html, industries.html, partners.html, privacy-policy.html, terms-of-service.html)
- **Total social profile coverage**: 11 indexable pages × 5 platforms
- **Each page includes**: 2 Instagram references, 2 Facebook references, 2 YouTube references, plus all profiles in JSON-LD schema

## Current improvement backlog

The migration branch is stable, but remains open for ongoing improvement. The initial visual redesign and contrast pass are complete; the following work remains intentionally open before merging back into `main`.

1. [ ] Convert the remaining legacy page bodies into structured, page-specific Nunjucks content blocks instead of raw HTML extraction.
2. [x] Rewrite the homepage to emphasize customer outcomes, proof points, and clear conversion intent.
3. [x] Standardize the shared landing-page cards, CTAs, spacing, typography, and contrast treatment.
4. [ ] Complete the page-by-page content rewrite for service, industry, regional, and company pages.
5. [ ] Run the final SEO crawler, accessibility, performance, responsive, and deployment review before merging into `main`.

## Flexible content pipeline for future pages

The redesign branch is prepared for scalable content onboarding without a fixed page-count target. The workflow is intentionally simple:

1. Add any planned page entries to `data/site-content.json` under `futurePages` when the content is ready.
2. Run `npm run generate:pages` to generate the matching Nunjucks templates in `migrated/generated/`.
3. Replace the scaffold with final brand-specific copy and production-ready page layout.
4. Run `npm run validate:content` and `npm run build` before publishing.

This keeps the site scalable without forcing placeholder pages or an arbitrary page limit.

## Recent progress

### Social Media & SEO Optimization (August 2026)
- **Social Profile Integration**: Added professional social media links to all 11 indexable website pages
  - Footer social icons with responsive design and hover effects
  - JSON-LD schema markup with `sameAs` property for 5 social platforms
  - Proper accessibility attributes (aria-labels, rel="me") for improved SEO
- **Social Profiles Configured**:
  - LinkedIn Company Page: https://www.linkedin.com/company/meaicon/
  - X (Twitter): https://x.com/meaicon
  - Instagram Official: https://www.instagram.com/meaicon.official/
  - Facebook Page: https://www.facebook.com/Meaicon.Official
  - YouTube Channel: https://www.youtube.com/channel/UCVbuZOFqHeFGAMmzu3jE3oA
- **SEO Benefits**: Schema.org integration improves entity recognition, knowledge graph linking, and cross-platform visibility

### Infrastructure & Compliance
- Updated repo with refreshed site content from the new zip package
- Replaced placeholder brand references with official Meaicon brand assets
- Normalized homepage and footer logo variants for consistent visual identity
- Added legal policy pages for privacy and terms references in the consent flow
- Improved cookie consent styling to match the corporate brand system
- Refined the consent prompt to read more like a premium enterprise compliance banner
- Verified the consent logic remains centralized and site-wide consistent

### Audit & Fixes
- Ran a full static-site audit and fixed invalid markup placement, sitemap/robots domain alignment, and site asset references
- Confirmed all core pages and critical assets return successful HTTP responses

### Premium Branding & Marketing Polish
- Refined the homepage hero, CTA hierarchy, and trust messaging for a more premium enterprise marketing feel
- Added a proof-led trust strip to reinforce credibility and conversion intent
- Completed premium editorial redesign of the global-connectivity (regional presence) page with enhanced storytelling and visual hierarchy
- Applied the same premium editorial polish across the remaining key pages:
  - **about.html**: Stronger mission/vision positioning and regional footprint narrative
  - **industries.html**: Enhanced value prop around mission-critical infrastructure; clearer sector differentiation
  - **partners.html**: Refined vendor-neutral positioning and ecosystem narrative
  - **case-studies.html**: Improved proof-based credibility messaging and outcome metrics
  - **contact.html**: Elevated conversion tone with strategic, high-touch engagement framing
- Increased spacing and layout rhythm for a more luxury, enterprise-ready feel
- Strengthened CTA hierarchy and messaging for better lead-generation conversion
- All pages now carry a consistent, cohesive brand voice across the entire site

## Notes

- This repo is intentionally lightweight and easy to manage.
- Keep the site stateless and static unless a new build system is explicitly added.
- If you update structure or asset paths, keep this README current.
- Run Lighthouse or PageSpeed Insights checks periodically and address Core Web Vitals issues when they appear.

## License

Proprietary — All rights reserved by Meaicon LLC FZ, unless otherwise specified.
