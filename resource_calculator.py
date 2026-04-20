# resource_calculator.py

def calculate_resources(disaster_type, affected_population, days=7):
    """
    Calculate required resources based on disaster type and affected population.

    Parameters:
    disaster_type (str): Type of disaster (flood, earthquake, cyclone, etc.)
    affected_population (int): Number of affected people
    days (int): Number of days for relief (default = 7)

    Returns:
    dict: Required quantities of water (liters), food (meals),
          medical kits, and tents
    """

    # --- Standard assumptions (approx NDRF guidelines) ---
    WATER_PER_PERSON_PER_DAY = 5        # liters
    FOOD_PER_PERSON_PER_DAY = 3         # meals
    PEOPLE_PER_TENT = 5
    PEOPLE_PER_MEDICAL_KIT = 50

    # --- Base calculations ---
    water = affected_population * WATER_PER_PERSON_PER_DAY * days
    food = affected_population * FOOD_PER_PERSON_PER_DAY * days
    tents = (affected_population // PEOPLE_PER_TENT) + (affected_population % PEOPLE_PER_TENT > 0)
    medical_kits = (affected_population // PEOPLE_PER_MEDICAL_KIT) + (affected_population % PEOPLE_PER_MEDICAL_KIT > 0)

    # --- Disaster-specific adjustments ---
    disaster_type = disaster_type.lower()

    if disaster_type == "flood":
        water *= 1.2        # contamination risk
        medical_kits *= 1.3

    elif disaster_type == "earthquake":
        tents *= 1.5        # more shelter needed
        medical_kits *= 1.5

    elif disaster_type == "cyclone":
        food *= 1.2
        tents *= 1.2

    elif disaster_type == "drought":
        water *= 1.5

    # Round values properly
    resources = {
        "water_liters": int(water),
        "food_meals": int(food),
        "tents": int(tents),
        "medical_kits": int(medical_kits)
    }

    return resources


# Example usage
if __name__ == "__main__":
    result = calculate_resources("flood", 1000, days=7)
    print("Estimated Resources Needed:")
    for key, value in result.items():
        print(f"{key}: {value}")