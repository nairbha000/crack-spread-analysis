import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def plot_cracks(df, path):
    fig, ax = plt.subplots(figsize=(11, 4.5))
    ax.plot(df.index, df["crack_321"].rolling(5).mean(), label="3-2-1 crack", linewidth=1.2, color="black")
    ax.plot(df.index, df["gasoline_crack"].rolling(5).mean(), label="Gasoline crack", linewidth=0.8, alpha=0.8)
    ax.plot(df.index, df["diesel_crack"].rolling(5).mean(), label="Diesel crack", linewidth=0.8, alpha=0.8)
    ax.axhline(0, color="gray", linewidth=0.6)
    ax.set_ylabel("$ per barrel of crude"); ax.set_title("U.S. refining margins (5-day average)")
    ax.legend(); fig.tight_layout(); fig.savefig(path, dpi=150); plt.close(fig)


def plot_seasonality(gas_prof, dsl_prof, path):
    fig, ax = plt.subplots(figsize=(9, 4))
    x = range(1, 13)
    ax.plot(x, gas_prof["avg_level"], marker="o", label="Gasoline crack")
    ax.plot(x, dsl_prof["avg_level"], marker="o", label="Diesel crack")
    ax.set_xticks(list(x)); ax.set_xticklabels(MONTHS)
    ax.set_ylabel("$ per barrel"); ax.set_title("Average crack by calendar month")
    ax.legend(); ax.grid(alpha=0.3); fig.tight_layout(); fig.savefig(path, dpi=150); plt.close(fig)


def plot_backtest(cum, split, path):
    fig, ax = plt.subplots(figsize=(11, 4))
    ax.plot(cum.index, cum, linewidth=1.2)
    ax.axhline(0, color="gray", linewidth=0.6)
    ax.set_ylabel("Cumulative $/bbl"); ax.set_title(f"Out-of-sample seasonal test (trained through {split}, after costs)")
    fig.tight_layout(); fig.savefig(path, dpi=150); plt.close(fig)
