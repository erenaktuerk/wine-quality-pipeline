"""
Model Evaluation Module.

This module loads the trained model from MLflow, evaluates it on a test set,
and generates evaluation metrics and plots.
"""

import pandas as pd
import mlflow
import mlflow.sklearn
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from src.utils import load_config
from sklearn.model_selection import train_test_split

def evaluate_model():
    # Load configuration
    config = load_config("configs/config.yaml")
    data_path = config["data"]["processed_path"]
    test_size = config["model"]["test_size"]
    random_state = config["model"]["random_state"]

    # Load processed data
    data = pd.read_csv(data_path)
    X = data.drop("quality", axis=1)
    y = data["quality"]

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    # Load latest model from MLflow (assumes only one run exists or adjust accordingly)
    client = mlflow.tracking.MlflowClient()
    runs = client.search_runs(experiment_ids=["0"], order_by=["start_time DESC"], max_results=1)
    if not runs:
        print("No MLflow runs found!")
        return
    run_id = runs[0].info.run_id
    model = mlflow.sklearn.load_model(f"runs:/{run_id}/model")

    # Make predictions and calculate evaluation metric
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    print(f"Mean Squared Error: {mse}")

    # Plot actual vs predicted
    plt.figure(figsize=(8, 6))
    plt.scatter(y_test, predictions, alpha=0.7)
    plt.xlabel("Actual Quality")
    plt.ylabel("Predicted Quality")
    plt.title("Actual vs Predicted Wine Quality")
    plt.savefig("data/processed/evaluation_plot.png")
    plt.close()

if __name__ == "__main__":
    evaluate_model()