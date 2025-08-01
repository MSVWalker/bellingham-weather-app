# src/plots/heatmap_streaks.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_over_80_streaks(df: pd.DataFrame):
    df = df.copy()
    df['time'] = pd.to_datetime(df['time'])
    df = df.sort_values('time')
    df['year'] = df['time'].dt.year
    df['temp_max_f'] = df['temp_high_c'] * 9 / 5 + 32
    df['over_80'] = df['temp_max_f'] > 80
    df['over_80'] = df['over_80'].fillna(False)

    streak_lengths = [1, 2, 3]
    results = []

    for year, group in df.groupby('year'):
        streaks, count = [], 0
        for val in group['over_80']:
            count = count + 1 if val else (streaks.append(count) or 0)
        if count > 0:
            streaks.append(count)
        streak_series = pd.Series(streaks)
        results.append({**{'year': year}, **{
            f"{l}_day+": (streak_series >= l).sum() for l in streak_lengths
        }})

    heat_df = pd.DataFrame(results).set_index('year')

    fig, ax = plt.subplots(figsize=(12, 5))
    sns.heatmap(heat_df.T, cmap="YlOrRd", annot=True, fmt='d',
                cbar_kws={'label': 'Number of Events'},
                linewidths=0.5, linecolor='gray', ax=ax)

    ax.set_title("Consecutive Days Over 80°F by Year", fontsize=16, weight='bold')
    ax.set_xlabel("Year")
    ax.set_ylabel("Streak Length")
    ax.tick_params(axis='x', rotation=45)
    ax.tick_params(axis='y', rotation=0)
    plt.tight_layout()

    return fig