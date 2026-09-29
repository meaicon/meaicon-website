#!/usr/bin/env python
"""
Inject enhanced content into solution page templates.
Inserts enhanced-content.md before </main> in each .njk template.
"""

from pathlib import Path

REPO_ROOT = Path("C:/Users/nev3s/repos/meaicon-website")
ENHANCED_DIR = REPO_ROOT / "research-data" / "langchain"
TEMPLATE_DIR = REPO_ROOT / "pages" / "solutions"

INJECTION_MAP = {
    "connectivity.njk": "connectivity/enhanced-content.md",
    "cyber-security.njk": "cyber-security/enhanced-content.md",
    "consulting.njk": "consulting/enhanced-content.md",
    "blockchain.njk": "blockchain/enhanced-content.md",
    "data-centre.njk": "data-centre/enhanced-content.md",
    "cloud.njk": "cloud/enhanced-content.md",
    "edge-compute-infrastructure.njk": "edge-compute-infrastructure/enhanced-content.md",
    "edge-ai-inference.njk": "edge-ai-inference/enhanced-content.md",
    "sovereign-compute.njk": "sovereign-compute/enhanced-content.md",
    "managed-services.njk": "managed-services/enhanced-content.md",
    "disaster-recovery.njk": "disaster-recovery/enhanced-content.md",
    "critical-infrastructure-consulting.njk": "critical-infrastructure-consulting/enhanced-content.md",
    "digital-workplace.njk": "digital-workplace/enhanced-content.md",
    "network-security.njk": "network-security/enhanced-content.md",
    "identity-access.njk": "identity-access/enhanced-content.md",
    "hardware-security.njk": "hardware-security/enhanced-content.md",
    "post-quantum-security.njk": "post-quantum-security/enhanced-content.md",
    "secure-edge-computing.njk": "secure-edge-computing/enhanced-content.md",
    "mobile-data-centre.njk": "mobile-data-centre/enhanced-content.md",
    "ota-fleet-management.njk": "ota-fleet-management/enhanced-content.md",
    "smart-building-edge.njk": "smart-building-edge/enhanced-content.md",
}

def inject(template_path: Path, enhanced_path: Path):
    if not enhanced_path.exists():
        print(f"⚠️  Missing: {enhanced_path}")
        return False

    original = template_path.read_text()
    enhanced = enhanced_path.read_text()

    if "</main>" in original:
        updated = original.replace("</main>", enhanced + "\n\n</main>")
    else:
        updated = original + "\n\n" + enhanced

    template_path.write_text(updated)
    print(f"✅ {template_path.name}")
    return True

def main():
    print("=== Enhanced Content Injection ===\n")
    updated = 0
    for tmpl, enh in INJECTION_MAP.items():
        if inject(TEMPLATE_DIR / tmpl, ENHANCED_DIR / enh):
            updated += 1
    print(f"\n=== Summary: {updated} files updated ===")

if __name__ == "__main__":
    main()
