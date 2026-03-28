def delivery_eta(distance_km, disaster_type="Normal", truck_speed=60, loading_time_hours=1.5):
    # Adjust speed if distance > 200 km
    if distance_km > 200:
        truck_speed = 45

    # Add emergency loading time if disaster is Critical
    if disaster_type.lower() == "critical":
        loading_time_hours += 0.5  # 30 minutes

    # Travel time
    travel_time_hours = distance_km / truck_speed

    # Total time
    total_time_hours = travel_time_hours + loading_time_hours

    # Convert to hours and minutes
    hours = int(total_time_hours)
    minutes = int((total_time_hours - hours) * 60)

    return hours, minutes


# -------- Test Data --------
warehouses = [
    ("Thane", 23),
    ("Pune", 148),
    ("Nashik", 320)
]

disaster_type = "Critical"  # Change to Normal if needed

# -------- Output --------
print("\n===== Delivery ETA =====\n")

for name, distance in warehouses:
    hours, minutes = delivery_eta(distance, disaster_type)

    if hours == 0:
        eta = f"{minutes} minutes"
    else:
        eta = f"{hours} hr {minutes} min"

    print(f"Warehouse: {name} | Distance: {distance}km | ETA: {eta}")