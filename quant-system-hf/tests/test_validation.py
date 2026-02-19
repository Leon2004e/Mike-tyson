import pandas as pd
from src.common.validation import validate_trades_standard

def test_validate_trades_standard_pass():
    df = pd.DataFrame({
        "ticket":["1"],
        "strategy_id":["s1"],
        "symbol":["EURUSD"],
        "type":["long"],
        "open_time":[pd.Timestamp("2024-01-01", tz="UTC")],
        "close_time":[pd.Timestamp("2024-01-01 01:00", tz="UTC")],
        "open_price":[1.1],
        "close_price":[1.2],
        "size":[0.1],
    })
    validate_trades_standard(df)
