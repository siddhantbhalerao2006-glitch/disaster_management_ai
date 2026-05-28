from sklearn.metrics import accuracy_score

# Example data (you MUST have this)
y_true = [1, 0, 1, 1]
y_pred = [1, 0, 0, 1]

accuracy = accuracy_score(y_true, y_pred)

print("Accuracy:", accuracy)