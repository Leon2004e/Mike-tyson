from __future__ import annotations
from pathlib import Path
import pandas as pd
from src.common.time import to_utc_datetime
from src.common.utils import snake
from src.common.io import write_parquet
from src.common.validation import validate_trades_standard

# Map possible raw column names -> standard names
COLMAP = {
    "ticket": "ticket",
    "Ticket": "ticket",
    "symbol": "symbol",
    "Symbol": "symbol",
    "type": "type",
    "Type": "type",
    "open time": "open_time",
    "Open time": "open_time",
    "close time": "close_time",
    "Close time": "close_time",
    "open price": "open_price",
    "Open price": "open_price",
    "close price": "close_price",
    "Close price": "close_price",
    "size": "size",
    "Size": "size",
    "profit/loss": "profit_loss",
    "Profit/Loss": "profit_loss",
    "p/l in money": "pl_money",
    "P/L in money": "pl_money",
    "comm/swap": "comm_swap",
    "Comm/Swap": "comm_swap",
    "p/l in pips": "pl_pips",
    "P/L in pips": "pl_pips",
    "comment": "comment",
    "Comment": "comment",
    "sample type": "sample_type",
    "Sample type": "sample_type",
    "__source_file": "__source_file",
    "strategy_id": "strategy_id",
}

def standardize_trades(interim_trades_path: str | Path, curated_out_path: str | Path) -> Path:
    df = pd.read_parquet(interim_trades_path)
    # normalize columns
    df.columns = [snake(c) for c in df.columns]
    # apply mapping where possible
    rename = {}
    for c in df.columns:
        rename[c] = COLMAP.get(c, c)
    df = df.rename(columns=rename)

    # ensure strategy_id exists
    if "strategy_id" not in df.columns:
        df["strategy_id"] = "strategy_unknown"

    # normalize type
    if "type" in df.columns:
        df["type"] = df["type"].astype(str).str.lower().map(
            {"buy":"long","sell":"short","long":"long","short":"short"}
        ).fillna(df["type"].astype(str).str.lower())

    # timestamps
    df["open_time"] = to_utc_datetime(df["open_time"])
    df["close_time"] = to_utc_datetime(df["close_time"])

    # numeric casts
    for c in ["open_price","close_price","size","pl_money","pl_pips","comm_swap"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # derived fields
    if "trade_duration_minutes" not in df.columns:
        df["trade_duration_minutes"] = (df["close_time"] - df["open_time"]).dt.total_seconds() / 60.0

    # if broker used Profit/Loss but no pl_money, map it
    if "pl_money" not in df.columns and "profit_loss" in df.columns:
        df["pl_money"] = pd.to_numeric(df["profit_loss"], errors="coerce")

    # fill missing meta
    if "sample_type" not in df.columns:
        df["sample_type"] = "unknown"
    if "__source_file" not in df.columns:
        df["__source_file"] = "unknown"
    if "comment" not in df.columns:
        df["comment"] = ""

    # keep only columns we care about now + passthrough known extras
    keep_cols = [
        "ticket","strategy_id","symbol","type",
        "open_time","close_time","open_price","close_price","size",
        "pl_money","pl_pips","comm_swap","trade_duration_minutes",
        "comment","sample_type","__source_file"
    ]
    for c in keep_cols:
        if c not in df.columns:
            df[c] = pd.NA
    df = df[keep_cols]

    validate_trades_standard(df.dropna(subset=["ticket","symbol","type","open_time","close_time"]))
    write_parquet(df, curated_out_path)
    return Path(curated_out_path)
