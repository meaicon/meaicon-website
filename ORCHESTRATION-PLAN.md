# MEAICON Website — Sub-Agent Orchestration Plan

## Pipeline

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
│ (Content Agent)  │  Output: migrated/*.njk, index.njk
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

## Profiles Created

| Profile | Role | Skill | Directory |
|---------|------|-------|-----------|
| `meaicon-research` | Crawl external sites, extract content | `meaicon-crawl` | `profiles/meaicon-research/` |
| `meaicon-content` | Rebrand content, remove source refs, verify facts | `meaicon-rebrand` | `profiles/meaicon-content/` |
| `meaicon-dev` | UI/UX, CSS, Tailwind, Eleventy build | `meaicon-ui` | `profiles/meaicon-dev/` |
| `meaicon-qa` | Validate build, SEO, accessibility, hallucination check | `meaicon-qa` | `profiles/meaicon-qa/` |

## Shared Context (in every profile's MEMORY.md)

- **Repo**: `C:/Users/nev3s/repos/meaicon-website`
- **GitHub**: `meaicon/meaicon-website` (branch `website-redesign`)
- **Tech**: Eleventy 3.1.6, Nunjucks, Tailwind CSS (CDN), Plus Jakarta Sans + Inter
- **Company**: MEAICON LLC FZ, Meydan Free Zone, Dubai, UAE
- **Services**: Connectivity, Data Centre, Cyber Security, Blockchain, Consulting
- **Pipeline**: Research → Content → Dev → QA → User

## Data Flow

```
research-data/
  <source-site>/
    extracted-content.md     # Raw extracted content from crawler
    metadata.json            # Source URL, date, type, word count
    key-data.json            # Structured data (pricing, features, specs)
    HANDOFF.md               # Handoff note to Content Agent

migrated/                    # Rebranded Nunjucks templates
  solutions.njk
  industries.njk
  contact.njk
  etc.

_site/                       # Built HTML output
  index.html
  solutions.html
  etc.

qa-reports/
  2026-09-22-qa-report.md    # Per-cycle validation report
```

## How to Use

### 1. User provides URLs
Tell the orchestrator (this Hermes session) which websites to crawl. Example:
> "Crawl these sites for content: https://example1.com, https://example2.com"

### 2. Orchestrator dispatches to Research Agent
The Research Agent crawls the URLs, extracts content, saves to `research-data/<site>/`.

### 3. Content Agent rebrands
The Content Agent reads the extracted content, removes all source references, rebrands under MEAICON voice, places into templates.

### 4. Dev Agent builds UI
The Dev Agent takes the content-laden templates, builds/refines UI components, ensures responsive design, runs the build.

### 5. QA Agent validates
The QA Agent runs the full validation suite — build, content integrity, SEO, accessibility, hallucination check. Produces a QA report.

### 6. User reviews
If QA passes, the user reviews the built site. If QA fails, issues route back to the responsible agent.

## Constraints

- **Branch only**: All work on `website-redesign`. Main branch untouched.
- **No hallucination**: Every claim must be verifiable or removed.
- **No source traces**: Zero references to original sites in final output.
- **Excellent UI/UX**: Target Stripe/Linear/Vercel-level polish.
- **Production-ready**: Lighthouse 95+, WCAG AA, semantic HTML.

## Infrastructure Audit (2026-09-22)

### Security Headers (`_headers`)
- ✅ CSP with restricted script/style/img/font/connect sources
- ✅ HSTS with preload, X-Frame-Options: DENY, X-Content-Type-Options: nosniff
- ✅ Referrer-Policy: strict-origin-when-cross-origin
- ✅ Permissions-Policy disabling geolocation, microphone, camera, payment, browsing-topics
- ✅ Cross-Origin-Opener-Policy + Resource-Policy: same-origin
- ✅ Caching: immutable for /assets/*, must-revalidate for HTML
- Note: `unsafe-inline` in CSP required while Tailwind CDN is in use

### Sitemap (`sitemap.xml`)
- Fixed: added 8 missing URLs (about/engagement-model, insights/ai-native-enterprise-transformation, insights/continuous-modernization, insights/hybrid-cloud-default-architecture, solutions/ai-data-services, solutions/application-services, solutions/critical-infrastructure-consulting, solutions/digital-workplace)
- Total: 80 URLs (homepage + 79 page templates)

### Cookie Consent (Accessibility)
- ✅ 44px minimum touch targets (WCAG 2.5.5)
- ✅ Visible `:focus-visible` outlines (WCAG 2.4.7)
- ✅ Focus trap + Escape key in preferences modal (WCAG 2.4.3)
- ✅ `prefers-reduced-motion` support (WCAG 2.3.3)
- ✅ `prefers-color-scheme: dark` support

### CI/CD
- ✅ GitHub Actions workflow builds and deploys to GitHub Pages
- Added `GITHUB_ACTIONS: true` env var for correct base-path rewriting
- Added `continue-on-error` for non-blocking validation/audit steps
