from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np

app = FastAPI(
    title="Iris Prediction API",
    description="ML model serving with FastAPI",
    version="1.0.0"
)

# Load the trained model
with open('iris_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Define input schema
class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

# Define output schema
class PredictionOutput(BaseModel):
    species: str
    probability: float

# Map prediction to species name
SPECIES = ['setosa', 'versicolor', 'virginica']

@app.get("/")
def read_root():
    return {
        "message": "Iris Classification API",
        "status": "active",
        "model": "RandomForestClassifier",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "predict": "/predict"
        }
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }

@app.post("/predict", response_model=PredictionOutput)
def predict(input_data: IrisInput):
    # Prepare input
    features = np.array([[
        input_data.sepal_length,
        input_data.sepal_width,
        input_data.petal_length,
        input_data.petal_width
    ]])
    
    # Make prediction
    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0][prediction]
    
    return {
        "species": SPECIES[prediction],
        "probability": float(probability)
    }