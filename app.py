# app.py

import streamlit as st
import duckdb
import pandas as pd
import matplotlib.pyplot as plt

from src.plots.heatmap_streaks import plot_over_80_streaks
from src.plots.anomalies_scatter import plot_anomaly_scatter
from src.plots.top10_bar import plot_top10_hottest_years
from src.plots.record_calendar import plot_record_calendar

# --- Setup ---
st.set_page_config(page_title="Bellingham Weather Dashboard", layout="wide")
st.title("🌤️ Bellingham, WA Weather Dashboard")

# --- Load Data ---
con = duckdb.connect("data/weather.duckdb")
df = con.execute("SELECT * FROM weather_data ORDER BY time").fetchdf()
con.close()
df['time'] = pd.to_datetime(df['time'])

# --- Visuals Layout ---
st.markdown("---")
st.header("📈 Weather Visualizations")

figures = []

# Add Daily Average Temperature line chart
fig1, ax1 = plt.subplots(figsize=(6, 3.5))
df.set_index("time")["temp_avg_c"].plot(ax=ax1, title="Daily Avg Temp (°C)")
figures.append(fig1)

# Add Monthly Average Temperature bar chart
monthly = df.resample("M", on="time")["temp_avg_c"].mean()
fig2, ax2 = plt.subplots(figsize=(6, 3.5))
monthly.plot(kind='bar', ax=ax2, title="Monthly Avg Temp (°C)")
fig2.tight_layout()
figures.append(fig2)

# Add custom visualizations
figures.append(plot_over_80_streaks(df))
figures.append(plot_anomaly_scatter(df))
figures.append(plot_top10_hottest_years(df))
figures.append(plot_record_calendar(df))

# Display all figures in 3 columns
cols = st.columns(3)
for i, fig in enumerate(figures):
    with cols[i % 3]:
        st.pyplot(fig)

st.markdown("---")
st.caption("Data from Meteostat. Built with DuckDB, pandas, seaborn, matplotlib, and Streamlit.")
