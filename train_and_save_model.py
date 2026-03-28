import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# 1️⃣ Load dataset
df = pd.read_csv("cleaned_disaster_data.csv")

# 2️⃣ Encode categorical columns
country_encoder = LabelEncoder()
df['country_encoded'] = country_encoder.fit_transform(df['country'])

# 3️⃣ Encode target
target_encoder = LabelEncoder()
df['disaster_type_encoded'] = target_encoder.fit_transform(df['disaster_type'])

# 4️⃣ Features (based on available data)
X = df[['country_encoded', 'year', 'deaths', 'affected', 'magnitude']]
y = df['disaster_type_encoded']

# 5️⃣ Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 6️⃣ Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 7️⃣ Evaluate
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred, target_names=target_encoder.classes_))

# 8️⃣ Save everything
joblib.dump(model, "disaster_model.pkl")
joblib.dump(country_encoder, "country_encoder.pkl")
joblib.dump(target_encoder, "disaster_label_encoder.pkl")

print("✅ Model and encoders saved successfully!")