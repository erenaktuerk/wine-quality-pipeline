"""
Utility functions for the wine_quality_pipeline.
"""

import yaml

def load_config(path: str) -> dict:
    """
    Load YAML configuration file.
    
    Parameters:
        path (str): Path to the config file.
    
    Returns:
        dict: Configuration parameters.
    """
    with open(path, "r") as file:
        config = yaml.safe_load(file)
    return config