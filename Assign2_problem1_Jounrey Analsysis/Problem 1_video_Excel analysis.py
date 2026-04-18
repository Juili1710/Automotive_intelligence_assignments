# -*- coding: utf-8 -*-
"""
Created on Sun Feb  8 15:16:52 2026

@author: Lenovo
"""

import cv2
import pytesseract
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# PART A: SPEED EXTRACTION FROM VIDEO (IMAGE PROCESSING)
# -----------------------------

video_path = "maps_recording.mp4"   # EDIT
cap = cv2.VideoCapture(video_path)

fps = cap.get(cv2.CAP_PROP_FPS)
speed_from_video = []
time_video = []

frame_id = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    if frame_id % int(fps) == 0:  # one frame per second
        roi = frame[50:150, 400:700]  # ADJUST to speed display region
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

        text = pytesseract.image_to_string(thresh, config='--psm 7 digits')
        try:
            speed = float(text.strip())
            speed_from_video.append(speed)
            time_video.append(frame_id / fps)
        except:
            pass

    frame_id += 1

cap.release()

# Plot extracted speed
plt.figure()
plt.plot(time_video, speed_from_video)
plt.xlabel("Time (s)")
plt.ylabel("Speed (km/h)")
plt.title("Speed vs Time (Image Processing)")
plt.grid()
plt.show()

# -----------------------------
# PART B: EXCEL DATA FOR CALCULATIONS
# -----------------------------

df = pd.read_excel("speed_data.xlsx")

time = df["time_sec"].values
speed_kmph = df["speed_kmph"].values
speed_mps = speed_kmph * 1000 / 3600

# -----------------------------
# 1(b) Time to Travel 10 km
# -----------------------------
speed_safe = np.where(speed_kmph == 0, np.nan, speed_kmph)
time_10km_min = (10 / speed_safe) * 60

plt.figure()
plt.plot(time, time_10km_min)
plt.xlabel("Time (s)")
plt.ylabel("Time to travel 10 km (min)")
plt.title("Instantaneous Travel Time for 10 km")
plt.grid()
plt.show()

# -----------------------------
# 1(c) Distance Integration
# -----------------------------
distance_m = np.cumsum(speed_mps * np.gradient(time))
distance_km = distance_m / 1000

plt.figure()
plt.plot(time, distance_km)
plt.xlabel("Time (s)")
plt.ylabel("Distance (km)")
plt.title("Distance Covered vs Time")
plt.grid()
plt.show()

# -----------------------------
# 1(d) Acceleration
# -----------------------------
acc = np.gradient(speed_mps, time)

plt.figure()
plt.plot(time, acc)
plt.xlabel("Time (s)")
plt.ylabel("Acceleration (m/s²)")
plt.title("Acceleration vs Time")
plt.grid()
plt.show()

# -----------------------------
# 1(e) Jerk
# -----------------------------
jerk = np.gradient(acc, time)

plt.figure()
plt.plot(time, jerk)
plt.xlabel("Time (s)")
plt.ylabel("Jerk (m/s³)")
plt.title("Jerk vs Time")
plt.grid()
plt.show()
