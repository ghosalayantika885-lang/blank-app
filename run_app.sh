#!/bin/bash

echo ""
echo "============================================"
echo "  AI Multi-Module Platform"
echo "============================================"
echo ""

echo "Activating virtual environment..."
source venv/bin/activate

echo ""
echo "Starting Streamlit app..."
echo ""
echo "Opening browser at http://localhost:8501"
echo ""

streamlit run app.py
