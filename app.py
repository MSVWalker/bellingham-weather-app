import streamlit as st
import duckdb
import pandas as pd
from src.plots.heatmap_streaks import plot_over_80_streaks
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

# --- Quick Stats ---
col1, col2 = st.columns(2)
with col1:
    st.subheader("Daily Average Temperature (°C)")
    st.line_chart(df.set_index("time")["temp_avg_c"])
with col2:
    st.subheader("Monthly Average Temperature")
    monthly = df.resample("M", on="time")["temp_avg_c"].mean()
    st.bar_chart(monthly)

st.markdown("---")

# --- Custom Matplotlib Visuals ---
st.header("📊 Historical Visualizations")

with st.spinner("Loading charts..."):
    fig1 = plot_over_80_streaks(df)
    st.pyplot(fig1)

    fig2 = plot_anomaly_scatter(df)
    st.pyplot(fig2)

    fig3 = plot_top10_hottest_years(df)
    st.pyplot(fig3)

    fig4 = plot_record_calendar(df)
    st.pyplot(fig4)

st.markdown("---")
st.caption("Data from Meteostat. Visuals built with DuckDB, pandas, seaborn, matplotlib, and Streamlit.")