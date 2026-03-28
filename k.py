import pickle

# Assume you already trained your model
# model = trained ML model
# label_encoder = fitted label encoder

# Save model
with open("disaster_model.pkl", "wb") as f:
    pickle.dump(model, f)

# Save label encoder
with open("disaster_label_encoder.pkl", "wb") as f:
    pickle.dump(label_encoder, f)

print("✅ Model and encoder saved successfully!")