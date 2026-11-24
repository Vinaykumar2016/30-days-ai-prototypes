@echo off
title Autonomous B2B Cold Outreach Agent - Day 03
echo ===============================================================================
echo   AUTONOMOUS B2B COLD OUTREACH & CLIENT ACQUISITION AGENT [Day 03 / 30]
echo   Engineered by Vinaykumar Mathad (@Vinaykumar2016 / @poweredbyvinay)
echo ===============================================================================
echo.

cd /d "%~dp0"

echo [*] Running Autonomous Outreach Agent...
python pitch_agent.py

echo.
echo ===============================================================================
echo   CAMPAIGN READY! Check outreach_campaign_ready.csv for your 1-click pitches.
echo ===============================================================================
pause
