@echo off
echo.
echo ============================================
echo  AI Multi-Module Platform - Setup
echo ============================================
echo.
echo Checking Python installation...
python --version

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo.
echo Creating virtual environment...
python -m venv venv

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ============================================
echo  ✅ Setup Complete!
echo ============================================
echo.
echo To run the app, use:
echo   run_app.bat
echo.
echo Or manually run:
echo   streamlit run app.py
echo.
pause
