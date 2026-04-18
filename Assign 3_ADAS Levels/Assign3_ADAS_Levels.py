# -*- coding: utf-8 -*-
"""
Created on Sun Feb  8 09:24:10 2026

@author: Lenovo
"""
adas_levels = {
    "no automation": 0,
    "adaptive cruise control": 1,
    "lane keeping assist": 1,
    "acc + lka": 2,
    "traffic jam assist": 2,
    "conditional autonomy": 3,
    "highway autopilot": 3,
    "geofenced autonomous driving": 4,
    "robotaxi": 4,
    "full self driving": 5
}

def get_automation_level(feature):
    feature = feature.lower()
    return adas_levels.get(feature, "Unknown ADAS feature")

# Example usage
feature = input("Enter ADAS feature: ")
print("Automation Level:", get_automation_level(feature))
