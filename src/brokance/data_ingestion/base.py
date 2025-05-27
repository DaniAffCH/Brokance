from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
import pandas as pd

class BaseDataProvider(ABC):
    @abstractmethod
    def fetch(self, symbol: str, start: datetime, end: Optional[datetime] = None) -> pd.DataFrame:
        pass
    

