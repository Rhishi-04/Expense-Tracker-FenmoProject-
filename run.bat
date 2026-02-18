@echo off
REM Script to run both FastAPI and Streamlit on Windows

echo Starting Personal Finance Tracker...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting FastAPI backend on http://localhost:8000
echo Starting Streamlit frontend on http://localhost:8501
echo.
echo Press Ctrl+C to stop both servers
echo.

REM Start FastAPI in background
start "FastAPI" cmd /k "uvicorn app:app --reload --port 8000"

REM Wait a moment for FastAPI to start
timeout /t 2 /nobreak >nul

REM Start Streamlit
streamlit run streamlit_app.py

