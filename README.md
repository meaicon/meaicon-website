# MEAICON Website

Static marketing website for MEAICON LLC FZ — a digital infrastructure company headquartered in Dubai, serving enterprises and governments across the Middle East &amp; Africa.

## Overview

- **72-page** corporate website built with Eleventy 3.1.6 and Nunjucks templates
- Original MEAICON content — connectivity, data centre, cybersecurity, blockchain, cloud, managed services, consulting
- 12 industry vertical pages, 8 insight articles, 8 case studies, company pages, legal pages
- Design system: Plus Jakarta Sans + Inter typography, custom CSS token system, Tailwind utility layer
- Production-ready: SEO-complete, accessible, semantic HTML5

## Tech Stack

| Layer | Technology |
|-------|-----------|
| SSG | Eleventy 3.1.6 |
| Templating | Nunjucks |
| Styling | Custom CSS design system + Tailwind CDN |
| Fonts | Google Fonts (Plus Jakarta Sans, Inter) |
| Build output | Static HTML/CSS/JS |

## Project Structure

```text
meaicon-website/
├── .eleventy.js              # Eleventy config — ignores migrated/ and root *.html
├── index.njk                 # Homepage
├── package.json              # npm scripts: build, validate, audit
├── _includes/
│   ├── layout.njk            # Base layout (head + header + main + footer)
│   ├── site-head.njk         # <head> — meta, OG, Twitter, JSON-LD, fonts, CSS
│   ├── header.njk            # Sticky nav with dropdown menus + mobile menu
│   ├── footer.njk            # 4-column footer + social links + mobile script
│   └── home-main.html        # Homepage content sections
├── pages/
│   ├── about.njk
│   ├── leadership.njk
│   ├── careers.njk
│   ├── contact.njk
│   ├── methodology.njk
│   ├── why-meaicon.njk
│   ├── faq.njk
│   ├── partners.njk
│   ├── global-connectivity.njk
│   ├── privacy-policy.njk
│   ├── terms-of-service.njk
│   ├── solutions-index.njk
│   ├── industries-index.njk
│   ├── case-studies-index.njk
│   ├── solutions/            # 22 solution pages + 6 consulting sub-pages
│   │   ├── connectivity.njk
│   │   ├── data-centre.njk
│   │   ├── cyber-security.njk
│   │   ├── blockchain.njk
│   │   ├── consulting.njk     # Main consulting hub → 6 sub-pages below
│   │   ├── managed-services.njk
│   │   ├── cloud.njk
│   │   ├── network-security.njk
│   │   ├── identity-access.njk
│   │   ├── disaster-recovery.njk
│   │   ├── iot.njk
│   │   ├── consulting/        # 6 consulting sub-pages
│   │   │   ├── digital-transformation-strategy.njk
│   │   │   ├── infrastructure-network-audits.njk
│   │   │   ├── technology-roadmap-vendor-selection.njk
│   │   │   ├── regulatory-compliance-advisory.njk
│   │   │   ├── managed-services-outsourcing.njk
│   │   │   └── tokenisation-advisory.njk
│   │   ├── edge-compute-infrastructure.njk   # Edge & AI solutions
│   │   ├── edge-ai-inference.njk
│   │   ├── sovereign-compute.njk
│   │   ├── mobile-data-centre.njk
│   │   ├── secure-edge-computing.njk
│   │   ├── hardware-security.njk
│   │   ├── post-quantum-security.njk
│   │   ├── ota-fleet-management.njk
│   │   └── smart-building-edge.njk
│   ├── industries/           # 12 industry pages
│   │   ├── government.njk
│   │   ├── banking.njk
│   │   ├── healthcare.njk
│   │   ├── energy.njk
│   │   ├── telecom.njk
│   │   ├── hospitality.njk
│   │   ├── retail.njk
│   │   ├── logistics.njk
│   │   ├── education.njk
│   │   ├── real-estate.njk
│   │   ├── defence.njk
│   │   └── maritime.njk
│   ├── insights/             # 11 insight pages (8 articles + 3 indexes)
│   │   ├── index.njk         # → /insights.html
│   │   ├── digital-transformation-mea.njk
│   │   ├── cybersecurity-threat-landscape.njk
│   │   ├── blockchain-trade-finance.njk
│   │   ├── data-centre-trends.njk
│   │   ├── sd-wan-mea.njk
│   │   ├── cloud-migration-strategy.njk
│   │   ├── edge-ai-fleet-management.njk
│   │   ├── sovereign-compute-mea.njk
│   │   ├── whitepapers.njk
│   │   └── case-studies.njk
│   └── case-studies/         # 8 case study pages
│       ├── banking-blockchain.njk
│       ├── government-smart-city.njk
│       ├── healthcare-uptime.njk
│       ├── telecom-edge.njk
│       ├── energy-scada.njk
│       ├── retail-omnichannel.njk
│       ├── hospitality-guest-experience.njk
│       └── fleet-predictive-maintenance.njk
├── data/
│   └── site-content.json     # Brand metadata (name, address, contact, nav)
├── scripts/
│   ├── validate-content.js   # Validates page structure and frontmatter
│   └── audit-metadata.js     # Audits unique titles, descriptions, canonicals
├── assets/
│   ├── css/
│   ├── js/
│   ├── images/
│   └── brand/
│       └── meaicon/
├── content/
│   └── page-template.njk     # Reusable page template
├── migrated/                 # Legacy pages (ignored by Eleventy)
├── research-data/            # Crawled source data (pipeline input)
├── qa-reports/               # QA validation reports
├── sitemap.xml               # 52 URLs
├── robots.txt
├── _headers                  # Cloudflare Pages security headers
├── _redirects                # URL redirects
└── .gitignore
```

