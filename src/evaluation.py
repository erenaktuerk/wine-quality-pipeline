"""
Model Evaluation Module.

This module loads the trained model from MLflow, evaluates it on a test set,
and generates evaluation metrics and plots.
"""

import os
import pandas as pd
import mlflow
import mlflow.sklearn
import matplotlib
matplotlib.use("Agg")  # Set Matplotlib to non-GUI backend to avoid Tkinter issues
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from src.utils import load_config


def evaluate_model(model, X_test, y_test):
    """Evaluates the model, generates plots, and logs metrics to MLflow."""
    
    # Ensure to end any previous active run before starting a new one
    if mlflow.active_run():
        mlflow.end_run()

    # Start a new MLflow run
    with mlflow.start_run():
        # Make predictions
        predictions = model.predict(X_test)

        # Calculate evaluation metrics
        mse = mean_squared_error(y_test, predictions)
        rmse = mean_squared_error(y_test, predictions)**0.5  # Wurzel des MSE
        mae = mean_absolute_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)

        print(f"Evaluation Results:\nMSE: {mse}\nRMSE: {rmse}\nMAE: {mae}\nR²: {r2}")

        # Log metrics to MLflow
        mlflow.log_metric("MSE", mse)
        mlflow.log_metric("RMSE", rmse)
        mlflow.log_metric("MAE", mae)
        mlflow.log_metric("R²", r2)

        # Ensure output directory exists
        output_dir = "data/processed/evaluation_plots"
        os.makedirs(output_dir, exist_ok=True)

        # Plot 1: Actual vs Predicted
        plt.figure(figsize=(8, 6))
        plt.scatter(y_test, predictions, alpha=0.7)
        plt.xlabel("Actual Quality")
        plt.ylabel("Predicted Quality")
        plt.title("Actual vs Predicted Wine Quality")
        plot_path_1 = os.path.join(output_dir, "actual_vs_predicted.png")
        plt.savefig(plot_path_1)
        plt.close()
        mlflow.log_artifact(plot_path_1)

        # Plot 2: Residual Plot
        residuals = y_test - predictions
        plt.figure(figsize=(8, 6))
        sns.histplot(residuals, bins=20, kde=True)
        plt.xlabel("Residuals")
        plt.ylabel("Frequency")
        plt.title("Residual Distribution")
        plot_path_2 = os.path.join(output_dir, "residual_distribution.png")
        plt.savefig(plot_path_2)
        plt.close()
        mlflow.log_artifact(plot_path_2)

        # Plot 3: Feature Importance (only if model supports it)
        if hasattr(model, "feature_importances_"):
            plt.figure(figsize=(10, 6))
            feature_importance = pd.Series(model.feature_importances_, index=X_test.columns)
            feature_importance.sort_values(ascending=False).plot(kind="bar")
            plt.xlabel("Feature")
            plt.ylabel("Importance")
            plt.title("Feature Importance")
            plot_path_3 = os.path.join(output_dir, "feature_importance.png")
            plt.savefig(plot_path_3)
            plt.close()
            mlflow.log_artifact(plot_path_3)

        print("Evaluation complete. Results and plots stored in MLflow.")


if __name__ == "__main__":
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

    # Load latest model from MLflow
    client = mlflow.tracking.MlflowClient()
    runs = client.search_runs(experiment_ids=["0"], order_by=["start_time DESC"], max_results=1)

    if not runs:
        print("No MLflow runs found!")
    else:
        run_id = runs[0].info.run_id
        model = mlflow.sklearn.load_model(f"runs:/{run_id}/model")
        evaluate_model(model, X_test, y_test)