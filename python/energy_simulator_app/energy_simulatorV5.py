import requests
import time
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import random

# -----------------------
# CONFIGURATION
# -----------------------
API_KEY = '1310cc9029637831bbb879313d029008'
LAT = '26.9124'  # Jaipur latitude
LON = '75.7873'  # Jaipur longitude
SEASON = 'Summer'  # Options: Summer, Winter, Monsoon
SIM_HOURS = 24
SIM_INTERVAL = 1  # seconds per simulated hour

# -----------------------
# USER SETUP
# -----------------------
users = {
    "user_1": {
        "can_sell": True,
        "has_solar": True,
        "battery": 5,
        "battery_capacity": 10,
        "solar_capacity": 5,
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

# -----------------------
# WEATHER FUNCTION
# -----------------------
# def get_weather_data():
#     url = f'https://api.openweathermap.org/data/2.5/forecast?lat={LAT}&lon={LON}&appid={API_KEY}'
#     response = requests.get(url)
#     if response.status_code != 200:
#         raise Exception("Weather API failed.")
#     data = response.json()
#     forecast = {}
#     for item in data['list']:
#         hour = datetime.utcfromtimestamp(item['dt']).hour
#         cloud_pct = item['clouds']['all']
#         forecast[hour] = cloud_pct
#     return forecast
def get_weather_data():
    url = f'https://api.openweathermap.org/data/2.5/forecast?lat={LAT}&lon={LON}&appid={API_KEY}'
    response = requests.get(url)
    print("Status Code:", response.status_code)
    print("Response:", response.text[:500])  # Print preview of JSON or error
    if response.status_code != 200:
        raise Exception("Weather API failed.")
    data = response.json()
    forecast = {}
    for item in data['list']:
        hour = datetime.utcfromtimestamp(item['dt']).hour
        cloud_pct = item['clouds']['all']
        forecast[hour] = cloud_pct
    return forecast
weather_forecast = get_weather_data()

# -----------------------
# SEASONAL + TIME PATTERN
# -----------------------
def get_hour_factor(hour, season, user_type):
    if user_type == "Home Office":
        if 9 <= hour <= 17:
            base = 1.2
        elif 18 <= hour <= 22:
            base = 1.1
        else:
            base = 0.7
    elif user_type == "Day Worker":
        if 6 <= hour <= 8:
            base = 1.0
        elif 18 <= hour <= 22:
            base = 1.3
        else:
            base = 0.5
    else:
        base = 1.0

    if season == "Summer":
        return base + 0.2
    elif season == "Winter":
        return base + 0.1 if hour >= 18 else base - 0.1
    elif season == "Monsoon":
        return base
    return base

def get_solar_production(hour, solar_capacity):
    if 6 <= hour <= 18:
        sunlight_intensity = max(0, (1 - abs(hour - 12) / 6))  # peak at noon
        clouds = weather_forecast.get(hour, 50)
        weather_factor = 1 - (clouds / 100)  # less clouds = more production
        return solar_capacity * sunlight_intensity * weather_factor
    return 0

# -----------------------
# DATA LOGGING
# -----------------------
hours = []
u1_consumption, u1_production, u1_battery, u1_sold = [], [], [], []
u2_consumption, u2_from_user1, u2_from_grid = [], [], []

start_time = datetime.now().replace(minute=0, second=0, microsecond=0)

# -----------------------
# SIMULATION LOOP
# -----------------------
for hour in range(SIM_HOURS):
    now = start_time + timedelta(hours=hour)
    hr = now.hour
    print(f"⏳ Simulating Hour: {hr}:00")

    # --- USER 1 ---
    u1 = users['user_1']
    base_c1 = random.uniform(2.0, 3.5)
    f1 = get_hour_factor(hr, SEASON, u1['user_type'])
    c1 = base_c1 * f1
    p1 = get_solar_production(hr, u1['solar_capacity'])
    net1 = p1 - c1

    if net1 > 0:
        space = u1['battery_capacity'] - u1['battery']
        to_battery = min(space, net1)
        u1['battery'] += to_battery
        to_sell = net1 - to_battery
    else:
        need = abs(net1)
        from_batt = min(need, u1['battery'])
        u1['battery'] -= from_batt
        from_grid = need - from_batt
        to_sell = 0

    # --- USER 2 ---
    u2 = users['user_2']
    base_c2 = random.uniform(2.0, 3.5)
    f2 = get_hour_factor(hr, SEASON, u2['user_type'])
    c2 = base_c2 * f2

    if to_sell >= c2:
        from_user1 = c2
        from_grid2 = 0
        to_sell -= c2
    else:
        from_user1 = to_sell
        from_grid2 = c2 - from_user1
        to_sell = 0

    # --- LOG DATA ---
    hours.append(hr)
    u1_consumption.append(round(c1, 2))
    u1_production.append(round(p1, 2))
    u1_battery.append(round(u1['battery'], 2))
    u1_sold.append(round(to_sell, 2))

    u2_consumption.append(round(c2, 2))
    u2_from_user1.append(round(from_user1, 2))
    u2_from_grid.append(round(from_grid2, 2))

    time.sleep(SIM_INTERVAL)

# -----------------------
# PLOTTING
# -----------------------
plt.figure(1, figsize=(12, 8))
plt.subplot(2, 1, 1)
plt.plot(hours, u1_consumption, 'r-', label="User 1 - Consumption")
plt.plot(hours, u1_production, 'g-', label="User 1 - Production")
plt.plot(hours, u1_battery, 'b-', label="Battery Level")
plt.title("User 1 - Energy Overview")
plt.xlabel("Hour")
plt.ylabel("kWh")
plt.legend()
plt.grid(True)

plt.subplot(2, 1, 2)
plt.plot(hours, u2_consumption, 'k-', label="User 2 - Consumption")
plt.plot(hours, u2_from_user1, 'c-', label="From User 1")
plt.plot(hours, u2_from_grid, 'm-', label="From Grid")
plt.title("User 2 - Energy Sources")
plt.xlabel("Hour")
plt.ylabel("kWh")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig("realistic_energy_simulation.png")
plt.show()

print("✅ Simulation completed. Graph saved as 'realistic_energy_simulation.png'.")
