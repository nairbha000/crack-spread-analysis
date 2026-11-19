"""Seasonality: average crack spread and average monthly change by calendar month."""
import pandas as pd


def monthly_profile(df: pd.DataFrame, col: str = "crack_321") -> pd.DataFrame:
    """Level and month-over-month change by calendar month, averaged across years."""
    m = df[col].resample("ME").mean()
    prof = pd.DataFrame({"level": m, "change": m.diff()})
    prof["month"] = prof.index.month
    return prof.groupby("month").agg(avg_level=("level", "mean"), avg_change=("change", "mean"),
                                     pct_up=("change", lambda x: (x > 0).mean() * 100)).round(2)
