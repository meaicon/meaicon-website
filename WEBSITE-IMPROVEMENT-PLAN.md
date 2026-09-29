# MEAICON Website — Master Improvement Plan

## Issues Identified

### 1. Navigation / IA Inconsistencies (header.njk + footer.njk)

**Header nav categories:** Solutions, Industries, Presence, Partners, Case Studies, Insights, About
**Footer categories:** Solutions, Company, Resources

**Problems:**
- Footer "Solutions" column lists 17 links flat — no grouping by category
- Footer "Solutions" column is MISSING: Network Security, Identity & Access, Disaster Recovery, IoT & Edge, Mobile Data Centre, Hardware Security, OTA Fleet Management, Smart Building Edge
- Footer "Company" column lists only Defence & Maritime under Industries (missing 10 other industries)
- Footer "Resources" column has redundant links (Insights & Analysis → /insights.html, Whitepapers → /insights/whitepapers.html, Case Studies → /insights/case-studies.html) — but main Case Studies page (/case-studies.html) is in "Company" column instead
- Pages NOT in footer: Why MEAICON, Methodology, Leadership, FAQ
- Pages NOT in header: Why MEAICON, Methodology, Leadership, FAQ, Careers
- Header Solutions mega-menu is a flat alphabetical list, not grouped by domain (Connectivity, Infrastructure, Security, Edge/AI, Consulting)

**Fix:**
- Group footer Solutions into sub-sections: Core Infrastructure, Security, Edge & AI, Consulting
- Add all missing solution links to footer
- Fix Industries in footer — either link to /industries.html only (no sub-items) or list all 12
- Add Why MEAICON, Methodology, Leadership, FAQ to both header and footer
- Reorganize header Solutions mega-menu into grouped categories with section headers
- Add Careers to header (currently only in footer)

### 2. Page Hero / Template Inconsistencies (71 page templates)

**Problems:**
- Consulting sub-pages (6 files in pages/solutions/consulting/) are BROKEN:
  - No `<main class="flex-1 site-shell">` wrapper
  - No `<div class="max-w-7xl mx-auto px-4 lg:px-6">` container inside sections
  - Use `<nav class="breadcrumb">` instead of `<div class="breadcrumb">` (different pattern)
  - No consistent section structure (content-section / content-section-alt alternating)
- Insights articles use `max-w-3xl mx-auto` (narrow, centered) while all other pages use `max-w-7xl mx-auto` (wide, left-aligned) — this is intentional for reading but the hero section also narrows, making it look different from other pages
- Some pages have CTA buttons in hero (solutions, industries, careers), others don't (about, contact, FAQ, leadership, methodology, why-meaicon, partners, case-studies-index, privacy, terms)
- Breadcrumb pattern differs: most use `<div class="breadcrumb">` with ` / ` separator, consulting sub-pages use `<nav class="breadcrumb" aria-label="Breadcrumb">` with `›` separator

**Fix:**
- Fix all 6 consulting sub-pages: add proper `<main>` wrapper, containers, consistent breadcrumb pattern
- Standardize hero: all pages get breadcrumb, eyebrow, H1, lede paragraph
- Add CTA buttons to pages that should have them (about, why-meaicon, methodology, partners, case-studies-index)
- Keep insights articles with narrow reading width but make hero section consistent

### 3. Visual Design Gap vs Design Prompt

**Current state:**
- Colors: paper (#FAFBFC), ink (#0A192F), accent (#4F46E5 - indigo), teal (#1E40AF)
- Fonts: Plus Jakarta Sans (display), Inter (body)
- Hero: light gradient background (linear-gradient(135deg, #F8FAFC 0%, #fff 72%))
- No dark hero sections (design prompt calls for dark hero with 100vh)
- No scroll animations (fade-in/slide-up)
- No dark mode support
- Tailwind CDN loaded at runtime (not built)
- No gradient accents on buttons/dividers
- Cards have hover lift but no scale-up

**Design prompt calls for:**
- Dark navy/charcoal hero sections (not pure black)
- Electric blue (#0066FF) accent — current is indigo (#4F46E5)
- Full viewport hero (100vh) with dark overlay
- Alternating light/dark section rhythm
- Scroll animations (Intersection Observer fade-in/slide-up)
- Gradients on buttons/dividers
- Dark mode support
- Card scale-up on hover (1.02-1.05)

**Recommended approach (evolutionary, not revolutionary):**
- Keep existing color palette (it's already good) but add dark hero variant
- Add scroll animation Intersection Observer
- Add gradient accents
- Improve card hover (add slight scale)
- Add dark section variants for visual rhythm
- DON'T change accent from indigo to electric blue — the indigo is already deployed and looks professional; the design prompt is a guide, not a mandate

### 4. Content Integration (from SharePoint documents)

**Document 1: meaicon-critical-infrastructure.md** (4 pages)
- Vendor-neutral critical infrastructure & data center consulting
- Covers: planning, high availability, efficiency, MEP, network/security architecture, data center design, bid process, certification, operations standards, audits, optimization
- **Best placement:** Enhance existing /solutions/data-centre.html and /solutions/consulting.html; create new page /solutions/critical-infrastructure-consulting.html

**Document 2: Meaicon-Enterprise-Technology-Services.md** (6 pages)
- Comprehensive: company overview, 7 core services, consulting, platform/integration, 5 key trends, customer outcomes, engagement model
- Covers services NOT currently on the site: AI & Data Services, Application Services, Digital Workplace Services, Mainframe Services
- Enriches existing: Cloud Services, Cyber Resilience, Network Services, Consulting
- **Best placement:**
  - Page 1 (Company Overview): Enhance /about.html and /why-meaicon.html
  - Page 2 (Core Services): Create new pages for AI & Data, Application Services, Digital Workplace; enhance Cloud, Cyber Security, Network pages
  - Page 3 (Consulting): Enhance /solutions/consulting.html and sub-pages
  - Page 4 (Platform): New page /solutions/integration-platform.html
  - Page 5 (Trends): New insight articles under /insights/
  - Page 6 (Outcomes): Enhance /about.html or create /about/engagement-model.html

## Execution Plan — Parallel Subagents

### Subagent A: Navigation & IA (header.njk, footer.njk)
- Reorganize header mega-menu into grouped categories
- Reorganize footer into proper grouped columns
- Add missing pages to both
- Ensure consistency between header and footer categories

### Subagent B: CSS & Visual Design (site-head.njk)
- Add scroll animation system (Intersection Observer)
- Add dark hero variant CSS
- Add gradient accents on buttons/dividers
- Improve card hover (scale-up)
- Add dark section rhythm variants
- Add skeleton/loading states
- Add dark mode CSS (prefers-color-scheme)

### Subagent C: Template Consistency (all pages/*.njk)
- Fix 6 consulting sub-pages (add main wrapper, containers, consistent breadcrumb)
- Standardize all page heroes
- Add CTA buttons where missing
- Ensure consistent section structure across all pages

### Subagent D: Content Integration (new + enhanced pages)
- Map content from both SharePoint documents to appropriate pages
- Create new pages for missing services
- Enhance existing pages with richer content
- Ensure content voice consistency
