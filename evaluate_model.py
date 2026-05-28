import pandas as pd
import joblib
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

print("🚀 Starting evaluation...")

# =========================
# 1. Load dataset
# =========================
df = pd.read_csv("cleaned_disaster_data.csv")
print("✅ Data loaded:", df.shape)

# =========================
# 2. Normalize columns
# =========================
df.columns = df.columns.str.strip().str.lower()
print("📂 Columns:", df.columns.tolist())

# =========================
# 3. Fix severity scale (IMPORTANT)
# =========================
df['severity'] = np.log1p(df['severity'])

# =========================
# 4. Load encoder
# =========================
country_encoder = joblib.load("country_encoder.pkl")

# =========================
# 5. Detect country column
# =========================
country_col = [col for col in df.columns if "country" in col][0]
print("🌍 Country column:", country_col)

# =========================
# 6. Encode country
# =========================
df['country_encoded'] = country_encoder.transform(df[country_col])

# =========================
# 7. Features & target
# =========================
features = ['country_encoded', 'year', 'deaths', 'affected', 'magnitude']
target = 'severity'

X = df[features]
y = df[target]

print("📊 Features:", features)
print("🎯 Target:", target)

# =========================
# 8. Split
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# 9. Load model
# =========================
model = joblib.load("disaster_model.pkl")
print("✅ Model loaded")

# Ensure feature order matches
if hasattr(model, "feature_names_in_"):
    X_test = X_test[model.feature_names_in_]

# =========================
# 10. Predict
# =========================
print("🔮 Predicting...")
y_pred = model.predict(X_test)

# =========================
# 11. Reverse transform (IMPORTANT)
# =========================
y_test_actual = np.expm1(y_test)
y_pred_actual = np.expm1(y_pred)

# =========================
# 12. Evaluation
# =========================
print("\n📈 Evaluation Results:")

mse = mean_squared_error(y_test_actual, y_pred_actual)
rmse = np.sqrt(mse)
r2 = r2_score(y_test_actual, y_pred_actual)

print(f"✅ MSE: {mse:.6f}")
print(f"✅ RMSE: {rmse:.6f}")
print(f"✅ R2 Score: {r2:.4f}")

# =========================
# 13. Sample predictions
# =========================
print("\n🧠 Sample Predictions:")
for i in range(5):
    print(f"Actual: {y_test_actual.iloc[i]:.6f} | Predicted: {y_pred_actual[i]:.6f}")