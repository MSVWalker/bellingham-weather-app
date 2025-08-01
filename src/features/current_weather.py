# src/features/current_weather.py

import streamlit as st
from meteostat import Point, Hourly
from datetime import datetime, timedelta

def show_current_weather():
    location = Point(48.7544, -122.4780)  # Bellingham, WA
    now = datetime.now()
    start = now - timedelta(hours=2)

    try:
        data = Hourly(location, start, now).fetch()

        if data.empty:
            st.warning("⚠️ No recent weather data available.")
            return

        latest = data.iloc[-1]
        temp_c = latest['temp']
        temp_f = temp_c * 9 / 5 + 32
        wind = latest.get('wspd', None)
        humidity = latest.get('rhum', None)

        st.markdown(f"### 🌡️ Current Temperature: **{temp_f:.1f}°F**")
        st.markdown(f"""
        **Conditions:**  
        - 💨 Wind: {wind} km/h  
        - 💧 Humidity: {humidity}%  
        """)
    except Exception as e:
        st.error(f"❌ Failed to fetch current weather: {e}")