@echo off
echo ========================================================
echo  P唯H TO GITHUB: 30-Days AI Prototypes (@Vinaykumar2016)
echo ========================================================
cd /d "c:\Users\s\OneDrive\Desktop\Antigravity _Projects\Content creator\30_Days_Challenge"

git add .
set /p commit_msg="Enter commit message (or press enter for default): "
if "%commit_msg%"=="" set commit_msg="Daily AI Challenge Update"

git commit -m "%commit_msg%"
git push -u origin main

echo.
echo ========================================================
echo  SUCCESS: Code pushed to https://github.com/Vinaykumar2016/30-days-ai-prototypes
echo ========================================================
pause
