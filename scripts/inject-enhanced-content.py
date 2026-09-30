#!/usr/bin/env python
"""Inject enhanced content into solution page templates. Inserts enhanced-content.md before </main> in each .njk template.

SANITIZATION: Strips code fences, enforces single H1, removes raw research notes before injection.
"""

import re
import json
from pathlib import Path

REPO_ROOT = Path("C:/Users/nev3s/repos/meaicon-website")
PROGRESS_FILE = REPO_ROOT / "research-data" / "progress.json"
ENHANCED_DIR = REPO_ROOT / "research-data" / "langchain"
PAGES_DIR = REPO_ROOT / "pages"

INJECTION_MAP = {
    # Core Solutions (pages/solutions/)
    "solutions/connectivity.njk": "connectivity/enhanced-content.md",
    "solutions/cyber-security.njk": "cyber-security/enhanced-content.md",
    "solutions/consulting.njk": "consulting/enhanced-content.md",
    "solutions/blockchain.njk": "blockchain/enhanced-content.md",
    "solutions/data-centre.njk": "data-centre/enhanced-content.md",
    "solutions/cloud.njk": "cloud/enhanced-content.md",
    "solutions/edge-compute-infrastructure.njk": "edge-compute-infrastructure/enhanced-content.md",
    "solutions/edge-ai-inference.njk": "edge-ai-inference/enhanced-content.md",
    "solutions/sovereign-compute.njk": "sovereign-compute/enhanced-content.md",
    "solutions/managed-services.njk": "managed-services/enhanced-content.md",
    "solutions/disaster-recovery.njk": "disaster-recovery/enhanced-content.md",
    "solutions/critical-infrastructure-consulting.njk": "critical-infrastructure-consulting/enhanced-content.md",
    "solutions/digital-workplace.njk": "digital-workplace/enhanced-content.md",
    "solutions/network-security.njk": "network-security/enhanced-content.md",
    "solutions/identity-access.njk": "identity-access/enhanced-content.md",
    "solutions/hardware-security.njk": "hardware-security/enhanced-content.md",
    "solutions/post-quantum-security.njk": "post-quantum-security/enhanced-content.md",
    "solutions/secure-edge-computing.njk": "secure-edge-computing/enhanced-content.md",
    "solutions/mobile-data-centre.njk": "mobile-data-centre/enhanced-content.md",
    "solutions/ota-fleet-management.njk": "ota-fleet-management/enhanced-content.md",
    "solutions/smart-building-edge.njk": "smart-building-edge/enhanced-content.md",
    "solutions/ai-compute.njk": "ai-compute/enhanced-content.md",
    "solutions/ai-data-services.njk": "ai-data-services/enhanced-content.md",
    "solutions/application-services.njk": "application-services/enhanced-content.md",
    "solutions/iot.njk": "iot/enhanced-content.md",
    # Consulting sub-pages
    "solutions/consulting/digital-transformation-strategy.njk": "consulting/digital-transformation-strategy/enhanced-content.md",
    "solutions/consulting/infrastructure-network-audits.njk": "consulting/infrastructure-network-audits/enhanced-content.md",
    "solutions/consulting/managed-services-outsourcing.njk": "consulting/managed-services-outsourcing/enhanced-content.md",
    "solutions/consulting/regulatory-compliance-advisory.njk": "consulting/regulatory-compliance-advisory/enhanced-content.md",
    "solutions/consulting/technology-roadmap-vendor-selection.njk": "consulting/technology-roadmap-vendor-selection/enhanced-content.md",
    "solutions/consulting/tokenisation-advisory.njk": "consulting/tokenisation-advisory/enhanced-content.md",
    # Industries
    "industries/banking.njk": "industries/banking/enhanced-content.md",
    "industries/defence.njk": "industries/defence/enhanced-content.md",
    "industries/education.njk": "industries/education/enhanced-content.md",
    "industries/energy.njk": "industries/energy/enhanced-content.md",
    "industries/government.njk": "industries/government/enhanced-content.md",
    "industries/healthcare.njk": "industries/healthcare/enhanced-content.md",
    "industries/hospitality.njk": "industries/hospitality/enhanced-content.md",
    "industries/logistics.njk": "industries/logistics/enhanced-content.md",
    "industries/maritime.njk": "industries/maritime/enhanced-content.md",
    "industries/real-estate.njk": "industries/real-estate/enhanced-content.md",
    "industries/retail.njk": "industries/retail/enhanced-content.md",
    "industries/telecom.njk": "industries/telecom/enhanced-content.md",
    # Case Studies
    "case-studies/banking-blockchain.njk": "case-studies/banking-blockchain/enhanced-content.md",
    "case-studies/defence-sovereign-edge.njk": "case-studies/defence-sovereign-edge/enhanced-content.md",
    "case-studies/education-connected-campus.njk": "case-studies/education-connected-campus/enhanced-content.md",
    "case-studies/energy-scada.njk": "case-studies/energy-scada/enhanced-content.md",
    "case-studies/fleet-predictive-maintenance.njk": "case-studies/fleet-predictive-maintenance/enhanced-content.md",
    "case-studies/government-smart-city.njk": "case-studies/government-smart-city/enhanced-content.md",
    "case-studies/healthcare-uptime.njk": "case-studies/healthcare-uptime/enhanced-content.md",
    "case-studies/hospitality-guest-experience.njk": "case-studies/hospitality-guest-experience/enhanced-content.md",
    "case-studies/maritime-fleet-tracking.njk": "case-studies/maritime-fleet-tracking/enhanced-content.md",
    "case-studies/real-estate-smart-tower.njk": "case-studies/real-estate-smart-tower/enhanced-content.md",
    "case-studies/retail-omnichannel.njk": "case-studies/retail-omnichannel/enhanced-content.md",
    "case-studies/telecom-edge.njk": "case-studies/telecom-edge/enhanced-content.md",
    # Index pages
    "case-studies-index.njk": "case-studies-index/enhanced-content.md",
    "industries-index.njk": "industries-index/enhanced-content.md",
    "insights-index.njk": "insights-index/enhanced-content.md",
    # Insights
    "insights/ai-native-enterprise-transformation.njk": "insights/ai-native-enterprise-transformation/enhanced-content.md",
    "insights/blockchain-trade-finance.njk": "insights/blockchain-trade-finance/enhanced-content.md",
    "insights/case-studies.njk": "insights/case-studies/enhanced-content.md",
    "insights/cloud-migration-strategy.njk": "insights/cloud-migration-strategy/enhanced-content.md",
    "insights/continuous-modernization.njk": "insights/continuous-modernization/enhanced-content.md",
    "insights/cybersecurity-threat-landscape.njk": "insights/cybersecurity-threat-landscape/enhanced-content.md",
    "insights/data-centre-trends.njk": "insights/data-centre-trends/enhanced-content.md",
    "insights/digital-transformation-mea.njk": "insights/digital-transformation-mea/enhanced-content.md",
    "insights/edge-ai-fleet-management.njk": "insights/edge-ai-fleet-management/enhanced-content.md",
    "insights/hybrid-cloud-default-architecture.njk": "insights/hybrid-cloud-default-architecture/enhanced-content.md",
    "insights/index.njk": "insights/index/enhanced-content.md",
        "insights/sd-wan-mea.njk": "insights/sd-wan-mea/enhanced-content.md",
    "insights/sovereign-compute-mea.njk": "insights/sovereign-compute-mea/enhanced-content.md",
    "insights/whitepapers.njk": "insights/whitepapers/enhanced-content.md",
}

