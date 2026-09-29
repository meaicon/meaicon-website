# MEAICON Website Content Audit Report

**Audit Date:** 2026-09-22
**Repository:** C:/Users/nev3s/repos/meaicon-website
**Branch:** website-redesign
**Total Pages Audited:** 80 (Nunjucks) + 1 standalone index.html
**Audit Type:** Read-only content verification (no source files modified)

## Executive Summary

| Metric | Value |
|--------|-------|
| Total Pages (Nunjucks) | 80 |
| Standalone HTML (index.html) | 1 |
| Complete Pages | 79 |
| Stub Pages | 1 |
| Placeholder Pages | 0 |
| Total Word Count (all pages) | 43,959 |
| Average Word Count per Page | 549.5 |
| Pages with Issues | 2 |
| Total Issues Found | 2 |
| **Content Health Score** | **98%** |
| Brand Issues | 0 |
| Duplicate Pages | 0 |
| Pages with Factual Claims | 1 |
| Pages Needing Rewrite | 5 |

### Architecture Notes

- **Page architecture:** Eleventy 3.x + Nunjucks templates. Each page has YAML front matter (layout, title, description, permalink) and an HTML body.
- **Meta tags:** All meta tags (description, OG tags, Twitter cards) are injected globally via `_includes/site-head.njk` using front matter `title` and `description` variables. Pages do not need inline meta tags.
- **JSON-LD:** Organization JSON-LD is in `site-head.njk`; BreadcrumbList JSON-LD is in `layout.njk`. All 80 pages inherit structured data from the layout — no per-page inline JSON-LD is required.
- **index.html:** Standalone HTML file (not Nunjucks). Has its own meta tags, OG tags, Twitter card, and JSON-LD directly inline.

## Homepage (index.html) Audit

| Attribute | Value |
|-----------|-------|
| Standalone HTML (not Nunjucks) | ✅ Yes |
| Nunjucks syntax present | ✅ No |
| Title | ✅ MEAICON — Digital Infrastructure Across MEA |
| Meta Description | ✅ MEAICON designs, deploys and operates the connectivity, data centre, security an |
| OG:title | ✅ |
| OG:description | ✅ |
| OG:image | ✅ |
| Twitter Card | ✅ |
| JSON-LD | ✅ |
| Hero Section | ✅ |
| CTA Buttons | ✅ |
| Images | ✅ |
| Word Count | 771 |
| H1 Count | 1 |
| H2 Count | 6 |
| Status | Complete |

✅ No issues found. Homepage is fully compliant.

## Shared Includes Audit

### _includes/site-head.njk

| Attribute | Value |
|-----------|-------|
| Provides meta description | ✅ |
| Provides OG:title | ✅ |
| Provides OG:description | ✅ |
| Provides OG:image | ✅ |
| Provides Twitter:card | ✅ |
| Provides JSON-LD (Organization) | ✅ |
| External/unrebranded refs | None |
| Placeholder content | TODO (1x) |

### _includes/layout.njk

| Attribute | Value |
|-----------|-------|
| Provides JSON-LD (BreadcrumbList) | ✅ |
| External/unrebranded refs | None |
| Placeholder content | None |

### _includes/header.njk

| Attribute | Value |
|-----------|-------|
| Word Count | 283 |
| Heading Count | 0 |
| External/unrebranded refs | None |
| Placeholder content | None |

**Navigation Structure (from header.njk):**

- **Solutions** (mega-menu): Connectivity, Data Centre, Cyber Security, Blockchain, Consulting, Cloud, Managed Services, Application Services, Digital Workplace, AI & Data Services, Edge Compute, Sovereign Compute, Identity & Access, Network Security, Disaster Recovery, Hardware Security, IoT, OTA Fleet Management, Edge AI Inference, Secure Edge Computing, Smart Building Edge, Mobile Data Centre, Post-Quantum Security, Critical Infrastructure Consulting
- **Industries** (mega-menu): Banking & Finance, Telecom Operators, Government & Smart Cities, Healthcare, Energy & Utilities, Defence & Military, Maritime, Logistics & Supply Chain, Hospitality, Retail & E-Commerce, Real Estate, Education
- **Insights**: Articles, Whitepapers, Case Studies
- **About**: About MEAICON, Methodology, Leadership, Partners, Careers, FAQ
- **Contact**: Talk to an Expert, Global Presence (Global Connectivity)

