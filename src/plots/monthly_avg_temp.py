import matplotlib.pyplot as plt
import pandas as pd


def plot_monthly_avg_temp(df):
    df = df.copy()
    df["time"] = pd.to_datetime(df["time"])

    # Resample monthly average temperature
    monthly = df.resample("M", on="time")["temp_avg_c"].mean()
    monthly.index = monthly.index.strftime("%Y-%m")  # Clean x-axis labels

    fig, ax = plt.subplots(figsize=(5, 3))
    monthly.plot(kind="bar", ax=ax, color="coral", width=0.8)

    ax.set_title("Monthly Avg Temp (°C)", fontsize=10)
    ax.set_xlabel("Month", fontsize=8)
    ax.set_ylabel("Temp (°C)", fontsize=8)

    # Limit number of x-ticks shown
    xticks = ax.get_xticks()
    ax.set_xticks(xticks[::max(1, len(xticks) // 10)])  # Show ~10 evenly spaced ticks

    ax.tick_params(axis='x', labelsize=6, rotation=45)
    ax.tick_params(axis='y', labelsize=7)
    fig.tight_layout()
    return fig