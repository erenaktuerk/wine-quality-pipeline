"""
Data Processing Pipeline using Prefect for the Wine Quality dataset.

This module loads the raw dataset, performs cleaning and feature engineering,
and saves the processed dataset to a specified location.
"""

import pandas as pd
from prefect import task, flow
import yaml
from src.utils import load_config

@task
def load_data(path: str) -> pd.DataFrame:
    """Load raw data from CSV file."""
    df = pd.read_csv(path, sep=";")
    return df

@task
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the data (handle missing values, type conversion, etc.)."""
    # For demonstration, assume no missing values.
    # You can add cleaning steps as needed.
    return df

@task
def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """Perform feature engineering on the data."""
    # Example: Create a new feature 'acidity_ratio'
    if 'fixed acidity' in df.columns and 'volatile acidity' in df.columns:
        df['acidity_ratio'] = df['fixed acidity'] / (df['volatile acidity'] + 1e-5)
    return df

@task
def save_data(df: pd.DataFrame, path: str):
    """Save processed data to CSV file."""
    df.to_csv(path, index=False)

@flow(name="Data Processing Pipeline")
def data_processing_pipeline():
    """Orchestrates the data processing steps."""
    config = load_config("configs/config.yaml")
    raw_path = config["data"]["raw_path"]
    processed_path = config["data"]["processed_path"]

    df = load_data(raw_path)
    df_clean = clean_data(df)
    df_features = feature_engineering(df_clean)
    save_data(df_features, processed_path)

if __name__ == "__main__":
    data_processing_pipeline()