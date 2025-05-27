import pandas as pd
import pytest
from brokance.data_ingestion.cache import DataCache, CachedProvider
from brokance.data_ingestion.factory import get_data_provider
from brokance.data_ingestion.yfinance_provider import YahooFinanceProvider
from brokance.data_ingestion.crypto_provider import CryptoProvider


def test_cache_save_load(tmp_path):
    cache = DataCache(cache_dir=tmp_path)
    key = "testkey"
    df = pd.DataFrame({"a": [1, 2, 3]})
    cache.save(key, df)
    loaded = cache.load(key)
    pd.testing.assert_frame_equal(df, loaded)

def test_cache_load_missing(tmp_path):
    cache = DataCache(cache_dir=tmp_path)
    assert cache.load("missing_key") is None

def test_get_yfinance_provider():
    p = get_data_provider("yfinance")
    assert isinstance(p, CachedProvider) and isinstance(p.provider, YahooFinanceProvider)

def test_get_crypto_provider():
    p = get_data_provider("ccxt:binance")
    assert isinstance(p, CachedProvider) and isinstance(p.provider, CryptoProvider)

def test_get_unknown_provider():
    with pytest.raises(ValueError):
        get_data_provider("unknown")
