import streamlit as st
import requests

st.title("🌊 Disaster Management System")

# -------- Flood Prediction --------
st.header("Flood Prediction")

rainfall = st.number_input("Rainfall")
river = st.number_input("River Level")
temp = st.number_input("Temperature")

if st.button("Predict"):
    response = requests.post(
        "http://127.0.0.1:5000/predict/",
        json={
            "rainfall": rainfall,
            "river_level": river,
            "temperature": temp
        }
    )

    data = response.json()

    if data["flood_risk"] == 1:
        st.error("⚠️ Flood Risk!")
    else:
        st.success("✅ Safe")

# -------- NEW PART (ADD THIS BELOW) --------
st.header("📦 Find Nearest Warehouse")

lat = st.number_input("Your Latitude")
lon = st.number_input("Your Longitude")

if st.button("Find Warehouse"):
    response = requests.post(
        "http://127.0.0.1:5000/warehouse/nearest",
        json={"lat": lat, "lon": lon}
    )

    data = response.json()

    st.write("FULL RESPONSE:", data)
    st.write("Food Stock:", data["food_stock"])


st.header("Food Requirement Calculator")

population = st.number_input("Population", min_value=1)
days = st.number_input("Number of Days", min_value=1)

if st.button("Calculate Food"):
    response = requests.post(
        "http://127.0.0.1:5000/disaster/food",
        json={
            "population": population,
            "days": days
        }
    )

    data = response.json()
    st.success(f"Total Food Required: {data['total_food_required']}")
st.header("🚚 Smart Supply Planner")

lat = st.number_input("Location Latitude", key="plan_lat")
lon = st.number_input("Location Longitude", key="plan_lon")
population = st.number_input("Population", min_value=1, key="plan_pop")
days = st.number_input("Days", min_value=1, key="plan_days")

if st.button("Plan Supply"):
    response = requests.post(
        "http://127.0.0.1:5000/disaster/plan",
        json={
            "lat": lat,
            "lon": lon,
            "population": population,
            "days": days
        }
    )

    data = response.json()

    st.write("Food Needed:", data["food_needed"])
    st.write("Selected Warehouse:", data["warehouse"]["name"])

    if data["enough_stock"]:
        st.success("✅ Warehouse has enough stock")
    else:
        st.warning("⚠️ Not enough stock, but nearest selected")

