from flask import Blueprint, request, jsonify
from backend.models.warehouse_model import get_all_warehouses
from backend.services.route_service import find_nearest_warehouse

disaster_bp = Blueprint('disaster', __name__)

@disaster_bp.route("/nearest", methods=["POST"])
def nearest():
    data = request.json
    warehouses = get_all_warehouses()

    nearest = find_nearest_warehouse(
        data['lat'],
        data['lon'],
        warehouses
    )

    return jsonify(nearest)
from flask import Blueprint, request, jsonify
from backend.services.food_service import calculate_food

disaster_bp = Blueprint('disaster', __name__)

@disaster_bp.route("/food", methods=["POST"])
def food_required():
    data = request.get_json()

    population = data["population"]
    days = data["days"]

    total_food = calculate_food(population, days)

    return jsonify({
        "total_food_required": total_food
    })
from backend.services.route_service import find_best_warehouse
from backend.models.warehouse_model import get_all_warehouses

@disaster_bp.route("/plan", methods=["POST"])
def plan_supply():
    data = request.get_json()

    lat = data["lat"]
    lon = data["lon"]
    population = data["population"]
    days = data["days"]

    food_needed = calculate_food(population, days)
    warehouses = get_all_warehouses()

    result = find_best_warehouse(lat, lon, warehouses, food_needed)

    return jsonify({
        "food_needed": food_needed,
        "warehouse": result["selected"],
        "enough_stock": result["enough"]
    })
