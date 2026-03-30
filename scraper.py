"""
Stock Market Ticker Info Script
"""

import sys
import yfinance as yf
from datetime import datetime
import pandas as pd


def fetch_stock_info(ticker_symbol: str) -> dict:
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info

    # Get today's price history (intraday fallback via fast_info)
    fast = ticker.fast_info

    return {
        "symbol": ticker_symbol.upper(),
        "name": info.get("longName", "N/A"),
        "exchange": info.get("exchange", "N/A"),
        "currency": info.get("currency", "USD"),
        "current_price": fast.last_price,
        "previous_close": fast.previous_close,
        "open": fast.open,
        "day_high": fast.day_high,
        "day_low": fast.day_low,
        "volume": fast.last_volume,
        "market_cap": info.get("marketCap"),
        "pe_ratio": info.get("trailingPE"),
        "sector": info.get("sector", "N/A"),
        "industry": info.get("industry", "N/A"),
    }


def format_large_number(n) -> str:
    if n is None:
        return "N/A"
    if n >= 1_000_000_000_000:
        return f"${n / 1_000_000_000_000:.2f}T"
    if n >= 1_000_000_000:
        return f"${n / 1_000_000_000:.2f}B"
    if n >= 1_000_000:
        return f"${n / 1_000_000:.2f}M"
    return f"${n:,.0f}"


def format_volume(v) -> str:
    if v is None:
        return "N/A"
    if v >= 1_000_000:
        return f"{v / 1_000_000:.2f}M"
    if v >= 1_000:
        return f"{v / 1_000:.1f}K"
    return str(v)


def print_stock_info(data: dict):
    current = data["current_price"]
    prev = data["previous_close"]

    if current is not None and prev is not None:
        change = current - prev
        change_pct = (change / prev) * 100
        arrow = "▲" if change >= 0 else "▼"
        change_str = f"{arrow} {abs(change):.2f} ({abs(change_pct):.2f}%)"
    else:
        change_str = "N/A"

    print(f"\n{'═' * 52}")
    print(f"  {data['symbol']}  —  {data['name']}")
    print(f"  {data['exchange']} · {data['sector']} · {data['industry']}")
    print(f"{'─' * 52}")
    print(f"  Price:          ${current:.2f} {data['currency']}" if current else "  Price:          N/A")
    print(f"  Change:         {change_str}")
    print(f"  Open:           ${data['open']:.2f}" if data["open"] else "  Open:           N/A")
    print(f"  Day High/Low:   ${data['day_high']:.2f} / ${data['day_low']:.2f}" if data["day_high"] else "  Day High/Low:   N/A")
    print(f"  Volume:         {format_volume(data['volume'])}")
    print(f"  Market Cap:     {format_large_number(data['market_cap'])}")
    print(f"  P/E Ratio:      {data['pe_ratio']:.2f}" if data["pe_ratio"] else "  P/E Ratio:      N/A")
    print(f"{'═' * 52}")

def build_dataframe(data):
    rows = []
    current = data["current_price"]
    prev = data["previous_close"]
    change = current - prev if current and prev else None
    change_pct = (change / prev * 100) if change and prev else None

    rows.append({
        "Symbol":       data["symbol"],
        "Name":         data["name"],
        "Price":        current,
        "Change":       round(change, 2) if change else None,
        "Change %":     round(change_pct, 2) if change_pct else None,
        "Open":         data["open"],
        "Day High":     data["day_high"],
        "Day Low":      data["day_low"],
        "Volume":       data["volume"],
        "Market Cap":   data["market_cap"],
        "P/E Ratio":    data["pe_ratio"],
        "Sector":       data["sector"],
    })

    return pd.DataFrame(rows).set_index("Symbol")

def main():
    tickers = sys.argv[1:] if len(sys.argv) > 1 else ["SNDK", "MU", "GOOGL"]

    print(f"\nFetching stock data at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ...")
    df = []
    for symbol in tickers:
        data = fetch_stock_info(symbol)
        data_df = build_dataframe(data)
        df.append(data_df)

    print(df)

if __name__ == "__main__":
    main()
