# -*- coding: utf-8 -*-
"""
Created on Fri Feb 13 15:54:32 2026

@author: Lenovo
"""

class ADASVehicle:

    # --- Master Feature List ---
    FEATURE_LIST = {
        1: "Automatic Emergency Braking",
        2: "Forward Collision Warning",
        3: "Adaptive Cruise Control",
        4: "Stop and Go Cruise Control",
        5: "Intelligent Speed Assist",
        6: "Predictive Cruise Control",
        7: "Emergency Brake Assist",
        8: "Rear Automatic Braking",

        9: "Lane Keeping Assist",
        10: "Lane Departure Warning",
        11: "Lane Centering Assist",
        12: "Emergency Lane Assist",
        13: "Evasive Steering Assist",

        14: "Blind Spot Detection",
        15: "Rear Cross Traffic Alert",
        16: "Traffic Sign Recognition",
        17: "Pedestrian Detection",
        18: "Cyclist Detection",
        19: "Driver Drowsiness Monitoring",
        20: "Driver Attention Monitoring",
        21: "Night Vision Assist",
        22: "High Beam Assist",
        23: "Adaptive Headlights",
        24: "Collision Mitigation System",
        25: "Turn Assist",
        26: "Crosswind Assist",

        27: "Park Assist",
        28: "Automated Parking",
        29: "Remote Parking Assist",
        30: "360 Surround View",
        31: "Parking Sensors",

        32: "Traffic Jam Assist",
        33: "Highway Pilot",
        34: "Conditional Autonomous Driving",
        35: "Geofenced Autonomous Driving",
        36: "Automated Valet Parking",
        37: "Robotaxi Mode",
        38: "Full Self Driving",

        39: "Automatic Lane Change",
        40: "Emergency Stop Assist",
        41: "Intersection Assist",
        42: "Wrong Way Warning",
        43: "Speed Limit Adaptation",
        44: "Active Steering Control",
        45: "Active Braking Control"
    }

    # --- Control Category Sets ---
    LONGITUDINAL = {1,3,4,5,6,7,8,32,45}
    LATERAL = {9,11,12,13,39,44}
    HIGH_AUTONOMY = {33,34,35,36,37,38}

    def __init__(self):
        self.selected_features = set()
        self.monitoring = None
        self.takeover_required = None
        self.operational_domain = None

    def determine_level(self):

        if self.monitoring == "human":
            longitudinal = len(self.selected_features & self.LONGITUDINAL) > 0
            lateral = len(self.selected_features & self.LATERAL) > 0

            if longitudinal and lateral:
                return 2
            elif longitudinal or lateral:
                return 1
            else:
                return 0

        elif self.monitoring == "system":
            if self.takeover_required:
                return 3
            else:
                if self.operational_domain == "limited":
                    return 4
                elif self.operational_domain == "all":
                    return 5

        return "Unknown"


# -----------------------------
# USER INTERFACE
# -----------------------------

vehicle = ADASVehicle()

print("\n--- ADAS Feature List ---\n")

for number, feature in ADASVehicle.FEATURE_LIST.items():
    print(f"{number}: {feature}")

print("\nEnter the feature numbers your car has (comma separated):")
user_input = input("Selection: ")

selected_numbers = [int(x.strip()) for x in user_input.split(",")]
vehicle.selected_features = set(selected_numbers)

print("\nWho monitors the driving environment?")
print("1: Human")
print("2: System")
choice = input("Enter 1 or 2: ")

if choice == "1":
    vehicle.monitoring = "human"
else:
    vehicle.monitoring = "system"

if vehicle.monitoring == "system":
    takeover = input("Does driver need to take over when requested? (yes/no): ")
    vehicle.takeover_required = (takeover.lower() == "yes")

    if not vehicle.takeover_required:
        domain = input("Is autonomy limited to specific areas? (limited/all): ")
        vehicle.operational_domain = domain.lower()

level = vehicle.determine_level()

print("\nEstimated SAE Automation Level:", level)