# src/features/on_this_day.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def plot_on_this_day(df: pd.DataFrame):
    """
    Plots the average temperature on this calendar day (month/day) across all available years.
    Assumes df has 'time' and 'temp_avg_c' columns.
    """
    today = datetime.today()
    month = today.month
    day = today.day

    # Filter for today's calendar day across years
    df_filtered = df[(df['time'].dt.month == month) & (df['time'].dt.day == day)].copy()

    if df_filtered.empty:
        st.info("No historical data for today.")
        return

    df_filtered['year'] = df_filtered['time'].dt.year

    # Drop nulls if any
    df_filtered = df_filtered.dropna(subset=['temp_avg_c'])

    # Sort for clean line plot
    df_filtered = df_filtered.sort_values('year')

    # --- Plot ---
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(df_filtered['year'], df_filtered['temp_avg_c'], marker='o', color='orange')
    ax.set_title(f"📅 Avg Temp on {today.strftime('%b %d')} Over Time", fontsize=14)
    ax.set_xlabel("Year")
    ax.set_ylabel("Avg Temp (°C)")
    ax.grid(True, alpha=0.3)

    st.pyplot(fig)