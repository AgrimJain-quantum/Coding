# crisispixels_manhattan_realmap.py

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from textblob import TextBlob
from datetime import datetime
import random

# Configuration
st.set_page_config(page_title="CrisisPixels - Manhattan Risk Map", layout="wide")
st.title("🗽 CrisisPixels – Manhattan Urban Risk Simulation")

# Define Manhattan bounding box (approximate)
LAT_MIN, LAT_MAX = 40.700, 40.880
LON_MIN, LON_MAX = -74.020, -73.930
GRID_SIZE = 20

# Generate lat/lon grid points
def generate_grid():
    lats = np.linspace(LAT_MIN, LAT_MAX, GRID_SIZE)
    lons = np.linspace(LON_MIN, LON_MAX, GRID_SIZE)
    return lats, lons

# Risk simulation functions (same logic as original)
def simulate_weather():
    return np.random.randint(10, 90, (GRID_SIZE, GRID_SIZE))

def simulate_social():
    sentiments = np.random.uniform(-1, 1, (GRID_SIZE, GRID_SIZE))
    return np.clip((1 - sentiments) * 50 + np.random.randint(0, 30, sentiments.shape), 0, 100)

def simulate_infra():
    grid = np.random.randint(10, 40, (GRID_SIZE, GRID_SIZE))
    for hx, hy in [(5, 5), (15, 10), (8, 15), (12, 3)]:
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                dist = np.sqrt((i - hx)**2 + (j - hy)**2)
                if dist < 3:
                    grid[i][j] += 30 - int(dist * 10)
    return np.clip(grid, 0, 100)

def simulate_econ():
    grid = np.zeros((GRID_SIZE, GRID_SIZE))
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if i < GRID_SIZE // 3:
                base = np.random.randint(10, 30)
            elif i < 2 * GRID_SIZE // 3:
                base = np.random.randint(20, 50)
            else:
                base = np.random.randint(30, 70)
            grid[i][j] = base + np.random.randint(-10, 10)
    return np.clip(grid, 0, 100)

def compute_composite(weather, social, infra, econ):
    return (
        weather * 0.3 +
        social * 0.25 +
        infra * 0.25 +
        econ * 0.2
    )

# Generate risk data
weather_risk = simulate_weather()
social_risk = simulate_social()
infra_risk = simulate_infra()
econ_risk = simulate_econ()
composite_risk = compute_composite(weather_risk, social_risk, infra_risk, econ_risk)

# Sidebar selector
risk_type = st.sidebar.selectbox("Select Risk Layer", ["composite", "weather", "social", "infrastructure", "economic"])
risk_map = {
    "composite": composite_risk,
    "weather": weather_risk,
    "social": social_risk,
    "infrastructure": infra_risk,
    "economic": econ_risk
}[risk_type]

# Generate lat/lon grid
lats, lons = generate_grid()

# Prepare data for heatmap
z = risk_map.tolist()

fig = go.Figure(data=go.Heatmap(
    z=z,
    x=lons,
    y=lats,
    colorscale=[[0, '#44ff44'], [0.4, '#ffaa00'], [0.7, '#ff4444']],
    colorbar=dict(title="Risk Score", tickvals=[20, 50, 80], ticktext=["Low", "Medium", "High"]),
    hovertemplate='Lat: %{y:.4f}<br>Lon: %{x:.4f}<br>Risk Score: %{z:.1f}<extra></extra>'
))

fig.update_layout(
    title=f"Manhattan {risk_type.title()} Risk Heatmap",
    xaxis_title="Longitude",
    yaxis_title="Latitude",
    height=650,
    width=900
)

st.plotly_chart(fig, use_container_width=True)

# Summary metrics
avg_risk = np.mean(composite_risk)
max_risk = np.max(composite_risk)
high_risk_zones = np.sum(composite_risk >= 70)

col1, col2, col3 = st.columns(3)
col1.metric("🌡 Average Composite Risk", f"{avg_risk:.2f}")
col2.metric("🚨 Maximum Risk Score", f"{max_risk:.1f}")
col3.metric("🔺 High Risk Zones", high_risk_zones)

st.caption("CrisisPixels simulated data (v1.0) | Grid overlay based on Manhattan lat/lon bounds")
