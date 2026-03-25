import pandas as pd

# 1. Load the dataset
# Make sure you have downloaded em_dat_disaster.csv from Kaggle first!
df = pd.read_csv('em_dat_disaster.csv')

# 2. Show basic info
print(f"Original Shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")

# 3. Filter for India
df_india = df[df['Country'] == 'India']

# 4. Drop rows with null values in critical columns
# Adjust column names if your CSV uses different casing (e.g., 'year' vs 'Year')
df_cleaned = df_india.dropna(subset=['Year', 'Disaster Type', 'Total Deaths'])

# 5. Save the cleaned file
df_cleaned.to_csv('cleaned_disaster_data.csv', index=False)
print("SUCCESS: cleaned_disaster_data.csv has been created.")