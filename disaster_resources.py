def calculate_resources(disaster_type, affected_population, days=7):
    # Base calculations
    water_liters = 3 * affected_population * days
    food_packets = 1 * affected_population * days
    medical_kits = affected_population // 50 + (1 if affected_population % 50 != 0 else 0)
    shelter_tents = affected_population // 5 + (1 if affected_population % 5 != 0 else 0)
    rescue_vehicles = affected_population // 10000 + (1 if affected_population % 10000 != 0 else 0)

    # Double resources for severe disasters
    if disaster_type.lower() in ["flood", "cyclone"]:
        water_liters *= 2
        food_packets *= 2
        medical_kits *= 2
        shelter_tents *= 2
        rescue_vehicles *= 2

    # Store in dictionary
    resources = {
        "Water (liters)": water_liters,
        "Food Packets": food_packets,
        "Medical Kits": medical_kits,
        "Shelter Tents": shelter_tents,
        "Rescue Vehicles": rescue_vehicles
    }

    return resources


# -------- Example Usage --------
disaster_type = input("Enter disaster type: ")
population = int(input("Enter affected population: "))
days = int(input("Enter number of days (default 7): ") or 7)

result = calculate_resources(disaster_type, population, days)

# -------- Formatted Output Table --------
print("\n===== Disaster Resource Summary =====")
print(f"Disaster Type      : {disaster_type}")
print(f"Affected Population: {population}")
print(f"Days               : {days}")
print("--------------------------------------")
print("{:<20} {:>10}".format("Resource", "Quantity"))
print("--------------------------------------")

for key, value in result.items():
    print("{:<20} {:>10}".format(key, value))

print("--------------------------------------")