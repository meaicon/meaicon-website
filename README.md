# Meaicon Website

This repository contains the static marketing website for Meaicon. The project is built with plain HTML, CSS, and JavaScript, and does not require a build step.

## Overview

- Static site with multi-page HTML structure
- No framework dependency required
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

Open the site directly in a browser, or run a local static server:

```bash
cd /workspaces/meaicon-website
python3 -m http.server 8000
```

Then open:

```text
http://localhost:8000
```

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

## Branding and UI consistency

The public site follows a fixed brand language built around the Meaicon identity:

- warm paper background: `#F6F3EC`
- dark ink text: `#23241F`
- accent gold: `#C1873D`
- border tone: `#E2DDCF`
- button and heading typography remain consistent with the existing design system

The cookie consent banner and modal were aligned to this system so they match the rest of the site instead of using a generic dark-template look. Recent refinements increased the luxury feel with more generous spacing, an enterprise-style legal tone, and a subtle gold brand accent line across the consent surfaces.

## Recent progress

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

Proprietary — All rights reserved by Meaicon / Triqbit, unless otherwise specified.
