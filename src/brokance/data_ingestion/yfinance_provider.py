import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional
from .base import BaseDataProvider

class YahooFinanceProvider(BaseDataProvider):
    def fetch(self, symbol: str, start: datetime, end: Optional[datetime] = None) -> pd.DataFrame:
        if end is None or end == start:
            end = start + timedelta(days=1)

        start_str = start.strftime("%Y-%m-%d")
        end_str = end.strftime("%Y-%m-%d")

        df = yf.download(symbol, start=start_str, end=end_str)
        df.dropna(inplace=True)
        return df
