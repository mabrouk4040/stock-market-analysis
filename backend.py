"""
Member 1 – Project Lead / Backend Developer
Responsibilities: API Integration, Stock Data Fetching, Validation, Error Handling
"""

import re
import yfinance as yf


def validate_symbol(symbol: str) -> bool:
    """
    Validate that a stock symbol looks reasonable.
    Rules: 1–5 uppercase letters, optionally followed by . and more letters (e.g. BRK.B)
    """
    if not symbol:
        return False
    pattern = r'^[A-Z]{1,5}(\.[A-Z]{1,2})?$'
    return bool(re.match(pattern, symbol.upper()))


def fetch_stock_data(symbol: str, period: str = "1mo"):
    """
    Fetch historical OHLCV stock data from Yahoo Finance.

    Args:
        symbol: Stock ticker symbol (e.g. "AAPL")
        period: Time period string — "7d", "1mo", "3mo", "6mo", "1y"

    Returns:
        (DataFrame, error_message) — one of them will be None
    """
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period)

        if hist is None or hist.empty:
            return None, (
                f'No data found for "{symbol}". '
                "The symbol may be delisted, invalid, or not available on Yahoo Finance."
            )

        # Keep only the columns we need
        cols = [c for c in ["Open", "High", "Low", "Close", "Volume"] if c in hist.columns]
        hist = hist[cols]
        hist.index = hist.index.tz_localize(None)   # remove timezone for cleaner display

        return hist, None

    except Exception as e:
        return None, f"Error fetching data for {symbol}: {str(e)}"


def get_stock_info(symbol: str):
    """
    Fetch company metadata from Yahoo Finance.

    Returns:
        (info_dict, error_message) — info_dict may be partial even on success
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info

        if not info or len(info) <= 1:
            return None, "Company info not available for this symbol."

        return info, None

    except Exception as e:
        return None, f"Could not load company info: {str(e)}"
