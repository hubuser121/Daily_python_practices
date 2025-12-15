@echo off
REM Budget Tracker - Quick Start Script (Windows)

setlocal enabledelayedexpansion

echo.
echo ================================
echo Budget Tracker - Quick Start
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python 3.8+
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt -q
echo [OK] Dependencies installed
echo.

REM Run the application
echo Starting Budget Tracker...
echo.
echo Open your browser and go to: http://localhost:5000
echo.

python app.py

pause
