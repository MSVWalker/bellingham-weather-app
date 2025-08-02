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

def display_day(day, center=False):
    icon = weather_icons.get(day["code"], "❓")
    date_str = day["date"].strftime("%a %b %d")
    high = day["max"] * 9 / 5 + 32
    low = day["min"] * 9 / 5 + 32

    if center:
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)

    st.markdown(f"#### {icon}")
    st.markdown(f"**{date_str}**")
    st.markdown(f"<span style='font-size: 14px;'>High: {high:.0f}°F</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='font-size: 14px;'>Low: {low:.0f}°F</span>", unsafe_allow_html=True)

    if center:
        st.markdown("</div>", unsafe_allow_html=True)

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
    dates = data["daily"]["time"][:4]# src/features/forecast_box.py

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
        "&past_days=1"
    )

    response = requests.get(url)
    if response.status_code != 200:
        st.error("⚠️ Failed to fetch forecast data.")
        return

    data = response.json()
    dates = data["daily"]["time"]
    temps_min = data["daily"]["temperature_2m_min"]
    temps_max = data["daily"]["temperature_2m_max"]
    codes = data["daily"]["weathercode"]

    # Separate yesterday and next 6 days
    yesterday = {
        "date": datetime.fromisoformat(dates[0]),
        "min": temps_min[0],
        "max": temps_max[0],
        "code": codes[0],
    }

    forecast_days = []
    for i in range(1, 7):
        forecast_days.append({
            "date": datetime.fromisoformat(dates[i]),
            "min": temps_min[i],
            "max": temps_max[i],
            "code": codes[i],
        })

    # 🌤️ Display
    st.markdown("### 🌤️ Forecast")
    st.markdown("##### ⬅️ Yesterday")
    display_day(yesterday, center=True)

    st.markdown("##### 📆 Next 6 Days")
    cols = st.columns(6, gap="small")
    for i, day in enumerate(forecast_days):
        with cols[i]:
            display_day(day)