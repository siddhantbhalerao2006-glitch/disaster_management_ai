import joblib
from sklearn.preprocessing import LabelEncoder

# Create encoder
season_encoder = LabelEncoder()

# Example data (replace with your actual data)
seasons = ["Summer", "Winter", "Monsoon"]
season_encoder.fit(seasons)

# Save the file (this creates the .pkl file)
joblib.dump(season_encoder, "season_encoder.pkl")