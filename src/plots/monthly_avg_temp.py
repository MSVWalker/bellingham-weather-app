import matplotlib.pyplot as plt
import pandas as pd

def plot_monthly_avg_temp(df):
    df = df.copy()
    df["time"] = pd.to_datetime(df["time"])
    monthly = df.resample("M", on="time")["temp_avg_c"].mean()

    fig, ax = plt.subplots(figsize=(5, 3))
    monthly.plot(kind="bar", ax=ax, color="coral", width=0.8)
    ax.set_title("Monthly Avg Temp (°C)", fontsize=10)
    ax.set_xlabel("Month", fontsize=8)
    ax.set_ylabel("Temp (°C)", fontsize=8)
    ax.tick_params(labelsize=6)
    fig.tight_layout()
    return fig