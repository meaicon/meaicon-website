# MEAICON Website Content Enhancement Pipeline

## Overview
This document tracks the content enhancement pipeline for the MEAICON website redesign.
The pipeline uses Firecrawl for web research, LangChain for AI-powered content enhancement,
and n8n for workflow automation.

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MEAICON CONTENT ENHANCEMENT PIPELINE                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌────────────┐ │
│  │  Firecrawl   │    │  LangChain   │    │  Content    │    │   n8n      │ │
│  │  Agent       │───▶│  Agent       │───▶│  Agent      │───▶│  Workflow  │ │
│  │              │    │              │    │              │    │            │ │
│  │ • Scrape     │    │ • Enhance    │    │ • Rebrand    │    │ • Trigger  │ │
│  │ • Search     │    │ • Fact-check │    │ • Polish     │    │ • Schedule │ │
│  │ • Research   │    │ • Analyze    │    │ • Template   │    │ • Notify   │ │
│  │ • Extract    │    │ • Summarize  │    │ • SEO        │    │ • Monitor   │ │
│  └─────────────┘    └──────────────┘    └─────────────┘    └────────────┘ │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                    ORCHESTRATOR AGENT (Master)                       │  │
│  │  Coordinates all agents, verifies handoffs, tracks pipeline status   │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Agent Profile Assignments

| Profile | Role | Tool/Technology | Status |
|---------|------|-----------------|--------|
| `meaicon-firecrawl` | Research & extraction | Firecrawl CLI | ✅ Active |
| `meaicon-langchain` | Content enhancement & synthesis | LangChain 1.4.2 (Python) | ✅ Active |
| `meaicon-n8n` | Workflow automation & pipeline | n8n v2.40.7 | ✅ Active |
| `meaicon-orchestrator` | Master coordination & verification | Hermes Agent | ✅ Active |
| `meaicon-content` | Rebranding & template integration | Hermes Agent | ✅ Active |
| `meaicon-dev` | UI/UX, CSS, Eleventy build | Hermes Agent | ✅ Active |
| `meaicon-qa` | Validation, SEO, a11y, hallucination check | Hermes Agent | ✅ Active |

## Data Flow

### Stage 1: Firecrawl Research (meaicon-firecrawl)
**Input**: Research topics (MEAICON services, industry trends)
**Process**: 
- `firecrawl scrape <url> --format markdown` — Scrape MEAICON live site
- `firecrawl search "<query>" --limit 5` — Search for related content
- `firecrawl research "<query>" --depth deep` — Deep research on topics
**Output**: `research-data/firecrawl/<topic>/`
- `extracted-content.md` — Cleaned scraped content
- `research-search.md` — Search results
- `metadata.json` — Source metadata
- `sources.json` — Source URLs

### Stage 2: LangChain Enhancement (meaicon-langchain)
**Input**: `research-data/firecrawl/<topic>/extracted-content.md`
**Process**: 
- LangChain ChatOpenAI via OmniRoute (localhost:20128)
- Content enhancement with ENHANCE_SYSTEM_PROMPT
- Fact-checking with FACT_CHECK_SYSTEM_PROMPT
- Content analysis with ANALYSIS_SYSTEM_PROMPT
- Executive summary with SUMMARY_SYSTEM_PROMPT
**Output**: `research-data/langchain/<topic>/`
- `enhanced-content.md` — Enhanced content with [ENHANCED] sections
- `fact-checks.json` — Fact verification results
- `content-analysis.json` — Quality analysis and recommendations
- `summary.md` — Executive summary

### Stage 3: Content Rebranding (meaicon-content)
**Input**: `research-data/langchain/<topic>/enhanced-content.md`
**Process**: 
- Rebrand to MEAICON voice (professional, authoritative, MEA-focused)
- Remove all source references
- Place into Nunjucks templates
- SEO optimization (title, meta, canonical, OG tags)
**Output**: `migrated/<page-name>.njk`

### Stage 4: Development (meaicon-dev)
**Input**: `migrated/*.njk`
**Process**: 
- Build Eleventy templates
- Apply Tailwind CSS design system
- Optimize for performance
- Deploy to Cloudflare Pages
**Output**: `_site/` (built HTML)

