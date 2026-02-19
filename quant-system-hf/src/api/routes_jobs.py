from __future__ import annotations
from fastapi import APIRouter
import subprocess, sys

router = APIRouter()

@router.post("/jobs/run_pipeline")
def run_pipeline():
    # simple: invoke script; replace with internal function calls later
    p = subprocess.run([sys.executable, "scripts/run_pipeline.py"], capture_output=True, text=True)
    return {"returncode": p.returncode, "stdout": p.stdout[-2000:], "stderr": p.stderr[-2000:]}
