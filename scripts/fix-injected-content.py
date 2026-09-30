#!/usr/bin/env python
"""Fix all .njk pages that have raw markdown injected by inject-enhanced-content.py.

Strips old injected markdown, converts it to HTML via Python markdown lib,
wraps it in proper semantic sections, and re-injects before </main>.
"""

import re
import os
from pathlib import Path
import markdown as md_lib

REPO_ROOT = Path("C:/Users/nev3s/repos/meaicon-website")
PAGES_DIR = REPO_ROOT / "pages"

MARKER_RE = r'<!-- enhanced-content-injected: enhanced-content\.md[^>]*-->'


def is_html(content: str) -> bool:
    """Check if content is already HTML."""
    return any(tag in content for tag in ['<h1', '<h2', '<h3', '<p>', '<ul', '<table', '<section'])


def html_to_markdown(html: str) -> str:
    """Convert HTML back to markdown for re-processing."""
    # Remove wrapper divs/sections
    html = re.sub(r'<section class="content-section reveal">\s*<div[^>]*>\s*<div class="prose-content">\s*', '', html)
    html = re.sub(r'\s*</div>\s*</div>\s*</section>\s*$', '', html)
    # H1-H3
    html = re.sub(r'<h([1-3])[^>]*>(.*?)</h\1>', lambda m: '#' * int(m.group(1)) + ' ' + m.group(2), html)
    # Bold
    html = re.sub(r'<strong>(.*?)</strong>', r'**\1**', html)
    html = re.sub(r'<b>(.*?)</b>', r'**\1**', html)
    # Links
    html = re.sub(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', r'[\2](\1)', html)
    # List items
    html = re.sub(r'<li>(.*?)</li>', r'- \1', html)
    # Unordered/ordered lists
    html = re.sub(r'</?[uo]l>', '', html)
    # Paragraphs
    html = re.sub(r'<p>(.*?)</p>', r'\1\n', html)
    html = re.sub(r'<p[^>]*>', '', html)
    # Tables
    html = re.sub(r'<table[^>]*>', '', html)
    html = re.sub(r'</table>', '', html)
    html = re.sub(r'<thead[^>]*>.*?</thead>', '', html, flags=re.DOTALL)
    # Line breaks
    html = re.sub(r'<br\s*/?>', '\n', html)
    # Remove hr tags (from --- separators)
    html = re.sub(r'<hr\s*/?>', '', html)
    # Remove remaining tags
    html = re.sub(r'</?div[^>]*>', '', html)
    html = re.sub(r'</?span[^>]*>', '', html)
    html = re.sub(r'</?em>', '*', html)
    return html.strip()

def strip_old_injection(content: str) -> tuple[str, str | None]:
    """Remove old injected content between marker and </main>.
    Returns (cleaned_content, old_content_or_None)."""
    match = re.search(MARKER_RE, content)
    if not match:
        return content, None

    idx = match.start()
    main_idx = content.rfind('</main>')
    if main_idx == -1:
        return content, None

    old_block = content[idx:main_idx]
    lines = old_block.split('\n')
    md_lines = []
    past_marker = False
    for line in lines:
        if re.match(r'<!-- enhanced-content-injected', line):
            past_marker = True
            continue
        if past_marker:
            md_lines.append(line)

    old_markdown = '\n'.join(md_lines).strip()

    # If the old content is already HTML (from previous fix), strip HTML wrapper
    if '<section class="content-section reveal">' in old_markdown:
        inner = re.sub(r'^\s*<section class="content-section reveal">\s*<div[^>]*>\s*<div class="prose-content">\s*', '', old_markdown)
        inner = re.sub(r'\s*</div>\s*</div>\s*</section>\s*$', '', inner)
        old_markdown = inner.strip()

    cleaned = content[:idx] + '</main>' + content[main_idx + len('</main>'):]
    return cleaned, old_markdown


def markdown_to_html(md: str) -> str:
    """Convert markdown to styled HTML matching the site's design system."""
    # Sanitize: strip metadata, frontmatter, enforce NO H1 (page already has one)
    lines = md.split('\n')
    cleaned = []
    in_frontmatter = False
    for line in lines:
        stripped = line.strip()
        # Skip YAML frontmatter blocks
        if stripped == '---' and len(cleaned) == 0:
            in_frontmatter = True
            continue
        if in_frontmatter:
            if stripped == '---':
                in_frontmatter = False
            continue
        # Skip YAML-style key: value lines
        if re.match(r'^(title|description|layout|permalink|canonical|ogTitle|ogDescription|ogImage)\s*:', stripped, re.IGNORECASE):
            continue
        # Skip metadata field lines (markdown bold format, optionally as list items)
        if re.match(r'^-?\s*\*\*(Title|Description|Canonical|Permalink|Section\s+title|Canonical\s+URL|OG\s+Title|OG\s+Description)\s*:', stripped, re.IGNORECASE):
            continue
        # Skip raw separator lines (--- becomes <hr>)
        if stripped == '---':
            continue
        # Skip lines that are just '---' with extra dashes
        if re.match(r'^-{3,}$', stripped):
            continue
        # Enforce NO H1 — convert all H1 to H2
        if stripped.startswith('# ') and not stripped.startswith('## '):
            line = line.replace('# ', '## ', 1)
        # Skip empty lines at start
        if not stripped and len(cleaned) == 0:
            continue
        cleaned.append(line.rstrip())

    md = '\n'.join(cleaned).strip()

    # Convert markdown to HTML
    html = md_lib.markdown(md, extensions=['tables', 'fenced_code', 'toc'])
    # Remove any hr tags that survived
    html = re.sub(r'<hr\s*/?>', '', html)
    # Remove empty sections that might result from stripping
    html = re.sub(r'<section[^>]*>\s*</section>', '', html)

    # Wrap in a content-section with prose-content
    wrapped = f'''
  <section class="content-section reveal">
    <div class="max-w-7xl mx-auto px-4 lg:px-6">
      <div class="prose-content">
{html}
      </div>
    </div>
  </section>
'''
    return wrapped


def fix_page(page_path: Path):
    """Fix a single .njk page."""
    content = page_path.read_text(encoding="utf-8")

    if not re.search(MARKER_RE, content):
        return False, "no_marker"

    cleaned, old_md = strip_old_injection(content)
    if not old_md or not old_md.strip():
        return False, "empty_old_content"

    # If old content is already HTML (from previous fix), convert back to markdown
    if is_html(old_md):
        md = html_to_markdown(old_md)
    else:
        md = old_md

    # Convert markdown to HTML
    html_block = markdown_to_html(md)

    # Re-inject as HTML before </main>
    new_marker = f"<!-- enhanced-content-injected: enhanced-content.md (html-converted) -->"
    updated = cleaned.replace(
        "</main>",
        f"{new_marker}\n{html_block}\n\n</main>"
    )

    page_path.write_text(updated, encoding="utf-8")
    return True, f"fixed ({len(html_block)} chars HTML)"


def main():
    print("=" * 60)
    print("Fixing injected content: markdown -> HTML conversion")
    print("=" * 60)

    fixed = 0
    skipped = 0
    errors = 0

    # Find all .njk files with the marker
    for page_path in sorted(PAGES_DIR.rglob("*.njk")):
        content = page_path.read_text(encoding="utf-8")
        if not re.search(MARKER_RE, content):
            continue

        success, reason = fix_page(page_path)
        rel = page_path.relative_to(PAGES_DIR)
        if success:
            print(f"  ✅ {rel}: {reason}")
            fixed += 1
        else:
            print(f"  ⏭️  {rel}: {reason}")
            skipped += 1

    print(f"\n{'=' * 60}")
    print(f"Summary: {fixed} fixed, {skipped} skipped, {fixed + skipped} total")


if __name__ == "__main__":
    main()
