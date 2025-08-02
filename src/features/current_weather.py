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

def display_day(day, label=None, highlight=False, is_today=False):
    icon = weather_icons.get(day["code"], "❓")
    date_str = day["date"].strftime("%a %b %d").upper()
    high = day["max"] * 9 / 5 + 32
    low = day["min"] * 9 / 5 + 32

    # Label row
    if label:
        label_color = "#FFD700" if highlight else "#90EE90" if is_today else "#AAAAAA"
        label_html = f"<div style='font-size:11px; font-weight:600; color:{label_color};'>{label.upper()}</div>"
    else:
        label_html = f"<div style='font-size:11px; font-weight:600; color:#AAAAAA;'>{date_str}</div>"

    # Card layout
    return (
        f"<div style='text-align:center; line-height:1.1; padding:2px;'>"
        f"{label_html}"
        f"<div style='font-size:20px; margin-top:1px;'>{icon}</div>"
        f"<div style='font-size:11px; font-weight:500; margin-top:1px;'>{date_str}</div>"
        f"<div style='font-size:10px;'>High: {high:.0f}°F</div>"
        f"<div style='font-size:10px;'>Low: {low:.0f}°F</div>"
        f"</div>"
    )

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

    # Yesterday
    yesterday = {
        "date": datetime.fromisoformat(dates[0]),
        "min": temps_min[0],
        "max": temps_max[0],
        "code": codes[0],
    }

    # Next 6 days
    forecast_days = []
    for i in range(1, 7):
        forecast_days.append({
            "date": datetime.fromisoformat(dates[i]),
            "min": temps_min[i],
            "max": temps_max[i],
            "code": codes[i],
        })

    # Header
    st.markdown("### 🌤️ Forecast")

    # Build HTML blocks
    html_blocks = [display_day(yesterday, label="Yesterday", highlight=True)]
    for i, day in enumerate(forecast_days):
        label = "Today" if i == 0 else None
        is_today = (i == 0)
        html_blocks.append(display_day(day, label=label, is_today=is_today))

    # Render as 1 horizontal row with tight spacing
    html = (
        "<div style='display: flex; justify-content: space-between; gap: 10px;'>"
        + "".join(f"<div style='flex: 1;'>{block}</div>" for block in html_blocks)
        + "</div>"
    )

    st.markdown(html, unsafe_allow_html=True)