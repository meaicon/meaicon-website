#!/usr/bin/env python
"""
MEAICON LangChain Content Enhancement Pipeline

Reads raw Firecrawl-extracted content and enhances it using LangChain
with the OmniRoute LLM endpoint (localhost:20128).

Usage:
    python scripts/langchain-enhance.py --topic "connectivity" --page-name connectivity --input-dir research-data/firecrawl/connectivity

Input:
    research-data/firecrawl/<topic>/extracted-content.md

Output:
    research-data/langchain/<topic>/enhanced-content.md
    research-data/langchain/<topic>/fact-checks.json
    research-data/langchain/<topic>/content-analysis.json
    research-data/langchain/<topic>/summary.md
"""

import argparse
import json
import os
import sys
import textwrap
from pathlib import Path
from datetime import datetime

# LangChain imports
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

# ── Constants ─────────────────────────────────────────────────────────────────

OMNIROUTE_URL = os.environ.get("OMNIROUTE_URL", "http://localhost:20128/v1")
OMNIROUTE_MODEL = os.environ.get("OMNIROUTE_MODEL", "my-free-tier")
REPO_ROOT = Path("C:/Users/nev3s/repos/meaicon-website")

ENHANCE_SYSTEM_PROMPT = """You are the LangChain Content Enhancement Agent for MEAICON LLC FZ,
a technology infrastructure company headquartered in Meydan Free Zone, Dubai, UAE.

Your job: take raw research content (extracted from external sources via Firecrawl) and
ENHANCE it — not rewrite, not rebrand — enhance with:
1. Additional context and background information
2. Technical depth and precision
3. Industry trends and market data for the MEA (Middle East & Africa) region
4. Factual substantiation for claims (cite sources where possible)
5. Structured organization for web presentation
6. Identification of gaps that need further research

MEAICON's services: Connectivity, Data Centre, Cyber Security, Blockchain, Consulting.
Target audience: Enterprise IT leaders and government decision-makers across MEA.

Output format: Enhanced markdown with clear heading hierarchy. Preserve all factual data
from the original. Add enhancement sections marked with [ENHANCED] prefix.
Do NOT rebrand — that is the Content Agent's job. Do NOT remove source attribution.
"""

FACT_CHECK_SYSTEM_PROMPT = """You are a fact-checking agent for MEAICON website content.
Analyze the provided content and identify:
1. All statistical claims, metrics, and quantitative data
2. All factual assertions that need verification
3. Any claims that appear unsubstantiated or potentially hallucinated
4. Cross-reference recommendations

Output JSON format:
{
  "claims_checked": [
    {
      "claim": "the specific claim text",
      "location": "section/paragraph reference",
      "verification_status": "verified|unverified|flagged",
      "source_needed": true/false,
      "notes": "explanation"
    }
  ],
  "overall_confidence": "high|medium|low",
  "recommendations": ["list of recommendations"]
}
"""

SUMMARY_SYSTEM_PROMPT = """You are an executive summary writer for MEAICON.
Create a concise executive summary (3-5 paragraphs) of the enhanced content.
Focus on key insights, market data, and strategic recommendations.
Target audience: C-suite executives and senior IT decision-makers.
"""

ANALYSIS_SYSTEM_PROMPT = """You are a content analysis agent for MEAICON.
Analyze the enhanced content and provide:
1. Content quality score (1-10)
2. Key topics covered
3. Missing topics that should be researched
4. SEO keyword recommendations
5. Content structure recommendations
6. Suggested call-to-action elements

Output JSON format:
{
  "quality_score": 0,
  "key_topics": [],
  "missing_topics": [],
  "seo_keywords": [],
  "structure_recommendations": [],
  "cta_suggestions": []
}
"""


def init_llm():
    """Initialize the LangChain LLM via OmniRoute."""
    return ChatOpenAI(
        model=OMNIROUTE_MODEL,
        openai_api_key="dummy-key",  # OmniRoute doesn't require a real key
        openai_api_base=OMNIROUTE_URL,
        temperature=0.7,
        max_tokens=4096,
    )


def read_input(input_dir: Path) -> str:
    """Read the extracted content from Firecrawl output."""
    content_file = input_dir / "extracted-content.md"
    if not content_file.exists():
        # Try research-report.md as fallback
        content_file = input_dir / "research-report.md"
    if not content_file.exists():
        print(f"ERROR: No content file found in {input_dir}", file=sys.stderr)
        sys.exit(1)

    with open(content_file, "r", encoding="utf-8") as f:
        return f.read()


