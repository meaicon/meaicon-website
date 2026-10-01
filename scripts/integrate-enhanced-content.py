#!/usr/bin/env python
"""Integrate enhanced content into existing page sections properly.

Removes the appended 'enhanced-content-injected' section and merges
worthwhile enhanced material into appropriate existing sections:
- Overview, Capabilities, Delivery approach, Why MEAICON, Related Solutions
"""

import re
import os
from pathlib import Path
import markdown as md_lib

REPO_ROOT = Path(r"C:/Users/nev3s/repos/meaicon-website")
PAGES_DIR = REPO_ROOT / "pages"
ENHANCED_DIR = REPO_ROOT / "research-data" / "langchain"

# Load injection map from inject script
with open(REPO_ROOT / "scripts" / "inject-enhanced-content.py", "r") as f:
    inject_content = f.read()

match = re.search(r'INJECTION_MAP\s*=\s*(\{.*?\})', inject_content, re.DOTALL)
INJECTION_MAP = eval(match.group(1))

# Map page types to their enhanced content file patterns
def get_enhanced_file(page_path: str) -> Path:
    """Get enhanced content file for a page."""
    if page_path in INJECTION_MAP:
        return ENHANCED_DIR / INJECTION_MAP[page_path]
    return None

def read_enhanced_content(enhanced_file: Path) -> dict:
    """Parse enhanced content markdown into sections."""
    if not enhanced_file or not enhanced_file.exists():
        return {}
    
    with open(enhanced_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove the initial blockquote and title
    content = re.sub(r'^# .*?\n>.*?\n', '', content, flags=re.DOTALL)
    
    # Split by ## and ### headers
    sections = {}
    current_section = None
    current_content = []
    
    for line in content.split('\n'):
        h2_match = re.match(r'^##\s+(.+)$', line)
        h3_match = re.match(r'^###\s+(.+)$', line)
        
        if h2_match:
            if current_section:
                sections[current_section] = '\n'.join(current_content).strip()
            current_section = h2_match.group(1).strip()
            current_content = []
        elif h3_match:
            if current_section:
                sections[current_section] = '\n'.join(current_content).strip()
            current_section = h3_match.group(1).strip()
            current_content = []
        else:
            current_content.append(line)
    
    if current_section:
        sections[current_section] = '\n'.join(current_content).strip()
    
    # Clean up section names (remove [ENHANCED] prefix)
    cleaned = {}
    for k, v in sections.items():
        clean_key = re.sub(r'^\[ENHANCED\]\s*', '', k).strip()
        cleaned[clean_key] = v
    
    return cleaned

def clean_enhanced_text(text: str) -> str:
    """Remove editorial artifacts from enhanced content."""
    if not text:
        return ""
    
    # Remove citation brackets like 【1】, 【2】, etc.
    text = re.sub(r'【\d+】', '', text)
    
    # Remove "Sources" section
    text = re.sub(r'\n\s*##?\s*Sources\s*\n.*?(?=\n##?|\Z)', '', text, flags=re.DOTALL)
    text = re.sub(r'\n\s*Sources\s*\n.*?(?=\n##?|\Z)', '', text, flags=re.DOTALL)
    
    # Remove "Further Research & Knowledge Gaps" section
    text = re.sub(r'\n\s*##?\s*Further Research.*?(?=\n##?|\Z)', '', text, flags=re.DOTALL)
    
    # Fix awkward phrases
    text = text.replace('the our region', 'the region')
    text = text.replace('our our region', 'our region')
    text = text.replace('across the the', 'across the')
    text = text.replace('MEA region', 'the region')
    text = text.replace('across MEA', 'across the region')
    
    # Remove [ENHANCED] labels
    text = re.sub(r'\[ENHANCED\]\s*', '', text)
    
    # Remove markdown bold from headers that shouldn't be bold
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    
    # Clean up multiple blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()

def convert_md_to_html(md_text: str) -> str:
    """Convert markdown to HTML."""
    if not md_text:
        return ""
    html = md_lib.markdown(md_text, extensions=['tables', 'fenced_code'])
    return html

def find_injected_section(page_content: str) -> tuple:
    """Find the injected section and return (start_pos, end_pos, before_marker, after_main)."""
    marker_pattern = r'<!--\s*enhanced-content-injected: enhanced-content\.md \(html-converted\)\s*-->'
    marker_match = re.search(marker_pattern, page_content)
    
    if not marker_match:
        return None
    
    marker_start = marker_match.start()
    marker_end = marker_match.end()
    
    # Find the closing </main> after the marker
    main_end = page_content.find('</main>', marker_end)
    if main_end == -1:
        return None
    
    # Find the section that wraps the injected content
    # Look backwards from marker to find the start of the section
    section_start = page_content.rfind('<section', 0, marker_start)
    if section_start == -1:
        section_start = marker_start
    
    # Find the closing </section> before </main>
    # The injected content is wrapped in <section class="content-section reveal">...</section>
    injected_section_end = page_content.rfind('</section>', marker_end, main_end)
    if injected_section_end == -1:
        injected_section_end = main_end
    else:
        injected_section_end += len('</section>')
    
    return (section_start, injected_section_end, page_content[:section_start], page_content[main_end:])

def integrate_into_existing_sections(page_content: str, enhanced_sections: dict) -> str:
    """Integrate enhanced content into existing page sections."""
    
    # Map enhanced section names to existing page section headers
    section_mapping = {
        # Solution pages
        'Overview': ['Defensive and offensive security, end to end', 'Overview', 'What we deliver'],
        'Capabilities': ['What we deliver', 'Capabilities', 'Core capabilities'],
        'Delivery approach': ['Delivery approach', 'How we deliver', 'Our approach'],
        'Continuous Improvement Loop': ['Delivery approach', 'Continuous Improvement'],
        'Why MEAICON': ['Why choose us', 'Why MEAICON', 'Our differentiators'],
        'Competitive Differentiators': ['Why choose us', 'Why MEAICON'],
        'Related Solutions': ['Related Solutions'],
        
        # Case study pages
        'The challenge': ['What the client needed', 'The challenge'],
        'How we engaged': ['How we engaged', 'Our approach'],
        'What we delivered': ['What we delivered', 'What we built'],
        'What changed': ['What changed', 'Results'],
        'More work': ['More work', 'Next steps'],
        
        # Industry pages
        'Sector challenges': ['Financial services demand uncompromising security and traceability', 'Sector challenges'],
        'Solutions for banking and finance': ['Solutions for banking and finance', 'Our solutions'],
        'Our approach': ['Our approach'],
        'Where MEAICON infrastructure makes the difference': ['Where MEAICON infrastructure makes the difference', 'Differentiators'],
        'Sector scenarios & case studies': ['Sector scenarios & case studies', 'Case studies'],
        'Connected capabilities': ['Connected capabilities'],
        
        # Insight pages
        'What This Means for You': ['What This Means for You', 'Key Takeaways'],
    }
    
    for enh_section, enh_content in enhanced_sections.items():
        enh_content = clean_enhanced_text(enh_content)
        if not enh_content:
            continue
        
        enh_html = convert_md_to_html(enh_content)
        
        # Find target section in page
        targets = section_mapping.get(enh_section, [enh_section])
        inserted = False
        
        for target in targets:
            # Look for the section with this header
            pattern = rf'(<h2[^>]*>\s*{re.escape(target)}\s*</h2>)'
            match = re.search(pattern, page_content, re.IGNORECASE)
            if match:
                # Insert after the header, before the next content
                insert_pos = match.end()
                # Find a good insertion point - after the header, before next tag
                page_content = page_content[:insert_pos] + '\n<div class="prose-content">\n' + enh_html + '\n</div>\n' + page_content[insert_pos:]
                inserted = True
                break
        
        if not inserted:
            # Could not find target, skip this enhanced section
            pass
    
    return page_content

def process_page(page_rel_path: str) -> bool:
    """Process a single page."""
    page_path = PAGES_DIR / page_rel_path
    if not page_path.exists():
        print(f"  ⚠️ Page not found: {page_rel_path}")
        return False
    
    with open(page_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and remove injected section
    injected = find_injected_section(content)
    if not injected:
        print(f"  ⚠️ No injected section found: {page_rel_path}")
        return False
    
    start_pos, end_pos, before, after = injected
    clean_content = before + after
    
    # Get enhanced content
    enhanced_file = get_enhanced_file(page_rel_path)
    enhanced_sections = read_enhanced_content(enhanced_file)
    
    if enhanced_sections:
        # Integrate enhanced content into existing sections
        clean_content = integrate_into_existing_sections(clean_content, enhanced_sections)
    
    # Write back
    with open(page_path, 'w', encoding='utf-8') as f:
        f.write(clean_content)
    
    return True

def main():
    print("============================================================")
    print("Integrating enhanced content into existing page sections")
    print("============================================================\n")
    
    processed = 0
    failed = 0
    
    for page_rel in INJECTION_MAP.keys():
        print(f"Processing: {page_rel}")
        try:
            if process_page(page_rel):
                processed += 1
                print(f"  ✅ {page_rel}: integrated")
            else:
                failed += 1
                print(f"  ❌ {page_rel}: failed")
        except Exception as e:
            failed += 1
            print(f"  ❌ {page_rel}: error - {e}")
    
    print(f"\n============================================================")
    print(f"Summary: {processed} processed, {failed} failed")
    print("============================================================")

if __name__ == "__main__":
    main()