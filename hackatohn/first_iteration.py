# crisispixels_v1.py

import streamlit as st
import pandas as pd
import pydeck as pdk
import requests

# Set page layout
st.set_page_config(page_title="CrisisPixels v1 – Manhattan Weather", layout="wide")
st.title("🗺️ CrisisPixels v1 – Real-Time Weather in Manhattan")

# Sample data for 3 zones in Manhattan
data = {
    "zone": ["Lower Manhattan", "Midtown", "Upper Manhattan"],
    "lat": [40.707, 40.754, 40.818],
    "lng": [-74.010, -73.984, -73.949]
}
df = pd.DataFrame(data)

# OpenWeatherMap API Key (replace with your own or use st.secrets)
API_KEY = "YOUR_API_KEY_HERE"

# Fetch weather function
def get_weather(lat, lon):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        res = requests.get(url).json()
        temp = res['main']['temp']
        desc = res['weather'][0]['description']
        return f"{temp}°C, {desc}"
    except:
        return "Unavailable"

# Fetch weather for each zone
df["weather"] = df.apply(lambda row: get_weather(row["lat"], row["lng"]), axis=1)

# Assign color per zone (for visual distinction)
zone_colors = {
    "Lower Manhattan": [255, 0, 0],     # Red
    "Midtown": [255, 255, 0],           # Yellow
    "Upper Manhattan": [0, 255, 0]      # Green
}
df["color"] = df["zone"].map(zone_colors)

# Map Layer
layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position='[lng, lat]',
    get_fill_color='color',
    get_radius=700,
    pickable=True
)

# View settings
view = pdk.ViewState(
    latitude=df["lat"].mean(),
    longitude=df["lng"].mean(),
    zoom=12,
    pitch=0
)

# Tooltip
tooltip = {
    "html": "<b>{zone}</b><br/>Weather: {weather}",
    "style": {"backgroundColor": "black", "color": "white"}
}

# Render map
st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view,
    tooltip=tooltip
))
