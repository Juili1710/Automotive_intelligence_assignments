# -*- coding: utf-8 -*-


class ADASVehicle:

    # --- Feature Database ---
    LONGITUDINAL = {
        "automatic emergency braking",
        "forward collision warning",
        "adaptive cruise control",
        "stop and go cruise control",
        "intelligent speed assist",
        "predictive cruise control",
        "emergency brake assist",
        "rear automatic braking"
    }

    LATERAL = {
        "lane keeping assist",
        "lane departure warning",
        "lane centering assist",
        "emergency lane assist",
        "evasive steering assist"
    }

    PARKING_LOW_SPEED = {
        "park assist",
        "automated parking",
        "remote parking assist",
        "360 surround view",
        "parking sensors"
    }

    MONITORING_ONLY = {
        "blind spot detection",
        "rear cross traffic alert",
        "traffic sign recognition",
        "pedestrian detection",
        "cyclist detection",
        "driver drowsiness monitoring",
        "driver attention monitoring",
        "night vision assist",
        "high beam assist",
        "adaptive headlights",
        "collision mitigation system",
        "turn assist",
        "crosswind assist"
    }

    HIGH_AUTONOMY = {
        "highway pilot",
        "conditional autonomous driving",
        "geofenced autonomous driving",
        "automated valet parking",
        "robotaxi mode",
        "full self driving"
    }

    # --- Initialization ---
    def __init__(self):
        self.features = set()
        self.monitoring = None
        self.takeover_required = None
        self.operational_domain = None

    # --- Add Features ---
    def add_features(self, feature_list):
        for f in feature_list:
            self.features.add(f.strip().lower())

    # --- Determine Level ---
    def determine_level(self):

        # Human monitors
        if self.monitoring == "human":

            longitudinal = len(self.features & self.LONGITUDINAL) > 0
            lateral = len(self.features & self.LATERAL) > 0

            if longitudinal and lateral:
                return 2
            elif longitudinal or lateral:
                return 1
            else:
                return 0

        # System monitors
        elif self.monitoring == "system":

            if self.takeover_required:
                return 3
            else:
                if self.operational_domain == "limited":
                    return 4
                elif self.operational_domain == "all":
                    return 5

        return "Unknown"


# --------------------------
# USER INTERFACE
# --------------------------

print("\n--- ADAS Feature Classifier (SAE J3016 Based) ---")

vehicle = ADASVehicle()

print("\nWho monitors driving environment?")
print("1: Human")
print("2: System")
choice = input("Enter choice (1/2): ")

if choice == "1":
    vehicle.monitoring = "human"
else:
    vehicle.monitoring = "system"

print("\nEnter your car's ADAS features (comma separated).")
print("Example: adaptive cruise control, lane keeping assist")

user_features = input("Features: ")
vehicle.add_features(user_features.split(","))

if vehicle.monitoring == "system":
    takeover = input("Does driver need to take over when requested? (yes/no): ")
    vehicle.takeover_required = (takeover.lower() == "yes")

    if not vehicle.takeover_required:
        domain = input("Is autonomy limited to specific areas? (limited/all): ")
        vehicle.operational_domain = domain.lower()

level = vehicle.determine_level()

print("\nEstimated SAE Automation Level:", level)