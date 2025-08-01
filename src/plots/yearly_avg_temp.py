# src/plots/daily_avg_temp.py

import matplotlib.pyplot as plt
import pandas as pd


def plot_yearly_avg_temp(df):
    df = df.copy()
    df["time"] = pd.to_datetime(df["time"])
    df["year"] = df["time"].dt.year
    yearly = df.groupby("year")["temp_avg_c"].mean()

    fig, ax = plt.subplots(figsize=(5, 3))
    yearly.plot(kind="bar", ax=ax, color="steelblue")
    ax.set_title("Yearly Avg Temp (°C)", fontsize=10)
    ax.set_xlabel("Year", fontsize=8)
    ax.set_ylabel("Temp (°C)", fontsize=8)
    ax.tick_params(labelsize=6)
    fig.tight_layout()
    return fig
