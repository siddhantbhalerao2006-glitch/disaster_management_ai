# =========================
# IMPORTS
# =========================
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.ensemble import RandomForestClassifier

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("cleaned_disaster_data.csv")

# =========================
# DATA CLEANING
# =========================
# Fill missing magnitude with mean
df['magnitude'] = df['magnitude'].fillna(df['magnitude'].mean())

# Encode categorical columns
le_country = LabelEncoder()
le_disaster = LabelEncoder()

df['country_encoded'] = le_country.fit_transform(df['country'])
df['disaster_encoded'] = le_disaster.fit_transform(df['disaster_type'])

# =========================
# FEATURES & TARGET
# =========================
X = df[['country_encoded', 'year', 'deaths', 'affected', 'magnitude']]
y = df['disaster_encoded']

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model (NEW model based on this dataset)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# =========================
# 1. CONFUSION MATRIX
# =========================
y_pred = model.predict(X_test)

cm = confusion_matrix(y_test, y_pred)

plt.figure()
sns.heatmap(cm, annot=True, fmt='d')
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")

plt.savefig("confusion_matrix.png")
plt.close()

print("✅ confusion_matrix.png saved")


# =========================
# 2. FEATURE IMPORTANCE
# =========================
features = ['country', 'year', 'deaths', 'affected', 'magnitude']
importance = model.feature_importances_

plt.figure()
plt.bar(features, importance)
plt.title("Feature Importance")
plt.xlabel("Features")
plt.ylabel("Importance")
plt.xticks(rotation=45)

plt.savefig("feature_importance.png")
plt.close()

print("✅ feature_importance.png saved")


# =========================
# 3. ACCURACY vs TREES
# =========================
trees = [10, 50, 100, 150, 200]
accuracies = []

for n in trees:
    temp_model = RandomForestClassifier(n_estimators=n, random_state=42)
    temp_model.fit(X_train, y_train)
    y_temp_pred = temp_model.predict(X_test)
    acc = accuracy_score(y_test, y_temp_pred)
    accuracies.append(acc)

plt.figure()
plt.plot(trees, accuracies, marker='o')
plt.title("Accuracy vs Number of Trees")
plt.xlabel("Number of Trees")
plt.ylabel("Accuracy")

plt.savefig("accuracy_vs_trees.png")
plt.close()

print("✅ accuracy_vs_trees.png saved")