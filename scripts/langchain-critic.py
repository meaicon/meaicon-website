#!/usr/bin/env python
"""
MEAICON LangGraph Critic — Adversarial Verification Loop.

Reads enhanced-content.md produced by the LangChain enhancer, checks it
against the MEAICON style/quality criteria, and either APPROVES or REJECTS
with specific feedback. On rejection, the feedback is written back to the
topic directory so the next enhancement cycle can self-correct.

Usage:
    python scripts/langchain-critic.py --topic connectivity
    python scripts/langchain-critic.py --all

Output:
    research-data/langchain/<topic>/critic-feedback.json
    research-data/langchain/<topic>/critic-approval.json
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from datetime import datetime

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

OMNIROUTE_URL = os.environ.get("OMNIROUTE_URL", "http://localhost:20128/v1")
OMNIROUTE_MODEL = os.environ.get("OMNIROUTE_MODEL", "my-free-tier")
REPO_ROOT = Path("C:/Users/nev3s/repos/meaicon-website")
LANGCHAIN_DIR = REPO_ROOT / "research-data" / "langchain"

CRITIC_SYSTEM_PROMPT = """You are a senior content critic for MEAICON LLC FZ, a Dubai technology infrastructure company.

Evaluate the content against these criteria:
1. FACTUAL ACCURACY: Flag unsubstantiated statistics or vague superlatives.
2. MEA RELEVANCE: Must reference Middle East / Africa context where applicable.
3. TECHNICAL PRECISION: No marketing fluff. Enterprise IT terminology.
4. STRUCTURE: Clear H2 sections. Single H1. No raw markdown fences.
5. COMPLETENESS: Min 900 chars. No placeholder text.
6. BRAND SAFETY: No competitor names. No AI-isms.
7. HALLUCINATION CHECK: Flag fabricated or unverifiable claims.

Respond as JSON:
{"verdict": "APPROVED" or "REJECTED", "quality_score": 0-10, "issues": [], "suggestions": []}

If REJECTED, every issue must have a matching suggestion.
"""

CRITIC_HUMAN_TEMPLATE = """Evaluate the following enhanced content for topic: {topic}

--- CONTENT START ---
{content}
--- CONTENT END ---

Evaluate against all 7 criteria. Be strict but fair. Quality score 7+ is passing.
"""


def run_critic(topic: str) -> dict:
    """Run critic on a single topic's enhanced content."""
    topic_dir = LANGCHAIN_DIR / topic
    enhanced_file = topic_dir / "enhanced-content.md"

    if not enhanced_file.exists():
        return {"topic": topic, "verdict": "SKIP", "reason": "enhanced-content.md not found"}

    content = enhanced_file.read_text(encoding="utf-8")

    # Pre-checks (local, no LLM needed)
    pre_issues = []

    # Check for code fences
    if "```" in content:
        pre_issues.append("Contains markdown code fences — must be stripped before injection")

    # Check for multiple H1s
    h1_count = len(re.findall(r"^# ", content, re.MULTILINE))
    if h1_count > 1:
        pre_issues.append(f"Contains {h1_count} H1 tags — only 1 allowed")

    # Check minimum length
    if len(content) < 900:
        pre_issues.append(f"Content too short: {len(content)} chars (min 900)")

    # Check for AI-isms
    ai_isms = ["in today's", "in the fast-paced", "delve into", "it's important to note",
               "it's worth noting", "in conclusion", "in summary", "as we navigate"]
    content_lower = content.lower()
    found_isms = [phrase for phrase in ai_isms if phrase in content_lower]
    if found_isms:
        pre_issues.append(f"Contains AI-isms: {', '.join(found_isms)}")

    # If pre-checks fail, reject without LLM call (saves tokens)
    if pre_issues:
        result = {
            "topic": topic,
            "verdict": "REJECTED",
            "quality_score": 0,
            "issues": pre_issues,
            "suggestions": ["Fix all pre-check issues before re-evaluation"],
            "timestamp": datetime.now().isoformat(),
            "evaluator": "local-pre-checks"
        }
        _save_critic_output(topic, result)
        return result

    # LLM-based critic evaluation
    try:
        llm = ChatOpenAI(
            model=OMNIROUTE_MODEL,
            openai_api_base=OMNIROUTE_URL,
            openai_api_key="placeholder",
            temperature=0.1,
            max_tokens=4000,
        )

        # Truncate to 3000 chars to leave output token budget for structured JSON
        messages = [
            SystemMessage(content=CRITIC_SYSTEM_PROMPT),
            HumanMessage(content=CRITIC_HUMAN_TEMPLATE.format(topic=topic, content=content[:3000])),
        ]

        response = llm.invoke(messages)
        raw = response.content if hasattr(response, "content") else str(response)

        # Parse JSON from response (handle markdown wrapping)
        json_match = re.search(r'\{[\s\S]*\}', raw)
        if json_match:
            try:
                result = json.loads(json_match.group(0))
            except json.JSONDecodeError:
                result = {
                    "topic": topic,
                    "verdict": "REJECTED",
                    "quality_score": 0,
                    "issues": ["Critic response was not valid JSON"],
                    "suggestions": ["Re-run critic"],
                    "raw_response": raw[:1000],
                }
        else:
            result = {
                "topic": topic,
                "verdict": "REJECTED",
                "quality_score": 0,
                "issues": ["Critic did not return structured JSON"],
                "suggestions": ["Re-run critic"],
                "raw_response": raw[:1000],
            }

        result["timestamp"] = datetime.now().isoformat()
        result["evaluator"] = "llm-critic"
        result["topic"] = topic

        _save_critic_output(topic, result)
        return result

    except Exception as e:
        result = {
            "topic": topic,
            "verdict": "ERROR",
            "quality_score": 0,
            "issues": [f"LLM critic failed: {str(e)}"],
            "suggestions": ["Check OmniRoute endpoint and retry"],
            "timestamp": datetime.now().isoformat(),
        }
        _save_critic_output(topic, result)
        return result


