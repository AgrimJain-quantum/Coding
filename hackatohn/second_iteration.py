# crisispixels_v2.py

import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from textblob import TextBlob
from datetime import datetime
import random

# Set Streamlit layout
st.set_page_config(page_title="CrisisPixels v2 – Urban Risk Simulator", layout="wide")
st.title("🧠 CrisisPixels v2 – AI-Powered Urban Risk Grid")

# --------------------------
# CrisisPixels Simulation Engine
# --------------------------
class RiskEngine:
    def __init__(self, grid_size=20):
        self.grid_size = grid_size
        self.generate_data()

    def generate_weather_data(self):
        risk = np.random.randint(10, 90, size=(self.grid_size, self.grid_size))
        return risk

    def generate_social_sentiment(self):
        sample_posts = [
            "Terrible traffic", "Peaceful protest downtown", "Great weather today", "Power outage in city",
            "Beautiful festival", "Major flooding reported", "Bus delays everywhere", "Happy to be out!"
        ]
        grid = np.zeros((self.grid_size, self.grid_size))
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                post = random.choice(sample_posts)
                sentiment = TextBlob(post).sentiment.polarity
                risk_score = max(0, (1 - sentiment) * 50 + random.randint(0, 20))
                grid[i][j] = min(100, risk_score)
        return grid

    def generate_infra_data(self):
        grid = np.random.randint(20, 60, size=(self.grid_size, self.grid_size))
        for x, y in [(5, 5), (15, 10), (8, 15)]:
            for i in range(self.grid_size):
                for j in range(self.grid_size):
                    dist = np.sqrt((i - x)**2 + (j - y)**2)
                    if dist < 3:
                        grid[i][j] += 30 - int(dist * 10)
        return np.clip(grid, 0, 100)

    def generate_economic_data(self):
        grid = np.zeros((self.grid_size, self.grid_size))
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if i < self.grid_size // 3:
                    base = random.randint(10, 30)
                elif i < 2 * self.grid_size // 3:
                    base = random.randint(20, 50)
                else:
                    base = random.randint(30, 70)
                grid[i][j] = base + random.randint(-10, 10)
        return np.clip(grid, 0, 100)

    def generate_data(self):
        self.weather = self.generate_weather_data()
        self.social = self.generate_social_sentiment()
        self.infra = self.generate_infra_data()
        self.economic = self.generate_economic_data()
        self.composite = (
            0.3 * self.weather +
            0.25 * self.social +
            0.25 * self.infra +
            0.2 * self.economic
        )

    def get_risk_label(self, value):
        if value >= 70: return "High"
        elif value >= 40: return "Medium"
        return "Low"

    def explain_zone(self, row, col):
        parts = []
        if self.weather[row][col] > 60: parts.append("severe weather")
        if self.social[row][col] > 60: parts.append("negative social sentiment")
        if self.infra[row][col] > 60: parts.append("infrastructure risk")
        if self.economic[row][col] > 60: parts.append("economic instability")
        if parts:
            reason = " and ".join(parts)
            return f"Zone ({row},{col}) is high-risk due to {reason}."
        return f"Zone ({row},{col}) is stable across major indicators."

# --------------------------
# App Logic
# --------------------------
engine = RiskEngine()

st.sidebar.title("📊 Controls")
selected_layer = st.sidebar.radio("Select Risk Layer", ["composite", "weather", "social", "infra", "economic"])
if st.sidebar.button("🔄 Refresh Data"):
    engine.generate_data()
    st.experimental_rerun()

# Risk data for plotting
risk_map = getattr(engine, selected_layer)

# Plot heatmap
fig = go.Figure(data=go.Heatmap(
    z=risk_map,
    colorscale=[[0, 'green'], [0.5, 'yellow'], [1, 'red']],
    colorbar=dict(title="Risk"),
    hovertemplate="Row %{y}, Col %{x}: %{z:.1f}<extra></extra>"
))
fig.update_layout(title=f"{selected_layer.title()} Risk Map", height=500, width=600)
st.plotly_chart(fig, use_container_width=True)

# Sidebar stats
avg = np.mean(engine.composite)
high_zones = np.sum(engine.composite >= 70)
st.sidebar.markdown(f"🟢 **Average Risk:** `{avg:.2f}`")
st.sidebar.markdown(f"🔴 **High Risk Zones:** `{high_zones}`")

# Zone explainer
st.markdown("---")
st.subheader("🔍 AI Explanation")
col1, col2 = st.columns(2)
with col1:
    row = st.slider("Select Row", 0, engine.grid_size - 1, 10)
with col2:
    col = st.slider("Select Column", 0, engine.grid_size - 1, 10)

if st.button("🤖 Explain Zone"):
    st.info(engine.explain_zone(row, col))
