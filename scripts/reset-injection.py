#!/usr/bin/env python
"""Reset injection markers from all .njk templates so they can be re-injected."""
import re
from pathlib import Path

PAGES_DIR = Path("C:/Users/nev3s/repos/meaicon-website/pages")

count = 0
for njk_file in PAGES_DIR.rglob("*.njk"):
    content = njk_file.read_text(encoding="utf-8")
    if "enhanced-content-injected" in content:
        # Remove everything from the marker comment to </main> (exclusive)
        # But keep the </main> tag
        pattern = r'<!-- enhanced-content-injected.*?-->\s*.*?(?=</main>)'
        cleaned = re.sub(pattern, '', content, flags=re.DOTALL)
        if cleaned != content:
            njk_file.write_text(cleaned, encoding="utf-8")
            count += 1
            print(f"Reset: {njk_file.name}")

print(f"\nReset {count} templates. Ready for re-injection.")
