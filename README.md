# Wine Quality Pipeline

Author: Eren Aktürk (GitHub: erenaktuerk)

## Overview

The Wine Quality Pipeline project demonstrates an end-to-end automated ML pipeline covering:
- Data processing using Prefect.
- Model training and experiment tracking with MLflow.
- Model evaluation with metrics and plots.
- Deployment of a prediction API using FastAPI.
- Containerization using Docker.
- CI/CD automation via GitHub Actions.

This project serves as a comprehensive demonstration of the ML lifecycle, including continuous integration and deployment.

## Project Structure

wine_quality_pipeline/
├── ci_cd/
│   └── github_actions.yml          # GitHub Actions…
Hier ist die aktualisierte README.md, die alle Anpassungen und Änderungen, die du vorgenommen hast, enthält:

⸻

Wine Quality Pipeline

Author: Eren Aktürk (GitHub: erenaktuerk)

Overview

The Wine Quality Pipeline project demonstrates an end-to-end automated ML pipeline covering:
	•	Data processing using Prefect.
	•	Model training and experiment tracking with MLflow.
	•	Model evaluation with metrics and plots.
	•	Deployment of a prediction API using FastAPI.
	•	Containerization using Docker.
	•	CI/CD automation via GitHub Actions.

This project serves as a comprehensive demonstration of the ML lifecycle, including continuous integration and deployment.

Project Structure

wine_quality_pipeline/
├── ci_cd/
│   └── github_actions.yml          # GitHub Actions workflow for CI/CD
├── configs/
│   └── config.yaml                 # Configuration file with paths and parameters
├── data/
│   ├── raw/                        # Raw Wine Quality dataset (CSV)
│   └── processed/                  # Processed data output from the pipeline
├── docker/
│   └── Dockerfile                  # Dockerfile to containerize the application
├── licenses/
│   └── LICENSE                     # MIT License
├── notebooks/                      # Jupyter notebooks for prototyping (optional)
├── scripts/                        # Utility scripts (if needed)
├── src/
│   ├── _init_.py                 # Package initializer
│   ├── data_processing.py          # Data processing pipeline with Prefect
│   ├── model_training.py           # Model training & MLflow integration
│   ├── model_evaluation.py         # Model evaluation and plotting
│   ├── deployment.py               # REST API deployment using FastAPI
│   └── utils.py                    # Utility functions (e.g., config loader)
├── tests/
│   └── test_pipeline.py            # Unit and integration tests for the pipeline
├── .gitignore                      # Git ignore file
├── README.md                       # Project documentation
└── requirements.txt                # Python dependencies

Setup Instructions

1. Clone the Repository

git clone https://github.com/erenaktuerk/wine_quality_pipeline.git
cd wine_quality_pipeline

2. Create and Activate a Virtual Environment

python -m venv venv
# Activate on Windows:
venv\Scripts\activate

3. Install Dependencies

pip install --upgrade pip
pip install -r requirements.txt

4. Data Processing
	•	Place the raw dataset (winequality.csv) into the data/raw/ folder.
	•	Run the data processing pipeline:

python src/data_processing.py

5. Model Training
	•	Ensure that the processed data exists in data/processed/.
	•	Train the model and log experiments with MLflow:

python src/model_training.py

6. Model Evaluation
	•	Evaluate the trained model:

python src/model_evaluation.py

7. Deployment
	•	Run the FastAPI server to serve predictions:

uvicorn src.deployment:app --host 0.0.0.0 --port 8000

	•	The API endpoint will be accessible at http://localhost:8000.

8. Testing
	•	Run unit and integration tests:

python -m unittest discover tests

9. Docker
	•	Build the Docker image:

docker build -t wine_quality_pipeline:latest -f docker/Dockerfile .

	•	Run the Docker container:

docker run -p 8000:8000 wine_quality_pipeline:latest

CI/CD

The GitHub Actions workflow defined in ci_cd/github_actions.yml will:
	•	Run tests on every push.
	•	Build the Docker image upon successful tests.
	•	(Optionally) Deploy the application.

Changes and Updates
	•	Database Integration: Added functionality to store model results in a PostgreSQL database. The database connection uses psycopg2, and model results (e.g., accuracy, loss, model name) are stored in the model_results table.
	•	MLflow Experiment Logging: Incorporated MLflow for experiment tracking and logging, allowing monitoring of model performance.
	•	Prefect for Data Processing: Prefect is used to orchestrate the data processing pipeline, including tasks like loading and transforming data.
	•	Error Handling and Debugging: Extensive error handling and debug outputs were added to ensure smooth execution and easier troubleshooting during database operations.

Additional Information and Resources
	•	Prefect Documentation: https://docs.prefect.io/
	•	MLflow Documentation: https://mlflow.org/docs/latest/index.html
	•	FastAPI Documentation: https://fastapi.tiangolo.com/
	•	Docker Documentation: https://docs.docker.com/
	•	GitHub Actions Documentation: https://docs.github.com/en/actions

License

This project is licensed under the MIT License. See the LICENSE file for details.

⸻