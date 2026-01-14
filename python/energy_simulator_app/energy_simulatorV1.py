import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import random
import json
from flask import Flask, jsonify, request

# Flask app setup
app = Flask(__name__)

class EnergyDataSimulator:
    def __init__(self, num_users=10, days=30, interval_minutes=60):
        """
        Initialize the energy data simulator.
        
        Parameters:
        - num_users: Number of users in the simulation
        - days: Number of days to simulate
        - interval_minutes: Data recording interval in minutes
        """
        self.num_users = num_users
        self.days = days
        self.interval_minutes = interval_minutes
        self.user_profiles = self._generate_user_profiles()
        
    def _generate_user_profiles(self):
        """Generate different user profiles with varying energy characteristics"""
        profiles = []
        
        # User types and their characteristics
        user_types = [
            {"type": "Residential Small", "base_consumption": 8, "solar_capacity": 3, "battery_capacity": 5},
            {"type": "Residential Medium", "base_consumption": 15, "solar_capacity": 5, "battery_capacity": 10},
            {"type": "Residential Large", "base_consumption": 25, "solar_capacity": 8, "battery_capacity": 15},
            {"type": "Small Business", "base_consumption": 40, "solar_capacity": 10, "battery_capacity": 20},
            {"type": "Medium Business", "base_consumption": 80, "solar_capacity": 20, "battery_capacity": 40},
            {"type": "Large Business", "base_consumption": 150, "solar_capacity": 40, "battery_capacity": 80}
        ]
        
        for i in range(self.num_users):
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
                "weather_sensitivity": random.uniform(0.5, 1.5)
            }
            
            profiles.append(profile)
            
        return profiles
    
    def _simulate_single_user_data(self, user_profile, start_date):
        """Simulate energy data for a single user"""
        timestamps = []
        consumption = []
        production = []
        battery_level = []
        grid_import = []
        grid_export = []
        
        # Initial battery level (random between 20% and 80%)
        current_battery = user_profile["battery_capacity"] * random.uniform(0.2, 0.8)
        
        # Create timestamps
        total_intervals = int((self.days * 24 * 60) / self.interval_minutes)
        for i in range(total_intervals):
            current_time = start_date + timedelta(minutes=i * self.interval_minutes)
            timestamps.append(current_time)
            
            # Hour of day (0-23) affects consumption and production patterns
            hour = current_time.hour
            
            # Day of week (0=Monday, 6=Sunday) affects patterns
            day_of_week = current_time.weekday()
            is_weekend = day_of_week >= 5
            
            # Base consumption with time-of-day variation
            if user_profile["consumption_pattern"] == "Day Worker":
                # Higher consumption in morning and evening
                hour_factor = 1.0 + 0.5 * (0.5 <= hour/24 <= 0.8)
            elif user_profile["consumption_pattern"] == "Night Worker":
                # Higher consumption during night
                hour_factor = 1.0 + 0.5 * (hour < 8 or hour > 20)
            elif user_profile["consumption_pattern"] == "Home Office":
                # Steady consumption throughout day
                hour_factor = 1.0 + 0.3 * (8 <= hour <= 18)
            else:  # Weekend Active
                # Higher consumption on weekends
                hour_factor = 1.0 + 0.5 * is_weekend
            
            # Add randomness to consumption
            random_factor = random.uniform(0.8, 1.2)
            
            # Calculate actual consumption
            user_consumption = user_profile["base_consumption"] * hour_factor * random_factor
            
            # Solar production based on time of day (peak at noon)
            sun_intensity = max(0, np.sin(np.pi * (hour - 6) / 12)) if 6 <= hour <= 18 else 0
            # Reduce production on weekends by 0-20% randomly to simulate weather variations
            weather_factor = user_profile["weather_sensitivity"] * random.uniform(0.7, 1.0) if random.random() < 0.3 else 1.0
            user_production = user_profile["solar_capacity"] * sun_intensity * weather_factor
            
            # Battery dynamics
            net_energy = user_production - user_consumption
            
            # If producing more than consuming, charge battery
            if net_energy > 0:
                energy_to_battery = min(net_energy, user_profile["battery_capacity"] - current_battery)
                current_battery += energy_to_battery
                excess_energy = net_energy - energy_to_battery
                user_grid_export = excess_energy
                user_grid_import = 0
            # If consuming more than producing, discharge battery
            else:
                energy_from_battery = min(abs(net_energy), current_battery)
                current_battery -= energy_from_battery
                energy_deficit = abs(net_energy) - energy_from_battery
                user_grid_import = energy_deficit
                user_grid_export = 0
            
            # Ensure battery level is within bounds
            current_battery = max(0, min(current_battery, user_profile["battery_capacity"]))
            
            # Record data
            consumption.append(round(user_consumption, 2))
            production.append(round(user_production, 2))
            battery_level.append(round(current_battery, 2))
            grid_import.append(round(user_grid_import, 2))
            grid_export.append(round(user_grid_export, 2))
        
        # Create DataFrame with all data
        df = pd.DataFrame({
            'timestamp': timestamps,
            'user_id': user_profile["user_id"],
            'user_type': user_profile["user_type"],
            'consumption_kwh': consumption,
            'production_kwh': production,
            'battery_level_kwh': battery_level,
            'grid_import_kwh': grid_import,
            'grid_export_kwh': grid_export
        })
        
        return df
    
    def generate_data(self, start_date=None):
        """Generate energy data for all users"""
        if start_date is None:
            start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=self.days)
        
        all_user_data = []
        
        for profile in self.user_profiles:
            user_df = self._simulate_single_user_data(profile, start_date)
            all_user_data.append(user_df)
        
        # Combine all user data
        combined_df = pd.concat(all_user_data, ignore_index=True)
        return combined_df
    
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
def get_energy_data():
    """API endpoint to get simulated energy data"""
    num_users = int(request.args.get('users', 10))
    days = int(request.args.get('days', 7))
    interval = int(request.args.get('interval', 60))
    
    simulator = EnergyDataSimulator(num_users=num_users, days=days, interval_minutes=interval)
    data = simulator.generate_data()
    
    # Convert to dictionary for JSON serialization
    result = data.to_dict(orient='records')
    
    return jsonify({"status": "success", "data": result})

