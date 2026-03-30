# from joblib import load

# season_encoder = load("season_encoder.pkl")
import pandas as pd

df = pd.read_csv("cleaned_disaster_data.csv")
print(df.columns)