from energy_simulatorV2 import EnergyDataSimulator

def main():
    # Create a simulator instance
    simulator = EnergyDataSimulator(num_users=10)
    
    # Generate data (optional: save to CSV)
    data = simulator.generate_data()
    simulator.save_to_csv(data)
    
    # Plot data for a specific user
    simulator.plot_user_data("user_001")
    
    # Plot grid summary for all users
    simulator.plot_grid_summary()

if __name__ == "__main__":
    main()
