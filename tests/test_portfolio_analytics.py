import pytest
import numpy as np
from brokance.portfolio.analytics import (
    portfolio_return,
    time_weighted_return,
    volatility,
    sharpe_ratio,
    max_drawdown,
)

def test_portfolio_return():
    assert portfolio_return(100, 110) == pytest.approx(0.1)
    assert portfolio_return(200, 180) == pytest.approx(-0.1)
    assert portfolio_return(0, 100) == float("inf")

def test_time_weighted_return():
    assert time_weighted_return([100, 110, 121]) == pytest.approx((1.1 * 1.1) - 1)
    assert time_weighted_return([100]) == 0.0
    with pytest.raises(ValueError):
        time_weighted_return([])

def test_volatility():
    r = [0.01, 0.02, 0.03]
    expected = np.std(r)
    assert np.isclose(volatility(r), expected)

def test_sharpe_ratio():
    r = [0.05, 0.06, 0.04]
    risk_free = 0.02
    excess = [x - risk_free for x in r]
    expected = np.mean(excess) / np.std(r)
    assert np.isclose(sharpe_ratio(r, risk_free), expected)
    
    assert sharpe_ratio([0.0, 0.0, 0.0], 0.0) == float("inf")

def test_max_drawdown():
    assert max_drawdown([100, 90, 120, 80, 110]) == pytest.approx((120-80)/120)  # from 120 to 80
    assert max_drawdown([100, 105, 110]) == 0.0
    assert max_drawdown([0, 0]) == float("inf")
