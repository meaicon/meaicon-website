# MEAICON Website Redesign - Coordination FAQ

**Last Updated:** Tuesday, September 22, 2026  
**Maintainer:** Boss Agent (this session)  
**Purpose:** Living FAQ for all four profiles (Research, Content, Dev, QA)  

---

## Quick Links
- [Pipeline Overview](#pipeline-overview)
- [Directory Structure](#directory-structure)
- [Branch & Git Rules](#branch--git-rules)
- [Research Agent FAQ](#research-agent-faq)
- [Content Agent FAQ](#content-agent-faq)
- [Dev Agent FAQ](#dev-agent-faq)
- [QA Agent FAQ](#qa-agent-faq)
- [Decision Log](#decision-log)

---

## Pipeline Overview

```
User provides URLs
       ↓
┌─────────────────┐
│ meaicon-research │  Crawl → extract → structure
│ (Research Agent) │  Output: research-data/<site>/
└────────┬────────┘
         ↓
┌─────────────────┐
│ meaicon-content  │  Rebrand → verify facts → place in templates
│ (Content Agent)  │  Output: migrated/*.njk, then pages/*.njk
└────────┬────────┘
         ↓
┌─────────────────┐
│ meaicon-dev      │  UI/UX → CSS → components → build
│ (Dev Agent)      │  Output: _site/ (built HTML)
└────────┬────────┘
         ↓
┌─────────────────┐
│ meaicon-qa       │  Validate → SEO → a11y → hallucination check
│ (QA Agent)      │  Output: qa-reports/<date>-qa-report.md
└────────┬────────┘
         ↓
    User review
```

**Key Principle:** Each agent works independently but passes artifacts forward. Never skip a stage. If QA fails, route back to the responsible agent.

---

## Directory Structure

```
meaicon-website/
├── .eleventy.js              # Eleventy config (SSOT for build)
├── ORCHESTRATION-PLAN.md     # Pipeline definition
├── docs/
│   └── design-guideline.md   # Visual design SSOT
├── _includes/
│   ├── site-head.njk         # <head> template (SEO, meta, CSS/JS)
│   ├── header.njk            # Navigation, logo, CTA
│   ├── footer.njk            # Footer columns, newsletter
│   ├── layout.njk            # Base HTML shell (includes above)
│   └── home-main.html        # Homepage hero section
├── pages/                    # 80 production .njk templates
│   ├── solutions/            # 20+ service pages
│   ├── industries/           # 10+ vertical pages
│   ├── insights/             # Blog/thought leadership
│   ├── case-studies/         # Customer stories
│   └── *.njk                 # Static pages (about, contact, etc.)
├── migrated/                 # Content Agent working area (10 stubs)
├── research-data/            # Research Agent output
│   ├── blue-edge-docs/
│   └── content-source/
├── data/
│   └── site-content.json     # Manifest for page generation
├── scripts/                  # Automation tools
│   ├── generate-page.js
│   ├── generate-pages-from-manifest.js
│   ├── audit-metadata.js
│   └── validate-content.js
├── assets/
│   ├── css/                  # Custom CSS (cookie-consent.css only)
│   ├── js/                   # Custom JS (cookie-consent.js)
│   └── brand/                # Logos, images
├── qa-reports/               # QA Agent output (empty initially)
├── _site/                    # Eleventy build output (gitignored)
└── node_modules/             # Dependencies
```

---

## Branch & Git Rules

| Rule | Detail |
|------|--------|
| **Working Branch** | `website-redesign` ONLY |
| **Protected Branch** | `main` – NEVER commit directly |
| **Push** | `git push origin website-redesign` |
| **Deploy** | Auto on push to `website-redesign` via GitHub Pages |
| **Commits** | Conventional format: `feat:`, `fix:`, `chore:`, `docs:` |
| **Profile Isolation** | Each profile has its own Hermes session; don't mix work |

---

## Research Agent FAQ

### What URLs should I crawl?
**Priority 1 (Core Services):**
- SD-WAN/MPLS providers: Aryaka, Cato, Versa, Cisco Meraki
- Data center: Equinix, Digital Realty, CyrusOne, Gulf Data Hub
- Cybersecurity: Palo Alto, Fortinet, CrowdStrike, Zscaler
- Blockchain enterprise: Hyperledger, R3 Corda, ConsenSys Quorum
- Consulting: McKinsey, BCG, Accenture, Deloitte digital practices

**Priority 2 (MEA Context):**
- UAE: TRA, DIFC, ADGM, Smart Dubai, Dubai Cyber Index
- KSA: NCA, SDAIA, Vision 2030, CITC
- Regional telcos: du, Etisalat, STC, Ooredoo, Zain

**Priority 3 (Thought Leadership):**
- Gartner, Forrester, IDC reports on MEA infrastructure
- White papers from IEEE, ISACA, Cloud Security Alliance

### Where do I save extracted content?
```
research-data/<site-name>/
├── extracted-content.md      # Full raw text from crawl
├── metadata.json             # { "url": "...", "crawled_at": "...", "type": "service/industry/insight", "word_count": 1234 }
├── key-data.json             # { "pricing": [...], "features": [...], "specs": {...} }
└── HANDOFF.md                # Notes for Content Agent: "Focus on SLA claims", "Verify UAE regulation dates"
```

### What's the file naming convention?
- `01-<topic>.md`, `02-<topic>.md` for ordered series
- `<topic>.md` for standalone documents
- Use kebab-case, lowercase

### How do I know when research is "done" for a page?
When you have:
1. ≥2 independent sources confirming key claims
2. Structured data (pricing, specs, features) in `key-data.json`
3. A clear `HANDOFF.md` telling Content Agent what to emphasize

### What if I find conflicting information?
- Note both sources in `extracted-content.md`
- Flag in `HANDOFF.md`: "CONFLICT: Source A says X, Source B says Y"
- Content Agent decides based on MEAICON positioning

---

## Content Agent FAQ

### What's the brand voice?
| Attribute | Guidance |
|-----------|----------|
| **Tone** | Authoritative, confident, professional |
| **Perspective** | First-person plural: "We design...", "Our solutions..." |
| **Audience** | Enterprise CIOs, CTOs, IT Directors, Government officials |
| **Style** | Active voice, concrete metrics, minimal jargon |
| **No-Nos** | "Cutting-edge", "world-class", "best-in-class" without proof; passive voice; source references |

### How do I rebrand content?
1. Read `research-data/<site>/extracted-content.md` and `HANDOFF.md`
2. Extract facts, discard source branding
3. Rewrite in MEAICON voice using template structure
4. Add MEAICON-specific details (location: Dubai, Meydan Free Zone; services: 5 pillars)
5. Verify every statistic with a second source
6. Output to `migrated/<page-slug>.njk`

### Which template structure should I use?
All pages follow the same front matter + layout pattern:
```njk
---
layout: layout.njk
title: "Page Title — MEAICON"
description: "≤165 chars, compelling, includes primary keyword"
canonical: "https://www.meaicon.com/page.html"
permalink: /page.html
---
<main class="flex-1 site-shell">
  <section class="reveal page-hero">
    <div class="max-w-7xl mx-auto px-4 lg:px-6">
      <nav class="breadcrumb" aria-label="Breadcrumb">...</nav>
      <p class="eyebrow mb-4 mt-6">Section Name</p>
      <h1 class="page-title max-w-3xl">Compelling Headline</h1>
      <p>Lead paragraph...</p>
      <div class="mt-8 flex flex-wrap gap-4">
        <a href="/contact.html" class="btn-primary inline-flex items-center px-5 py-3">Talk to an expert &rarr;</a>
        <a href="/section.html" class="btn-secondary inline-flex items-center px-5 py-3">All [section]</a>
      </div>
    </div>
  </section>
  
  <section class="content-section reveal">
    <div class="max-w-7xl mx-auto px-4 lg:px-6">
      <!-- Section content here -->
    </div>
  </section>
</main>
```

### How do I verify facts?
- **Statistics:** Must appear in ≥2 reputable sources
- **Dates/Regulations:** Check official government sites (TRA, NCA, etc.)
- **Technical Specs:** Vendor documentation or IEEE standards
- **Case Study Metrics:** Must be plausible; if hypothetical, label clearly

### When do I move content from `migrated/` to `pages/`?
When:
- ✅ Front matter complete (title, description, canonical, permalink)
- ✅ Content rewritten in MEAICON voice
- ✅ No source references remain
- ✅ Passes `npm run validate:content` (no errors)
- ✅ QA Agent has reviewed (optional but recommended)

### What if a page needs content I don't have?
- Flag in front matter: `contentStatus: "needs-research"`
- Note specific gaps in a comment: `<!-- NEED: UAE data center pricing benchmarks -->`
- Research Agent will pick up on next cycle

---

## Dev Agent FAQ

### What CSS patterns are approved?
**CSS Variables (define in `:root` of custom CSS):**
```css
:root {
  --accent: #0066FF;
  --accent-strong: #0052cc;
  --accent-light: rgba(0, 102, 255, 0.1);
  --bg-primary: #0a0e1a;
  --bg-secondary: #111827;
  --bg-card: #ffffff;
  --text-primary: #0f172a;
  --text-secondary: #475569;
  --text-muted: #94a3b8;
  --line: #e2e8f0;
  --card: #ffffff;
}
[data-theme="dark"] {
  --bg-card: #1e293b;
  --text-primary: #f8fafc;
  --text-secondary: #cbd5e1;
  --line: #334155;
  --card: #1e293b;
}
```

**Spacing:** 4px base grid (Tailwind `p-1`=4px, `p-4`=16px, etc.)

**Typography:**
- Headings: `font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 700;`
- Body: `font-family: 'Inter', sans-serif; font-weight: 400; line-height: 1.7;`

**Buttons:**
```css
.btn-primary { background: var(--accent); color: white; }
.btn-primary:hover { background: var(--accent-strong); }
.btn-secondary { border: 2px solid var(--accent); color: var(--accent); }
.btn-secondary:hover { background: var(--accent-light); }
```

### What components need building?
| Component | Location | Status | Priority |
|-----------|----------|--------|----------|
| Card (service/insight/case-study) | `_includes/card.njk` | Needed | High |
| Button macro | `_includes/button.njk` | Needed | High |
| Mega-menu data | `_includes/header.njk` + data file | Partial | High |
| Form elements | `_includes/form-fields.njk` | Needed | Medium |
| Footer columns (dynamic) | `_includes/footer.njk` + data | Static now | Medium |
| Hero variants | `_includes/hero.njk` | Inline now | Medium |
| Table of contents | `_includes/toc.njk` | Needed | Low |
| Cookie consent | Already in assets/ | Done | — |

### Where do I put custom CSS/JS?
- **CSS:** `assets/css/custom.css` – import in `site-head.njk` after Tailwind
- **JS:** `assets/js/modules/` – ES modules, defer in `site-head.njk`
- **Images:** `assets/brand/`, `assets/images/` – Eleventy passthrough copies

### How do I add a new component?
1. Create in `_includes/<component>.njk`
2. Use `{% include "<component>.njk" %}` in pages
3. Pass data via front matter or data files
4. Document props in component file header comment

### What's the responsive breakpoint strategy?
- **Mobile-first** (Tailwind default)
- Breakpoints: `sm: 640px`, `md: 768px`, `lg: 1024px`, `xl: 1280px`
- Test at: 320px, 375px, 768px, 1024px, 1440px
- Use `container` class (`max-w-7xl mx-auto px-4 sm:px-6 lg:px-8`)

### How do I run the build locally?
```bash
npm run build    # Production build to _site/
npm run start    # Dev server with live reload
npm run clean    # Remove _site/
```

---

## QA Agent FAQ

### What are the acceptance criteria per page?
A page passes when **all** of these are true:

| Category | Criteria |
|----------|----------|
| **Build** | `npm run build` succeeds; HTML in `_site/` valid |
| **Content** | Title ≤65 chars, Description ≤165 chars, unique; no lorem ipsum; no source refs; claims verifiable |
| **Design** | #0066FF on primary CTAs/links; no #C1873D; responsive at 320/768/1440px |
| **SEO** | Canonical matches permalink; OG/Twitter tags present; JSON-LD Organization; H1 matches title intent |
| **A11y** | WCAG 2.1 AA: contrast ≥4.5:1; keyboard nav logical; skip link; alt text; form labels |
| **Perf** | Page weight <1.5MB; CSS in head, JS deferred; images WebP + lazy-loaded |

### What tools do I use?
- **Build validation:** `npm run build`, then `scripts/audit-metadata.js` on `_site/`
- **Content validation:** `npm run validate:content` on `pages/`
- **A11y:** axe-core via Playwright or browser extension
- **SEO:** Manual checklist + `scripts/audit-metadata.js`
- **Visual regression:** Playwright screenshots (to be implemented)

### Where do I save reports?
```
qa-reports/
└── <YYYY-MM-DD>-qa-report.md
```

**Report structure:**
```markdown
# QA Report - <date>

## Summary
- Pages tested: X
- Passed: Y
- Failed: Z
- Blockers: N

## Detailed Findings
### Critical (must fix)
- Page: issue

### High
...

### Medium
...

### Low
...

## Metrics
- Avg. load time: Xms
- Accessibility score: X/100
- SEO score: X/100

## Recommendations
1. [High] Fix ...
2. [Medium] Improve ...
3. [Low] Consider ...
```

### What if QA fails?
- Create GitHub issue with label `qa-fail`
- Assign to responsible agent (Content/Dev)
- Reference report: `qa-reports/<date>-qa-report.md`
- Re-test after fix; update report

### What's the hallucination check?
Verify every factual claim:
1. Search the claim + "MEAICON" – should only return our site
2. Search the claim without "MEAICON" – should find independent source
3. If no independent source: flag as "unverified" or remove
4. Common hallucinations: fake statistics, invented partnerships, wrong dates

---

## Decision Log

| Date | Decision | Made By | Impact |
|------|----------|---------|--------|
| 2026-09-22 | Accent color = #0066FF (electric blue) | Design guideline | All primary CTAs/links |
| 2026-09-22 | No old gold (#C1873D) anywhere | Design guideline | Clean migration |
| 2026-09-22 | 80 pages in `pages/` are production | Boss Agent | Content Agent targets these |
| 2026-09-22 | `migrated/` = Content working area | Boss Agent | 10 stubs to populate |
| 2026-09-22 | Eleventy 3.x + Nunjucks + Tailwind CDN | Tech stack | Dev Agent uses these |
| 2026-09-22 | GitHub Pages deploy on push to `website-redesign` | Ops | Auto-deploy configured |

---

## Quick Commands Reference

| Task | Command |
|------|---------|
| Build site | `npm run build` |
| Dev server | `npm run start` |
| Validate content | `npm run validate:content` |
| Audit metadata | `npm run audit:metadata` |
| Generate page stub | `npm run generate:page -- --slug=foo --title="Foo" --section=Solutions` |
| Generate all from manifest | `npm run generate:pages` |

---

## Contact / Escalation

- **Blockers:** Tag @boss-agent in GitHub issue
- **Design questions:** Reference `docs/design-guideline.md`
- **Content questions:** Check `ORCHESTRATION-PLAN.md` → Shared Context
- **Technical questions:** Check `.eleventy.js` and `_includes/`

---

**This FAQ is a living document.** Update it when decisions change or new patterns emerge.  
Last editor: Boss Agent (this session)