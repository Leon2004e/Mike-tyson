from __future__ import annotations
from pathlib import Path
import pandas as pd
from src.common.io import write_parquet
from src.common.validation import assert_columns

def build_features(trades_path: str | Path, out_path: str | Path, feature_version: str = "v1_0") -> Path:
    df = pd.read_parquet(trades_path).copy()
    # Minimal: realized R from money P/L relative to average absolute loss (fallback)
    # NOTE: replace with true R once init_sl_dist_price exists.
    assert_columns(df, ["pl_money"])
    denom = df.loc[df["pl_money"] < 0, "pl_money"].abs().mean()
    if pd.isna(denom) or denom == 0:
        denom = df["pl_money"].abs().mean()
    df["r_multiple_price"] = df["pl_money"] / denom

    # costs ratio proxy if comm/swap present
    if "comm_swap" in df.columns:
        gross = df["pl_money"] + df["comm_swap"].fillna(0.0)
        df["cost_to_gross_ratio"] = (df["comm_swap"].fillna(0.0).abs()) / (gross.abs().replace(0, pd.NA))
    else:
        df["cost_to_gross_ratio"] = pd.NA

    write_parquet(df, out_path)
    return Path(out_path)
