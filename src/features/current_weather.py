import streamlit as st
import requests
from datetime import datetime, timedelta

# Emoji map for Open-Meteo's weather codes
weather_icons = {
    0: "☀️", 1: "🌤️", 2: "⛅", 3: "☁️",
    45: "🌫️", 48: "🌫️", 51: "🌦️", 53: "🌦️", 55: "🌦️",
    56: "🌧️", 57: "🌧️", 61: "🌧️", 63: "🌧️", 65: "🌧️",
    66: "🌧️", 67: "🌧️", 71: "🌨️", 73: "🌨️", 75: "❄️",
    80: "🌦️", 81: "🌦️", 82: "🌧️", 95: "⛈️", 96: "⛈️", 99: "⛈️"
}

def show_current_weather():
    lat, lon = 48.7544, -122.4780
    tz = "America/Los_Angeles"

    # Dates
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    start_date = yesterday.strftime("%Y-%m-%d")
    end_date = (today + timedelta(days=3)).strftime("%Y-%m-%d")

    # API for historical + forecast combined
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&start_date={start_date}&end_date={end_date}"
        "&daily=temperature_2m_min,temperature_2m_max,weathercode"
        f"&timezone={tz}"
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

    # Display: Yesterday + Next 3 Days
    st.markdown("### 🌤️ Forecast: Yesterday + Next 3 Days")

    with st.container():
        col_style = """
        display: flex;
        justify-content: center;
        gap: 1.5rem;
        flex-wrap: nowrap;
        """
        st.markdown(f"<div style='{col_style}'>", unsafe_allow_html=True)

        for i in range(4):
            date = datetime.fromisoformat(dates[i]).strftime("%a %b %d")
            icon = weather_icons.get(codes[i], "❓")
            high_f = temps_max[i] * 9 / 5 + 32
            low_f = temps_min[i] * 9 / 5 + 32

            box = f"""
            <div style='text-align: center; padding: 0.5rem 1rem; border-radius: 12px; background: #f9f9f9; box-shadow: 0 1px 3px rgba(0,0,0,0.1); min-width: 100px;'>
                <div style='font-size: 32px;'>{icon}</div>
                <div><strong>{date}</strong></div>
                <div style='font-size: 14px;'>High: {high_f:.0f}°F</div>
                <div style='font-size: 14px;'>Low: {low_f:.0f}°F</div>
            </div>
            """
            st.markdown(box, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)