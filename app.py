import streamlit as st
import duckdb
import pandas as pd
from src.plots.heatmap_streaks import plot_over_80_streaks
from src.plots.anomalies_scatter import plot_anomaly_scatter
from src.plots.top10_bar import plot_top10_hottest_years
from src.plots.record_calendar import plot_record_calendar

st.set_page_config(page_title="Bellingham Weather Dashboard", layout="wide")

# --- Header ---
st.markdown("<h1 style='text-align: center;'>🌤️ Bellingham, WA Weather Trends</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:18px;'>Visualizing daily weather data from 1972 to today</p>", unsafe_allow_html=True)

# --- Load Data ---
con = duckdb.connect("data/weather.duckdb")
df = con.execute("SELECT * FROM weather_data ORDER BY time").fetchdf()
con.close()
df['time'] = pd.to_datetime(df['time'])

# --- Quick Metrics ---
latest = df.iloc[-1]
col1, col2, col3 = st.columns(3)
col1.metric("Latest Date", latest['time'].strftime("%b %d, %Y"))
col2.metric("Temp Avg (°C)", f"{latest['temp_avg_c']:.1f}")
col3.metric("Precip (mm)", f"{latest['precip_mm']:.1f}")

st.markdown("---")

# --- Trends Section ---
st.header("📈 Temperature Trends")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Daily Avg Temp")
    st.line_chart(df.set_index("time")["temp_avg_c"])

with col2:
    st.subheader("Monthly Avg Temp")
    monthly = df.resample("M", on="time")["temp_avg_c"].mean()
    st.bar_chart(monthly)

st.markdown("---")

# --- Historical Visuals ---
st.header("🧊 Historical Heat & Anomalies")

with st.spinner("Loading visuals..."):
    st.subheader("☀️ Longest Streaks Over 80°F")
    st.pyplot(plot_over_80_streaks(df))

    st.subheader("📉 Temperature Anomalies")
    st.pyplot(plot_anomaly_scatter(df))

    st.subheader("🔥 Top 10 Hottest Years")
    st.pyplot(plot_top10_hottest_years(df))

    st.subheader("🗓️ Calendar of Record Highs")
    st.pyplot(plot_record_calendar(df))

st.markdown("---")
st.caption("Data from Meteostat | Built with Streamlit, DuckDB, Matplotlib, and Python.")