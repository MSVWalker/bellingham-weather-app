import streamlit as st
import duckdb
import pandas as pd

from src.plots.heatmap_streaks import plot_over_80_streaks
from src.plots.anomalies_scatter import plot_anomaly_scatter
from src.plots.top10_bar import plot_top10_hottest_years
from src.plots.record_calendar import plot_record_calendar
from src.plots.daily_avg_temp import plot_daily_avg_temp
from src.plots.monthly_avg_temp import plot_monthly_avg_temp

# --- Setup ---
st.set_page_config(page_title="Bellingham Weather Dashboard", layout="wide")
st.title("\ud83c\udf24\ufe0f Bellingham, WA Weather Dashboard")
st.markdown("---")

# --- Load Data ---
con = duckdb.connect("data/weather.duckdb")
df = con.execute("SELECT * FROM weather_data ORDER BY time").fetchdf()
con.close()
df['time'] = pd.to_datetime(df['time'])

# --- Custom Visuals ---
st.subheader("\ud83d\udcc9 Weather Visualizations")

# Layout in rows of 3
plots = [
    plot_daily_avg_temp(df),
    plot_monthly_avg_temp(df),
    plot_over_80_streaks(df),
    plot_anomaly_scatter(df),
    plot_top10_hottest_years(df),
    plot_record_calendar(df),
]

cols = st.columns(3)
for i, fig in enumerate(plots):
    with cols[i % 3]:
        st.pyplot(fig)
    if (i + 1) % 3 == 0:
        cols = st.columns(3)

st.markdown("---")
st.caption("Data from Meteostat. Visuals built with DuckDB, pandas, seaborn, matplotlib, and Streamlit.")