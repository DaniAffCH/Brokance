import pandas as pd
from brokance.portfolio.portfolio import Portfolio

def export_to_excel(portfolio: Portfolio, prices: dict, path: str) -> None:
    df = _portfolio_summary_df(portfolio, prices)
    df.to_excel(path, index=False)

def export_to_html(portfolio: Portfolio, prices: dict, path: str) -> None:
    df = _portfolio_summary_df(portfolio, prices)
    df.to_html(path, index=False)

def _portfolio_summary_df(portfolio: Portfolio, prices: dict) -> pd.DataFrame:
    data = []

    for symbol, pos in portfolio.positions.items():
        if symbol not in prices:
            raise KeyError(f"Missing price for symbol: {symbol}")
        price = prices[symbol]
        data.append({
            "Symbol": symbol,
            "Quantity": pos.quantity(),
            "Avg Cost": pos.average_cost(),
            "Market Price": price,
            "Market Value": pos.market_value(price),
            "Unrealized PnL": pos.unrealized_pnl(price)
        })

    return pd.DataFrame(data)