def enhance_content(llm, raw_content: str, topic: str) -> str:
    """Use LangChain to enhance the raw research content."""
    messages = [
        SystemMessage(content=ENHANCE_SYSTEM_PROMPT),
        HumanMessage(content=f"Topic: {topic}\n\nRaw research content:\n\n{raw_content}"),
    ]
    response = llm.invoke(messages)
    return response.content


def fact_check(llm, enhanced_content: str) -> dict:
    """Run fact-checking on enhanced content."""
    messages = [
        SystemMessage(content=FACT_CHECK_SYSTEM_PROMPT),
        HumanMessage(content=f"Content to fact-check:\n\n{enhanced_content}"),
    ]
    response = llm.invoke(messages)
    try:
        return json.loads(response.content)
    except json.JSONDecodeError:
        return {"raw_response": response.content, "error": "Failed to parse JSON"}


def analyze_content(llm, enhanced_content: str) -> dict:
    """Analyze content quality and provide recommendations."""
    messages = [
        SystemMessage(content=ANALYSIS_SYSTEM_PROMPT),
        HumanMessage(content=f"Content to analyze:\n\n{enhanced_content}"),
    ]
    response = llm.invoke(messages)
    try:
        return json.loads(response.content)
    except json.JSONDecodeError:
        return {"raw_response": response.content, "error": "Failed to parse JSON"}


def summarize(llm, enhanced_content: str) -> str:
    """Generate an executive summary."""
    messages = [
        SystemMessage(content=SUMMARY_SYSTEM_PROMPT),
        HumanMessage(content=f"Content to summarize:\n\n{enhanced_content}"),
    ]
    response = llm.invoke(messages)
    return response.content


def write_output(output_dir: Path, enhanced: str, facts: dict, analysis: dict, summary: str):
    """Write all output files."""
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_dir / "enhanced-content.md", "w", encoding="utf-8") as f:
        f.write(enhanced)

    with open(output_dir / "fact-checks.json", "w", encoding="utf-8") as f:
        json.dump(facts, f, indent=2, ensure_ascii=False)

    with open(output_dir / "content-analysis.json", "w", encoding="utf-8") as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)

    with open(output_dir / "summary.md", "w", encoding="utf-8") as f:
        f.write(summary)

    print(f"Output written to {output_dir}")
    print(f"  - enhanced-content.md ({len(enhanced)} chars)")
    print(f"  - fact-checks.json")
    print(f"  - content-analysis.json")
    print(f"  - summary.md ({len(summary)} chars)")


def main():
    parser = argparse.ArgumentParser(description="MEAICON LangChain Content Enhancement")
    parser.add_argument("--topic", required=True, help="Research topic")
    parser.add_argument("--page-name", required=True, help="Page name (e.g., connectivity)")
    parser.add_argument("--input-dir", required=True, help="Input directory with Firecrawl content")
    parser.add_argument("--output-dir", default=None, help="Output directory (default: research-data/langchain/<page-name>)")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    if not input_dir.is_absolute():
        input_dir = REPO_ROOT / input_dir

    output_dir = Path(args.output_dir) if args.output_dir else REPO_ROOT / "research-data/langchain" / args.page_name
    if not output_dir.is_absolute():
        output_dir = REPO_ROOT / output_dir

    print(f"MEAICON LangChain Content Enhancement Pipeline")
    print(f"  Topic: {args.topic}")
    print(f"  Page: {args.page_name}")
    print(f"  Input: {input_dir}")
    print(f"  Output: {output_dir}")
    print(f"  LLM: {OMNIROUTE_MODEL} @ {OMNIROUTE_URL}")
    print()

    # Read input
    raw_content = read_input(input_dir)
    print(f"Read {len(raw_content)} chars from input")

    # Initialize LLM
    llm = init_llm()
    print("LangChain LLM initialized")

    # Enhance
    print("Enhancing content...")
    enhanced = enhance_content(llm, raw_content, args.topic)
    print(f"Enhanced content: {len(enhanced)} chars")

    # Fact-check
    print("Fact-checking...")
    facts = fact_check(llm, enhanced)

    # Analyze
    print("Analyzing content...")
    analysis = analyze_content(llm, enhanced)

    # Summarize
    print("Generating summary...")
    summary_text = summarize(llm, enhanced)

    # Write output
    write_output(output_dir, enhanced, facts, analysis, summary_text)

    print("\nPipeline complete!")


if __name__ == "__main__":
    main()
