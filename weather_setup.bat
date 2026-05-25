@echo off
echo.
echo ============================================
echo  Weather Dashboard - Setup
echo ============================================
echo.
echo Checking Python installation...
python --version

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python is not installed
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
pip install -r weather_requirements.txt

echo.
echo ============================================
echo  Setup Complete!
echo ============================================
echo.
echo To run the app:
echo   run_weather.bat
echo.
pause
