"""Crack spreads: the gross margin from turning crude into products, in $/bbl of crude."""
import pandas as pd


def add_cracks(prices: pd.DataFrame) -> pd.DataFrame:
    out = prices.copy()
    # 3-2-1: 3 bbl crude -> 2 bbl gasoline + 1 bbl diesel, expressed per barrel of crude
    out["crack_321"] = (2 * out["gasoline"] + out["diesel"] - 3 * out["wti"]) / 3
    out["gasoline_crack"] = out["gasoline"] - out["wti"]
    out["diesel_crack"] = out["diesel"] - out["wti"]
    return out


def yearly_summary(df: pd.DataFrame) -> pd.DataFrame:
    cols = ["wti", "crack_321", "gasoline_crack", "diesel_crack"]
    return df[cols].resample("YE").mean().round(2).rename_axis("year").set_index(
        df[cols].resample("YE").mean().index.year)


def summary_stats(df: pd.DataFrame) -> dict:
    c = df["crack_321"]
    return {
        "first_date": str(df.index[0].date()),
        "last_date": str(df.index[-1].date()),
        "years": round((df.index[-1] - df.index[0]).days / 365.25, 1),
        "trading_days": int(len(df)),
        "mean_321": round(float(c.mean()), 2),
        "median_321": round(float(c.median()), 2),
        "max_321": round(float(c.max()), 2),
        "max_321_date": str(c.idxmax().date()),
        "min_321": round(float(c.min()), 2),
        "min_321_date": str(c.idxmin().date()),
        "pct_days_negative_321": round(float((c < 0).mean() * 100), 2),
        "corr_daily_change_crack_vs_wti": round(float(c.diff().corr(df["wti"].diff())), 3),
    }
