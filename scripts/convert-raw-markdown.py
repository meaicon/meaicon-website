#!/usr/bin/env python
"""Convert any raw markdown in .njk templates to HTML.

Targets raw markdown (##, ###, |, - **, etc.) that exists OUTSIDE the
enhanced-content-injected block — i.e., pre-existing markdown from earlier
injection attempts that was never converted to HTML.

Strategy: for each .njk file, find contiguous runs of raw markdown lines
(lines starting with ##, ###, -, *, |, >, 1., etc.) that are NOT inside
the <!-- enhanced-content-injected --> block, convert them to HTML using
Python's markdown library, and wrap in prose-content div.
"""
import re
from pathlib import Path
import markdown as md

PAGES_DIR = Path("C:/Users/nev3s/repos/meaicon-website/pages")

# Markdown line indicators
MD_LINE_RE = re.compile(r'^(#{1,6}\s|[-*+]\s|\d+\.\s|>\s||\||```|---|\*\*\s)')

def is_markdown_line(line):
    """Check if a line looks like markdown."""
    stripped = line.strip()
    if not stripped:
        return False
    # Headings
    if re.match(r'^#{1,6}\s', stripped):
        return True
    # List items
    if re.match(r'^[-*+]\s', stripped):
        return True
    # Numbered lists
    if re.match(r'^\d+\.\s', stripped):
        return True
    # Blockquotes
    if stripped.startswith('>'):
        return True
    # Table rows
    if stripped.startswith('|') and stripped.count('|') >= 2:
        return True
    # Table separator
    if re.match(r'^\|[-:\s|]+\|$', stripped):
        return True
    # Horizontal rule
    if stripped == '---':
        return True
    # Bold-only line (like **Key Trends**)
    if re.match(r'^\*\*[^*]+\*\*$', stripped):
        return True
    return False

def convert_raw_markdown_in_template(njk_path):
    """Find and convert raw markdown blocks in a .njk template to HTML."""
    content = njk_path.read_text(encoding='utf-8')
    lines = content.split('\n')

    # Find injection marker boundaries
    inject_start = None
    inject_end = None
    for i, line in enumerate(lines):
        if 'enhanced-content-injected' in line:
            inject_start = i
        if inject_start is not None and '</main>' in line:
            inject_end = i
            break

    # Find markdown blocks outside the injected section
    blocks = []  # list of (start_line, end_line, markdown_text)
    i = 0
    while i < len(lines):
        # Skip if inside injected section
        if inject_start is not None and inject_start <= i <= (inject_end or len(lines)):
            i += 1
            continue

        line = lines[i]
        if is_markdown_line(line):
            # Start of a markdown block
            block_start = i
            block_lines = []
            while i < len(lines):
                if inject_start is not None and inject_start <= i <= (inject_end or len(lines)):
                    break
                line = lines[i]
                if is_markdown_line(line) or line.strip() == '':
                    block_lines.append(line)
                    i += 1
                else:
                    break
            # Trim trailing empty lines
            while block_lines and block_lines[-1].strip() == '':
                block_lines.pop()
            if len(block_lines) >= 2:  # Only convert blocks with 2+ lines
                blocks.append((block_start, block_start + len(block_lines) - 1, '\n'.join(block_lines)))
        else:
            i += 1

    if not blocks:
        return 0

    # Convert blocks to HTML (process in reverse to preserve line numbers)
    for start, end, md_text in reversed(blocks):
        html = md.markdown(md_text, extensions=['tables', 'fenced_code', 'toc'])
        # Wrap in prose-content
        wrapped = f'<div class="prose-content">\n{html}\n</div>'
        # Replace the markdown lines with HTML
        html_lines = wrapped.split('\n')
        lines = lines[:start] + html_lines + lines[end + 1:]

    new_content = '\n'.join(lines)
    if new_content != content:
        njk_path.write_text(new_content, encoding='utf-8')
        return len(blocks)
    return 0

# Process all .njk files
total_converted = 0
for njk_file in sorted(PAGES_DIR.rglob("*.njk")):
    count = convert_raw_markdown_in_template(njk_file)
    if count > 0:
        print(f"Converted {count} markdown block(s) in {njk_file.name}")
        total_converted += count

print(f"\nTotal: {total_converted} markdown block(s) converted to HTML across all templates.")
