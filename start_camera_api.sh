#!/bin/bash

# Create a Python virtual environment
python -m venv venv

# Activate the virtual environment
# Note: This syntax is for bash and similar shells
source venv/bin/activate

# Install dependencies from requirements.txt
pip install -r requirements_camera_api.txt

# Navigate to the camera_api directory
cd camera_api

# Start the Uvicorn server for the FastAPI application
uvicorn main:app --host 0.0.0.0 --port 5000 --reload
