#!/usr/bin/env python3
"""
MEAICON Content Enhancement API Server
Provides HTTP endpoints for n8n workflow to call Firecrawl, LangChain, and Safety Gate
"""

import asyncio
import json
import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import uvicorn

PROJECT_ROOT = Path("C:/Users/nev3s/repos/meaicon-website")
LANGCHAIN_DIR = PROJECT_ROOT / "research-data/langchain"
FIRECRAWL_DIR = PROJECT_ROOT / "research-data/firecrawl"

TOPICS = ["connectivity", "data-centre", "cyber-security", "blockchain", "consulting", "general"]

app = FastAPI(title="MEAICON Content Enhancement API", version="1.0.0")

class ScrapeRequest(BaseModel):
    topic: str

class EnhanceRequest(BaseModel):
    topic: str

class ValidateRequest(BaseModel):
    pass  # No parameters needed - validates all topics

class BuildRequest(BaseModel):
    pass  # No parameters needed - builds the site

@app.post("/api/scrape")
async def scrape_topic(req: ScrapeRequest):
    """Run firecrawl-snapshot.py for a topic."""
    if req.topic not in TOPICS:
        raise HTTPException(status_code=400, detail=f"Unknown topic: {req.topic}")
    
    input_dir = FIRECRAWL_DIR / req.topic
    if not input_dir.exists():
        raise HTTPException(status_code=404, detail=f"Input directory not found: {input_dir}")
    
    try:
        # Run firecrawl-snapshot.py
        result = subprocess.run(
            [sys.executable, "scripts/firecrawl-snapshot.py", "--page", req.topic],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            timeout=300
        )
        
        return {
            "success": result.returncode == 0,
            "topic": req.topic,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "topic": req.topic, "error": "Timeout"}
    except Exception as e:
        return {"success": False, "topic": req.topic, "error": str(e)}

@app.post("/api/enhance")
async def enhance_topic(req: EnhanceRequest):
    """Run langchain-enhance.py for a topic."""
    if req.topic not in TOPICS:
        raise HTTPException(status_code=400, detail=f"Unknown topic: {req.topic}")
    
    input_dir = FIRECRAWL_DIR / req.topic
    if not input_dir.exists():
        raise HTTPException(status_code=404, detail=f"Input directory not found: {input_dir}")
    
    try:
        result = subprocess.run(
            [sys.executable, "scripts/langchain-enhance.py", 
             "--topic", req.topic, 
             "--page-name", req.topic, 
             "--input-dir", str(input_dir)],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            timeout=300
        )
        
        return {
            "success": result.returncode == 0,
            "topic": req.topic,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "topic": req.topic, "error": "Timeout"}
    except Exception as e:
        return {"success": False, "topic": req.topic, "error": str(e)}

@app.post("/api/validate")
async def validate_all(req: ValidateRequest):
    """Run safety-gate.py validation on all topics."""
    try:
        result = subprocess.run(
            [sys.executable, "scripts/safety-gate.py"],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            timeout=120
        )
        
        # Parse the report
        report_file = PROJECT_ROOT / "research-data" / "safety-gate-report.json"
        report = {}
        if report_file.exists():
            with open(report_file) as f:
                report = json.load(f)
        
        return {
            "success": result.returncode == 0,
            "approved": report.get("approved", 0),
            "rejected": report.get("rejected", 0),
            "total": report.get("total_topics", 0),
            "results": report.get("results", []),
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/api/build")
async def build_site(req: BuildRequest):
    """Build the website with npm run build."""
    npm_path = "C:/Users/nev3s/AppData/Local/hermes/tools/node-26.7.0-win32-x64/npm.cmd"
    
    # Debug logging
    import os
    print(f"[DEBUG] npm_path: {npm_path}")
    print(f"[DEBUG] npm_path exists: {os.path.exists(npm_path)}")
    print(f"[DEBUG] PROJECT_ROOT: {PROJECT_ROOT}")
    print(f"[DEBUG] PROJECT_ROOT exists: {PROJECT_ROOT.exists()}")
    
    try:
        result = subprocess.run(
            [npm_path, "run", "build"],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            timeout=180
        )
        
        print(f"[DEBUG] Return code: {result.returncode}")
        
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout[-2000:] if result.stdout else "",
            "stderr": result.stderr[-2000:] if result.stderr else ""
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Build timeout"}
    except Exception as e:
        print(f"[DEBUG] Exception: {type(e).__name__}: {e}")
        return {"success": False, "error": str(e)}

@app.get("/health")
async def health():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)