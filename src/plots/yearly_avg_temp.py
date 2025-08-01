import matplotlib.pyplot as plt
import pandas as pd

def plot_yearly_avg_temp(df):
    df = df.copy()
    df["time"] = pd.to_datetime(df["time"])
    df["year"] = df["time"].dt.year
    yearly_avg = df.groupby("year")["temp_avg_c"].mean()

    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(yearly_avg.index, yearly_avg.values, marker="o", linestyle="-", color="tomato", linewidth=2)

    ax.set_title("Yearly Avg Temp (°C)", fontsize=10)
    ax.set_xlabel("Year", fontsize=8)
    ax.set_ylabel("Temp (°C)", fontsize=8)

    # Show x-axis ticks every 5 years
    ax.set_xticks([year for year in yearly_avg.index if year % 5 == 0])
    ax.tick_params(labelsize=6)

    # Add grid and background for clarity
    ax.grid(True, linestyle="--", alpha=0.3)
    ax.set_facecolor("#f9f9f9")
    fig.tight_layout()
    return fig