from flask import Blueprint, request, jsonify
from backend.models.warehouse_model import get_all_warehouses
from backend.services.route_service import find_nearest_warehouse

# ✅ DEFINE FIRST
warehouse_bp = Blueprint('warehouse', __name__)

# ✅ THEN USE IT
@warehouse_bp.route("/", methods=["GET"])
def warehouses():
    data = get_all_warehouses()
    return jsonify(data)

@warehouse_bp.route("/nearest", methods=["POST"])
def nearest():
    try:
        data = request.get_json()
        print("Incoming:", data)

        warehouses = get_all_warehouses()
        print("Warehouses:", warehouses)

        nearest = find_nearest_warehouse(
            data['lat'],
            data['lon'],
            warehouses
        )

        return jsonify(nearest)

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500
