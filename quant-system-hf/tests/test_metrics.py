import pandas as pd
from src.common.metrics import expectancy, profit_factor

def test_expectancy():
    s = pd.Series([1.0, -1.0, 2.0])
    assert expectancy(s) == (1.0 - 1.0 + 2.0) / 3.0

def test_profit_factor():
    s = pd.Series([10.0, -5.0, 5.0, -5.0])
    assert profit_factor(s) == 15.0 / 10.0
