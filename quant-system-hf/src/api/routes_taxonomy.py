from __future__ import annotations
from fastapi import APIRouter, Query
import pandas as pd
from pathlib import Path

router = APIRouter()

@router.get("/taxonomy/weekly")
def weekly(path: str = "data/taxonomy/weekly/taxonomy_weekly.parquet",
           limit: int = Query(2000, ge=1, le=50000)):
    p = Path(path)
    if not p.exists():
        return {"error": f"missing {p}"}
    df = pd.read_parquet(p).head(limit)
    return {"rows": df.to_dict(orient="records")}
