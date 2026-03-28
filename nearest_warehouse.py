from geopy.distance import geodesic

# Disaster location (Mumbai)
disaster_location = (19.08, 72.88)

# Warehouses: (Name, Latitude, Longitude)
warehouses = [
    ("Thane", 19.21, 72.97),
    ("Pune", 18.52, 73.85),
    ("Nashik", 19.99, 73.79),
    ("Aurangabad", 19.87, 75.34),
    ("Nagpur", 21.14, 79.08)
]

# Calculate distances
distances = []

for name, lat, lon in warehouses:
    warehouse_location = (lat, lon)
    distance_km = geodesic(disaster_location, warehouse_location).kilometers
    distances.append((name, distance_km))

# Sort by distance
distances.sort(key=lambda x: x[1])

# Get 2 nearest warehouses
nearest_two = distances[:2]

# Print results
print("\n===== Nearest Warehouses =====")
print("{:<15} {:>15}".format("Warehouse", "Distance (km)"))
print("----------------------------------------")

for name, dist in nearest_two:
    print("{:<15} {:>15.2f}".format(name, dist))

print("----------------------------------------")