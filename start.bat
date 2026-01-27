@echo off
title AI Studio - Start
color 0A
echo ============================================================
echo                    AI Studio - Start
echo ============================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.11+ and try again.
    pause
    exit /b 1
)

:: Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed or not in PATH.
    echo Please install Node.js 18+ and try again.
    pause
    exit /b 1
)

:: Navigate to backend and try to start
cd backend
echo Starting backend server...
python main.py
if errorlevel 1 (
    echo.
    echo ============================================================
    echo [ERROR] Application failed to launch!
    echo ============================================================
    echo.
    echo Dependencies may be missing or not properly installed.
    echo.
    echo Would you like to execute:
    echo   [1] update.bat - Run this if you have installed before
    echo   [2] first-install.bat - Run this for first-time setup
    echo   [0] Exit
    echo.
    set /p choice="Enter your choice (0, 1, or 2): "
    
    if "%choice%"=="1" (
        cd ..
        call update.bat
    ) else if "%choice%"=="2" (
        cd ..
        call first-install.bat
    ) else (
        echo Exiting...
        cd ..
        exit /b 1
    )
)

cd ..
pause
