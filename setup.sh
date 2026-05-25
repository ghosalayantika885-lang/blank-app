#!/bin/bash

echo ""
echo "============================================"
echo "  AI Multi-Module Platform - Setup"
echo "============================================"
echo ""

echo "Checking Python installation..."
python3 --version

if [ $? -ne 0 ]; then
    echo "ERROR: Python3 is not installed"
    echo "Please install Python from https://www.python.org/"
    exit 1
fi

echo ""
echo "Creating virtual environment..."
python3 -m venv venv

echo ""
echo "Activating virtual environment..."
source venv/bin/activate

echo ""
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "============================================"
echo "  ✅ Setup Complete!"
echo "============================================"
echo ""
echo "To run the app, use:"
echo "  bash run_app.sh"
echo ""
echo "Or manually run:"
echo "  streamlit run app.py"
echo ""
