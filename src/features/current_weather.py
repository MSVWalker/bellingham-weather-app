# src/features/forecast_box.py

import streamlit as st
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

# Emoji map for Open-Meteo's weather codes
weather_icons = {
    0: "☀️", 1: "🌤️", 2: "⛅", 3: "☁️",
    45: "🌫️", 48: "🌫️", 51: "🌦️", 53: "🌦️", 55: "🌦️",
    56: "🌧️", 57: "🌧️", 61: "🌧️", 63: "🌧️", 65: "🌧️",
    66: "🌧️", 67: "🌧️", 71: "🌨️", 73: "🌨️", 75: "❄️",
    80: "🌦️", 81: "🌦️", 82: "🌧️", 95: "⛈️", 96: "⛈️", 99: "⛈️"
}

def show_current_weather():
    # Bellingham coordinates
    lat, lon = 48.7544, -122.4780

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&daily=temperature_2m_min,temperature_2m_max,weathercode"
        "&timezone=America%2FLos_Angeles"
    )

    response = requests.get(url)
    if response.status_code != 200:
        st.error("⚠️ Failed to fetch forecast data.")
        return

    data = response.json()
    dates = data["daily"]["time"][:3]
    temps_min = data["daily"]["temperature_2m_min"][:3]
    temps_max = data["daily"]["temperature_2m_max"][:3]
    codes = data["daily"]["weathercode"][:3]

    st.markdown("### 🌤️ 3-Day Forecast")

    cols = st.columns(3)
    for i in range(3):
        with cols[i]:
            date = datetime.fromisoformat(dates[i]).strftime("%a %b %d")
            icon = weather_icons.get(codes[i], "❓")

            high_f = temps_max[i] * 9 / 5 + 32
            low_f = temps_min[i] * 9 / 5 + 32

            st.markdown(f"#### {icon}")
            st.markdown(f"**{date}**")
            st.markdown(f"High: **{high_f:.0f}°F**")
            st.markdown(f"Low: **{low_f:.0f}°F**")