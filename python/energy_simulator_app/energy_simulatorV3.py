import time
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Set interactive mode on
plt.ion()

# Constants
SOLAR_HOURS = range(6, 19)
SIMULATION_INTERVAL = 2  # Seconds per hour (demo)
TOTAL_HOURS = 24

# User data
users = {
    "user_1": {
        "can_sell": True,
        "has_solar": True,
        "battery": 5,
        "battery_capacity": 10,
        "solar_capacity": 5,
    },
    "user_2": {
        "can_sell": False,
        "has_solar": False,
        "battery": 0,
        "battery_capacity": 0,
    }
}

# Data storage for plotting
hours = []
u1_consumption, u1_production, u1_battery, u1_sold = [], [], [], []
u2_consumption, u2_from_user1, u2_from_grid = [], [], []

# Simulation loop
start_time = datetime.now().replace(minute=0, second=0, microsecond=0)

for hour in range(TOTAL_HOURS):
    now = start_time + timedelta(hours=hour)
    hour_label = now.strftime("%H:%M")
    hour_of_day = now.hour
    print(f"⏳ Hour {hour_label}")

    # --- User 1 ---
    user1 = users["user_1"]
    c1 = random.uniform(2.0, 4.0)
    p1 = random.uniform(2.0, 5.0) if hour_of_day in SOLAR_HOURS else 0
    net1 = p1 - c1

    if net1 > 0:
        space = user1["battery_capacity"] - user1["battery"]
        to_battery = min(space, net1)
        user1["battery"] += to_battery
        to_sell = net1 - to_battery
    else:
        need = abs(net1)
        from_battery = min(need, user1["battery"])
        user1["battery"] -= from_battery
        from_grid = need - from_battery
        to_sell = 0

    # --- User 2 ---
    c2 = random.uniform(2.0, 4.0)
    if to_sell >= c2:
        from_user1 = c2
        from_grid2 = 0
        to_sell -= c2
    else:
        from_user1 = to_sell
        from_grid2 = c2 - from_user1
        to_sell = 0

    # Append data for plotting
    hours.append(hour)
    u1_consumption.append(c1)
    u1_production.append(p1)
    u1_battery.append(user1["battery"])
    u1_sold.append(to_sell)

    u2_consumption.append(c2)
    u2_from_user1.append(from_user1)
    u2_from_grid.append(from_grid2)

    # --- Plotting ---
    plt.figure(1, figsize=(12, 8))
    plt.clf()

    # Subplot 1: User 1
    plt.subplot(2, 1, 1)
    plt.plot(hours, u1_consumption, 'r-', label="User 1 - Consumption")
    plt.plot(hours, u1_production, 'g-', label="User 1 - Production")
    plt.plot(hours, u1_battery, 'b-', label="User 1 - Battery Level")
    plt.title("User 1 - Energy Overview")
    plt.xlabel("Hour")
    plt.ylabel("kWh")
    plt.legend()
    plt.grid(True)

    # Subplot 2: User 2
    plt.subplot(2, 1, 2)
    plt.plot(hours, u2_consumption, 'k-', label="User 2 - Consumption")
    plt.plot(hours, u2_from_user1, 'c-', label="User 2 - From User 1")
    plt.plot(hours, u2_from_grid, 'm-', label="User 2 - From Grid")
    plt.title("User 2 - Energy Sources")
    plt.xlabel("Hour")
    plt.ylabel("kWh")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.pause(0.1)  # Live update

    time.sleep(SIMULATION_INTERVAL)

plt.ioff()
plt.show()
print("✅ Live simulation completed.")