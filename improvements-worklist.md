# MEAICON Website Improvements Worklist

## Executive Summary
Overall Site Health Score: 6.5/10. The transition from legacy static files to Eleventy is in progress, but the codebase suffers from significant technical debt inherited from the legacy structure.

### Top 5 Critical Issues:
1. **Performance**: Reliance on Tailwind CDN vs. local build pipeline.
2. **Maintenance**: `_includes/site-head.njk` (860 lines) is unsustainable; needs componentization.
3. **Design Consistency**: Potential remnants of old accent color (#C1873D) need eradication in favor of #0066FF.
4. **Optimization**: Lack of automated image resizing/optimization plugins.
5. **Technical Debt**: Excessive use of "legacy" filters in `.eleventy.js` to parse old HTML files.

---

## By Profile

### meaicon-research (Research Agent)
- [ ] Crawl all pages to map remaining hardcoded legacy links.
- [ ] Conduct competitor analysis: Compare our new hero sections against top 3 competitors in UAE IT infra space.
- [ ] Source content for new case study pages based on current site data.

### meaicon-content (Content Agent)
- [ ] Audit meta descriptions for all pages; ensure all meet SEO length and keyword requirements.
- [ ] Standardize brand voice: Review all text against the Design Guidelines (docs/design-guideline.md).
- [ ] Create missing OG/Twitter images for social sharing.

### meaicon-dev (Dev Agent)
- [ ] Migrate Tailwind from CDN to local PostCSS compilation.
- [ ] Refactor `_includes/site-head.njk` into modular partials (e.g., `_includes/components/button.njk`, `_includes/layout/head.njk`).
- [ ] Replace all hardcoded colors in CSS with CSS variables linked to the design guidelines.
- [ ] Implement `eleventy-img` plugin for automated image optimization.
- [ ] Clean up `.eleventy.js` and remove legacy filters once pages are fully converted.

### meaicon-qa (QA Agent)
- [ ] Accessibility: Run axe-core audit on all template pages.
- [ ] SEO: Verify JSON-LD implementation on all service pages.
- [ ] Visual Regression: Perform cross-browser testing for the new mega-menu.
- [ ] Performance: Establish Lighthouse budget performance thresholds.

---

## Priority Matrix

| ID | Profile | Task | Priority | Effort | Dependencies |
|----|---------|------|----------|--------|--------------|
| 1  | Dev     | Local Tailwind Build | P0 | M | - |
| 2  | Dev     | Refactor site-head.njk | P1 | L | - |
| 3  | QA      | Accessibility Audit | P1 | S | - |
| 4  | Content | SEO Meta Audit | P1 | M | - |
| 5  | Dev     | Image Optimization | P2 | S | - |
| 6  | Research| Competitor Analysis | P2 | M | - |
| 7  | Dev     | CSS Variable Cleanup | P2 | M | Refactor |
| 8  | Content | Brand Voice Review | P3 | M | - |
| 9  | QA      | Perf Threshold Setup | P3 | S | - |
| 10 | QA      | Mega-menu QA | P3 | S | - |

---

## Quick Wins (Top 10)
1. **Remove unused CSS**: Audit `site-head.njk` for dead rules.
2. **Fix Alt Text**: Audit images on index page.
3. **Standardize H1s**: Verify single H1 per page across all 80 pages.
4. **Enable `eleventy-img`**: Low effort, huge perf impact.
5. **Add Skip-to-content**: Simple CSS/HTML fix.
6. **Canonical URLs**: Ensure all pages have proper canonical meta tags.
7. **Robots.txt**: Validate coverage of all directories.
8. **Favicon Audit**: Ensure standard sizes are served.
9. **Form Labels**: Ensure all forms have associated `<label>` tags.
10. **Heading Hierarchy**: Enforce consistent H2/H3 use in `content/`.
