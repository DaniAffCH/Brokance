from .yfinance_provider import YahooFinanceProvider
from .crypto_provider import CryptoProvider
from .base import BaseDataProvider
from .cache import DataCache, CachedProvider

_cache = DataCache()

def get_data_provider(name: str) -> BaseDataProvider:
    if name == "yfinance":
        base = YahooFinanceProvider()
    elif name.startswith("ccxt:"):
        exchange = name.split(":", 1)[1]
        base = CryptoProvider(exchange)
    else:
        raise ValueError(f"Unknown provider: {name}")
    return CachedProvider(base, _cache)
