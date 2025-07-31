import streamlit as st
import duckdb
import pandas as pd

st.set_page_config(page_title="Bellingham Weather Dashboard", layout="wide")
st.title("🌤️ Bellingham, WA Weather Dashboard")

# Load weather data from DuckDB
con = duckdb.connect("data/weather.duckdb")
df = con.execute("SELECT * FROM weather_data ORDER BY time").fetchdf()
con.close()

df['time'] = pd.to_datetime(df['time'])

# Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Daily Average Temperature (°C)")
    st.line_chart(df.set_index("time")["temp_avg_c"])

with col2:
    st.subheader("Monthly Average Temperature")
    monthly = df.resample("M", on="time")["temp_avg_c"].mean()
    st.bar_chart(monthly)

st.markdown("---")
st.caption("Data from Meteostat. Updated daily.")