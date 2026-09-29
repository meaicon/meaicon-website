#!/usr/bin/env python
"""
MEAICON Firecrawl Snapshot Script

Uses the Firecrawl CLI to perform a complete snapshot of the meaicon-website
branch (live site at meaicon.com) and all key pages. Outputs structured
content to research-data/firecrawl/snapshot/.

Usage:
    python scripts/firecrawl-snapshot.py

    # Or for a single page:
    python scripts/firecrawl-snapshot.py --page connectivity
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# ── Constants ─────────────────────────────────────────────────────────────────

REPO_ROOT = Path("C:/Users/nev3s/repos/meaicon-website")
BASE_URL = "https://meaicon.com"
OUTPUT_ROOT = REPO_ROOT / "research-data/firecrawl/snapshot"
FIRECRAWL_CMD = os.environ.get(
    "FIRECRAWL_CMD",
    "C:/Users/nev3s/AppData/Local/hermes/tools/node-26.7.0-win32-x64/firecrawl.cmd"
)

# All pages on the MEAICON website
PAGES = {
    # Main pages
    "home": "/",
    "solutions-index": "/solutions.html",
    "industries-index": "/industries.html",
    "global-connectivity": "/global-connectivity.html",
    "partners": "/partners.html",
    "case-studies": "/case-studies.html",
    "about": "/about.html",
    "contact": "/contact.html",
    # Solutions
    "connectivity": "/solutions/connectivity.html",
    "data-centre": "/solutions/data-centre.html",
    "cyber-security": "/solutions/cyber-security.html",
    "blockchain": "/solutions/blockchain.html",
    "consulting": "/solutions/consulting.html",
    # Industries
    "banking": "/industries/banking.html",
    "defence": "/industries/defence.html",
    "education": "/industries/education.html",
    "energy": "/industries/energy.html",
    "government": "/industries/government.html",
    "healthcare": "/industries/healthcare.html",
    "hospitality": "/industries/hospitality.html",
    "logistics": "/industries/logistics.html",
    "maritime": "/industries/maritime.html",
    "real-estate": "/industries/real-estate.html",
    "retail": "/industries/retail.html",
    "telecom": "/industries/telecom.html",
}

# Research topics for content enhancement
RESEARCH_TOPICS = {
    "connectivity": "MEA connectivity SD-WAN MPLS satellite subsea cables 5G edge networking",
    "data-centre": "Data centre colocation managed hosting edge DC sovereign DC green DC MEA",
    "cyber-security": "Cyber security SOC MSSP zero-trust OT security compliance NCA DIFC ADGM",
    "blockchain": "Blockchain DLT smart contracts CBDC tokenization DeFi MEA Middle East Africa",
    "consulting": "Digital transformation IT strategy cloud migration managed services consulting MEA",
}


def firecrawl_scrape(url: str, output_dir: Path, page_name: str) -> dict:
    """Scrape a URL using Firecrawl CLI and save the output."""
    output_dir.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        [FIRECRAWL_CMD, "scrape", url, "--format", "markdown"],
        capture_output=True, text=True, timeout=120, encoding="utf-8"
    )
    if result.returncode != 0:
        print(f"  ERROR scraping {url}: {result.stderr}", file=sys.stderr)
        return {"url": url, "status": "error", "error": result.stderr}

    content = result.stdout
    # Save content
    with open(output_dir / "extracted-content.md", "w", encoding="utf-8") as f:
        f.write(content)

    # Save metadata
    metadata = {
        "url": url,
        "page_name": page_name,
        "extracted_date": datetime.now().isoformat(),
        "content_type": "page_snapshot",
        "word_count": len(content.split()),
        "char_count": len(content),
    }
    with open(output_dir / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print(f"  Scraped {url} → {len(content)} chars, {metadata['word_count']} words")
    return metadata


def firecrawl_search(topic: str, output_dir: Path) -> dict:
    """Search for research topics using Firecrawl."""
    output_dir.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        [FIRECRAWL_CMD, "search", topic, "--limit", "5"],
        capture_output=True, text=True, timeout=120, encoding="utf-8"
    )
    if result.returncode != 0:
        print(f"  ERROR searching '{topic}': {result.stderr}", file=sys.stderr)
        return {"topic": topic, "status": "error", "error": result.stderr}

    content = result.stdout
    with open(output_dir / "research-search.md", "w", encoding="utf-8") as f:
        f.write(content)

    metadata = {
        "topic": topic,
        "search_date": datetime.now().isoformat(),
        "results_count": content.count("http"),
        "content_type": "search_results",
    }
    with open(output_dir / "search-metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print(f"  Searched '{topic}' → {len(content)} chars")
    return metadata


def main():
    parser = argparse.ArgumentParser(description="MEAICON Firecrawl Snapshot")
    parser.add_argument("--page", help="Scrape only a single page (by key name)")
    parser.add_argument("--research", action="store_true", help="Also run research searches for each topic")
    parser.add_argument("--output-dir", default=None, help="Output directory override")
    args = parser.parse_args()

    print("MEAICON Firecrawl Snapshot")
    print(f"  Base URL: {BASE_URL}")
    print(f"  Output: {OUTPUT_ROOT}")
    print()

    # Determine which pages to scrape
    if args.page:
        if args.page not in PAGES:
            print(f"ERROR: Unknown page '{args.page}'. Available: {', '.join(PAGES.keys())}", file=sys.stderr)
            sys.exit(1)
        pages = {args.page: PAGES[args.page]}
    else:
        pages = PAGES

    # Snapshot all pages
    print(f"Scraping {len(pages)} pages...")
    all_metadata = []
    for page_name, path in pages.items():
        url = f"{BASE_URL}{path}"
        print(f"  [{page_name}] {url}")
        page_output_dir = OUTPUT_ROOT / page_name
        metadata = firecrawl_scrape(url, page_output_dir, page_name)
        all_metadata.append(metadata)

    # Save index
    with open(OUTPUT_ROOT / "snapshot-index.json", "w", encoding="utf-8") as f:
        json.dump({
            "snapshot_date": datetime.now().isoformat(),
            "base_url": BASE_URL,
            "pages_scraped": len(all_metadata),
            "pages": all_metadata,
        }, f, indent=2)

    print(f"\nSnapshot complete: {len(all_metadata)} pages scraped")

    # Optional: Run research searches
    if args.research:
        print(f"\nRunning research searches for {len(RESEARCH_TOPICS)} topics...")
        for page_name, topic in RESEARCH_TOPICS.items():
            print(f"  [{page_name}] {topic}")
            research_output_dir = REPO_ROOT / "research-data/firecrawl" / page_name
            firecrawl_search(topic, research_output_dir)

        print(f"\nResearch searches complete")

    print(f"\nAll output in: {OUTPUT_ROOT}")


if __name__ == "__main__":
    main()
