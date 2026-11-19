"""Largest moves in the 3-2-1 crack, for event research."""
import pandas as pd


def biggest_moves(df: pd.DataFrame, col: str = "crack_321", window: int = 20, n: int = 8) -> pd.DataFrame:
    """Largest absolute changes over `window` trading days, keeping events at least 60 days apart."""
    chg = df[col].diff(window).dropna()
    picked = []
    for date in chg.abs().sort_values(ascending=False).index:
        if all(abs((date - p).days) > 60 for p in picked):
            picked.append(date)
        if len(picked) == n:
            break
    out = pd.DataFrame({"end_date": [d.date() for d in picked],
                        f"change_{window}d": [round(float(chg[d]), 2) for d in picked],
                        "crack_at_end": [round(float(df.loc[d, col]), 2) for d in picked]})
    return out.sort_values("end_date").reset_index(drop=True)
