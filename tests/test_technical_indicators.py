import pandas as pd
import numpy as np
from brokance.technical_indicators import moving_average, exponential_moving_average, macd

def test_moving_average_basic():
    data = pd.DataFrame({'Close': [1, 2, 3, 4, 5]})
    result = moving_average(data, window=3)
    expected = pd.Series([np.nan, np.nan, 2.0, 3.0, 4.0])
    pd.testing.assert_series_equal(result.reset_index(drop=True), expected, check_names=False)

def test_ema_basic():
    data = pd.DataFrame({'Close': [1, 2, 3, 4, 5]})
    result = exponential_moving_average(data, window=3)
    expected = data['Close'].ewm(span=3, adjust=False).mean()
    pd.testing.assert_series_equal(result, expected)

def test_moving_average_different_column():
    data = pd.DataFrame({'Price': [10, 20, 30, 40, 50]})
    result = moving_average(data, window=2, column='Price')
    expected = pd.Series([np.nan, 15.0, 25.0, 35.0, 45.0])
    pd.testing.assert_series_equal(result.reset_index(drop=True), expected, check_names=False)

def test_ema_different_column():
    data = pd.DataFrame({'Price': [10, 20, 30, 40, 50]})
    result = exponential_moving_average(data, window=2, column='Price')
    expected = data['Price'].ewm(span=2, adjust=False).mean()
    pd.testing.assert_series_equal(result, expected)

def test_moving_average_series():
    data = pd.Series([5, 10, 15, 20, 25])
    result = moving_average(data, window=3)
    expected = pd.Series([np.nan, np.nan, 10, 15, 20])
    pd.testing.assert_series_equal(result.reset_index(drop=True), expected, check_names=False)

def test_ema_series():
    data = pd.Series([5, 10, 15, 20, 25])
    result = exponential_moving_average(data, window=3)
    expected = data.ewm(span=3, adjust=False).mean()
    pd.testing.assert_series_equal(result.reset_index(drop=True), expected, check_names=False)

def test_macd_output_structure():
    df = pd.DataFrame({"Close": np.linspace(100, 120, 50)})
    out = macd(df)
    assert isinstance(out, pd.DataFrame)
    assert set(out.columns) == {"MACD", "signal", "histogram"}
    assert len(out) == len(df)

def test_macd_with_constant_input():
    df = pd.DataFrame({"Close": [100.0] * 50})
    out = macd(df)
    assert np.allclose(out["MACD"], 0)
    assert np.allclose(out["signal"], 0)
    assert np.allclose(out["histogram"], 0)

def test_macd_with_nan_handling():
    df = pd.DataFrame({"Close": [np.nan] * 5 + [100 + i for i in range(45)]})
    out = macd(df)
    assert out.isnull().sum().max() > 0  # some NaNs are expected
    