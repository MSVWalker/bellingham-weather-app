import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import pandas as pd

def plot_top10_hottest_years(df):
    df['year'] = df['time'].dt.year
    df['doy'] = df['time'].dt.dayofyear
    df = df[df['doy'] != 366]
    df['temp_avg_f'] = df['temp_avg_c'] * 9 / 5 + 32

    yearly_avg = df.groupby('year')['temp_avg_f'].mean()
    baseline_avg = yearly_avg.mean()
    anomalies = yearly_avg - baseline_avg

    top10 = anomalies.sort_values(ascending=False).head(10).sort_values()

    fig, ax = plt.subplots(figsize=(12, 6))
    x_pos = range(len(top10))
    bars = ax.bar(x_pos, top10.values, color='#ff5e4d', width=0.8, align='edge')
    bars[-1].set_color('#ff2a00')

    def plus_formatter(x, pos):
        return f"+{x:.1f}°F" if x >= 0 else f"{x:.1f}°F"
    ax.yaxis.set_major_formatter(FuncFormatter(plus_formatter))

    ax.set_xticks([x + 0.4 for x in x_pos])
    ax.set_xticklabels(top10.index.astype(str), fontsize=12)
    ax.set_title("10 Hottest Years on Record — Above Avg (°F)", fontsize=15, weight='bold')
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    return fig