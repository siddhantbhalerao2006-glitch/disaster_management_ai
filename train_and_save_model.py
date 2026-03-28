import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# 1️⃣ Load dataset
df = pd.read_csv("cleaned_disaster_data.csv")

# 2️⃣ Encode categorical columns
season_encoder = LabelEncoder()
df['season_encoded'] = season_encoder.fit_transform(df['season'])

target_encoder = LabelEncoder()
df['disaster_type_encoded'] = target_encoder.fit_transform(df['disaster_type'])

# 3️⃣ Prepare features and target
X = df[['rainfall_mm', 'temperature_c', 'wind_speed_kmph', 'season_encoded', 'population_lakhs']]
y = df['disaster_type_encoded']

# 4️⃣ Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5️⃣ Train Random Forest
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)  # ✅ Now rf_model exists

# 6️⃣ Evaluate
y_pred = rf_model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred, target_names=target_encoder.classes_))

# 7️⃣ Save model and encoders
joblib.dump(rf_model, 'disaster_model.pkl')
joblib.dump(season_encoder, 'season_label_encoder.pkl')
joblib.dump(target_encoder, 'disaster_label_encoder.pkl')
print("Model and encoders saved successfully!")