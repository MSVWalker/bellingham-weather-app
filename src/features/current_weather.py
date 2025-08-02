import streamlit as st
import requests
from datetime import datetime

# Emoji map for Open-Meteo's weather codes
weather_icons = {
    0: "☀️", 1: "🌤️", 2: "⛅", 3: "☁️",
    45: "🌫️", 48: "🌫️", 51: "🌦️", 53: "🌦️", 55: "🌦️",
    56: "🌧️", 57: "🌧️", 61: "🌧️", 63: "🌧️", 65: "🌧️",
    66: "🌧️", 67: "🌧️", 71: "🌨️", 73: "🌨️", 75: "❄️",
    80: "🌦️", 81: "🌦️", 82: "🌧️", 95: "⛈️", 96: "⛈️", 99: "⛈️"
}

def display_day(day, label=None, highlight=False):
    icon = weather_icons.get(day["code"], "❓")
    date_str = day["date"].strftime("%a %b %d")
    high = day["max"] * 9 / 5 + 32
    low = day["min"] * 9 / 5 + 32

    # Optional label above the card (e.g. "Yesterday")
    label_html = ""
    if label:
        color = "#FFD700" if highlight else "#FFFFFF"
        label_html = f"<div style='font-size:13px; color:{color}; font-weight: bold;'>{label}</div>"

    html = f"""
    <div style='text-align: center; line-height: 1.3; padding: 0 4px;'>
        {label_html}
        <div style='font-size:22px;'>{icon}</div>
        <div style='font-size:12px; font-weight:600;'>{date_str}</div>
        <div style='font-size:11px;'>High: {high:.0f}°F</div>
        <div style='font-size:11px;'>Low: {low:.0f}°F</div>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)

def show_current_weather():
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

    if len(dates) < 7:
        st.warning("Not enough forecast data.")
        return

    # Parse yesterday + next 6 days
    yesterday = {
        "date": datetime.fromisoformat(dates[0]),
        "min": temps_min[0],
        "max": temps_max[0],
        "code": codes[0],
    }

    forecast_days = []
    for i in range(1, 7):  # next 6 days
        forecast_days.append({
            "date": datetime.fromisoformat(dates[i]),
            "min": temps_min[i],
            "max": temps_max[i],
            "code": codes[i],
        })

    # Title and layout
    st.markdown("### 🌤️ Forecast")

    # Compact 1-row layout: Yesterday + 6 days
    cols = st.columns(7, gap="small")
    with cols[0]:
        display_day(yesterday, label="Yesterday", highlight=True)
    for i in range(6):
        with cols[i + 1]:
            display_day(forecast_days[i])