import ccxt
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional
from .base import BaseDataProvider

class CryptoProvider(BaseDataProvider):
    def __init__(self, exchange_name="binance"):
        exchange_class = getattr(ccxt, exchange_name)
        self.exchange = exchange_class()

    def fetch(self, symbol: str, start: datetime, end: Optional[datetime] = None) -> pd.DataFrame:
        if end is None or end == start:
            end = start + timedelta(days=1)
        
        since = int(pd.Timestamp(start).timestamp() * 1000)
        ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe='1d', since=since)
        
        df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("timestamp", inplace=True)
        df = df.loc[start:end]
        
        return df
