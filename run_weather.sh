#!/bin/bash

echo ""
echo "============================================"
echo "  Weather Dashboard"
echo "============================================"
echo ""

echo "Activating virtual environment..."
source venv/bin/activate

echo ""
echo "Starting Weather Dashboard..."
echo ""
echo "Opening browser at http://localhost:8501"
echo ""

streamlit run weather_app.py
