import numpy as np

from crack import backtest
from crack.seasonality import monthly_profile
from crack.spreads import add_cracks


def test_learns_spring_months_for_seasonal_crack(prices):
    df = add_cracks(prices)
    months = backtest.learn_months(df.loc[:"2017-12-31"], "gasoline_crack")
    assert 3 in months and 4 in months          # rising into the spring peak
    assert 9 not in months and 10 not in months  # falling after summer


def test_no_lookahead_training_uses_only_past(prices):
    df = add_cracks(prices)
    altered = df.copy()
    altered.loc["2020-01-01":, "crack_321"] += 1000   # change only the test period
    assert backtest.learn_months(df.loc[:"2018-12-31"]) == backtest.learn_months(altered.loc[:"2018-12-31"])


def test_seasonal_signal_beats_zero_out_of_sample(prices):
    df = add_cracks(prices)
    res, cum = backtest.run(df, "2017-12-31", col="gasoline_crack", cost=0.0)
    assert res["test_total_pnl_per_bbl"] > 0
    assert np.isclose(cum.iloc[-1], res["test_total_pnl_per_bbl"], atol=0.01)


def test_costs_reduce_pnl(prices):
    df = add_cracks(prices)
    free, _ = backtest.run(df, "2017-12-31", cost=0.0)
    costly, _ = backtest.run(df, "2017-12-31", cost=1.0)
    assert costly["test_total_pnl_per_bbl"] < free["test_total_pnl_per_bbl"]


def test_monthly_profile_has_12_months(prices):
    assert len(monthly_profile(add_cracks(prices))) == 12
