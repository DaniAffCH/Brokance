import os
import hashlib
import joblib
import pandas as pd
from typing import Optional
from .base import BaseDataProvider
from datetime import datetime

class DataCache:
    def __init__(self, cache_dir="~/.brokerance/cache"):
        self.cache_dir = os.path.expanduser(cache_dir)
        os.makedirs(self.cache_dir, exist_ok=True)

    def _get_cache_path(self, key: str) -> str:
        hash_key = hashlib.md5(key.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{hash_key}.pkl")

    def load(self, key: str) -> Optional[pd.DataFrame]:
        path = self._get_cache_path(key)
        if os.path.exists(path):
            try:
                return joblib.load(path)
            except Exception:
                os.remove(path)
        return None

    def save(self, key: str, data: pd.DataFrame):
        path = self._get_cache_path(key)
        joblib.dump(data, path)
        
class CachedProvider(BaseDataProvider):
    def __init__(self, provider, cache: DataCache):
        self.provider = provider
        self.cache = cache

    def fetch(self, symbol: str, start: datetime, end: Optional[datetime] = None):
        key = f"{self.provider.__class__.__name__}:{symbol}:{start}:{end}"
        cached = self.cache.load(key)
        if cached is not None:
            return cached
        df = self.provider.fetch(symbol, start, end)
        self.cache.save(key, df)
        return df
