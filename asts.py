"""
stock_prices.py
Fetches open, close, and 15-minute interval prices for a given stock ticker.

Requirements:
    pip install yfinance pandas

Usage:
    python stock_prices.py                        # defaults to AAPL, last 5 days
    python stock_prices.py TSLA                   # specify ticker
    python stock_prices.py TSLA --days 3          # last 3 days of 15-min data
    python stock_prices.py TSLA --output csv      # save results to a CSV file

Note:
    yfinance 15-minute data is available for the past 60 days only.
    Each trading day yields ~26 bars (9:30 AM – 4:00 PM ET).
"""

import argparse
import sys
import pandas as pd
import yfinance as yf


def fetch_stock_data(ticker: str, days: int = 5) -> dict:
    """
    Fetches daily open/close and 15-minute interval prices.

    Args:
        ticker: Stock ticker symbol (e.g. 'AAPL')
        days:   Number of trading days to look back (max 60 for 15-min data)

    Returns:
        dict with keys 'daily' and 'intraday', each a DataFrame
    """
    if days > 60:
        print("Warning: 15-minute data is only available for the past 60 days. Capping at 60.")
        days = 60

    period = f"{days}d"
    tk = yf.Ticker(ticker)

    # --- Daily open / close ---
    daily = tk.history(period=period, interval="1d")
    if daily.empty:
        print(f"Error: No data found for ticker '{ticker}'. Check the symbol and try again.")
        sys.exit(1)

    daily = daily[["Open", "Close", "Volume"]].copy()
    daily.index = daily.index.tz_localize(None) if daily.index.tz is None else daily.index.tz_convert("America/New_York").tz_localize(None)
    daily.index.name = "Date"
    daily.columns = ["Open", "Close", "Volume"]

    # --- 15-minute intraday ---
    intraday = tk.history(period=period, interval="15m")
    intraday = intraday[["Open", "Close", "High", "Low", "Volume"]].copy()
    intraday.index = (
        intraday.index.tz_localize(None)
        if intraday.index.tz is None
        else intraday.index.tz_convert("America/New_York").tz_localize(None)
    )
    intraday.index.name = "Datetime (ET)"

    return {"daily": daily, "intraday": intraday}


def print_summary(ticker: str, data: dict) -> None:
    """Pretty-prints daily and intraday data to the console."""
    daily: pd.DataFrame = data["daily"]
    intraday: pd.DataFrame = data["intraday"]

    print(f"\n{'='*60}")
    print(f"  {ticker.upper()} — Daily Open / Close")
    print(f"{'='*60}")
    print(daily.to_string(float_format="%.2f"))

    print(f"\n{'='*60}")
    print(f"  {ticker.upper()} — 15-Minute Interval Prices")
    print(f"{'='*60}")
    pd.set_option("display.max_rows", 200)
    print(intraday.to_string(float_format="%.2f"))
    print()


def save_to_csv(ticker: str, data: dict) -> None:
    """Saves daily and intraday DataFrames to CSV files."""
    daily_file = f"{ticker.upper()}_daily.csv"
    intraday_file = f"{ticker.upper()}_15min.csv"

    data["daily"].to_csv(daily_file)
    data["intraday"].to_csv(intraday_file)

    print(f"\nSaved daily data    →  {daily_file}")
    print(f"Saved intraday data →  {intraday_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Fetch open, close, and 15-minute interval prices for a stock ticker."
    )
    parser.add_argument(
        "ticker",
        nargs="?",
        default="AAPL",
        help="Stock ticker symbol (default: AAPL)",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=5,
        help="Number of trading days to fetch (default: 5, max: 60)",
    )
    parser.add_argument(
        "--output",
        choices=["print", "csv", "both"],
        default="print",
        help="Output mode: print to console, save to CSV, or both (default: print)",
    )
    args = parser.parse_args()

    ticker = args.ticker.upper()
    print(f"\nFetching data for {ticker} ({args.days} days) ...")

    data = fetch_stock_data(ticker, days=args.days)

    if args.output in ("print", "both"):
        print_summary(ticker, data)

    if args.output in ("csv", "both"):
        save_to_csv(ticker, data)

    # Return data dict for use as an imported module
    return data


if __name__ == "__main__":
    main()