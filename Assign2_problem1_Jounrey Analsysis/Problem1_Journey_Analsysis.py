# -*- coding: utf-8 -*-
"""
Created on Sun Feb  8 14:23:18 2026

@author: Lenovo
"""

import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# INPUT DATA (EDIT THIS)
# -----------------------------
# Time in seconds (example: every 10 seconds)
time = np.array([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120])

# Speed from Google Maps (km/h)
speed_kmph = np.array([0, 18, 22, 25, 28, 30, 32, 30, 28, 25, 20, 15, 0])

# -----------------------------
# CONVERSIONS
# -----------------------------
speed_mps = speed_kmph * (1000/3600)  # km/h → m/s

# -----------------------------
# 1(a) Speed vs Time
# -----------------------------
plt.figure()
plt.plot(time, speed_kmph, marker='o')
plt.xlabel("Time (s)")
plt.ylabel("Speed (km/h)")
plt.title("Speed vs Time")
plt.grid()
plt.show()

# -----------------------------
# 1(b) Instantaneous time to travel 10 km
# -----------------------------
# Avoid division by zero
speed_kmph_safe = np.where(speed_kmph == 0, np.nan, speed_kmph)
time_to_10km_hr = 10 / speed_kmph_safe
time_to_10km_min = time_to_10km_hr * 60

plt.figure()
plt.plot(time, time_to_10km_min, marker='o')
plt.xlabel("Time (s)")
plt.ylabel("Time to travel 10 km (min)")
plt.title("Instantaneous Time to Travel 10 km")
plt.grid()
plt.show()

# -----------------------------
# 1(c) Distance calculation
# -----------------------------
distance = np.cumsum(speed_mps * np.gradient(time))  # meters
distance_km = distance / 1000

plt.figure()
plt.plot(time, distance_km, marker='o')
plt.xlabel("Time (s)")
plt.ylabel("Distance Covered (km)")
plt.title("Cumulative Distance Covered")
plt.grid()
plt.show()

# -----------------------------
# 1(c2) Percentage Error
# -----------------------------
actual_distance_km = 10  # EDIT if different
calculated_distance_km = distance_km[-1]

percentage_error = abs(calculated_distance_km - actual_distance_km) / actual_distance_km * 100

print("Calculated Distance (km):", calculated_distance_km)
print("Percentage Error (%):", percentage_error)

# -----------------------------
# 1(c3) Speed Error Metrics
# -----------------------------
inst_speed_calc = np.gradient(distance_km, time) * 3600  # km/h
error = inst_speed_calc - speed_kmph

absolute_error = np.abs(error)
mean_error = np.mean(error)
rmse = np.sqrt(np.mean(error**2))

print("Mean Error (km/h):", mean_error)
print("RMSE (km/h):", rmse)

# -----------------------------
# 1(d) Acceleration vs Time
# -----------------------------
acceleration = np.gradient(speed_mps, time)

plt.figure()
plt.plot(time, acceleration)
plt.xlabel("Time (s)")
plt.ylabel("Acceleration (m/s²)")
plt.title("Acceleration vs Time")
plt.grid()
plt.show()

# -----------------------------
# 1(e) Jerk vs Time
# -----------------------------
jerk = np.gradient(acceleration, time)

plt.figure()
plt.plot(time, jerk)
plt.xlabel("Time (s)")
plt.ylabel("Jerk (m/s³)")
plt.title("Jerk vs Time")
plt.grid()
plt.show()
