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
def load_data(file_path: str) -> pd.DataFrame:
    """
    Loads data from a CSV file, ensuring proper column separation, and returns the DataFrame.
    
    Args:
        file_path (str): The path to the CSV file to be loaded.
    
    Returns:
        DataFrame: The processed DataFrame.
    """
    logger = get_run_logger()
    try:
        # Attempt to read the CSV with a semicolon as separator (common for the Wine Quality dataset)
        df = pd.read_csv(file_path, sep=";")
        
        # If only one column is present, the file might be comma-separated
        if len(df.columns) == 1:
            header_line = df.columns[0]
            if "," in header_line:
                logger.info("Detected comma-separated header. Re-reading CSV with comma as separator.")
                df = pd.read_csv(file_path, sep=",")
                
        logger.info("Data loaded successfully!")
        return df
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise

# Task to clean the data (handle missing values, type conversion, etc.)
@task
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the data by handling missing values and performing necessary type conversions.
    
    Args:
        df (DataFrame): The input DataFrame.
        
    Returns:
        DataFrame: The cleaned DataFrame.
    """
    logger = get_run_logger()
    logger.info("Cleaning data...")
    
    if df is None:
        raise ValueError("DataFrame is None. Data loading failed.")
    
    # Check for missing values and drop rows if any are found
    if df.isnull().sum().any():
        logger.info("Handling missing values by dropping rows.")
        df = df.dropna().reset_index(drop=True)
    
    logger.info("Data cleaned successfully!")
    return df

# Task to perform feature engineering on the dataset
@task
def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """
    Performs feature engineering on the data, such as creating new features.
    
    Args:
        df (DataFrame): The cleaned DataFrame.
        
    Returns:
        DataFrame: The DataFrame with additional features.
    """
    logger = get_run_logger()
    logger.info("Performing feature engineering...")
    
    # Example: Create a new feature 'acidity_ratio' if the required columns are present
    if 'fixed acidity' in df.columns and 'volatile acidity' in df.columns:
        df['acidity_ratio'] = df['fixed acidity'] / (df['volatile acidity'] + 1e-5)
    
    logger.info("Feature engineering complete!")
    return df

# Task to save the processed data to CSV
@task
def save_data(df: pd.DataFrame, path: str):
    """
    Saves the processed data to a CSV file.
    
    Args:
        df (DataFrame): The DataFrame to be saved.
        path (str): The path where the CSV file will be stored.
    """
    logger = get_run_logger()
    try:
        df.to_csv(path, index=False)
        logger.info(f"Data saved to {path}")
    except Exception as e:
        logger.error(f"Error saving data: {e}")
        raise

# Orchestrating the entire data processing pipeline using Prefect and DaskTaskRunner
@flow(name="Wine Quality Data Processing Pipeline", task_runner=DaskTaskRunner())
def data_processing_pipeline():
    """
    Orchestrates the data processing steps.
    """
    logger = get_run_logger()
    logger.info("Starting data processing pipeline...")
    
    # Load configuration from YAML file
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