## Quick Start

```bash
npm install
npm run build
```

Output is written to `_site/`. Serve locally with:

```bash
npx @11ty/eleventy --serve
```

## npm Scripts

| Script | Purpose |
|--------|---------|
| `npm run build` | Build static site to `_site/` |
| `npm run start` | Local dev server with live reload |
| `npm run clean` | Remove `_site/` build directory |
| `npm run validate:content` | Validate frontmatter and page structure |
| `npm run audit:metadata` | Audit unique titles, descriptions, canonicals |
| `npm run lint` | Lint JS/CSS (if eslint configured) |
| `npm run format` | Format files with prettier (if configured) |
| `npm run audit` | Run npm security audit |

## SEO Compliance

- ✅ Unique `<title>` on every page (under 60 chars)
- ✅ Unique `<meta name="description">` on every page (under 160 chars)
- ✅ `<link rel="canonical">` on every page
- ✅ Open Graph tags (og:title, og:description, og:type, og:image, og:url)
- ✅ Twitter Card tags (summary_large_image)
- ✅ JSON-LD structured data (Organization schema on every page)
- ✅ `sitemap.xml` with all 52 URLs
- ✅ `robots.txt` with sitemap reference
- ✅ Semantic HTML5 (`<main>`, `<section>`, `<nav>`, `<header>`, `<footer>`, `<article>`)
- ✅ Single `<h1>` per page
- ✅ All `<img>` tags have `alt` attributes
- ✅ All internal links are relative
- ✅ No broken links (verified)

## Accessibility (WCAG AA)

- ✅ `lang="en"` on `<html>`
- ✅ `viewport` meta tag
- ✅ Skip-link ready navigation structure
- ✅ `aria-label` on icon-only links (social media)
- ✅ `aria-expanded` on mobile menu toggle
- ✅ `aria-hidden="true"` on decorative SVG icons
- ✅ `<button type="button">` on interactive controls
- ✅ `.sr-only` class for screen-reader text
- ✅ Color contrast meets WCAG AA (4.5:1 normal text, 3:1 large text)
- ✅ Cookie consent: 44px minimum touch targets (WCAG 2.5.5)
- ✅ Cookie consent: visible `:focus-visible` outlines (WCAG 2.4.7)
- ✅ Cookie consent: focus trap + Escape key in preferences modal (WCAG 2.4.3)
- ✅ Cookie consent: `prefers-reduced-motion` support (WCAG 2.3.3)
- ✅ Cookie consent: `prefers-color-scheme: dark` support

