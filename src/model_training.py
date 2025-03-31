import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from src.utils import load_config
from prefect import flow, task
from src.database import Database  # Using the Database class

# Function to store model results in the database
def store_model_results_to_db(model_name: str, train_score: float, test_score: float):
    try:
        # Initialize the database connection
        db = Database(dbname='wine_quality', user='postgres', password='Bubble69$')
        db.connect()
        
        # Ensure the table exists
        db.create_table_if_not_exists()

        # SQL query to store the results in the 'model_results' table
        insert_query = """
        INSERT INTO model_results (accuracy, loss, model_name)
        VALUES (%s, %s, %s);
        """
        params = (train_score, test_score, model_name)
        print(f"Executing query: {insert_query} with parameters: {params}")
        db.execute_query(insert_query, params)

        # Optional: Fetch results from DB to ensure they were stored
        fetched_results = db.fetch_all("SELECT * FROM model_results;")
        print("Stored results:", fetched_results)

        db.close()

    except Exception as e:
        print(f"Error storing results to DB: {e}")

@task
def load_processed_data(path: str) -> pd.DataFrame:
    """Load processed data from a CSV file."""
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
        print(data.columns) #debugging
        X = data.drop("quality", axis=1)
        y = data["quality"]

        # Split data into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )

        # Train RandomForest model
        model = RandomForestRegressor(n_estimators=n_estimators, random_state=random_state)
        model.fit(X_train, y_train)

        # Log parameters, metrics, and model in MLflow
        mlflow.log_param("n_estimators", n_estimators)
        train_score = model.score(X_train, y_train)
        test_score = model.score(X_test, y_test)
        mlflow.log_metric("train_score", train_score)
        mlflow.log_metric("test_score", test_score)
        mlflow.sklearn.log_model(model, "model")

        print(f"Training complete. Train score: {train_score}, Test score: {test_score}")

        # Save results to database after training
        store_model_results_to_db("RandomForestModel", train_score, test_score)

if __name__ == "__main__":
    train_model_pipeline()