"""Out-of-sample seasonal test.

Train: learn which calendar months the crack spread tends to RISE in (average daily change > 0).
Test: on later, unseen years, hold a long crack position only in those months.
PnL is in $/bbl of crack spread. A cost per entry/exit (in $/bbl) is charged on every position change.
This is a test of whether seasonality persists, not a tradable strategy: spot cracks are not directly tradable
(a real trade would use RBOB, ULSD and WTI futures, with roll costs and margin).
"""
import numpy as np
import pandas as pd


def learn_months(train: pd.DataFrame, col: str = "crack_321") -> list[int]:
    chg = train[col].diff()
    avg = chg.groupby(train.index.month).mean()
    return sorted(int(m) for m in avg[avg > 0].index)


def run(df: pd.DataFrame, split: str, col: str = "crack_321", cost: float = 0.05) -> dict:
    train, test = df.loc[:split], df.loc[split:].iloc[1:]
    months = learn_months(train, col)
    pos = pd.Series(test.index.month.isin(months).astype(float), index=test.index)
    chg = test[col].diff().fillna(0)
    held = pos.shift(1).fillna(0)                      # today's PnL uses yesterday's position
    trades = pos.diff().abs().fillna(pos.iloc[0])
    pnl = held * chg - trades * cost
    always_long = chg.sum()

    # month-level results: each calendar month held in the test period is one "trade"
    monthly = pnl.resample("ME").sum()[pos.resample("ME").max() > 0]
    return {
        "train_period": f"{train.index[0].date()} to {train.index[-1].date()}",
        "test_period": f"{test.index[0].date()} to {test.index[-1].date()}",
        "months_long": months,
        "test_months_held": int(len(monthly)),
        "test_hit_rate_pct": round(float((monthly > 0).mean() * 100), 1) if len(monthly) else None,
        "test_total_pnl_per_bbl": round(float(pnl.sum()), 2),
        "test_buy_and_hold_pnl_per_bbl": round(float(always_long), 2),
        "cost_per_trade": cost,
        "num_position_changes": int(trades.sum()),
    }, pnl.cumsum()