### Stage 5: QA Validation (meaicon-qa)
**Input**: `_site/` (built HTML)
**Process**: 
- Build validation: `npm run build`
- Content validation: `npm run validate:content`
- Metadata audit: `npm run audit:metadata`
- Source reference scan
- Link checking
- Brand compliance check
- Accessibility audit
- Hallucination check
**Output**: `qa-reports/<date>-qa-report.md`

## n8n Workflow

### Workflow: MEAICON Content Enhancement Pipeline
**Import**: `scripts/n8n/meaicon-content-enhancement.json`

### Workflow Nodes:
1. **Manual Trigger** — Start pipeline manually or via cron
2. **Firecrawl Research** — HTTP Request to Firecrawl webhook
3. **LangChain Enhance** — Execute Command: `python scripts/langchain-enhance.py`
4. **Content Rebrand (OmniRoute LLM)** — HTTP Request to OmniRoute LLM
5. **Write content.md** — Write binary file to `research-data/content.md`
6. **Pipeline Status** — Function node for status tracking

### n8n Configuration:
- URL: http://localhost:5678
- API key: ~/.n8n/api-key.txt
- Start: ~/.n8n/start-n8n.sh
- N8N_SECURE_COOKIE=false
- OmniRoute via HTTP Request node → 127.0.0.1:20128/v1/chat/completions
- Native OpenAI node has 401 issues — HTTP Request is reliable

## Scripts

### Firecrawl Snapshot
```bash
# Full site snapshot
python scripts/firecrawl-snapshot.py

# Single page
python scripts/firecrawl-snapshot.py --page connectivity

# With research searches
python scripts/firecrawl-snapshot.py --research
```

### LangChain Enhancement
```bash
# Enhance a single topic
python scripts/langchain-enhance.py --topic "connectivity" --page-name connectivity --input-dir research-data/firecrawl/connectivity
```

## Research Topics (MEAICON Services)

### 1. Connectivity
- SD-WAN, MPLS, satellite communication
- Subsea cable systems serving MEA
- 5G and edge networking
- Network as a Service (NaaS)
- Last-mile connectivity in remote areas

### 2. Data Centre
- Colocation and managed hosting
- Edge data centres
- Sovereign data centres (data residency)
- Green/energy-efficient data centres
- MEA data centre market trends

### 3. Cyber Security
- Security Operations Centre (SOC)
- Managed Security Service Provider (MSSP)
- Zero-trust architecture
- OT/ICS security
- Compliance: NCA (Saudi), DIFC (Dubai), ADGM (Abu Dhabi)

### 4. Blockchain
- Distributed Ledger Technology (DLT)
- Smart contracts
- Central Bank Digital Currency (CBDC)
- Asset tokenization
- DeFi in MEA regulatory environment

### 5. Consulting
- Digital transformation strategy
- IT strategy and planning
- Cloud migration
- Managed services
- MEA market entry and expansion

## Verification Checklist

### Pipeline Verification
- [ ] Firecrawl snapshot completed for all 25+ pages
- [ ] LangChain enhancement completed for all 5 service topics
- [ ] Content rebranding completed for all pages
- [ ] Eleventy build passes clean
- [ ] Content validation passes
- [ ] Metadata audit passes
- [ ] No source references in built HTML
- [ ] All internal links resolve
- [ ] Brand compliance verified
- [ ] Accessibility audit passes
- [ ] Hallucination check passes

### Cross-Verification
- [ ] n8n workflow imports and executes
- [ ] LangChain script runs with OmniRoute LLM
- [ ] Firecrawl CLI scrapes MEAICON live site
- [ ] All profiles have correct SOUL.md and MEMORY.md
- [ ] Pipeline handoffs produce verifiable artifacts

## Status Tracking

| Stage | Status | Last Run | Artifacts |
|-------|--------|----------|-----------|
| Firecrawl Snapshot | ⏳ Pending | — | research-data/firecrawl/snapshot/ |
| LangChain Enhancement | ⏳ Pending | — | research-data/langchain/ |
| Content Rebranding | ⏳ Pending | — | migrated/ |
| Dev Build | ⏳ Pending | — | _site/ |
| QA Validation | ⏳ Pending | — | qa-reports/ |

---

*Last updated: 2026-09-28*
*Pipeline version: 1.0*
