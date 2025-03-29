# Use official Python runtime as a parent image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Expose the deployment port (as defined in configs/config.yaml)
EXPOSE 8000

# Command to run the FastAPI deployment server
CMD ["uvicorn", "src.deployment:app", "--host", "0.0.0.0", "--port", "8000"]