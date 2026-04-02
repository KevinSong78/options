
import sys
import yfinance as yf
from datetime import datetime
import pandas as pd

def fetch_options_chain(self, expiration: str = None) -> dict:
    ticker = yf.Ticker(self.ticker_symbol)

    # Use nearest expiration if none specified
    expirations = ticker.options
    if not expirations:
        raise ValueError(f"No options data available for {self.ticker_symbol}")

    exp = expiration if expiration in expirations else expirations[0]

    chain = ticker.option_chain(exp)

    return {
        "ticker": self.ticker_symbol,
        "expiration": exp,
        "available_expirations": list(expirations),
        "calls": chain.calls,   # DataFrame
        "puts": chain.puts,     # DataFrame
    }