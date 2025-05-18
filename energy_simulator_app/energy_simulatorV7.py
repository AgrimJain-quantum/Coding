import requests
import time
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import random
from math import sin, pi

# --------------------
# CONFIGURATION
# --------------------
API_KEY = '1310cc9029637831bbb879313d029008'  # Replace with your real API key
LAT, LON = '26.9124', '75.7873'  # Jaipur coordinates
SEASON = 'Summer'
SIM_HOURS = 24
SIM_INTERVAL = 1  # seconds

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
        "solar_capacity": 6,  # Boosted from 5
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

    if season == "Summer":
        base += 0.2
    elif season == "Winter":
        base += 0.1 if hour >= 18 else -0.1

    return base

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
start_time = datetime.now().replace(minute=0, second=0, microsecond=0)

for h in range(SIM_HOURS):
    hr = (start_time + timedelta(hours=h)).hour
    print(f"⏳ Simulating Hour {hr}:00")

    # USER 1
    u1 = users["user_1"]
    c1 = random.uniform(2.0, 3.5) * get_hour_factor(hr, SEASON, u1['user_type'])
    p1 = get_solar_production(hr, u1['solar_capacity'])
    net1 = p1 - c1

    to_sell = 0
    if net1 > 0:
        to_battery = min(net1, u1['battery_capacity'] - u1['battery'])
        u1['battery'] += to_battery
        if u1['battery'] > 0.1 * u1['battery_capacity']:  # Lowered threshold
            to_sell = net1 - to_battery
    else:
        demand = abs(net1)
        from_batt = min(demand, u1['battery'])
        u1['battery'] -= from_batt
        from_grid = demand - from_batt

    # USER 2
    u2 = users["user_2"]
    c2 = random.uniform(2.0, 3.5) * get_hour_factor(hr, SEASON, u2['user_type'])

    if to_sell >= c2:
        from_user1 = c2
        from_grid2 = 0
        to_sell -= c2
    else:
        from_user1 = to_sell
        from_grid2 = c2 - from_user1
        to_sell = 0

    # LOGGING
    print(f"[User 1] Prod: {p1:.2f}, Cons: {c1:.2f}, Batt: {u1['battery']:.2f}, Sold: {to_sell:.2f}")
    print(f"[User 2] Cons: {c2:.2f}, From U1: {from_user1:.2f}, From Grid: {from_grid2:.2f}")

    hours.append(hr)
    u1_consumption.append(round(c1, 2))
    u1_production.append(round(p1, 2))
    u1_battery.append(round(u1['battery'], 2))
    u1_sold.append(round(to_sell, 2))

    u2_consumption.append(round(c2, 2))
    u2_from_user1.append(round(from_user1, 2))
    u2_from_grid.append(round(from_grid2, 2))

    time.sleep(SIM_INTERVAL)

# --------------------
# PLOTTING
# --------------------
plt.figure(figsize=(12, 8))

plt.subplot(2, 1, 1)
plt.plot(hours, u1_consumption, 'r-', label="User 1 - Consumption")
plt.plot(hours, u1_production, 'g-', label="User 1 - Production")
plt.plot(hours, u1_battery, 'b-', label="Battery Level")
plt.title("User 1 - Energy Overview")
plt.xlabel("Hour")
plt.ylabel("kWh")
plt.grid(True)
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(hours, u2_consumption, 'k-', label="User 2 - Consumption")
plt.plot(hours, u2_from_user1, 'c-', label="From User 1")
plt.plot(hours, u2_from_grid, 'm-', label="From Grid")
plt.title("User 2 - Energy Sources")
plt.xlabel("Hour")
plt.ylabel("kWh")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.savefig("enhanced_energy_simulation.png")
plt.show()

print("✅ Simulation complete. Graph saved as 'enhanced_energy_simulation.png'")



