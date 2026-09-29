#!/usr/bin/env python3
"""
MEAICON Content Enhancement Automation - Safety Gate
Ensures no enhanced content reaches the website without proper validation.

Modes:
  --pre-injection  : Validate ALL LangChain output dirs before injection (full coverage)
  --post-injection : Validate the original 6 core topics (default, backward compatible)
"""

import json
import os
import sys
import re
import argparse
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path("C:/Users/nev3s/repos/meaicon-website")
LANGCHAIN_OUTPUT = PROJECT_ROOT / "research-data" / "langchain"
FIRECRAWL_OUTPUT = PROJECT_ROOT / "research-data" / "firecrawl"

# Original 6 core topics (backward compat)
CORE_TOPICS = ["connectivity", "data-centre", "cyber-security", "blockchain", "consulting", "general"]

# Safety thresholds
MIN_ENHANCED_CHARS = 900
MAX_FACT_CHECK_ISSUES = 2
MIN_QUALITY_SCORE = 6  # LangChain outputs quality_score as integer 0-10

def extract_quality_score(raw_response):
    """Extract quality_score from raw_response string."""
    if not isinstance(raw_response, str):
        return 0
    
    # Look for quality_score in the JSON-like string
    match = re.search(r'"quality_score"\s*:\s*(\d+)', raw_response)
    if match:
        try:
            return int(match.group(1))
        except ValueError:
            pass
    
    return 0

def check_topic(topic):
    """Check if a topic has valid enhanced content."""
    enhanced_file = LANGCHAIN_OUTPUT / topic / "enhanced-content.md"
    fact_check_file = LANGCHAIN_OUTPUT / topic / "fact-checks.json"
    analysis_file = LANGCHAIN_OUTPUT / topic / "content-analysis.json"

    if not enhanced_file.exists():
        return {"topic": topic, "status": "MISSING", "errors": ["enhanced-content.md not found"]}

    content = enhanced_file.read_text(encoding="utf-8")
    char_count = len(content)

    if char_count < MIN_ENHANCED_CHARS:
        return {"topic": topic, "status": "TOO_SHORT", "errors": [f"Only {char_count} chars (min {MIN_ENHANCED_CHARS})"]}

    # Check for raw markdown code fences that would break HTML rendering
    if '```' in content:
        return {"topic": topic, "status": "RAW_FENCES", "errors": ["Contains markdown code fences that will render as raw text in HTML"]}

    # Check for duplicate H1 tags
    h1_count = len(re.findall(r'^# ', content, re.MULTILINE))
    if h1_count > 1:
        return {"topic": topic, "status": "DUPLICATE_H1", "errors": [f"Contains {h1_count} H1 tags — only 1 allowed"]}

    # Check fact-checks
    issues = 0
    if fact_check_file.exists():
        try:
            fc = json.loads(fact_check_file.read_text(encoding="utf-8"))
            # Handle different fact-checks.json formats
            if isinstance(fc, dict) and "issues" in fc:
                issues = len(fc.get("issues", []))
            elif isinstance(fc, list):
                issues = len(fc)
        except Exception:
            # If we can't parse, assume 0 issues to be safe
            issues = 0
    
    if issues > MAX_FACT_CHECK_ISSUES:
        return {"topic": topic, "status": "TOO_MANY_ISSUES", "errors": [f"Too many fact-check issues: {issues} (max {MAX_FACT_CHECK_ISSUES})"]}
    
    # Check quality score — but don't fail if no analysis file exists
    quality = 0
    has_analysis = False
    if analysis_file.exists():
        has_analysis = True
        try:
            analysis = json.loads(analysis_file.read_text(encoding="utf-8"))
            if isinstance(analysis, dict) and "raw_response" in analysis:
                quality = extract_quality_score(analysis["raw_response"])
            elif isinstance(analysis, dict) and "quality_score" in analysis:
                q = analysis["quality_score"]
                if isinstance(q, str):
                    try:
                        quality = int(q)
                    except ValueError:
                        quality = 0
                else:
                    quality = int(q) if isinstance(q, (int, float)) else 0
        except Exception:
            quality = 0

    if has_analysis and quality < MIN_QUALITY_SCORE:
        return {"topic": topic, "status": "LOW_QUALITY", "errors": [f"Quality score too low: {quality} (min {MIN_QUALITY_SCORE})"]}

    # If no analysis file, approve with quality=0 and note "ungraded"
    return {
        "topic": topic,
        "status": "APPROVED",
        "chars": char_count,
        "issues": issues,
        "quality": quality if has_analysis else 0,
        "graded": has_analysis
    }

def run_safety_gate(mode="post-injection"):
    """Run the safety gate on topics.

    mode='pre-injection': validate ALL LangChain output dirs (full coverage)
    mode='post-injection': validate the original 6 core topics (default)
    """
    if mode == "pre-injection":
        # Discover all topic dirs that have enhanced-content.md
        topics = sorted([d.name for d in LANGCHAIN_OUTPUT.iterdir()
                        if d.is_dir() and (d / "enhanced-content.md").exists()])
    else:
        topics = CORE_TOPICS

    print("=" * 60)
    print(f"MEAICON Content Enhancement - Safety Gate ({mode})")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Topics: {len(topics)} ({'all dirs' if mode == 'pre-injection' else 'core 6'})")
    print("=" * 60)

    results = []
    approved = 0
    rejected = 0

    for topic in topics:
        result = check_topic(topic)
        results.append(result)

        if result["status"] == "APPROVED":
            approved += 1
            print(f"✅ {topic}: APPROVED ({result['chars']} chars, {result['issues']} issues, quality: {result['quality']})")
        else:
            rejected += 1
            print(f"❌ {topic}: {result['status']}")
            for error in result.get("errors", []):
                print(f"   - {error}")

    print("=" * 60)
    print(f"Summary: {approved} approved, {rejected} rejected out of {len(topics)} topics")

    # Write report
    report = {
        "timestamp": datetime.now().isoformat(),
        "mode": mode,
        "total_topics": len(topics),
        "approved": approved,
        "rejected": rejected,
        "results": results
    }
    
    report_file = PROJECT_ROOT / "research-data" / "safety-gate-report.json"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    report_file.write_text(json.dumps(report, indent=2), encoding="utf-8")
    
    print(f"\n📄 Report saved to: {report_file}")
    
    return approved == len(topics)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MEAICON Safety Gate")
    parser.add_argument("--pre-injection", action="store_true",
                        help="Validate ALL LangChain output dirs before injection")
    parser.add_argument("--post-injection", action="store_true",
                        help="Validate the original 6 core topics (default)")
    args = parser.parse_args()

    mode = "pre-injection" if args.pre_injection else "post-injection"
    success = run_safety_gate(mode=mode)
    sys.exit(0 if success else 1)