### _includes/footer.njk

| Attribute | Value |
|-----------|-------|
| Word Count | 103 |
| Heading Count | 5 |
| External/unrebranded refs | None |
| Placeholder content | None |

**Footer Content Verification:**

- ✅ Company name: **MEAICON LLC FZ** present
- ✅ Address: **Meydan Free Zone, Dubai, UAE** present
- ✅ Services listed: Connectivity, Data Centre, Cyber Security, Blockchain, Consulting
- ✅ Social links: LinkedIn (linkedin.com/company/meaicon), X (x.com/meaicon), Instagram (instagram.com/meaicon.official)
- ✅ Newsletter signup form present
- ✅ Footer navigation columns: Solutions, Security & Edge, Industries, Company, Legal

## Per-Section Breakdown

### root/ (15 pages)

| Metric | Value |
|--------|-------|
| Pages | 15 |
| Total Words | 4,565 |
| Average Words/Page | 304.3 |
| Complete | 14 |
| Stub | 1 |
| Placeholder | 0 |
| Issues | 2 |

### solutions/ (30 pages)

| Metric | Value |
|--------|-------|
| Pages | 30 |
| Total Words | 17,942 |
| Average Words/Page | 598.1 |
| Complete | 30 |
| Stub | 0 |
| Placeholder | 0 |
| Issues | 0 |

### industries/ (12 pages)

| Metric | Value |
|--------|-------|
| Pages | 12 |
| Total Words | 4,608 |
| Average Words/Page | 384.0 |
| Complete | 12 |
| Stub | 0 |
| Placeholder | 0 |
| Issues | 0 |

### insights/ (14 pages)

| Metric | Value |
|--------|-------|
| Pages | 14 |
| Total Words | 12,184 |
| Average Words/Page | 870.3 |
| Complete | 14 |
| Stub | 0 |
| Placeholder | 0 |
| Issues | 0 |

### case-studies/ (8 pages)

| Metric | Value |
|--------|-------|
| Pages | 8 |
| Total Words | 4,152 |
| Average Words/Page | 519.0 |
| Complete | 8 |
| Stub | 0 |
| Placeholder | 0 |
| Issues | 0 |

### about/ (1 pages)

| Metric | Value |
|--------|-------|
| Pages | 1 |
| Total Words | 508 |
| Average Words/Page | 508.0 |
| Complete | 1 |
| Stub | 0 |
| Placeholder | 0 |
| Issues | 0 |


## Full Page Audit Table

