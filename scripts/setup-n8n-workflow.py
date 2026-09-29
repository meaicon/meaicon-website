#!/usr/bin/env python
"""
MEAICON n8n Workflow Setup Script

Sets up the n8n workflow for the MEAICON content enhancement pipeline.
Imports the workflow JSON and creates the necessary webhook endpoints.

Usage:
    python scripts/setup-n8n-workflow.py
"""

import argparse
import json
import os
import sys
import subprocess
from pathlib import Path

# ── Constants ─────────────────────────────────────────────────────────────────

N8N_URL = os.environ.get("N8N_URL", "http://localhost:5678")
N8N_API_KEY_FILE = "~/.n8n/api-key.txt"
WORKFLOW_FILE = "scripts/n8n/meaicon-content-enhancement.json"
REPO_ROOT = Path("C:/Users/nev3s/repos/meaicon-website")


def get_n8n_api_key():
    """Read the n8n API key from the file."""
    key_file = Path(os.path.expanduser(N8N_API_KEY_FILE))
    if not key_file.exists():
        print(f"ERROR: n8n API key file not found at {key_file}", file=sys.stderr)
        sys.exit(1)
    return key_file.read_text().strip()


def check_n8n_running():
    """Check if n8n is running."""
    try:
        result = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", f"{N8N_URL}/health"],
            capture_output=True, text=True, timeout=10
        )
        return result.stdout.strip() == "200"
    except Exception:
        return False


def import_workflow(api_key):
    """Import the workflow JSON into n8n."""
    workflow_path = REPO_ROOT / WORKFLOW_FILE
    if not workflow_path.exists():
        print(f"ERROR: Workflow file not found at {workflow_path}", file=sys.stderr)
        sys.exit(1)

    with open(workflow_path, "r", encoding="utf-8") as f:
        workflow = json.load(f)

    # Create workflow via n8n API
    result = subprocess.run(
        [
            "curl", "-s", "-X", "POST",
            f"{N8N_URL}/api/v1/workflows",
            "-H", f"X-N8N-API-KEY: {api_key}",
            "-H", "Content-Type: application/json",
            "-d", json.dumps(workflow)
        ],
        capture_output=True, text=True, timeout=30
    )

    if result.returncode != 0:
        print(f"ERROR: Failed to import workflow: {result.stderr}", file=sys.stderr)
        return None

    response = json.loads(result.stdout)
    if "data" in response and "id" in response["data"]:
        workflow_id = response["data"]["id"]
        print(f"Workflow imported successfully. ID: {workflow_id}")
        return workflow_id
    elif "id" in response:
        workflow_id = response["id"]
        print(f"Workflow imported successfully. ID: {workflow_id}")
        return workflow_id
    else:
        print(f"Unexpected response: {result.stdout[:500]}", file=sys.stderr)
        return None


def activate_workflow(api_key, workflow_id):
    """Activate the workflow."""
    result = subprocess.run(
        [
            "curl", "-s", "-X", "PATCH",
            f"{N8N_URL}/api/v1/workflows/{workflow_id}",
            "-H", f"X-N8N-API-KEY: {api_key}",
            "-H", "Content-Type: application/json",
            "-d", json.dumps({"active": True})
        ],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode == 0:
        print(f"Workflow {workflow_id} activated")
    else:
        print(f"Failed to activate workflow: {result.stderr}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="MEAICON n8n Workflow Setup")
    parser.add_argument("--skip-import", action="store_true", help="Skip workflow import")
    args = parser.parse_args()

    print("MEAICON n8n Workflow Setup")
    print(f"  n8n URL: {N8N_URL}")
    print()

    # Check if n8n is running
    if not check_n8n_running():
        print("n8n is not running. Start it with: ~/.n8n/start-n8n.sh")
        print("Skipping workflow import. The workflow JSON is ready at:")
        print(f"  {REPO_ROOT / WORKFLOW_FILE}")
        print("\nYou can import it manually via the n8n UI: Import from File.")
        return

    print("n8n is running")

    if args.skip_import:
        print("Skipping import as requested")
        return

    # Get API key
    api_key = get_n8n_api_key()
    print(f"API key loaded")

    # Import workflow
    workflow_id = import_workflow(api_key)
    if workflow_id:
        # Activate workflow
        activate_workflow(api_key, workflow_id)
        print(f"\nWorkflow is ready at: {N8N_URL}/workflow/{workflow_id}")
    else:
        print("\nImport failed. You can manually import the workflow JSON via n8n UI.")
        print(f"  File: {REPO_ROOT / WORKFLOW_FILE}")


if __name__ == "__main__":
    main()
