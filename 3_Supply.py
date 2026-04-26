import streamlit as st
import requests

st.title("📦 Supply Planner")

lat = st.number_input("Latitude")
lon = st.number_input("Longitude")
population = st.number_input("Population")
days = st.number_input("Days")

if st.button("Generate Plan"):
    res = requests.post(
        "http://127.0.0.1:5000/disaster/plan",
        json={
            "lat": lat,
            "lon": lon,
            "population": population,
            "days": days
        }
    )

    data = res.json()

    st.write("Warehouse:", data["warehouse"])
    st.write("Food Required:", data["food_required"])
    st.write("Water Required:", data["water_required"])