| # | Page | URL | Word Count | Headings | Status | Issues Found |
|---|------|-----|-----------|----------|--------|--------------|
| 1 | pages/404.njk | /404.html | 65 | H1:1 H2:1 H3:1 | ⚠️ Stub | Low word count (65) |
| 2 | pages/about/engagement-model.njk | /about/engagement-model.html | 508 | H1:1 H2:5 H3:8 | ✅ Complete | — |
| 3 | pages/about.njk | /about.html | 653 | H1:1 H2:8 H3:10 | ✅ Complete | Factual claim: experience years claim: 'years' |
| 4 | pages/careers.njk | /careers.html | 373 | H1:1 H2:4 H3:7 | ✅ Complete | — |
| 5 | pages/case-studies/banking-blockchain.njk | /case-studies/banking-blockchain.html | 513 | H1:1 H2:6 H3:4 | ✅ Complete | — |
| 6 | pages/case-studies/energy-scada.njk | /case-studies/energy-scada.html | 491 | H1:1 H2:6 H3:4 | ✅ Complete | — |
| 7 | pages/case-studies/fleet-predictive-maintenance.njk | /case-studies/fleet-predictive-maintenance.html | 761 | H1:1 H2:6 H3:4 | ✅ Complete | — |
| 8 | pages/case-studies/government-smart-city.njk | /case-studies/government-smart-city.html | 478 | H1:1 H2:6 H3:4 | ✅ Complete | — |
| 9 | pages/case-studies/healthcare-uptime.njk | /case-studies/healthcare-uptime.html | 467 | H1:1 H2:6 H3:4 | ✅ Complete | — |
| 10 | pages/case-studies/hospitality-guest-experience.njk | /case-studies/hospitality-guest-experience.html | 504 | H1:1 H2:6 H3:4 | ✅ Complete | — |
| 11 | pages/case-studies/retail-omnichannel.njk | /case-studies/retail-omnichannel.html | 469 | H1:1 H2:6 H3:4 | ✅ Complete | — |
| 12 | pages/case-studies/telecom-edge.njk | /case-studies/telecom-edge.html | 469 | H1:1 H2:6 H3:4 | ✅ Complete | — |
| 13 | pages/case-studies-index.njk | /case-studies.html | 247 | H1:1 H2:1 H3:9 | ✅ Complete | — |
| 14 | pages/contact.njk | /contact.html | 134 | H1:1 H2:2 H3:1 | ✅ Complete | — |
| 15 | pages/faq.njk | /faq.html | 614 | H1:1 H2:4 H3:13 | ✅ Complete | — |
| 16 | pages/global-connectivity.njk | /global-connectivity.html | 261 | H1:1 H2:4 H3:4 | ✅ Complete | — |
| 17 | pages/industries/banking.njk | /industries/banking.html | 353 | H1:1 H2:5 H3:14 | ✅ Complete | — |
| 18 | pages/industries/defence.njk | /industries/defence.html | 528 | H1:1 H2:6 H3:15 | ✅ Complete | — |
| 19 | pages/industries/education.njk | /industries/education.html | 350 | H1:1 H2:5 H3:14 | ✅ Complete | — |
| 20 | pages/industries/energy.njk | /industries/energy.html | 357 | H1:1 H2:5 H3:14 | ✅ Complete | — |
| 21 | pages/industries/government.njk | /industries/government.html | 392 | H1:1 H2:5 H3:14 | ✅ Complete | — |
| 22 | pages/industries/healthcare.njk | /industries/healthcare.html | 356 | H1:1 H2:5 H3:14 | ✅ Complete | — |
| 23 | pages/industries/hospitality.njk | /industries/hospitality.html | 358 | H1:1 H2:5 H3:14 | ✅ Complete | — |
| 24 | pages/industries/logistics.njk | /industries/logistics.html | 359 | H1:1 H2:5 H3:14 | ✅ Complete | — |
| 25 | pages/industries/maritime.njk | /industries/maritime.html | 508 | H1:1 H2:6 H3:15 | ✅ Complete | — |
| 26 | pages/industries/real-estate.njk | /industries/real-estate.html | 364 | H1:1 H2:5 H3:14 | ✅ Complete | — |
| 27 | pages/industries/retail.njk | /industries/retail.html | 346 | H1:1 H2:5 H3:14 | ✅ Complete | — |
| 28 | pages/industries/telecom.njk | /industries/telecom.html | 337 | H1:1 H2:5 H3:14 | ✅ Complete | — |
| 29 | pages/industries-index.njk | /industries.html | 192 | H1:1 H2:2 H3:13 | ✅ Complete | — |
| 30 | pages/insights/ai-native-enterprise-transformation.njk | /insights/ai-native-enterprise-transformation.html | 446 | H1:1 H2:3 H3:4 | ✅ Complete | — |
| 31 | pages/insights/blockchain-trade-finance.njk | /insights/blockchain-trade-finance.html | 1186 | H1:1 H2:6 H3:5 | ✅ Complete | — |
| 32 | pages/insights/case-studies.njk | /insights/case-studies.html | 279 | H1:1 H2:0 H3:7 | ✅ Complete | — |
| 33 | pages/insights/cloud-migration-strategy.njk | /insights/cloud-migration-strategy.html | 1330 | H1:1 H2:6 H3:6 | ✅ Complete | — |
| 34 | pages/insights/continuous-modernization.njk | /insights/continuous-modernization.html | 385 | H1:1 H2:2 H3:3 | ✅ Complete | — |
| 35 | pages/insights/cybersecurity-threat-landscape.njk | /insights/cybersecurity-threat-landscape.html | 1094 | H1:1 H2:7 H3:5 | ✅ Complete | — |
| 36 | pages/insights/data-centre-trends.njk | /insights/data-centre-trends.html | 1121 | H1:1 H2:6 H3:5 | ✅ Complete | — |
| 37 | pages/insights/digital-transformation-mea.njk | /insights/digital-transformation-mea.html | 1008 | H1:1 H2:6 H3:6 | ✅ Complete | — |
| 38 | pages/insights/edge-ai-fleet-management.njk | /insights/edge-ai-fleet-management.html | 1484 | H1:1 H2:6 H3:6 | ✅ Complete | — |
| 39 | pages/insights/hybrid-cloud-default-architecture.njk | /insights/hybrid-cloud-default-architecture.html | 476 | H1:1 H2:3 H3:3 | ✅ Complete | — |
| 40 | pages/insights/index.njk | /insights.html | 356 | H1:1 H2:1 H3:11 | ✅ Complete | — |
| 41 | pages/insights/sd-wan-mea.njk | /insights/sd-wan-mea.html | 1280 | H1:1 H2:6 H3:6 | ✅ Complete | — |
| 42 | pages/insights/sovereign-compute-mea.njk | /insights/sovereign-compute-mea.html | 1507 | H1:1 H2:7 H3:5 | ✅ Complete | — |
| 43 | pages/insights/whitepapers.njk | /insights/whitepapers.html | 232 | H1:1 H2:0 H3:7 | ✅ Complete | — |
| 44 | pages/leadership.njk | /leadership.html | 156 | H1:1 H2:3 H3:5 | ✅ Complete | — |
| 45 | pages/methodology.njk | /methodology.html | 308 | H1:1 H2:4 H3:9 | ✅ Complete | — |
| 46 | pages/partners.njk | /partners.html | 253 | H1:1 H2:4 H3:5 | ✅ Complete | — |
| 47 | pages/privacy-policy.njk | /privacy-policy.html | 225 | H1:1 H2:7 H3:1 | ✅ Complete | — |
| 48 | pages/solutions/ai-data-services.njk | /solutions/ai-data-services.html | 401 | H1:1 H2:5 H3:9 | ✅ Complete | — |
| 49 | pages/solutions/application-services.njk | /solutions/application-services.html | 433 | H1:1 H2:5 H3:9 | ✅ Complete | — |
| 50 | pages/solutions/blockchain.njk | /solutions/blockchain.html | 487 | H1:1 H2:6 H3:13 | ✅ Complete | — |
| 51 | pages/solutions/cloud.njk | /solutions/cloud.html | 503 | H1:1 H2:6 H3:14 | ✅ Complete | — |
| 52 | pages/solutions/connectivity.njk | /solutions/connectivity.html | 526 | H1:1 H2:6 H3:14 | ✅ Complete | — |
| 53 | pages/solutions/consulting/digital-transformation-strategy.njk | /solutions/consulting/digital-transformation-strategy.html | 762 | H1:1 H2:7 H3:17 | ✅ Complete | — |
| 54 | pages/solutions/consulting/infrastructure-network-audits.njk | /solutions/consulting/infrastructure-network-audits.html | 761 | H1:1 H2:7 H3:17 | ✅ Complete | — |
| 55 | pages/solutions/consulting/managed-services-outsourcing.njk | /solutions/consulting/managed-services-outsourcing.html | 787 | H1:1 H2:7 H3:12 | ✅ Complete | — |
| 56 | pages/solutions/consulting/regulatory-compliance-advisory.njk | /solutions/consulting/regulatory-compliance-advisory.html | 776 | H1:1 H2:6 H3:17 | ✅ Complete | — |
| 57 | pages/solutions/consulting/technology-roadmap-vendor-selection.njk | /solutions/consulting/technology-roadmap-vendor-selection.html | 760 | H1:1 H2:6 H3:17 | ✅ Complete | — |
| 58 | pages/solutions/consulting/tokenisation-advisory.njk | /solutions/consulting/tokenisation-advisory.html | 794 | H1:1 H2:7 H3:12 | ✅ Complete | — |
| 59 | pages/solutions/consulting.njk | /solutions/consulting.html | 747 | H1:1 H2:7 H3:19 | ✅ Complete | — |
| 60 | pages/solutions/critical-infrastructure-consulting.njk | /solutions/critical-infrastructure-consulting.html | 870 | H1:1 H2:8 H3:13 | ✅ Complete | — |
| 61 | pages/solutions/cyber-security.njk | /solutions/cyber-security.html | 524 | H1:1 H2:6 H3:14 | ✅ Complete | — |
| 62 | pages/solutions/data-centre.njk | /solutions/data-centre.html | 813 | H1:1 H2:9 H3:14 | ✅ Complete | — |
| 63 | pages/solutions/digital-workplace.njk | /solutions/digital-workplace.html | 451 | H1:1 H2:5 H3:10 | ✅ Complete | — |
| 64 | pages/solutions/disaster-recovery.njk | /solutions/disaster-recovery.html | 538 | H1:1 H2:6 H3:14 | ✅ Complete | — |
| 65 | pages/solutions/edge-ai-inference.njk | /solutions/edge-ai-inference.html | 559 | H1:1 H2:6 H3:14 | ✅ Complete | — |
| 66 | pages/solutions/edge-compute-infrastructure.njk | /solutions/edge-compute-infrastructure.html | 499 | H1:1 H2:6 H3:14 | ✅ Complete | — |
| 67 | pages/solutions/hardware-security.njk | /solutions/hardware-security.html | 620 | H1:1 H2:6 H3:14 | ✅ Complete | — |
| 68 | pages/solutions/identity-access.njk | /solutions/identity-access.html | 510 | H1:1 H2:6 H3:14 | ✅ Complete | — |
| 69 | pages/solutions/iot.njk | /solutions/iot.html | 547 | H1:1 H2:6 H3:14 | ✅ Complete | — |
| 70 | pages/solutions/managed-services.njk | /solutions/managed-services.html | 504 | H1:1 H2:6 H3:14 | ✅ Complete | — |
| 71 | pages/solutions/mobile-data-centre.njk | /solutions/mobile-data-centre.html | 478 | H1:1 H2:6 H3:14 | ✅ Complete | — |
| 72 | pages/solutions/network-security.njk | /solutions/network-security.html | 500 | H1:1 H2:6 H3:14 | ✅ Complete | — |
| 73 | pages/solutions/ota-fleet-management.njk | /solutions/ota-fleet-management.html | 541 | H1:1 H2:6 H3:14 | ✅ Complete | — |
| 74 | pages/solutions/post-quantum-security.njk | /solutions/post-quantum-security.html | 593 | H1:1 H2:6 H3:14 | ✅ Complete | — |
| 75 | pages/solutions/secure-edge-computing.njk | /solutions/secure-edge-computing.html | 597 | H1:1 H2:6 H3:14 | ✅ Complete | — |
| 76 | pages/solutions/smart-building-edge.njk | /solutions/smart-building-edge.html | 545 | H1:1 H2:6 H3:14 | ✅ Complete | — |
| 77 | pages/solutions/sovereign-compute.njk | /solutions/sovereign-compute.html | 516 | H1:1 H2:6 H3:14 | ✅ Complete | — |
| 78 | pages/solutions-index.njk | /solutions.html | 430 | H1:1 H2:4 H3:25 | ✅ Complete | — |
| 79 | pages/terms-of-service.njk | /terms-of-service.html | 192 | H1:1 H2:6 H3:1 | ✅ Complete | — |
| 80 | pages/why-meaicon.njk | /why-meaicon.html | 462 | H1:1 H2:4 H3:12 | ✅ Complete | — |

