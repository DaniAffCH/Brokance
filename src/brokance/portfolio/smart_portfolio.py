from .portfolio import Portfolio, Transaction
from brokance.data_ingestion.base import BaseDataProvider
from datetime import datetime
from typing import Literal


class SmartPortfolio(Portfolio):
    def __init__(self, data_provider: BaseDataProvider):
        super().__init__()
        self.data_provider = data_provider

    def _get_all_latest_prices(self):
        prices = {}
        for sym in self.positions.keys():
            prices[sym] = self.data_provider.latest_price(sym)
        return prices

    def add_transaction(self, symbol: str, quantity: float, date: datetime, type: Literal["buy", "sell", "dividend"]) -> None:
        if not self.data_provider.symbol_exists(symbol):
            raise ValueError(f"Ticker {symbol} not available in {self.data_provider.__class__.__name__}")
        
        tx = Transaction.from_provider(symbol, quantity, date, type, self.data_provider)
        super().add_transaction(tx)
        
    def market_value(self) -> float:
        latest_prices = self._get_all_latest_prices()
        return super().market_value(latest_prices)
    
    def unrealized_pnl(self) -> float:
        latest_prices = self._get_all_latest_prices()
        return super().unrealized_pnl(latest_prices)