import matplotlib.pyplot as plt
import pandas as pd

def plot_monthly_avg_temp(df):
    df = df.copy()
    df["time"] = pd.to_datetime(df["time"])
    df["month"] = df["time"].dt.month

    # Group by month and calculate the mean temperature across all years
    monthly_avg = df.groupby("month")["temp_avg_c"].mean()

    # Month labels
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    fig, ax = plt.subplots(figsize=(5, 3))
    monthly_avg.plot(kind="bar", ax=ax, color="coral", width=0.8)

    ax.set_title("Avg Temp by Month (°C)", fontsize=10)
    ax.set_xlabel("Month", fontsize=8)
    ax.set_ylabel("Temp (°C)", fontsize=8)
    ax.set_xticks(range(12))
    ax.set_xticklabels(month_names, fontsize=7, rotation=0)
    ax.tick_params(axis='y', labelsize=7)
    fig.tight_layout()
    return fig