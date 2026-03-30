import pandas as pd
import random

# Possible values
countries = ["India"]
disasters = ["Flood", "Cyclone", "Earthquake"]

data = []

for i in range(1500):
    country = random.choice(countries)
    year = random.randint(1995, 2025)
    disaster = random.choice(disasters)

    if disaster == "Flood":
        deaths = random.randint(100, 6000)
        affected = random.randint(50000, 20000000)
        magnitude = round(random.uniform(4.0, 6.0), 1)

    elif disaster == "Cyclone":
        deaths = random.randint(50, 10000)
        affected = random.randint(100000, 15000000)
        magnitude = round(random.uniform(5.0, 7.5), 1)

    else:  # Earthquake
        deaths = random.randint(10, 20000)
        affected = random.randint(10000, 6000000)
        magnitude = round(random.uniform(5.0, 8.0), 1)

    # 🔥 NEW FEATURE
    severity = deaths / (affected + 1)

    data.append([country, year, disaster, deaths, affected, magnitude, severity])

# Create DataFrame
df = pd.DataFrame(data, columns=[
    "country", "year", "disaster_type", "deaths", "affected", "magnitude", "severity"
])

# Save
df.to_csv("cleaned_disaster_data.csv", index=False)

print("✅ 1500 rows dataset generated with severity!")