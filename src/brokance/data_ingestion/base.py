from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Dict, List
from datetime import timedelta
import pandas as pd

class BaseDataProvider(ABC):
    @abstractmethod
    def fetch(self, symbol: str, start: datetime, end: Optional[datetime] = None) -> pd.DataFrame:
        pass
    
    def latest_price(self, symbol: List[str], now: Optional[datetime] = None, lookback_days: int = 5) -> float:        
        if not now:
            now = datetime.now()
        start = now - timedelta(days=lookback_days)
        df = self.fetch(symbol, start=start, end=now)
        if df.empty:
            raise ValueError(f"No data for {symbol} from {start.date()} to {now.date()}")
        return df['Close'].iloc[-1].item()

    def symbol_exists(self, symbol: str, since: datetime = datetime(2000, 1, 1)) -> bool:
        try:
            df = self.fetch(symbol, start=since)
            return not df.empty
        except Exception:
            return False