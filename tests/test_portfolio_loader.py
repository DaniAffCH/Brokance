import tempfile
import os
import json
from datetime import datetime
from brokance.portfolio.portfolio import Portfolio, Transaction
from brokance.portfolio.loader import save_portfolio, load_portfolio

def test_save_and_load_portfolio(tmp_path):
    path = tmp_path / "portfolio.json"
    portfolio = Portfolio()
    tx1 = Transaction("AAPL", 10, 150.0, datetime(2023, 1, 1), "buy")
    tx2 = Transaction("AAPL", 5, 155.0, datetime(2023, 2, 1), "sell")
    tx3 = Transaction("TSLA", 8, 700.0, datetime(2023, 1, 15), "buy")

    portfolio.add_transaction(tx1)
    portfolio.add_transaction(tx2)
    portfolio.add_transaction(tx3)

    save_portfolio(portfolio, path)
    assert os.path.exists(path)

    loaded = load_portfolio(path)
    assert set(loaded.positions.keys()) == {"AAPL", "TSLA"}
    assert len(loaded.positions["AAPL"].transactions) == 2
    assert len(loaded.positions["TSLA"].transactions) == 1
    assert loaded.positions["AAPL"].transactions[0].price == 150.0
