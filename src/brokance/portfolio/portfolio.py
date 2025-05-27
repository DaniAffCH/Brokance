from datetime import datetime
from typing import Literal, Dict
from dataclasses import dataclass, asdict

@dataclass
class Transaction:
    symbol: str
    quantity: float
    price: float
    date: datetime
    type: Literal["buy", "sell", "dividend"]
    
    def to_dict(self):
        d = asdict(self)
        d["date"] = self.date.isoformat()
        return d

    @staticmethod
    def from_dict(d):
        return Transaction(
            symbol=d["symbol"],
            quantity=d["quantity"],
            price=d["price"],
            date=datetime.fromisoformat(d["date"]),
            type=d["type"]
        )

class Position:
    
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.transactions = []
        
    def add_transaction(self, tx: Transaction) -> None:
        if tx.symbol != self.symbol:
            raise ValueError("Transaction symbol does not match position symbol")
        self.transactions.append(tx)
        
    def quantity(self) -> float:
        return sum([tx.quantity if tx.type == "buy" else -tx.quantity for tx in self.transactions if tx.type in ["buy", "sell"]])

    def average_cost(self) -> float:
        total_cost = sum(tx.price * tx.quantity for tx in self.transactions if tx.type == "buy")
        total_quantity = sum(tx.quantity for tx in self.transactions if tx.type == "buy")
        return total_cost / total_quantity if total_quantity > 0 else 0.0
    
    def market_value(self, price: float):
        return price * self.quantity()
    
    def unrealized_pnl(self, price: float) -> float:
        return self.market_value(price) - (self.average_cost() * self.quantity())
    
class Portfolio:
    def __init__(self):
        self.positions = {}
        
    def add_transaction(self, tx: Transaction) -> None:
        if tx.symbol not in self.positions:
            self.positions[tx.symbol] = Position(tx.symbol)
            
        self.positions[tx.symbol].add_transaction(tx)
        
    def market_value(self, prices: Dict[str, float]) -> float:
        value = 0
        for sym, pos in self.positions.items():
            if sym not in prices:
                raise KeyError(f"Missing price for symbol: {sym}")
            value += pos.market_value(prices[sym])
        return value
    
    def unrealized_pnl(self, prices: Dict[str, float]) -> float:
        pnl = 0
        for sym, pos in self.positions.items():
            if sym not in prices:
                raise KeyError(f"Missing price for symbol: {sym}")
            pnl += pos.unrealized_pnl(prices[sym])
        return pnl
    