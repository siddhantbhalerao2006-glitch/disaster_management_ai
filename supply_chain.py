import json
from geopy.distance import geodesic
from tabulate import tabulate

# ------------------ 1. Disaster Prediction (dummy) ------------------
disaster_prediction = {
    "type": "Flood",
    "severity": "Critical",
    "location": (19.08, 72.88)  # Mumbai
}

# ------------------ 2. Resource Calculation ------------------
def calculate_resources(disaster_type, affected_population, days=7):
    water = 3 * affected_population * days
    food = affected_population * days
    medical = -(-affected_population // 50)
    tents = -(-affected_population // 5)
    vehicles = -(-affected_population // 10000)

    if disaster_type.lower() in ["flood", "cyclone"]:
        water *= 2
        food *= 2
        medical *= 2
        tents *= 2
        vehicles *= 2

    return {
        "water_liters": water,
        "food_packets": food,
        "medical_kits": medical,
        "shelter_tents": tents,
        "rescue_vehicles": vehicles
    }

# ------------------ 3. Nearest Warehouse ------------------
warehouses = [
    ("Thane", 19.21, 72.97),
    ("Pune", 18.52, 73.85),
    ("Nashik", 19.99, 73.79),
    ("Aurangabad", 19.87, 75.34),
    ("Nagpur", 21.14, 79.08)
]

def find_nearest(disaster_loc):
    distances = []
    for name, lat, lon in warehouses:
        dist = geodesic(disaster_loc, (lat, lon)).km
        distances.append((name, dist))
    distances.sort(key=lambda x: x[1])
    return distances[0]  # nearest one

# ------------------ 4. Delivery ETA ------------------
def delivery_eta(distance_km, disaster_type):
    speed = 60
    if distance_km > 200:
        speed = 45

    loading = 1.5
    if disaster_type.lower() == "critical":
        loading += 0.5

    total_hours = (distance_km / speed) + loading
    hours = int(total_hours)
    minutes = int((total_hours - hours) * 60)

    return f"{hours} hr {minutes} min" if hours > 0 else f"{minutes} minutes"

# ------------------ 5. Combine Everything ------------------
population = 50000

resources = calculate_resources(disaster_prediction["type"], population)

nearest_name, nearest_distance = find_nearest(disaster_prediction["location"])

eta = delivery_eta(nearest_distance, disaster_prediction["severity"])

supply_chain_output = {
    "disaster": disaster_prediction,
    "resources": resources,
    "nearest_warehouse": {
        "name": nearest_name,
        "distance_km": round(nearest_distance, 2)
    },
    "delivery_eta": eta
}

# ------------------ 6. Save as JSON ------------------
with open("supply_chain_result.json", "w") as f:
    json.dump(supply_chain_output, f, indent=4)

# ------------------ 7. Print Table ------------------
table = [
    ["Disaster Type", disaster_prediction["type"]],
    ["Severity", disaster_prediction["severity"]],
    ["Nearest Warehouse", nearest_name],
    ["Distance (km)", round(nearest_distance, 2)],
    ["Delivery ETA", eta],
    ["Water (L)", resources["water_liters"]],
    ["Food Packets", resources["food_packets"]],
    ["Medical Kits", resources["medical_kits"]],
    ["Tents", resources["shelter_tents"]],
    ["Rescue Vehicles", resources["rescue_vehicles"]],
]

print("\n===== Supply Chain Summary =====\n")
print(tabulate(table, headers=["Parameter", "Value"], tablefmt="grid"))