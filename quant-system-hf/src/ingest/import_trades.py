from __future__ import annotations
from pathlib import Path
import pandas as pd
from src.common.io import write_parquet, ensure_dir

def ingest_trades(raw_root: str | Path, out_path: str | Path) -> Path:
    raw_root = Path(raw_root)
    files = list(raw_root.rglob("*.csv"))
    if not files:
        raise FileNotFoundError(f"No CSV files found under {raw_root}")
    dfs = []
    for f in files:
        df = pd.read_csv(f)
        df["__source_file"] = str(f)
        # sample_type inferred from folder name if present
        parts = [p.lower() for p in f.parts]
        if "backtest" in parts:
            df["sample_type"] = "backtest"
        elif "live" in parts:
            df["sample_type"] = "live"
        elif "demo" in parts:
            df["sample_type"] = "demo"
        else:
            df["sample_type"] = "unknown"
        dfs.append(df)
    out = pd.concat(dfs, ignore_index=True)
    write_parquet(out, out_path)
    return Path(out_path)
