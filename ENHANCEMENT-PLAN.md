# MEAICON Website Content Enhancement Plan — `website-redesign` Branch

## Executive Summary

**Objective**: Enhance all content across the MEAICON redesign website using a three-agent pipeline (Firecrawl → LangChain → n8n) with master orchestrator verification. Work exclusively on `website-redesign` branch (GitHub Pages), never touching `main` (Cloudflare Pages).

**Current State**: 5 core solution pages already enhanced (connectivity, cyber-security, consulting, blockchain, data-centre). 35+ remaining solution/industry/case-study pages need enhancement.

**Pipeline**: Firecrawl (crawl/snapshot) → LangChain (research/enhancement) → n8n (content pipeline/automation) → Master Orchestrator (verify/inject/commit/deploy)

---

## Site Architecture (Website-Redesign Branch)

### Page Inventory (~72 pages)

| Category | Pages | Status |
|----------|-------|--------|
| **Core Solutions** | 5 (connectivity, cyber-security, consulting, blockchain, data-centre) | ✅ Enhanced |
| **Extended Solutions** | 22 (ai-compute, cloud, edge-*, iot, managed-services, etc.) | ⏳ Pending |
| **Consulting Sub-pages** | 6 (digital-transformation, infrastructure-audits, managed-services-outsourcing, regulatory-compliance, technology-roadmap, tokenisation) | ⏳ Pending |
| **Industries** | 11 (banking, defence, education, energy, government, healthcare, hospitality, logistics, maritime, real-estate, retail, telecom) | ⏳ Pending |
| **Case Studies** | 11 (banking-blockchain, defence-sovereign-edge, education-connected-campus, energy-scada, fleet-predictive-maintenance, government-smart-city, healthcare-uptime, hospitality-guest-experience, maritime-fleet-tracking, real-estate-smart-tower, retail-omnichannel, telecom-edge) | ⏳ Pending |
| **Insights/Blog** | 11 (ai-native-enterprise, blockchain-trade-finance, cloud-migration, continuous-modernization, cybersecurity-threat-landscape, data-centre-trends, digital-transformation-mea, edge-ai-fleet, hybrid-cloud, sd-wan-mea, sovereign-compute, whitepapers) | ⏳ Pending |
| **Company/Legal** | 8 (about, engagement-model, careers, contact, faq, leadership, methodology, partners, privacy-policy, terms-of-service) | ⏳ Pending |

**Total**: ~72 pages across 7 categories

---

## Three-Agent Pipeline Architecture

### Agent 1: Firecrawl (Crawl & Snapshot)
- **Role**: Automated crawling, snapshotting, content extraction
- **Tools**: `firecrawl scrape`, `firecrawl search`, `firecrawl research`
- **Output**: `research-data/firecrawl/<category>/extracted-content.md`, `sources.json`, `search-metadata.json`
- **Scope**: Competitor sites, industry references, best-practice content sources

### Agent 2: LangChain/LangGraph (Research & Enhancement)
- **Role**: Content analysis, fact verification, rebranding, enhancement generation
- **Tools**: LangGraph workflows, LLM chains for content transformation
- **Output**: `research-data/langchain/<category>/enhanced-content.md`, `content-analysis.json`, `fact-checks.json`, `summary.md`
- **Scope**: Transform raw research into MEAICON-branded, technically accurate content

### Agent 3: n8n (Content Pipeline Automation)
- **Role**: Orchestrate the end-to-end flow, schedule runs, handle retries, manage state
- **Tools**: n8n workflows at `localhost:5678`, HTTP Request nodes → OmniRoute (127.0.0.1:20128)
- **Output**: Automated pipeline execution, status tracking, error handling
- **Scope**: Chain Firecrawl → LangChain → injection → validation → commit

### Master Orchestrator (Verification & Deployment)
- **Role**: Cross-verify all agents, validate output quality, inject content, commit, deploy
- **Tools**: `meaicon-audit-orchestration` skill, `inject-enhanced-content.py`, git, GitHub Actions
- **Output**: Verified artifacts, git commits, GitHub Pages deployment

---

## Competitor/Reference Sources by Solution Domain

| Solution | Reference Competitors (to crawl) |
|----------|----------------------------------|
| **Connectivity** | Cisco Meraki, Aryaka, Cato Networks, Versa Networks, Expereo, GTT, Colt, PCCW |
| **Cyber Security** | Palo Alto Networks, CrowdStrike, SentinelOne, Fortinet, Check Point, Darktrace, Zscaler |
| **Consulting** | Deloitte Digital, Accenture, BCG Platinion, McKinsey Digital, Thoughtworks, EPAM |
| **Blockchain** | ConsenSys, Chainalysis, Fireblocks, Polygon, Hyperledger, R3 Corda, Hedera |
| **Data Centre** | Equinix, Digital Realty, CyrusOne, Iron Mountain, NTT, STT GDC, Khazna |
| **Edge/AI Compute** | NVIDIA, Lambda Labs, CoreWeave, RunPod, Paperspace, FluidStack |
| **Industries** | Industry-specific: Banking (FIS, Temenos), Defence (Lockheed, Raytheon), Energy (Schneider, Siemens), Healthcare (Epic, Cerner) |

