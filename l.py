from sklearn.model_selection import cross_val_score

scores = cross_val_score(model, X, y, cv=5)
print("Accuracy per fold:", scores)
print("Mean accuracy:", scores.mean())