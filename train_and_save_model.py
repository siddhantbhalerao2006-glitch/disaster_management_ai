import os
os.environ["WANDB_API_KEY"] = "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"

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import wandb

# =========================
# INIT WANDB
# =========================
wandb.init(
    project="disaster-management-ai",
    config={
        "n_estimators": 100,
        "max_depth": 10,
        "test_size": 0.2
    }
)

config = wandb.config
# =========================
# LOAD DATA
# =========================
df = pd.read_csv("cleaned_disaster_data.csv")

# Check data distribution
print(df['disaster_type'].value_counts())

# Fill missing values
df['magnitude'] = df['magnitude'].fillna(df['magnitude'].mean())

# Encode
le_country = LabelEncoder()
le_disaster = LabelEncoder()

df['country_encoded'] = le_country.fit_transform(df['country'])
df['disaster_encoded'] = le_disaster.fit_transform(df['disaster_type'])

# =========================
# FEATURES
# =========================
X = df[['country_encoded', 'year', 'deaths', 'affected', 'magnitude', 'severity']]
y = df['disaster_encoded']

# =========================
# TRAIN TEST SPLIT (FIXED)
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=config.test_size,
    stratify=y,          # 🔥 important
    random_state=42
)

# =========================
# MODEL (FIXED)
# =========================
model = RandomForestClassifier(
    n_estimators=500,
    max_depth=25,
    min_samples_split=5,
    min_samples_leaf=2,
    class_weight='balanced',
    random_state=42
)




model.fit(X_train, y_train)

# =========================
# EVALUATION (FIXED)
# =========================
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)

# =========================
# LOG TO WANDB
# =========================
wandb.log({
    "accuracy": accuracy,
    "precision": precision,
    "recall": recall,
    "f1_score": f1,
    "n_estimators": config.n_estimators,
    "max_depth": config.max_depth
})

print("✅ Done")
print(f"Accuracy: {accuracy}")