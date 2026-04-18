# -*- coding: utf-8 -*-
"""
Created on Sun Feb  8 14:25:09 2026

@author: Lenovo
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, find_peaks

video_path = "heartbeat_video.mp4"  # EDIT THIS

cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)

signal = []

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    red = frame[:, :, 2]
    signal.append(np.mean(red))

cap.release()

signal = np.array(signal)
time = np.arange(len(signal)) / fps

# Normalize
signal = signal - np.mean(signal)
signal = signal / np.max(np.abs(signal))

# Bandpass filter
def bandpass(data, low, high, fs, order=3):
    nyq = 0.5 * fs
    b, a = butter(order, [low/nyq, high/nyq], btype='band')
    return filtfilt(b, a, data)

filtered = bandpass(signal, 0.7, 3.0, fps)

# Peak detection
peaks, _ = find_peaks(filtered, distance=fps*0.4)

# Plots
plt.figure()
plt.plot(time, filtered)
plt.plot(time[peaks], filtered[peaks], 'rx')
plt.xlabel("Time (s)")
plt.ylabel("Pulse Signal")
plt.title("Heartbeat Detection using PPG")
plt.show()

# Calculations
total_beats = len(peaks)
duration_min = time[-1] / 60
bpm = total_beats / duration_min

print("Total Beats:", total_beats)
print("Average BPM:", bpm)

# Beats per 10 seconds
beats_10s = []
for t in np.arange(0, time[-1], 10):
    beats_10s.append(np.sum((time[peaks] >= t) & (time[peaks] < t+10)))

print("Beats per 10 seconds:", beats_10s)
