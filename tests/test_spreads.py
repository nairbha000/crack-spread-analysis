import numpy as np
import pandas as pd

from crack.spreads import add_cracks, summary_stats


def test_321_formula():
    df = pd.DataFrame({"wti": [70.0], "gasoline": [94.5], "diesel": [105.0]}, index=pd.to_datetime(["2024-01-02"]))
    out = add_cracks(df)
    assert np.isclose(out["crack_321"].iloc[0], (2 * 94.5 + 105 - 3 * 70) / 3)
    assert np.isclose(out["gasoline_crack"].iloc[0], 24.5)
    assert np.isclose(out["diesel_crack"].iloc[0], 35.0)


def test_321_is_weighted_average_of_product_cracks(prices):
    out = add_cracks(prices)
    expected = (2 * out["gasoline_crack"] + out["diesel_crack"]) / 3
    assert np.allclose(out["crack_321"], expected)


def test_summary_has_no_nans(prices):
    s = summary_stats(add_cracks(prices))
    assert all(v == v for v in s.values() if isinstance(v, float))
