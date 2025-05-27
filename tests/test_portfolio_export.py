import pandas as pd
from brokance.portfolio.portfolio import Portfolio, Transaction
from brokance.portfolio.export import export_to_excel, export_to_html

def test_export_to_excel(tmp_path):
    p = Portfolio()
    p.add_transaction(Transaction(symbol="AAPL", quantity=10, price=150, date=pd.Timestamp("2023-01-01"), type="buy"))
    prices = {"AAPL": 160}

    excel_path = tmp_path / "portfolio.xlsx"
    export_to_excel(p, prices, excel_path)

    assert excel_path.exists()
    df_excel = pd.read_excel(excel_path)
    assert "Symbol" in df_excel.columns
    assert df_excel["Symbol"].iloc[0] == "AAPL"


def test_export_to_html(tmp_path):
    p = Portfolio()
    p.add_transaction(Transaction(symbol="AAPL", quantity=10, price=150, date=pd.Timestamp("2023-01-01"), type="buy"))
    prices = {"AAPL": 160}

    html_path = tmp_path / "portfolio.html"
    export_to_html(p, prices, html_path)

    assert html_path.exists()
    with open(html_path) as f:
        html_content = f.read()
    assert "<table" in html_content
    assert "AAPL" in html_content
