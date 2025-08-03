"""Populate the qtools price cache for the three markets used by this repo.

Self-contained: uses the installed qtools public API rather than shelling
out to a sibling checkout. Idempotent — re-running verifies the parquet
cache (fast path).
"""
from __future__ import annotations

import sys
import time
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

from qtools.data.loaders.crypto import get_crypto_prices, get_top_pairs
from qtools.data.loaders.twse import get_tw50_constituents, get_tw_prices
from qtools.data.loaders.us import get_sp500_constituents, get_us_prices

START = "2015-01-01"
END = "2025-07-31"
CRYPTO_UNIVERSE_SIZE = 30  # requested; after history filter, ~25 survive


def log(msg: str) -> None:
    print(f"[{datetime.now():%H:%M:%S}] {msg}", flush=True)


def fetch_us():
    log("US: fetching S&P 500 constituents")
    tickers = get_sp500_constituents()
    log(f"US: {len(tickers)} tickers; downloading {START} -> {END}")
    t0 = time.time()
    df = get_us_prices(tickers, START, END, adjust=True)
    log(f"US: {len(df):,} rows in {time.time() - t0:.1f}s")
    return df


def fetch_tw():
    tickers = get_tw50_constituents()
    log(f"TW: downloading {len(tickers)} tickers {START} -> {END}")
    t0 = time.time()
    df = get_tw_prices(tickers, START, END, adjust=True)
    log(f"TW: {len(df):,} rows in {time.time() - t0:.1f}s")
    return df


def fetch_crypto():
    log(f"Crypto: fetching top {CRYPTO_UNIVERSE_SIZE} USDT pairs by volume")
    pairs = get_top_pairs(n=CRYPTO_UNIVERSE_SIZE, quote="USDT")
    log(f"Crypto: {len(pairs)} pairs; downloading daily {START} -> {END}")
    t0 = time.time()
    df = get_crypto_prices(pairs, START, END, interval="1d")
    log(f"Crypto: {len(df):,} rows in {time.time() - t0:.1f}s")
    return df


def main() -> int:
    sections = {"US": fetch_us, "TW": fetch_tw, "Crypto": fetch_crypto}
    results = {}
    for name, fn in sections.items():
        try:
            results[name] = fn()
        except Exception as e:
            log(f"{name}: FAILED -- {type(e).__name__}: {e}")
            results[name] = None

    print("\n=== Summary ===")
    for name, df in results.items():
        if df is None or df.empty:
            print(f"  {name:<7}: FAILED or empty")
        else:
            print(
                f"  {name:<7}: {len(df):>7,} rows  "
                f"{df['symbol'].nunique():>3} symbols  "
                f"{df['date'].min().date()} -> {df['date'].max().date()}"
            )
    return 0 if all(df is not None and not df.empty for df in results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
