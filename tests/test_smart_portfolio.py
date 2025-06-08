import pytest
from unittest.mock import MagicMock
from datetime import datetime
from brokance.portfolio.smart_portfolio import SmartPortfolio, Transaction

@pytest.fixture
def mock_data_provider():
    dp = MagicMock()
    dp.symbol_exists.return_value = True
    dp.latest_price.return_value = 150.0
    return dp

def test_add_transaction_with_valid_symbol(mock_data_provider):
    sp = SmartPortfolio(mock_data_provider)
    sp.add_transaction("AAPL", 1, datetime.now(), "buy")
    assert "AAPL" in sp.positions

def test_add_transaction_invalid_symbol_raises(mock_data_provider):
    mock_data_provider.symbol_exists.return_value = False
    sp = SmartPortfolio(mock_data_provider)
    with pytest.raises(ValueError):
        sp.add_transaction("AAPL", 1, datetime.now(), "buy")

def test_market_value_calls_base_with_fetched_prices(mock_data_provider):
    sp = SmartPortfolio(mock_data_provider)
    sp.positions["AAPL"] = MagicMock()
    sp.positions["AAPL"].market_value.return_value = 1000
    value = sp.market_value()
    mock_data_provider.latest_price.assert_called_once_with("AAPL")
    assert value == 1000

def test_unrealized_pnl_calls_base_with_fetched_prices(mock_data_provider):
    sp = SmartPortfolio(mock_data_provider)
    sp.positions["AAPL"] = MagicMock()
    sp.positions["AAPL"].unrealized_pnl.return_value = 200
    pnl = sp.unrealized_pnl()
    mock_data_provider.latest_price.assert_called_once_with("AAPL")
    assert pnl == 200
