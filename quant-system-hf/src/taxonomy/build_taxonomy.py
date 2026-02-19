from __future__ import annotations
from pathlib import Path
import pandas as pd
from src.common.metrics import expectancy, profit_factor, winrate
from src.common.io import write_parquet
from src.common.validation import assert_columns

def build_taxonomy(features_path: str | Path, out_path: str | Path, freq: str = "weekly") -> Path:
    df = pd.read_parquet(features_path)
    assert_columns(df, ["strategy_id","symbol","sample_type","r_multiple_price","pl_money","open_time"])
    dt = pd.to_datetime(df["open_time"], utc=True)
    if freq == "daily":
        df["_bucket"] = dt.dt.floor("D")
    elif freq == "monthly":
        df["_bucket"] = dt.dt.to_period("M").astype(str)
    else:
        df["_bucket"] = dt.dt.to_period("W").astype(str)

    gcols = ["strategy_id","symbol","sample_type","_bucket"]
    out = df.groupby(gcols, dropna=False).apply(lambda x: pd.Series({
        "trades_n": int(len(x)),
        "expectancy_r": expectancy(x["r_multiple_price"]),
        "winrate": winrate(x["r_multiple_price"]),
        "profit_factor": profit_factor(x["pl_money"]),
        "avg_pl_money": float(x["pl_money"].mean()),
    })).reset_index()

    write_parquet(out, out_path)
    return Path(out_path)
