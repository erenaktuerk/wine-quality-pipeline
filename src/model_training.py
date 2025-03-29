"""
Model Training Module using MLflow for tracking.

This module loads the processed data, splits it into training and test sets,
trains a model, and logs the experiment details and model artifact to MLflow.
"""

import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from src.utils import load_config
from prefect import flow, task

@task
def load_processed_data(path: str) -> pd.DataFrame:
    """Load processed data from CSV file."""
    return pd.read_csv(path)

@flow(name="Model Training Pipeline")
def train_model_pipeline():
    """End-to-end model training pipeline."""
    # Load configuration
    config = load_config("configs/config.yaml")
    data_path = config["data"]["processed_path"]
    test_size = config["model"]["test_size"]
    random_state = config["model"]["random_state"]
    n_estimators = config["model"]["n_estimators"]

    # Start MLflow run
    mlflow.set_tracking_uri(config["mlflow"]["tracking_uri"])
    with mlflow.start_run():
        # Load data
        data = load_processed_data(data_path)
        
        # Assuming 'quality' is the target variable
        X = data.drop("quality", axis=1)
        y = data["quality"]

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )

        # Train model
        model = RandomForestRegressor(n_estimators=n_estimators, random_state=random_state)
        model.fit(X_train, y_train)

        # Log parameters, metrics and model
        mlflow.log_param("n_estimators", n_estimators)
        train_score = model.score(X_train, y_train)
        test_score = model.score(X_test, y_test)
        mlflow.log_metric("train_score", train_score)
        mlflow.log_metric("test_score", test_score)
        mlflow.sklearn.log_model(model, "model")

        print(f"Training complete. Train score: {train_score}, Test score: {test_score}")

if __name__ == "__main__":
    train_model_pipeline()