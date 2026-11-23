@echo off
title Autonomous Google Maps Lead Extractor - Day 02
echo ===============================================================================
echo   AUTONOMOUS GOOGLE MAPS B2B LEAD EXTRACTOR [Day 02 / 30-Day AI Challenge]
echo   Engineered by Vinaykumar Mathad (@Vinaykumar2016 / @poweredbyvinay)
echo ===============================================================================
echo.

cd /d "%~dp0"

echo [*] Verifying Python environment...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.9+ from https://www.python.org/
    pause
    exit /b
)

echo [*] Checking dependencies...
python -c "import playwright" >nul 2>&1
if %errorlevel% neq 0 (
    echo [*] Installing Playwright automation engine...
    pip install playwright
    playwright install chromium
)

echo.
echo [*] Launching Autonomous Scraper Engine...
echo.
python scraper.py

echo.
echo ===============================================================================
echo   EXTRACTION COMPLETED! Your leads have been exported to CSV.
echo ===============================================================================
pause