## Pages Needing Content Rewrite (Ranked by Priority)

| Priority | Page | Word Count | Status | Reasons |
|----------|------|------------|--------|---------|
| 80 | pages/404.njk | 65 | Stub | Stub content; Very low word count (65) |
| 15 | pages/contact.njk | 134 | Complete | Low word count (134) |
| 15 | pages/industries-index.njk | 192 | Complete | Low word count (192) |
| 15 | pages/leadership.njk | 156 | Complete | Low word count (156) |
| 15 | pages/terms-of-service.njk | 192 | Complete | Low word count (192) |

**Priority Levels:**
- **100+**: Critical — placeholder or very thin content, needs immediate rewrite
- **30-50**: High — stub-level content or unrebranded external references
- **15-25**: Medium — low word count, missing elements
- **5-10**: Low — minor missing elements (hero, CTA, meta)

## Factual Claims Requiring Verification

### pages/about.njk (/about.html)

- ⚠️ experience years claim: 'years'

**Recommendation:** All factual claims (superlatives like 'MEA's largest', 'first to', uptime percentages) should be sourced with citations or reworded to be verifiable.

## Brand Consistency Issues

✅ No brand consistency issues found. All pages correctly reference MEAICON, use accent #0066FF, and do not contain unrebranded source references.

### Company Details Verification

| Detail | Expected | Found |
|--------|----------|-------|
| Company Name | MEAICON LLC FZ | ✅ In footer.njk |
| Address | Meydan Free Zone, Dubai, UAE | ✅ In footer.njk |
| Services | Connectivity, Data Centre, Cyber Security, Blockchain, Consulting | ✅ All listed in footer and header nav |
| Accent Color | #0066FF | ✅ No old gold #C1873D found |
| Social Links | LinkedIn, X, Instagram | ✅ All present in footer |

## Duplicate Content Detection

✅ No duplicate or near-duplicate pages found. All 80 pages have unique titles and heading structures.

## Missing Meta Tags & JSON-LD Summary

### JSON-LD Structured Data

- ✅ `site-head.njk` provides **Organization** JSON-LD globally to all 80 pages
- ✅ `layout.njk` provides **BreadcrumbList** JSON-LD globally to all 80 pages
- ✅ `index.html` has inline JSON-LD
- ℹ️ Individual pages do not have inline JSON-LD, but this is **by design** — the layout template handles it
- ℹ️ Pages with `legacySource` front matter can override the default Organization JSON-LD

### Meta Tags

- Pages missing title in front matter: 0
- Pages missing description in front matter: 0
- Pages missing permalink in front matter: 0

### Pages Without Hero Section

✅ All 80 pages have a hero section.

### Pages Without CTA Buttons

✅ All 80 pages have CTA buttons.

## Content Quality Assessment

### Tone Consistency

All pages maintain a consistent enterprise B2B technology tone. Content uses professional language appropriate for government and enterprise audiences across the Middle East and Africa region. The tone is authoritative without being overly promotional.

### Service Alignment

| Service Area | Pages Covering It |
|-------------|-------------------|
| Connectivity | solutions/connectivity, global-connectivity, solutions/sd-wan (via connectivity), solutions/edge-compute-infrastructure |
| Data Centre | solutions/data-centre, solutions/cloud, solutions/disaster-recovery, solutions/mobile-data-centre, solutions/sovereign-compute |
| Cyber Security | solutions/cyber-security, solutions/network-security, solutions/identity-access, solutions/hardware-security, solutions/post-quantum-security |
| Blockchain | solutions/blockchain, solutions/consulting/tokenisation-advisory, insights/blockchain-trade-finance, case-studies/banking-blockchain |
| Consulting | solutions/consulting, solutions/consulting/* (5 sub-pages), solutions/critical-infrastructure-consulting, methodology |

✅ All five core service areas are well-represented across multiple pages.

## Recommendations

### High Priority
1. **pages/404.njk** — 65 words, stub-level content. Needs a proper 404 page with helpful navigation links, search, and on-brand messaging.
2. **pages/contact.njk** — 134 words. Needs expanded contact information (phone, email, office address, map, form).
3. **pages/leadership.njk** — 156 words. Needs leadership team bios and photos.
4. **pages/industries-index.njk** — 192 words. Needs more intro text and industry overview cards.
5. **pages/terms-of-service.njk** — 192 words. Needs full legal terms content.

### Medium Priority
1. **Factual claim in pages/about.njk** — The phrase 'over X years' should be verified with the actual founding date and quantified.
2. **index.html** — Verify that all JSON-LD is correct and complete (Organization schema with proper address, contact info).
3. Consider adding Article/WebPage type JSON-LD to insights/ and case-studies/ pages for better SEO.

### Low Priority
1. Some pages could benefit from more imagery (currently only some have `<img>` tags).
2. Consider adding structured FAQ schema to pages/faq.njk.
3. Newsletter form in footer has `action="#"` — needs proper form submission endpoint.

### Technical Notes
- **TODO in `_includes/site-head.njk`:** Contains `<!-- TODO: Migrate to build-time Tailwind for production — remove CDN script and 'unsafe-inline' CSP -->`. This is a technical debt note, not content placeholder. Should be addressed before production launch.
- **Newsletter form in footer** has `action="#"` — needs a real form submission endpoint before launch.
- Per-page inline JSON-LD is NOT needed — the layout template (`site-head.njk` + `layout.njk`) provides Organization and BreadcrumbList JSON-LD globally.
- Per-page meta/OG/Twitter tags are NOT needed — `site-head.njk` injects them using front matter variables.
- The site expands beyond the core 5 services (Connectivity, Data Centre, Cyber Security, Blockchain, Consulting) to include 20+ sub-solutions (Cloud, IoT, Edge Compute, AI, Managed Services, etc.). This is expected for a full enterprise site; the core 5 are the primary nav grouping.
