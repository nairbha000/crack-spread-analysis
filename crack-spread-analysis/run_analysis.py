"""Run the full crack spread analysis.

Examples:
    python run_analysis.py --xls-dir data                 # EIA files saved in data/
    python run_analysis.py                                # download from EIA directly
    python run_analysis.py --region nyh --xls-dir data    # New York Harbor products instead of Gulf Coast
"""
import argparse
import json
from pathlib import Path

from crack import backtest
from crack.data import load_csv, load_prices
from crack.events import biggest_moves
from crack.plots import plot_backtest, plot_cracks, plot_seasonality
from crack.seasonality import monthly_profile
from crack.spreads import add_cracks, summary_stats, yearly_summary


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--region", choices=["gulf", "nyh"], default="gulf")
    p.add_argument("--xls-dir")
    p.add_argument("--csv")
    p.add_argument("--start", default="2010-01-01")
    p.add_argument("--split", default="2018-12-31", help="last date of the training period")
    p.add_argument("--cost", type=float, default=0.05, help="$/bbl charged per position change")
    p.add_argument("--out", default="outputs")
    a = p.parse_args()
    out = Path(a.out); out.mkdir(exist_ok=True)

    prices = load_csv(a.csv, a.start) if a.csv else load_prices(a.region, a.start, a.xls_dir)
    # Drop days with non-positive crude (WTI spot was -$36.98 on 2020-04-20). A crack spread
    # against a negative crude price measures a storage squeeze, not refining economics.
    dropped = prices.index[prices["wti"] <= 0]
    prices = prices[prices["wti"] > 0]
    df = add_cracks(prices)

    gas, dsl, c321 = (monthly_profile(df, c) for c in ("gasoline_crack", "diesel_crack", "crack_321"))
    bt, cum = backtest.run(df, a.split, cost=a.cost)
    years = yearly_summary(df)
    events = biggest_moves(df)

    plot_cracks(df, out / "cracks.png")
    plot_seasonality(gas, dsl, out / "seasonality.png")
    plot_backtest(cum, a.split, out / "backtest.png")
    years.to_csv(out / "yearly.csv"); events.to_csv(out / "biggest_moves.csv", index=False)
    c321.to_csv(out / "seasonality_321.csv")

    results = {"region": a.region, "dropped_negative_wti_days": [str(d.date()) for d in dropped],
               "summary": summary_stats(df), "backtest": bt,
               "gasoline_peak_month": int(gas["avg_level"].idxmax()),
               "diesel_peak_month": int(dsl["avg_level"].idxmax())}
    (out / "results.json").write_text(json.dumps(results, indent=2))
    print(json.dumps(results, indent=2)); print(years); print(events)


if __name__ == "__main__":
    main()