@app.route('/api/energy/user/<user_id>', methods=['GET'])
def get_user_data(user_id):
    """API endpoint to get data for a specific user"""
    days = int(request.args.get('days', 7))
    interval = int(request.args.get('interval', 60))
    
    simulator = EnergyDataSimulator(num_users=20, days=days, interval_minutes=interval)
    data = simulator.generate_data()
    
    user_data = data[data['user_id'] == user_id]
    
    if user_data.empty:
        return jsonify({"status": "error", "message": f"No data found for user {user_id}"}), 404
    
    # Convert to dictionary for JSON serialization
    result = user_data.to_dict(orient='records')
    
    return jsonify({"status": "success", "data": result})

@app.route('/api/energy/summary', methods=['GET'])
def get_energy_summary():
    """API endpoint to get summary statistics of energy data"""
    num_users = int(request.args.get('users', 10))
    days = int(request.args.get('days', 7))
    interval = int(request.args.get('interval', 60))
    
    simulator = EnergyDataSimulator(num_users=num_users, days=days, interval_minutes=interval)
    data = simulator.generate_data()
    
    # Calculate summary statistics
    total_consumption = data['consumption_kwh'].sum()
    total_production = data['production_kwh'].sum()
    total_grid_import = data['grid_import_kwh'].sum()
    total_grid_export = data['grid_export_kwh'].sum()
    
    # Calculate peak times
    consumption_by_hour = data.groupby(data['timestamp'].dt.hour)['consumption_kwh'].mean()
    production_by_hour = data.groupby(data['timestamp'].dt.hour)['production_kwh'].mean()
    
    peak_consumption_hour = consumption_by_hour.idxmax()
    peak_production_hour = production_by_hour.idxmax()
    
    summary = {
        "total_consumption_kwh": round(total_consumption, 2),
        "total_production_kwh": round(total_production, 2),
        "total_grid_import_kwh": round(total_grid_import, 2),
        "total_grid_export_kwh": round(total_grid_export, 2),
        "grid_dependency_percentage": round((total_grid_import / total_consumption) * 100, 2),
        "self_sufficiency_percentage": round(((total_consumption - total_grid_import) / total_consumption) * 100, 2),
        "peak_consumption_hour": int(peak_consumption_hour),
        "peak_production_hour": int(peak_production_hour)
    }
    
    return jsonify({"status": "success", "summary": summary})

# Main execution
if __name__ == "__main__":
    # Example usage without running the server
    simulator = EnergyDataSimulator(num_users=15, days=7, interval_minutes=60)
    data = simulator.generate_data()
    
    # Save to CSV
    simulator.save_to_csv(data)
    
    # Plot one user's data
    simulator.plot_user_data("user_001")
    
    # Plot grid summary
    simulator.plot_grid_summary()
    
    # Uncomment to run the Flask server
    app.run(debug=True, host='0.0.0.0', port=5000)