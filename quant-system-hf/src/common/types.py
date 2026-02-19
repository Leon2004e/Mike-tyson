from enum import Enum

class SampleType(str, Enum):
    backtest='backtest'
    live='live'
    demo='demo'
    prop='prop'