def sanitize_content(content: str) -> str:
    """Sanitize enhanced content before injection into templates.

    - Strips markdown code fences that would render as raw text in HTML
    - Enforces single H1: converts any H1 after the first to H2
    - Removes raw research notes (metadata-like lines)
    - Strips trailing whitespace per line
    """
    # Strip code fences (```...``` blocks)
    content = re.sub(r'```[a-zA-Z]*\n.*?```', '', content, flags=re.DOTALL)
    content = re.sub(r'```', '', content)

    lines = content.split('\n')
    cleaned_lines = []
    h1_count = 0
    for line in lines:
        stripped = line.strip()

        # Enforce single H1: convert subsequent H1s to H2
        if stripped.startswith('# ') and not stripped.startswith('## '):
            h1_count += 1
            if h1_count > 1:
                line = line.replace('# ', '## ', 1)

        # Skip raw separator lines (---) in body content
        if stripped == '---' and len(cleaned_lines) > 0:
            continue

        # Skip metadata-like lines
        if re.match(r'^(Source|Research|URL|Reference|Metadata|Fact-check)\s*:', stripped, re.IGNORECASE):
            continue

        cleaned_lines.append(line.rstrip())

    return '\n'.join(cleaned_lines).strip()


def inject(template_path: Path, enhanced_path: Path):
    """Inject sanitized enhanced content into a template."""
    if not enhanced_path.exists():
        print(f"SKIP: {enhanced_path} not found")
        return False, "missing_enhanced"

    original = template_path.read_text(encoding="utf-8")
    raw_enhanced = enhanced_path.read_text(encoding="utf-8")

    # SANITIZE before injection
    enhanced = sanitize_content(raw_enhanced)

    if not enhanced.strip():
        print(f"SKIP: {enhanced_path} empty after sanitization")
        return False, "empty_after_sanitize"

    # Prevent double-injection with a marker comment
    marker = f"<!-- enhanced-content-injected: {enhanced_path.name} -->"
    if marker in original:
        print(f"SKIP: {template_path.name} already injected")
        return False, "already_injected"

    if "</main>" in original:
        updated = original.replace("</main>", f"{marker}\n{enhanced}\n\n</main>")
    else:
        updated = original + f"\n{marker}\n{enhanced}\n"

    template_path.write_text(updated, encoding="utf-8")
    print(f"OK: {template_path.name} ({len(enhanced)} chars injected)")
    return True, "injected"


def main():
    print("=" * 60)
    print("Enhanced Content Injection (with sanitization)")
    print("=" * 60)

    # Load or init progress tracking
    if PROGRESS_FILE.exists():
        progress = json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
    else:
        progress = {"pages": {}}

    updated = 0
    skipped = 0
    for tmpl, enh in INJECTION_MAP.items():
        template_path = PAGES_DIR / tmpl
        enhanced_path = ENHANCED_DIR / enh

        if not template_path.exists():
            print(f"SKIP: {tmpl} template not found")
            progress["pages"][tmpl] = {"status": "template_missing"}
            continue

        success, reason = inject(template_path, enhanced_path)

        progress["pages"][tmpl] = {
            "status": "injected" if success else reason,
            "enhanced_source": enh,
        }

        if success:
            updated += 1
        else:
            skipped += 1

    progress["injection_summary"] = {
        "injected": updated,
        "skipped": skipped,
        "total": len(INJECTION_MAP),
    }

    # Save progress
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2), encoding="utf-8")

    print(f"\n{'=' * 60}")
    print(f"Summary: {updated} injected, {skipped} skipped, {len(INJECTION_MAP)} total")
    print(f"Progress saved to: {PROGRESS_FILE}")


if __name__ == "__main__":
    main()
