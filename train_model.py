import pickle
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Load iris dataset
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model
with open('iris_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print(f"Model trained! Accuracy: {model.score(X_test, y_test):.2f}")
print("Model saved as iris_model.pkl")