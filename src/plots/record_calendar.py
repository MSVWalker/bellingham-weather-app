# src/plots/record_calendar.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import calendar
from datetime import datetime

def plot_record_calendar(df):
    # --- Prepare Data ---
    df['time'] = pd.to_datetime(df['time'])
    df['year'] = df['time'].dt.year
    df['month'] = df['time'].dt.month
    df['day'] = df['time'].dt.day
    df['weekday'] = df['time'].dt.weekday
    df['week_of_month'] = df['time'].apply(lambda x: (x.day - 1) // 7)
    df['temp_avg_f'] = df['temp_avg_c'] * 9 / 5 + 32
    df['doy'] = df['time'].dt.dayofyear
    df = df[df['doy'] != 366]
    df = df.sort_values('time')

    # --- Rolling Record Tracker ---
    historical_max = pd.Series(-np.inf, index=range(1, 366))
    records = []

    for _, row in df.iterrows():
        doy = row['doy']
        temp = row['temp_avg_f']
        if pd.notna(temp) and temp > historical_max.get(doy, -np.inf):
            historical_max[doy] = temp
            records.append({
                'date': row['time'],
                'year': row['year'],
                'month': row['month'],
                'day': row['day'],
                'weekday': row['weekday'],
                'week_of_month': (row['day'] - 1) // 7
            })

    record_df = pd.DataFrame(records)

    # --- Use all years from 2015 to 2025 ---
    all_years = list(range(2015, 2026))
    record_df = record_df[record_df['year'].isin(all_years)]

    # --- Layout Settings ---
    cell_size = 0.2
    cell_gap = 0.02
    month_gap = 0.10
    year_gap = 0.70

    # --- Compute total height needed ---
    max_y_offset = 0
    for month in range(1, 13):
        first_weekday = pd.Timestamp(year=2015, month=month, day=1).weekday()
        num_days = calendar.monthrange(2015, month)[1]
        num_weeks = ((num_days + first_weekday - 1) // 7) + 1
        max_y_offset += num_weeks * (cell_size + cell_gap) + month_gap

    # --- Create Figure ---
    fig_width = max(13, len(all_years) * (7 * (cell_size + cell_gap) + year_gap))
    fig, ax = plt.subplots(figsize=(fig_width, max_y_offset * 1.05))
    ax.set_xlim(0, len(all_years) * (7 * (cell_size + cell_gap) + year_gap))
    ax.set_ylim(max_y_offset + 1.2 * cell_size, 0)
    ax.set_aspect('equal')
    ax.set_yticks([])
    ax.set_xticks([])

    today = datetime.today().date()

    for i, year in enumerate(all_years):
        year_df = record_df[record_df['year'] == year]
        x_offset = i * (7 * (cell_size + cell_gap) + year_gap)
        y_offset = 0

        for month in range(1, 13):
            num_days = calendar.monthrange(year, month)[1]
            first_day = pd.Timestamp(year=year, month=month, day=1)
            first_weekday = first_day.weekday()

            for day in range(1, num_days + 1):
                date = pd.Timestamp(year=year, month=month, day=day).date()
                if year == today.year and date > today:
                    continue

                weekday = date.weekday()
                week_row = ((day + first_weekday - 1) // 7)
                x = x_offset + weekday * (cell_size + cell_gap)
                y = y_offset + week_row * (cell_size + cell_gap)

                ax.add_patch(Rectangle(
                    (x, y), cell_size, cell_size,
                    facecolor='#e0e0e0', edgecolor='white', linewidth=0.2
                ))

                if date == today:
                    ax.add_patch(Rectangle(
                        (x, y), cell_size, cell_size,
                        facecolor='none', edgecolor='black', linewidth=1.5
                    ))
                    ax.text(x + cell_size / 2, y + cell_size / 2 + 0.25, today.strftime('%b %d'),
                            ha='center', va='center', fontsize=15.0, fontweight='bold', color='#ff6347')

            for _, row in year_df[year_df['month'] == month].iterrows():
                date = pd.Timestamp(year=row['year'], month=row['month'], day=row['day']).date()
                if year == today.year and date > today:
                    continue

                weekday = row['weekday']
                day = row['day']
                first_weekday = pd.Timestamp(year=year, month=month, day=1).weekday()
                week_row = ((day + first_weekday - 1) // 7)
                x = x_offset + weekday * (cell_size + cell_gap)
                y = y_offset + week_row * (cell_size + cell_gap)

                ax.add_patch(Rectangle(
                    (x, y), cell_size, cell_size,
                    facecolor='#ff6347', edgecolor='white', linewidth=0.2
                ))

            if i == 0:
                mid_y = y_offset + 1.5 * (cell_size + cell_gap)
                ax.text(x_offset - 0.6, mid_y, calendar.month_abbr[month],
                        va='center', ha='right', fontsize=10)

            num_weeks = ((num_days + first_weekday - 1) // 7) + 1
            y_offset += num_weeks * (cell_size + cell_gap) + month_gap

        xtick_pos = [x_offset + (j + 0.5) * (cell_size + cell_gap) for j in range(7)]
        for j, label in enumerate(['M', 'T', 'W', 'T', 'F', 'S', 'S']):
            ax.text(xtick_pos[j], -0.4, label, ha='center', va='bottom', fontsize=9)

        ax.text(x_offset + 3.5 * (cell_size + cell_gap), -1.2, str(year),
                ha='center', va='bottom', fontsize=12)

    plt.suptitle("Record-Breaking Daily Highs (2015–2025)", fontsize=11, y=1.05)
    plt.axis('off')
    return fig