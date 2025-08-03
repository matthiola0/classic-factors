"""Factor signal definitions.

Each function takes a wide close-price DataFrame (index=date, columns=symbol)
and returns a signal DataFrame of the same shape. Convention: higher signal
value = higher expected forward return (i.e. signals are always oriented so
the "long" leg is the top quantile).
"""
import pandas as pd


def momentum(close: pd.DataFrame, lookback: int = 252, skip: int = 21) -> pd.DataFrame:
    """12-1 momentum: total return over `lookback` trading days, skipping the
    most recent `skip` days to avoid the short-term reversal effect.

    Default (252, 21) ≈ 12-month return skipping the last month.
    """
    return close.shift(skip) / close.shift(skip + lookback) - 1


def short_term_reversal(close: pd.DataFrame, lookback: int = 5) -> pd.DataFrame:
    """Negative of recent cumulative return — bets on mean reversion over
    short horizons (1 trading week by default).
    """
    return -(close / close.shift(lookback) - 1)


def low_volatility(close: pd.DataFrame, lookback: int = 60) -> pd.DataFrame:
    """Negative of rolling return std-dev — the low-vol anomaly: lower-vol
    names outperform on a risk-adjusted basis.
    """
    return -close.pct_change().rolling(lookback).std()


def size_adv(close: pd.DataFrame, volume: pd.DataFrame, lookback: int = 60) -> pd.DataFrame:
    """Liquidity-proxied size: negative of average dollar volume over `lookback`.

    True size uses market capitalization (price × shares outstanding). Without
    shares-outstanding data, average dollar volume (ADV) is the standard proxy
    since cap and ADV correlate ~0.8 for liquid names.
    """
    adv = (close * volume).rolling(lookback).mean()
    return -adv
