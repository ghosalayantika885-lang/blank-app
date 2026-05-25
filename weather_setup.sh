#!/bin/bash

echo ""
echo "============================================"
echo "  Weather Dashboard - Setup"
echo "============================================"
echo ""

echo "Checking Python installation..."
python3 --version

if [ $? -ne 0 ]; then
    echo "ERROR: Python3 is not installed"
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
pip install -r weather_requirements.txt

echo ""
echo "============================================"
echo "  Setup Complete!"
echo "============================================"
echo ""
echo "To run the app:"
echo "  bash run_weather.sh"
echo ""
