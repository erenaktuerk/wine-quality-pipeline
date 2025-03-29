import pandas as pd
from prefect import task, flow, get_run_logger
import yaml
from src.utils import load_config
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from prefect_dask import DaskTaskRunner

# Task to load raw data from CSV file
@task
def load_data(path: str) -> pd.DataFrame:
    """Load raw data from CSV file."""
    logger = get_run_logger()
    try:
        df = pd.read_csv(path, sep=";")
        logger.info("Data Loaded Successfully!")
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise
    return df

# Task to clean the data (handle missing values, type conversion, etc.)
@task
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the data (handle missing values, type conversion, etc.)."""
    logger = get_run_logger()
    logger.info("Cleaning data...")
    
    # Check for missing values
    if df.isnull().sum().any():
        logger.info("Handling missing values...")
        df = df.dropna()  # Drop rows with missing values (adjust as necessary)
    
    # Additional data cleaning steps can be added here (e.g., type conversions, outlier removal)
    
    logger.info("Data cleaned successfully!")
    return df

# Task to perform feature engineering on the dataset
@task
def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """Perform feature engineering on the data."""
    logger = get_run_logger()
    logger.info("Performing feature engineering...")
    
    # Example: Create a new feature 'acidity_ratio'
    if 'fixed acidity' in df.columns and 'volatile acidity' in df.columns:
        df['acidity_ratio'] = df['fixed acidity'] / (df['volatile acidity'] + 1e-5)
    
    # You can add more feature engineering steps as needed
    
    logger.info("Feature engineering complete!")
    return df

# Task to save the processed data to CSV
@task
def save_data(df: pd.DataFrame, path: str):
    """Save processed data to CSV file."""
    logger = get_run_logger()
    try:
        df.to_csv(path, index=False)
        logger.info(f"Data saved to {path}")
    except Exception as e:
        logger.error(f"Error saving data: {e}")
        raise

# Orchestrating the entire data processing pipeline using Prefect and DaskTaskRunner
@flow(name="Wine Quality Data Processing Pipeline", task_runner=DaskTaskRunner())  # Use DaskTaskRunner
def data_processing_pipeline():
    """Orchestrates the data processing steps."""
    logger = get_run_logger()
    logger.info("Starting data processing pipeline...")
    
    # Load the configuration file
    config = load_config("configs/config.yaml")
    raw_path = config["data"]["raw_path"]
    processed_path = config["data"]["processed_path"]
    
    # Execute tasks in sequence
    df = load_data(raw_path)
    df_clean = clean_data(df)
    df_features = feature_engineering(df_clean)
    save_data(df_features, processed_path)
    
    logger.info("Data processing pipeline completed successfully!")

if __name__ == "__main__":
    data_processing_pipeline()