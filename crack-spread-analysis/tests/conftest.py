import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def prices():
    idx = pd.bdate_range("2012-01-02", "2022-12-30")
    rng = np.random.default_rng(0)
    wti = 70 + rng.normal(0, 1, len(idx)).cumsum() * 0.3
    season = 6 * np.sin(2 * np.pi * (idx.dayofyear - 60) / 365)       # gasoline peaks in late spring
    gasoline = wti + 15 + season + rng.normal(0, 1, len(idx))
    diesel = wti + 20 - 0.5 * season + rng.normal(0, 1, len(idx))
    return pd.DataFrame({"wti": wti, "gasoline": gasoline, "diesel": diesel}, index=idx)
