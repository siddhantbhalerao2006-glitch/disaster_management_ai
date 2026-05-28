import os
os.environ["WANDB_API_KEY"] = "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"

import pandas as pd
import joblib
import wandb
import matplotlib.pyplot as plt

from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

# =========================
# INIT WANDB
# =========================
wandb.init(
    project="disaster-management-ai",
    config={
        "n_estimators": 500,
        "max_depth": 25,
        "test_size": 0.2,
        "random_state": 42
    }
)

config = wandb.config

print("🚀 Starting Disaster Model Training...")

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("cleaned_disaster_data.csv")

print("✅ Dataset Loaded")
print("📊 Shape:", df.shape)

# =========================
# CLEAN COLUMN NAMES
# =========================
df.columns = df.columns.str.strip().str.lower()

print("📂 Columns:")
print(df.columns.tolist())

# =========================
# HANDLE MISSING VALUES
# =========================
df['magnitude'] = df['magnitude'].fillna(df['magnitude'].mean())

# =========================
# LABEL ENCODING
# =========================
le_country = LabelEncoder()
le_disaster = LabelEncoder()

df['country_encoded'] = le_country.fit_transform(df['country'])
df['disaster_encoded'] = le_disaster.fit_transform(df['disaster_type'])

# =========================
# SAVE ENCODERS
# =========================
joblib.dump(le_country, "country_encoder.pkl")
joblib.dump(le_disaster, "disaster_label_encoder.pkl")

print("✅ Encoders Saved")

# =========================
# FEATURES & TARGET
# =========================
X = df[
    [
        'country_encoded',
        'year',
        'deaths',
        'affected',
        'magnitude',
        'severity'
    ]
]

y = df['disaster_encoded']

print("📊 Features:")
print(X.columns.tolist())

print("🎯 Target:")
print("disaster_encoded")

# =========================
# TRAIN TEST SPLIT
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=config.test_size,
    stratify=y,
    random_state=config.random_state
)

print("✅ Data Split Complete")

# =========================
# MODEL
# =========================
model = RandomForestClassifier(
    n_estimators=config.n_estimators,
    max_depth=config.max_depth,
    min_samples_split=5,
    min_samples_leaf=2,
    class_weight='balanced',
    random_state=config.random_state
)

print("🧠 Training Model...")

# =========================
# TRAIN MODEL
# =========================
model.fit(X_train, y_train)

print("✅ Model Training Complete")

# =========================
# SAVE MODEL
# =========================
joblib.dump(model, "disaster_model.pkl")

print("✅ Model Saved")

# =========================
# PREDICTIONS
# =========================
print("🔮 Predicting...")

y_pred = model.predict(X_test)

# =========================
# EVALUATION
# =========================
accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(
    y_test,
    y_pred,
    average='weighted',
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    average='weighted',
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    average='weighted',
    zero_division=0
)

# =========================
# PRINT RESULTS
# =========================
print("\n📈 MODEL EVALUATION RESULTS")
print("=" * 40)

print(f"✅ Accuracy  : {accuracy:.4f}")
print(f"✅ Precision : {precision:.4f}")
print(f"✅ Recall    : {recall:.4f}")
print(f"✅ F1 Score  : {f1:.4f}")

# =========================
# CLASSIFICATION REPORT
# =========================
print("\n📊 Classification Report:")
print("=" * 40)

target_names = le_disaster.classes_

print(
    classification_report(
        y_test,
        y_pred,
        target_names=target_names
    )
)

# =========================
# CONFUSION MATRIX
# =========================
cm = confusion_matrix(y_test, y_pred)

print("\n🧩 Confusion Matrix:")
print(cm)

# =========================
# FEATURE IMPORTANCE PLOT
# =========================
importance = model.feature_importances_
features = X.columns

plt.figure(figsize=(8, 5))

plt.bar(features, importance)

plt.title("Feature Importance")
plt.xlabel("Features")
plt.ylabel("Importance")

plt.tight_layout()

plt.savefig("feature_importance.png")

print("✅ Feature Importance Plot Saved")

# =========================
# LOG TO WANDB
# =========================
wandb.log({
    "accuracy": accuracy,
    "precision": precision,
    "recall": recall,
    "f1_score": f1
})

# =========================
# SAMPLE PREDICTIONS
# =========================
print("\n🧠 Sample Predictions:")
print("=" * 40)

for i in range(5):

    actual = le_disaster.inverse_transform([y_test.iloc[i]])[0]

    predicted = le_disaster.inverse_transform([y_pred[i]])[0]

    print(f"Actual: {actual} | Predicted: {predicted}")

print("\n🎉 Training & Evaluation Completed Successfully")