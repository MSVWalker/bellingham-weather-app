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
    # Bellingham, WA coordinates
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

    # Yesterday + Next 3 Days
    dates = data["daily"]["time"][:4]
    temps_min = data["daily"]["temperature_2m_min"][:4]
    temps_max = data["daily"]["temperature_2m_max"][:4]
    codes = data["daily"]["weathercode"][:4]

    st.markdown("### 🌤️ Forecast: Yesterday + Next 3 Days")
    cols = st.columns(4, gap="small")

    for i in range(4):
        with cols[i]:
            date = datetime.fromisoformat(dates[i]).strftime("%a %b %d")
            icon = weather_icons.get(codes[i], "❓")
            high_f = temps_max[i] * 9 / 5 + 32
            low_f = temps_min[i] * 9 / 5 + 32

            with st.container():
                st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
                st.markdown(f"#### {icon}")
                st.markdown(f"**{date}**")
                st.markdown(f"<span style='font-size: 14px;'>High: {high_f:.0f}°F</span>", unsafe_allow_html=True)
                st.markdown(f"<span style='font-size: 14px;'>Low: {low_f:.0f}°F</span>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)