import streamlit as st
import pandas as pd
import requests

st.title("🗺️ Disaster Map")

# Get warehouse data
response = requests.get("http://127.0.0.1:5000/warehouse/")
warehouses = response.json()

df = pd.DataFrame(warehouses)

st.map(df.rename(columns={
    "latitude": "lat",
    "longitude": "lon"
}))