## Performance (Core Web Vitals)

- LCP < 2.5s — preload critical fonts, minimize render-blocking CSS
- CLS < 0.1 — reserve space for images/ads, avoid layout shifts
- INP < 200ms — defer non-critical JS, use `async` on analytics

### Resource Hints

The following `<link>` hints should be added to the `<head>` (via `site-head.njk`):

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://cdn.tailwindcss.com">
<link rel="dns-prefetch" href="https://www.googletagmanager.com">
```

### Tailwind CDN Performance Tradeoff

This site uses the **Tailwind CDN** (`https://cdn.tailwindcss.com`) for rapid prototyping.
The CDN injects a runtime script that parses the DOM and generates utility classes in the
browser — this has known tradeoffs:

| Factor | CDN (current) | Build-time Tailwind (recommended for production) |
|--------|---------------|--------------------------------------------------|
| Initial JS payload | ~400 KB runtime script | 0 — purged CSS only |
| Render blocking | Yes — script must execute before styles apply | No — CSS is static |
| LCP impact | Can delay LCP by 200-500ms | Minimal |
| CSP compatibility | Requires `script-src` for CDN | Fully self-hosted |
| Tree-shaking | None — all utilities shipped | Full purge of unused classes |

**Recommendation**: Migrate to build-time Tailwind (`tailwindcss` + `@tailwindcss/postcss`) before
production launch. This removes the runtime script, reduces CSP to `script-src 'self'`, and
improves LCP by ~200-500ms.

## Security Headers

All security headers are configured in `_headers` and deployed via Cloudflare Pages:

| Header | Value | Purpose |
|--------|-------|---------|
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains; preload` | Force HTTPS |
| `Content-Security-Policy` | `default-src 'self'; ...` | Restrict resource origins |
| `X-Frame-Options` | `DENY` | Prevent clickjacking |
| `X-Content-Type-Options` | `nosniff` | Prevent MIME sniffing |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | Limit referrer leakage |
| `Permissions-Policy` | `geolocation=(), microphone=(), camera=(), payment=(), browsing-topics=()` | Disable unused APIs |
| `Cross-Origin-Opener-Policy` | `same-origin` | Isolate browsing context |
| `Cross-Origin-Resource-Policy` | `same-origin` | Restrict cross-origin loads |

### Caching Strategy

- `/assets/*` — `Cache-Control: public, max-age=31536000, immutable` (1 year, never revalidate)
- `/*.html` — `Cache-Control: public, max-age=0, must-revalidate` (always check for updates)
- `/favicon.*` — `Cache-Control: public, max-age=604800` (7 days)

### CSP Inline Allowances

The CSP includes `'unsafe-inline'` for `script-src` and `style-src` because the site currently
uses the Tailwind CDN (which injects inline styles/scripts). When migrating to build-time
Tailwind, remove `'unsafe-inline'` from both directives for stricter security.

## Content Pipeline

```
User provides URLs → Research Agent crawls → Content Agent rebrands → Dev Agent builds → QA Agent validates → User reviews
```

- `research-data/` — crawled source data (input)
- `qa-reports/` — QA validation reports (output)
- `ORCHESTRATION-PLAN.md` — full pipeline documentation

## Branch & Deployment

- Active branch: `website-redesign`
- Main branch: untouched — merge only after final review
- Deploy: Cloudflare Pages (via `_headers`, `_redirects`)
- Build command: `npm run build`
- Output directory: `_site/`

## Browser Support

- Modern browsers (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)
- Graceful degradation for IE 11 (basic content, no Tailwind utilities)
- Mobile-first responsive design

## License

© 2026 MEAICON LLC FZ. All rights reserved.
