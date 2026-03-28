from sklearn.ensemble import RandomForestClassifier
import joblib

# Example training (you must have your X_train and y_train ready)
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)  # X_train and y_train must be defined

# Now save the model
joblib.dump(rf_model, 'best_disaster_model.pkl')
