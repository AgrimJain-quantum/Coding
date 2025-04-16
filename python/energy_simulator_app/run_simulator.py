from energy_simulatorV2 import EnergyDataSimulator

# Create simulator instance
simulator = EnergyDataSimulator(num_users=10)

# Generate data and save to CSV
data = simulator.generate_data()
simulator.save_to_csv(data)
print("Energy data saved to energy_data_simulation.csv")

# Show visualization for user_001
print("Showing visualization for user_001...")
simulator.plot_user_data("user_001")

# Show grid summary visualization 
print("Showing grid summary...")
simulator.plot_grid_summary()
