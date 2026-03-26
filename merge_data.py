import pandas as pd

# Load data
disaster_df = pd.read_csv("cleaned_disaster_data.csv")

# Dummy weather data (agar file nahi hai)
weather_df = pd.DataFrame({
    "year": disaster_df["year"],
    "district": ["Pune"] * len(disaster_df),
    "rainfall": [100] * len(disaster_df),
    "temperature": [30] * len(disaster_df),
    "wind_speed": [10] * len(disaster_df)
})

# Add district column in disaster_df (important)
disaster_df["district"] = "Pune"

# Merge
merged_df = pd.merge(disaster_df, weather_df, on=["year", "district"])

# Show output
print("Merged Shape:", merged_df.shape)
print(merged_df.head(3))

# Save file
merged_df.to_csv("final_merged_data.csv", index=False)

print("✅ File saved successfully!")