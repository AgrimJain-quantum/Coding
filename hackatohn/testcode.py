import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import random
import json
try:
    from textblob import TextBlob
except ImportError:
    st.error("TextBlob not installed. Run: pip install textblob")
    st.stop()
    
try:
    import plotly.express as px
    import plotly.graph_objects as go
except ImportError:
    st.error("Plotly not installed. Run: pip install plotly")
    st.stop()

# Set page config
st.set_page_config(
    page_title="CrisisPixels - Urban Risk Visualizer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f2937;
        text-align: center;
        margin-bottom: 2rem;
    }
    .risk-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    .high-risk {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
    }
    .medium-risk {
        background: linear-gradient(135deg, #feca57 0%, #ff9ff3 100%);
    }
    .low-risk {
        background: linear-gradient(135deg, #48dbfb 0%, #0abde3 100%);
    }
</style>
""", unsafe_allow_html=True)

class CrisisPixelsEngine:
    def __init__(self, grid_size=20):
        self.grid_size = grid_size
        self.risk_data = None
        self.generate_risk_data()
    
    def generate_weather_data(self):
        """Simulate weather risk data"""
        weather_conditions = ['Clear', 'Cloudy', 'Rainy', 'Storm', 'Heatwave', 'Fog']
        weather_risks = [10, 20, 50, 80, 90, 30]
        
        grid = np.zeros((self.grid_size, self.grid_size))
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                condition = random.choice(list(zip(weather_conditions, weather_risks)))
                grid[i][j] = condition[1] + random.randint(-10, 10)
                grid[i][j] = max(0, min(100, grid[i][j]))  # Clamp between 0-100
        
        return grid
    
    def generate_social_sentiment(self):
        """Simulate social media sentiment analysis"""
        # Simulate social media posts
        sample_posts = [
            "Traffic is terrible today, completely stuck",
            "Amazing weather for a picnic!",
            "Power outage in downtown area",
            "Protest happening near city hall",
            "Great community event today",
            "Road construction causing delays",
            "Beautiful sunset over the city",
            "Concerned about rising crime rates"
        ]
        
        grid = np.zeros((self.grid_size, self.grid_size))
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                # Simulate sentiment analysis
                post = random.choice(sample_posts)
                sentiment = TextBlob(post).sentiment.polarity
                
                # Convert sentiment to risk score (negative sentiment = higher risk)
                risk_score = max(0, (1 - sentiment) * 50 + random.randint(0, 30))
                grid[i][j] = min(100, risk_score)
        
        return grid
    
    def generate_infrastructure_data(self):
        """Simulate infrastructure risk data"""
        grid = np.zeros((self.grid_size, self.grid_size))
        
        # Create infrastructure hotspots
        hotspots = [(5, 5), (15, 10), (8, 15), (12, 3)]
        
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                base_risk = random.randint(10, 40)
                
                # Add hotspot influence
                for hx, hy in hotspots:
                    distance = np.sqrt((i - hx)**2 + (j - hy)**2)
                    if distance < 3:
                        base_risk += 30 - int(distance * 10)
                
                grid[i][j] = min(100, max(0, base_risk))
        
        return grid
    
    def generate_economic_data(self):
        """Simulate economic risk indicators"""
        grid = np.zeros((self.grid_size, self.grid_size))
        
        # Create economic zones with different risk levels
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                # Simulate unemployment, business closure, etc.
                if i < self.grid_size // 3:  # Downtown - lower risk
                    base_risk = random.randint(10, 30)
                elif i < 2 * self.grid_size // 3:  # Mid-city - medium risk
                    base_risk = random.randint(20, 50)
                else:  # Outskirts - higher risk
                    base_risk = random.randint(30, 70)
                
                grid[i][j] = base_risk + random.randint(-10, 10)
                grid[i][j] = max(0, min(100, grid[i][j]))
        
        return grid
    
    def generate_risk_data(self):
        """Generate comprehensive risk data for the city grid"""
        weather_grid = self.generate_weather_data()
        social_grid = self.generate_social_sentiment()
        infra_grid = self.generate_infrastructure_data()
        economic_grid = self.generate_economic_data()
        
        # Calculate composite risk scores
        weights = {'weather': 0.3, 'social': 0.25, 'infrastructure': 0.25, 'economic': 0.2}
        
        composite_grid = (
            weather_grid * weights['weather'] +
            social_grid * weights['social'] +
            infra_grid * weights['infrastructure'] +
            economic_grid * weights['economic']
        )
        
        # Store all data
        self.risk_data = {
            'weather': weather_grid,
            'social': social_grid,
            'infrastructure': infra_grid,
            'economic': economic_grid,
            'composite': composite_grid
        }
        
        return self.risk_data
    
    def get_risk_level(self, score):
        """Convert risk score to risk level"""
        if score >= 70:
            return 'High Risk', '#ff4444'
        elif score >= 40:
            return 'Medium Risk', '#ffaa00'
        else:
            return 'Low Risk', '#44ff44'
    
    def generate_llm_explanation(self, row, col):
        """Generate AI explanation for a specific pixel"""
        if self.risk_data is None:
            return "No data available"
        
        weather_risk = self.risk_data['weather'][row][col]
        social_risk = self.risk_data['social'][row][col]
        infra_risk = self.risk_data['infrastructure'][row][col]
        economic_risk = self.risk_data['economic'][row][col]
        composite_risk = self.risk_data['composite'][row][col]
        
        risk_level, _ = self.get_risk_level(composite_risk)
        
        # Generate explanation based on dominant risk factors
        explanations = []
        
        if weather_risk > 60:
            explanations.append("severe weather conditions")
        if social_risk > 60:
            explanations.append("negative social sentiment and potential unrest")
        if infra_risk > 60:
            explanations.append("infrastructure vulnerabilities")
        if economic_risk > 60:
            explanations.append("economic instability indicators")
        
        zone_name = f"Zone {chr(65 + row//4)}{col//4 + 1}"
        
        if explanations:
            reason = " and ".join(explanations)
            return f"{zone_name} is at {risk_level.lower()} due to {reason}. Immediate attention recommended for emergency preparedness."
        else:
            return f"{zone_name} shows {risk_level.lower()} with stable conditions across all monitored factors."

def main():
    # Initialize the CrisisPixels engine
    if 'crisis_engine' not in st.session_state:
        st.session_state.crisis_engine = CrisisPixelsEngine()
    
    engine = st.session_state.crisis_engine
    
    # Header
    st.markdown('<h1 class="main-header">🧠 CrisisPixels - Urban Risk Visualizer</h1>', unsafe_allow_html=True)
    
    # Sidebar controls
    st.sidebar.header("🔧 Control Panel")
    
    # Refresh data button
    if st.sidebar.button("🔄 Refresh Data", type="primary"):
        engine.generate_risk_data()
        st.rerun()
    
    # Risk filter
    risk_filter = st.sidebar.selectbox(
        "📊 View Risk Type",
        ["composite", "weather", "social", "infrastructure", "economic"],
        format_func=lambda x: x.replace("_", " ").title()
    )
    
    # Auto-refresh toggle
    auto_refresh = st.sidebar.checkbox("⚡ Auto Refresh (30s)", value=False)
    
    if auto_refresh:
        st.sidebar.info("Data will refresh automatically every 30 seconds")
    
    # Display timestamp
    st.sidebar.info(f"📅 Last Updated: {datetime.now().strftime('%H:%M:%S')}")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"🗺️ City Risk Map - {risk_filter.replace('_', ' ').title()}")
        
        # Create the pixel map
        risk_grid = engine.risk_data[risk_filter]
        
        # Create heatmap using plotly
        fig = go.Figure(data=go.Heatmap(
            z=risk_grid,
            colorscale=[
                [0, '#44ff44'],    # Green (low risk)
                [0.4, '#ffaa00'],  # Yellow (medium risk)
                [0.7, '#ff4444']   # Red (high risk)
            ],
            showscale=True,
            colorbar=dict(
                title="Risk Score"
            ),
            hovertemplate='<b>Row: %{y}</b><br>' +
                         '<b>Col: %{x}</b><br>' +
                         '<b>Risk Score: %{z:.1f}</b><br>' +
                         '<extra></extra>'
        ))
        
        fig.update_layout(
            title=f"{risk_filter.replace('_', ' ').title()} Risk Distribution",
            xaxis_title="Grid Column",
            yaxis_title="Grid Row",
            height=500,
            width=600
        )
        
        # Display the heatmap
        selected_point = st.plotly_chart(fig, use_container_width=True, key="heatmap")
    
    with col2:
        st.subheader("📈 Risk Analytics")
        
        # Overall statistics
        composite_grid = engine.risk_data['composite']
        avg_risk = np.mean(composite_grid)
        max_risk = np.max(composite_grid)
        high_risk_zones = np.sum(composite_grid >= 70)
        
        # Risk level distribution
        risk_levels = []
        colors = []
        for i in range(engine.grid_size):
            for j in range(engine.grid_size):
                score = composite_grid[i][j]
                level, color = engine.get_risk_level(score)
                risk_levels.append(level)
                colors.append(color)
        
        # Count risk levels
        from collections import Counter
        level_counts = Counter(risk_levels)
        
        # Display metrics
        st.metric("🎯 Average Risk Score", f"{avg_risk:.1f}")
        st.metric("⚠️ Maximum Risk Score", f"{max_risk:.1f}")
        st.metric("🚨 High Risk Zones", high_risk_zones)
        
        # Risk distribution pie chart
        fig_pie = px.pie(
            values=list(level_counts.values()),
            names=list(level_counts.keys()),
            title="Risk Level Distribution",
            color_discrete_map={
                'Low Risk': '#44ff44',
                'Medium Risk': '#ffaa00',
                'High Risk': '#ff4444'
            }
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Detailed Analysis Section
    st.subheader("🔍 Detailed Zone Analysis")
    
    # Zone selector
    col1, col2 = st.columns(2)
    with col1:
        selected_row = st.slider("Select Row", 0, engine.grid_size-1, 10)
    with col2:
        selected_col = st.slider("Select Column", 0, engine.grid_size-1, 10)
    
    # Generate AI explanation for selected zone
    if st.button("🤖 Generate AI Analysis", type="secondary"):
        explanation = engine.generate_llm_explanation(selected_row, selected_col)
        st.info(f"**AI Analysis:** {explanation}")
    
    # Detailed breakdown for selected pixel
    st.subheader(f"📊 Zone {chr(65 + selected_row//4)}{selected_col//4 + 1} Breakdown")
    
    risk_breakdown = {
        'Weather Risk': engine.risk_data['weather'][selected_row][selected_col],
        'Social Risk': engine.risk_data['social'][selected_row][selected_col],
        'Infrastructure Risk': engine.risk_data['infrastructure'][selected_row][selected_col],
        'Economic Risk': engine.risk_data['economic'][selected_row][selected_col],
        'Composite Risk': engine.risk_data['composite'][selected_row][selected_col]
    }
    
    # Create bar chart for risk breakdown
    fig_bar = px.bar(
        x=list(risk_breakdown.keys()),
        y=list(risk_breakdown.values()),
        title=f"Risk Factor Breakdown - Row {selected_row}, Col {selected_col}",
        color=list(risk_breakdown.values()),
        color_continuous_scale=['green', 'yellow', 'red']
    )
    fig_bar.update_layout(height=400)
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    **CrisisPixels v1.0** | Built with ❤️ using Streamlit  
    🔄 Data refreshes in real-time | 🤖 AI-powered risk analysis | 🎯 Precision urban monitoring
    """)
    
    # Auto-refresh mechanism
    if auto_refresh:
        import time
        time.sleep(1)  # Reduced sleep time for better UX
        st.rerun()

if __name__ == "__main__":
    # Check if running with streamlit
    try:
        # This will only work when running with streamlit run
        st.session_state
        main()
    except Exception as e:
        print("\n" + "="*60)
        print("🚨 PLEASE RUN WITH STREAMLIT COMMAND:")
        print("="*60)
        print(f"streamlit run {__file__}")
        print("="*60)
        print("\nDo NOT run with: python main.py")
        print("="*60)