---

## Chunked Execution Plan (8 pages per chunk)

### Chunk 1: Extended Solutions — Core Infrastructure (8 pages)
1. `cloud.njk`
2. `edge-compute-infrastructure.njk`
3. `edge-ai-inference.njk`
4. `sovereign-compute.njk`
5. `managed-services.njk`
6. `disaster-recovery.njk`
7. `critical-infrastructure-consulting.njk`
8. `digital-workplace.njk`

### Chunk 2: Extended Solutions — Security & Identity (8 pages)
1. `network-security.njk`
2. `identity-access.njk`
3. `hardware-security.njk`
4. `post-quantum-security.njk`
5. `secure-edge-computing.njk`
6. `mobile-data-centre.njk`
7. `ota-fleet-management.njk`
8. `smart-building-edge.njk`

### Chunk 3: Extended Solutions — AI/Data/IoT + Consulting Sub-pages (8 pages)
1. `ai-compute.njk`
2. `ai-data-services.njk`
3. `application-services.njk`
4. `iot.njk`
5. `consulting/digital-transformation-strategy.njk`
6. `consulting/infrastructure-network-audits.njk`
7. `consulting/managed-services-outsourcing.njk`
8. `consulting/regulatory-compliance-advisory.njk`

### Chunk 4: Consulting Sub-pages + Industries Batch 1 (8 pages)
1. `consulting/technology-roadmap-vendor-selection.njk`
2. `consulting/tokenisation-advisory.njk`
2. `pages/industries/banking.njk`
3. `pages/industries/defence.njk`
4. `pages/industries/education.njk`
5. `pages/industries/energy.njk`
6. `pages/industries/government.njk`
7. `pages/industries/healthcare.njk`

### Chunk 5: Industries Batch 2 + Case Studies Batch 1 (8 pages)
1. `pages/industries/hospitality.njk`
2. `pages/industries/logistics.njk`
3. `pages/industries/maritime.njk`
4. `pages/industries/real-estate.njk`
5. `pages/industries/retail.njk`
6. `pages/industries/telecom.njk`
7. `pages/case-studies/banking-blockchain.njk`
8. `pages/case-studies/defence-sovereign-edge.njk`

### Chunk 6: Case Studies Batch 2 (8 pages)
1. `pages/case-studies/education-connected-campus.njk`
2. `pages/case-studies/energy-scada.njk`
3. `pages/case-studies/fleet-predictive-maintenance.njk`
4. `pages/case-studies/government-smart-city.njk`
5. `pages/case-studies/healthcare-uptime.njk`
8. `pages/case-studies/hospitality-guest-experience.njk`
9. `pages/case-studies/maritime-fleet-tracking.njk`
10. `pages/case-studies/real-estate-smart-tower.njk`

### Chunk 7: Case Studies Batch 3 + Insights Batch 1 (8 pages)
1. `pages/case-studies/retail-omnichannel.njk`
2. `pages/case-studies/telecom-edge.njk`
3. `pages/insights/ai-native-enterprise-transformation.njk`
4. `pages/insights/blockchain-trade-finance.njk`
5. `pages/insights/cloud-migration-strategy.njk`
6. `pages/insights/continuous-modernization.njk`
7. `pages/insights/cybersecurity-threat-landscape.njk`
8. `pages/insights/data-centre-trends.njk`

### Chunk 8: Insights Batch 2 + Company/Legal (8 pages)
1. `pages/insights/digital-transformation-mea.njk`
2. `pages/insights/edge-ai-fleet-management.njk`
3. `pages/insights/hybrid-cloud-default-architecture.njk`
4. `pages/insights/sd-wan-mea.njk`
5. `pages/insights/sovereign-compute-mea.njk`
6. `pages/insights/whitepapers.njk`
7. `pages/about.njk`
8. `pages/engagement-model.njk`

### Chunk 9: Remaining Company/Legal + Index Pages (6 pages)
1. `pages/careers.njk`
2. `pages/contact.njk`
3. `pages/faq.njk`
4. `pages/leadership.njk`
5. `pages/methodology.njk`
6. `pages/partners.njk`
7. `pages/privacy-policy.njk`
8. `pages/terms-of-service.njk`
9. Index pages: `index.njk`, `pages/solutions-index.njk`, `pages/industries-index.njk`, `pages/case-studies-index.njk`, `pages/insights/index.njk`

---

## Detailed Process Per Chunk

### Phase A: Firecrawl Research (Parallel, 30 min/chunk)
```bash
# For each solution domain, crawl 3-5 competitor/reference sites
firecrawl research --query "enterprise SD-WAN solutions architecture" --limit 5
firecrawl scrape --url "https://competitor.com/solutions/connectivity" --format markdown
# Output to research-data/firecrawl/<domain>/
```

