from __future__ import annotations
import pandas as pd

def assert_columns(df: pd.DataFrame, cols: list[str]) -> None:
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

def assert_unique(df: pd.DataFrame, keys: list[str]) -> None:
    dup = df.duplicated(keys)
    if dup.any():
        raise ValueError(f"Duplicate keys found: {int(dup.sum())}")

def validate_trades_standard(df: pd.DataFrame) -> None:
    keys = ["ticket","strategy_id","symbol","type","open_time","close_time"]
    core = ["open_price","close_price","size"]
    assert_columns(df, keys + core)
    assert_unique(df, keys)
    if not (df["open_time"] < df["close_time"]).all():
        raise ValueError("Found trades with open_time >= close_time")
    if not (df["open_price"] > 0).all() or not (df["close_price"] > 0).all():
        raise ValueError("Found non-positive prices")
    if not (df["size"] > 0).all():
        raise ValueError("Found non-positive size")
