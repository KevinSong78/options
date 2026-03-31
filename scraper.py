"""
Stock Market Ticker Info Script
"""

import sys
import yfinance as yf
from datetime import datetime
import pandas as pd
from utils import format_large_number, format_volume, build_dataframe

class StockInfo:
    def __init__(self, ticker_symbol: str):
        self.ticker_symbol = ticker_symbol.upper()

    def fetch_stock_info(self, ticker_symbol: str) -> dict:
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


def main():
    tickers = sys.argv[1:] if len(sys.argv) > 1 else ["SNDK", "MU", "GOOGL"]

    print(f"\nFetching stock data at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ...")

    frames = []
    for symbol in tickers:
        try:
            data = StockInfo.fetch_stock_info(symbol)   # fix 3: call via class name
            data_df = StockInfo.build_dataframe(data)   # fix 3: same here
            frames.append(data_df)
        except Exception as e:
            print(f"[ERROR] Could not fetch '{symbol}': {e}")

    if frames:
        df = pd.concat(frames)  # fix 4: concat the list into one df, don't just print a list
        pd.set_option("display.float_format", "{:.2f}".format)
        pd.set_option("display.max_columns", None)
        print(df.to_string())

if __name__ == "__main__":
    main()
