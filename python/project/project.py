import pandas as pd
import numpy as np

# Generate random energy consumption data
hours = np.arange(1, 25)  # 24-hour period
energy_usage = np.random.randint(1, 10, size=24)  # Random kWh usage

# Save as CSV
df = pd.DataFrame({"Hour": hours, "Energy_Consumption": energy_usage})
df.to_csv("energy_data.csv", index=False)
print("Energy data saved successfully!")
