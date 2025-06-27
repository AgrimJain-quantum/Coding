# CrisisPixels - Unified Real-Time + Simulated Risk Visualizer

import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime
from textblob import TextBlob

# Page config
st.set_page_config(page_title="CrisisPixels Unified App", layout="wide")

# Sidebar - mode selector
mode = st.sidebar.selectbox("Select Mode", ["Real Manhattan Map", "Simulated Risk Grid"])
st.sidebar.write("\nBuilt with ❤️ by CrisisPixels Team")

###################################
# Mode 1 - Real Manhattan Weather #
###################################
if mode == "Real Manhattan Map":
    st.title("🌆 CrisisPixels – Real-Time Manhattan Weather Map")
    df = pd.read_csv("manhattan_ny_zones.csv")
    API_KEY = "1310cc9029637831bbb879313d029008"

    zone_colors = {
        "Lower Manhattan": [255, 0, 0],
        "Midtown": [255, 255, 0],
        "Upper Manhattan": [0, 255, 0]
    }
    df["color"] = df["zone"].map(zone_colors)

    def get_weather(lat, lon):
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
            res = requests.get(url).json()
            temp = res['main']['temp']
            desc = res['weather'][0]['description']
            return f"{temp}°C, {desc}"
        except:
            return "N/A"

    if "weather" not in df.columns:
        df["weather"] = df.apply(lambda row: get_weather(row["lat"], row["lng"]), axis=1)

    layer = pdk.Layer("ScatterplotLayer", data=df, get_position='[lng, lat]', get_radius=500, get_fill_color='color', pickable=True)
    view = pdk.ViewState(latitude=df["lat"].mean(), longitude=df["lng"].mean(), zoom=12, pitch=0)
    tooltip = {"html": "<b>{zone}</b><br/>Weather: {weather}", "style": {"backgroundColor": "black", "color": "white"}}
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view, tooltip=tooltip))

######################################
# Mode 2 - Simulated Pixel Grid View #
######################################
else:
    st.title("🧠 CrisisPixels – Simulated Urban Risk Grid")

    class CrisisPixelsEngine:
        def __init__(self, grid_size=20):
            self.grid_size = grid_size
            self.risk_data = None
            self.generate_risk_data()

        def generate_weather_data(self):
            conditions = [10, 20, 50, 80, 90, 30]
            return np.clip(np.random.normal(loc=50, scale=25, size=(self.grid_size, self.grid_size)), 0, 100)

        def generate_social_sentiment(self):
            posts = ["Protest downtown", "Fun festival", "Crime reports", "Nice event"]
            grid = np.zeros((self.grid_size, self.grid_size))
            for i in range(self.grid_size):
                for j in range(self.grid_size):
                    sent = TextBlob(np.random.choice(posts)).sentiment.polarity
                    grid[i][j] = max(0, (1 - sent) * 50 + np.random.randint(0, 30))
            return np.clip(grid, 0, 100)

        def generate_infrastructure_data(self):
            base = np.random.randint(10, 40, size=(self.grid_size, self.grid_size))
            for x, y in [(5, 5), (15, 10), (12, 3)]:
                for i in range(self.grid_size):
                    for j in range(self.grid_size):
                        dist = np.sqrt((i - x)**2 + (j - y)**2)
                        if dist < 3:
                            base[i][j] += 30 - int(dist * 10)
            return np.clip(base, 0, 100)

        def generate_economic_data(self):
            grid = np.zeros((self.grid_size, self.grid_size))
            for i in range(self.grid_size):
                for j in range(self.grid_size):
                    if i < self.grid_size // 3:
                        risk = np.random.randint(10, 30)
                    elif i < 2 * self.grid_size // 3:
                        risk = np.random.randint(20, 50)
                    else:
                        risk = np.random.randint(30, 70)
                    grid[i][j] = np.clip(risk + np.random.randint(-10, 10), 0, 100)
            return grid

        def generate_risk_data(self):
            w, s, i, e = self.generate_weather_data(), self.generate_social_sentiment(), self.generate_infrastructure_data(), self.generate_economic_data()
            self.risk_data = {
                'weather': w,
                'social': s,
                'infrastructure': i,
                'economic': e,
                'composite': 0.3*w + 0.25*s + 0.25*i + 0.2*e
            }
            return self.risk_data

        def get_risk_level(self, val):
            if val >= 70: return 'High', '#ff4444'
            elif val >= 40: return 'Medium', '#ffaa00'
            else: return 'Low', '#44ff44'

        def explain(self, row, col):
            r = {k: self.risk_data[k][row][col] for k in self.risk_data}
            level, _ = self.get_risk_level(r['composite'])
            reasons = []
            for k, v in r.items():
                if k != 'composite' and v > 60:
                    reasons.append(k)
            if reasons:
                return f"Zone {chr(65+row//4)}{col//4+1} is at {level} risk due to {', '.join(reasons)}."
            return f"Zone {chr(65+row//4)}{col//4+1} is stable ({level} risk)."

    # Engine setup
    if 'crisis_engine' not in st.session_state:
        st.session_state.crisis_engine = CrisisPixelsEngine()
    engine = st.session_state.crisis_engine

    col1, col2 = st.columns([2, 1])

    with col1:
        grid = engine.risk_data['composite']
        fig = go.Figure(data=go.Heatmap(
            z=grid,
            colorscale=[[0, '#44ff44'], [0.4, '#ffaa00'], [0.7, '#ff4444']],
            showscale=True,
            colorbar=dict(title="Risk")
        ))
        fig.update_layout(title="Simulated City Risk Heatmap", height=500)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        avg = np.mean(grid)
        st.metric("Average Risk", f"{avg:.1f}")
        st.metric("Max Risk", f"{np.max(grid):.1f}")
        count = np.sum(grid >= 70)
        st.metric("High Risk Zones", count)

        row = st.slider("Row", 0, engine.grid_size-1, 10)
        col = st.slider("Col", 0, engine.grid_size-1, 10)

        if st.button("Explain Pixel"):
            st.info(engine.explain(row, col))
