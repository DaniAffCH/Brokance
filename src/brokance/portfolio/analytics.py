from typing import List
import numpy as np

def portfolio_return(start_value: float, end_value: float) -> float:
    return end_value/start_value - 1.0 if start_value != 0 else float("inf")

def time_weighted_return(values: List[float]) -> float:
    if not values:
        raise ValueError("Cannot compute time weighted return on an empty list")
    
    if len(values) == 1:
        return 0.0
    
    returns = [1.0 + portfolio_return(values[i], values[i+1]) for i in range(len(values)- 1)]
    return np.prod(returns) - 1.0

def volatility(returns: List[float]) -> float:
    return np.std(returns)

def sharpe_ratio(returns: List[float], risk_free_return: float = 0.0) -> float:
    vol = volatility(returns)
    excess_return = [r - risk_free_return for r in returns]
    
    return np.mean(excess_return) / vol if vol > 0 else float("inf")

def max_drawdown(values: List[float]) -> float:
    if not values or values[0] == 0:
        return float("inf")
    
    peak = values[0]
    max_dd = 0.0
    
    for v in values:
        peak = max(peak, v)
        drawdown = (peak - v) / peak
        max_dd = max(max_dd, drawdown)
        
    return max_dd