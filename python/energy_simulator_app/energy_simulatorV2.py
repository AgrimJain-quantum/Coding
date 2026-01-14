import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import random
import json
from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth

# Flask app setup
app = Flask(__name__, static_url_path='', static_folder='static')
auth = HTTPBasicAuth()

users = {
    "admin": "password123"
}

@auth.get_password
def get_password(username):
    if username in users:
        return users[username]
    return None

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@app.route('/')
def index():
    """Serve the main HTML page"""
    return app.send_static_file('index.html')

# Energy Data Simulator Class
class EnergyDataSimulator:
    def __init__(self, num_users=10, days=1, interval_minutes=60):  # Changed days=1
        """
        Initialize the energy data simulator.
        
        Parameters:
        - num_users: Number of users in the simulation
        - days: Number of days to simulate (now fixed to 1 day)
        - interval_minutes: Data recording interval in minutes
        """
        self.num_users = num_users
        self.days = days  # Now fixed to 1 day
        self.interval_minutes = interval_minutes  # Keep 60 minutes interval
        self.user_profiles = self._generate_user_profiles()
    
    def _generate_user_profiles(self):
        """Generate different user profiles with varying energy characteristics"""
        profiles = []

        # Add specialized users first
        profiles.append({
            "user_id": "user_001",
            "user_type": "Prosumer (Solar+Grid)",
            "base_consumption": 20,
            "solar_capacity": 10,
            "battery_capacity": 15,
            "can_sell": True,
            "max_price": 0.18,  # $/kWh
            "consumption_pattern": "Day Worker",
            "location": "Urban",
            "weather_sensitivity": 1.0
        })

        profiles.append({
            "user_id": "user_002",
            "user_type": "Grid-Dependent Consumer",
            "base_consumption": 25,
            "solar_capacity": 0,
            "battery_capacity": 0,
            "can_sell": False,  # Changed from can_resell to can_sell for consistency
            "max_purchase_price": 0.15,  # $/kWh
            "consumption_pattern": "Night Worker",
            "location": "Urban",
            "weather_sensitivity": 0.8
        })
        
        # User types and their characteristics
        user_types = [
            {"type": "Residential Small", "base_consumption": 8, "solar_capacity": 3, "battery_capacity": 5},
            {"type": "Residential Medium", "base_consumption": 15, "solar_capacity": 5, "battery_capacity": 10},
            {"type": "Residential Large", "base_consumption": 25, "solar_capacity": 8, "battery_capacity": 15},
            {"type": "Small Business", "base_consumption": 40, "solar_capacity": 10, "battery_capacity": 20},
            {"type": "Medium Business", "base_consumption": 80, "solar_capacity": 20, "battery_capacity": 40},
            {"type": "Large Business", "base_consumption": 150, "solar_capacity": 40, "battery_capacity": 80}
        ]
        
        for i in range(3, self.num_users + 1):  # Start from 3 since we added two users manually
            # Randomly assign a user type
            user_type = random.choice(user_types)
            
            # Add some randomness to the profile
            variation = random.uniform(0.8, 1.2)
            
            profile = {
                "user_id": f"user_{i+1:03d}",
                "user_type": user_type["type"],
                "base_consumption": user_type["base_consumption"] * variation,
                "solar_capacity": user_type["solar_capacity"] * variation,
                "battery_capacity": user_type["battery_capacity"] * variation,
                "consumption_pattern": random.choice(["Day Worker", "Night Worker", "Home Office", "Weekend Active"]),
                "location": random.choice(["Urban", "Suburban", "Rural"]),
                "weather_sensitivity": random.uniform(0.5, 1.5),
                "can_sell": False
            }
            
            profiles.append(profile)
            
        return profiles
    
    def _calculate_hourly_consumption(self, profile, hour):
        """Calculate consumption for a specific hour"""
        base = profile["base_consumption"]
        pattern = profile["consumption_pattern"]
        
        # Time-based multipliers
        if pattern == "Day Worker":
            return base * (1.5 if 7 <= hour <= 19 else 0.8)
        elif pattern == "Night Worker":
            return base * (1.5 if hour < 6 or hour >= 20 else 0.8)
        else:  # Home Office
            return base * (1.2 if 9 <= hour <= 17 else 1.0)
        
    def _calculate_hourly_production(self, profile, hour):
        """Calculate solar production for a specific hour"""
        if 6 <= hour <= 18:
            return profile["solar_capacity"] * np.sin(np.pi * (hour - 6) / 12)
        return 0.0

    def _calculate_energy_flows(self, net_energy, current_battery, battery_capacity):
        """Calculate energy flows between battery and grid."""
        if net_energy > 0:
            energy_to_battery = min(net_energy, battery_capacity - current_battery)
            current_battery += energy_to_battery
            grid_export = net_energy - energy_to_battery
            grid_import = 0
        else:
            energy_from_battery = min(abs(net_energy), current_battery)
            current_battery -= energy_from_battery
            grid_import = abs(net_energy) - energy_from_battery
            grid_export = 0
        
        # Ensure battery level is within bounds
        current_battery = max(0, min(current_battery, battery_capacity))
        
        return current_battery, grid_import, grid_export
        
    def _simulate_hourly_user_data(self, user_profile, timestamps):
        """Simulate hourly energy data for a single user"""
        data = {
            'timestamp': timestamps,
            'user_id': user_profile["user_id"],
            'consumption_kwh': [],
            'production_kwh': [],
            'battery_level_kwh': [],
            'grid_import_kwh': [],
            'grid_export_kwh': []
        }
        
        current_battery = user_profile["battery_capacity"] * random.uniform(0.2, 0.8)
        
        for hour in range(24):
            # Simplified hourly simulation (customize as needed)
            consumption = self._calculate_hourly_consumption(user_profile, hour)
            production = self._calculate_hourly_production(user_profile, hour)
            
            # Battery and grid calculations
            net_energy = production - consumption
            current_battery, grid_import, grid_export = self._calculate_energy_flows(
                net_energy, current_battery, user_profile["battery_capacity"]
            )
            
            # Append values
            data['consumption_kwh'].append(round(consumption, 2))
            data['production_kwh'].append(round(production, 2))
            data['battery_level_kwh'].append(round(current_battery, 2))
            data['grid_import_kwh'].append(round(grid_import, 2))
            data['grid_export_kwh'].append(round(grid_export, 2))
        
        return pd.DataFrame(data)
        
    def generate_data(self, start_date=None):
        """Generate energy data for all users"""
        if start_date is None:
            # Start at midnight of current day
            start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            
        # Generate 24 hours of data (1 day)
        total_intervals = 24  # Hardcoded for 24 hours
        timestamps = [start_date + timedelta(hours=i) for i in range(24)]
        
        all_user_data = []
        
        for profile in self.user_profiles:
            user_df = self._simulate_hourly_user_data(profile, timestamps)
            all_user_data.append(user_df)
        
        return pd.concat(all_user_data, ignore_index=True)
    
    def save_to_csv(self, dataframe, filename="energy_data_simulation.csv"):
        """Save the simulated data to a CSV file"""
        dataframe.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
        
    def plot_user_data(self, user_id):
        """Plot energy data for a specific user"""
        # Generate data first if not already done
        data = self.generate_data()
        user_data = data[data['user_id'] == user_id]
        
        if user_data.empty:
            print(f"No data found for user {user_id}")
            return
        
        # Plotting
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Consumption and Production
        ax1.plot(user_data['timestamp'], user_data['consumption_kwh'], 'r-', label='Consumption (kWh)')
        ax1.plot(user_data['timestamp'], user_data['production_kwh'], 'g-', label='Production (kWh)')
        ax1.set_title(f'Energy Consumption and Production for {user_id}')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Energy (kWh)')
        ax1.legend()
        ax1.grid(True)
        
        # Battery Level and Grid Interactions
        ax2.plot(user_data['timestamp'], user_data['battery_level_kwh'], 'b-', label='Battery Level (kWh)')
        ax2.plot(user_data['timestamp'], user_data['grid_import_kwh'], 'r--', label='Grid Import (kWh)')
        ax2.plot(user_data['timestamp'], user_data['grid_export_kwh'], 'g--', label='Grid Export (kWh)')
        ax2.set_title(f'Battery and Grid Interactions for {user_id}')
        ax2.set_xlabel('Time')
        ax2.set_ylabel('Energy (kWh)')
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        plt.show()
        
    def plot_grid_summary(self):
        """Plot summary of grid import/export across all users"""
        # Generate data first if not already done
        data = self.generate_data()
        
        # Aggregate by timestamp
        grid_summary = data.groupby('timestamp').agg({
            'grid_import_kwh': 'sum',
            'grid_export_kwh': 'sum',
            'consumption_kwh': 'sum',
            'production_kwh': 'sum'
        }).reset_index()
        
        # Plotting
        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.plot(grid_summary['timestamp'], grid_summary['grid_import_kwh'], 'r-', label='Total Grid Import (kWh)')
        ax.plot(grid_summary['timestamp'], grid_summary['grid_export_kwh'], 'g-', label='Total Grid Export (kWh)')
        ax.plot(grid_summary['timestamp'], grid_summary['consumption_kwh'], 'b--', label='Total Consumption (kWh)')
        ax.plot(grid_summary['timestamp'], grid_summary['production_kwh'], 'y--', label='Total Production (kWh)')
        
        ax.set_title('Grid Summary - All Users')
        ax.set_xlabel('Time')
        ax.set_ylabel('Energy (kWh)')
        ax.legend()
        ax.grid(True)
        
        plt.tight_layout()
        plt.show()

