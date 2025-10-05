@echo off
echo =========================================
echo Food Delivery System - Quick Setup
echo =========================================
echo.

echo Installing Flask...
pip install flask
echo.

echo Creating database and populating sample data...
python populate_data.py
echo.

echo =========================================
echo Setup Complete!
echo =========================================
echo.
echo To start the application, run:
echo     python app.py
echo.
echo Then open your browser to:
echo     http://localhost:5000
echo.
pause
