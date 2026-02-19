from __future__ import annotations
from fastapi import APIRouter, Query
import pandas as pd
from pathlib import Path

router = APIRouter()

@router.get("/trades")
def get_trades(path: str = "data/curated/trades/trades_standard.parquet",
               limit: int = Query(1000, ge=1, le=20000)):
    p = Path(path)
    if not p.exists():
        return {"error": f"missing {p}"}
    df = pd.read_parquet(p).head(limit)
    return {"rows": df.to_dict(orient="records")}