# Flask API routes
@app.route('/api/energy/data', methods=['GET'])
@auth.login_required
def get_energy_data():
    """API endpoint to get hourly data for current day"""
    num_users = int(request.args.get('users', 10))
    simulator = EnergyDataSimulator(num_users=num_users)
    data = simulator.generate_data()
    
    # Convert timestamps to string for JSON serialization
    data['timestamp'] = data['timestamp'].astype(str)
    
    return jsonify(data.to_dict(orient='records'))

@app.route('/api/energy/user/<user_id>', methods=['GET'])
@auth.login_required
def get_user_data(user_id):
    """API endpoint to get data for a specific user"""
    num_users = int(request.args.get('users', 10))
    simulator = EnergyDataSimulator(num_users=num_users)
    data = simulator.generate_data()
    user_data = data[data['user_id'] == user_id]
    
    if user_data.empty:
        return jsonify({"error": f"No data found for user {user_id}"}), 404
    
    # Convert timestamps to string for JSON serialization
    user_data['timestamp'] = user_data['timestamp'].astype(str)
    
    return jsonify(user_data.to_dict(orient='records'))

@app.route('/api/energy/summary', methods=['GET'])
@auth.login_required
def get_grid_summary():
    """API endpoint to get grid summary data"""
    num_users = int(request.args.get('users', 10))
    simulator = EnergyDataSimulator(num_users=num_users)
    data = simulator.generate_data()
    
    # Aggregate by timestamp
    grid_summary = data.groupby('timestamp').agg({
        'grid_import_kwh': 'sum',
        'grid_export_kwh': 'sum',
        'consumption_kwh': 'sum',
        'production_kwh': 'sum'
    }).reset_index()
    
    # Convert timestamps to string for JSON serialization
    grid_summary['timestamp'] = grid_summary['timestamp'].astype(str)
    
    return jsonify(grid_summary.to_dict(orient='records'))

if __name__ == "__main__":
    app.run(debug=True)
