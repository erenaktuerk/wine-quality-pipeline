Wine Quality Pipeline

Author: Eren Aktürk (GitHub)

Overview

The Wine Quality Pipeline is a fully automated MLOps pipeline that integrates modern tools and best practices to handle data processing, model training, evaluation, and deployment efficiently.

Key Features
	•	Automated Data Processing with Prefect for scalable workflow management.
	•	Model Training & Experiment Tracking with MLflow, ensuring full traceability of models.
	•	PostgreSQL Database Integration for structured storage of model results.
	•	Comprehensive Model Evaluation with advanced metrics and visualizations.
	•	FastAPI Deployment for real-time predictions.
	•	CI/CD with GitHub Actions for continuous integration and deployment.
	•	Docker Containerization for scalability and portability.

This project provides a complete MLOps demonstration, covering the entire lifecycle from raw data processing to automated model versioning and deployment.

⸻

Project Structure

wine_quality_pipeline/
├── ci_cd/
│   └── github_actions.yml      # GitHub Actions workflow for CI/CD automation
├── configs/
│   └── config.yaml             # Centralized configuration file
├── data/
│   ├── raw/                    # Raw Wine Quality dataset
│   └── processed/              # Processed dataset after Prefect pipeline execution
├── docker/
│   └── Dockerfile              # Containerization setup
├── notebooks/                  # Jupyter notebooks for prototyping (optional)
├── src/
│   ├── _init_.py             # Package initializer
│   ├── data_processing.py      # Prefect-powered data transformation pipeline
│   ├── model_training.py       # Model training pipeline with MLflow integration
│   ├── model_evaluation.py     # Automated evaluation with metrics and plots
│   ├── deployment.py           # FastAPI service for inference
│   └── utils.py                # Helper functions
├── tests/
│   └── test_pipeline.py        # Unit and integration tests
├── .gitignore                  # Ignore unnecessary files
├── README.md                   # Project documentation
└── requirements.txt            # Python dependencies



⸻

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
	•	Place the raw dataset (winequality.csv) in the data/raw/ folder.
	•	Run the Prefect-powered data pipeline:

python -m src.data_preprocessing

5. Model Training and Experiment Logging
	•	Train the model and log experiments with MLflow:

python -m src.train

6. Model Evaluation and Performance Analysis
	•	Compute metrics such as MSE, RMSE, MAE, R² and generate visualizations using evaluation.py:

python -m src.evaluation

7. FastAPI Deployment
	•	Deploy the trained model as a REST API:

uvicorn src.deployment:app --host 0.0.0.0 --port 8000

	•	Access the API at http://localhost:8000

8. Run Tests
	•	Validate the pipeline using unit tests:

python -m unittest discover tests

9. Docker Containerization
	•	Build the Docker image:

docker build -t wine_quality_pipeline:latest -f docker/Dockerfile .

	•	Run the containerized API:

docker run -p 8000:8000 wine_quality_pipeline:latest



⸻

CI/CD Pipeline

The GitHub Actions workflow (ci_cd/github_actions.yml) ensures:
	•	Automated testing on every commit
	•	Docker image build for deployment
	•	Optional automatic deployment to cloud environments

⸻

Recent Enhancements and Achievements

PostgreSQL Database Integration
	•	Model results, including accuracy and loss, are stored in a PostgreSQL database for structured tracking
	•	Uses psycopg2 for database connectivity

MLflow Experiment Tracking
	•	Every model run is automatically logged in MLflow for better experiment management

Prefect Workflow Orchestration
	•	Prefect is used for fault-tolerant and scalable data processing, ensuring robust pipeline execution

Advanced Error Handling and Debugging
	•	Detailed logging and structured error handling make debugging more efficient

⸻

Resources and References
	•	Prefect Documentation
	•	MLflow Documentation
	•	FastAPI Documentation
	•	Docker Documentation
	•	GitHub Actions

⸻

License

This project is licensed under the MIT License. See the LICENSE file for details.