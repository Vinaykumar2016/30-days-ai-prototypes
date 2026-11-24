@echo off
setlocal enabledelayedexpansion
title Autonomous Google Maps Lead Extractor - Day 02
echo ===============================================================================
echo   AUTONOMOUS GOOGLE MAPS B2B LEAD EXTRACTOR [Day 02 / 30-Day AI Challenge]
echo   Engineered by Vinaykumar Mathad (@Vinaykumar2016 / @poweredbyvinay)
echo ===============================================================================
echo.

cd /d "%~dp0"

:: 1. Detect Python Command
set "PY_CMD="
py -3 --version >nul 2>&1 && set "PY_CMD=py -3"
if not defined PY_CMD (
    python --version >nul 2>&1 && set "PY_CMD=python"
)

if not defined PY_CMD (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.9+ from https://www.python.org/ or Microsoft Store.
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo [*] Detected Python environment: %PY_CMD%

:: 2. Install requirements using exact python interpreter (-m pip)
echo [*] Verifying and installing required packages (playwright, requests)...
%PY_CMD% -m pip install --quiet --upgrade playwright requests

:: 3. Install Chromium browser for Playwright using -m playwright (works even if playwright.exe is not in PATH)
echo [*] Verifying Playwright Chromium browser engine...
%PY_CMD% -m playwright install chromium

echo.
echo [*] Launching Autonomous Scraper Engine...
echo.
%PY_CMD% scraper.py

echo.
echo ===============================================================================
echo   EXTRACTION COMPLETED! Your leads have been exported to CSV.
echo ===============================================================================
pause
