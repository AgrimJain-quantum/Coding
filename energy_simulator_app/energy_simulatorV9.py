import requests
import time
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import random
from math import sin, pi
import pandas as pd

# --------------------
# CONFIGURATION
# --------------------
API_KEY = '1310cc9029637831bbb879313d029008'  # Replace with your OpenWeatherMap API key
LAT, LON = '26.9124', '75.7873'
SEASON = 'Summer'
SIM_HOURS = 24
SIM_INTERVAL = 0.2  # Reduce wait time for faster testing

# --------------------
# WEATHER DATA
# --------------------
def get_weather_data():
    url = f'https://api.openweathermap.org/data/2.5/forecast?lat={LAT}&lon={LON}&appid={API_KEY}'
    res = requests.get(url)
    if res.status_code != 200:
        print("⚠️ Weather API failed. Using default cloud values.")
        return {hour: 50 for hour in range(24)}
    data = res.json()
    forecast = {}
    for item in data['list']:
        hour = datetime.utcfromtimestamp(item['dt']).hour
        forecast[hour] = item['clouds']['all']
    return forecast

weather_forecast = get_weather_data()

# --------------------
# USER PROFILES
# --------------------
users = {
    "user_1": {
        "can_sell": True,
        "has_solar": True,
        "battery": 5,
        "battery_capacity": 10,
        "solar_capacity": 6,
        "user_type": "Home Office"
    },
    "user_2": {
        "can_sell": False,
        "has_solar": False,
        "battery": 0,
        "battery_capacity": 0,
        "user_type": "Day Worker"
    }
}

# --------------------
# BEHAVIOR FUNCTIONS
# --------------------
def get_hour_factor(hour, season, user_type):
    if user_type == "Home Office":
        base = 1.2 if 9 <= hour <= 17 else 1.1 if 18 <= hour <= 22 else 0.7
    elif user_type == "Day Worker":
        base = 1.0 if 6 <= hour <= 8 else 1.3 if 18 <= hour <= 22 else 0.5
    else:
        base = 1.0
    return base + (0.2 if season == "Summer" else 0.1 if season == "Winter" and hour >= 18 else 0)

def get_solar_production(hour, solar_capacity):
    if 6 <= hour <= 18:
        sunlight_curve = sin((pi / 12) * (hour - 6))
        cloud_factor = 1 - (weather_forecast.get(hour, 50) / 100)
        return solar_capacity * sunlight_curve * cloud_factor
    return 0

# --------------------
# LOGGING SETUP
# --------------------
hours = []
u1_consumption, u1_production, u1_battery, u1_sold = [], [], [], []
u2_consumption, u2_from_user1, u2_from_grid = [], [], []

# --------------------
# SIMULATION LOOP
# --------------------
for h in range(SIM_HOURS):
    hour = h  # Use 0–23 for plotting
    print(f"\n⏳ Simulating Hour {hour}:00")

    # --- USER 1 (Prosumer) ---
    u1 = users["user_1"]
    c1 = random.uniform(2.0, 3.5) * get_hour_factor(hour, SEASON, u1['user_type'])
    p1 = get_solar_production(hour, u1['solar_capacity'])
    net_energy = p1 - c1

    # Charging logic
    to_sell = 0
    if net_energy > 0:
        free_capacity = u1['battery_capacity'] - u1['battery']
        charge = min(free_capacity, net_energy)
        u1['battery'] += charge
        to_sell = max(0, net_energy - charge)
    else:
        demand = abs(net_energy)
        from_batt = min(demand, u1['battery'])
        u1['battery'] -= from_batt
        from_grid = demand - from_batt

    u1['battery'] = max(0, min(u1['battery'], u1['battery_capacity']))  # cap battery

    # --- USER 2 (Consumer) ---
    u2 = users["user_2"]
    c2 = random.uniform(2.0, 3.5) * get_hour_factor(hour, SEASON, u2['user_type'])

    if to_sell >= c2:
        from_user1 = c2
        from_grid2 = 0
        to_sell -= c2
    else:
        from_user1 = to_sell
        from_grid2 = c2 - from_user1
        to_sell = 0

    # Log
    print(f"[User 1] Prod: {p1:.2f} | Cons: {c1:.2f} | Batt: {u1['battery']:.2f} | Sold: {from_user1:.2f}")
    print(f"[User 2] Cons: {c2:.2f} | From U1: {from_user1:.2f} | From Grid: {from_grid2:.2f}")

    # Store
    hours.append(hour)
    u1_consumption.append(round(c1, 2))
    u1_production.append(round(p1, 2))
    u1_battery.append(round(u1['battery'], 2))
    u1_sold.append(round(from_user1, 2))
    u2_consumption.append(round(c2, 2))
    u2_from_user1.append(round(from_user1, 2))
    u2_from_grid.append(round(from_grid2, 2))

    time.sleep(SIM_INTERVAL)

# --------------------
# EXPORT TO CSV
# --------------------
df = pd.DataFrame({
    'Hour': hours,
    'U1_Consumption_kWh': u1_consumption,
    'U1_Production_kWh': u1_production,
    'U1_Battery_kWh': u1_battery,
    'U1_Energy_Sold_kWh': u1_sold,
    'U2_Consumption_kWh': u2_consumption,
    'U2_From_User1_kWh': u2_from_user1,
    'U2_From_Grid_kWh': u2_from_grid
})
df.to_csv("simulation_output.csv", index=False)
print("✅ CSV saved as simulation_output.csv")

# --------------------
# PLOTTING
# --------------------
plt.figure(figsize=(12, 8))

# USER 1
plt.subplot(2, 1, 1)
plt.step(hours, u1_consumption, label="U1 - Consumption", color='r', where='mid')
plt.step(hours, u1_production, label="U1 - Production", color='g', where='mid')
plt.step(hours, u1_battery, label="U1 - Battery Level", color='b', where='mid')
plt.title("User 1 - Energy Overview")
plt.xlabel("Hour")
plt.ylabel("kWh")
plt.legend()
plt.grid(True)

# USER 2
plt.subplot(2, 1, 2)
plt.step(hours, u2_consumption, label="U2 - Consumption", color='k', where='mid')
plt.step(hours, u2_from_user1, label="U2 - From User 1", color='c', where='mid')
plt.step(hours, u2_from_grid, label="U2 - From Grid", color='m', where='mid')
plt.title("User 2 - Energy Sources")
plt.xlabel("Hour")
plt.ylabel("kWh")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig("enhanced_energy_simulation.png")
plt.show()
print("📊 Graph saved as enhanced_energy_simulation.png")
