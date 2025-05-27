import json
from brokance.portfolio.portfolio import Portfolio, Transaction

def save_portfolio(portfolio: Portfolio, path: str) -> None:
    all_transactions = []
    for pos in portfolio.positions.values():
        for tx in pos.transactions:
            all_transactions.append(tx.to_dict())
    
    with open(path, "w") as f:
        json.dump(all_transactions, f, indent=2)

def load_portfolio(path: str) -> Portfolio:
    with open(path, "r") as f:
        data = json.load(f)
    
    p = Portfolio()
    for tx_data in data:
        tx = Transaction.from_dict(tx_data)
        p.add_transaction(tx)
    return p
