#!/usr/bin/env python
"""
MEAICON Pipeline Gate — Build + Lint verification with error capture.

Runs `npm run build` and `npm run lint`, captures failures, and writes
structured error output to research-data/pipeline-errors.json for the
LLM agent to consume on self-correction retries.

Usage:
    python scripts/pipeline-gate.py              # Run build + lint, exit 0 on success
    python scripts/pipeline-gate.py --build-only # Only build
    python scripts/pipeline-gate.py --lint-only  # Only lint
    python scripts/pipeline-gate.py --retry      # Load errors.json and print for agent context

Exit codes:
    0 = all checks passed
    1 = build or lint failed (errors written to pipeline-errors.json)
"""

import json
import subprocess
import sys
import argparse
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).resolve().parent.parent
ERRORS_FILE = REPO_ROOT / "research-data" / "pipeline-errors.json"


def run_command(cmd: str) -> tuple[int, str]:
    """Run a shell command, return (exit_code, combined_output)."""
    result = subprocess.run(
        cmd,
        shell=True,
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=120,
    )
    output = result.stdout + result.stderr
    return result.returncode, output


def write_errors(stage: str, output: str, exit_code: int):
    """Append or replace error entry in pipeline-errors.json."""
    ERRORS_FILE.parent.mkdir(parents=True, exist_ok=True)

    if ERRORS_FILE.exists():
        data = json.loads(ERRORS_FILE.read_text(encoding="utf-8"))
    else:
        data = {"errors": []}

    data["errors"].append({
        "stage": stage,
        "exit_code": exit_code,
        "output": output[-4000:],  # Cap at 4KB to stay within LLM context
        "timestamp": datetime.now().isoformat(),
    })
    data["last_updated"] = datetime.now().isoformat()

    ERRORS_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


def clear_errors():
    """Clear previous errors on successful run."""
    if ERRORS_FILE.exists():
        data = {"errors": [], "last_updated": datetime.now().isoformat(), "last_success": datetime.now().isoformat()}
        ERRORS_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


def show_errors_for_retry():
    """Print errors from pipeline-errors.json for agent self-correction context."""
    if not ERRORS_FILE.exists():
        print("No previous errors found.")
        return

    data = json.loads(ERRORS_FILE.read_text(encoding="utf-8"))
    errors = data.get("errors", [])

    if not errors:
        print("No errors recorded. Last successful run: " + data.get("last_success", "unknown"))
        return

    print(f"=== PIPELINE ERRORS ({len(errors)} entries) ===\n")
    for i, err in enumerate(errors, 1):
        print(f"--- Error {i}: {err['stage']} (exit {err['exit_code']}) ---")
        print(f"Time: {err['timestamp']}")
        print(f"Output:\n{err['output']}")
        print()


def main():
    parser = argparse.ArgumentParser(description="MEAICON Pipeline Gate")
    parser.add_argument("--build-only", action="store_true", help="Run build only")
    parser.add_argument("--lint-only", action="store_true", help="Run lint only")
    parser.add_argument("--retry", action="store_true", help="Show previous errors for agent context")
    args = parser.parse_args()

    if args.retry:
        show_errors_for_retry()
        return

    stages = []
    if not args.lint_only:
        stages.append(("build", "npm run build"))
    if not args.build_only:
        stages.append(("lint", "npm run lint"))

    all_passed = True

    print("=" * 60)
    print("MEAICON Pipeline Gate")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Stages: {', '.join(s[0] for s in stages)}")
    print("=" * 60)

    for stage_name, cmd in stages:
        print(f"\n▶ Running {stage_name}: {cmd}")
        exit_code, output = run_command(cmd)

        if exit_code == 0:
            print(f"✅ {stage_name} PASSED")
        else:
            print(f"❌ {stage_name} FAILED (exit {exit_code})")
            print(f"   Output (last 500 chars): {output[-500:]}")
            write_errors(stage_name, output, exit_code)
            all_passed = False

    if all_passed:
        clear_errors()
        print("\n" + "=" * 60)
        print("✅ ALL CHECKS PASSED — content is safe to commit")
        print("=" * 60)
        sys.exit(0)
    else:
        print("\n" + "=" * 60)
        print("❌ PIPELINE FAILED — errors saved to research-data/pipeline-errors.json")
        print("   Run `python scripts/pipeline-gate.py --retry` to see errors for self-correction")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
