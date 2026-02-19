from __future__ import annotations
from pathlib import Path
import pandas as pd
from src.common.io import write_parquet

def enrich_calendar(trades_path: str | Path, out_path: str | Path) -> Path:
    df = pd.read_parquet(trades_path)[["open_time"]].dropna()
    dt = pd.to_datetime(df["open_time"], utc=True)
    cal = pd.DataFrame({
        "date": dt.dt.floor("D").unique()
    })
    cal["date"] = pd.to_datetime(cal["date"], utc=True)
    cal["weekday"] = cal["date"].dt.weekday
    cal["week_of_year"] = cal["date"].dt.isocalendar().week.astype(int)
    cal["month"] = cal["date"].dt.month.astype(int)
    cal["quarter"] = cal["date"].dt.quarter.astype(int)
    write_parquet(cal.sort_values("date"), out_path)
    return Path(out_path)
