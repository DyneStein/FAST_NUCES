@echo off
echo ========================================
echo       GitHub Daily Upload Script
echo ========================================
echo.

:: Automatically track empty folders by adding a dummy file to them.
echo Preparing folders (checking for empty ones)...
powershell -NoProfile -ExecutionPolicy Bypass -Command "Get-ChildItem -Directory -Recurse -Force | Where-Object { $_.FullName -notmatch '\\.git' -and @(Get-ChildItem -Path $_.FullName -Force).Count -eq 0 } | ForEach-Object { New-Item -ItemType File -Path (Join-Path $_.FullName '.gitkeep') -Force }"

:: Stage all changes (new files, modified files, deleted files, and empty folders)
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
