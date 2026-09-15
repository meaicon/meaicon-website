# Meaicon Website

This repository contains the static marketing website for Meaicon. The source remains plain HTML, CSS, and JavaScript, with Eleventy providing an optional static build layer for shared layouts and future content collections.

## Overview

- Static site with multi-page HTML structure
- Eleventy generates static output without a server-side runtime
- Designed for fast hosting on GitHub Pages, Netlify, Vercel, or any static host
- Assets are stored in the `assets/` folder, including branding, CSS, and JavaScript

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

The existing root HTML pages remain the source of truth during the incremental migration, except for the homepage, which is now generated from `index.njk` using the shared files in `_includes/`. Shared layouts and content collections will move into Eleventy templates in later phases.

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

- warm paper background: `#F6F3EC`
- dark ink text: `#23241F`
- accent gold: `#C1873D`
- border tone: `#E2DDCF`
- button and heading typography remain consistent with the existing design system

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
