import math

def calculate_distance(lat1, lon1, lat2, lon2):
    return ((lat1 - lat2)**2 + (lon1 - lon2)**2) ** 0.5

def find_nearest_warehouse(user_lat, user_lon, warehouses):
    nearest = None
    min_dist = float('inf')

    for w in warehouses:
        dist = calculate_distance(user_lat, user_lon, w['latitude'], w['longitude'])

        if dist < min_dist:
            min_dist = dist
            nearest = w

    return nearest
def find_best_warehouse(user_lat, user_lon, warehouses, food_needed):
    # Sort by distance
    warehouses_sorted = sorted(
        warehouses,
        key=lambda w: calculate_distance(user_lat, user_lon, w['latitude'], w['longitude'])
    )

    # Try to find one with enough stock
    for w in warehouses_sorted:
        if w.get("food_stock", 0) >= food_needed:
            return {
                "selected": w,
                "enough": True
            }

    # If none have enough → return nearest anyway
    return {
        "selected": warehouses_sorted[0] if warehouses_sorted else None,
        "enough": False
    }
