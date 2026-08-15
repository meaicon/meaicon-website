# Meaicon Website

Official static website for **Meaicon**. This repository contains the full source for the corporate/marketing site — plain HTML, CSS (Tailwind), and vanilla JavaScript, with no build step required to view pages locally.

## Table of Contents

- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Folder Structure](#folder-structure)
- [Getting Started](#getting-started)
- [Coding Standards](#coding-standards)
- [SEO & Corporate Website Standards](#seo--corporate-website-standards)
- [Branching & Commit Conventions](#branching--commit-conventions)
- [Deployment](#deployment)
- [Guidelines for AI Agents](#guidelines-for-ai-agents)
- [Pre-Commit / Pre-Merge Checklist](#pre-commit--pre-merge-checklist)
- [Roadmap / TODO](#roadmap--todo)
- [License](#license)

## Project Overview

This is a **static HTML website** (no framework, no server-side rendering). Pages are plain `.html` files linked together via relative paths, styled with Tailwind CSS, and enhanced with minimal vanilla JS where necessary. The goal is a fast, dependency-free, easily maintainable, and **SEO-optimized corporate website** that meets professional industry standards at all times.

## Tech Stack

| Layer      | Technology                                      |
|------------|--------------------------------------------------|
| Markup     | HTML5 (semantic)                                  |
| Styling    | Tailwind CSS (currently via CDN script — see Roadmap for production build) |
| Fonts      | Space Grotesk (display), Inter (body), IBM Plex Mono (mono/labels) |
| Scripting  | Vanilla JavaScript (ES6+)                         |
| Structured Data | JSON-LD (schema.org/Organization) on index.html |
| Hosting    | Static hosting (GitHub Pages / Netlify / Vercel — TBD) |
| Build Tool | None currently required (pure static files)       |

If a bundler or CSS build pipeline is introduced later (recommended for production — see Roadmap), this section must be updated accordingly.

## Folder Structure

meaicon-website/
├── index.html                # Homepage
├── about.html                # About page (mission, vision, values)
├── solutions.html            # Solutions overview (5 disciplines)
├── industries.html           # Industries served
├── global-connectivity.html  # Presence / regional footprint (7 MEA markets)
├── partners.html             # Partners page
├── case-studies.html         # Case studies / selected work
├── contact.html              # Contact page (embedded form + map)
├── products.html             # Legacy redirect stub -> solutions.html (noindex, canonical set)
├── assets/
│   ├── css/                  # Shared stylesheets (currently placeholder; Tailwind is CDN-based, see Roadmap)
│   ├── js/                   # Shared vanilla JS files (currently placeholder; inline scripts still in use)
│   └── images/               # Shared images/media (currently placeholder)
├── README.md                 # This file
└── .gitignore

Note: /assets/css/, /assets/js/, and /assets/images/ now exist for shared static assets. New shared stylesheets, scripts, and media should be added there instead of inline per-page, to keep the site maintainable as it grows. Update this section immediately if the structure changes again.

## Getting Started

1. Clone the repository:
   git clone https://github.com/triqbit/meaicon-website.git
   cd meaicon-website

2. Open index.html directly in a browser, or serve locally for accurate relative-path behavior:
   npx serve .
   # or
   python3 -m http.server 8080

3. Visit http://localhost:8080 (or the port shown).

No dependencies, no npm install required for the core site.

## Coding Standards

- HTML: Semantic HTML5 elements (header, nav, main, section, article, footer). Every page must have proper title, meta charset, meta viewport, and meta description tags.
- CSS: Follow the existing Tailwind utility-class approach and the established design tokens (paper, card, ink, muted, accent, teal, line, dark). Do not introduce a second color system or naming convention.
- JavaScript: Vanilla ES6+, no inline onclick handlers. Keep scripts unobtrusive, placed at the end of body.
- Accessibility: All images require descriptive alt text. Maintain proper heading hierarchy (h1 -> h2 -> h3, one h1 per page). Ensure sufficient color contrast and full keyboard navigability. Respect prefers-reduced-motion for animations.
- Performance: Optimize/compress images before committing (WebP/AVIF preferred). Avoid unused CSS/JS. Do not block rendering with synchronous scripts.
- Responsiveness: Mobile-first CSS. Test at common breakpoints (360px, 768px, 1024px, 1440px). Verify the mobile menu toggle works on every page that includes it.
- Consistency: Reuse existing header/footer/nav markup exactly across all pages before creating new variants. Do not duplicate design patterns already defined elsewhere.

## SEO & Corporate Website Standards

This section is mandatory and must be respected on every page, at all times, without exception. The website represents Meaicon's public corporate identity — it must always meet professional, industry-standard SEO and UX benchmarks, not just at launch but on every future edit.

### On-Page SEO (required on every page)
- Unique, descriptive title per page (50-60 characters), following the pattern "Page Topic — Meaicon" or "Meaicon — Value Proposition".
- Unique meta description per page (140-160 characters), written for humans first, keywords second.
- Exactly one h1 per page that matches page intent; logical h2/h3 hierarchy beneath it.
- link rel="canonical" on every page (including redirects/legacy stubs like products.html).
- Descriptive, keyword-relevant file names and internal link anchor text (avoid "click here").
- lang="en" (or correct locale) set on html.

### Structured Data
- Keep and maintain the Organization JSON-LD schema on index.html (name, url, address, contactPoint).
- Add BreadcrumbList schema on inner pages once site depth increases.
- Add Service/Product schema on solutions.html describing each of the five disciplines.
- Validate all structured data with Google's Rich Results Test before merging.

### Social & Sharing
- Every page must include Open Graph tags: og:title, og:description, og:type, og:url, and og:image (currently missing og:image — must be added, 1200x630px recommended).
- Include twitter:card, twitter:title, twitter:description, twitter:image.

### Technical SEO
- Add a sitemap.xml at the repo root listing all indexable pages, and reference it in robots.txt.
- Add a robots.txt at the repo root; disallow legacy/duplicate stubs (e.g. products.html) via noindex and keep it consistent with the sitemap.
- Ensure only one canonical version of any duplicate content exists — products.html must always redirect/canonicalize to solutions.html and never be indexed.
- Add a real favicon.ico / favicon.svg and apple-touch-icon (currently using a data URI placeholder — replace with a proper brand favicon).
- Replace the Tailwind CDN script with a compiled/purged production stylesheet to eliminate render-blocking JS and improve Core Web Vitals (LCP/CLS/INP).
- Self-host or preload critical fonts where possible to reduce third-party font-loading delay.
- Ensure all internal links use relative paths and resolve correctly with no 404s.
- Target Core Web Vitals: LCP < 2.5s, CLS < 0.1, INP < 200ms on mobile.

### Corporate Website Standards
- Consistency: Identical header, navigation, and footer markup/content across all pages (verify after every content change).
- Trust signals: Company legal name, registered address, phone, and email must appear in the footer on every page.
- Contact & CTAs: Every page should offer a clear path to contact.html ("Talk to an expert" or equivalent).
- Legal: Add privacy-policy.html and terms-of-service.html before public launch; link them in the footer. A corporate site must never launch without these.
- 404 page: Add a custom 404.html with navigation back into the site.
- Analytics & consent: Before adding any analytics/tracking script, add a cookie-consent mechanism appropriate for the target markets (UAE, KSA, Qatar, Oman, Egypt, Kenya, Pakistan, EU visitors if applicable).
- Accessibility compliance: Target WCAG 2.1 AA as the minimum bar for a professional corporate site.
- Content accuracy: Statistics, uptime SLAs, and market claims (e.g. "99.95% uptime", "7 countries") must be kept accurate and updated when business facts change — never leave stale claims live.

## Branching & Commit Conventions

- main — production-ready branch, always deployable.
- Feature branches: feature/<short-description>
- Fixes: fix/<short-description>
- Commits should follow Conventional Commits (https://www.conventionalcommits.org/):
  - feat: add new pricing section
  - fix: correct broken nav link on mobile
  - style: adjust footer spacing
  - docs: update README structure
  - refactor: simplify hero section markup
  - seo: add missing meta description to industries page

## Deployment

- The site is static and can be deployed to GitHub Pages, Netlify, Vercel, or any static host.
- Do not commit build artifacts unless a build step is formally introduced and documented here.
- Confirm all relative paths (href, src) resolve correctly relative to the deployed root before merging to main.
- Re-run the Pre-Commit / Pre-Merge Checklist before every deploy.

## Guidelines for AI Agents

This section exists so that any AI coding agent (e.g. Google Jules, Copilot, Claude, etc.) can work on this repo efficiently, consistently, and with minimal back-and-forth correction.

1. Read this README first, especially the SEO & Corporate Website Standards section, before making any change. Do not assume framework usage — this is plain HTML/Tailwind/vanilla JS unless explicitly stated otherwise above.
2. Preserve existing structure. Do not introduce a new folder layout, CSS framework, or JS library without explicit instruction.
3. Match existing patterns. Reuse the existing header/nav/footer markup, Tailwind design tokens, and section patterns before creating new components.
4. Never regress SEO. Any new or edited page must retain/add: unique title, meta description, canonical tag, Open Graph tags, and correct heading hierarchy.
5. No unrequested dependencies. Do not add npm packages, CDNs, or build tools unless the task explicitly asks for it.
6. Small, scoped changes. Prefer minimal diffs that solve the stated task rather than broad refactors, unless refactoring is the explicit task.
7. Update this README whenever the folder structure, tech stack, or conventions change, so future agents/humans stay in sync.
8. Validate before committing: HTML validates (no unclosed tags, correct nesting); links are not broken; pages render correctly at mobile and desktop widths; SEO checklist items are intact.
9. Commit messages must follow the Conventional Commits format described above.
10. Never remove content (copy, sections, images) without explicit instruction — flag it instead of deleting.
11. Ask/flag ambiguity in a PR description or comment rather than guessing silently when requirements are unclear.

## Pre-Commit / Pre-Merge Checklist

Run through this list before every commit or pull request merge:

- [ ] Every page has a unique `<title>` and `<meta name="description">`
- [ ] Every page has a `>` pointing to its correct URL
- [ ] Every page has Open Graph tags (title, description, type, url, image)
- [ ] Exactly one `<h1>` per page; heading hierarchy is logical
- [ ] All images have descriptive `alt` text
- [ ] All internal links resolve correctly (no 404s)
- [ ] Header, nav, and footer markup is identical/consistent across all pages
- [ ] Mobile menu toggle works on every page
- [ ] Page renders correctly at 360px, 768px, 1024px, and 1440px widths
- [ ] No inline styles or `onclick` handlers introduced
- [ ] No new dependencies, CDNs, or build tools added without explicit approval
- [ ] Commit message follows Conventional Commits format
- [ ] README updated if structure, stack, or conventions changed

## Roadmap / TODO

- [x] Add `sitemap.xml` and `robots.txt`
- [x] Add real favicon (`favicon.ico`, `favicon.svg`) and `apple-touch-icon` (replace data URI placeholder) — done for all 10 pages
- [x] Add `og:image` and `twitter:image`/`twitter:title`/`twitter:description` to all pages; add `link rel="canonical"` to all pages
- [ ] Replace Tailwind CDN script with compiled/purged production CSS
- [ ] Self-host or preload critical fonts
- [ ] Add `privacy-policy.html` and `terms-of-service.html`
- [ ] Add custom `404.html`
- [ ] Add cookie-consent mechanism before enabling analytics
- [ ] Add `BreadcrumbList` and `Service` schema (JSON-LD) to inner pages
- [ ] Set up GitHub Pages / hosting deployment
- [ ] Add basic HTML/CSS linting (e.g. Prettier, Stylelint) if project grows
- [ ] Run a full accessibility audit (WCAG 2.1 AA)
- [ ] Run Lighthouse/PageSpeed Insights audit and address Core Web Vitals issues

## License

Proprietary — All rights reserved by Meaicon / Triqbit, unless otherwise specified.
