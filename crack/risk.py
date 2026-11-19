"""Risk metrics for a daily PnL series measured in $/bbl of spread.

There is no capital base for a spread position, so the Sharpe ratio here is the annualized
mean daily PnL divided by its standard deviation (an information ratio on PnL), not a return on capital.
"""
import numpy as np
import pandas as pd


def max_drawdown(pnl: pd.Series) -> tuple[float, str, str]:
    """Largest peak-to-trough fall in cumulative PnL, with the peak and trough dates."""
    cum = pnl.cumsum()
    peak = cum.cummax()
    dd = cum - peak
    trough = dd.idxmin()
    start = cum.loc[:trough].idxmax()
    return float(dd.min()), str(pd.Timestamp(start).date()), str(pd.Timestamp(trough).date())


def sharpe(pnl: pd.Series, periods_per_year: int = 252, active_only: bool = False) -> float:
    s = pnl[pnl != 0] if active_only else pnl
    if len(s) < 2 or s.std() == 0:
        return float("nan")
    return float(s.mean() / s.std() * np.sqrt(periods_per_year))


def risk_metrics(pnl: pd.Series) -> dict:
    dd, start, trough = max_drawdown(pnl)
    return {
        "max_drawdown_per_bbl": round(dd, 2),
        "max_drawdown_start": start,
        "max_drawdown_trough": trough,
        "sharpe_annualized": round(sharpe(pnl), 2),
        "worst_day_per_bbl": round(float(pnl.min()), 2),
        "best_day_per_bbl": round(float(pnl.max()), 2),
    }
