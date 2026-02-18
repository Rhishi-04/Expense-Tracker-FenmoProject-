#!/bin/bash

# Script to run both FastAPI and Streamlit

echo "Starting Personal Finance Tracker..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Starting FastAPI backend on http://localhost:8000"
echo "Starting Streamlit frontend on http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Start FastAPI in background
uvicorn app:app --reload --port 8000 &
FASTAPI_PID=$!

# Wait a moment for FastAPI to start
sleep 2

# Start Streamlit
streamlit run streamlit_app.py

# Kill FastAPI when Streamlit stops
kill $FASTAPI_PID 2>/dev/null