### Phase B: LangChain Enhancement (Sequential per page, 45 min/page)
```bash
# LangGraph workflow: research-data/firecrawl/<domain>/extracted-content.md
# → analysis → fact-check → rebrand → enhanced-content.md
# Output to research-data/langchain/<domain>/
```

### Phase C: n8n Pipeline Execution (Automated, 15 min/chunk)
```bash
# Trigger n8n workflow: "meaicon-content-enhancement"
# Input: chunk definition (list of pages)
# Flow: Firecrawl → LangChain → inject-enhanced-content.py → validate
```

### Phase D: Master Orchestrator Verification (Per chunk, 30 min)
```bash
# 1. Validate all enhanced-content.md exist and pass quality gates
# 2. Run inject-enhanced-content.py for chunk pages
# 3. npm run build && npm run audit:metadata && npm run validate:content
# 4. Visual QA via Playwright (nev3s_visual_regression)
# 5. SEO audit (nev3s_seo_regression_check)
# 6. Link check (nev3s_link_checker)
# 7. Accessibility audit (nev3s_accessibility_audit)
# 8. Commit chunk: git add . && git commit -m "feat: enhance chunk N - <pages>"
# 9. Push: git push origin website-redesign
# 10. Verify GitHub Pages deployment
```

---

## Quality Gates (Per Page)

| Gate | Tool | Threshold |
|------|------|-----------|
| **Content Length** | Custom | 1,500-3,000 words per solution page |
| **SEO Title** | `audit:metadata` | 30-70 chars |
| **Meta Description** | `audit:metadata` | 120-160 chars |
| **Canonical URL** | `audit:metadata` | Matches permalink |
| **H1 Uniqueness** | `validate:content` | Exactly 1 per page |
| **Internal Links** | `nev3s_link_checker` | 0 broken, min 3 internal |
| **External Links** | `nev3s_link_checker` | 0 broken, rel="noopener" |
| **Images** | `nev3s_seo_audit_page` | All have alt, WebP, sized |
| **Accessibility** | `nev3s_accessibility_audit` | WCAG 2.1 AA, axe-core 0 violations |
| **Visual Regression** | `nev3s_visual_regression` | <1% pixel diff vs baseline |
| **Performance** | `nev3s_performance_budget` | LCP <2.5s, INP <200ms, CLS <0.1 |
| **Hallucination Check** | LangChain fact-checks | All claims verifiable |

---

## Skills & Tools to Install/Use

| Skill/Tool | Purpose | Status |
|------------|---------|--------|
| `firecrawl` | Crawling & extraction | ✅ Available |
| `meaicon-audit-orchestration` | Pipeline orchestration | ✅ Available |
| `research-web-content` | Competitor research | ✅ Available |
| `static-site-content-pipeline` | Static site build process | ✅ Available |
| `nev3s_seo_audit_page` | SEO validation | Need to load |
| `nev3s_link_checker` | Link validation | Need to load |
| `nev3s_visual_regression` | Visual QA | Need to load |
| `nev3s_accessibility_audit` | A11y validation | Need to load |
| `nev3s_performance_budget` | Core Web Vitals | Need to load |
| `n8n` (localhost:5678) | Workflow automation | ✅ Running |
| `langgraph` (v1.2.12) | LLM orchestration | ✅ Installed |

---

## Deployment Target

| Branch | Platform | Purpose |
|--------|----------|---------|
| `website-redesign` | GitHub Pages | **Active development & deployment target** |
| `main` | Cloudflare Pages | **Production — DO NOT TOUCH** |

**Deploy Command**: `git push origin website-redesign` → triggers GitHub Actions → GitHub Pages

---

## Success Criteria

- [ ] All 72 pages have enhanced, verified content
- [ ] Zero broken links (internal + external)
- [ ] 100% SEO metadata compliance
- [ ] WCAG 2.1 AA across all pages
- [ ] Visual regression <1% on all pages
- [ ] Core Web Vitals pass on all pages
- [ ] Zero hallucinated claims (all fact-checked)
- [ ] Consistent MEAICON brand voice throughout
- [ ] Clean git history on `website-redesign` with chunked commits
- [ ] Successful GitHub Pages deployment verified

---

## Immediate Next Actions

1. **Load required NEV3S QA skills** (`nev3s_seo_audit_page`, `nev3s_link_checker`, `nev3s_visual_regression`, `nev3s_accessibility_audit`, `nev3s_performance_budget`)
2. **Configure n8n workflow** "meaicon-content-enhancement" with Firecrawl → LangChain → inject → validate nodes
3. **Execute Chunk 1** (Extended Solutions — Core Infrastructure, 8 pages)
4. **Verify Chunk 1** with full QA suite
5. **Commit & deploy Chunk 1**
6. **Repeat for Chunks 2-9**

---

*Plan created: 2026-09-28 | Branch: website-redesign | Orchestrator: meaicon-audit-orchestration*