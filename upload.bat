@echo off
echo ========================================
echo       GitHub Daily Upload Script
echo ========================================
echo.

:: Stage all changes (new, modified, and deleted files)
git add .

:: Prompt for a commit message (optional)
set /p commit_msg="Enter a commit message (or press Enter for 'Daily Auto-Upload'): "

:: If no message is provided, use a default one
if "%commit_msg%"=="" set commit_msg=Daily Auto-Upload

:: Commit the changes
git commit -m "%commit_msg%"

:: Push to the main branch
echo.
echo Pushing changes to GitHub...
git push origin main

echo.
echo ========================================
echo  All changes have been successfully uploaded!
echo ========================================
pause
