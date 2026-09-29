#!/usr/bin/env python3

import os
import re
from pathlib import Path

# Paths
repo_root = Path("C:/Users/nev3s/repos/meaicon-website")
solutions_dir = repo_root / "pages" / "solutions"
icons_svg_path = repo_root / "assets" / "icons.svg"

# Read existing icon IDs from icons.svg
with open(icons_svg_path, 'r', encoding='utf-8') as f:
    icons_content = f.read()

# Extract icon IDs using regex (id="icon-name")
icon_ids = set(re.findall(r'id="([^"]+)"', icons_content))
print(f"Found icon IDs: {sorted(icon_ids)}")

# Known IDs from the task description (to cross-check)
known_ids = {"connectivity", "data-centre", "cyber-security", "consulting", "blockchain"}
print(f"Known IDs: {known_ids}")

# Process each solution page
updated_count = 0
missing_icon_pages = []

for page_path in solutions_dir.glob("*.njk"):
    page_name = page_path.stem  # e.g., "connectivity"
    
    # Check if icon exists for this page
    if page_name in icon_ids:
        # Read the page content
        with open(page_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if icon is already present
        icon_tag = f'<svg class="solution-icon-sm"><use href="/assets/icons.svg#{page_name}"></use></svg>'
        if icon_tag not in content:
            # Find the h1 tag and insert icon before it
            # Look for the pattern: <h1 class="page-title">
            h1_pattern = r'(<h1[^>]*class="page-title"[^>]*>)'
            
            icon_line = f'      <svg class="solution-icon-sm"><use href="/assets/icons.svg#{page_name}"></use></svg>\n'
            
            def add_icon_before_h1(match):
                return icon_line + match.group(1)
            
            updated_count += 1
            new_content = re.sub(h1_pattern, add_icon_before_h1, content)

            # Write back if changed
            if new_content != content:
                with open(page_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"✓ Updated {page_name}.njk")
            else:
                print(f"- Already has icon: {page_name}.njk")
        else:
            print(f"- Icon already present: {page_name}.njk")
    else:
        # Icon doesn't exist - add to missing list
        missing_icon_pages.append(page_name)
        print(f"⚠ Missing icon for: {page_name}.njk")

print(f"\nSummary:")
print(f"Updated: {updated_count} pages")
print(f"Already had icons: pages that matched but already had them")
print(f"Missing icons: {len(missing_icon_pages)} pages")
if missing_icon_pages:
    print(f"  {', '.join(missing_icon_pages)}")