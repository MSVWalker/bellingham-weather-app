# app.py

import streamlit as st
import duckdb
import pandas as pd
import matplotlib.pyplot as plt

from src.plots.heatmap_streaks import plot_over_80_streaks
from src.plots.anomalies_scatter import plot_anomaly_scatter
from src.plots.top10_bar import plot_top10_hottest_years
from src.plots.record_calendar import plot_record_calendar
from src.plots.monthly_avg_temp import plot_monthly_avg_temp
from src.plots.yearly_avg_temp import plot_yearly_avg_temp
from src.features.on_this_day import plot_on_this_day


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

# Add custom visualizations
figures.append(plot_yearly_avg_temp(df))
figures.append(plot_monthly_avg_temp(df))
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
plot_on_this_day(df)

st.markdown("---")
st.caption("Data from Meteostat. Built with DuckDB, pandas, seaborn, matplotlib, and Streamlit.")