# Meaicon Website Roadmap

This branch is the working branch for the professional website improvement programme. `main` remains the stable published baseline until the redesign is approved.

## Branch policy

- Keep `website-redesign` as the shared working branch during the redesign.
- Use short-lived branches only for isolated work that benefits from separate review, such as `content/homepage`, `design/navigation`, or `seo/structured-data`.
- Merge those small branches back into `website-redesign`, not directly into `main`.
- Merge `website-redesign` into `main` only after the complete acceptance checklist passes.
- Make small commits with clear messages so changes can be reviewed or reverted safely.

## Delivery phases

### Phase 1: Discovery and direction

- Confirm target audiences, services, markets, differentiators, and proof points.
- Define the brand voice, visual direction, page hierarchy, and conversion goals.
- Inventory existing content, images, claims, forms, legal copy, and analytics needs.

### Phase 2: Design system

- [x] Add the Eleventy static build layer without changing public URLs.
- [x] Move the shared head, navigation, footer, and cookie-consent shell into reusable templates.
- [x] Route the homepage and 10 primary interior pages through the shared layout.
- Establish shared typography, colors, spacing, buttons, navigation, footer, cards, forms, and responsive rules.
- Improve the experience at mobile, tablet, and desktop widths.
- Keep shared components visually consistent across every page.

### Phase 3: Content and page improvements

- [ ] Replace legacy `<main>` extraction with structured page content and reusable collections.
- Rewrite the homepage around a clear value proposition and qualified leads.
- Strengthen Solutions, Consulting, Industries, Partners, Case Studies, Presence, About, and Contact pages.
- Replace generic claims with specific outcomes, service details, markets, evidence, and calls to action.
- Keep Privacy Policy and Terms accurate and easy to find.

### Phase 4: Technical quality

- Maintain unique titles, descriptions, canonical URLs, headings, structured data, sitemap, and robots rules.
- Check accessibility, keyboard navigation, focus states, contrast, alt text, and reduced-motion behavior.
- Optimize images, loading performance, security headers, forms, links, and mobile layout stability.

### Phase 5: Review and launch

- Run the SEO crawler and repository audit.
- Review every page on mobile and desktop.
- Test navigation, forms, external links, cookies, metadata, and redirects.
- Review copy and visual direction with stakeholders.
- Create a release candidate, deploy it for final review, then merge into `main`.

## Definition of done

- The site communicates what Meaicon does within the first viewport.
- Every important page has a clear audience, purpose, proof, and next action.
- The design is consistent, responsive, accessible, and recognizably Meaicon.
- No broken local links, missing assets, console errors, or metadata conflicts remain.
- SEO, security, performance, and sitemap checks pass.
- Final content and claims have stakeholder approval.
