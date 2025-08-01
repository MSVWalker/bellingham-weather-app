import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import pandas as pd

def plot_anomaly_scatter(df):
    df['year'] = df['time'].dt.year
    df['doy'] = df['time'].dt.dayofyear
    df = df[df['doy'] != 366]
    df['temp_avg_f'] = df['temp_avg_c'] * 9 / 5 + 32

    yearly_avg = df.groupby('year')['temp_avg_f'].mean()
    baseline = yearly_avg.mean()
    anomalies = yearly_avg - baseline
    anomaly_df = anomalies.reset_index()
    anomaly_df.columns = ['year', 'anomaly']

    norm = mcolors.Normalize(vmin=anomaly_df['year'].min(), vmax=anomaly_df['year'].max())
    cmap = cm.get_cmap('coolwarm')
    colors = cmap(norm(anomaly_df['year']))

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.scatter(anomaly_df['year'], anomaly_df['anomaly'], c=colors, edgecolor='black', s=160, alpha=0.85)
    ax.axhline(0, color='gray', linestyle='--', lw=1)

    def plus_formatter(x, pos):
        return f"+{x:.1f}°F" if x > 0 else f"{x:.1f}°F"
    ax.yaxis.set_major_formatter(FuncFormatter(plus_formatter))

    ax.set_title("Annual Temperature Anomalies — Bellingham", fontsize=18, weight='bold')
    ax.set_xlabel("Year")
    ax.set_ylabel("Above/Below Avg (°F)")
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    return fig