def _save_critic_output(topic: str, result: dict):
    """Save critic feedback and approval to topic directory."""
    topic_dir = LANGCHAIN_DIR / topic
    topic_dir.mkdir(parents=True, exist_ok=True)

    # Full critic result
    (topic_dir / "critic-feedback.json").write_text(
        json.dumps(result, indent=2), encoding="utf-8"
    )

    # Simplified approval status for pipeline gate
    approval = {
        "topic": topic,
        "approved": result["verdict"] == "APPROVED",
        "quality_score": result.get("quality_score", 0),
        "timestamp": result["timestamp"],
    }
    (topic_dir / "critic-approval.json").write_text(
        json.dumps(approval, indent=2), encoding="utf-8"
    )


def main():
    parser = argparse.ArgumentParser(description="MEAICON LangGraph Critic")
    parser.add_argument("--topic", type=str, help="Topic to evaluate")
    parser.add_argument("--all", action="store_true", help="Evaluate all topics with enhanced-content.md")
    args = parser.parse_args()

    if not args.topic and not args.all:
        print("Usage: python scripts/langchain-critic.py --topic <name> | --all")
        sys.exit(1)

    if args.all:
        topics = sorted([d.name for d in LANGCHAIN_DIR.iterdir()
                        if d.is_dir() and (d / "enhanced-content.md").exists()])
    else:
        topics = [args.topic]

    print("=" * 60)
    print(f"MEAICON LangGraph Critic — Adversarial Verification")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Topics: {len(topics)} ({', '.join(topics)})")
    print("=" * 60)

    approved = 0
    rejected = 0
    errors = 0

    for topic in topics:
        result = run_critic(topic)
        verdict = result["verdict"]
        score = result.get("quality_score", 0)

        if verdict == "APPROVED":
            approved += 1
            print(f"✅ {topic}: APPROVED (score: {score})")
        elif verdict == "REJECTED":
            rejected += 1
            print(f"❌ {topic}: REJECTED (score: {score})")
            for issue in result.get("issues", []):
                print(f"   - {issue}")
        elif verdict == "ERROR":
            errors += 1
            print(f"⚠ {topic}: ERROR — {result.get('issues', ['unknown'])[0]}")
        else:
            print(f"⏭ {topic}: {verdict}")

    print("=" * 60)
    print(f"Summary: {approved} approved, {rejected} rejected, {errors} errors")
    print("Feedback saved to research-data/langchain/<topic>/critic-feedback.json")

    sys.exit(0 if rejected == 0 and errors == 0 else 1)


if __name__ == "__main__":
    main()
