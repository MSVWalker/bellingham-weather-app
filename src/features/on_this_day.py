# src/features/on_this_day.py

import streamlit as st
import pandas as pd
from datetime import datetime

def show_on_this_day(df: pd.DataFrame):
    """
    Display historical weather data for the current day (month/day) across all years.
    Assumes 'time' column is in datetime format and includes temp_high_c, temp_low_c, and precip_mm.
    """
    today = datetime.today()
    month = today.month
    day = today.day

    df_filtered = df[(df['time'].dt.month == month) & (df['time'].dt.day == day)].sort_values("time")

    st.markdown("## 📅 On This Day in Bellingham Weather History")

    if df_filtered.empty:
        st.info("No historical data available for this day.")
        return

    with st.expander(f"See historical data for {today.strftime('%B %d')}"):
        for _, row in df_filtered.iterrows():
            year = row['time'].year
            high = row.get('temp_high_c', 'N/A')
            low = row.get('temp_low_c', 'N/A')
            precip = row.get('precip_mm', 'N/A')
            st.write(f"**{year}** — High: {high}°C, Low: {low}°C, Precip: {precip} mm")