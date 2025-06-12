#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Run the backend server in the background
echo "Starting backend server..."
uvicorn backend.main:app --host 0.0.0.0 --port 8000 &

# Wait for the backend to start
sleep 10

# Run the frontend application
echo "Starting frontend application..."
streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0