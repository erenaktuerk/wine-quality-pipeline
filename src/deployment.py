"""
Deployment Module using FastAPI.

This module creates a REST API to serve predictions from the trained model.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow.sklearn
import pandas as pd
from src.utils import load_config

# Initialize FastAPI app
app = FastAPI(title="Wine Quality Prediction API")

# Define request model
class WineData(BaseModel):
    fixed_acidity: float
    volatile_acidity: float
    citric_acid: float
    residual_sugar: float
    chlorides: float
    free_sulfur_dioxide: float
    total_sulfur_dioxide: float
    density: float
    pH: float
    sulphates: float
    alcohol: float

# Load configuration and model at startup
config = load_config("configs/config.yaml")
mlflow.set_tracking_uri(config["mlflow"]["tracking_uri"])
# For simplicity, load the latest model from MLflow
import mlflow
client = mlflow.tracking.MlflowClient()
runs = client.search_runs(experiment_ids=["0"], order_by=["start_time DESC"], max_results=1)
if runs:
    run_id = runs[0].info.run_id
    model = mlflow.sklearn.load_model(f"runs:/{run_id}/model")
else:
    model = None

@app.get("/")
def read_root():
    return {"message": "Welcome to the Wine Quality Prediction API!"}

@app.post("/predict")
def predict(wine_data: WineData):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not available")
    
    # Convert input data to DataFrame
    data = pd.DataFrame([wine_data.dict()])
    # Ensure column names match those used in training (adjust if needed)
    prediction = model.predict(data)[0]
    return {"predicted_quality": prediction}