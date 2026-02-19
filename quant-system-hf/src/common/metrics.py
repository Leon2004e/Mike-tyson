from __future__ import annotations
import numpy as np
import pandas as pd

def expectancy(r: pd.Series) -> float:
    return float(np.nanmean(r.to_numpy(dtype=float)))

def profit_factor(pl_money: pd.Series) -> float:
    x = pl_money.to_numpy(dtype=float)
    gp = x[x > 0].sum()
    gl = -x[x < 0].sum()
    return float(gp / gl) if gl > 0 else np.inf

def winrate(r: pd.Series) -> float:
    x = r.to_numpy(dtype=float)
    return float(np.mean(x > 0))

def sharpe(r: pd.Series, periods_per_year: float = 252) -> float:
    x = r.to_numpy(dtype=float)
    mu = np.nanmean(x)
    sd = np.nanstd(x, ddof=1)
    return float((mu / sd) * np.sqrt(periods_per_year)) if sd > 0 else np.nan

def max_drawdown(equity: pd.Series) -> float:
    x = equity.to_numpy(dtype=float)
    peak = np.maximum.accumulate(x)
    dd = (x - peak)
    return float(dd.min())
