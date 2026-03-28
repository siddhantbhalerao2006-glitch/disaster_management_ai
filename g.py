from joblib import load

encoder = load("season_encoder.pkl")
print(encoder.classes_)