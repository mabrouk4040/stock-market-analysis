"""
Member 2 – Data Processing & Analysis
Responsibilities: Data cleaning, field extraction, moving averages, daily change
"""

import pandas as pd
import numpy as np


def process_stock_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and enrich raw OHLCV DataFrame.

    Adds:
        - Daily Change: absolute price change vs previous close
        - Daily Change %: percentage change vs previous close
        - Typical Price: (High + Low + Close) / 3
    """
    df = df.copy()
    df.dropna(inplace=True)

    # Daily change
    df["Daily Change"]   = df["Close"].diff()
    df["Daily Change %"] = df["Close"].pct_change() * 100

    # Typical price (used for some indicators)
    df["Typical Price"]  = (df["High"] + df["Low"] + df["Close"]) / 3

    return df


def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute common technical indicators on top of processed OHLCV data.

    Adds:
        - MA7:  7-period simple moving average
        - MA20: 20-period simple moving average
        - MA50: 50-period simple moving average (if enough data)
        - EMA12, EMA26: Exponential moving averages
        - MACD, Signal Line
        - Bollinger Bands (upper, middle, lower)
        - RSI (14-period)
        - VWAP
    """
    df = df.copy()

    # ── Simple Moving Averages ──────────────────────────────────────────────
    df["MA7"]  = df["Close"].rolling(window=7,  min_periods=1).mean()
    df["MA20"] = df["Close"].rolling(window=20, min_periods=1).mean()
    df["MA50"] = df["Close"].rolling(window=50, min_periods=1).mean()

    # ── Exponential Moving Averages ─────────────────────────────────────────
    df["EMA12"] = df["Close"].ewm(span=12, adjust=False).mean()
    df["EMA26"] = df["Close"].ewm(span=26, adjust=False).mean()

    # ── MACD ────────────────────────────────────────────────────────────────
    df["MACD"]        = df["EMA12"] - df["EMA26"]
    df["MACD_Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
    df["MACD_Hist"]   = df["MACD"] - df["MACD_Signal"]

    # ── Bollinger Bands ─────────────────────────────────────────────────────
    rolling_std       = df["Close"].rolling(window=20, min_periods=1).std()
    df["BB_Middle"]   = df["MA20"]
    df["BB_Upper"]    = df["MA20"] + 2 * rolling_std
    df["BB_Lower"]    = df["MA20"] - 2 * rolling_std

    # ── RSI ─────────────────────────────────────────────────────────────────
    delta  = df["Close"].diff()
    gain   = delta.clip(lower=0)
    loss   = -delta.clip(upper=0)
    avg_g  = gain.rolling(window=14, min_periods=1).mean()
    avg_l  = loss.rolling(window=14, min_periods=1).mean()
    rs     = avg_g / avg_l.replace(0, np.nan)
    df["RSI"] = 100 - (100 / (1 + rs))

    # ── VWAP ────────────────────────────────────────────────────────────────
    cum_vol_price = (df["Typical Price"] * df["Volume"]).cumsum()
    cum_vol       = df["Volume"].cumsum()
    df["VWAP"]    = cum_vol_price / cum_vol

    return df


def get_summary_stats(df: pd.DataFrame) -> dict:
    """
    Return a dict of summary statistics for quick display.
    """
    return {
        "current_price":  df["Close"].iloc[-1],
        "period_high":    df["High"].max(),
        "period_low":     df["Low"].min(),
        "avg_volume":     df["Volume"].mean(),
        "total_return":   (df["Close"].iloc[-1] / df["Close"].iloc[0] - 1) * 100,
        "volatility":     df["Daily Change %"].std(),
        "avg_daily_chg":  df["Daily Change %"].mean(),
    }
