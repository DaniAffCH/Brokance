import pytest
from datetime import datetime
from brokance.portfolio.portfolio import Transaction, Position, Portfolio

def make_tx(symbol="AAPL", qty=1, price=100, ttype="buy"):
    return Transaction(symbol=symbol, quantity=qty, price=price, date=datetime.now(), type=ttype)

def test_add_transaction_symbol_mismatch():
    pos = Position("AAPL")
    tx = make_tx(symbol="GOOG")
    with pytest.raises(ValueError):
        pos.add_transaction(tx)

def test_quantity_simple_buys_and_sells():
    pos = Position("AAPL")
    pos.add_transaction(make_tx(qty=10, ttype="buy"))
    pos.add_transaction(make_tx(qty=3, ttype="sell"))
    assert pos.quantity() == 7

def test_quantity_ignores_dividends():
    pos = Position("AAPL")
    pos.add_transaction(make_tx(qty=10, ttype="buy"))
    pos.add_transaction(make_tx(qty=1, ttype="dividend"))
    assert pos.quantity() == 10

def test_average_cost_single_buy():
    pos = Position("AAPL")
    pos.add_transaction(make_tx(qty=10, price=100, ttype="buy"))
    assert pos.average_cost() == 100

def test_average_cost_multiple_buys():
    pos = Position("AAPL")
    pos.add_transaction(make_tx(qty=10, price=100, ttype="buy"))
    pos.add_transaction(make_tx(qty=20, price=110, ttype="buy"))
    expected = (10*100 + 20*110) / 30
    assert pos.average_cost() == pytest.approx(expected)

def test_average_cost_no_buys():
    pos = Position("AAPL")
    assert pos.average_cost() == 0.0

def test_market_value():
    pos = Position("AAPL")
    pos.add_transaction(make_tx(qty=5, ttype="buy"))
    pos.add_transaction(make_tx(qty=2, ttype="sell"))
    price = 50
    expected = 3 * price
    assert pos.market_value(price) == expected

def test_unrealized_pnl():
    pos = Position("AAPL")
    pos.add_transaction(make_tx(qty=10, price=100, ttype="buy"))
    price = 120
    expected_pnl = (price - 100) * 10
    assert pos.unrealized_pnl(price) == expected_pnl

def test_add_single_transaction():
    p = Portfolio()
    tx = Transaction("AAPL", 10, 150.0, datetime.now(), "buy")
    p.add_transaction(tx)

    assert "AAPL" in p.positions
    assert p.positions["AAPL"].quantity() == 10
    assert p.positions["AAPL"].average_cost() == 150.0

def test_market_value():
    p = Portfolio()
    p.add_transaction(Transaction("AAPL", 10, 150.0, datetime.now(), "buy"))
    p.add_transaction(Transaction("GOOG", 5, 100.0, datetime.now(), "buy"))

    prices = {"AAPL": 160.0, "GOOG": 120.0}
    assert p.market_value(prices) == 10 * 160.0 + 5 * 120.0

def test_unrealized_pnl():
    p = Portfolio()
    p.add_transaction(Transaction("AAPL", 10, 150.0, datetime.now(), "buy"))
    prices = {"AAPL": 170.0}
    assert p.unrealized_pnl(prices) == (170 - 150) * 10

def test_price_missing_key_error_market_value():
    p = Portfolio()
    p.add_transaction(Transaction("AAPL", 10, 150.0, datetime.now(), "buy"))
    with pytest.raises(KeyError):
        p.market_value({})  # Missing AAPL

def test_price_missing_key_error_unrealized_pnl():
    p = Portfolio()
    p.add_transaction(Transaction("AAPL", 10, 150.0, datetime.now(), "buy"))
    with pytest.raises(KeyError):
        p.unrealized_pnl({})  # Missing AAPL
        