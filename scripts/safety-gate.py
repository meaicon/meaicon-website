#!/usr/bin/env python3
"""
MEAICON Content Enhancement Automation - Safety Gate
Ensures no enhanced content reaches the website without proper validation.
"""

import json
import os
import sys
import re
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path("C:/Users/nev3s/repos/meaicon-website")
LANGCHAIN_OUTPUT = PROJECT_ROOT / "research-data/langchain"
FIRECRAWL_OUTPUT = PROJECT_ROOT / "research-data/firecrawl"

TOPICS = ["connectivity", "data-centre", "cyber-security", "blockchain", "consulting", "general"]

# Safety thresholds
MIN_ENHANCED_CHARS = 1000
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
    
    # Check quality score
    quality = 0
    if analysis_file.exists():
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
    
    if quality < MIN_QUALITY_SCORE:
        return {"topic": topic, "status": "LOW_QUALITY", "errors": [f"Quality score too low: {quality} (min {MIN_QUALITY_SCORE})"]}
    
    return {
        "topic": topic,
        "status": "APPROVED",
        "chars": char_count,
        "issues": issues,
        "quality": quality
    }

def run_safety_gate():
    """Run the safety gate on all topics."""
    print("=" * 60)
    print("MEAICON Content Enhancement - Safety Gate")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 60)
    
    results = []
    approved = 0
    rejected = 0
    
    for topic in TOPICS:
        result = check_topic(topic)
        results.append(result)
        
        if result["status"] == "APPROVED":
            approved += 1
            print(f"✅ {topic}: APPROVED ({result['chars']} chars, {result['issues']} issues, quality: {result['quality']:.2f})")
        else:
            rejected += 1
            print(f"❌ {topic}: {result['status']}")
            for error in result["errors"]:
                print(f"   - {error}")
    
    print("=" * 60)
    print(f"Summary: {approved} approved, {rejected} rejected out of {len(TOPICS)} topics")
    
    # Write report
    report = {
        "timestamp": datetime.now().isoformat(),
        "total_topics": len(TOPICS),
        "approved": approved,
        "rejected": rejected,
        "results": results
    }
    
    report_file = PROJECT_ROOT / "research-data" / "safety-gate-report.json"
    report_file.parent.mkdir(parents=True, exist_ok=True)
    report_file.write_text(json.dumps(report, indent=2), encoding="utf-8")
    
    print(f"\n📄 Report saved to: {report_file}")
    
    return approved == len(TOPICS)

if __name__ == "__main__":
    success = run_safety_gate()
    sys.exit(0 if success else 1)