import pandas as pd
import numpy as np
from typing import Union

def moving_average(df: Union[pd.DataFrame, pd.Series], window: int, column: str = 'Close') -> pd.Series:
    series = df
    if isinstance(series, pd.DataFrame):
        series = series[column]
    
    return series.rolling(window=window).mean()

def exponential_moving_average(df: Union[pd.DataFrame, pd.Series], window: int, column: str = 'Close') -> pd.Series:
    series = df
    if isinstance(series, pd.DataFrame):
        series = series[column]
    
    return series.ewm(span=window, adjust=False).mean()

# moving average convergence/divergence 
def macd(df: Union[pd.DataFrame, pd.Series], fast: int = 12, slow: int = 26, signal: int = 9, column: str = 'Close') -> pd.DataFrame:    
    fast_ema = exponential_moving_average(df, fast, column)
    slow_ema = exponential_moving_average(df, slow, column)
    
    macd = fast_ema - slow_ema
    
    signal = exponential_moving_average(macd, signal, column)
    histogram = macd - signal
    return pd.DataFrame({
        'MACD': macd,
        'signal': signal,
        'histogram': histogram
    })
    