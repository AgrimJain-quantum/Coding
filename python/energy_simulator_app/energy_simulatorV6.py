import requests
import time
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import random
from math import sin, pi

# -----------------------------------
# CONFIGURATION
# -----------------------------------
API_KEY = '1310cc9029637831bbb879313d029008'
LAT = '26.9124'  # Jaipur latitude
LON = '75.7873'  # Jaipur longitude
SEASON = 'Summer'  # Options: Summer, Winter, Monsoon
SIM_HOURS = 24
SIM_INTERVAL = 1  # seconds per simulated hour

# -----------------------------------
# WEATHER DATA
# -----------------------------------
def get_weather_data():
    url = f'https://api.openweathermap.org/data/2.5/forecast?lat={LAT}&lon={LON}&appid={API_KEY}'
    res = requests.get(url)
    if res.status_code != 200:
        print("Weather API failed.")
        return {hour: 50 for hour in range(24)}  # Default 50% cloud if API fails
    data = res.json()
    forecast = {}
    for item in data['list']:
        hour = datetime.utcfromtimestamp(item['dt']).hour
        cloud_pct = item['clouds']['all']
        forecast[hour] = cloud_pct
    return forecast

weather_forecast = get_weather_data()

# -----------------------------------
# USER PROFILES
# -----------------------------------
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

# -----------------------------------
# SEASON + TIME CONSUMPTION LOGIC
# -----------------------------------
def get_hour_factor(hour, season, user_type):
    if user_type == "Home Office":
        if 9 <= hour <= 17: base = 1.2
        elif 18 <= hour <= 22: base = 1.1
        else: base = 0.7
    elif user_type == "Day Worker":
        if 6 <= hour <= 8: base = 1.0
        elif 18 <= hour <= 22: base = 1.3
        else: base = 0.5
    else: base = 1.0

    if season == "Summer": base += 0.2
    elif season == "Winter": base += 0.1 if hour >= 18 else -0.1

    return base

# -----------------------------------
# REALISTIC SOLAR PRODUCTION
# -----------------------------------
def get_solar_production(hour, solar_capacity):
    if 6 <= hour <= 18:
        sunlight_curve = sin((pi / 12) * (hour - 6))  # peak at 12:00
        cloud_factor = 1 - (weather_forecast.get(hour, 50) / 100)
        return solar_capacity * sunlight_curve * cloud_factor
    return 0

# -----------------------------------
# LOGGING & SIMULATION
# -----------------------------------
hours = []
u1_consumption, u1_production, u1_battery, u1_sold = [], [], [], []
u2_consumption, u2_from_user1, u2_from_grid = [], [], []

start_time = datetime.now().replace(minute=0, second=0, microsecond=0)

for hour in range(SIM_HOURS):
    hr = (start_time + timedelta(hours=hour)).hour
    print(f"⏳ Hour {hr}:00")

    # --- USER 1 ---
    u1 = users["user_1"]
    c1 = random.uniform(2.0, 3.5) * get_hour_factor(hr, SEASON, u1['user_type'])
    p1 = get_solar_production(hr, u1['solar_capacity'])
    net1 = p1 - c1

    to_sell = 0
    if net1 > 0:
        free_capacity = u1['battery_capacity'] - u1['battery']
        to_battery = min(free_capacity, net1)
        u1['battery'] += to_battery
        # Only sell if battery is at least 30% full
        if u1['battery'] > 0.3 * u1['battery_capacity']:
            to_sell = net1 - to_battery
    else:
        need = abs(net1)
        from_batt = min(need, u1['battery'])
        u1['battery'] -= from_batt
        from_grid = need - from_batt

    # --- USER 2 ---
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

    # --- LOGGING ---
    hours.append(hr)
    u1_consumption.append(round(c1, 2))
    u1_production.append(round(p1, 2))
    u1_battery.append(round(u1['battery'], 2))
    u1_sold.append(round(to_sell, 2))

    u2_consumption.append(round(c2, 2))
    u2_from_user1.append(round(from_user1, 2))
    u2_from_grid.append(round(from_grid2, 2))

    time.sleep(SIM_INTERVAL)

# -----------------------------------
# PLOTTING
# -----------------------------------
def plot_smooth(data, label, color):
    plt.plot(hours, data, label=label, color=color)

plt.figure(figsize=(12, 8))

# USER 1
plt.subplot(2, 1, 1)
plot_smooth(u1_consumption, 'User 1 - Consumption', 'r')
plot_smooth(u1_production, 'User 1 - Production', 'g')
plot_smooth(u1_battery, 'Battery Level', 'b')
plt.title("User 1 - Energy Overview")
plt.xlabel("Hour")
plt.ylabel("kWh")
plt.legend()
plt.grid(True)

# USER 2
plt.subplot(2, 1, 2)
plot_smooth(u2_consumption, 'User 2 - Consumption', 'k')
plot_smooth(u2_from_user1, 'From User 1', 'c')
plot_smooth(u2_from_grid, 'From Grid', 'm')
plt.title("User 2 - Energy Sources")
plt.xlabel("Hour")
plt.ylabel("kWh")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig("realistic_energy_simulation.png")
plt.show()

print("✅ Simulation complete. Graph saved as 'realistic_energy_simulation.png'")
