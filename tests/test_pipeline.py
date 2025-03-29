"""
Unit and integration tests for the wine_quality_pipeline.
"""

import unittest
import pandas as pd
from src.data_preprocessing import clean_data, feature_engineering
from src.utils import load_config

class TestDataProcessing(unittest.TestCase):

    def setUp(self):
        # Create a dummy dataframe similar to wine quality data
        self.df = pd.DataFrame({
            "fixed acidity": [7.4, 7.8],
            "volatile acidity": [0.70, 0.88],
            "citric acid": [0.00, 0.00],
            "residual sugar": [1.9, 2.6],
            "chlorides": [0.076, 0.098],
            "free sulfur_dioxide": [11, 25],
            "total sulfur_dioxide": [34, 67],
            "density": [0.9978, 0.9968],
            "pH": [3.51, 3.20],
            "sulphates": [0.56, 0.68],
            "alcohol": [9.4, 9.8],
            "quality": [5, 5]
        })

    def test_clean_data(self):
        # Test clean_data simply returns a DataFrame of the same shape
        from src.data_preprocessing import clean_data
        cleaned = clean_data.run(self.df)
        self.assertEqual(cleaned.shape, self.df.shape)

    def test_feature_engineering(self):
        # Test feature engineering adds the 'acidity_ratio' column
        from src.data_preprocessing import feature_engineering
        df_fe = feature_engineering.run(self.df)
        self.assertIn("acidity_ratio", df_fe.columns)

class TestConfigLoader(unittest.TestCase):
    def test_load_config(self):
        # Assuming the config file exists in the correct location
        config = load_config("configs/config.yaml")
        self.assertIn("data", config)
        self.assertIn("model", config)

if __name__ == "__main__":
    unittest.main()