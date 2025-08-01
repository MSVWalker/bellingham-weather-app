import matplotlib.pyplot as plt

def plot_daily_avg_temp(df):
    fig, ax = plt.subplots(figsize=(5, 3))
    df = df.copy()
    df = df.sort_values("time")
    df["temp_avg_c"].plot(ax=ax, linewidth=0.5, color="steelblue")
    ax.set_title("Daily Avg Temp (°C)", fontsize=10)
    ax.set_xlabel("Date", fontsize=8)
    ax.set_ylabel("Temp (°C)", fontsize=8)
    ax.tick_params(labelsize=6)
    fig.tight_layout()
    return fig