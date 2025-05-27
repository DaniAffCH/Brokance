from brokance.portfolio.portfolio import Portfolio, Transaction
from brokance.portfolio.export import export_to_excel, export_to_html
from brokance.data_ingestion.factory import get_data_provider

from datetime import datetime, timedelta


p = Portfolio()
tx1 = Transaction("AAPL", 10, 150.0, datetime(2023, 4, 14), "buy")
tx2 = Transaction("AAPL", 5, 155.0, datetime(2023, 6, 1), "sell")
tx3 = Transaction("TSLA", 3, 700.0, datetime(2023, 4, 15), "buy")

p.add_transaction(tx1)
p.add_transaction(tx2)
p.add_transaction(tx3)

excel_path = "portfolio.html"

dataProvider = get_data_provider("yfinance")

prices = {}
yesterday = datetime.now() - timedelta(days=3)
for sym, pos in p.positions.items():
    prices[sym] = float(dataProvider.fetch(sym, yesterday)["Close", sym].iloc[0])
export_to_html(p, prices, excel_path)
