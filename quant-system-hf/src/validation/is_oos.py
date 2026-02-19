from __future__ import annotations
from pathlib import Path
import pandas as pd
from src.common.metrics import expectancy
from src.common.io import write_parquet

def is_oos_split(df: pd.DataFrame, split_date: str):
    split_ts = pd.to_datetime(split_date, utc=True)
    dt = pd.to_datetime(df["open_time"], utc=True)
    is_mask = dt < split_ts
    return df[is_mask].copy(), df[~is_mask].copy()

def run_is_oos(features_path: str | Path, out_path: str | Path, split_date: str) -> Path:
    df = pd.read_parquet(features_path)
    is_df, oos_df = is_oos_split(df, split_date)
    rep = pd.DataFrame([{
        "split_date": split_date,
        "is_n": len(is_df),
        "oos_n": len(oos_df),
        "is_expectancy_r": expectancy(is_df["r_multiple_price"]) if len(is_df) else None,
        "oos_expectancy_r": expectancy(oos_df["r_multiple_price"]) if len(oos_df) else None,
    }])
    write_parquet(rep, out_path)
    return Path(out_path)
