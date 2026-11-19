import numpy as np
import pandas as pd

from crack.risk import max_drawdown, risk_metrics, sharpe


def test_max_drawdown_known_path():
    idx = pd.bdate_range("2024-01-01", periods=6)
    pnl = pd.Series([1.0, 2.0, -4.0, -1.0, 3.0, 1.0], index=idx)   # cum: 1, 3, -1, -2, 1, 2
    dd, start, trough = max_drawdown(pnl)
    assert dd == -5.0
    assert start == str(idx[1].date()) and trough == str(idx[3].date())


def test_sharpe_sign_and_zero_vol():
    idx = pd.bdate_range("2024-01-01", periods=300)
    rng = np.random.default_rng(1)
    assert sharpe(pd.Series(1.0 + rng.normal(0, 1, 300), index=idx)) > 0
    assert np.isnan(sharpe(pd.Series(np.zeros(300), index=idx)))


def test_risk_metrics_keys():
    idx = pd.bdate_range("2024-01-01", periods=50)
    m = risk_metrics(pd.Series(np.linspace(-1, 1, 50), index=idx))
    assert set(m) >= {"max_drawdown_per_bbl", "sharpe_annualized", "worst_day_per_bbl"}
