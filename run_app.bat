@echo off
echo.
echo ============================================
echo  AI Multi-Module Platform
echo ============================================
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Starting Streamlit app...
echo.
echo Opening browser at http://localhost:8501
echo.

streamlit run app.py

pause
