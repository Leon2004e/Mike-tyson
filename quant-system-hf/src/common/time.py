from __future__ import annotations
import pandas as pd

def to_utc_datetime(s: pd.Series) -> pd.Series:
    # Accepts strings or datetimes; forces UTC timezone-aware timestamps
    dt = pd.to_datetime(s, utc=True, errors="coerce")
    return dt
