import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load your dataset
df = pd.read_csv("cleaned_disaster_data.csv")
print(df.head())

# Encode target 'disaster_type'
disaster_encoder = LabelEncoder()
df['disaster_type_encoded'] = disaster_encoder.fit_transform(df['disaster_type'])

# Use available features: year, deaths, affected, magnitude
X = df[['year', 'deaths', 'affected', 'magnitude']].fillna(0)  # Fill NaN with 0
y = df['disaster_type_encoded']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Predict and evaluate
y_pred = rf_model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred, target_names=disaster_encoder.classes_))

# Save model and encoder
joblib.dump(rf_model, 'disaster_model.pkl')
joblib.dump(disaster_encoder, 'disaster_label_encoder.pkl')
print("Model and encoder saved successfully!")