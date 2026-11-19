"""Load daily EIA spot prices for crude, gasoline and ULSD.

Crude is in $/barrel. Gasoline and ULSD are in $/gallon and converted to $/barrel (x 42).
Files come from EIA's public history spreadsheets (sheet "Data 1", two header rows).
"""
import os
import pandas as pd

GALLONS_PER_BARREL = 42

# EIA series IDs. Gulf Coast products pair naturally with WTI: most U.S. refining capacity is on the Gulf.
SERIES = {
    "gulf": {"wti": "RWTC", "gasoline": "EER_EPMRU_PF4_RGC_DPG", "diesel": "EER_EPD2DXL0_PF4_RGC_DPG"},
    "nyh": {"wti": "RWTC", "gasoline": "EER_EPMRU_PF4_Y35NY_DPG", "diesel": "EER_EPD2DXL0_PF4_Y35NY_DPG"},
}
XLS_URL = "https://www.eia.gov/dnav/pet/hist_xls/{series}d.xls"


def _read_eia_xls(src):
    df = pd.read_excel(src, sheet_name="Data 1", skiprows=2)
    df = df.iloc[:, :2]
    df.columns = ["date", "value"]
    df["date"] = pd.to_datetime(df["date"])
    return df.dropna().set_index("date")["value"].astype(float)


def load_prices(region="gulf", start="2010-01-01", xls_dir=None):
    """Return a DataFrame with wti ($/bbl), gasoline and diesel ($/bbl), on days all three traded."""
    ids = SERIES[region]
    out = {}
    for name, series in ids.items():
        src = os.path.join(xls_dir, f"{series}d.xls") if xls_dir else XLS_URL.format(series=series)
        s = _read_eia_xls(src)
        out[name] = s * GALLONS_PER_BARREL if name in ("gasoline", "diesel") else s
    df = pd.DataFrame(out).sort_index()
    df.index.name = "date"
    return df.loc[start:].dropna()


def load_csv(path, start="2010-01-01"):
    """CSV with columns date, wti, gasoline, diesel, all already in $/bbl."""
    df = pd.read_csv(path, parse_dates=["date"]).set_index("date").sort_index()
    return df.loc[start:, ["wti", "gasoline", "diesel"]].dropna()
