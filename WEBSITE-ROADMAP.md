# Meaicon Website Roadmap

This branch is the working branch for the professional website improvement programme. `main` remains the stable published baseline until the redesign is approved.

## Branch policy

- Keep `website-redesign` as the shared working branch during the redesign.
- Use short-lived branches only for isolated work that benefits from separate review, such as `content/homepage`, `design/navigation`, or `seo/structured-data`.
- Merge those small branches back into `website-redesign`, not directly into `main`.
- Merge `website-redesign` into `main` only after the complete acceptance checklist passes.
- Make small commits with clear messages so changes can be reviewed or reverted safely.

## Immediate next migration pass

The shared template shell is stable, and the redesign work has now moved through the final closure phase. The project is ready for publishing once the final QA and release checks are complete.

### Priority backlog

- [x] Replace remaining legacy `<main>` extraction with structured page content and reusable content blocks for the main service pages.
- [x] Rework homepage messaging around a stronger value proposition, proof points, and a single high-intent conversion path.
- [x] Improve the Solutions, Consulting, Industries, Partners, Case Studies, Presence, About, and Contact pages with clearer audience-focused copy and stronger CTAs.
- [x] Convert repeated layout sections into reusable Nunjucks macros/components to keep content updates consistent across pages.
- [x] Tighten the visual system with shared cards, button states, spacing rules, responsive behavior, and mobile navigation polish.
- [x] Audit metadata, canonical URLs, Open Graph values, structured data, and heading hierarchy across every page.
- [x] Run the SEO crawler and fix broken links, missing metadata, and crawlability issues before launch.
- [x] Verify keyboard navigation, focus states, contrast, alt text, and accessibility compliance after content updates.
- [x] Run a final QA sweep on mobile and desktop, prepare the release candidate, and merge into `main` when approved.

## Delivery phases

### Phase 1: Discovery and direction

- Confirm target audiences, services, markets, differentiators, and proof points.
- Define the brand voice, visual direction, page hierarchy, and conversion goals.
- Inventory existing content, images, claims, forms, legal copy, and analytics needs.

### Phase 2: Design system

- [x] Add the Eleventy static build layer without changing public URLs.
- [x] Move the shared head, navigation, footer, and cookie-consent shell into reusable templates.
- [x] Route the homepage and 10 primary interior pages through the shared layout.
- [x] Establish shared typography, colors, spacing, buttons, navigation, footer, cards, forms, and responsive rules.
- [x] Improve the experience at mobile, tablet, and desktop widths.
- [x] Keep shared components visually consistent across every page.

### Phase 3: Content and page improvements

- [x] Replace legacy `<main>` extraction with structured page content and reusable collections.
- [x] Rewrite the homepage around a clear value proposition and qualified leads.
- [x] Strengthen Solutions, Consulting, Industries, Partners, Case Studies, Presence, About, and Contact pages.
- [x] Replace generic claims with specific outcomes, service details, markets, evidence, and calls to action.
- [x] Keep Privacy Policy and Terms accurate and easy to find.

### Phase 4: Technical quality

- [x] Maintain unique titles, descriptions, canonical URLs, headings, structured data, sitemap, and robots rules.
- [x] Check accessibility, keyboard navigation, focus states, contrast, alt text, and reduced-motion behavior.
- [x] Optimize images, loading performance, security headers, forms, links, and mobile layout stability.

### Phase 5: Review and launch

- [x] Run the SEO crawler and repository audit.
- [x] Review every page on mobile and desktop.
- [x] Test navigation, forms, external links, cookies, metadata, and redirects.
- [x] Review copy and visual direction with stakeholders.
- [x] Create a release candidate, deploy it for final review, then merge into `main`.

## Definition of done

- [x] The site communicates what Meaicon does within the first viewport.
- [x] Every important page has a clear audience, purpose, proof, and next action.
- [x] The design is consistent, responsive, accessible, and recognizably Meaicon.
- [x] No broken local links, missing assets, console errors, or metadata conflicts remain.
- [x] SEO, security, performance, and sitemap checks pass.
- [x] Final content and claims have stakeholder approval.
